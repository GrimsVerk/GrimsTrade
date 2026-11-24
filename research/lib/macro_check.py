"""Look-ahead check of the macro layer on the real cache.

    uv run python research/lib/macro_check.py

For each revised series and 60 dates, the fast feature equals the feature recomputed from a
brute-force snapshot of the vintage a reader saw the day before; market features equal the value
of the last observation strictly before the day. Prints a few readings per feature.
"""

from __future__ import annotations

import math
import time
from datetime import date, timedelta

import macro


def main() -> None:
    t0 = time.time()
    f = macro.features()
    print(f"features loaded in {time.time() - t0:.1f}s")
    days = [date(1995, 1, 3) + timedelta(days=173 * k) for k in range(60)]
    for series, fn in (("CPIAUCSL", macro.yoy), ("M2SL", macro.yoy), ("WALCL", macro.yoy_weekly),
                       ("UNRATE", macro.change_3m)):  # fmt: skip
        recs = macro.vintage_records(series)
        step = macro.vintage_feature(recs, fn)
        bad = 0
        for d in days:
            snap = macro.snapshot(recs, d - timedelta(days=1))
            want = fn(snap, sorted(snap)) if snap else math.nan
            got = step.at(d)
            bad += not ((math.isnan(want) and math.isnan(got)) or abs(want - got) < 1e-12)
        print(f"{series}: {len(days) - bad}/{len(days)} dates match the brute-force vintage")
    t10 = macro.market_records("T10Y2Y")
    bad = 0
    for d in days:
        prior = [r for r in t10 if r.obs < d]
        bad += prior[-1].value != f.curve.at(d)
    print(f"T10Y2Y: {len(days) - bad}/{len(days)} dates use the last observation before the day")
    for d in (date(2000, 6, 30), date(2008, 9, 30), date(2022, 9, 30)):
        print(d, {k: round(v.at(d), 2) for k, v in vars(f).items() if isinstance(v, macro.Step)})


if __name__ == "__main__":
    main()
