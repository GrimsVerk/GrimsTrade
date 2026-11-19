"""Lane wide-12, step 3: event-study gate for W24 `inflation-disagreement` (research/wide-12.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).
Dose: Survey of Professional Forecasters dispersion (keyless xlsx in the shared cache,
`philly-spf/2026-11-19/` under macro.cache_root()).

Run: `uv run python -I research/lib/wide12_spf.py`  (DRY=1: counts only)
Output: research/results/inflation-disagreement.md
"""

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from datetime import timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import macro  # noqa: E402
import wide11_events as w11  # noqa: E402
import wide12_events as ev  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "inflation-disagreement.md"
DRY = bool(os.environ.get("DRY"))
LAST = harness.TRAIN_LAST_BAR
GATE = (ev.quarter_index("2010Q1"), ev.quarter_index("2025Q2"))
PRE = (ev.quarter_index("1996Q4"), ev.quarter_index("2009Q4"))
GATE_ASSETS = ["TLT", "IEF"]
SHOWN = ["SPY"]
CTRL_DAYS = (91, 182, 364)

ZFn = Callable[[int], float]


def qlabel(q: int) -> str:
    return f"{q // 4}Q{q % 4 + 1}"


def main() -> None:
    book = macro.cache_root() / "philly-spf" / "2026-11-19" / "Dispersion_1.xlsx"
    d10 = ev.quarter_column(ev.read_xlsx_sheet(book, "CPI10"), "CPI10_D1")
    d1 = ev.quarter_column(ev.read_xlsx_sheet(book, "CPI"), "CPI_D1(T+4)")
    # Train only: drop surveys released after the last train bar (entry after LAST).
    d10 = {q: v for q, v in d10.items() if ev.entry_target(q) <= LAST}
    d1 = {q: v for q, v in d1.items() if ev.entry_target(q) <= LAST}
    z10, z1 = ev.zscores_q(d10), ev.zscores_q(d1)
    hist = harness.load_history("train", syms=GATE_ASSETS + SHOWN)
    px = {a: w11.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}

    def rows(assets: list[str], lo: int, hi: int) -> list[tuple[str, int]]:
        return [(a, q) for a in assets for q in range(lo, hi + 1)]

    def past(a: str, q: int, back: int) -> float:
        return w11.past_return(px[a], ev.entry_target(q) - timedelta(days=1), back)

    def fit(
        assets: list[str], zf: ZFn, lo: int = GATE[0], hi: int = GATE[1], controls: bool = False
    ) -> tuple[float, float, int]:
        rs = rows(assets, lo, hi)
        y = np.array([ev.outcome_q(px[a], q, LAST) for a, q in rs])
        cols = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in assets]
        cols.append(np.array([zf(q) for _, q in rs]))
        if controls:
            for back in CTRL_DAYS:
                cols.append(np.array([past(a, q, back) for a, q in rs]))
        beta, tt, n = w11.ols_dk(cols, y, np.array([q for _, q in rs]), 1)
        j = len(assets)
        return float(beta[j]), float(tt[j]), n

    def true_z(q: int) -> float:
        return z10.get(q, np.nan)

    def placebo_z(k: int) -> ZFn:
        return lambda q: z10.get(q - k, np.nan)

    if DRY:
        print("CPI10 surveys", len(d10), qlabel(min(d10)), qlabel(max(d10)), "z", len(z10),
              "first z", qlabel(min(z10)))  # fmt: skip
        print("CPI(T+4) surveys", len(d1), "z", len(z1))
        for a in GATE_ASSETS + SHOWN:
            ok = sum(
                not np.isnan(ev.outcome_q(px[a], q, LAST) + true_z(q)) for _, q in rows([a], *GATE)
            )
            print(a, "gate quarters", GATE[1] - GATE[0] + 1, "rows", ok)
        print("gate rows (true, pooled)", fit(GATE_ASSETS, true_z)[2])  # count only
        ns = [fit(GATE_ASSETS, placebo_z(k))[2] for k in ev.SHIFTS_W24]
        print("placebos", len(ns), "min rows", min(ns), "max", max(ns))
        return

    b, t, n = fit(GATE_ASSETS, true_z)
    placebo = [fit(GATE_ASSETS, placebo_z(k))[1] for k in ev.SHIFTS_W24]
    rank = w11.rank_highest(t, placebo)
    sd, share = w11.null_spread(placebo)
    med = float(np.median(placebo))
    gate = [b > 0 and t >= 2, rank <= 2]
    out = [
        "# Inflation disagreement and next quarter's bond return: gate (wide-12, W24)",
        "",
        "Rule: `research/wide-12.md` step 3 (pushed before this ran). Script",
        "`research/lib/wide12_spf.py`. Dose: SPF interquartile range of 10-year CPI inflation",
        "forecasts (`CPI10_D1`), z against the previous 40 surveys. y = log return from the first",
        "bar >= the first day of the survey quarter's third month to the first bar three months",
        "later. Pooled over TLT and IEF with asset intercepts. b = quarterly return per unit of z;",
        "Driscoll-Kraay t (scores summed by quarter, Newey-West 1 lag).",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Surveys 2010Q1..2025Q2, b (t), {n} rows | {b * 100:+.3f}% ({t:+.2f}) |"
        f" > 0, t >= 2 | {gate[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {gate[1]} |",
        "",
        f"**Gate: {'PASS' if all(gate) else 'fail'}.** Empirical one-sided p = {rank}/41 ="
        f" {rank / 41:.3f}. z against the placebo scale: (t - median) / sd ="
        f" {(t - med) / sd:+.2f}.",
        "",
        "## Placebo null (the dose calendar moved k quarters)",
        "",
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {np.quantile(placebo, 0.05):+.2f}, 50% {med:+.2f},"
        f" 95% {np.quantile(placebo, 0.95):+.2f}; smallest {min(placebo):+.2f}, largest"
        f" {max(placebo):+.2f}.",
        "",
        "| k (quarters) | t | rows |",
        "|---:|---:|---:|",
    ]
    for k, v in zip(ev.SHIFTS_W24, placebo, strict=True):
        out.append(f"| {k:+d} | {v:+.2f} | {fit(GATE_ASSETS, placebo_z(k))[2]} |")
    out += [
        "",
        "## Shown (not gating)",
        "",
        "| Cut | b, % per unit (t) | Rows |",
        "|---|---:|---:|",
    ]

    def row(name: str, r: tuple[float, float, int]) -> None:
        out.append(f"| {name} | {r[0] * 100:+.3f} ({r[1]:+.2f}) | {r[2]} |")

    row("With past 13/26/52-week returns as controls", fit(GATE_ASSETS, true_z, controls=True))
    row("Next-year dose CPI_D1(T+4) instead", fit(GATE_ASSETS, lambda q: z1.get(q, np.nan)))
    for a in GATE_ASSETS + SHOWN:
        row(f"{a} alone", fit([a], true_z))
    row(f"Pre-gate years {qlabel(PRE[0])}..{qlabel(PRE[1])}", fit(GATE_ASSETS, true_z, *PRE))

    rs = rows(GATE_ASSETS, *GATE)
    zz = np.array([true_z(q) for _, q in rs])
    qi = np.array([q for _, q in rs])
    dummies = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in GATE_ASSETS]
    j = len(GATE_ASSETS)
    out += ["", "Feedback check (F2): z(q) on the asset's own past return, pooled TLT and IEF:", ""]
    out += ["| Past return | Slope, z per unit of log return (t) | Rows |", "|---|---:|---:|"]
    for back in (91, 364):
        r = np.array([past(a, q, back) for a, q in rs])
        fb, ft, fn = w11.ols_dk([*dummies, r], zz, qi, 1)
        out.append(f"| {back // 7} weeks | {fb[j]:+.2f} ({ft[j]:+.2f}) | {fn} |")
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
