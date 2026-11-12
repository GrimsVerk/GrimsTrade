# Data sources for GrimsTrade

Data scout run `data-search-1`, 2026-11-12. Every "probe" line is a real fetch made that day from
the owner's PC (an EU IP, Amsterdam CDN edge). GitHub Actions runners have US IPs; where that matters
it says so. No keys, accounts or payments were used.

## Summary for the owner (read this first)

- **Yes, there is much more free data.** The biggest win is **1-minute crypto bars**: free and
  keyless, BTC back to 2012 (Bitstamp), 2013 (Bitfinex), 2015 (Coinbase), and hundreds of coins
  since 2017 (Binance bulk files). For BTC that is ~6 million bars instead of ~4,000 daily ones.
  This is the data an RL agent needs.
- **Crypto "derivatives" data is free too**: funding rates (what longs pay shorts), open interest
  and the Deribit volatility index (DVOL). One catch: Kraken Futures only serves the **last 12
  months**, so we should start saving it daily **now**, or lose it.
- **Stock/ETF intraday is the hard part.** Free and keyless: Yahoo hourly bars for the last ~2
  years only (a rolling window, so again: start saving now). Longer minute history (since 2016)
  needs a free Alpaca account, which only you can create.
- **Long daily history is easy**: S&P 500 since 1927 (Yahoo), factor returns since 1926 (Ken
  French), monthly S&P since 1871 (Shiller), 10-year yield since 1962 and VIX since 1990 (FRED).
- **Macro without cheating**: FRED's sister site ALFRED gives each number **as it was known on a
  past date** (keyless, verified). That lets the agent use macro data with no look-ahead.
- **Two warnings.** (1) Stooq, our backup ETF source, now shows a JavaScript bot check: the
  fallback in `sources.py` probably no longer works. (2) The repo is public; most exchange data
  terms forbid re-publishing raw data. Big raw files should live in a local, git-ignored cache that
  a script can rebuild, not in git.
- **Nothing here needs money.** Cheap paid options are listed at the end for you to decide.
- **Recommended first three to add**: (1) intraday bars (Coinbase 1-min crypto + Yahoo hourly ETFs),
  (2) crypto funding rates and open interest, (3) FRED/ALFRED macro with vintages.

## How to read the entries

Fields: **What / Assets / Granularity / History / Access / Key / Cost / Licence / US runner /
Reliability / Probe / Verdict.** "US runner" = can a GitHub Actions job fetch it. "Commit?" in
Licence is about the public repo. Verdicts: **ADD** (first wave), **LATER**, **SKIP**.

Rule of thumb for all exchange data: storing it locally for our own research is fine; re-publishing
raw bulk data in a public repo is not clearly allowed by any exchange's terms. The repo already
commits small daily bars on `paper-trail`; that is low-risk in practice, but minute data should not
be committed raw (size and terms). Owner's call if you want to change the current daily practice.

---

## 1. Intraday crypto history

### 1.1 Binance bulk archive (data.binance.vision)
- **What:** official public S3 archive of Binance spot and futures data, monthly and daily zips with
  `.CHECKSUM` files.
- **Assets:** every Binance spot pair (BTCUSDT, ETHUSDT, SOLUSDT, ... hundreds), plus USD-M and
  COIN-M futures.
- **Granularity:** klines 1s / 1m / 5m / ... / 1d; raw `trades` and `aggTrades` (tick level).
- **History:** spot BTCUSDT from 2017-08; other coins from their listing.
- **Access:** plain HTTPS file download, no rate limit published (CloudFront). ~2 MB per coin-month
  for 1m klines (estimate); BTC 1m 2017-2026 ≈ 0.2-0.3 GB zipped. Trades are far larger (GBs/month).
- **Key / Cost:** none / free.
- **Licence:** Binance Terms of Use; local research use is the intended use, re-publishing raw data
  is not granted. **Do not commit raw.**
- **US runner:** **unknown.** The archive is S3/CloudFront, not `api.binance.com` (which returns 451
  to US IPs). Not testable from here. Not needed: backfill is a one-off on the owner's PC.
- **Reliability:** high; files are immutable, with checksums.
- **Probe 2026-11-12:** `HEAD .../spot/monthly/klines/BTCUSDT/1m/BTCUSDT-1m-2017-08.zip` -> 200,
  595,271 bytes, AmazonS3.
- **Verdict: ADD (second wave)** for breadth: many coins for RL training. Prices are USDT, not USD,
  and Binance is not our trading venue, so use it for training, and Coinbase/Kraken for the
  live/test record.

### 1.2 Coinbase Exchange candles API
- **What:** public REST candles, the same API `sources.py` already uses for daily bars.
- **Assets:** all Coinbase USD pairs (BTC-USD, ETH-USD, SOL-USD, ...).
- **Granularity:** 1m, 5m, 15m, 1h, 6h, 1d.
- **History:** BTC-USD 1m from 2015-07-20 (verified); ETH-USD from 2016 (listing).
- **Access:** 300 candles per request; public limit ~10 req/s. BTC 1m full backfill ≈ 20,000
  requests ≈ 1 hour at a polite 5 req/s. Gaps: minutes with no trades are simply missing.
- **Key / Cost:** none / free.
- **Licence:** Coinbase market data terms; same status as today's daily bars. Don't commit raw 1m.
- **US runner:** yes (US exchange; already used from Actions).
- **Reliability:** good; occasional 429s, needs retry with backoff.
- **Probe 2026-11-12:** `/products/BTC-USD/candles?granularity=60&start=2015-07-21T00:00Z` -> 200,
  11 one-minute candles at ~279.9 USD.
- **Verdict: ADD (first wave).** USD prices, same venue family as our record, reachable from
  Actions, so one source serves backfill and daily append.

### 1.3 Bitstamp OHLC API
- **What:** public REST OHLC of one of the oldest exchanges.
- **Assets:** BTC/USD, ETH/USD, a few dozen USD/EUR pairs.
- **Granularity:** 1m to 3d (`step` in seconds).
- **History:** BTC/USD from 2011-2012 (probe returned 2012-01-01 bars).
- **Access:** up to 1,000 candles per call; ~8,000 calls per 10 min allowed (docs, from memory).
- **Key / Cost:** none / free.
- **Licence:** exchange terms; don't commit raw.
- **US runner:** yes (Bitstamp serves US customers).
- **Reliability:** good. Early years are thin: zero-volume minutes are forward-filled at the last
  price (seen in the probe), so filter those.
- **Probe 2026-11-12:** `/api/v2/ohlc/btcusd/?step=60&start=1325376000` -> 200, 3 bars at 4.58 USD,
  volume 0.
- **Verdict: LATER.** Longest BTC intraday series (adds 2012-2015 incl. the Mt. Gox era) and a
  second source to cross-check Coinbase.

### 1.4 Bitfinex candles API
- **What / Assets:** public v2 candles; BTC, ETH and many USD pairs.
- **Granularity / History:** 1m to 1M; BTC from 2013-04-01 (verified).
- **Access:** up to 10,000 candles per call, ~30 req/min limit.
- **Key / Cost / Licence:** none / free / exchange terms, don't commit raw.
- **US runner:** probably yes for public data (Bitfinex bars US customers, not public endpoints);
  not verified.
- **Probe 2026-11-12:** `/v2/candles/trade:1m:tBTCUSD/hist?start=2013-01-01` -> 200, first bar
  2013-04-01 at 93.25.
- **Verdict: LATER** (cross-check source; Bitstamp is longer).

### 1.5 Kraken trades API and Kraken bulk files
- **What:** `/0/public/Trades` returns the full tick history paged by `since`; Kraken also publishes
  downloadable OHLCVT and trade zips (Google Drive link in their support article "Downloadable
  historical OHLCVT data"). The OHLC API itself only returns the last 720 candles.
- **Assets:** all Kraken pairs. **History:** XBT/USD trades from 2013-10-06 (verified).
- **Access:** 1,000 trades per call, ~1 call/s: the full BTC tick history would take days. The
  bulk zips are the practical route (Drive download, not probed).
- **Key / Cost / Licence:** none / free / exchange terms, don't commit raw.
- **US runner:** yes (already used).
- **Probe 2026-11-12:** `Trades?pair=XBTUSD&since=0&count=3` -> 200, first trade 1381095256
  (2013-10-06) at 122.00.
- **Verdict: LATER.** Our trading venue for crypto fees, so the best match for the gym, but the
  bulk path needs a manual Drive download; Coinbase gives the same bars more simply.

### 1.6 Bybit public archive (public.bybit.com)
- **What:** daily trade CSVs for Bybit perps/spot since 2019-2020.
- **Probe 2026-11-12:** `HEAD /trading/BTCUSDT/BTCUSDT2020-03-25.csv.gz` -> 200, 121 KB.
- **US runner:** no (Bybit blocks US IPs). Owner's PC only.
- **Verdict: SKIP for now** (Binance archive covers the same ground, larger).

### 1.7 BitMEX public archive and API
- **Probe 2026-11-12:** `public.bitmex.com/data/trade/...` -> 302 to the home page;
  `www.bitmex.com/api/v1/funding` -> 403 "Request blocked" (CloudFront geo-block from this IP).
- **Verdict: SKIP** (blocked here; would have had funding since 2016).

## 2. Longer and wider daily history

### 2.1 Yahoo chart API (already used)
- **What:** `query1.finance.yahoo.com/v8/finance/chart`. Assets: all ETFs, stocks, indexes (`^GSPC`,
  `^DJI`, `^IXIC`, `^VIX`, ...), FX, futures.
- **History:** `^GSPC` firstTradeDate 1927-12-30 (verified in the response metadata).
- **Access:** unofficial; returns 429 to clients without a browser-like User-Agent (probe with a
  plain curl client -> 429). The existing `sources.py` fetcher already handles this.
- **Key / Cost:** none / free. **Licence:** Yahoo terms forbid redistribution; personal use only.
- **US runner:** yes (in use). **Reliability:** medium: unofficial, can break or rate-limit.
- **Probe 2026-11-12:** `^GSPC` for Jan 1928 -> 200 with bars.
- **Verdict: ADD (cheap)** more symbols: indexes back to 1927 for the long-horizon investing agent,
  plus the BACKLOG ETFs (IWM, EFA, ...). Adjusted closes for dividends come from the same call.

### 2.2 Stooq
- **Probe 2026-11-12:** `stooq.com/q/d/l/?s=^spx&i=d` -> 200 but the body is an HTML page "This site
  requires JavaScript to verify your browser". Stooq has added a bot check.
- **Verdict: problem.** `sources.py` uses Stooq as the ETF fallback. **Code request:** check whether
  the fallback still works from Actions; if not, drop it or replace it (e.g. second Yahoo host
  `query2`, or Alpaca once there is an account). Not fixed here (no `src/` changes).

### 2.3 Ken French Data Library
- **What:** Fama-French factors (market, size, value, momentum, ...) and industry/size portfolios.
- **Granularity / History:** daily from 1926-07, monthly from 1926.
- **Access:** zip of CSV, ~180 KB for daily 3 factors. **Key / Cost:** none / free.
- **Licence:** freely published for research; no explicit licence. Small: commit with a citation
  is low-risk, but keep it in the cache to be safe.
- **US runner:** yes (Dartmouth, US). **Reliability:** high, updated monthly.
- **Probe 2026-11-12:** `HEAD F-F_Research_Data_Factors_daily_CSV.zip` -> 200, 178,326 bytes,
  last-modified 2026-10-27.
- **Verdict: ADD (investing agent)**: ~100 years of daily market returns incl. 1929 and 1970s.

### 2.4 Shiller "Irrational Exuberance" data
- **What:** monthly S&P price, dividends, earnings, CPI, 10-year rate, CAPE since 1871.
- **Probe 2026-11-12:** `HEAD .../ie_data.xls` -> 200 (Excel, last-modified 2024-09-04: updates
  may have stopped).
- **Verdict: LATER (investing agent)**, monthly only, and possibly no longer updated.

### 2.5 FRED daily market series
- FRED (keyless `fredgraph.csv?id=`) has `DGS10` 10-year yield from 1962-01-02 (verified), `VIXCLS`
  from 1990-01-02 (verified), `DTWEXBGS` dollar index, `DCOILWTICO` oil, gold was removed. See 5.1.

## 3. Intraday ETF / stock history

### 3.1 Yahoo intraday
- **What:** same chart API: 1h bars for ~730 days, 5m/15m for 60 days, 1m for 7-8 days. A rolling
  window: older bars disappear.
- **Probe 2026-11-12:** `SPY range=730d interval=1h` -> 200, 5,099 bars, 2023-12-14 to 2026-11-11.
- **US runner:** yes. **Licence:** as 2.1.
- **Verdict: ADD (first wave), time-sensitive.** Every day we don't save it, a day of history
  falls out of the window. Hourly SPY/QQQ/GLD/TLT is ~2 KB/day in total.

### 3.2 Alpaca market data (free account needed)
- **What:** official API, US stocks and ETFs, minute bars from 2016, trades and quotes. Free plan:
  IEX feed live, full SIP history older than 15 minutes.
- **Key:** yes (free account; **owner must sign up**, keys go in Actions secrets as BACKLOG says).
- **Cost:** free plan; paid "Algo Trader Plus" ~99 USD/month (from memory, not needed).
- **US runner:** yes. **Licence:** for own use, no redistribution.
- **Probe:** not possible without a key.
- **Verdict: ADD when the owner creates the account.** The only free route to ~10 years of ETF
  minute bars found.

### 3.3 Dukascopy tick data
- **What:** Swiss bank's free tick feed for FX, gold, and index CFDs (USA500IDXUSD, USATECHIDXUSD, ...)
  from ~2003-2012, in `.bi5` hourly files.
- **Probe 2026-11-12:** `datafeed.dukascopy.com/.../USA500IDXUSD/2020/02/03/14h_ticks.bi5` -> 429
  "Too Many Requests. For instructions see wiki.dukascopy.com/.../data-export". They now throttle
  direct downloads.
- **Verdict: LATER.** CFD prices (not the ETF), throttled; useful only for very long intraday index
  history. Terms forbid redistribution.

### 3.4 Others noted, not probed
- Polygon.io / Massive, Tiingo IEX intraday, Twelve Data: all need a (free) key; free tiers are
  short (about 2 years) or rate-limited. See paid list.

## 4. Crypto derivatives (funding, open interest, basis, implied vol)

### 4.1 Kraken Futures funding rates
- **What:** hourly funding rate for Kraken perpetuals (PF_XBTUSD, PF_ETHUSD, ...).
- **Access:** `futures.kraken.com/derivatives/api/v4/historicalfundingrates?symbol=PF_XBTUSD` (the v3
  path in BACKLOG also works). One call returns everything it has.
- **History: only the last 12 months.** Probe returned 8,769 hourly rows, 2025-11-11 23:00 to
  2026-11-12 13:00. Older data is not served.
- **Key / Cost:** none / free. **US runner:** yes (Kraken, in use).
- **Licence:** exchange terms. ~1 MB/year as JSON, ~0.3 MB as CSV.
- **Kraken Futures analytics (open interest, candles):** `api/charts/v1/...` returned empty for
  2022 ranges: also short history only. Not explored further.
- **Verdict: ADD (first wave), time-sensitive.** It is the venue the carry idea in BACKLOG would
  trade, and history is lost daily if we don't store it.

### 4.2 Binance futures archive (funding, open interest, premium index)
- **What:** on data.binance.vision: `futures/um/monthly/fundingRate/` (8-hourly funding since
  2019-09), `futures/um/daily/metrics/` (5-minute open interest, long/short ratios, since ~2021),
  `premiumIndexKlines`, `markPriceKlines`, `indexPriceKlines` (basis).
- **Probes 2026-11-12:** `HEAD .../fundingRate/BTCUSDT/BTCUSDT-fundingRate-2020-01.zip` -> 200;
  `HEAD .../metrics/BTCUSDT/BTCUSDT-metrics-2022-01-01.zip` -> 200.
- **US runner:** unknown (see 1.1); backfill from the owner's PC.
- **Verdict: ADD (backfill for 4.1).** Longest free funding + OI history; the biggest market, so the
  best "crowding" signal.

### 4.3 Deribit public API (funding, DVOL implied volatility)
- **What:** `get_funding_rate_history` (BTC-PERPETUAL, hourly), `get_volatility_index_data` (DVOL,
  the crypto VIX, hourly/daily), plus options chains and historical volatility.
- **Probes 2026-11-12:** funding for 2021-01-01 -> 200 with hourly rows; for 2019-01-01 -> 200 but
  empty (history start somewhere 2019-2020). DVOL for 2021-04-01 -> 200 with hourly OHLC (~86).
- **Key / Cost:** none / free. **US runner:** unknown; Deribit excludes US customers, public API
  geo-blocking not verified.
- **Verdict: ADD DVOL with wave 2.** The only free implied-vol series for crypto found. Funding is
  a backup to 4.2.

### 4.4 Hyperliquid info API
- **What:** POST `api.hyperliquid.xyz/info` `{"type":"fundingHistory",...}`; also candles and
  order-book snapshots (live).
- **Probe 2026-11-12:** BTC funding from 2023-05-12 -> 200, one row (-0.000613).
- **US runner:** likely yes (front-end blocks US, API is open; not verified).
- **Verdict: LATER** (short history; good fallback).

### 4.5 OKX public API
- **Probe 2026-11-12:** `funding-rate-history?instId=BTC-USDT-SWAP` -> 200, with recent 8-hourly
  rates (history depth not checked); OKX blocks US users. **Verdict: SKIP.**

## 5. Macro

### 5.1 FRED (keyless CSV)
- **What:** St. Louis Fed database: rates (`DFF`, `FEDFUNDS`, `DGS2`, `DGS10`, `T10Y2Y`), money
  (`M2SL`, `WALCL`), credit (`BAA10Y`), inflation (`CPIAUCSL`), jobs (`PAYEMS`), VIX (`VIXCLS`).
- **Access:** `fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>`; no key; be polite (~1 req/s).
- **Licence:** US-government series (Treasury, Fed, BLS, BEA) are public domain: committing them is
  fine. Some series are third-party copyrighted (S&P 500, ICE BofA spreads, Cboe VIX): keep those
  out of git.
- **US runner:** yes. **Reliability:** high.
- **Probes 2026-11-12:** `DGS10` -> 200, 269 KB, from 1962-01-02. `VIXCLS` -> 200, from 1990-01-02.
- **Verdict: ADD (first wave)** together with 5.2.

### 5.2 ALFRED vintages (keyless CSV) - the no-look-ahead version of FRED
- **What:** every past version of each FRED series, as it was published on a given date.
- **Access:** `alfred.stlouisfed.org/graph/alfredgraph.csv?id=PAYEMS&vintage_date=2020-04-01`.
  No key needed for the CSV (the JSON API does need a free key).
- **Probe 2026-11-12:** that URL -> 200, 17 KB, column `PAYEMS_20200401`, rows from 1939.
- **Verdict: ADD (first wave).** For revised monthly series (payrolls, M2, CPI, GDP) a decision at
  time T must use the vintage as of T. Daily market rates (`DFF`, `DGS10`) are not revised, so
  plain FRED plus "first seen" timestamps is enough for those.

### 5.3 US Treasury daily yield curve
- **What:** official par yield curve, 1-month to 30-year, daily since 1990.
- **Probe 2026-11-12:** 1990 CSV from home.treasury.gov -> 200, 14 KB, `12/31/1990 ... 8.08` (10y).
- **Licence:** public domain. **US runner:** yes.
- **Verdict: LATER** (FRED's `DGS*` series carry the same numbers more simply).

### 5.4 Philadelphia Fed Real-Time Data Set
- **What:** quarterly vintages of GDP, etc. since 1965, as Excel.
- **Probe 2026-11-12:** `HEAD ROUTPUTQvQd.xlsx` -> 200, 245 KB.
- **Verdict: LATER** (ALFRED covers this more conveniently).

## 6. Volatility, on-chain, sentiment, news, order books

### 6.1 Cboe index history (VIX, VIX9D, VIX3M, VVIX, SKEW)
- **Probe 2026-11-12:** `cdn.cboe.com/.../VIX_History.csv` -> 307 redirect behind Cloudflare; not
  followed (it would need a browser-like client). FRED `VIXCLS` (5.1) gives VIX daily since 1990
  keyless; Yahoo has `^VIX`, `^VIX3M`, `^VVIX`, `^SKEW`.
- **Verdict: use FRED/Yahoo for VIX; LATER** for the term structure (VIX3M/VIX ratio is a known
  risk-off signal).

### 6.2 Coin Metrics Community API (on-chain)
- **What:** daily on-chain metrics: active addresses, MVRV, realised cap, fees, hash rate, supply,
  for BTC, ETH and dozens of assets.
- **History:** BTC from 2009-01-03 (verified with `paging_from=start`).
- **Access:** `community-api.coinmetrics.io/v4/timeseries/asset-metrics`, keyless, ~10 req/6 s.
- **Licence:** **CC BY-NC 4.0** (non-commercial, attribution). Fine for this project; don't commit.
- **US runner:** yes (US company).
- **Probe 2026-11-12:** `btc AdrActCnt,CapMVRVCur,PriceUSD` -> 200, rows for 2026-11-10/11
  (MVRV 1.37).
- **Verdict: ADD (wave 2).** MVRV and active addresses are the standard "cycle phase" on-chain
  signals the macro lane in BACKLOG asks about. Note: on-chain values for day d are known only
  after d closes; stamp them as available at d+1 00:00 UTC (or later if the API lags).

### 6.3 Blockchain.com charts API
- **Probe 2026-11-12:** `charts/hash-rate?timespan=all` -> 200, daily from 2009-01-03.
- **Verdict: LATER** (overlaps Coin Metrics; useful backup for hash rate, miner revenue, fees).

### 6.4 Crypto Fear & Greed Index (alternative.me)
- **Probe 2026-11-12:** `api.alternative.me/fng/?limit=0` -> 200, 302 KB, full daily history
  (from 2018-02), today 28 "Fear".
- **Licence:** free with attribution. **US runner:** yes (likely).
- **Verdict: LATER.** Cheap sentiment feature; but it is itself built from price/volatility, so
  partly redundant.

### 6.5 GDELT 2.0 (news events and tone)
- **What:** global news events, mentions and tone, every 15 minutes since 2015-02.
- **Probe 2026-11-12:** `https://data.gdeltproject.org/gdeltv2/lastupdate.txt` -> 200, lists the
  14:00 files (export 95 KB, mentions 126 KB, GKG 5.5 MB zipped per 15 min).
- **Licence:** open, redistribution allowed with citation. **US runner:** yes.
- **Size:** full GKG history is several TB; events-only ~100 MB/month zipped.
- **Verdict: LATER (M3+).** Needs filtering to finance/crypto topics and a daily aggregate (counts,
  average tone); a good job for the owner's GPU box later, writing a dated signal file.

### 6.6 Historical order books
- **Tardis.dev** free samples (first day of each month): probe `datasets.tardis.dev/v1/deribit/...
  2020/09/01/...` -> 404 for both `trades` and `book_snapshot_25`. Free sample path not found;
  paid otherwise.
- No free historical order-book source found that works. Options: record our own snapshots (Kraken
  `/0/public/Depth`) - but Actions cron runs at most every 5 minutes and is unreliable, so this
  would need the owner's PC running a recorder.
- **Verdict: SKIP for now.** Revisit only if an intraday strategy needs it (VISION: no intraday
  trading before daily works).

## 7. Cheap paid options (owner decides; nothing bought)

Prices are from memory, **not verified today**; check before paying.

| Source | Price (approx.) | Adds over free |
|---|---|---|
| Databento (pay-as-you-go, signup credit) | a few USD for SPY/QQQ 1-min since 2018 | official exchange data, clean ETF minute bars |
| FirstRate Data (one-off bundles) | ~100-200 USD one-off | ETF 1-min history back to 2000s |
| Polygon/Massive Starter | ~29 USD/month | 5 years of stock/ETF minute bars, simple API |
| Tiingo Power | ~30 USD/month | 30+ years EOD, IEX intraday, news |
| Tardis.dev | from ~50 USD/month | tick-level order books for crypto |

Free-with-account (no money, but the owner must sign up): Alpaca (3.2), FRED API key (JSON
access), Tiingo free, Polygon free (2 years, 5 calls/min).

## 8. Ranking for GrimsTrade (RL first)

1. Crypto 1-minute bars: Coinbase (1.2) for BTC/ETH/more, Binance archive (1.1) for breadth.
2. Crypto funding and open interest: Kraken Futures (4.1, start saving now), Binance archive (4.2).
3. Macro with vintages: FRED + ALFRED (5.1, 5.2).
4. ETF hourly bars from Yahoo (3.1, start saving now); ETF minute bars from Alpaca (3.2, needs
   account).
5. Long daily history: Yahoo indexes from 1927 (2.1), Ken French factors from 1926 (2.3).
6. Implied vol: Deribit DVOL (4.3), VIX family (6.1).
7. On-chain: Coin Metrics (6.2).
8. Sentiment/news: Fear & Greed (6.4), GDELT (6.5).
9. Order books: none free (6.6).

## 9. Recommended ingest plan (not implemented)

Shared rules for all three:
- New module `src/grimstrade/intraday.py` (or a `sources_*` file per family), one fetcher per source,
  same `settled()` rule as today: store a bar or rate only after its period has closed (+15 min).
- **Two tiers of storage.** (a) Raw bulk backfill: a local git-ignored cache
  (`cache/<source>/...`, path in the gitignored local config file with a committed `.example`), each
  file written once, with its source checksum, never edited; a script rebuilds it on any computer.
  (b) The append-only record on `paper-trail`: only what the daily runner itself fetches, small, in
  CSV, never rewritten; differences from a re-fetch go to `data/revisions.jsonl` as today.
- Every row carries `available_at` (UTC time it could first have been known). The gym and strategies
  filter on `available_at <= decision_time`, which generalises today's "bar close <= T" rule.

**1. Intraday bars (crypto 1-min, ETF 1-hour).**
- What: Coinbase 1m for BTC-USD, ETH-USD (+ SOL-USD and a few liquid coins); Yahoo 1h for the
  4 ETFs. Daily append from Actions; one-off backfill of Coinbase 1m from 2015 on the owner's PC.
- Why: ~1,500x more bars for RL; Yahoo hourly disappears after 730 days, so every day counts.
- Size: 1m backfill ≈ 5.9 M rows per coin ≈ 250-300 MB CSV / ~60 MB Parquet per coin (local
  cache). Committed record: crypto **1-hour** bars (~9k rows/year/coin ≈ 0.6 MB/year) plus ETF
  hourly (~2k rows/year/ETF); 1m stays local. Daily append from Actions ≈ 1,440 rows/coin/day
  fetched, aggregated to hourly for git.
- No look-ahead: bar timestamp = open; `available_at` = open + interval + 15 min. Coinbase omits
  empty minutes: store them as missing, never fill forward from a later bar.
- Append-only: backfill files immutable; the daily job only appends hours after the last stored one.

**2. Crypto funding rates and open interest.**
- What: Kraken Futures hourly funding (PF_XBTUSD, PF_ETHUSD) appended daily from Actions; one-off
  backfill from the Binance archive (8-hourly funding since 2019, 5-min OI since ~2021) locally.
- Why: crowding/leverage signal for RL and the input the funding-carry idea in BACKLOG needs;
  Kraken only keeps 12 months, so storing it starts the clock.
- Size: Kraken ~0.3 MB/year/symbol committed; Binance backfill ~10-50 MB local.
- No look-ahead: a funding rate is known when its period settles (Kraken timestamp = settlement);
  `available_at` = timestamp + 15 min. Kraken's live/estimated rate is never stored as history.
- Append-only: rows keyed by (symbol, timestamp); new rows only; a changed past value goes to
  `revisions.jsonl`.

**3. Macro with vintages (FRED + ALFRED).**
- What: daily `DFF`, `DGS2`, `DGS10`, `T10Y2Y`, `BAA10Y`, `VIXCLS`; weekly `WALCL`; monthly `M2SL`,
  `CPIAUCSL`, `PAYEMS`.
- Why: the macro/cycle lane in BACKLOG; slow features for the investing agent and regime inputs
  for RL.
- Size: under 5 MB total including vintages; US-government series may be committed (public domain);
  `VIXCLS` (Cboe-owned) stays in the local cache.
- No look-ahead: monthly series are backfilled from ALFRED so each observation's value is the one
  published at that time, with `available_at` = its release date; the daily job stores each new
  value with the date it first appeared. Daily market rates use the observation date + 1 day
  (FRED posts them the next morning).
- Append-only: a later revision is a new row (new vintage), never an edit.

## 10. Code requests (for a later `src/` session)

- Check the Stooq fallback in `sources.py` (bot check seen 2026-11-12, see 2.2).
- Test once from an Actions runner whether `data.binance.vision`, `api.hyperliquid.xyz` and
  `www.deribit.com` answer from US IPs (a tiny `workflow_dispatch` job); this doc could not.

## Status

- **Done (2026-11-12):** read AGENTS/VISION/DESIGN/BACKLOG; ~35 keyless probes across all six
  categories; catalogue, ranking, ingest plan written.
- **Doing:** nothing.
- **Next (if another session continues):** verify paid prices in section 7 on the vendors' pages;
  find the Kraken bulk OHLCVT download link and its size; find the start date of Deribit funding
  history (between 2019 and 2021); look for a free source of older ETF intraday data; check whether
  Tardis still offers free monthly samples (new path?).
