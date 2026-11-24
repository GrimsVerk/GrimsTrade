"""Lane wide-7, step 3: event-study gate for W12 `rmd-december` (research/wide-7.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).

Run: `uv run python -I research/lib/wide7_rmd.py`  (DRY=1: year counts only)
Output: research/results/rmd-december.md
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide7_rules as r  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "rmd-december.md"
DRY = bool(os.environ.get("DRY"))
SERIES = [("SPY", 1993, 2024), ("TLT", 2002, 2024), ("GSPC", 1975, 2024)]


def table(sym: str, lo: int, hi: int, first: bool = False) -> dict[int, tuple[float, float]]:
    bars = harness.load_history("train", syms=[sym])[sym]
    days = [b.date for b in bars]
    logc = np.log(np.array([b.close for b in bars]))
    out = {}
    for y in range(lo, hi + 1):
        v = r.december_window(days, logc, y, first=first)
        if v is not None:
            out[y] = v
    return out


def main() -> None:
    tabs = {s: table(s, lo, hi) for s, lo, hi in SERIES}
    if DRY:
        for s, t in tabs.items():
            print(s, len(t), min(t), max(t), [y for y in r.RMD_WAIVED if y in t])
        return
    res = {}
    for s, t in tabs.items():
        ex = {y: v[0] for y, v in t.items()}
        raw = {y: v[1] for y, v in t.items()}
        first = {y: v[0] for y, v in table(s, min(t), max(t), first=True).items()}
        res[s] = (
            r.pair_permutation(ex, r.RMD_WAIVED),
            r.pair_permutation(raw, r.RMD_WAIVED),
            r.pair_permutation(first, r.RMD_WAIVED),
            ex,
        )
    (d_spy, p_spy), (d_tlt, _) = res["SPY"][0], res["TLT"][0]
    passed = d_spy > 0 and p_spy <= 0.05 and d_tlt > 0
    out = [
        "# RMD December: event-study gate (wide-7, W12)",
        "",
        "Rule: `research/wide-7.md` (pushed before this ran). Script `research/lib/wide7_rmd.py`.",
        "Excess = log return over the last ten December sessions minus ten times the year's",
        "mean daily log return on its other sessions. D = mean over the RMD waiver years (2009,",
        "2020) minus mean over the other years, in %; p = exact one-sided permutation over all",
        "pairs of years.",
        "",
        "## Gate",
        "",
        "| Test | D, % (p) | Needed |",
        "|---|---:|---|",
        f"| SPY excess, Decembers 1993-2024 | {d_spy * 100:+.2f} ({p_spy:.3f}) "
        "| D > 0, p <= 0.05 |",
        f"| TLT excess, Decembers 2002-2024 | {d_tlt * 100:+.2f} | D > 0 |",
        "",
        f"**Gate: {'PASS' if passed else 'fail'}.**",
        "",
        "## Shown",
        "",
        "| Series | Years | Last ten, excess | Last ten, raw | First ten, excess (placebo) |"
        " 2009 excess (rank) | 2020 excess (rank) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for s, _, _ in SERIES:
        (d1, p1), (d2, p2), (d3, p3), ex = res[s]
        order = sorted(ex, key=lambda y: -ex[y])
        cells = [f"{ex[y] * 100:+.2f} ({order.index(y) + 1} of {len(ex)})" for y in r.RMD_WAIVED]
        out.append(
            f"| {s} | {min(ex)}-{max(ex)} | {d1 * 100:+.2f} ({p1:.2f}) | "
            f"{d2 * 100:+.2f} ({p2:.2f}) | {d3 * 100:+.2f} ({p3:.2f}) | " + " | ".join(cells) + " |"
        )
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
