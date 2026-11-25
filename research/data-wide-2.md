# Data wide 2: keyless sources that add independent episodes

Lane `data-wide-2`, 2026-11-25 (night, UTC). Branch `data-wide-2`. Data survey only: no
strategy, no backtest, no return statistic of any rule. Keyless public data only; no accounts,
keys or sign-ups; paid sources listed with their price only.

## The answer on one screen

**The stock wall is real, but bonds, currencies and old stocks are not used up.** Counted
against everything the project has scored (`SEEN` in `lib/datawide2.py`, written from the
records before any count), the sources cached tonight add (union over sources, one country-year
once per asset class; `results/data-wide-2.md`):

| Asset | New market-years | Falls of 25%+ with the trough in a new year |
|---|---:|---:|
| Currencies (vs USD, mostly emerging, 1950s-2025) | 12,456 | 193 |
| Government bonds (77 sovereigns in London 1869-1929; UK 1753-; Norway 1820-; 44 IFS yields) | 3,856 | 173 |
| Stocks (IMM country indices 1869-1929; UK 1709-1866; US 1815-1870; Russia 1865-1917; OECD 1955-) | 3,383 | 265 |
| Commodity futures (AQR aggregate 1877-1912) | 36 | 2 |

Three numbers decide how much each adds, and they disagree:

- **For e4-indep-1's rule (no time overlap with the 41 stock markets, i.e. before 1927-07)**
  the best new stock pool is the **Yale ICF London Investor's Monthly Manual (IMM)**: monthly
  prices 1869-1929 of every security quoted in London. Built into sterling country indices it
  gives 1,496 new pre-1927 stock market-years in 50 countries (618 in 23 countries when a month
  needs 3+ quoted shares), with 85 (23) falls of 25%+. Plus Russia 1865-1917 (St Petersburg,
  50 years) and the UK 1709-1866 (BoE). The clean IMM file is truncated at Excel's row limit
  (1,048,575 rows): government bonds are complete (cross-checked against the original
  "British, colonial and foreign stocks" section, 220k rows), common stocks are not.
- **For bond tests** the IMM government bonds are the big gain: 77 sovereign borrowers,
  2,463 new market-years before 1927 (1,162 with 3+ quoted bonds a month), 82 falls of 25%+
  (34 with 3+ quoted bonds: defaults and wars such as Egypt and Turkey 1876-77, Peru 1877 and
  1884, Argentina 1891, Mexico 1893, Greece 1897, Brazil 1898, Russia 1922, France 1926; they
  cluster in 1876-78 and 1920-21, so they are fewer independent events than the count). pooled-2 found `e4` and `tsmom12` near zero on 21 bond and currency markets; this is
  an independent bond calendar to test that on.
- **For currencies** IMF IFS via DBnomics adds 217 currencies 1950s-2025 and 188 falls of
  25%+ (devaluations). Most were pegged for long stretches, so the count of *tradable*
  independent years is far smaller than 12,117; a peg filter is needed before any trend test.
- **New calendar years** (years no scored series of that asset class covers at all, the
  strictest independence): stocks 1709-1866 (BoE UK share index, 158 years; NYSE 1815-1870),
  bonds 1753-1870 (consols, Norway 1820-), currencies 1791-1970 (USD/GBP, NOK). These are the
  only additions that do not share any crash calendar with what was scored.

**Ranked by usable independent market-years** (cleaned counts where a cleaner variant exists):
1. Yale IMM government bonds (1,162-2,463 pre-1927 bond years, fetched); 2. Yale IMM stocks
(618-1,496 pre-1927 stock years, fetched, truncated; the complete raw sections are 120 MB more);
3. NBER Macrohistory ch. IV single-commodity prices (101 series with 10+ years before 1913,
2,702 commodity-years; **manual download only**, robots.txt); 4. BoE millennium monthly sheet
(262 new calendar years; cached); 5. IFS currencies (thousands of years but mostly pegs;
fetched); 6. OECD share prices via DBnomics (1,061 new market-years, 0 before 1927: same
calendar as the 41 from 1966, new mainly for 1955-1974 and emerging markets 1980-; fetched);
7. Norges Bank bond yields 1820- and FX 1819- (end-of-month, clean, small); 8. Yale NYSE
1815-1870 and St Petersburg 1865-1917; 9. NBER ch. XI/XIII non-US bonds (manual); 10. IFS bond
yields and share prices; 11. SNB equity 1924- and bonds 1943-1981; 12. AQR commodity futures
1877- (one aggregate series). Crypto archives add no independent market-years (one calendar,
2010 on); they add microstructure depth only.

## Sources (probed 2026-11-25, 21:15-21:45 UTC)

"Script" = a polite scripted fetch is allowed by robots.txt and the terms and worked from this
machine (generic user agent `grimstrade-research/0.1`, 3-10 s between calls). Spans and counts
are read from the files unless marked (doc).

| # | Source | URL | Licence / terms | Freq, timing | Span | Series | Script | Size | Cached |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Yale ICF, London Investor's Monthly Manual, clean file | som.yale.edu/sites/default/files/2021-12/Totaldata.zip (page: .../historical-financial-research-data/london-stock-exchange) | academic research only, no commercial use or redistribution, cite ICF Yale | monthly, open/high/low/late price | 1869-01..1929-12 | 1,208 govt bonds (79 countries), 1,445 common stocks shown (truncated), 1,906 corp bonds | yes (robots allow `/sites/`, crawl delay 10 s) | 10.3 MB zip, 145 MB csv | yes |
| 1b | Yale IMM original sections | .../2021-12/Stocks_new.csv.zip (govt "stocks"), Railways_new, Banks_new, Misc_new | same | monthly | 1869-1929 | complete per section | yes | 14.5 MB fetched; Misc 90 MB, Railways and Banks not fetched | Stocks only |
| 2 | Yale ICF St Petersburg / NYSE comparison | .../2021-12/SPSENYSE18651917ind.xls ; St_ Petersburg data Revised 082010.xlsx | academic only, cite | monthly, USD price indices | 1865-01..1917-02 | 2 (SPSE, NYSE) | yes | 0.2 MB | yes |
| 3 | Yale ICF NYSE 1815-1925 (Goetzmann-Ibbotson-Peng) | .../2021-12/Price-Weighted-Index-Returns-2020-08-20.xls (a CSV) | academic only, cite | monthly price returns | 1815-02..1925-12 | 1 index (+ 1815-1925 security file, not fetched) | yes | 67 kB | yes |
| 4 | Bank of England "A millennium of macroeconomic data" v3.1, monthly sheet | bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/a-millennium-of-macroeconomic-data-for-the-uk.xlsx | Open Government Licence v3 | monthly (mixed timing per series) | share index 1709-04.., consols 1753-08.., corp bonds 1854.., USD/GBP 1791.., PPI 1790.. to 2016-17 | 26 monthly series | yes (HEAD 200, 27.5 MB) | 6.3 MB long CSV | yes (datahub long-CSV copy cached by jst-autocorr-2; xlsx not refetched) |
| 5 | IMF IFS via DBnomics | api.db.nomics.world/v22/series/IMF/IFS?dimensions={"INDICATOR":["ENDA_XDC_USD_RATE"|"FIGB_PA"|"FPE_IX"],"FREQ":["M"]} | IMF data free with attribution; DBnomics is an open aggregator | monthly (FX end of period; yields, shares average) | FX 1950s..2025; bond yields 1950s/80s-; shares 1950-/57- | 217 FX, 44 bond yields, 30 share indices | yes | 4.3 MB trimmed | yes, months after 2025-10 dropped at fetch |
| 6 | OECD MEI share prices via DBnomics | api.db.nomics.world/v22/series/OECD/DSD_STES@DF_FINMARK?dimensions={"FREQ":["M"],"MEASURE":["SHARE"]} | OECD CC BY 4.0 | monthly average | 1950-/55-/57- (SE, FR, CH, IE 1955, ...) to 2025 | 47 countries | yes (OECD's own API: Cloudflare 403) | 0.6 MB | yes, trimmed |
| 7 | Norges Bank Historical Monetary Statistics | norges-bank.no/globalassets/upload/hms/data/{bond_yields,fx,stockprices,shortterm_ir,cpi}.xlsx | free, cite Eitrheim, Klovland and Qvigstad (2004); disclaimer | monthly; bonds and FX to 1914 end of month | govt bond yields 1820-05..2005, FX 1819-04.., stocks 1914-01..2001 (total + 5 sectors) | 1 + 6 + 7 used | yes (crawl delay 5 s) | 1.9 MB | yes (stocks: jst-autocorr-2's copy) |
| 8 | SNB historical time series, capital market | snb.ch/dam/jcr:2478e077-fd40-4dea-88d5-33e6b60f5035/histz_km.n.xls | free, cite SNB | monthly, end of month | equity index 1924-01..1968-08 (+ sectors), SBC index 1959-1997, bond price index 1943-1981, bond yield index 1924-1943 | 2 spliced/used | yes | 5.4 MB | yes |
| 9 | AQR "Commodities for the Long Run" | images.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Commodities-for-the-Long-Run-Index-Level-Data-Monthly.xlsx | free download, copyright the authors, AQR disclosures | monthly returns | 1877-02..2025-05 | aggregates only: EW excess, spot, carry; long/short; no single commodities | yes | 0.45 MB (+ paper version 0.27 MB) | yes |
| 10 | NBER Macrohistory ch. IV Prices | nber.org/research/data/nber-macrohistory-iv-prices ; files data.nber.org/databases/macrohistory/rectdata/04/m04xxx.dat | public, cite NBER | monthly | e.g. wheat Chicago 1841-1944, corn 1860-1951, cotton 1870-, cattle and hogs 1858-1940, copper 1860-, pig iron 1842-, GB wheat 1845-1934, Berlin wheat 1879-1935 | 312 series (209 single commodities, 101 with 10+ years before 1913) | **no: data.nber.org robots.txt `Disallow: /`** | small (.dat, kB each) | no (manual) |
| 11 | NBER Macrohistory ch. XI/XIII non-US bonds | m11017a/b GB consol prices 1853-1934, m11019 GB fixed interest 1867-1914, m11020 DE 3.5% 1877-1925, m11021 FR 3% rentes 1873-1940, m13027 FR yields 1898-1939, m13028a-c DE yields 1870-1935, m13041a-c consol yields 1840-1938 | public | monthly | as listed | 17 | no (robots) | small | no (manual) |
| 12 | Riksbank Historical Monetary Statistics of Sweden | riksbank.se/globalassets/media/forskning/monetar-statistik/volym2/volumeiich6stocksandbonds.xls ; volym1/volumeich6exchangerates1804_1914.xls | free, cite | stocks/bonds (doc: annual 1856-, frequency of the sheet not read), FX 1804-1914 | | | **no: robots.txt disallows `*.xls`** | | no (manual). The vol. III bonds .xlsx (allowed) holds annual issue volumes only |
| 13 | FRED / ALFRED (mirror NBER ch. IV, OECD MEI, many more) | fred.stlouisfed.org/graph/fredgraph.csv?id=... | mostly public domain | | | | no tonight: HTTP/2 reset then time-out from this machine | | no |
| 14 | Stooq (long EM index histories) | stooq.com/q/d/l/?s=...&i=m | site terms | daily/monthly | | | no: TLS connection refused | | no |

Paid or account-only (listed, not used): Global Financial Data / GFD Finaeon (stock, bond,
commodity and FX series back to the 1600s for ~150 countries; subscription, **no published
price, quote on request**); Dimson-Marsh-Staunton global returns database (licensed via
Morningstar/UBS yearbook; annual; price on request); MSCI end-of-day index history (free to view
on msci.com, but the terms forbid automated download and redistribution: manual only);
Bloomberg / LSEG (enterprise). World Gold Council and LBMA bulk files need an account or a
licence (data-long-1).

## Crypto archives (free, bulk, keyless)

| Archive | What | Span | Script | Note |
|---|---|---|---|---|
| Binance data.binance.vision (S3 listing) | spot and USD-M futures aggTrades, trades, klines; futures `bookDepth` (depth snapshots by % band), `bookTicker`, `metrics`; options `BVOLIndex`, `EOHSummary` | bookDepth from 2023-01 (~0.46 MB a day for BTCUSDT); trades from 2017/2019 | yes | klines, metrics already cached |
| Bybit public.bybit.com, quote-saver.bycsi.com | trades (`trading/`), premium and spot index, 500-level order-book snapshots `orderbook/linear/<SYM>/` | ob500 from 2023-01 | yes | |
| OKX static.okx.com/cdn/okex/traderecords/ | daily trade files (e.g. BTC-USDT 2024-03-01: 5 MB zip, 29 MB csv) | | yes (robots allow `/cdn/okex/traderecords`) | download page path moved (404); file pattern works |
| Deribit history.deribit.com/api/v2/public | every option and futures trade, keyless | options from 2016-12 | yes | the only free full options-trade history found |
| Tardis.dev datasets.tardis.dev/v1 | tick trades, book updates, many venues | first day of each month free without key | works | terms page not found (404): treat as an evaluation sample, do not bulk-fetch |
| Kraken OHLCVT | full history zip | | no (Google Drive link) | manual |

None of these adds an independent episode: every coin shares one crash calendar since 2010
(the project already holds 1-minute bars from Bitstamp 2011-, Bitfinex 2013-, Coinbase 2015-).
They would serve execution and microstructure questions (book depth, spread, impact), not the
power problem.

## What each source would unlock

- **IMM government bonds:** `tsmom12` / `e4` and the insurance (crash) tests on ~50 sovereign
  bond markets 1869-1927, a calendar of defaults and wars independent of the post-1927 bond
  and stock samples; also a cross-section (value = yield spread, momentum) of sovereign bonds.
- **IMM stocks + St Petersburg + BoE 1709-1866 + NYSE 1815-1870:** a second pre-1927 stock pool
  for e4-indep-1's test (it had 4 markets, power 0.26). Countries with 3+ quoted shares a month
  for 30+ years: Canada, Australia, New Zealand, Ireland, Argentina, Brazil, South Africa,
  India, Chile, Egypt, Uruguay (sterling-listed firms operating there: a London listing, not
  the local exchange; currency is sterling).
- **IFS currencies:** devaluation episodes for the crash-protection and "falls" tests, and
  an emerging-currency trend/carry pool once pegs are flagged (a regime classification such as
  Ilzetzki-Reinhart-Rogoff would be the next data step; not probed).
- **OECD/IFS share prices:** 1955-1974 for 15 developed markets (the 1962 and 1973-74
  bears, before most of the 41 start) and 1980s-1990s emerging markets; same calendar as the
  41 after 1966, so not independent in e4-indep-1's sense.
- **NBER ch. IV commodities (manual):** a single-commodity trend pool 1841-1912, before the PPI
  groups pooled-2 used (1913-); the only source here with many independent commodity series.
- **Norges Bank, SNB:** clean end-of-month bond and FX series back to 1819-1820 (Norway), Swiss
  equity 1924-1974.

## Caveats

- Counts are upper bounds on independence. A "new market-year" is new for that market; many
  share a world calendar (1873, 1890, 1914, 1929-32). The new-calendar-year column is the
  strict version. IMM country indices are chained medians of sterling quotes in London: thin
  countries (one or two securities) jump on redemptions, conversions and stale quotes (62
  monthly moves above 40% in log terms in the bond indices, e.g. Germany 1920-24, Bolivia
  1872); the 3+ quotes variant cuts those.
- IFS currency counts include long pegs and the 1950s multiple-rate regimes; a fall there is a
  devaluation, real for a holder but not a tradable trend.
- Yields were turned into a perpetuity price (100 / y) only to count falls; a bond test needs
  a proper total-return rebuild (data-long-3's method).
- Timing differs: IMM, Norway to 1914, SNB, Yale NYSE/SPSE are end of month; OECD and IFS
  shares and yields are monthly averages (a one-month gap needed, as e4-indep-1 found).
- Nothing after 2025-10 was kept (DBnomics files trimmed at fetch; the others end 2001-2025-05).

## Note for the lead

data.nber.org's robots.txt is `Disallow: /` for all agents. Earlier lanes (data-long-1,
e4-indep-1) fetched a few NBER .dat files by script. This lane did not; it suggests NBER files
go to the owner's manual-download list from now on.

## Files

- `lib/datawide2.py`: parsers (IMM, Yale NYSE/SPSE, Norges Bank, SNB, DBnomics, AQR, BoE
  long CSV, a stdlib .xlsx reader), `falls`, `count_new`, `SEEN`. Tests: `tests/test_datawide2.py`
  (offline fixtures).
- `lib/datawide2_run.py`: rebuilds `results/data-wide-2.md` / `.json` from the cache.
- Cache: `<cache_root>/data-wide-2/` (41 MB: `yale/2026-11-25/`, `dbnomics/2026-11-25/`,
  `probe/`), plus jst-autocorr-2's BoE and Norges Bank stock copies (read only). Nothing raw is
  committed.

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
- 21:28 OECD SDMX API: Cloudflare challenge (403) for a script; DBnomics mirror answers keyless.
- 21:30 Norges Bank HMS (robots allow, crawl delay 5 s), SNB historical series (allow),
  Riksbank (robots disallow `*.xls`: the stock and exchange-rate sheets are .xls, manual only).
