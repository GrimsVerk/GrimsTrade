# Data inventory (local cache)

What is downloaded to the raw-data cache, what is still running, and how to rebuild it. The cache
is never committed: it is large, and exchange/Yahoo terms forbid re-publishing. Paths below are
relative to the cache root (`[cache] root` in `local.toml`; this machine: `~/data/grimstrade`).
Sources and verdicts: `docs/data-sources.md`.

Last updated 2026-11-12 ~15:35 UTC (ingest 1). Numbers for running jobs are a snapshot; for the
current state run the commands under "Check progress".

## Rules every file follows

- Written once (temp file + rename), never edited. A rerun skips files already there.
- `manifest.jsonl` at the root: one line per file with `path`, `fetched_at` (UTC), `url`, `bytes`,
  `sha256`. Binance zips are also checked against Binance's own `.CHECKSUM` before saving.
- Whole-history files (Yahoo daily, FRED, ...) sit in a dated folder (`<source>/<YYYY-MM-DD>/`): a
  later run adds a new snapshot beside the old one, so revisions stay visible.
- Raw responses only (JSON, CSV, zip, xls), except the rolling-window snapshot, which adds a tidy
  CSV with `available_at` per row.
- Read downloaded files with `python -I` only; never run anything that was downloaded.
- Size cap 300 GB in total (`grimstrade.cache.CAP_BYTES`; the Binance job checks it).

## Done

| Source | Path | Range | Rows / files | Size | Rebuild |
| --- | --- | --- | --- | --- | --- |
| Yahoo 1h bars SPY, QQQ, GLD, TLT | `snapshots/yahoo-1h/2026-11-12/` | 2023-12 to 2026-11-12 (~730 days) | 5,093 bars each | 2 MB raw | **Cannot**: rolling window. `scripts/snapshot_rolling.py` adds a new day's snapshot |
| Kraken Futures funding PF_XBTUSD, PF_ETHUSD | `snapshots/kraken-funding/2026-11-12/` | 2025-11-11 to 2026-11-12, hourly | 8,771 each | 2 MB raw | **Cannot**: 12-month window. Same script |
| Kraken Futures open interest PF_XBTUSD, PF_ETHUSD | `snapshots/kraken-oi/2026-11-12/` | ~83 days, hourly (one call: 2,000 points) | 2,000 each | 0.25 MB | Same script. Since 2026-11-13 (ingest 2) it pages with `since`: every hour from 2023-03-07 (~32,300 rows each, checked live); the first snapshot with it is the next dated folder |

## Running (detached; PIDs in `pids/<job>.pid`, logs in `logs/<job>.log`)

| Job | Script | What | Expected size | Expected time |
| --- | --- | --- | --- | --- |
| `binance` | `scripts/backfill/binance.py` | `binance/futures/um/monthly/fundingRate/`, `.../premiumIndexKlines/<S>/1h/`, `binance/spot/monthly/klines/<S>/1m/`, `binance/futures/um/daily/metrics/` (5-min OI, long/short ratios) for 30 USDT pairs (BTC, ETH first) | ~10-20 GB (estimate) | ~1 s per file; spot 1m ~1 h, metrics ~50k daily files ~14 h |
| `rest_1m-coinbase` | `scripts/backfill/rest_1m.py coinbase` | BTC-USD from 2015-07-20, ETH-USD from 2016-05-18, 1m, `coinbase/1m/<pair>/<year>/<chunk>.json` (300 min per file) | ~1 GB | ~2-3 h per pair |
| `rest_1m-bitstamp` | `rest_1m.py bitstamp` | btcusd from 2011-08, ethusd from 2017-08, 1m (1,000 min per file) | ~1.5 GB (121 KB per file) | a few hours |
| `rest_1m-bitfinex` | `rest_1m.py bitfinex` | tBTCUSD from 2013-04, tETHUSD from 2016-03, 1m (10,000 min per file, 2.5 s apart: 30 req/min limit) | ~1 GB | ~1-2 h |
| `small` | `scripts/backfill/small.py` | Yahoo daily full history (14 indexes from 1927, 20 ETFs, BTC/ETH, gold, oil, dollar) `yahoo-1d/`; FRED 21 series `fred/<date>/`; ALFRED vintages (1st and 15th of each month since 2000) for PAYEMS, M2SL, CPIAUCSL, UNRATE, INDPRO, WALCL `fred/alfred/<ID>/<vintage>.csv`; Ken French (6 files) `french/`; Shiller `shiller/`; Treasury curve 1990+ `treasury/`; Philly Fed RTDSM (4 files) `philly-rtdsm/`; Cboe VIX family `cboe/`; Blockchain.com (5 charts) `blockchain-com/`; Fear & Greed `fear-greed/`; Deribit BTC/ETH perpetual funding (30-day chunks from 2019-04) and DVOL (hourly from 2021-03) `deribit/`; GDELT 1.0 daily events, last 30 days `gdelt/events/` | ~0.5 GB | ~1.2 h (4,343 requests at ~1/s) |

| `alpaca` | `scripts/backfill/alpaca.py` | ETF 1m bars, **SIP feed** (the free plan allowed it), raw prices, from 2016-01, 20 ETFs: `alpaca/1m-sip/<SYM>/<YYYY-MM>.json`. Started by the Chief of Staff ~15:35 UTC (PID 1017108) after creating the key file | ~5-10 GB (estimate) | ~1-2 h (~170 req/min) |
| `coinmetrics` | `scripts/backfill/coinmetrics.py <date>` | Every free (community) daily asset metric for every asset in the catalog: 3,547 assets, 14,667 series (~11M points; BTC/ETH 31 metrics each, most small coins only market-cap estimates and volume): `coinmetrics/full/<date>/assets/<asset>/page-NNN.json` + both catalogs. Free tier has no exchange/pair/market data (403). License CC BY-NC 4.0: local only. Started by the Chief of Staff 2026-11-13 02:14 UTC (the BTC/ETH 8-metric pull in `small` is `coinmetrics/2026-11-12/`) | ~1-2 GB (estimate) | ~1.2 h (~1 req/s) |

Known gaps: FRED and ALFRED are **skipped** (`SKIP_HOSTS` in `small.py`): their CSV endpoints
stall our User-Agent, and we don't disguise the client (owner's call, `next-steps.md`). Coin
Metrics community refuses `CapRealUSD` and `FeeTotUSD` (dropped; `FeeTotNtv` instead). The
`small` job was restarted ~15:50 UTC after these fixes. Check the
logs for `FAIL` lines; a rerun retries only what is missing.

## Not downloaded

- Kraken bulk OHLCVT (1.5): download is a Google Drive link; needs a person or a browser.
- Raw tick/trade dumps (Binance trades, Kraken trades, Bybit, BitMEX, Dukascopy): too big for now.
- Hyperliquid funding (4.4, LATER): short history; easy to add to `small.py`.
- Anything needing a key (Polygon, Tiingo, Twelve Data, FRED JSON API).

## Check progress

```sh
ROOT=~/data/grimstrade
tail -n 3 $ROOT/logs/*.log          # each job ends with "DONE errors=N"
grep -c FAIL $ROOT/logs/*.log
du -sh $ROOT/*/
cat $ROOT/pids/*.pid                 # is it still running? ps -p <PID>
```

## How to run the backfills (any computer)

```sh
cp local.example.toml local.toml     # set [cache] root
uv sync
uv run python -I scripts/snapshot_rolling.py
# each family detached, logging into the cache (example for binance):
setsid -f sh -c 'exec .venv/bin/python -I scripts/backfill/binance.py >> <root>/logs/binance.log 2>&1'
# others: rest_1m.py coinbase | bitstamp | bitfinex, small.py, alpaca.py
```

Stop a job only by its own PID from `pids/` (`kill <PID>`), never by name pattern.

## New sources noticed (not yet assessed)

- Binance archive also has `futures/um/monthly/klines` (perp 1m), `markPriceKlines`,
  `indexPriceKlines` (basis = mark vs index) and `futures/cm` (coin-margined): cheap to add to
  `binance.py`.
- Bitstamp's OHLC API goes back to 2011-08 at 1-minute: the longest free BTC minute series found.
- Cboe also publishes VIX6M history (added to `small.py`).
- FRED `RRPONTSYD` (reverse repo) and `T10Y3M`: liquidity and curve signals (added).
