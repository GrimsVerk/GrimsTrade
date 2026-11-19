"""Snapshot data that only lives in a rolling window, before it falls out.

Yahoo 1-hour bars (~730 days) for SPY, QQQ, GLD, TLT; Kraken Futures funding history (~12 months)
and open interest for PF_XBTUSD, PF_ETHUSD. Raw responses and a tidy CSV go to
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


def main() -> int:
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    since = int(time.time()) - 400 * 86400
    jobs = []
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
        url = (
            f"https://futures.kraken.com/api/charts/v1/analytics/{s}/open-interest"
            f"?since={since}&interval=3600"
        )
        jobs.append((f"snapshots/kraken-oi/{day}", s, url, kraken_oi_csv))
    failed = 0
    for dirpath, name, url, conv in jobs:
        try:
            print(save(dirpath, name, url, conv), flush=True)
        except Exception as e:  # noqa: BLE001 - one source failing must not stop the rest
            failed += 1
            print(f"FAIL {dirpath}/{name}: {e!r}", flush=True)
        time.sleep(1)
    return 1 if failed else 0


def kraken_oi_csv(raw: bytes) -> bytes:
    """Kraken analytics: {"result": {"timestamp": [...], "more": ..., "data": [...]}}."""
    res = json.loads(raw)["result"]
    pairs = zip(res["timestamp"], res["data"], strict=True)
    rows = [{"time": t, "open_interest": v} for t, v in pairs]
    if not rows:
        raise ValueError("empty open-interest series")
    # value for the hour starting at `time`; treat it as known after the hour (+15 min)
    return rows_csv(rows, "time", 3600 + SETTLE)


if __name__ == "__main__":
    sys.exit(main())
