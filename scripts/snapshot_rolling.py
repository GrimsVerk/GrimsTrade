"""Snapshot data that only lives in a rolling window, before it falls out.

Yahoo 1-hour bars (~730 days) for SPY, QQQ, GLD, TLT; Kraken Futures funding history (~12 months)
and open interest for PF_XBTUSD, PF_ETHUSD (every hour served, paged forward from
`grimstrade.intraday.OI_START`; the raw file holds every page). Raw responses and a tidy CSV go to
`<cache>/snapshots/<source>/<date>/`, each written once with a manifest line (fetch time, SHA-256).
Re-running on the same day skips what is already there. Run: `uv run python -I
scripts/snapshot_rolling.py`.
"""

from __future__ import annotations

import csv
import io
import json
import sys
import time
from datetime import UTC, datetime
from typing import Any

from grimstrade.cache import cache_root, write_once
from grimstrade.intraday import OI_FIELDS, OI_START, kraken_open_interest
from grimstrade.sources import http_get

ETFS = ["SPY", "QQQ", "GLD", "TLT"]
PERPS = ["PF_XBTUSD", "PF_ETHUSD"]
SETTLE = 15 * 60  # seconds after a period closes before we call it known


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def yahoo_csv(raw: bytes) -> bytes:
    res = json.loads(raw)["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(["open_time", "open", "high", "low", "close", "volume", "available_at"])
    for i, ts in enumerate(res.get("timestamp") or []):
        row = [q[k][i] for k in ("open", "high", "low", "close", "volume")]
        # bar timestamp = open; the last bar may still be open: available_at tells.
        w.writerow([iso(ts), *("" if v is None else v for v in row), iso(ts + 3600 + SETTLE)])
    return out.getvalue().encode()


def rows_csv(rows: list[dict[str, Any]], time_key: str, lag: int) -> bytes:
    out = io.StringIO()
    keys = sorted({k for r in rows for k in r})
    w = csv.writer(out, lineterminator="\n")
    w.writerow([*keys, "available_at"])
    for r in rows:
        t = r.get(time_key)
        if isinstance(t, str):
            ts = datetime.fromisoformat(t.replace("Z", "+00:00")).timestamp()
        else:
            ts = float(t) / (1000 if float(t) > 1e11 else 1)
        w.writerow([*(r.get(k, "") for k in keys), iso(ts + lag)])
    return out.getvalue().encode()


def save(dirpath: str, name: str, url: str, to_csv: Any) -> str:
    root = cache_root()
    raw_rel, csv_rel = f"{dirpath}/{name}.json", f"{dirpath}/{name}.csv"
    if (root / raw_rel).exists():
        return f"skip {raw_rel} (already saved)"
    fetched = datetime.now(UTC)
    raw = http_get(url)
    tidy = to_csv(raw)  # parse before writing, so a bad body fails loudly
    write_once(root, raw_rel, raw, url, fetched)
    write_once(root, csv_rel, tidy, url, fetched)
    return f"ok   {raw_rel} {len(raw)} B, {tidy.count(b'\n') - 1} rows"


def save_oi(dirpath: str, symbol: str) -> str:
    """Open interest needs many calls (2,000 hours each): fetch them all, then write once."""
    root = cache_root()
    raw_rel, csv_rel = f"{dirpath}/{symbol}.json", f"{dirpath}/{symbol}.csv"
    if (root / raw_rel).exists():
        return f"skip {raw_rel} (already saved)"
    fetched = datetime.now(UTC)
    pages: list[dict[str, Any]] = []

    def get(url: str) -> bytes:
        time.sleep(1)
        body = http_get(url)
        pages.append({"url": url, "body": json.loads(body)})
        return body

    rows = kraken_open_interest(symbol, OI_START, fetched, get)
    if not rows:
        raise ValueError("empty open-interest series")
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=OI_FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    write_once(root, raw_rel, json.dumps(pages).encode(), pages[0]["url"], fetched)
    write_once(root, csv_rel, out.getvalue().encode(), pages[0]["url"], fetched)
    return f"ok   {raw_rel} {len(pages)} pages, {len(rows)} rows from {rows[0]['time']}"


def main() -> int:
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    jobs: list[tuple[str, str, str, Any]] = []
    for t in ETFS:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=730d&interval=1h"
        jobs.append((f"snapshots/yahoo-1h/{day}", t, url, yahoo_csv))
    for s in PERPS:
        url = f"https://futures.kraken.com/derivatives/api/v4/historicalfundingrates?symbol={s}"
        # funding timestamp = settlement time, so known from then (+15 min)
        jobs.append(
            (
                f"snapshots/kraken-funding/{day}",
                s,
                url,
                lambda b: rows_csv(json.loads(b)["rates"], "timestamp", SETTLE),
            )
        )
    failed = 0
    for dirpath, name, url, conv in jobs:
        try:
            print(save(dirpath, name, url, conv), flush=True)
        except Exception as e:  # noqa: BLE001 - one source failing must not stop the rest
            failed += 1
            print(f"FAIL {dirpath}/{name}: {e!r}", flush=True)
        time.sleep(1)
    for s in PERPS:
        try:
            print(save_oi(f"snapshots/kraken-oi/{day}", s), flush=True)
        except Exception as e:  # noqa: BLE001 - one source failing must not stop the rest
            failed += 1
            print(f"FAIL snapshots/kraken-oi/{day}/{s}: {e!r}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
