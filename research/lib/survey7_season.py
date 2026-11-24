"""Lane survey-7: event-study gate for `seasonal-20y` (research/survey-7.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The rule was pushed before
this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).

Run: `uv run python -I research/lib/survey7_season.py`  (DRY=1: counts only)
Output: research/results/seasonal-20y.md
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import survey7_events as ev  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "seasonal-20y.md"
DRY = bool(os.environ.get("DRY"))

LIVE = ["SPY", "QQQ", "TLT", "GLD", "BTC", "ETH"]
ETFS = [
    "DBC", "EEM", "EFA", "IEF", "IWM", "LQD", "SLV", "VNQ",
    "XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY",
]  # fmt: skip
UNIV = LIVE + ETFS
FIRST: ev.Month = (1994, 1)
POST = ((2017, 1), (2025, 10))
LAST: ev.Month = POST[1]

Series = dict[ev.Month, float]


def load() -> tuple[dict[str, Series], dict[str, Series]]:
    """Per asset: calendar-month returns and Friday-clock holding returns, months <= LAST."""
    hist = harness.load_history("train", syms=UNIV)
    mret: dict[str, Series] = {}
    fret: dict[str, Series] = {}
    for s in UNIV:
        bars = hist[s]
        days = [b.date for b in bars]
        logc = [math.log(b.close) for b in bars]
        mret[s] = {m: v for m, v in ev.month_returns(days, logc).items() if m <= LAST}
        fret[s] = {
            m: r
            for m in ev.months(FIRST, LAST)
            if math.isfinite(r := ev.friday_return(days, logc, m))
        }
    return mret, fret


def series(
    mret: dict[str, Series],
    hold: dict[str, Series],
    syms: list[str],
    span: tuple[ev.Month, ev.Month],
    s: int = 0,
    a: int = 0,
) -> tuple[list[float], list[int], list[int]]:
    """y(M) over the months of `span` (NaN where n < MIN_N), the n per month and the years
    used per (asset, month) with a signal. The true and every placebo series come from here."""
    ys, ns, yrs = [], [], []
    for m in ev.months(*span):
        sig, ret = {}, {}
        for x in syms:
            v, used = ev.signal(mret[x], m, s, a)
            if math.isfinite(v) and m in hold[x]:
                sig[x], ret[x] = v, hold[x][m]
                yrs.append(used)
        y, n = ev.spread(sig, ret)
        ys.append(y)
        ns.append(n)
    return ys, ns, yrs


def first_month(mret: dict[str, Series], hold: dict[str, Series]) -> ev.Month:
    ys, _, _ = series(mret, hold, UNIV, (FIRST, (2016, 12)))
    i = next(i for i, y in enumerate(ys) if math.isfinite(y))
    return ev.months(FIRST, (2016, 12))[i]


def cell(ys: list[float]) -> str:
    m, t, n = ev.mean_t(ys)
    return f"{m * 100:+.2f}% | {t:+.2f} | {n}"


def main() -> None:
    mret, fret = load()
    ys, ns, yrs = series(mret, fret, UNIV, POST)
    plac = {k: series(mret, fret, UNIV, POST, *k)[0] for k in ev.PLACEBOS}
    kept = {k: y for k, y in plac.items() if math.isfinite(ev.mean_t(y)[1])}
    if DRY:
        print("assets", len(UNIV), "months in gate sample", sum(math.isfinite(y) for y in ys))
        print("assets per month: min", min(ns), "median", int(np.median(ns)), "max", max(ns))
        print("years used: min", min(yrs), "median", int(np.median(yrs)), "max", max(yrs))
        print("placebos kept", len(kept), "of", len(ev.PLACEBOS))
        print("months per placebo", sorted(ev.mean_t(y)[2] for y in kept.values()))
        print("first month with n >= 6:", first_month(mret, fret))
        return
    m, t, n = ev.mean_t(ys)
    pt = [ev.mean_t(y)[1] for y in kept.values()]
    rank = ev.rank_highest(t, pt)
    g = [m > 0 and t >= 2, rank <= 2]
    nul = ev.null_summary(pt)
    early = (first_month(mret, fret), (2016, 12))
    cal = series(mret, mret, UNIV, POST)[0]
    out = [
        "# Same-calendar-month seasonality: event-study gate (survey-7, `seasonal-20y`)",
        "",
        "Rule: `research/survey-7.md` (pushed before this ran). Script",
        "`research/lib/survey7_season.py`. Signal = an asset's mean return in the same calendar",
        "month over the past 20 years (at least 5); y = top fifth minus bottom fifth of the",
        f"{len(UNIV)} assets, held from the last Friday of M - 1 to the last Friday of M.",
        "",
        "## Gate (holding months 2017-01 .. 2025-10)",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Mean y a month (t), {n} months | {m * 100:+.2f}% ({t:+.2f}) | > 0, t >= 2 | {g[0]} |",
        f"| Rank of true t among {1 + len(pt)} (1 = highest) | {rank} | <= 2 | {g[1]} |",
        "",
        f"**Gate: {'PASS' if all(g) else 'fail'}.** Empirical one-sided p = {rank}/"
        f"{1 + len(pt)} = {rank / (1 + len(pt)):.3f}.",
        "",
        f"Assets per month: median {int(np.median(ns))} (min {min(ns)}, max {max(ns)}); years",
        f"per signal: median {int(np.median(yrs))} (min {min(yrs)}, max {max(yrs)}).",
        "",
        "## Placebo null (lags 12j + s, s = 1..10, j = 1 + a .. 20 + a, a = 0..3)",
        "",
        f"SD of placebo t {nul['sd']:.2f}; share with |t| >= 2 {nul['share2']:.0%}; quantiles",
        f"5/50/95% {nul['q5']:+.2f} / {nul['q50']:+.2f} / {nul['q95']:+.2f}; extremes",
        f"{nul['min']:+.2f} / {nul['max']:+.2f}. Placebos kept: {len(pt)} of {len(ev.PLACEBOS)}.",
        "",
        "| s | a = 0 | a = 1 | a = 2 | a = 3 |",
        "|---:|---:|---:|---:|---:|",
    ]
    for s in range(1, 11):
        row = [f"{ev.mean_t(kept[(s, a)])[1]:+.2f}" if (s, a) in kept else "-" for a in range(4)]
        out.append(f"| {s} | " + " | ".join(row) + " |")
    out += [
        "",
        "## Shown, not gating",
        "",
        "| Cell | Mean y a month | t | Months |",
        "|---|---:|---:|---:|",
        f"| Calendar months (month end to month end), 2017-2025 | {cell(cal)} |",
        f"| Friday clock, {early[0][0]}-{early[0][1]:02d} .. 2016-12 | "
        f"{cell(series(mret, fret, UNIV, early)[0])} |",
        f"| Calendar months, {early[0][0]}-{early[0][1]:02d} .. 2016-12 | "
        f"{cell(series(mret, mret, UNIV, early)[0])} |",
        f"| Six live assets only, Friday clock, 2017-2025 | "
        f"{cell(series(mret, fret, LIVE, POST)[0])} |",
        f"| 17 ETFs only, Friday clock, 2017-2025 | {cell(series(mret, fret, ETFS, POST)[0])} |",
        "",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
