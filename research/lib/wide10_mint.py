"""Lane wide-10, step 3: event-study gate for W21 `stablecoin-mint` (research/wide-10.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10);
stablecoin snapshots after 2025-11-10 are not read. Supply: DefiLlama (keyless), one JSON file
in research/data/stablecoins/.

Run: `uv run python -I research/lib/wide10_mint.py`  (DRY=1: counts only)
Output: research/results/stablecoin-mint.md
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide10_events as ev  # noqa: E402

FILE = harness.DATA / "stablecoins" / "all.json"
OUT = Path(__file__).resolve().parents[1] / "results" / "stablecoin-mint.md"
DRY = bool(os.environ.get("DRY"))
GATE = (date(2018, 4, 6), date(2025, 10, 31))
HALVES = [(date(2018, 4, 6), date(2021, 12, 31)), (date(2022, 1, 1), date(2025, 10, 31))]


def closes(sym: str) -> dict[date, float]:
    return {b.date: b.close for b in harness.load_history("train", syms=[sym])[sym]}


def main() -> None:
    supply = ev.parse_supply(json.loads(FILE.read_text()), harness.TRAIN_LAST_BAR)
    btc, eth = closes("BTC"), closes("ETH")
    fr = ev.fridays(*GATE)
    reasons = Counter(ev.issuance(supply, f)[1] for f in fr)

    def dose(k: int) -> np.ndarray:
        return np.array([ev.issuance(supply, f - timedelta(days=7 * k))[0] for f in fr])

    def coin(c: dict[date, float], prev: bool) -> np.ndarray:
        return np.array([ev.week_return(c, f, prev) for f in fr])

    yb, ye = coin(btc, False), coin(eth, False)
    cb, ce = coin(btc, True), coin(eth, True)
    y, c = (yb + ye) / 2, (cb + ce) / 2
    m = dose(0)
    if DRY:
        print("Fridays", len(fr), "dose guards", dict(reasons))
        print("weeks with dose, outcome and control", int((~np.isnan(m + y + c)).sum()))
        print(
            "placebos",
            len(ev.SHIFTS_W21),
            "min weeks",
            min(int((~np.isnan(dose(k) + y + c)).sum()) for k in ev.SHIFTS_W21),
        )
        return

    def fit(md: np.ndarray, yy: np.ndarray, ctrl: np.ndarray | None, sel=None) -> tuple:
        mask = np.ones(len(fr), bool) if sel is None else sel
        cols = [md[mask]] + ([] if ctrl is None else [ctrl[mask]])
        beta, t = ev.ols_hc1_multi(cols, yy[mask])
        n = int((~np.isnan(np.column_stack(cols)).any(axis=1) & ~np.isnan(yy[mask])).sum())
        return float(beta[1]), float(t[1]), n

    b, t, n = fit(m, y, c)
    placebo = [fit(dose(k), y, c)[1] for k in ev.SHIFTS_W21]
    rank = ev.rank_highest(t, placebo)
    sd, share = ev.null_spread(placebo)
    gate = [b > 0 and t >= 2, rank <= 2]
    out = [
        "# Stablecoin issuance and next-week coin returns: event-study gate (wide-10, W21)",
        "",
        "Rule: `research/wide-10.md` step 3 (pushed before this ran). Script",
        "`research/lib/wide10_mint.py`. Supply: DefiLlama (keyless). y = mean of BTC and ETH",
        "log return, Friday 00:00 UTC to the next; m = the week's log change of total USD",
        "stablecoin supply to Thursday 00:00 UTC; control = last week's y. b = next-week return",
        "per unit of m (a 1% week of issuance is m = 0.01); White (HC1) t.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Fridays 2018-04-06..2025-10-31 b (t), {n} weeks | {b:+.2f} ({t:+.2f}) |"
        f" > 0, t >= 2 | {gate[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {gate[1]} |",
        "",
        f"**Gate: {'PASS' if all(gate) else 'fail'}.** Empirical one-sided p = {rank}/41 ="
        f" {rank / 41:.3f}. Dose guards over {len(fr)} Fridays: {dict(reasons)}. Weekly m:"
        f" mean {np.nanmean(m) * 100:+.2f}%, sd {np.nanstd(m) * 100:.2f}%.",
        "",
        "## Placebo null (dose calendar moved k weeks), 2018-2025",
        "",
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {np.quantile(placebo, 0.05):+.2f}, 50% {np.quantile(placebo, 0.5):+.2f},"
        f" 95% {np.quantile(placebo, 0.95):+.2f}; smallest {min(placebo):+.2f}, largest"
        f" {max(placebo):+.2f}.",
        "",
        "| k (weeks) | t |",
        "|---:|---:|",
    ]
    out += [f"| {k:+d} | {v:+.2f} |" for k, v in zip(ev.SHIFTS_W21, placebo, strict=True)]
    out += ["", "## Shown (not gating)", "", "| Cut | b (t) | Weeks |", "|---|---:|---:|"]

    def row(name: str, r: tuple) -> None:
        out.append(f"| {name} | {r[0]:+.2f} ({r[1]:+.2f}) | {r[2]} |")

    row("Without the control", fit(m, y, None))
    row("BTC alone (own control)", fit(m, yb, cb))
    row("ETH alone (own control)", fit(m, ye, ce))
    for a, z in HALVES:
        sel = np.array([a <= f <= z for f in fr])
        row(f"Half {a}..{z}", fit(m, y, c, sel))
    row("Same week: this week's m on this week's return (no control)", fit(c, m, None))
    ok = ~np.isnan(m + y)
    q = np.quantile(m[ok], 0.8)
    top, rest = y[ok][m[ok] >= q], y[ok][m[ok] < q]
    out += [
        "",
        f"Next-week y after the top fifth of m (m >= {q * 100:.2f}%): mean"
        f" {top.mean() * 100:+.2f}% ({len(top)} weeks); after the rest {rest.mean() * 100:+.2f}%"
        f" ({len(rest)} weeks). The same-week row's slope is m per unit of return (reversed axes).",
        "",
    ]
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
