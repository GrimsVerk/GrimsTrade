"""Lane wide-12, step 2: event-study gate for W23 `custody-selling` (research/wide-12.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10);
H.4.1 weeks dated after 2025-11-10 are not read. Holdings: Fed H.4.1 memo item, custody of
marketable Treasuries for foreign official accounts (keyless DDP zip in the shared cache,
`fed-ddp/h41-2026-11-19/` under macro.cache_root()).

Run: `uv run python -I research/lib/wide12_custody.py`  (DRY=1: counts only)
Output: research/results/custody-selling.md
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
import wide11_events as w11  # noqa: E402
import wide12_events as ev  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "custody-selling.md"
DRY = bool(os.environ.get("DRY"))
LAST = harness.TRAIN_LAST_BAR
GATE = (date(2010, 1, 6), date(2025, 10, 1))
PRE = (date(2005, 1, 5), date(2009, 12, 30))
REF = date(2000, 1, 5)  # a Wednesday: week index origin
GATE_ASSETS = ["TLT", "IEF"]
SHOWN = ["SPY", "GLD"]
CTRL_DAYS = (28, 91, 182, 364)

ZFn = Callable[[date], float]


def week_of(d: date) -> int:
    return round((d - REF).days / 7)


def main() -> None:
    h = ev.read_h41(macro.cache_root() / "fed-ddp" / "h41-2026-11-19" / "H41.zip", ev.SERIES, LAST)
    f = ev.flows(h)
    z = w11.zscores(f)
    hist = harness.load_history("train", syms=GATE_ASSETS + SHOWN)
    px = {a: w11.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}
    weds = sorted(h)

    def rows(assets: list[str], lo: date, hi: date) -> list[tuple[str, date]]:
        return [(a, w) for a in assets for w in weds if lo <= w <= hi]

    def fit(
        assets: list[str],
        zf: ZFn,
        lo: date = GATE[0],
        hi: date = GATE[1],
        exit_days: int = 33,
        lags: int = 4,
        controls: bool = True,
    ) -> tuple[float, float, int]:
        rs = rows(assets, lo, hi)
        y = np.array([ev.outcome(px[a], w, exit_days, LAST) for a, w in rs])
        cols = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in assets]
        cols.append(np.array([zf(w) for _, w in rs]))
        if controls:
            for back in CTRL_DAYS:
                cols.append(np.array([w11.past_return(px[a], w, back) for a, w in rs]))
        week = np.array([week_of(w) for _, w in rs])
        beta, tt, n = w11.ols_dk(cols, y, week, lags)
        j = len(assets)
        return float(beta[j]), float(tt[j]), n

    def true_z(w: date) -> float:
        return z.get(w, np.nan)

    def placebo_z(k: int) -> ZFn:
        return lambda w: w11.shifted_z(z, w, k)

    if DRY:
        print("weeks", len(h), "flows", len(f), "z", len(z), "first z", min(z))
        for a in GATE_ASSETS + SHOWN:
            g = rows([a], *GATE)
            ok = sum(
                not np.isnan(
                    ev.outcome(px[a], w, 33, LAST)
                    + true_z(w)
                    + sum(w11.past_return(px[a], w, d) for d in CTRL_DAYS)
                )
                for _, w in g
            )
            print(a, "gate weeks", len(g), "rows", ok)
        print("gate rows (true, pooled)", fit(GATE_ASSETS, true_z)[2])  # count only
        g = [w for w in weds if GATE[0] <= w <= GATE[1]]
        ns = [sum(not np.isnan(w11.shifted_z(z, w, k)) for w in g) for k in w11.SHIFTS_W22]
        print("placebos", len(w11.SHIFTS_W22), "min dose weeks", min(ns), "max", max(ns))
        return

    b, t, n = fit(GATE_ASSETS, true_z)
    placebo = [fit(GATE_ASSETS, placebo_z(k))[1] for k in w11.SHIFTS_W22]
    rank = w11.rank_highest(t, placebo)
    sd, share = w11.null_spread(placebo)
    med = float(np.median(placebo))
    gate = [b > 0 and t >= 2, rank <= 2]
    out = [
        "# Foreign official custody flows and the next 4 weeks of Treasuries: gate (wide-12, W23)",
        "",
        "Rule: `research/wide-12.md` step 2 (pushed before this ran). Script",
        "`research/lib/wide12_custody.py`. Holdings: Fed H.4.1, custody of marketable Treasuries",
        "for foreign official accounts, Wednesday level (DDP series RESH4FG_N.WW, keyless).",
        "f = 4-week log change; z = f against its previous 156 weeks. y = log return from the",
        "close of the first bar >= W + 5 to the first bar >= W + 33 (W = Wednesday). Pooled over",
        "TLT and IEF with asset intercepts and the asset's past 4-, 13-, 26- and 52-week returns",
        "as controls. b = 4-week return per unit of z; Driscoll-Kraay t (scores summed by week,",
        "Newey-West 4 lags).",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Wednesdays 2010-01-06..2025-10-01, b (t), {n} rows | {b * 100:+.3f}% ({t:+.2f}) |"
        f" > 0, t >= 2 | {gate[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {gate[1]} |",
        "",
        f"**Gate: {'PASS' if all(gate) else 'fail'}.** Empirical one-sided p = {rank}/41 ="
        f" {rank / 41:.3f}. z against the placebo scale: (t - median) / sd ="
        f" {(t - med) / sd:+.2f}.",
        "",
        "## Placebo null (the dose calendar moved k weeks)",
        "",
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {np.quantile(placebo, 0.05):+.2f}, 50% {med:+.2f},"
        f" 95% {np.quantile(placebo, 0.95):+.2f}; smallest {min(placebo):+.2f}, largest"
        f" {max(placebo):+.2f}.",
        "",
        "| k (weeks) | t |",
        "|---:|---:|",
    ]
    out += [f"| {k:+d} | {v:+.2f} |" for k, v in zip(w11.SHIFTS_W22, placebo, strict=True)]
    out += [
        "",
        "## Shown (not gating)",
        "",
        "| Cut | b, % per unit (t) | Rows |",
        "|---|---:|---:|",
    ]

    def row(name: str, r: tuple[float, float, int]) -> None:
        out.append(f"| {name} | {r[0] * 100:+.3f} ({r[1]:+.2f}) | {r[2]} |")

    def raw_flow(w: date) -> float:
        return f.get(w, np.nan) if w in z else np.nan

    row("Without the controls", fit(GATE_ASSETS, true_z, controls=False))
    row("1-week horizon (exit >= W + 12, 1 lag)", fit(GATE_ASSETS, true_z, exit_days=12, lags=1))
    row("Raw 4-week flow f instead of z (same rows)", fit(GATE_ASSETS, raw_flow))
    for a in GATE_ASSETS + SHOWN:
        row(f"{a} alone", fit([a], true_z))
    row(f"Pre-gate years {PRE[0]}..{PRE[1]}", fit(GATE_ASSETS, true_z, *PRE))

    # F2 feedback: z(W) on each past return alone, pooled TLT and IEF, asset intercepts.
    rs = rows(GATE_ASSETS, *GATE)
    zz = np.array([true_z(w) for _, w in rs])
    wk = np.array([week_of(w) for _, w in rs])
    dummies = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in GATE_ASSETS]
    j = len(GATE_ASSETS)
    out += ["", "Feedback check (F2): z(W) on the asset's own past return, pooled TLT and IEF:", ""]
    out += ["| Past return | Slope, z per unit of log return (t) | Rows |", "|---|---:|---:|"]
    for back in CTRL_DAYS:
        r = np.array([w11.past_return(px[a], w, back) for a, w in rs])
        fb, ft, fn = w11.ols_dk([*dummies, r], zz, wk, 4)
        out.append(f"| {back // 7} weeks | {fb[j]:+.2f} ({ft[j]:+.2f}) | {fn} |")

    # Face-value check: weekly flow on TLT's return over the same week, 1 lag.
    g = [w for w in weds if GATE[0] <= w <= GATE[1]]
    f1 = ev.flows(h, 7)
    yy = np.array([f1.get(w, np.nan) for w in g])
    r1 = np.array([w11.past_return(px["TLT"], w, 7) for w in g])
    cb, ct, cn = w11.ols_dk([np.ones(len(g)), r1], yy, np.array([week_of(w) for w in g]), 1)
    out += [
        "",
        f"Face-value check: weekly log change of holdings on TLT's same-week log return: slope"
        f" {cb[1]:+.4f} (t {ct[1]:+.2f}, {cn} weeks). A market-value series would show a"
        " slope near the holdings' duration ratio to TLT (about +0.3).",
        "",
    ]
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
