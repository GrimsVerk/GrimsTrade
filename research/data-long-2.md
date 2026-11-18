# Data long 2: gold loader, cross-check, trend-where on long bonds and gold

Lane `data-long-2`, 2026-11-18, branch `data-long-2` (from `data-long-1`, draft PR #48).
Research only, fake money, no raw data committed.

## 1. Gold loader

`research/lib/long_gold.py` reads `<cache_root>/datahub-gold/<YYYY-MM-DD>/monthly.csv` (newest
dated folder; download by hand from https://datahub.io/core/gold-prices/r/monthly.csv, PDDL).
Offline test `tests/test_long_gold.py` on a five-row fixture.

Spans read from the copy fetched 2026-11-18 (HTTP 200, 35,747 bytes, sha256
`f20720f3413b3dd114cd116951516f0fab577ff8c91e102a3a92549582ea9608`), parsed with `python -I`:

- 2,326 months, 1833-01 to 2026-10, consecutive (no gaps, no duplicates).
- 670 monthly returns from `FREE_FROM` = 1971-01 to 2026-10.
- Before 1971 the price moves in only 88 of ~1,650 months (fixed USD price 20.67, then 35 from
  1934; the 1968-70 two-tier market wiggles between 35 and 43). Not market risk.
- Prices are whole dollars into the 1970s and look like monthly averages, not month-end closes
  (checked in section 2).

Other caches used here (same root, not committed): Shiller `shiller/ie_data.xls` (sha256
`89c5c210...6d7`, lane data-long-1), Damodaran `damodaran/2026-11-18/histretSP.xls` (HTTP 200,
527,872 bytes, sha256 `28b81109...49c69`).
