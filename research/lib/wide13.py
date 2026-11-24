"""Lane wide-13: event-study gates W25 `act-haven` and W26 `failure-premium`
(research/wide-13.md steps 2 and 3; rules pushed before this script's first run).

Descriptive only: no strategy, no backtest. Train bars only (load_history("train") cuts at
2025-11-10); GPR days and FDIC failures dated after 2025-11-10 are never read. Doses come from
the data-wide-1 cache (untrusted downloads: run with `python -I`).

Run: `uv run --with xlrd python -I research/lib/wide13.py`  (DRY=1: counts only)
Output: research/results/act-haven.md and research/results/failure-premium.md
"""

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import harness  # noqa: E402
import wide11_events as e11  # noqa: E402
import wide13_events as ev  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = harness.TRAIN_LAST_BAR
HS = (28, 91, 182, 364)  # control horizons, days

DoseFn = Callable[[date], float]


def week_index(ref: date) -> Callable[[date], int]:
    return lambda d: round((d - ref).days / 7)


class Panel:
    """One gate design: dates, assets, entry/exit clock; `fit` is the one code path for the
    true dose, the placebos and the shown cells."""

    def __init__(self, px: dict[str, ev.Closes], ref: date, entry: int, exit_: int):
        self.px, self.week, self.entry, self.exit = px, week_index(ref), entry, exit_

    def fit(
        self,
        assets: list[str],
        dates: list[date],
        dose: DoseFn,
        controls: bool,
        exit_: int | None = None,
        lags: int = 4,
        reaction: bool = False,
    ) -> tuple[float, float, int]:
        ex = self.exit if exit_ is None else exit_
        rs = [(a, t) for a in assets for t in dates]
        if reaction:
            y = np.array([ev.reaction_return(self.px[a], t, self.entry, LAST) for a, t in rs])
        else:
            y = np.array([ev.window_return(self.px[a], t, self.entry, ex, 7, LAST) for a, t in rs])
        cols = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in assets]
        cols.append(np.array([dose(t) for _, t in rs]))
        if controls:
            for h in HS:
                cols.append(np.array([ev.past_return(self.px[a], t, h) for a, t in rs]))
        wk = np.array([self.week(t) for _, t in rs])
        beta, tt, n = e11.ols_dk(cols, y, wk, lags)
        j = len(assets)
        return float(beta[j]), float(tt[j]), n

    def feedback(
        self, assets: list[str], dates: list[date], dose: DoseFn, h: int
    ) -> tuple[float, float, int]:
        """Dose on the asset's own past h-day return alone (asset intercepts, DK 4 lags)."""
        rs = [(a, t) for a in assets for t in dates]
        y = np.array([dose(t) for _, t in rs])
        cols = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in assets]
        cols.append(np.array([ev.past_return(self.px[a], t, h) for a, t in rs]))
        beta, tt, n = e11.ols_dk(cols, y, np.array([self.week(t) for _, t in rs]), 4)
        j = len(assets)
        return float(beta[j]), float(tt[j]), n


def gate_block(
    title: str, b: float, t: float, n: int, placebo: list[float], scale: str
) -> list[str]:
    rank = e11.rank_highest(t, placebo)
    sd, share = e11.null_spread(placebo)
    q5, med, q95 = ev.quantiles(placebo)
    met = [b > 0 and t >= 2, rank <= 2]
    return [
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| {title}, b (t), {n} rows | {b * 100:+.3f}% {scale} ({t:+.2f}) | > 0, t >= 2 |"
        f" {met[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {met[1]} |",
        "",
        f"**Gate: {'PASS' if all(met) else 'fail'}.** Empirical one-sided p = {rank}/41 ="
        f" {rank / 41:.3f}. z against the placebo scale: (t - median) / sd ="
        f" {(t - med) / sd:+.2f}.",
        "",
        "## Placebo null (dose calendar moved k weeks)",
        "",
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {q5:+.2f}, 50% {med:+.2f}, 95% {q95:+.2f}; smallest"
        f" {min(placebo):+.2f}, largest {max(placebo):+.2f}.",
        "",
        "| k (weeks) | t |",
        "|---:|---:|",
        *[f"| {k:+d} | {v:+.2f} |" for k, v in zip(ev.SHIFTS, placebo, strict=True)],
        "",
        "## Shown (not gating)",
        "",
        "| Cut | b, % per unit (t) | Rows |",
        "|---|---:|---:|",
    ]


def cell(name: str, r: tuple[float, float, int]) -> str:
    return f"| {name} | {r[0] * 100:+.3f} ({r[1]:+.2f}) | {r[2]} |"


def act_haven(px: dict[str, ev.Closes]) -> None:
    rows = [g for g in dw.read_gpr_xls(dw.snapshot("gpr") / "data_gpr_daily_recent.xls")]
    rows = [g for g in rows if g.day <= LAST]
    ends = ev.mondays(date(1985, 1, 7), LAST)
    z = {
        f: e11.zscores(ev.weekly_log_mean({g.day: getattr(g, f) for g in rows}, ends))
        for f in ("act", "threat", "gprd")
    }
    za = z["act"]
    gate_dates = ev.mondays(date(2005, 1, 3), date(2025, 10, 6))
    post = ev.mondays(date(2020, 1, 6), date(2025, 10, 6))
    p = Panel(px, date(2000, 1, 3), 9, 37)
    assets = ["GLD", "TLT"]

    def true(t: date) -> float:
        return za.get(t, np.nan)

    if DRY:
        print("W25 GPR days", len(rows), rows[0].day, rows[-1].day, "act z weeks", len(za))
        print("W25 gate Mondays", len(gate_dates), "with z", sum(t in za for t in gate_dates))
        for a in assets + ["SPY"]:
            ok = sum(
                not np.isnan(ev.window_return(px[a], t, 9, 37, 7, LAST) + true(t))
                for t in gate_dates
            )
            print("W25", a, "rows with z and outcome", ok)
        ns = [sum(not np.isnan(ev.shifted(za, t, k)) for t in gate_dates) for k in ev.SHIFTS]
        print("W25 placebos", len(ev.SHIFTS), "dose weeks min", min(ns), "max", max(ns))
        return

    b, t, n = p.fit(assets, gate_dates, true, controls=False)
    placebo = [
        p.fit(assets, gate_dates, lambda d, k=k: ev.shifted(za, d, k), controls=False)[1]
        for k in ev.SHIFTS
    ]
    out = [
        "# Geopolitical acts and safe havens over the next 4 weeks (wide-13, W25 `act-haven`)",
        "",
        "Rule: `research/wide-13.md` step 2 (pushed before this ran). Script",
        "`research/lib/wide13.py`. Dose: z of ln(1 + weekly mean of the Caldara-Iacoviello daily",
        "acts sub-index), week ending Monday M, against the previous 156 weeks. y = log return",
        "from the close of the first bar >= M + 9 (the index's available-on date) to the first bar",
        ">= M + 37. GLD and TLT pooled with asset intercepts, no controls. Driscoll-Kraay t",
        "(scores summed by Monday, Newey-West 4 lags). Values are today's revised index.",
        "",
        *gate_block("Mondays 2005-01-03..2025-10-06", b, t, n, placebo, "per unit of z"),
    ]

    def zf(field: str) -> DoseFn:
        return lambda d: z[field].get(d, np.nan)

    out += [
        cell("Threats sub-index z instead", p.fit(assets, gate_dates, zf("threat"), False)),
        cell("Total index GPRD z instead", p.fit(assets, gate_dates, zf("gprd"), False)),
        cell("GLD alone", p.fit(["GLD"], gate_dates, true, False)),
        cell("TLT alone", p.fit(["TLT"], gate_dates, true, False)),
        cell("SPY alone (D3's neighbour)", p.fit(["SPY"], gate_dates, true, False)),
        cell("Post-paper years 2020-01-06..2025-10-06", p.fit(assets, post, true, False)),
        cell("With past 4/13/26/52-week returns", p.fit(assets, gate_dates, true, True)),
        cell(
            "1-week horizon (exit >= M + 16, 1 lag)",
            p.fit(assets, gate_dates, true, False, exit_=16, lags=1),
        ),
        "",
        "F2 feedback check: acts z on GLD/TLT's own past return alone (pooled, DK 4 lags):",
        "",
        "| Past return | Slope, z per unit of log return (t) | Rows |",
        "|---|---:|---:|",
    ]
    for h in HS:
        fb = p.feedback(assets, gate_dates, true, h)
        out.append(f"| {h // 7} weeks | {fb[0]:+.2f} ({fb[1]:+.2f}) | {fb[2]} |")
    out.append("")
    (RESULTS / "act-haven.md").write_text("\n".join(out))
    print("\n".join(out))


def failure_premium(px: dict[str, ev.Closes]) -> None:
    fs = dw.parse_fdic_failures((dw.snapshot("fdic") / "failures.json").read_text())
    fs = [f for f in fs if f.kind in ("FAILURE", "ASSISTANCE")]
    weeks = ev.fridays(date(1990, 1, 5), LAST)
    x = ev.failure_dose(((f.day, f.assets_k) for f in fs), weeks, LAST)
    gate_dates = ev.fridays(date(2000, 1, 7), date(2025, 10, 3))
    p = Panel(px, date(2000, 1, 7), 3, 31)

    def true(t: date) -> float:
        return x.get(t, np.nan)

    if DRY:
        print("W26 failures read", sum(f.day <= LAST for f in fs), "dose weeks", len(x))
        print(
            "W26 gate Fridays",
            len(gate_dates),
            "failure weeks",
            sum(x.get(t, 0) > 0 for t in gate_dates),
        )
        for a in ("XLF", "SPY", "TLT", "IEF"):
            ok = sum(
                not np.isnan(
                    ev.window_return(px[a], t, 3, 31, 7, LAST)
                    + sum(ev.past_return(px[a], t, h) for h in HS)
                )
                for t in gate_dates
            )
            print("W26", a, "rows with outcome and controls", ok)
        ns = [sum(not np.isnan(ev.shifted(x, t, k)) for t in gate_dates) for k in ev.SHIFTS]
        print("W26 placebos", len(ev.SHIFTS), "dose weeks min", min(ns), "max", max(ns))
        return

    b, t, n = p.fit(["XLF"], gate_dates, true, controls=True)
    placebo = [
        p.fit(["XLF"], gate_dates, lambda d, k=k: ev.shifted(x, d, k), controls=True)[1]
        for k in ev.SHIFTS
    ]
    out = [
        "# Bank failures and XLF over the next 4 weeks (wide-13, W26 `failure-premium`)",
        "",
        "Rule: `research/wide-13.md` step 3 (pushed before this ran). Script",
        "`research/lib/wide13.py`. Dose x = ln(1 + total assets, millions of USD, of FDIC",
        "failures and assistance transactions dated Saturday..Friday F); 0 without one.",
        "y = log return of XLF from the close of the first bar >= F + 3 to the first bar",
        ">= F + 31.",
        "Controls: XLF's past 4/13/26/52-week returns. Newey-West t, 4 lags (one row a week).",
        "",
        *gate_block("Fridays 2000-01-07..2025-10-03", b, t, n, placebo, "per unit of x"),
    ]

    def dummy(d: date) -> float:
        v = x.get(d, np.nan)
        return v if v != v else float(v > 0)

    no23 = [d for d in gate_dates if d.year != 2023]
    out += [
        cell("Without the controls", p.fit(["XLF"], gate_dates, true, False)),
        cell("Failure-week dummy instead of x", p.fit(["XLF"], gate_dates, dummy, True)),
        cell("Year 2023 dropped", p.fit(["XLF"], no23, true, True)),
        cell("SPY instead of XLF", p.fit(["SPY"], gate_dates, true, True)),
        cell("TLT instead (idea 3, F1 fails)", p.fit(["TLT"], gate_dates, true, True)),
        cell("IEF instead (idea 3, F1 fails)", p.fit(["IEF"], gate_dates, true, True)),
        cell(
            "Monday reaction (last close <= F to first close >= F + 3, 1 lag)",
            p.fit(["XLF"], gate_dates, true, False, lags=1, reaction=True),
        ),
        cell(
            "1-week horizon (exit >= F + 10, 1 lag)",
            p.fit(["XLF"], gate_dates, true, True, exit_=10, lags=1),
        ),
        "",
        "F2 feedback check: x on XLF's own past return alone (NW 4 lags; negative = failures",
        "follow falls):",
        "",
        "| Past return | Slope, x per unit of log return (t) | Rows |",
        "|---|---:|---:|",
    ]
    for h in HS:
        fb = p.feedback(["XLF"], gate_dates, true, h)
        out.append(f"| {h // 7} weeks | {fb[0]:+.2f} ({fb[1]:+.2f}) | {fb[2]} |")
    out.append("")
    (RESULTS / "failure-premium.md").write_text("\n".join(out))
    print("\n".join(out))


def main() -> None:
    syms = ["GLD", "TLT", "SPY", "XLF", "IEF"]
    hist = harness.load_history("train", syms=syms)
    px = {a: ev.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}
    which = os.environ.get("GATE", "both")
    if which in ("both", "W25"):
        act_haven(px)
    if which in ("both", "W26"):
        failure_premium(px)


if __name__ == "__main__":
    main()
