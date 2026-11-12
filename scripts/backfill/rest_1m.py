"""Backfill BTC and ETH 1-minute bars from exchange REST APIs into the local cache.

`python -I scripts/backfill/rest_1m.py <coinbase|bitstamp|bitfinex>`. Time is cut into fixed,
epoch-aligned chunks of one request each (300 / 1,000 / 10,000 minutes); each chunk's raw
response is written once to `<source>/1m/<pair>/<year>/<chunk start unix>.json`. Only chunks that
closed 15+ minutes ago are fetched. Resumable: re-run skips chunks already saved. Empty minutes
are simply absent (never filled). No checksums are published by these APIs; the manifest keeps
our own SHA-256.
"""

from __future__ import annotations

import sys
import time
from datetime import UTC, datetime

from grimstrade.cache import cache_root, fetch_file, start_job
from grimstrade.sources import http_get


def _iso(t: int) -> str:
    return datetime.fromtimestamp(t, tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# source: (minutes per request, seconds between requests, {pair: first day}, url(pair, start, end))
SOURCES = {
    "coinbase": (
        300,
        0.15,  # public limit 10 req/s
        {"BTC-USD": "2015-07-20", "ETH-USD": "2016-05-18"},
        lambda p, s, e: (
            f"https://api.exchange.coinbase.com/products/{p}/candles"
            f"?granularity=60&start={_iso(s)}&end={_iso(e - 60)}"
        ),
    ),
    "bitstamp": (
        1000,
        0.2,  # published limit 400 req/s, 10,000 per 10 min
        {"btcusd": "2011-08-18", "ethusd": "2017-08-17"},
        lambda p, s, e: (
            f"https://www.bitstamp.net/api/v2/ohlc/{p}/?step=60&limit=1000&start={s}&end={e - 60}"
        ),
    ),
    "bitfinex": (
        10000,
        2.5,  # published limit 30 req/min for candles
        {"tBTCUSD": "2013-04-01", "tETHUSD": "2016-03-09"},
        lambda p, s, e: (
            f"https://api-pub.bitfinex.com/v2/candles/trade:1m:{p}/hist"
            f"?start={s * 1000}&end={(e - 60) * 1000}&limit=10000&sort=1"
        ),
    ),
}


def main(source: str) -> int:
    minutes, pause, pairs, url = SOURCES[source]
    root = cache_root()
    start_job(root, f"rest_1m-{source}")
    step = minutes * 60
    now = int(time.time())
    errors = 0
    for pair, first in pairs.items():
        t0 = int(datetime.fromisoformat(first).replace(tzinfo=UTC).timestamp())
        s = t0 - t0 % step
        new = 0
        while s + step + 900 <= now:
            rel = f"{source}/1m/{pair}/{datetime.fromtimestamp(s, tz=UTC).year}/{s}.json"
            if not (root / rel).exists():
                for attempt in range(5):
                    try:
                        fetch_file(root, rel, url(pair, s, s + step), http_get)
                        new += 1
                        break
                    except Exception as e:  # noqa: BLE001
                        print(f"retry {attempt} {rel}: {e!r}", flush=True)
                        time.sleep(30 * (attempt + 1))
                else:
                    errors += 1
                    print(f"FAIL {rel}", flush=True)
                time.sleep(pause)
                if new % 500 == 0 and new:
                    print(f"{time.strftime('%H:%M:%S')} {pair} at {_iso(s)}", flush=True)
            s += step
        print(f"{time.strftime('%H:%M:%S')} {source} {pair}: {new} new chunks", flush=True)
    print(f"DONE errors={errors}", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
