# Data wide 2: keyless sources that add independent episodes

Lane `data-wide-2`, 2026-11-25 (night, UTC). Branch `data-wide-2`. Data survey only: no
strategy, no backtest, no return statistic of any rule. Keyless public data only; no accounts,
keys or sign-ups; paid sources listed with their price only.

## The answer on one screen

**The stock wall is real for monthly data after 1927. Pre-1927 sovereign bonds and stocks, and
pre-1871 UK and US series, are not used up.** Counted against everything the project has
scored (`SEEN` in `lib/datawide2.py`: the 41 stock markets, Shiller, NBER ch. XI, French
country files, the JST annual equity panel scored by insure-1870-1, data-long-3 bonds and
currencies, PPI commodities), the sources cached here add (union over sources, one
country-year once per asset class; `results/data-wide-2.md`):

| Asset | New market-years | Falls of 25%+ with the trough in a new year |
|---|---:|---:|
| Government bonds (77 sovereigns in London 1869-1929; UK consols 1753-; Norway 1820-; Swiss 1943-) | 2,946 | 88 |
| Stocks (London-listed country indices 1869-1929; UK 1709-1866; US 1815-1870; Russia 1865-1917) | 1,620 | 94 |
| Currencies (USD/GBP 1791-1970; NOK 1819-1970) | 379 (was 367 before the #PRNUM date fix) | 5 |
| Commodity futures (AQR aggregate 1877-1912) | 36 | 2 |

What decides the ranking:

- **Before 1927 (e4-indep-1's rule: no time overlap with the 41 stock markets).** The best new
  pool is the **Yale ICF London Investor's Monthly Manual (IMM)**: monthly prices 1869-1929 of
  every security quoted in London. Sterling country indices give 1,289 new stock market-years
  before 1927 in 50 countries, with 78 falls of 25%+. If a month needs 3+ quoted shares, that
  drops to 540 years in 23 countries and 22 falls. The clean IMM file is cut off at Excel's
  row limit (1,048,575 rows). Government bonds are complete: checked against the original
  "British, colonial and foreign stocks" section, 220k rows. Common stocks are not complete.
  For bonds, the IMM gives 77 sovereign borrowers and 2,463 new bond market-years before 1927,
  with 82 falls. With 3+ quoted bonds a month it gives 1,162 years and 32 falls. These are
  defaults and wars such as Egypt and Turkey 1876-77, Peru 1877 and 1884, Argentina 1891,
  Mexico 1893, Greece 1897, Brazil 1898, Russia 1922 and France 1926. They cluster in 1876-78
  and 1920-21, so they are fewer independent events than the count.
  **Owner decision needed:** Yale's terms say the data are "supplied solely for academic
  research purposes; any commercial use or redistribution without the authorization of the
  authors and the International Center for Finance at Yale is prohibited". This project is open
  research with fake money and publishes only statistics. Whether that allows using the data
  to select or test trading rules is the owner's call, or needs Yale's authorization. This
  lane does not decide it, and no rule may be run on the data until then.
- **New calendar years.** These are years that no scored series of the asset class covers at
  all, the strictest form of independence:
  - stocks 1709-1866: the BoE UK share index (158 years) and the NYSE 1815-1870;
  - bonds 1753-1870: UK consols and Norway from 1820;
  - currencies 1791-1970: USD/GBP and NOK.

  These are the only additions that share no crash calendar with what has been scored. All of
  them except the NYSE are free of Yale's terms (BoE: Open Government Licence; Norges Bank: cite).
- **JST changes the count a lot.** With insure-1870-1's annual JST equity panel (16 countries
  1871-2020) counted as seen, the Norway (1914-2001) and Swiss (1924-1997) monthly stock
  indices add no new market-years. They add monthly detail inside years that were already
  scored, not new episodes.

**Ranking by usable independent market-years:**
1. Yale IMM government bonds: 1,162-2,463 bond years before 1927. Fetched; owner decision needed.
2. Yale IMM stocks: 540-1,289 stock years before 1927. Fetched but truncated; the complete raw
   sections are 120 MB more. Owner decision needed.
3. NBER Macrohistory ch. IV single-commodity prices: 101 series with 10+ years before 1913,
   about 2,702 commodity-years. These figures come from the series titles on the chapter page
   (doc), not from the files. **Manual download only** (robots.txt).
4. BoE millennium monthly sheet: 707 new market-years, 540 of them before 1927, and 262 new
   calendar years. Cached; Open Government Licence.
5. Norges Bank government bond yields from 1820 (96 new years, 46 new calendar years) and
   exchange rates from 1819 (199 and 152; were 187 and 140 before the #PRNUM date fix). End of
   month to 1914, monthly averages after. Fetched.
6. Yale NYSE 1815-1925 (56 new years, 52 new calendar years) and St Petersburg 1865-1917
   (50). Fetched; owner decision needed.
7. IMF IFS exchange rates (about 217 currencies from the 1950s, mostly long pegs) and OECD
   share prices (47 countries, 1950s on). The probe listings showed this coverage; the data
   are not kept. **Manual download only**: DBnomics robots.txt, OECD Cloudflare.
8. NBER ch. XI/XIII non-US bonds (17 series 1840-1940). Manual download only.
9. AQR commodity futures from 1877: one aggregate series, 36 new years. SNB bonds 1943-1981:
   12 new years.

Crypto archives add no independent market-years (one calendar, from 2010). They add
microstructure depth only.

## Sources (probed 2026-11-25, 21:15-21:45 UTC)

"Script" = robots.txt and the terms allow a scripted fetch, and it worked from this machine.
The user agent was the generic `grimstrade-research/0.1`. See the probe log for the delays
actually kept. Spans and counts are read from the files unless marked (doc).

| # | Source | URL | Licence / terms | Freq, timing | Span | Series | Script | Size | Cached |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Yale ICF, London Investor's Monthly Manual, clean file | som.yale.edu/sites/default/files/2021-12/Totaldata.zip (page: .../historical-financial-research-data/london-stock-exchange) | **academic research only; commercial use or redistribution prohibited without authorization; cite ICF Yale** (owner decision needed before rule tests) | monthly, open/high/low/late price | 1869-01..1929-12 | 1,208 govt bonds (79 countries), 1,445 common stocks shown (truncated), 1,906 corp bonds | yes (robots allow `/sites/`, crawl delay 10 s) | 10.3 MB zip, 145 MB csv | yes |
| 1b | Yale IMM original sections | .../2021-12/Stocks_new.csv.zip (govt "stocks"), Railways_new, Banks_new, Misc_new | same | monthly | 1869-1929 | complete per section | yes | 14.5 MB fetched; Misc 90 MB, Railways and Banks not fetched | Stocks only |
| 2 | Yale ICF St Petersburg / NYSE comparison | .../2021-12/SPSENYSE18651917ind.xls ; St_ Petersburg data Revised 082010.xlsx | same as 1 | monthly, USD price indices | 1865-01..1917-02 | 2 (SPSE, NYSE) | yes | 0.2 MB | yes |
| 3 | Yale ICF NYSE 1815-1925 (Goetzmann-Ibbotson-Peng) | .../2021-12/Price-Weighted-Index-Returns-2020-08-20.xls (a CSV) | same as 1 | monthly price returns | 1815-02..1925-12 | 1 index (+ 1815-1925 security file, not fetched) | yes | 67 kB | yes |
| 4 | Bank of England "A millennium of macroeconomic data" v3.1, monthly sheet | bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/a-millennium-of-macroeconomic-data-for-the-uk.xlsx | Open Government Licence v3 | monthly (mixed timing per series) | share index 1709-04.., consols 1753-08.., corp bonds 1854.., USD/GBP 1791.., PPI 1790.. to 2016-17 | 26 monthly series | yes (robots allow; HEAD 200, 27.5 MB) | 6.3 MB long CSV | yes (datahub long-CSV copy cached by jst-autocorr-2; xlsx not refetched) |
| 5 | Norges Bank Historical Monetary Statistics | norges-bank.no/globalassets/upload/hms/data/{bond_yields,fx,stockprices,shortterm_ir,cpi}.xlsx | free, cite Eitrheim, Klovland and Qvigstad (2004); disclaimer | monthly; bonds and FX to 1914 end of month | govt bond yields 1820-05..2005, FX 1819-04.., stocks 1914-01..2001 (total + 5 sectors) | 1 + 6 + 7 used | yes (crawl delay 5 s) | 1.9 MB | yes (stocks: jst-autocorr-2's copy) |
| 6 | SNB historical time series, capital market | snb.ch/dam/jcr:2478e077-fd40-4dea-88d5-33e6b60f5035/histz_km.n.xls | free, cite SNB | monthly, end of month | equity index 1924-01..1968-08 (+ sectors), SBC index 1959-1997, bond price index 1943-1981, bond yield index 1924-1943 | 2 spliced/used | yes | 5.4 MB | yes |
| 7 | AQR "Commodities for the Long Run" | images.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Commodities-for-the-Long-Run-Index-Level-Data-Monthly.xlsx | free download, copyright the authors, AQR disclosures; no robots.txt served | monthly returns | 1877-02..2025-05 | aggregates only: EW excess, spot, carry; long/short; no single commodities | yes | 0.45 MB (+ paper version 0.27 MB) | yes |
| 8 | NBER Macrohistory ch. IV Prices | nber.org/research/data/nber-macrohistory-iv-prices ; files data.nber.org/databases/macrohistory/rectdata/04/m04xxx.dat | public, cite NBER | monthly | (doc, from series titles) e.g. wheat Chicago 1841-1944, corn 1860-1951, cotton 1870-, cattle and hogs 1858-1940, copper 1860-, pig iron 1842-, GB wheat 1845-1934, Berlin wheat 1879-1935 | (doc) 312 series, 209 single commodities, 101 with 10+ years before 1913 | **no: data.nber.org robots.txt `Disallow: /`** | small (.dat, kB each) | no (manual) |
| 9 | NBER Macrohistory ch. XI/XIII non-US bonds | m11017a/b GB consol prices 1853-1934, m11019 GB fixed interest 1867-1914, m11020 DE 3.5% 1877-1925, m11021 FR 3% rentes 1873-1940, m13027 FR yields 1898-1939, m13028a-c DE yields 1870-1935, m13041a-c consol yields 1840-1938 | public | monthly | (doc) as listed | 17 | no (robots) | small | no (manual) |
| 10 | IMF IFS via DBnomics | api.db.nomics.world/v22/series/IMF/IFS (indicators ENDA_XDC_USD_RATE, FIGB_PA, FPE_IX; monthly) | IMF data free with attribution | monthly | (probe listing) FX for ~217 currencies 1950s-; 44 bond yields; 30 share indices | | **no: api.db.nomics.world robots.txt `Disallow: /`** (checked after four probe calls; those files are deleted) | | no (manual; or IMF's own portal by hand) |
| 11 | OECD MEI share prices (DSD_STES@DF_FINMARK) | sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES@DF_FINMARK (own API); DBnomics mirror | OECD CC BY 4.0 | monthly average | (probe listing) 47 countries, 1950-/55-/57- | | **no**: OECD API Cloudflare 403; DBnomics robots disallow | | no (manual via the OECD Data Explorer) |
| 12 | Riksbank Historical Monetary Statistics of Sweden | riksbank.se/globalassets/media/forskning/monetar-statistik/volym2/volumeiich6stocksandbonds.xls ; volym1/volumeich6exchangerates1804_1914.xls ; volym-3/volumeiiich4bonds.xlsx | free, cite | stocks/bonds (doc: annual 1856-; frequency of the sheet not read), FX 1804-1914 | | | **no: robots.txt `Disallow: *.xls`**, which also matches `.xlsx` (no `$` anchor) | | no (manual). One .xlsx was fetched by mistake (annual issue volumes only) and is deleted |
| 13 | FRED / ALFRED (mirror NBER ch. IV, OECD MEI, many more) | fred.stlouisfed.org/graph/fredgraph.csv?id=... | mostly public domain | | | | no tonight: HTTP/2 reset then time-out from this machine | | no |
| 14 | Stooq (long EM index histories) | stooq.com/q/d/l/?s=...&i=m | site terms | daily/monthly | | | no: TLS connection refused | | no |

Paid or account-only (listed, not used):
- Global Financial Data / GFD Finaeon: stock, bond, commodity and FX series back to the 1600s
  for about 150 countries. Subscription; **no published price, quote on request**.
- Dimson-Marsh-Staunton global returns database: annual, licensed through Morningstar and the
  UBS yearbook; price on request.
- MSCI end-of-day index history: free to view on msci.com, but the terms forbid automated
  download and redistribution, so manual only.
- Bloomberg and LSEG: enterprise licences.
- World Gold Council and LBMA bulk files: need an account or a licence (data-long-1).

## Crypto archives (free, bulk, keyless)

| Archive | What | Span | Script | Note |
|---|---|---|---|---|
| Binance data.binance.vision (S3 listing) | spot and USD-M futures aggTrades, trades, klines; futures `bookDepth` (depth snapshots by % band), `bookTicker`, `metrics`; options `BVOLIndex`, `EOHSummary` | bookDepth from 2023-01 (~0.46 MB a day for BTCUSDT); trades from 2017/2019 | yes (no robots.txt served) | klines, metrics already cached |
| Bybit public.bybit.com, quote-saver.bycsi.com | trades (`trading/`), premium and spot index, 500-level order-book snapshots `orderbook/linear/<SYM>/` | ob500 from 2023-01 | yes (no robots.txt served) | |
| OKX static.okx.com/cdn/okex/traderecords/ | daily trade files (e.g. BTC-USDT 2024-03-01: 5 MB zip, 29 MB csv) | | yes (www.okx.com robots allow `/cdn/okex/traderecords`) | download page path moved (404); file pattern works; the sample was deleted |
| Deribit history.deribit.com/api/v2/public | every option and futures trade, keyless | options from 2016-12 | yes (no robots.txt served) | the only free full options-trade history found |
| Tardis.dev datasets.tardis.dev/v1 | tick trades, book updates, many venues | first day of each month free without key | works | terms page not found (404): treat as an evaluation sample, do not bulk-fetch; the sample was deleted |
| Kraken OHLCVT | full history zip | | no (Google Drive link) | manual |

None of these adds an independent episode. Every coin has shared one crash calendar since
2010, and the project already holds 1-minute bars from Bitstamp (2011-), Bitfinex (2013-)
and Coinbase (2015-). They would serve execution and microstructure questions (book depth,
spread, impact), not the power problem.

## What each source would unlock

- **IMM government bonds** (after the owner's decision on Yale's terms):
  - `tsmom12`, `e4` and the insurance (crash) tests on about 50 sovereign bond markets
    1869-1927, with a calendar of defaults and wars independent of the post-1927 bond and
    stock samples;
  - a cross-section of sovereign bonds (value = yield spread, momentum).
- **IMM stocks, St Petersburg, BoE 1709-1866, NYSE 1815-1870:** a second pre-1927 stock pool
  for e4-indep-1's test (it had 4 markets, power 0.26). With 3+ quoted shares a month for 30+
  years: Canada, Australia, New Zealand, Ireland, Argentina, Brazil, South Africa, India,
  Chile, Egypt and Uruguay. These are sterling-listed firms that operate there: a London
  listing, not the local exchange. BoE and Norges Bank need no owner decision.
- **NBER ch. IV commodities (manual):** a single-commodity trend pool 1841-1912, before the
  PPI groups that pooled-2 used (1913-). It is the only source here with many independent
  commodity series.
- **IFS currencies (manual):** devaluation episodes for the crash-protection tests. An
  emerging-currency trend/carry pool needs pegs flagged first, e.g. with the
  Ilzetzki-Reinhart-Rogoff regime classification (not probed).
- **Norges Bank, BoE:** clean bond and FX series back to 1753 (consols) and 1819-1820
  (Norway), end of month for Norway to 1914.

## Caveats

- **Yale ICF terms** (sources 1-3): academic research only, no commercial use or
  redistribution without authorization. The data stay in the local cache. Only these counts
  are committed. Using the data to select or test trading rules waits for the owner's decision.
- **Counts are upper bounds on independence.** A "new market-year" is new for that market,
  but many share a world calendar (1873, 1890, 1914, 1929-32). The new-calendar-year column is
  the strict version.
- **IMM country indices are chained medians of sterling quotes in London.** Thin countries
  (one or two securities) jump on redemptions, conversions and stale quotes: there are 62
  monthly moves above 40% in log terms in the bond indices, e.g. Germany 1920-24 and Bolivia
  1872. The 3+ quotes variant cuts those.
- **Annual JST coverage counts as seen.** A monthly series inside JST's years adds no new
  market-year here, even though monthly tests could not use JST.
- **Yield-based prices are rough.** Yields were turned into a perpetuity price (100 / y) only
  to count falls. A bond test needs a proper total-return rebuild (data-long-3's method).
- **Timing differs between sources.** IMM, Norway to 1914, SNB and Yale NYSE/SPSE are end of
  month. The BoE sheet mixes conventions by series.
- Nothing after 2025-10 is kept. The cached files end between 1917 and 2025-05.

## Note for the lead and the owner

- **Owner decision:** can Yale ICF data (IMM, St Petersburg, NYSE 1815-1925), "supplied
  solely for academic research purposes", be used in this open, fake-money research to select
  or test trading rules? Otherwise ask Yale's ICF for authorization. Until then they are
  ranked, cached locally and counted, but not used in any rule test.
- **robots.txt:** data.nber.org and api.db.nomics.world are `Disallow: /`, and Riksbank
  disallows `*.xls` (which also matches `.xlsx`). Earlier lanes (data-long-1, e4-indep-1)
  fetched a few data.nber.org files by script. This lane fetched four DBnomics files and one
  Riksbank .xlsx before it checked those hosts' robots.txt, and has deleted them. The
  suggestion is that all three go through a manual download from now on.

## Files

- `lib/datawide2.py`: parsers (IMM, Yale NYSE/SPSE, Norges Bank, SNB, AQR, BoE long CSV, a
  stdlib .xlsx reader), `splice`, `falls`, `count_new`, `SEEN`. Tests:
  `tests/test_datawide2.py` (offline fixtures).
- `lib/datawide2_run.py`: rebuilds `results/data-wide-2.md` and `.json` from the cache.
- Cache: `<cache_root>/data-wide-2/` (36 MB: `yale/2026-11-25/`, `probe/`, `derived/`), plus
  jst-autocorr-2's BoE and Norges Bank stock copies (read only). Nothing raw is committed.

## Plan (written and pushed before any probe)

Goal: rank keyless public data sets by how many **new independent market-years** (and falls of
25% or more) they add to the project's tests, beyond what is already cached or scored:
Shiller US 1871-; NBER Macrohistory ch. XI (GB, DE, FR stocks; e4-indep-1); French country
files 1975-; JST R6 annual; data-long-3 (US bonds, 9 foreign 10y, 9 FX, PPI commodities,
Pink Sheet); data-long-4 (BIS CPI, policy rates); BoE "millennium" monthly sheet and Norges
Bank monthly stock index 1914-2001 (both cached by jst-autocorr-2 for description only);
crypto 1m bars from Binance, Bybit, Bitstamp, Bitfinex, Coinbase, Hyperliquid, Deribit.

Counting rule (fixed now): a market-year is independent when its series is a market (country,
asset or commodity) and a year that no scored series of the same asset class already covers.
A "fall" is a peak-to-trough decline of 25% or more in the monthly level, counted once per
episode (the level must recover to a new high, or the series end, before the next one counts).

Targets: monthly pre-1960 non-US stock, bond and commodity prices; emerging-market indices with
long free history; long monthly commodity spot or futures series; free bulk crypto intraday or
order-book archives. For each: URL, licence or terms, frequency, span, number of series,
whether a polite script fetch works, size. Fetch and cache only the top few that are clearly
allowed (total < 3 GB), with a loader in `research/lib/` and an offline test on a fixture.

## Probe log (2026-11-25 UTC)

- 21:20 AQR "Commodities for the Long Run" (index level, monthly 1877-02 on): 200, keyless xlsx,
  aggregate portfolios only (equal-weight and long/short), no single commodities.
- 21:22 NBER Macrohistory chapter pages read (www.nber.org allows it). **data.nber.org's
  robots.txt is `Disallow: /` for every agent**: no scripted fetch of the .dat files from this
  lane (manual download only). FRED and ALFRED (which mirror many NBER series) reset the
  connection from this machine tonight (HTTP/2 reset, then time-outs).
- 21:25 Yale ICF (som.yale.edu, robots allow `/sites/default/files`, crawl delay 10 s, terms:
  academic research only, no redistribution, cite): St Petersburg and NYSE monthly indices,
  NYSE index 1815-1925, London IMM clean file fetched (10 MB zip).
- 21:28 OECD SDMX API: Cloudflare challenge (403) for a script. The DBnomics mirror answered
  four listing calls (21:28-21:32); its robots.txt (`User-agent: * / Disallow: /`) was **not
  checked before those calls**. Found in review: the four files were deleted and DBnomics moved
  to manual download.
- 21:30 Norges Bank HMS (robots allow, crawl delay 5 s), SNB historical series (allow),
  Riksbank (robots `Disallow: *.xls`). The stock and exchange-rate sheets are .xls, so manual
  only. One `volumeiiich4bonds.xlsx` was fetched at 21:30 on the reading that `.xlsx` was
  allowed. Without a `$` anchor the rule matches `.xlsx` too: the file was deleted.
- Order and delays, honestly: robots.txt was read *after* the first page fetches for
  som.yale.edu, norges-bank.no, snb.ch and riksbank.se (the probe script slept 3 s between
  calls). The Yale crawl delay (10 s) was kept for the HEAD checks and the data downloads, but
  not for the three Yale HTML pages fetched 3 s apart. The Norges Bank crawl delay (5 s) was not
  kept (3 s between its 3 calls). About 10 calls per host in all.
- Review fixes (22:00-22:20 UTC): `SEEN` extended with the JST annual equity coverage that
  insure-1870-1 scored, DBnomics and Riksbank data removed, counts regenerated.
- Date fix (dw2-dates-1, #PRNUM, found by fx-peg-1): the label parser read Excel serial dates
  only above 10,000 (1927-05-18), so Norges Bank Table A2 (NOK in USD) lost its 1914-01..1927-04
  rows and started in 1927-05. It now reads serials of any size (and Excel's 1900 leap-day
  quirk for serials below 60). Every other sheet the module reads (Norges Bank stocks, bonds
  A1, FX A1; SNB; AQR; the BoE long CSV) has text labels or its own year/month columns and was
  unchanged. With the fix the USD series starts 1914-09 (the USD column is blank 1914-01..08):
  +152 months, +12 new market-years and new calendar years (1915-1926), no new falls. Moved:
  currencies union 367 -> 379; Norges Bank FX 187 -> 199 new market-years, 96 -> 108 before
  1927, 140 -> 152 new calendar years, 2,232 -> 2,384 months.
