# weather-2: CPC 6-10 / 8-14 day outlook revisions and natural gas

Lane weather-2, 2026-11-19, branch `weather-2` (from `weather-1`). Follow-up suggested by
weather-1 (`research/weather-1.md`): the realised heating-degree-day surprise is dead
because the market trades the forecast, so test the forecast revision itself.

## 1. Feasibility (no prices loaded)

Question: is there a keyless archive of NOAA CPC 6-10 and 8-14 day temperature outlooks,
numeric (probabilities or gridded anomalies) and with issue dates, covering at least 10
winters before the held-out cut (2025-11-09)?

**Answer: yes, from September 2012. 13 train winters (2012-13 .. 2024-25). Feasible.**

- **Source:** `https://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/`, files
  `610temp_YYYYMMDD.zip` and `814temp_YYYYMMDD.zip` (ESRI shapefiles, keyless, public
  domain). Each holds the official outlook as nested polygons in lon/lat (NAD83) with
  attributes `Fcst_Date` (issue date), `Start_Date`, `End_Date`, `Prob` (33, 40, 50, 60,
  70, 80, 90) and `Cat` (Above / Below; equal-chances areas have no polygon).
- **Coverage (directory listing, 2026-11-19):** 610temp 4,969 issues, 814temp 4,971, both
  first 2012-09-11, last 2026-11-18 (only issues <= 2025-11-09 will be read). Per year:
  2012 77, 2013 252, 2014 ~310, 2015 onward 362-366. So weekdays only in the first winter
  and a half (2012-13 and most of 2013-14), daily including weekends from 2014-15 on. Only
  two gaps longer than four days, both in September 2013 (5 days each), outside the season.
- **Issue time:** CPC issues the 6-10 and 8-14 day outlooks once a day around 3 pm US
  Eastern. File modification times on the server agree: of 4,969 6-10 files, 4,931 were
  written on the issue date, 3,032 in the 19:00 hour and 1,745 in the 20:00 hour (server
  clock, consistent with UTC: 3 pm EDT / 3 pm EST), a few later; 38 were written 1-4 days
  late (re-uploads; the attribute `Fcst_Date` is the issue date). So an outlook dated D is
  public at about 3 pm ET on D, before the 4 pm equity close but after the 2:30 pm NYMEX
  gas settlement. The test below therefore never enters before the next session's open.
- **Earlier data:** the same directory has `610tempabv_/bel_` files for 2011-01 and
  2012-01 .. 2012-10 only (189 issues, a different two-file layout); the CPC web archive of
  map images (`/products/archives/short_range/`) refuses scripted access (HTTP 403) and is
  images, not numbers. Nothing numeric and keyless reaches 2007. Not used.
- **Weighting by gas-heated homes:** CPC's utility-gas-weighted degree-day files already
  used by weather-1 give daily HDD for the 9 Census divisions and a CONUS row that is their
  gas-household-weighted mean. The 9 division weights can be recovered from those files
  (constrained least squares, CONUS on divisions, years before the sample) and the
  outlook evaluated at Census state population centroids grouped by division.

Verdict: feasible with 13 winters (fewer than weather-1's 18). Next: the card, written and
pushed before any price is loaded.
