"""Parse Shiller's monthly S&P 500 dividends (cached download) into a small CSV.

    uv run --with xlrd python -I research/lib/survey4_shiller.py <cache_root>

Reads `<cache_root>/shiller/2026-11-12/ie_data.xls` (untrusted download, read as data only) and
writes `<cache_root>/derived/survey-4/shiller_div.csv` with columns `month` (YYYY-MM) and `div`
(Shiller's annual dividend rate, index points). Prints only counts and the first/last month.
Used by `idea_survey4_carry.py` for the S&P 500 index's carry (card `cards/ts-carry.md`).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import xlrd  # type: ignore[import-untyped]


def main() -> None:
    root = Path(sys.argv[1]).expanduser()
    book = xlrd.open_workbook(str(root / "shiller" / "2026-11-12" / "ie_data.xls"))
    sheet = book.sheet_by_name("Data")
    rows = []
    for i in range(sheet.nrows):
        v = sheet.row_values(i)
        if not isinstance(v[0], float) or not isinstance(v[2], float):
            continue
        year = int(v[0])
        month = round((v[0] - year) * 100)
        if not 1 <= month <= 12 or v[2] <= 0:
            continue
        rows.append((f"{year:04d}-{month:02d}", v[2]))
    out = root / "derived" / "survey-4"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "shiller_div.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "div"])
        w.writerows(rows)
    print(f"{len(rows)} months, {rows[0][0]} .. {rows[-1][0]}")


if __name__ == "__main__":
    main()
