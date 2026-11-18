"""The walk-forward search of evo-1 (research/evo-1.md, "The search", "Walk-forward", "Bar 3,
replaced", "Controls"), on the real bars or on a synthetic world (`evo_world`).

One world = the six assets (decisions 1994-02-01 .. 2025-11-09) and the S&P 500 index alone
(decisions 1962-01-02 .. 1993-01-27), the fitness window's two parts. At each fit date `D` (the
first Friday of 1998, 2000, .., 2024) five GP runs (seeds 1000 x year + 0..4, population 500,
30 generations) score rules on every return day before `D` with the fast scorer
(`evo_score.Book`); the 20 best behaviourally different rules of each run are the candidates.
Three selection rules turn the candidates into a walk-forward procedure:

- `evo-top1`: the best candidate by fitness (ties: fewer nodes, then alphabetical);
- `evo-ens10`: down the candidates by fitness, keep a rule whose daily returns on the window
  correlate below 0.95 with every rule kept, up to 10; hold the average of their weights;
- `evo-val`: the previous fit's candidates scored (no node penalty) on the six-asset days
  between the previous fit date and this one; the best trades.

Each procedure trades from its fit date to the day before the next one; the out-of-sample
series runs 2000-01-07 .. 2025-11-09. The replay statistic is its fast-scorer Sharpe minus
`tsmom12`'s in the same world; controls compare with cash and replay the decisions through
`gym.simulate` (the harness, unchanged).

Commands (run from the repo root, `uv run python research/lib/evo_wf.py ...`):

- `timing`: the timing test of the card (no fitness or result is printed), on control world 1.
- `ceilings`: the planted controls' ceilings (`H` through the gym), logged first.
- `baselines noise|plant`: equal weight and `tsmom12` (no search) in the control worlds.
- `control noise SEED` / `control plant K`: one control world through the whole pipeline
  (14 fits; the final fit enters no out-of-sample number), logged as `control` rows
  (`evo-1-control`) in `research/tries.md`.

Scratch output goes to `<cache_root>/derived/evo-1/` (never committed).
"""

from __future__ import annotations

import bisect
import json
import math
import multiprocessing as mp
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from typing import Any

import evo_feat
import evo_gp as gp
import evo_score as es
import evo_world as ew
import harness
import numpy as np
import stats
from harness import Panel, View

SIX_START, SIX_END = date(1994, 2, 1), harness.TRAIN_END
GSPC_START, GSPC_END = date(1962, 1, 2), date(1993, 1, 27)
OOS_START = date(2000, 1, 7)
FIT_YEARS = tuple(range(1998, 2025, 2))
SEEDS = 5
POPULATION, GENERATIONS = 500, 30
CANDIDATES, ENSEMBLE, ENS_CORR = 20, 10, 0.95
MIN_INVESTED = 0.2
PROCS = ("evo-top1", "evo-ens10", "evo-val")
WORKERS = 8  # the lane's cap on parallel processes


def first_friday(year: int) -> date:
    d = date(year, 1, 1)
    return d + timedelta(days=(4 - d.weekday()) % 7)


FIT_DATES = tuple(first_friday(y) for y in FIT_YEARS)


@dataclass
class Prepared:
    """A world's inputs and books, computed once and shared by every run on it."""

    label: str
    hist: dict[str, Any]
    six_panel: Panel
    six_fridays: list[date]
    six_feats: gp.Feats
    six_elig: np.ndarray
    six_book: es.Book
    oos_book: es.Book
    gspc_feats: gp.Feats
    gspc_elig: np.ndarray
    gspc_book: es.Book
    seconds: float = 0.0


def prepare(w: ew.World) -> Prepared:
    t0 = time.process_time()
    six = Panel(w.six)
    six_fr = es.fridays_between(SIX_START, SIX_END)
    f6, e6 = evo_feat.friday_feats(six, six_fr)
    gspc = Panel(w.gspc)
    g_fr = es.fridays_between(GSPC_START, GSPC_END)
    fg, eg = evo_feat.friday_feats(gspc, g_fr)
    return Prepared(
        w.label,
        w.six,
        six,
        six_fr,
        f6,
        e6,
        es.Book(six, six_fr, SIX_START, SIX_END),
        es.Book(six, six_fr, OOS_START, SIX_END),
        fg,
        eg,
        es.Book(gspc, g_fr, GSPC_START, GSPC_END),
        time.process_time() - t0,
    )


def _slice(feats: gp.Feats, t: int) -> gp.Feats:
    return {k: (v if k == "coin" else v[:t]) for k, v in feats.items()}


class Fitness:
    """The card's fitness at one fit date: Sharpe of the index days and the six-asset days
    before `D` as one series, minus 0.01 per node; -inf if under 20% invested on average."""

    def __init__(self, p: Prepared, fit_date: date) -> None:
        self.p, self.fit_date = p, fit_date
        self.t6 = bisect.bisect_left(p.six_fridays, fit_date)
        self.f6, self.e6 = _slice(p.six_feats, self.t6), p.six_elig[: self.t6]
        self.evaluations = 0
        self.behaviours: set[int] = set()

    def weights(self, rule: gp.Rule) -> tuple[np.ndarray, np.ndarray]:
        return gp.weights(rule, self.p.gspc_feats, self.p.gspc_elig), gp.weights(
            rule, self.f6, self.e6
        )

    def daily(self, rule: gp.Rule) -> list[np.ndarray]:
        wg, w6 = self.weights(rule)
        return [self.p.gspc_book.daily(wg), self.p.six_book.daily(w6, before=self.fit_date)]

    def __call__(self, rule: gp.Rule) -> float:
        self.evaluations += 1
        wg, w6 = self.weights(rule)
        sg, ng = self.p.gspc_book.invested(wg)
        s6, n6 = self.p.six_book.invested(w6, before=self.fit_date)
        self.behaviours.add(hash((wg.tobytes(), w6.tobytes())))
        if ng + n6 == 0 or (sg + s6) / (ng + n6) < MIN_INVESTED:
            return -math.inf
        r = [self.p.gspc_book.daily(wg), self.p.six_book.daily(w6, before=self.fit_date)]
        return es.sharpe_of(r) - gp.NODE_PENALTY * gp.size(rule[1])


_P: Prepared | None = None  # the world a worker process searches (set before forking)


def run_one(task: tuple[int, int]) -> dict[str, Any]:
    """One GP run: fit year, seed offset. Returns its candidates and counts."""
    year, k = task
    assert _P is not None
    t0 = time.process_time()
    fit = Fitness(_P, first_friday(year))
    scored = gp.evolve(fit, 1000 * year + k, POPULATION, GENERATIONS)
    cands: list[tuple[gp.Rule, float]] = []
    seen: set[bytes] = set()
    for rule in gp.order(scored):
        if len(cands) == CANDIDATES or scored[rule] == -math.inf:
            break
        key = fit.weights(rule)[1].tobytes()
        if key not in seen:
            seen.add(key)
            cands.append((rule, scored[rule]))
    return {
        "year": year,
        "seed": 1000 * year + k,
        "candidates": cands,
        "evaluations": fit.evaluations,
        "formulas": len(scored),
        "behaviours": sorted(fit.behaviours),
        "cpu": time.process_time() - t0,
    }


def search(p: Prepared, workers: int = WORKERS) -> list[dict[str, Any]]:
    """All GP runs of the walk-forward on one world (largest windows first)."""
    global _P
    _P = p
    tasks = [(y, k) for y in reversed(FIT_YEARS) for k in range(SEEDS)]
    if workers <= 1:
        return [run_one(t) for t in tasks]
    with mp.get_context("fork").Pool(workers) as pool:
        return list(pool.imap_unordered(run_one, tasks))


# --- selection and the out-of-sample series ---


@dataclass
class Procedure:
    name: str
    chosen: dict[int, list[gp.Rule]] = field(default_factory=dict)  # fit year -> rule(s)
    weights: np.ndarray | None = None  # six-asset Friday rows, out of sample


def _candidates(p: Prepared, runs: Sequence[dict[str, Any]], year: int) -> list[gp.Rule]:
    """The fit's candidates over its five runs, behaviourally different, best first."""
    fit = Fitness(p, first_friday(year))
    merged: dict[gp.Rule, float] = {}
    for r in runs:
        if r["year"] == year:
            merged.update(dict(r["candidates"]))
    out, seen = [], set()
    for rule in gp.order(merged):
        key = fit.weights(rule)[1].tobytes()
        if key not in seen:
            seen.add(key)
            out.append(rule)
    return out


def _ensemble(p: Prepared, year: int, cands: list[gp.Rule]) -> list[gp.Rule]:
    fit = Fitness(p, first_friday(year))
    kept: list[gp.Rule] = []
    series: list[np.ndarray] = []
    for rule in cands:
        r = np.concatenate(fit.daily(rule))
        if r.std() == 0:
            continue
        if all(np.corrcoef(r, q)[0, 1] < ENS_CORR for q in series):
            kept.append(rule)
            series.append(r)
        if len(kept) == ENSEMBLE:
            break
    return kept or cands[:1]


def _validate(p: Prepared, prev_year: int, year: int, cands: list[gp.Rule]) -> gp.Rule:
    a, b = first_friday(prev_year), first_friday(year)
    i, j = p.six_book.day_index(a), p.six_book.day_index(b)
    scores = {}
    for rule in cands:
        w = gp.weights(rule, p.six_feats, p.six_elig)
        scores[rule] = stats.sharpe(p.six_book.daily(w, before=b)[i:j])
    return gp.order(scores)[0]


def select(p: Prepared, runs: Sequence[dict[str, Any]]) -> dict[str, Procedure]:
    cands = {y: _candidates(p, runs, y) for y in FIT_YEARS}
    procs = {n: Procedure(n) for n in PROCS}
    for i, y in enumerate(FIT_YEARS):
        if not cands[y]:
            raise RuntimeError(f"{p.label}: no valid candidate at the {y} fit")
        procs["evo-top1"].chosen[y] = [cands[y][0]]
        procs["evo-ens10"].chosen[y] = _ensemble(p, y, cands[y])
        if i:
            prev = FIT_YEARS[i - 1]
            procs["evo-val"].chosen[y] = [_validate(p, prev, y, cands[prev])]
    for proc in procs.values():
        proc.weights = oos_weights(p, proc.chosen)
    return procs


def oos_weights(p: Prepared, chosen: dict[int, list[gp.Rule]]) -> np.ndarray:
    """Six-asset Friday rows: each traded fit's choice from its fit date to the next one."""
    w = np.zeros(p.six_elig.shape)
    traded = [y for y in FIT_YEARS if first_friday(y) >= OOS_START]
    for n, y in enumerate(traded):
        a = bisect.bisect_left(p.six_fridays, first_friday(y))
        nxt = first_friday(traded[n + 1]) if n + 1 < len(traded) else None
        b = bisect.bisect_left(p.six_fridays, nxt) if nxt else len(p.six_fridays)
        rules = chosen[y]
        ws = np.mean([gp.weights(r, p.six_feats, p.six_elig) for r in rules], axis=0)
        w[a:b] = ws[a:b]
    return w


def lookup(fridays: list[date], w: np.ndarray, syms: list[str]) -> harness.ResearchStrategy:
    """A weight matrix as a daily research strategy, mapped to Fridays like `common.weekly`."""
    row = {f: i for i, f in enumerate(fridays)}

    def strategy(view: View) -> dict[str, float]:
        f = view.today - timedelta(days=(view.today.weekday() - 4) % 7)
        if f not in row:
            return {}
        i = row[f]
        return {s: float(w[i, j]) for j, s in enumerate(syms) if w[i, j] > 0}

    return strategy


def gym_run(p: Prepared, idea: str, variant: str, w: np.ndarray) -> harness.Run:
    """Replay a weight matrix through `gym.simulate` (the harness), not logged."""
    strat = lookup(p.six_fridays, w, p.six_panel.syms)
    return harness.run(
        idea, variant, strat, kind="robustness", panel=p.six_panel, history=p.hist,
        start=OOS_START, end=SIX_END, log=False,
    )  # fmt: skip


# --- commands ---


def scratch() -> Any:
    import macro

    d = macro.cache_root() / "derived" / "evo-1"
    d.mkdir(parents=True, exist_ok=True)
    return d


def timing() -> None:
    """The card's timing test: CPU seconds of one GP run at the first and last fit (no fitness
    printed), extrapolated to every search of the plan."""
    real = ew.load_real()
    t0 = time.process_time()
    p = prepare(ew.world(real, "shuffle", 1))
    prep = time.process_time() - t0
    global _P
    _P = p
    out = {}
    for y in (FIT_YEARS[0], FIT_YEARS[-1]):
        r = run_one((y, 0))
        out[y] = r
        print(f"fit {y}: {r['cpu']:.1f} CPU s, {r['evaluations']} evaluations", flush=True)
    days = {y: p.six_book.day_index(first_friday(y)) for y in FIT_YEARS}
    y0, y1 = FIT_YEARS[0], FIT_YEARS[-1]
    slope = (out[y1]["cpu"] - out[y0]["cpu"]) / (days[y1] - days[y0])
    per_run = {y: out[y0]["cpu"] + slope * (days[y] - days[y0]) for y in FIT_YEARS}
    final = out[y0]["cpu"] + slope * (p.six_book.days - days[y0])
    search_14 = SEEDS * sum(per_run.values())
    t1 = time.process_time()
    gym_run(p, "timing", "tsmom12", gp.weights(gp.TSMOM12, p.six_feats, p.six_elig))
    gym_s = time.process_time() - t1
    world_s = prep + 3 * gym_s  # inputs + three gym replays per world
    print(f"inputs per world: {prep:.0f} CPU s; one gym replay {gym_s:.1f} CPU s")
    print(f"one walk-forward search (14 fits x {SEEDS} seeds): {search_14 / 3600:.2f} CPU h")
    print(f"final fit ({SEEDS} seeds): {SEEDS * final / 3600:.2f} CPU h")
    real_h = (search_14 + SEEDS * final + world_s) / 3600
    world_h = (search_14 + world_s) / 3600
    for n in (20, 40):
        total = real_h + 6 * world_h + n * world_h
        print(f"plan with {n} replays: real {real_h:.1f} + 6 controls + {n} replays "
              f"= {total:.1f} CPU h (re-evolved runs not included)")  # fmt: skip
    path = scratch() / "timing.json"
    path.write_text(
        json.dumps(
            {
                "when": datetime.now(UTC).isoformat(timespec="minutes"),
                "prep_s": prep,
                "run_s": {str(y): out[y]["cpu"] for y in out},
                "evaluations": {str(y): out[y]["evaluations"] for y in out},
                "search_h": search_14 / 3600,
                "real_h": real_h,
                "world_h": world_h,
            },
            indent=1,
        )
    )


def _log_control(run: harness.Run, variant: str) -> None:
    run.idea, run.variant = "evo-1-control", variant
    harness._log(run, "control", OOS_START, SIX_END)


def control(kind: str, arg: str) -> None:
    """One control world through the whole pipeline (benchmark: cash)."""
    real = ew.load_real()
    base = ew.world(real, "shuffle", int(arg) if kind == "noise" else 1)
    w = base if kind == "noise" else ew.plant(base, float(arg))
    t0 = time.time()
    p = prepare(w)
    print(f"{w.label}: inputs in {p.seconds:.0f} CPU s", flush=True)
    ceiling = None
    if kind == "plant":
        wh = gp.weights(ew.H_RULE, p.six_feats, p.six_elig)
        ceiling = gym_run(p, "evo-1-control", "H", wh)
        sh = stats.sharpe(ceiling.rets)
        print(f"ceiling (H through the gym, no search): Sharpe {sh:.2f}", flush=True)
    runs = search(p)
    cpu = sum(r["cpu"] for r in runs)
    evals = sum(r["evaluations"] for r in runs)
    formulas = sum(r["formulas"] for r in runs)
    behaviours = len({b for r in runs for b in r["behaviours"]})
    procs = select(p, runs)
    lines = []
    p_min = 1.0
    res: dict[str, Any] = {}
    for name, proc in procs.items():
        assert proc.weights is not None
        g = gym_run(p, "evo-1-control", name, proc.weights)
        rets = g.rets
        fast = p.oos_book.daily(proc.weights)
        d, pv, _, _ = stats.sharpe_diff_boot(rets, np.zeros_like(rets), seed=0)
        p_min = min(p_min, pv)
        extra = ""
        if ceiling is not None:
            wh = gp.weights(ew.H_RULE, p.six_feats, p.six_elig)
            rows = slice(bisect.bisect_left(p.six_fridays, OOS_START), None)
            corr = float(np.corrcoef(proc.weights[rows].ravel(), wh[rows].ravel())[0, 1])
            extra = f"; weights corr to H {corr:.2f}; ceiling {stats.sharpe(ceiling.rets):.2f}"
        sharpe = stats.sharpe(rets)
        found = sharpe > 0 and pv < 0.10
        if ceiling is not None:
            found = found and sharpe >= 0.5 * stats.sharpe(ceiling.rets)
        extra += "; FOUND" if found else "; not found"
        res[name] = {
            "found": found,
            "gym_sharpe": sharpe,
            "fast_sharpe": stats.sharpe(fast),
            "p": pv,
            "rules": {y: [gp.show_rule(r) for r in rs] for y, rs in proc.chosen.items()},
        }
        lines.append(f"{name}: gym Sharpe {stats.sharpe(rets):.2f} (fast {stats.sharpe(fast):.2f})"
                     f", bootstrap p {pv:.3f}{extra}")  # fmt: skip
        _log_control(
            g,
            f"{w.label}: {name}, walk-forward 2000-2025 ({evals} evaluations, {formulas} "
            f"formulas, {behaviours} behaviours; bootstrap p vs cash {pv:.3f}{extra})",
        )
    for line in lines:
        print(line, flush=True)
    print(f"smallest p x 3 = {min(1.0, 3 * p_min):.3f}; CPU {cpu / 3600:.2f} h, "
          f"wall {(time.time() - t0) / 60:.0f} min", flush=True)  # fmt: skip
    name = w.label.replace(" ", "-").replace("=", "")
    (scratch() / f"control-{name}.json").write_text(
        json.dumps(
            {
                "label": w.label,
                "procedures": res,
                "p_min_x3": min(1.0, 3 * p_min),
                "ceiling_sharpe": stats.sharpe(ceiling.rets) if ceiling else None,
                "cpu_h": cpu / 3600,
                "evaluations": evals,
                "formulas": formulas,
                "behaviours": behaviours,
                "runs": [{k: v for k, v in r.items() if k != "behaviours"} for r in runs],
            },
            indent=1,
            default=str,
        )
    )


PLANTS = (0.01, 0.02, 0.04)


def ceilings() -> None:
    """The planted controls' ceilings (`H` itself through the gym, no search), logged before
    any planted search result exists."""
    base = ew.world(ew.load_real(), "shuffle", 1)
    for k in PLANTS:
        w = ew.plant(base, k)
        p = prepare(w)
        run = gym_run(p, "evo-1-control", "H", gp.weights(ew.H_RULE, p.six_feats, p.six_elig))
        print(f"{w.label}: ceiling Sharpe {stats.sharpe(run.rets):.2f}", flush=True)
        _log_control(run, f"{w.label}: ceiling, H itself through the gym, no search")


EQUAL: gp.Rule = ("slot", ("const", 1.0))  # every eligible asset's equal slot: equal weight


def world_baselines(which: str) -> None:
    """Context for the controls (added after the first control runs, 2026-11-18): plain rules
    with no search in the three noise worlds and the three planted ones. A zero log-drift
    world still pays a long holder about half the variance a day in simple returns, so
    holding is not exactly cash there."""
    real = ew.load_real()
    noise = [ew.world(real, "shuffle", seed) for seed in (1, 2, 3)]
    worlds = noise if which == "noise" else [ew.plant(noise[0], k) for k in PLANTS]
    for w in worlds:
        p = prepare(w)
        for name, rule in (("equal weight", EQUAL), ("tsmom12", gp.TSMOM12)):
            run = gym_run(p, "evo-1-control", name, gp.weights(rule, p.six_feats, p.six_elig))
            pv = stats.sharpe_diff_boot(run.rets, np.zeros_like(run.rets), seed=0)[1]
            print(f"{p.label}: {name} Sharpe {stats.sharpe(run.rets):.2f}, p {pv:.3f}")
            _log_control(run, f"{p.label}: {name}, no search (world context; p vs cash {pv:.3f})")


def main(argv: Sequence[str]) -> None:
    if argv[:1] == ["timing"]:
        timing()
    elif argv[:1] == ["ceilings"]:
        ceilings()
    elif argv[:1] == ["baselines"] and argv[1:] in (["noise"], ["plant"]):
        world_baselines(argv[1])
    elif argv[:1] == ["control"] and len(argv) == 3 and argv[1] in ("noise", "plant"):
        control(argv[1], argv[2])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
