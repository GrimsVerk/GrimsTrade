"""Backfill the Binance public archive (data.binance.vision) into the local cache.

Funding rates, premium index (1h), spot 1-minute klines and futures metrics (5-minute open
interest, long/short ratios) for ~30 liquid USDT pairs. Lists the bucket, downloads each zip once,
verifies it against Binance's `.CHECKSUM`, skips what is already there. Resumable: just re-run.
Run detached: see docs/data-inventory.md ("How to run the backfills").
"""

from __future__ import annotations

import re
import sys
import time

from grimstrade.cache import CAP_BYTES, cache_root, fetch_file, start_job, used_bytes
from grimstrade.sources import http_get

PAIRS = [
    "BTC",
    "ETH",
    "BNB",
    "SOL",
    "XRP",
    "DOGE",
    "ADA",
    "TRX",
    "AVAX",
    "LINK",
    "DOT",
    "LTC",
    "BCH",
    "NEAR",
    "UNI",
    "ATOM",
    "ETC",
    "XLM",
    "FIL",
    "APT",
    "ARB",
    "OP",
    "SUI",
    "INJ",
    "AAVE",
    "HBAR",
    "ICP",
    "TON",
    "MKR",
    "SEI",
]
DATASETS = [  # (prefix template, which pairs); cheap ones first, BTC/ETH first within each
    ("data/futures/um/monthly/fundingRate/{s}/", PAIRS),
    ("data/futures/um/monthly/premiumIndexKlines/{s}/1h/", PAIRS),
    ("data/spot/monthly/klines/{s}/1m/", PAIRS),
    ("data/futures/um/daily/metrics/{s}/", PAIRS),
]
LIST = (
    "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix={p}&marker={m}"
)
BASE = "https://data.binance.vision/"
PAUSE = 0.2  # no published limit for the archive; stay polite


def keys(prefix: str) -> list[str]:
    out: list[str] = []
    marker = ""
    while True:
        body = http_get(LIST.format(p=prefix, m=marker)).decode()
        page = re.findall(r"<Key>([^<]+)</Key>", body)
        out += page
        if "<IsTruncated>true</IsTruncated>" not in body or not page:
            return out
        marker = page[-1]


def main() -> int:
    root = cache_root()
    start_job(root, "binance")
    errors = 0
    for template, pairs in DATASETS:
        for p in pairs:
            prefix = template.format(s=f"{p}USDT")
            if used_bytes(root) > CAP_BYTES:  # checked per prefix (one prefix is < 1 GB)
                print("STOP cache cap reached", flush=True)
                return 2
            try:
                zips = [k for k in keys(prefix) if k.endswith(".zip")]
            except Exception as e:  # noqa: BLE001
                print(f"FAIL list {prefix}: {e!r}", flush=True)
                errors += 1
                continue
            done = 0
            for k in zips:
                rel = "binance/" + k.removeprefix("data/")
                if (root / rel).exists():
                    continue
                try:
                    sha = http_get(BASE + k + ".CHECKSUM").decode().split()[0]
                    fetch_file(root, rel, BASE + k, http_get, sha)
                    done += 1
                except Exception as e:  # noqa: BLE001
                    print(f"FAIL {k}: {e!r}", flush=True)
                    errors += 1
                time.sleep(PAUSE)
            print(
                f"{time.strftime('%H:%M:%S')} {prefix}: {len(zips)} files, {done} new", flush=True
            )
    print(f"DONE errors={errors}", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
