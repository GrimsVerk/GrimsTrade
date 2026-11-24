# Data wide 1: verification of the downloads

Script `research/lib/datawide1_check.py`, files from `scripts/fetch_datawide1.py` in
the git-ignored cache. Counts, spans, gaps, release lags only: no price, no return, no
correlation was read. Generated 2026-11-19 02:52 UTC.

## 1. USGS ComCat earthquakes

Snapshot `2026-11-19`, 7 files, 96,705 distinct earthquake rows.
- M >= 6: 14,487 events, 1900-01-05 .. 2026-11-18; per decade: 1900s 350, 1910s 684, 1920s 966, 1930s 1073, 1940s 964, 1950s 1300, 1960s 1267, 1970s 1093, 1980s 1257, 1990s 1530, 2000s 1585, 2010s 1493, 2020s 925.
- Years with no M >= 6 event: 0 ([]).
- Longest gap between M >= 6 days since 1973: 39 days (1978-09-23 .. 1978-11-01).
- M >= 5 since 1973: 89,674 events; per decade: 1970s 10977, 1980s 15800, 1990s 14627, 2000s 17234, 2010s 18411, 2020s 12625.
- M >= 6.5 since 1973: 2321 events.
- M >= 7.0 since 1973: 742 events.
- M >= 7.5 since 1973: 236 events.
- M >= 8.0 since 1973: 40 events.
- Revisions: 7428 of 7456 M >= 6 rows since 1973 were last updated more than 30 days after the event (the catalogue holds reviewed magnitudes, not first estimates).
- Magnitude types (M >= 6): {'mw': 8533, 'mww': 2105, 'mwc': 1590, 'mwb': 924, 'ms': 797, 'mb': 412}.
- Release: real time (minutes); no dated vintages, only the `updated` stamp.

## 2. Geopolitical risk, daily (Caldara-Iacoviello)

Snapshot `2026-11-19`: 15,295 daily rows, 1985-01-01 .. 2026-11-16.
- Calendar days in span 15,295; missing 0; duplicate days 0; rows with no index value 0.
- Days with 0 articles searched (N10D): 0.
- Weekday of the last row: Monday; file posted 2026-11-17 18:00 UTC (Last-Modified header).

Archived vintages (authors' GitHub): last day carried vs the vintage date, and revisions
against the current file on days both carry.

| Vintage (file date) | Weekday | Last day carried | Lag, days | Days compared | Changed by > 0.5% | Median abs change |
|---|---|---|---:|---:|---:|---:|
| 2022-02-24 | Thu | 2022-02-24 | 0 | 13,569 | 11,889 | 2.7203% |
| 2024-07-01 | Mon | 2024-07-01 | 0 | 14,427 | 61 | 0.0000% |
| 2026-07-06 | Mon | 2026-07-06 | 0 | 15,162 | 49 | 0.0000% |
| 2026-07-07 | Tue | 2026-07-07 | 0 | 15,163 | 49 | 0.0000% |
| 2026-11-02 | Mon | 2026-11-02 | 0 | 15,281 | 22 | 0.0000% |
| 2026-11-09 | Mon | 2026-11-02 | 7 | 15,281 | 33 | 0.0000% |

## 3. EIA NUC_STATUS (US nuclear outages)

Snapshot `2026-11-19`: series by kind {'OUT_PCT': 174, 'CAP': 174, 'OUT': 174}; 173 plant/generator ids; span 20070101 .. 20261118.
- `NUC_STATUS.CAP.US.D` (U.S. nuclear capacity, daily): 7,262 rows, 20070101 .. 20261118, missing 0 days.
- `NUC_STATUS.OUT.US.D` (U.S. nuclear capacity outage, daily): 7,262 rows, 20070101 .. 20261118, missing 0 days.
- `NUC_STATUS.OUT_PCT.US.D` (U.S. nuclear capacity percent outage, daily): 7,262 rows, 20070101 .. 20261118, missing 0 days.
- No planned/unplanned flag in the file; the NRC reason text (row 25 of the inventory) was not reachable.

## 4. Delphi FluView (US national ILI)

Snapshot `2026-11-19`: 1,424 weekly rows, epiweeks 199740 .. 202644.
- Years with fewer than 52 weeks (inside the span): {1998: 33, 1999: 33, 2000: 33, 2001: 33, 2002: 33}.
- Latest issue 202644, released 2026-11-13; the oldest rows carry issue 201352 (lag 847 weeks), i.e. early history is a back-fill, not a real-time vintage.
- Vintage check: issue 201001 has 14 rows; weighted ILI differs from today's value by up to 0.07 points (median 0.03): revisions are real, so a card must read `issues=`.

## 5. DefiLlama hacks

Snapshot `2026-11-19`: 1,367 events, 2011-06-19 .. 2026-11-18.
- Per year: 2011 1, 2012 3, 2013 2, 2014 6, 2015 6, 2016 5, 2017 8, 2018 31, 2019 26, 2020 46, 2021 127, 2022 185, 2023 197, 2024 217, 2025 148, 2026 359.
- With a USD amount: 1,297; bridge hacks 104; with returned funds 29.
- Top chains: {'Ethereum': 561, 'BSC': 269, 'Arbitrum': 106, 'Bitcoin': 71, 'Polygon': 69}.
- No publication timestamp per event (curated, back-filled): treat each event as known only some days later; no vintages.

## 6. FDIC bank failures

Snapshot `2026-11-19`: 4,117 failures and assistance transactions, 1934-04-19 .. 2026-07-17.
- Per decade: 1930s 312, 1940s 99, 1950s 28, 1960s 44, 1970s 79, 1980s 2036, 1990s 925, 2000s 210, 2010s 367, 2020s 17.
- Kinds: {'FAILURE': 3524, 'ASSISTANCE': 593}; funds: {'FDIC': 1644, 'FSLIC': 572, 'RTC': 747, 'BIF': 583, 'SAIF': 6, 'DIF': 565}.
- Weekday of closing since 2000: {'Fri': 562, 'Thu': 19, 'Sun': 6, 'Wed': 2, 'Mon': 2, 'Tue': 2, 'Sat': 1} (Friday-evening closures).
- Missing assets 154, missing cost 637.
- Longest gap between failures since 1990: 952 days (2004-06-25 .. 2007-02-02).

## 7. IMF PortWatch daily chokepoint transits

Snapshot `2026-11-19`: 80,528 rows, 28 chokepoints.

| Chokepoint | Rows | First | Last | Missing days |
|---|---:|---|---|---:|
| Bab el-Mandeb Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Balabac Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Bering Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Bohai Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Bosporus Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Cape of Good Hope | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Dover Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Gibraltar Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Kerch Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Korea Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Lombok Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Luzon Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Magellan Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Makassar Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Malacca Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Mindoro Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Mona Passage | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Ombai Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Oresund Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Panama Canal | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Strait of Hormuz | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Suez Canal | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Sunda Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Taiwan Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Torres Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Tsugaru Strait | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Windward Passage | 2,876 | 2019-01-01 | 2026-11-15 | 0 |
| Yucatan Channel | 2,876 | 2019-01-01 | 2026-11-15 | 0 |

## 8. Japan MOF FX intervention

Snapshot `2026-11-19`: 389 operation days, 1991-05-13 .. 2026-08-03; 142 published quarter totals.
- Daily rows summed per quarter vs the published totals: 0 quarters differ by more than 2 (x 100 million yen).
- Yen bought (support) days 45, yen sold days 338, yen not involved 6.
- Episodes (operation days more than 30 days apart start a new one): 35; per decade (days): 1990s 206, 2000s 162, 2010s 8, 2020s 13.

## 9. CISA KEV

Snapshot `2026-11-19`: 1,786 rows, added 2021-11-03 .. 2026-11-18; per year 2021 311, 2022 555, 2023 187, 2024 186, 2025 245, 2026 302. The first day holds the initial catalogue (287 rows on 2021-11-03).

