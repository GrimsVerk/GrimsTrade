# Data wide 1: keyless sources that could carry F1/F2 doses

Research run data-wide-1, 2026-11-19. Branch `data-wide-1` (from `wide-11`), draft PR into
`wide-11`. Data survey only: no candidate written, no gate, no backtest, no return statistic,
no correlation with any price. Weather and climate data are out of scope (another lane).

**In one paragraph.** 23 free keyless sources inventoried across geophysics, geopolitics,
banking, central-bank operations, epidemiology, energy, shipping, cyber, regulation and crypto
(plus 8 that refused a scripted client and the signup/paid ones, listed so nobody retries
blindly); 9 verified by a download into the cache (counts, spans, gaps, release lags in
`results/data-wide-1.md`); loaders with offline tests for 4 (`lib/datawide1.py`). Best F1/F2
doses by the rule below: **(1) the daily geopolitical risk index** (1985-, no gaps, archived
vintages since 2022), **(2) FDIC bank failures** (1934-, closures on Friday evenings without
notice), **(3) Japan MOF FX intervention** (1991-, 389 operation days in 35 episodes, a direct
Treasury flow). The purest by construction is **USGS earthquakes** (1900-, nothing about it
follows prices) but its reach into the gym's assets is indirect. Every dose source has a
caveat a card must carry: GPR and FluView values are revised (use vintages), earthquake
magnitudes are the reviewed ones, MOF daily detail is published a quarter late, FDIC failures
cluster in two episodes (1980s-90s, 2008-12), DefiLlama's curation grew over time.

## Why

wide-11's filters ask for a dose that is **F1 not announced** (an unscheduled flow, or a
premium) and **F2 not price-driven** (the dose does not follow the asset's own prices at any
horizon up to a year). Most sources the project has read so far fail one of them: schedules
(Treasury auctions, Fed purchase schedules, index lists) fail F1; positioning, issuance and
attention (COT, stablecoin supply, pageviews) fail F2. This run looks for public keyless
series whose dose is set by something outside markets.

## Already in the project (not repeated)

From `docs/data-sources.md` on branch `data-search-1` and the wide/survey lanes: exchange
bars, funding and open interest, FRED/ALFRED, Treasury yield curve and auctions
(fiscaldata), NY Fed operations, CFTC COT, Cboe put/call, Ken French, Shiller, Coin Metrics,
blockchain.com hash rate, Fear & Greed, GDELT events (30 files probed), GFZ Kp/Ap, NHC
hurricane tracks, CPC ENSO, Wikimedia pageviews, DefiLlama stablecoins.

## Inventory

Every row was probed from this machine on 2026-11-19 with a plain scripted client and a generic
User-Agent (no key, no account, no cookie), unless marked otherwise. `[memory]` marks a fact
taken from memory and not re-read tonight; `[unverified]` a fact not checked at all.

**Ranking rule (fixed before any download).** Score = (F1 + F2) x H x R x M.
- F1, F2: 2 = passes by construction; 1 = passes only with a split or a control (planned vs
  unplanned, seasonal norm removed, price-path controls); 0 = fails.
- H, history usable for a gate: 3 = 30+ years, 2 = 15-30, 1 = 8-15, 0.5 = under 8 (the
  wide-11 post-sample point needs 8 train years after the latest source sample).
- R, reliability: 1 = official agency, documented interface; 0.8-0.9 = academic or agency
  with known caveats (revisions, format breaks); 0.6-0.7 = curated by an aggregator or
  machine-coded, no vintages.
- M, reach: 1 = the dose plausibly forces a flow in an asset the gym holds (SPY, QQQ, GLD,
  TLT, BTC, ETH, or the research book's ETFs); 0.5 = indirect (a sector or commodity the
  research book holds only partly); 0.25 = remote.

No score uses any price or return.

| # | Source (what) | Licence / automated use | History | Frequency | Release lag | F1 (why) | F2 (why) | Effort | H | R | M | Score |
|---:|---|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1 | **Geopolitical Risk index (Caldara-Iacoviello)** `matteoiacoviello.com/gpr.htm` (XLS/DTA) | free, cite AER 2022 and the download date; static files | daily 1985- (10 papers), monthly 1900-, 44 country indexes | daily values, file updated Mondays (monthly file on the 1st) | up to 7 days; **daily vintages since 2022-02-24 on the authors' GitHub** (`gpr_archive_files`) | **2**: share of newspaper articles on war, terror, nuclear threats; unscheduled | **2**: counts war/terror words, not market words; caveat: wars move oil, so oil-asset tests need an oil control | low (XLS needs `xlrd`, or the DTA) | 3 | 0.8 | 1 | **9.6** |
| 2 | **FDIC bank failures** `banks.data.fdic.gov/api/failures` (JSON/CSV) | US public domain; documented API, no key | 1934- (4,117 failures) | event | same evening: closures are announced Friday after the close | **2**: regulators close banks without notice | **1**: failures follow rate rises and the bank's own stock with lags (SVB 2023); for TLT/SPY the bank's price is not the asset's own, but waves cluster after crashes: controls for past 52-week returns | low | 3 | 1 | 1 | **9.0** |
| 3 | **Japan MOF FX intervention** `mof.go.jp/english/policy/international_policy/reference/feio/` (CSV, Shift-JIS) | Japanese government terms (CC BY 4.0-compatible) `[memory]`; static file | 1991-04- (daily amounts) | event | monthly total on the month's last business day; daily detail each quarter | **2**: operations are not pre-announced (several were "stealth") | **1**: leans against the yen (fails for USDJPY); for TLT (reserves sold to fund yen buying) it passes only with USDJPY and yield controls | low | 3 | 1 | 1 | **9.0** (few episodes) |
| 4 | **GDELT 1.0 daily event files** `data.gdeltproject.org/events/` | open, cite GDELT; static files | 1979- (yearly then monthly files to 2013-03, daily after) | daily | next morning | **2**: machine-coded events (CAMEO 18-20: assault, fight, mass violence) | **2**: event coding does not read markets; source count drifts up, so normalise by all events | high (GBs; 30 v2 files already in cache) | 3 | 0.7 | 1 | **8.4** |
| 5 | **EPU daily (Baker-Bloom-Davis)** `policyuncertainty.com/media/All_Daily_Policy_Data.csv` | free, cite; static file | daily 1985- | daily | 1 day | **2** | **1**: "uncertainty" coverage rises after market falls; heavily studied (fails "unseen") | low | 3 | 0.8 | 1 | 7.2 |
| 6 | **USGS ComCat earthquakes** `earthquake.usgs.gov/fdsnws/event/1/query` (CSV/GeoJSON) | US public domain; documented FDSN API, 20,000 events per query | 1900- (M >= 6; complete globally from about 1963 `[memory]`); M >= 5 complete from 1973 | event, minutes | minutes; magnitudes revised later (`updated` column) | **2**: not schedulable or forecastable | **2**: geophysics | low | 3 | 1 | 0.5 | 6.0 |
| 7 | **US Treasury TIC** `ticdata.treasury.gov/.../slt_table1.txt` | US public domain; static text | SLT 2011-, older TIC S 1977- | monthly | about 6-7 weeks | **1**: the month's flow is past when released; next month's is unknown | **1**: foreign buying follows yields | low | 3 | 1 | 1 | 6.0 |
| 8 | **IMF official gold and reserves (IL, MFS)** `api.imf.org/external/sdmx/2.1/` | IMF terms, free with attribution `[memory]`; SDMX keyless (dataflow list fetched; data query not tried) | IFS international liquidity 1950s- `[memory]`; monthly vintages since 2026-01 listed | monthly | 1-2 months | **1**: a central bank's buying is not announced; persistence carries it forward | **1**: some paused on price spikes (2024): controls | medium (SDMX keys) | 3 | 0.9 | 1 | 5.4 |
| 9 | **Delphi Epidata FluView** `api.delphi.cmu.edu/epidata/fluview/` (JSON) | CDC data US public domain; Delphi API free, key optional (anonymous rate limit) `[memory]` | US national ILI 1997-w40-; **each weekly issue kept** (`issues=`), so as-of reads are exact | weekly | about 1 week, then revised | **1**: the flu season is a calendar fact; only the deviation from the seasonal norm is unscheduled | **2**: epidemiology | low | 3 | 0.9 | 0.5 | 4.1 |
| 10 | **EIA NUC_STATUS** `eia.gov/opendata/bulk/NUC_STATUS.zip` (bulk JSON lines) | US public domain; bulk files meant for download, no key (the v2 API needs one) | daily 2007- by plant and US total | daily | about 1 day | **1**: unplanned trips are unscheduled, refuelling outages are planned and seasonal; the file does not flag which (NRC reason codes are blocked, row 25) | **2**: reactor trips are engineering events | low | 2 | 1 | 0.5 | 3.0 |
| 11 | **SNB balance sheet** `data.snb.ch/api/cube/snbbipo/data/csv/en` | free, cite SNB; keyless API | monthly 1996- (intervention quarterly since 2020) | monthly | about 1 month | **1** | **1**: leans against the franc; the SNB invests reserves partly in US equities | low | 3 | 1 | 0.5 | 3.0 |
| 12 | **NHTSA recalls** `api.nhtsa.gov`, flat files | US public domain | 1966- | event | days | **2** | **2** | medium | 3 | 1 | 0.25 | 3.0 |
| 13 | **NVD CVE API** `services.nvd.nist.gov/rest/json/cves/2.0` | US public domain; keyless at 5 requests / 30 s | 1999- | event | days | **2** | **2** but counts are administrative | medium | 3 | 1 | 0.25 | 3.0 (dose is bureaucratic) |
| 14 | **NOAA GOES X-ray flares** `ngdc.noaa.gov/stp/space-weather/.../goes/xrs/` (1975-2017 text), `services.swpc.noaa.gov/json/goes/` (recent) | US public domain | 1975- | event | minutes | **2** | **2** | medium (format break 2017) | 3 | 0.8 | 0.25 | 2.4 (geomagnetic storms already died, W16) |
| 15 | **Federal Register API** `federalregister.gov/api/v1/` | US public domain; documented API, no key | 1994- | daily | public inspection the day before | **1**: most rules are pre-announced (Unified Agenda, inspection); executive orders less so | **2** mostly | low | 3 | 1 | 0.25 | 2.25 |
| 16 | **USAspending** `api.usaspending.gov` | US public domain; documented API | FY2008- | daily | days | **1**: large awards are announced the day they are made; the September spike is calendar | **2** | medium | 2 | 1 | 0.25 | 1.5 |
| 17 | **OpenSanctions (OFAC SDN and others)** `data.opensanctions.org` | CC BY-NC 4.0 (non-commercial: fits this project) | listing dates partly back to the 1990s; reliable `first_seen` only recently | daily | 1 day | **2** | **2** | medium | 1 | 0.7 | 0.5 | 1.4 |
| 18 | **openFDA enforcement / recalls** `api.fda.gov` | CC0; keyless 1,000 requests a day | 2004- (enforcement 2012-) | event | days | **2** | **2** | low | 1 | 1 | 0.25 | 1.0 |
| 19 | **DefiLlama hacks** `api.llama.fi/hacks` (JSON) | free open API; no key (other endpoints paid: `/raises` answered 402) | 2011- (1,367 events; under 10 a year before 2018, 359 in 2026) | event | days; curated and back-filled, no vintages | **2**: hacks are not announced | **1**: the sum stolen scales with token prices and value locked: controls | low | 0.5 | 0.6 | 1 | 0.9 (best reach for BTC/ETH) |
| 20 | **IMF PortWatch chokepoints** ArcGIS `services9.arcgis.com/weJ1QsnbMYJlCHdG/.../Daily_Chokepoints_Data` | IMF data, free with attribution `[unverified]`; public ArcGIS REST, 2,000 rows a page | daily 2019- (28 chokepoints, transits by vessel type, capacity); daily port calls (5.95 M rows); disruptions list (132) | daily, updated weekly | 4-10 days | **2**: attacks and closures are unscheduled | **2**: transit counts are not set by asset prices | medium | 0.5 | 0.9 | 0.5 | 0.9 |
| 21 | **NY Fed repo / standing repo take-up** `markets.newyorkfed.org/api/rp/` (host known from wide-10; new series) | free, keyless | 2019- for current operations | daily | same day | **2**: take-up is the banks' choice on the day | **1**: follows repo-rate spikes (not an asset's own price) | low | 0.5 | 1 | 0.5 | 0.75 |
| 22 | **CISA KEV** `cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv` | US public domain | 2021-11- | event (daily adds) | same day | **2** | **2** | low | 0.5 | 1 | 0.25 | 0.5 |
| 23 | **IODA internet outages** `api.ioda.inetintel.cc.gatech.edu/v2/` | academic, free for research `[memory]` | events API answers back to 2012 ranges, depth unverified | event | hours | **2** | **2** | medium | 0.5 | 0.7 | 0.25 | 0.35 |

**Not usable keyless from here tonight (recorded so nobody retries blindly):**

| # | Source | What happened | Note |
|---:|---|---|---|
| 24 | SEC EDGAR indices, fails-to-deliver files | 403 | SEC asks automated clients for a name and e-mail in the User-Agent; this public research repo uses a generic one, so not fetched |
| 25 | NRC daily power reactor status (planned vs unplanned reasons) | 403 | EIA NUC_STATUS (row 8) carries the capacity part without the reasons |
| 26 | BLS work stoppages | 403 | same policy as SEC |
| 27 | UCDP GED conflict events API | 401 | now needs an access token |
| 28 | Smithsonian GVP volcano database | 403 | |
| 29 | CPSC recalls | 403 | |
| 30 | mempool.space (hash rate, difficulty) | TLS reset from this machine | blockchain.com / Coin Metrics already carry hash rate |
| 31 | USDA FAS PSD, ERS | DNS failure tonight | retry later |

**Signup needed (skipped, no accounts):** ACLED (conflict events), EM-DAT (disasters), NASA
FIRMS (fires; weather lane anyway), NASA Earthdata (Black Marble night lights), Cloudflare Radar
(outages), ENTSO-E (European grid), EIA API v2 (the bulk files above need no key), Global
Terrorism Database.

**Paid (listed, never bought; prices from memory, not verified tonight):** DefiLlama Pro API
(about 300 USD a month; `/raises` answered 402), Glassnode (about 30-800 USD a month by tier),
Kpler / Vortexa ship and cargo tracking (enterprise, five figures a year), MarineTraffic API
(from about 100 USD a month), Baltic Exchange freight indices (subscription), RavenPack news
analytics (enterprise), Spire Maritime AIS (enterprise).

**Excluded by the filters before any download:** Wikipedia pageviews and Google Trends
(attention follows price: F2), ICI fund flows and ETF shares outstanding (flows follow returns:
F2), FINRA margin debt (F2), BoJ ETF purchases (bought on down mornings: F2), SPR releases and
OPEC meetings (announced: F1), index changes (published lists: F1), US Mint coin sales (follow
price: F2), weather and climate (another lane).

## Verified downloads

Nine sources were downloaded on 2026-11-19 by `scripts/fetch_datawide1.py` into the shared
git-ignored cache (`data-wide-1/<source>/<date>/` under the cache root of
`research/macro.local.json`; sha256 per file in the cache's `manifest.jsonl`), about 50 MB in
all. They were read as data only (`python -I`), never executed, never committed. The
description script `lib/datawide1_check.py` writes `results/data-wide-1.md`; it reads no price
and computes no return or correlation. What it found, per source:

| Source | Rows | Span | Gaps | Release, as-of | Surprise for a card |
|---|---:|---|---|---|---|
| USGS M >= 6 (and M >= 5 since 1973) | 14,487 (89,674) | 1900-01-05 .. 2026-11-18 | no year without an M >= 6; longest pause since 1973: 39 days | minutes; **reviewed magnitudes only** (7,428 of 7,456 M >= 6 rows since 1973 updated 30+ days after the event) | M >= 7.5 since 1973: 236 events; M >= 8: 40 |
| GPR daily | 15,295 | 1985-01-01 .. 2026-11-16 | none (every calendar day) | weekly file; Monday vintages carry that Monday; **one Monday vintage (2026-11-09) still ended a week earlier**; the 2022-02-24 vintage differs from today's values by a median 2.7% (later vintages: under 0.5% on all but 22-61 days) | values before 2022 are only available in today's revised form |
| EIA NUC_STATUS | 3 US series x 7,262 days; 174 generator series of each kind | 2007-01-01 .. 2026-11-18 | none | daily | no planned/unplanned flag |
| FluView US ILI | 1,424 weeks | 1997-w40 .. 2026-w44 | **1998-2002: 33 weeks a year** (season only) | weekly; issue kept, revisions up to 0.07 points | rows before issue 201352 are a back-fill |
| DefiLlama hacks | 1,367 events | 2011-06-19 .. 2026-11-18 | 1-8 a year before 2018; 359 in 2026 alone | no publication date per event | counts follow curation effort, not only hacking |
| FDIC failures | 4,117 | 1934-04-19 .. 2026-07-17 | longest pause since 1990: 952 days (2004-2007) | **562 of 594 closures since 2000 on a Friday** | two big episodes hold most events |
| PortWatch chokepoints | 80,528 (28 x 2,876 days) | 2019-01-01 .. 2026-11-15 | none | weekly refresh, last day 4 days old | under 7 years |
| MOF intervention | 389 operation days | 1991-05-13 .. 2026-08-03 | 35 episodes; 2010s: 8 days | daily rows sum to every one of 142 published quarter totals | 338 days sold yen (1991-2004, buying dollar assets), 45 bought yen (1998, 2022-2026) |
| CISA KEV | 1,786 | 2021-11-03 .. 2026-11-18 | 287 rows on the first day (the initial catalogue) | daily | under 5 years |

What changed in the inventory after the downloads: DefiLlama's history starts in 2011 but holds
too few events before 2018 for a gate (H stays 0.5); the MOF file is cleaner than expected
(totals reconcile); GPR's release can slip a week, so its "available on" rule is conservative
(below). No score in the table moved enough to change the top three.

## Loaders

`research/lib/datawide1.py` (pattern of the other research loaders: plain functions over
text/bytes/rows, so tests need no network and no cache), tests `tests/test_datawide1.py`
(10 tests, offline, literal samples copied from the real formats):

- **USGS** `parse_usgs_csv`, `merge_quakes` (one row per event id, the latest revision wins),
  `load_quakes(folder)`, `daily_max_magnitude(quakes, min_mag)` by UTC day.
- **GPR** `parse_gpr_rows` (columns found by name), `read_gpr_xls` (needs
  `uv run --with xlrd`; xlrd is not a project dependency), `gpr_available_on(day)`: the first
  Wednesday at least 9 days after the day (covers one slipped weekly update); from 2022-02-24
  a card should read the archived vintages (`gprvint` in the fetch script fetches six; the
  archive has every weekly file).
- **FDIC** `parse_fdic_failures`, `failure_available_on(day)` = next calendar day (evening
  announcements).
- **MOF** `parse_mof_csv` (Shift-JIS; year and month carried down; quarter-total rows
  skipped), `mof_quarter_totals`, `monthly_totals(signed)`, `mof_month_available_on` (day
  after the month end: the month's total is published on its last business day),
  `mof_daily_available_on` (quarter end + 45 days: a default, the exact quarterly publication
  dates were not checked).

Not loaded (format is simple, left for the lane that needs them): NUC_STATUS (JSON lines in a
zip), FluView (JSON with `issue`), DefiLlama hacks (JSON), PortWatch (ArcGIS pages), KEV (CSV).

## For wide-13 (ideas only, nothing tested)

Each is a mechanism a source could feed, written against the filters; none has been scored,
looked at against prices, or carded. Literature checks are still to do.

1. **GPR acts vs threats as a safe-haven premium (GLD, TLT).** A risk premium (F1 b): after
   adverse acts (war starts, escalation) safe assets earn a premium over the following weeks
   for bearing the risk of escalation; threats without acts are priced on the day. Caveat:
   Caldara-Iacoviello (2022) is the source sample; post-sample years from 2022 are few.
2. **GPR and the oil risk premium (DBC, XLE).** Same dose, commodity side; needs an oil-supply
   control because wars move oil directly.
3. **Bank-failure Fridays and the Monday flight to quality (TLT, IEF; XLF).** F1 by
   construction (no notice); F2 with controls for the past 4/52-week return of SPY and XLF.
   Dose: failed assets as a share of bank assets; few independent episodes, so the placebo
   family must be shifted calendars, not permutations.
4. **MOF dollar buying and Treasury purchases (TLT, IEF).** In 1991-2004 the MOF sold yen on
   338 days; the dollars were invested in Treasuries over the following weeks. The monthly total
   is public at month end, the investment flow follows it: an unscheduled flow into Treasuries
   whose size is known before the flow completes. F2: intervention answers USDJPY, so USDJPY
   and US yield changes are the controls. The 2022-2026 yen support (45 days) is the reverse:
   Treasury sales.
5. **Large earthquakes near Japan and yen repatriation (TLT, SPY).** Insurers and investors
   repatriate after a big domestic disaster (2011 is the known case); dose: M >= 7 within a
   radius of Japan; pure F1/F2, few events.
6. **Earthquakes in copper and oil regions (DBC).** Supply shocks in Chile/Peru (copper) or
   the Gulf; pure F1/F2; reach through a broad commodity fund is diluted.
7. **Nuclear outages above the seasonal norm and gas burn (DBC, XLU).** Dose: US outage % minus
   the same calendar week's 5-year mean, which removes most planned refuelling (F1 by the
   split); F2 by construction.
8. **Flu above the seasonal norm and absences (XLV, SPY).** Dose: ILI minus same-week 5-year
   mean, read at its issue (vintages); weak reach.
9. **Stolen coins and forced laundering sales (ETH vs BTC).** Hackers sell or bridge stolen
   ETH within days; dose: USD stolen on Ethereum minus returned funds; F2 with controls (the
   value stolen scales with prices and value locked). Counts drift with curation, so use
   sizes, not counts.
10. **Chokepoint closures and the shipping/oil premium (DBC).** Dose: Suez/Bab el-Mandeb/Hormuz
    transits below their 1-year norm; pure F1/F2 for attacks; under 7 years of history, so a
    lead at most, never a gate before 2027.
11. **Central-bank gold buying and GLD.** IMF monthly official gold holdings (dataflow `IL`
    keyless, not yet queried); persistence makes last month's buying a forecast of this
    month's flow; F2 with controls (some buyers paused on price spikes).
