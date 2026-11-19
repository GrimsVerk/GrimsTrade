"""Lane wide-11, step 2: event-study gate for W22 `hedging-pressure` (research/wide-11.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10);
COT reports dated after 2025-11-10 are not read. Positions: CFTC legacy COT, futures only
(keyless yearly zips in the shared cache, `cftc/legacy/` under macro.cache_root()).

Run: `uv run python -I research/lib/wide11_hp.py`  (DRY=1: counts only)
Output: research/results/hedging-pressure.md
"""

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import macro  # noqa: E402
import wide11_events as ev  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "hedging-pressure.md"
DRY = bool(os.environ.get("DRY"))
LAST = harness.TRAIN_LAST_BAR
GATE = (date(2018, 6, 5), date(2025, 10, 6))
PRE = (date(2008, 1, 1), date(2018, 5, 29))
REF = date(2000, 1, 4)  # a Tuesday: week index origin
GATE_ASSETS = list(ev.GATE_CODES)
ALL_CODES = {**ev.GATE_CODES, **ev.SHOWN_CODES}

ZFn = Callable[[str, date], float]


def week_of(d: date) -> int:
    return round((d - REF).days / 7)


def main() -> None:
    folder = macro.cache_root() / "cftc" / "legacy"
    zips = [folder / "deacot1986_2016.zip"] + [folder / f"deacot{y}.zip" for y in range(2017, 2026)]
    hp = ev.read_zips(zips, ALL_CODES, LAST)
    z = {a: ev.zscores(m) for a, m in hp.items()}
    hist = harness.load_history("train", syms=list(ALL_CODES))
    px = {a: ev.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}

    def rows(assets: list[str], lo: date, hi: date) -> list[tuple[str, date]]:
        return [(a, t) for a in assets for t in sorted(hp[a]) if lo <= t <= hi]

    def fit(
        assets: list[str],
        zf: ZFn,
        lo: date = GATE[0],
        hi: date = GATE[1],
        hold: int = 35,
        lags: int = 4,
        controls: bool = True,
    ) -> tuple[float, float, int]:
        rs = rows(assets, lo, hi)
        y = np.array([ev.outcome(px[a], t, hold, LAST) for a, t in rs])
        dose = np.array([zf(a, t) for a, t in rs])
        cols = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in assets]
        cols.append(dose)
        if controls:
            cols.append(np.array([ev.past_return(px[a], t, 28) for a, t in rs]))
            cols.append(np.array([ev.past_return(px[a], t, 364) for a, t in rs]))
        week = np.array([week_of(t) for _, t in rs])
        beta, tt, n = ev.ols_dk(cols, y, week, lags)
        j = len(assets)
        return float(beta[j]), float(tt[j]), n

    def true_z(a: str, t: date) -> float:
        return z[a].get(t, np.nan)

    def placebo_z(k: int) -> ZFn:
        return lambda a, t: ev.shifted_z(z[a], t, k)

    if DRY:
        for a in ALL_CODES:
            g = rows([a], *GATE)
            ok = sum(
                not np.isnan(
                    ev.outcome(px[a], t, 35, LAST)
                    + true_z(a, t)
                    + ev.past_return(px[a], t, 28)
                    + ev.past_return(px[a], t, 364)
                )
                for _, t in g
            )
            print(a, "reports", len(hp[a]), "z", len(z[a]), "gate reports", len(g), "rows", ok)
        print("gate rows (true, pooled)", fit(GATE_ASSETS, true_z)[2])  # count only
        ns = []
        for k in ev.SHIFTS_W22:
            rs = rows(GATE_ASSETS, *GATE)
            ns.append(sum(not np.isnan(ev.shifted_z(z[a], t, k)) for a, t in rs))
        print("placebos", len(ev.SHIFTS_W22), "min dose rows", min(ns), "max", max(ns))
        return

    b, t, n = fit(GATE_ASSETS, true_z)
    placebo = [fit(GATE_ASSETS, placebo_z(k))[1] for k in ev.SHIFTS_W22]
    rank = ev.rank_highest(t, placebo)
    sd, share = ev.null_spread(placebo)
    med = float(np.median(placebo))
    gate = [b > 0 and t >= 2, rank <= 2]
    out = [
        "# Hedging pressure and the next 4 weeks: event-study gate (wide-11, W22)",
        "",
        "Rule: `research/wide-11.md` step 2 (pushed before this ran). Script",
        "`research/lib/wide11_hp.py`. Positions: CFTC legacy COT, futures only (keyless).",
        "HP = (commercial short - long) / (short + long); z = HP against its previous 156 weeks.",
        "y = log return from the close of the first bar >= T + 7 to the first bar >= T + 35",
        "(T = Tuesday position date). Pooled over GLD, TLT, SPY, QQQ with market intercepts and",
        "the asset's past 4- and 52-week returns as controls. b = 4-week return per unit of z;",
        "Driscoll-Kraay t (scores summed by report week, Newey-West 4 lags).",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Reports 2018-06-05..2025-10-06, b (t), {n} rows | {b * 100:+.3f}% ({t:+.2f}) |"
        f" > 0, t >= 2 | {gate[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {gate[1]} |",
        "",
        f"**Gate: {'PASS' if all(gate) else 'fail'}.** Empirical one-sided p = {rank}/41 ="
        f" {rank / 41:.3f}. z against the placebo scale: (t - median) / sd ="
        f" {(t - med) / sd:+.2f}.",
        "",
        "## Placebo null (each market's dose calendar moved k weeks)",
        "",
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {np.quantile(placebo, 0.05):+.2f}, 50% {med:+.2f},"
        f" 95% {np.quantile(placebo, 0.95):+.2f}; smallest {min(placebo):+.2f}, largest"
        f" {max(placebo):+.2f}.",
        "",
        "| k (weeks) | t |",
        "|---:|---:|",
    ]
    out += [f"| {k:+d} | {v:+.2f} |" for k, v in zip(ev.SHIFTS_W22, placebo, strict=True)]
    out += [
        "",
        "## Shown (not gating)",
        "",
        "| Cut | b, % per unit (t) | Rows |",
        "|---|---:|---:|",
    ]

    def row(name: str, r: tuple[float, float, int]) -> None:
        out.append(f"| {name} | {r[0] * 100:+.3f} ({r[1]:+.2f}) | {r[2]} |")

    def level(a: str, t: date) -> float:
        return hp[a].get(t, np.nan) if t in z[a] else np.nan

    row("Without the controls", fit(GATE_ASSETS, true_z, controls=False))
    row("1-week horizon (exit >= T + 14, 1 lag)", fit(GATE_ASSETS, true_z, hold=14, lags=1))
    row("Raw HP level instead of z (same rows)", fit(GATE_ASSETS, level))
    for a in GATE_ASSETS + list(ev.SHOWN_CODES):
        row(f"{a} alone", fit([a], true_z))
    row(f"Pre-gate years {PRE[0]}..{PRE[1]} (inside Fan et al.)", fit(GATE_ASSETS, true_z, *PRE))

    # F2 feedback check: z(T) - z(T - 28 days) on r4(T), pooled, market intercepts.
    rs = rows(GATE_ASSETS, *GATE)
    dz = np.array([z[a].get(t, np.nan) - z[a].get(t.fromordinal(t.toordinal() - 28), np.nan)
                   for a, t in rs])  # fmt: skip
    r4 = np.array([ev.past_return(px[a], t, 28) for a, t in rs])
    cols = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in GATE_ASSETS] + [r4]
    fb, ft, fn = ev.ols_dk(cols, dz, np.array([week_of(t) for _, t in rs]), 4)
    j = len(GATE_ASSETS)
    out += [
        "",
        f"Feedback check (F2): 4-week change in z on the past 4-week return, pooled: slope"
        f" {fb[j]:+.2f} z per unit of log return (t {ft[j]:+.2f}, {fn} rows). Positive ="
        " hedgers add to their net short after a rally.",
        "",
    ]
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
