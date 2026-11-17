"""deep-1, Part B: run the three combination rules through the gym and judge them.

    uv run --with numpy python research/lib/deep1_combo.py            # the test (logs tries)
    uv run --with numpy --with scikit-learn --with numba python research/lib/deep1_combo.py check

Needs the sleeve series from `deep1_models.py` on six, etf, coin and idx. The rules are in
`deep1_mix.py`, the card and its pass bar in research/deep-1.md. `DRY=1`: nothing is logged and
the result goes to a `.dry.md` file. `check` recomputes the books' weights on six days from
history cut off at each day (no look-ahead) and logs nothing.
"""

from __future__ import annotations

import csv
import math
import pickle
import sys
from dataclasses import dataclass
from datetime import date

import common as c
import deep1_mix as mix
import deep1_models as dm
import harness
import numpy as np
import stats

from grimstrade import gym, report
from grimstrade.data import UNIVERSE, close_time

RULES = ("stack", "switch", "meta")
SINCE = date(2003, 1, 1)
P_BAR = 0.10 / 3
SETS = {"etf": "8 other ETFs", "coin": "6 other coins", "idx": "4 indexes as one portfolio"}
CHECK_DAYS = [date(1999, 6, 15), date(2003, 3, 14), date(2009, 1, 2), date(2015, 8, 24),
              date(2020, 3, 20), date(2025, 1, 3)]  # fmt: skip


@dataclass
class Books:
    names: list[str]  # sleeves; names[0] is tsmom12
    series: list[dm.Series]
    plan: mix.Plan
    weights: dict[str, np.ndarray]  # rule -> days x assets target weights

    @property
    def days(self) -> np.ndarray:
        return self.series[0].days


def combine(series: list[dm.Series]) -> Books:
    """The three books from the sleeves' saved series (sleeve 0 is `tsmom12`)."""
    r = np.column_stack([s.rets for s in series])
    w = np.stack([s.w for s in series])  # sleeves x days x assets
    p = mix.plan(series[0].days, r, w[0].sum(axis=1), 0, list(range(1, len(series))))
    n = r.shape[0]
    books = {
        "stack": np.einsum("dm,mda->da", p.stack, w),
        "switch": w[p.switch, np.arange(n)],
        "meta": np.einsum("dm,mda->da", p.meta, w),
    }
    return Books([s.name for s in series], series, p, books)


def load_books(universe: str, skip: tuple[str, ...] = ()) -> Books:
    names = ["tsmom12"] + [m.name for m in dm.pool_for(universe) if m.name not in skip]
    return combine([dm.load(universe, nm) for nm in names])


def replay(idea: str, variant: str, w: np.ndarray, u: c.Ctx, days: np.ndarray, kind: str) -> c.Run:
    """Target weights through `gym.simulate`, scored and logged like `harness.run`."""
    syms = u.panel.syms
    tag = variant if u.name == "six" else f"{variant}@{u.name}"
    done = dm.OUT / "runs" / f"{idea}.{tag}.pkl"  # a logged run is never replayed a second time
    if done.exists() and not c.DRY:
        with done.open("rb") as f:
            old: c.Run = pickle.load(f)  # noqa: S301 (our own file)
        return old
    decs = [
        gym.Decision(
            harness.decide_time(date.fromordinal(int(days[k]))),
            harness.clean({s: float(x) for s, x in zip(syms, w[k], strict=True)}),
        )
        for k in range(len(w))
    ]
    res = gym.simulate(decs, u.hist)
    cal, eq = harness._calendar(res.equity)
    run = c.Run(idea, tag, "train", report.score(f"{idea}/{tag}", res), cal, eq,
                float(np.mean([sum(d.weights.values()) for d in decs])), decs)  # fmt: skip
    if not c.DRY:
        harness._log(run, kind, u.start, u.end)
        path = harness.DATA / "runs" / idea / f"{tag}.train.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as f:
            wr = csv.writer(f, lineterminator="\n")
            wr.writerow(["date", "equity"])
            wr.writerows((d.isoformat(), repr(float(e))) for d, e in zip(cal, eq, strict=True))
        done.parent.mkdir(parents=True, exist_ok=True)
        with done.open("wb") as f:
            pickle.dump(run, f)
    return run


def run_books(universe: str, kind: str) -> tuple[c.Ctx, Books, dict[str, c.Run], c.Run, c.Run]:
    u = c.ctx(universe)
    b = load_books(universe)
    runs = {r: replay(f"deep-1-{r}", r, b.weights[r], u, b.days, kind) for r in RULES}
    twin = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), u, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), u, "baseline", log=False)
    return u, b, runs, twin, ew


# --- reporting ---


def since(run: c.Run, a: date = SINCE) -> np.ndarray:
    return run.rets_between(a, run.days[-1])


def window_table(runs: list[c.Run], twin: c.Run, ew: c.Run) -> list[str]:
    out = ["| Variant | Sharpe | CAGR | Max DD | vs tsmom12 (p) | vs equal weight (p) |",
           "|---|---:|---:|---:|---:|---:|"]  # fmt: skip
    for r in runs:
        x = since(r)
        cells = []
        for other in (twin, ew):
            if r is other:
                cells.append("-")
            else:
                d, p, _, _ = stats.sharpe_diff_boot(x, since(other))
                cells.append(f"{d:+.2f} ({p:.2f})")
        out.append(f"| {r.variant} | {stats.sharpe(x):.2f} | {stats.cagr(x):+.1%} | "
                   f"{stats.max_drawdown(x):.1%} | {cells[0]} | {cells[1]} |")  # fmt: skip
    return out


def distance(b: Books, rule: str) -> float:
    """Average share of the book held differently from `tsmom12` (half the sum of |gaps|)."""
    return float(np.abs(b.weights[rule] - b.series[0].w).sum(axis=1).mean() / 2)


def choices(b: Books) -> list[str]:
    out = ["| Refit | `stack`: complement (share of `tsmom12`) | `switch`: off / mixed / on | "
           "`meta`: largest shares (lambda) |", "|---|---|---|---|"]  # fmt: skip
    for e in b.plan.log:
        k = int(e["k"])  # type: ignore[call-overload]
        comp = e["stack"]
        st = f"{b.names[comp]} ({e['share']:.0%})" if comp is not None else "none"  # type: ignore[call-overload]
        sw = " / ".join(b.names[i] for i in e["switch"])  # type: ignore[attr-defined]
        sh: np.ndarray = e["meta"]  # type: ignore[assignment]
        top = ", ".join(f"{b.names[i]} {sh[i]:.0%}" for i in np.argsort(-sh)[:4] if sh[i] > 0.005)
        lam = e["lam"]
        lam_txt = "-" if isinstance(lam, float) and math.isnan(lam) else f"{lam:g}"
        out.append(f"| {date.fromordinal(int(b.days[k]))} | {st} | {sw} | {top} ({lam_txt}) |")
    return out


def main() -> None:
    out = ["# deep-1, Part B: three combination rules", ""]
    out += ["Card and pass bar: `deep-1.md`. Twin: `tsmom12`. Train period, total-return prices, "
            "gym costs. The sleeves are the 29 pool models of the card; every choice is made by "
            "the rule from past returns, refitted each first Friday of January.", ""]  # fmt: skip
    six, b, runs, twin, ew = run_books("six", "variant")
    rs = [runs[r] for r in RULES]
    out += ["## The six live assets, 1994-2025", "", c.table([*rs, twin, ew], versus=twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table([*rs, twin, ew]), ""]
    out += ["## Since 2003 (the review's window)", "", *window_table([*rs, twin, ew], twin, ew), ""]
    out += ["## How far each book is from `tsmom12`", ""]
    out += [f"- `{r}`: on average {distance(b, r):.1%} of the book is held differently from "
            f"`tsmom12`; average invested {runs[r].exposure:.0%} (`tsmom12` {twin.exposure:.0%})."
            for r in RULES]  # fmt: skip
    best = max(b.series[1:], key=lambda s: stats.sharpe(s.rets[~np.isnan(s.rets)]))
    bs = stats.sharpe(best.rets[~np.isnan(best.rets)])
    out += ["", f"Best single pool model with hindsight: `{best.name}`, Sharpe {bs:.2f} over its "
            f"own span (`tsmom12` {stats.sharpe(twin.rets):.2f}).", ""]  # fmt: skip
    out += ["## What each refit chose (six assets)", "", *choices(b), ""]

    signs: dict[str, dict[str, float]] = {r: {} for r in RULES}
    for name, title in SETS.items():
        u, bu, ru, tu, eu = run_books(name, "robustness")
        rr = [ru[r] for r in RULES]
        out += [f"## Out of universe: {title}, from {u.start}", "",
                c.table([*rr, tu, eu], versus=tu), ""]  # fmt: skip
        out += [f"Sleeves: {len(bu.names) - 1} complements. Distance from `tsmom12`: " +
                ", ".join(f"`{r}` {distance(bu, r):.1%}" for r in RULES) + ".", ""]  # fmt: skip
        for r in RULES:
            x, y = c.align(ru[r], tu)
            signs[r][name] = stats.sharpe(x) - stats.sharpe(y)

    out += ["## Pass bar", ""]
    for r in RULES:
        run = runs[r]
        x, y = c.align(run, twin)
        diff, pval, _, _ = stats.sharpe_diff_boot(x, y)
        ep, et = c.era_sharpes(run), c.era_sharpes(twin)
        both = [n for n in ep if not (math.isnan(ep[n]) or math.isnan(et[n]))]
        ahead = sum(ep[n] > et[n] for n in both)
        dp, dt, de = c.describe(run), c.describe(twin), c.describe(ew)
        same = sum(1 for v in signs[r].values() if v > 0)
        s_r, s_t, s_e = (stats.sharpe(since(z)) for z in (run, twin, ew))
        bars = [
            (f"1. Sharpe beats `tsmom12` with p < {P_BAR:.3f}", diff > 0 and pval < P_BAR,
             f"difference {diff:+.2f}, p = {pval:.2f}"),
            ("2. Ahead of `tsmom12` in at least 4 of 5 eras", ahead >= 4,
             f"{ahead} of {len(both)}"),
            ("3. Max drawdown not more than 5 points worse", dp["mdd"] <= dt["mdd"] + 0.05,
             f"{dp['mdd']:.1%} vs {dt['mdd']:.1%}"),
            ("4. Ahead of `tsmom12` out of universe in at least 2 of 3 sets",
             diff > 0 and same >= 2, ", ".join(f"{k} {v:+.2f}" for k, v in signs[r].items())),
            ("5. Beats equal weight on Sharpe", dp["sharpe"] > de["sharpe"],
             f"{dp['sharpe']:.2f} vs {de['sharpe']:.2f}"),
            ("6. Since 2003 not behind `tsmom12` nor equal weight", s_r >= s_t and s_r >= s_e,
             f"{s_r:.2f} vs {s_t:.2f} and {s_e:.2f}"),
        ]  # fmt: skip
        ok = all(x for _, x, _ in bars)
        out += [f"### `{r}`", ""]
        out += [f"- {'PASS' if good else 'FAIL'}: {text} ({detail})" for text, good, detail in bars]
        out += ["", f"**`{r}` {'PASSES' if ok else 'FAILS'} train.**", ""]
    c.write_result("deep-1", "\n".join(out))


# --- look-ahead check ---


def truncated(u: c.Ctx, d: date) -> c.Ctx:
    """The universe as a decision on day `d` sees it: only bars closed by then."""
    t = harness.decide_time(d)
    hist = {s: [x for x in bars if close_time(UNIVERSE[s], x.date) <= t]
            for s, bars in u.hist.items()}  # fmt: skip
    return c.Ctx(u.name, u.period, hist, harness.Panel(hist), u.start, d)


def check() -> None:
    skip = ("gbm-wk",)  # needs its own process (ML_HORIZON=7); left out on both sides
    u = c.ctx("six")
    full = load_books("six", skip)
    for d in CHECK_DAYS:
        u2 = truncated(u, d)
        series = []
        for nm in full.names:
            m = dm.BY_NAME[nm]
            start = m.first(u2) if m.first else u2.start
            run = c.go(m.idea, m.variant, m.make(u2), u2, "robustness", log=False, start=start)
            series.append(dm.to_series(run, u2, nm))
        cut = combine(series)
        k = d.toordinal() - int(full.days[0])
        for r in RULES:
            a, b = full.weights[r][k], cut.weights[r][k]
            if not np.allclose(a, b, atol=1e-9):
                raise AssertionError(f"{d} {r}: full {a} != truncated {b}")
        print(f"{d}: stack, switch and meta give the same weights from truncated history",
              flush=True)  # fmt: skip
    print("look-ahead check passed")


if __name__ == "__main__":
    check() if sys.argv[1:] == ["check"] else main()
