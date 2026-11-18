"""The one real search of evo-1 (research/evo-1.md), on train data only, and its pass bar.

`uv run python research/lib/evo_real.py SETTING` (the setting chosen and confirmed under the
card note "Lead's decision 2"). Needs the 40 `evo-1-replay` rows of that setting in
`research/tries.md` (bar 3). Logs one `variant` row per procedure on the six assets, one per
procedure and out-of-universe set (`@etf`, `@coin`, `@idx`), and one `search` row. The
held-out year is never loaded here.

Bars (card, "Pass bar"; bar 3 as replaced and tightened by the card notes):
1. Out of sample 2000-01-07 .. 2025-11-09 through the gym: Sharpe ahead of `tsmom12` with
   bootstrap p x 3 < 0.10; ahead in at least 3 of the 4 eras; max drawdown at most 5 points
   worse; Sharpe ahead of equal weight.
2. Not behind `tsmom12` on Sharpe from 2003-01-01.
3. At most one of the 40 replay scores at or above the real statistic (fast scorer).
4. Transfer: the very rules chosen, fit by fit, ahead of `tsmom12` in at least 2 of 3 sets.
5. The confirmation noise control found in fewer than 2 of 3 worlds (it was 0 of 3, or the
   search would not have run).
"""

from __future__ import annotations

import bisect
import fcntl
import json
import math
import re
import sys
from collections.abc import Sequence
from datetime import UTC, date, datetime
from typing import Any

import common
import evo_feat
import evo_gp as gp
import evo_score as es
import evo_wf as wf
import evo_world as ew
import harness
import numpy as np
import stats

ERAS_OOS = ("2000-09", "2010-16", "2017-21", "2022-25")
REPLAYS = 40


def replay_scores(setting: str) -> list[float]:
    """The replay worlds' scores of this setting, from `tries.md`."""
    tag = f"[setting {setting}:"
    out = {}
    for line in harness.TRIES.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 8 and cells[1] == "evo-1-replay" and tag in cells[2]:
            seed = int(re.match(r"block (\d+)", cells[2]).group(1))  # type: ignore[union-attr]
            out[seed] = float(cells[7])
    return [out[s] for s in sorted(out)]


def run_weights(
    c: common.Ctx, fridays: list[date], w: np.ndarray, idea: str, variant: str, log: bool
) -> harness.Run:
    strat = wf.lookup(fridays, w, c.panel.syms)
    start = max(wf.OOS_START, c.start)
    return harness.run(
        idea, variant, strat, kind="variant", panel=c.panel, history=c.hist,
        start=start, end=c.end, log=log,
    )  # fmt: skip


def chosen_weights(
    chosen: dict[int, list[gp.Rule]], fridays: list[date], feats: gp.Feats, elig: np.ndarray
) -> np.ndarray:
    """The procedure's rules fit by fit on any asset set (rows: that set's Fridays)."""
    w = np.zeros(elig.shape)
    traded = [y for y in wf.FIT_YEARS if wf.first_friday(y) >= wf.OOS_START]
    for n, y in enumerate(traded):
        a = bisect.bisect_left(fridays, wf.first_friday(y))
        nxt = wf.first_friday(traded[n + 1]) if n + 1 < len(traded) else None
        b = bisect.bisect_left(fridays, nxt) if nxt else len(fridays)
        if b <= a:
            continue
        ws = np.mean([gp.weights(r, feats, elig) for r in chosen[y]], axis=0)
        w[a:b] = ws[a:b]
    return w


def mdd(run: harness.Run) -> float:
    return float(stats.max_drawdown(run.rets))


def main(argv: Sequence[str]) -> None:
    setting = argv[0]
    wf.use(setting)
    replays = replay_scores(setting)
    if len(replays) != REPLAYS:
        raise SystemExit(f"need {REPLAYS} replay rows of setting {setting}, have {len(replays)}")
    real = ew.load_real()
    p = wf.prepare(real)
    runs = wf.search(p, final=True)
    walk = [r for r in runs if r["year"] != wf.FINAL_YEAR]
    procs = wf.select(p, walk)
    final = wf._candidates(p, runs, wf.FINAL_YEAR)
    stat = wf.replay_stats(p, procs)
    evals = sum(r["evaluations"] for r in runs)
    behaviours = len({b for r in runs for b in r["behaviours"]})
    with harness.TRIES.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(
            f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | evo-1 | GP search [{wf.setting_text()}]: "
            f"{evals} rule evaluations ({evals} different formulas, {behaviours} different "
            f"behaviours) over 15 fits x {wf.SEEDS} seeds | search | train | 1962-01-02 | "
            f"{wf.SIX_END} | - | - | - | - |\n"
        )

    six = common.ctx("six")
    tsmom = wf.oos_weights(p, {y: [gp.TSMOM12] for y in wf.FIT_YEARS})
    bench = run_weights(six, p.six_fridays, tsmom, "evo-1", "tsmom12", False)
    eq_w = gp.weights(wf.EQUAL, p.six_feats, p.six_elig)
    rows = slice(bisect.bisect_left(p.six_fridays, wf.OOS_START), None)
    eq_full = np.zeros_like(eq_w)
    eq_full[rows] = eq_w[rows]
    equal = run_weights(six, p.six_fridays, eq_full, "evo-1", "equal-weight", False)
    b_es = common.era_sharpes(bench)

    sets = {}
    for name in ("etf", "coin", "idx"):
        c = common.ctx(name)
        fr = es.fridays_between(c.start, c.end)
        feats, elig = evo_feat.friday_feats(c.panel, fr)
        sets[name] = (c, fr, feats, elig)

    out: dict[str, Any] = {"setting": setting, "replays": replays, "stat": stat, "procs": {}}
    for name, proc in procs.items():
        assert proc.weights is not None
        run = run_weights(six, p.six_fridays, proc.weights, "evo-1", name, True)
        d, pv, _, _ = stats.sharpe_diff_boot(run.rets, bench.rets, seed=0)
        r_es = common.era_sharpes(run)
        eras_ahead = sum(r_es[e] > b_es[e] for e in ERAS_OOS)
        late = stats.sharpe(run.rets_between(date(2003, 1, 1), wf.SIX_END)) - stats.sharpe(
            bench.rets_between(date(2003, 1, 1), wf.SIX_END)
        )
        dd_gap = mdd(run) - mdd(bench)
        vs_eq = stats.sharpe(run.rets) - stats.sharpe(equal.rets)
        at_or_above = sum(x >= stat[name] for x in replays)
        transfer = {}
        for sname, (c, fr, feats, elig) in sets.items():
            wt = chosen_weights(proc.chosen, fr, feats, elig)
            rt = run_weights(c, fr, wt, "evo-1", name, True)
            wb = chosen_weights({y: [gp.TSMOM12] for y in wf.FIT_YEARS}, fr, feats, elig)
            rb = run_weights(c, fr, wb, "evo-1", "tsmom12", False)
            transfer[sname] = stats.sharpe(rt.rets) - stats.sharpe(rb.rets)
        bars = {
            "1": d > 0 and 3 * pv < 0.10 and eras_ahead >= 3 and dd_gap <= 0.05 and vs_eq > 0,
            "2": late >= 0,
            "3": at_or_above <= 1,
            "4": sum(x > 0 for x in transfer.values()) >= 2,
            "5": True,
        }
        out["procs"][name] = {
            "sharpe": stats.sharpe(run.rets),
            "tsmom12": stats.sharpe(bench.rets),
            "diff": d,
            "p_x3": min(1.0, 3 * pv),
            "eras": r_es,
            "eras_ahead": eras_ahead,
            "from_2003": late,
            "mdd_gap": dd_gap,
            "vs_equal_weight": vs_eq,
            "replay_stat": stat[name],
            "replays_at_or_above": at_or_above,
            "transfer": transfer,
            "bars": bars,
            "pass": all(bars.values()),
            "rules": {y: [gp.show_rule(r) for r in rs] for y, rs in proc.chosen.items()},
        }
        print(json.dumps({name: out["procs"][name]}, default=str), flush=True)
    out["final_fit_top5"] = [gp.show_rule(r) for r in final[:5]]
    out["tsmom12_eras"] = b_es
    out["equal_weight"] = stats.sharpe(equal.rets)
    (wf.scratch() / f"real-{setting}.json").write_text(json.dumps(out, indent=1, default=str))
    verdict = [n for n, v in out["procs"].items() if v["pass"]]
    print(f"passing procedures: {verdict or 'none'}", flush=True)
    if any(math.isnan(x) for x in b_es.values()):
        print("note: an era has no tsmom12 Sharpe", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
