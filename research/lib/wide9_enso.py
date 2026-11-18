"""Lane wide-9, step 1: event-study gate for W19 `enso-commodity` (research/wide-9.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).
Needs NOAA CPC's keyless oni.ascii.txt in research/data/oni/ (public domain; see wide-9.md).

Run: `uv run python -I research/lib/wide9_enso.py`  (DRY=1: counts only)
Output: research/results/enso-commodity.md
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide6_rules as r6  # noqa: E402
import wide9_events as ev  # noqa: E402

ONI = harness.DATA / "oni" / "oni.ascii.txt"
OUT = Path(__file__).resolve().parents[1] / "results" / "enso-commodity.md"
DRY = bool(os.environ.get("DRY"))
GATE = ((2014, 1), (2025, 4))
PAPER = ((2006, 2), (2013, 12))
SHIFTS = list(range(2, 42))
LAGS = 6
H = 6


class Series:
    def __init__(self, sym: str):
        bars = harness.load_history("train", syms=[sym])[sym]
        self.days = [b.date for b in bars]
        self.logc = np.log(np.array([b.close for b in bars]))


def points(
    s: Series, oni: dict[ev.Month, float], span: tuple[ev.Month, ev.Month], k: int = 0, h: int = H
) -> tuple[np.ndarray, np.ndarray]:
    xs, ys = [], []
    for m in ev.months(*span):
        x = ev.dose(oni, m, k)
        y = ev.horizon_return(s.days, s.logc, m, h, harness.TRAIN_LAST_BAR)
        if not (math.isnan(x) or math.isnan(y)):
            xs.append(x)
            ys.append(y)
    return np.array(xs), np.array(ys)


def fit(x: np.ndarray, y: np.ndarray, lags: int = LAGS) -> tuple[float, float]:
    beta, t = r6.ols_dk(y, np.column_stack([np.ones(len(x)), x]), list(range(len(x))), lags)
    return float(beta[1]), float(t[1])


def mean_in(x: np.ndarray, y: np.ndarray, lo: float, hi: float) -> tuple[float, int]:
    sel = np.array([ev.in_bin(v, lo, hi) for v in x], dtype=bool)
    return (float(y[sel].mean()) if sel.any() else math.nan), int(sel.sum())


def pts(v: float) -> str:
    return f"{v * 100:+.2f}"


def main() -> None:
    oni = ev.parse_oni(ONI.read_text())
    dbc = Series("DBC")
    if DRY:
        for name, span in (("gate", GATE), ("paper", PAPER)):
            x, _ = points(dbc, oni, span)
            print(name, "months", len(x))
        print(
            "placebos",
            len(SHIFTS),
            "min months",
            min(len(points(dbc, oni, GATE, k)[0]) for k in SHIFTS),
        )
        return
    x, y = points(dbc, oni, GATE)
    b, t = fit(x, y)
    placebo = [fit(*points(dbc, oni, GATE, k))[1] for k in SHIFTS]
    rank = ev.rank_highest(t, placebo)
    strong, n_s = mean_in(x, y, 1.0, math.inf)
    weak, n_w = mean_in(x, y, 0.5, 1.0)
    bp, tp = fit(*points(dbc, oni, PAPER))
    sd, share = ev.null_spread(placebo)
    g = [b > 0 and t >= 2, rank <= 2, strong > weak, bp > 0]
    out = [
        "# ENSO and commodities: event-study gate (wide-9, W19)",
        "",
        "Rule: `research/wide-9.md` step 1 (pushed before this ran). Script",
        "`research/lib/wide9_enso.py`. ONI: NOAA CPC (public domain). y = six-month log return",
        "after each month end; x = ONI of the season ending the month before. Slopes in points",
        "of six-month return per degree of ONI; Newey-West t, 6 lags.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| DBC 2014-01..2025-04 b (t), {len(x)} months | {pts(b)} ({t:+.2f}) |"
        f" > 0, t >= 2 | {g[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {g[1]} |",
        f"| Mean y, x >= 1.0 ({n_s}) vs 0.5 <= x < 1.0 ({n_w}) | {pts(strong)} vs {pts(weak)} |"
        f" strong > weak | {g[2]} |",
        f"| DBC 2006-02..2013-12 b (t) | {pts(bp)} ({tp:+.2f}) | > 0 | {g[3]} |",
        "",
        f"**Gate: {'PASS' if all(g) else 'fail'}.** Empirical one-sided p = {rank}/41 ="
        f" {rank / 41:.3f}.",
        "",
        "## Placebo null (ONI moved k = 2..41 years earlier), DBC 2014-2025",
        "",
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {np.quantile(placebo, 0.05):+.2f}, 50% {np.quantile(placebo, 0.5):+.2f},"
        f" 95% {np.quantile(placebo, 0.95):+.2f}; largest {max(placebo):+.2f}.",
        "",
        "| k (years) | t |",
        "|---:|---:|",
    ]
    out += [f"| {k} | {v:+.2f} |" for k, v in zip(SHIFTS, placebo, strict=True)]
    out += [
        "",
        "## Shown",
        "",
        "| Series, sample | b (t) |",
        "|---|---:|",
    ]
    for sym in ("GLD", "SLV"):
        bs, ts = fit(*points(Series(sym), oni, GATE))
        out.append(f"| {sym} 2014-2025, 6 months | {pts(bs)} ({ts:+.2f}) |")
    b3, t3 = fit(*points(dbc, oni, GATE, h=3), lags=3)
    out += [f"| DBC 2014-2025, 3 months | {pts(b3)} ({t3:+.2f}) |", ""]
    out += ["| ONI bin (DBC 2014-2025) | Mean six-month y | Months |", "|---|---:|---:|"]
    for name, lo, hi in ev.ONI_BINS:
        mu, n = mean_in(x, y, lo, hi)
        out.append(f"| {name} | {pts(mu)} | {n} |")
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
