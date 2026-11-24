"""Backfill US ETF 1-minute bars from Alpaca's market-data API (free account) into the cache.

Market data only (`data.alpaca.markets/v2/stocks/bars`): this script never calls a trading or
order endpoint. Keys come from the env file named in `local.toml` (`[alpaca] env_file`), are sent
only as request headers and are never printed or logged. Tries the SIP feed first and falls back
to IEX if the free plan refuses it; the feed is part of the path
(`alpaca/1m-<feed>/<SYM>/<YYYY-MM>.json`, one file per symbol and finished month, all pages).
Raw prices (`adjustment=raw`). Free plan limit ~200 requests/min. Resumable: re-run.
"""

from __future__ import annotations

import json
import os
import sys
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime

from grimstrade.cache import LOCAL_CONFIG, cache_root, start_job, write_once

SYMBOLS = [
    "SPY",
    "QQQ",
    "GLD",
    "TLT",
    "IWM",
    "DIA",
    "EFA",
    "EEM",
    "VNQ",
    "IEF",
    "SHY",
    "LQD",
    "HYG",
    "SLV",
    "USO",
    "UUP",
    "XLE",
    "XLF",
    "XLK",
    "XLV",
]
FIRST = (2016, 1)
URL = "https://data.alpaca.markets/v2/stocks/bars"
PAUSE = 0.35  # ~170 requests/min, under the free plan's 200


def keys() -> dict[str, str]:
    with LOCAL_CONFIG.open("rb") as f:
        path = os.path.expanduser(str(tomllib.load(f)["alpaca"]["env_file"]))
    env: dict[str, str] = {}
    with open(path) as f:
        for line in f:
            k, sep, v = line.strip().partition("=")
            if sep:
                env[k.strip()] = v.strip().strip("\"'")
    return {
        "APCA-API-KEY-ID": env["ALPACA_KEY_ID"],
        "APCA-API-SECRET-KEY": env["ALPACA_SECRET_KEY"],
    }


def get(params: dict[str, str], headers: dict[str, str]) -> bytes:
    req = urllib.request.Request(URL + "?" + urllib.parse.urlencode(params), headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        body: bytes = resp.read()
        return body


def month(sym: str, y: int, m: int, feed: str, headers: dict[str, str]) -> bytes:
    nxt = (y + m // 12, m % 12 + 1)
    params = {
        "symbols": sym,
        "timeframe": "1Min",
        "start": f"{y:04d}-{m:02d}-01T00:00:00Z",
        "end": f"{nxt[0]:04d}-{nxt[1]:02d}-01T00:00:00Z",
        "limit": "10000",
        "adjustment": "raw",
        "feed": feed,
    }
    pages = []
    while True:
        page = json.loads(get(params, headers))
        pages.append(page)
        time.sleep(PAUSE)
        token = page.get("next_page_token")
        if not token:
            return json.dumps(pages).encode()
        params["page_token"] = token


def pick_feed(headers: dict[str, str]) -> str:
    try:
        month("SPY", 2020, 1, "sip", headers)
        return "sip"
    except urllib.error.HTTPError as e:
        print(f"SIP refused (HTTP {e.code}); using IEX", flush=True)
        return "iex"


def main() -> int:
    root = cache_root()
    start_job(root, "alpaca")
    headers = keys()
    feed = pick_feed(headers)
    print(f"feed={feed}", flush=True)
    now = datetime.now(UTC)
    errors = 0
    for sym in SYMBOLS:
        y, m = FIRST
        new = 0
        while (y, m) < (now.year, now.month):  # finished months only
            rel = f"alpaca/1m-{feed}/{sym}/{y:04d}-{m:02d}.json"
            if not (root / rel).exists():
                url = f"{URL}?symbols={sym}&timeframe=1Min&feed={feed}&month={y:04d}-{m:02d}"
                try:
                    write_once(root, rel, month(sym, y, m, feed, headers), url)
                    new += 1
                except Exception as e:  # noqa: BLE001 - message holds no headers
                    errors += 1
                    print(f"FAIL {rel}: {type(e).__name__} {getattr(e, 'code', '')}", flush=True)
                    time.sleep(60)
            y, m = (y + m // 12, m % 12 + 1)
        print(f"{time.strftime('%H:%M:%S')} {sym}: {new} new months", flush=True)
    print(f"DONE errors={errors}", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
