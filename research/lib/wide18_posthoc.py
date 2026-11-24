"""wide-18 post hoc (after the one real run; not a try, no rows): where `vclock12`'s window sat.

    uv run --with numpy python research/lib/wide18_posthoc.py

For each of the six, the share of Fridays (1994-02-01 .. 2025-10-31, once eligible) on which
the variance-time window was at the quarter-year floor, under a year, over a year or at the
two-year cap, and the median window in years.
"""

from __future__ import annotations

from datetime import date, timedelta

import common as c
import numpy as np
from wide18 import LAST, bars_per_year, vclock_window


def main() -> None:
    ctx = c.ctx("six")
    print("| Asset | Fridays | At floor (3 m) | Under 1 y | Over 1 y | At cap (2 y) | Median, y |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    d = ctx.start + timedelta(days=(4 - ctx.start.weekday()) % 7)
    fridays: list[date] = []
    while d <= LAST:
        fridays.append(d)
        d += timedelta(days=7)
    for s in ctx.panel.syms:
        b = bars_per_year(s)
        ks = []
        for f in fridays:
            v = ctx.panel.view(c.harness.decide_time(f))
            if not c.eligible(v, s):
                continue
            k = vclock_window(v.logret(s), b)
            if k:
                ks.append(k / b)
        x = np.array(ks)
        print(
            f"| {s} | {len(x)} | {(x <= 0.25 + 1e-9).mean():.0%} | {(x < 1).mean():.0%} | "
            f"{(x > 1).mean():.0%} | {(x >= 2 - 1e-9).mean():.0%} | {np.median(x):.2f} |"
        )


if __name__ == "__main__":
    main()
