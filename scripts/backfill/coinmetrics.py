"""Backfill every free (community) daily asset metric from Coin Metrics, for every asset.

Keyless community API (`community-api.coinmetrics.io/v4`). The free tier only serves asset
metrics (exchange, pair and market endpoints need a paid key), so "everything free" means:
for each asset in `catalog-v2/asset-metrics`, every metric it has at frequency `1d`.
Sub-daily reference rates (1s/1m/1h) are skipped: we already collect exchange 1-minute bars.

Layout under the cache root (one folder per snapshot date, written once):
- `coinmetrics/full/<DATE>/catalog-v2-asset-metrics.json`: which metrics each asset has.
- `coinmetrics/full/<DATE>/catalog-asset-metrics.json`: metric names and descriptions.
- `coinmetrics/full/<DATE>/assets/<ASSET>/page-NNN.json`: raw API pages (follow `next_page_url`).

Community rate limit is 10 requests / 6 seconds per IP; we send about one per second.
Resumable: re-run with the same date (`coinmetrics.py 2026-11-13`); default date is today (UTC).
Coin Metrics community data is CC BY-NC 4.0: personal research only, keep it local.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
from datetime import UTC, datetime

from grimstrade.cache import cache_root, fetch_file, start_job
from grimstrade.sources import http_get

API = "https://community-api.coinmetrics.io/v4"
PAUSE = 1.0
CHUNK = 40  # metrics per request, keeps URLs short
SAFE = re.compile(r"[a-z0-9][a-z0-9_.-]*")


def get(url: str) -> bytes:
    """http_get with a few retries for timeouts and 429/5xx."""
    for attempt in range(5):
        try:
            data = http_get(url)
            time.sleep(PAUSE)
            return data
        except Exception as e:  # noqa: BLE001 - retried, then re-raised
            code = getattr(e, "code", None)
            if code is not None and code not in (429, 500, 502, 503, 504):
                raise
            print(f"retry {attempt} {url[:120]}: {e!r}", flush=True)
            time.sleep(10 * (attempt + 1))
    return http_get(url)


def main() -> int:
    root = cache_root()
    start_job(root, "coinmetrics")
    day = sys.argv[1] if len(sys.argv) > 1 else datetime.now(UTC).date().isoformat()
    base = f"coinmetrics/full/{day}"
    fetch_file(root, f"{base}/catalog-asset-metrics.json", f"{API}/catalog/asset-metrics", get)
    cat_rel = f"{base}/catalog-v2-asset-metrics.json"
    fetch_file(root, cat_rel, f"{API}/catalog-v2/asset-metrics?page_size=10000", get)
    catalog = json.loads((root / cat_rel).read_bytes())
    if catalog.get("next_page_url"):
        print("WARN catalog has more than one page; only the first is used", flush=True)

    jobs: list[tuple[str, list[str]]] = []
    for a in catalog["data"]:
        metrics = sorted(
            m["metric"]
            for m in a["metrics"]
            if any(f["frequency"] == "1d" for f in m["frequencies"])
        )
        if metrics and SAFE.fullmatch(a["asset"]):
            jobs.append((a["asset"], metrics))
        elif metrics:
            print(f"SKIP odd asset id {a['asset']!r}", flush=True)
    print(f"{len(jobs)} assets, {sum(len(m) for _, m in jobs)} series", flush=True)

    errors = 0
    for i, (asset, metrics) in enumerate(jobs):
        for c in range(0, len(metrics), CHUNK):
            part = metrics[c : c + CHUNK]
            tag = "" if len(metrics) <= CHUNK else f"m{c // CHUNK}-"
            q = urllib.parse.urlencode(
                {
                    "assets": asset,
                    "metrics": ",".join(part),
                    "frequency": "1d",
                    "page_size": "10000",
                    "ignore_forbidden_errors": "true",
                    "ignore_unsupported_errors": "true",
                }
            )
            url: str = f"{API}/timeseries/asset-metrics?{q}"
            page = 0
            while url:
                rel = f"{base}/assets/{asset}/{tag}page-{page:03d}.json"
                try:
                    fetch_file(root, rel, url, get)
                    url = json.loads((root / rel).read_bytes()).get("next_page_url", "")
                except Exception as e:  # noqa: BLE001 - log and go on; a re-run retries
                    errors += 1
                    print(f"FAIL {rel}: {e!r}", flush=True)
                    break
                page += 1
        if i % 100 == 0:
            print(f"{time.strftime('%H:%M:%S')} {i}/{len(jobs)} {asset}", flush=True)
    print(f"DONE errors={errors}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
