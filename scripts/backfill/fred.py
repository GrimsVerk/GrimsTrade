"""Backfill FRED series and their ALFRED vintages from the official FRED API (free key).

FRED's keyless CSV endpoints stall our honest User-Agent (2026-11-12), so this uses the official
JSON API (`api.stlouisfed.org/fred/series/observations`). The key comes from the env file named in
`local.toml` (`[fred] env_file`, default `~/.config/grimstrade/fred.env` with `FRED_API_KEY=...`),
is sent only as a query parameter and never printed or logged: manifest URLs are written without it.

- `fred/api/latest/<SERIES>/<YYYY-MM-DD>.json`: the series as it reads today (one file per run day).
- `fred/api/vintages/<SERIES>.json`: every value with the period it was valid in
  (`realtime_start` / `realtime_end`), i.e. what was known on each past date (no look-ahead).
  Written once; delete the file by hand to refresh it.

Series lists are `small.FRED` and `small.ALFRED`. Rate limit 120 requests/min; we stay well under.
Resumable: re-run.
"""

from __future__ import annotations

import json
import os
import sys
import time
import tomllib
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from small import ALFRED, FRED  # noqa: E402

from grimstrade.cache import LOCAL_CONFIG, cache_root, start_job, write_once  # noqa: E402

URL = "https://api.stlouisfed.org/fred/series/observations"
PAUSE = 1.0  # 60 requests/min, half the published limit
PAGE = 100_000  # the API's maximum `limit`


def api_key() -> str:
    path = "~/.config/grimstrade/fred.env"
    if LOCAL_CONFIG.exists():
        with LOCAL_CONFIG.open("rb") as f:
            path = tomllib.load(f).get("fred", {}).get("env_file", path)
    with open(os.path.expanduser(path)) as f:
        env = dict(line.strip().split("=", 1) for line in f if "=" in line)
    return env["FRED_API_KEY"]


def fetch_all(key: str, params: dict[str, str]) -> tuple[bytes, str]:
    """All pages of one observations query, merged. Returns (json bytes, URL without the key)."""
    observations: list[dict[str, str]] = []
    offset = 0
    head: dict[str, object] = {}
    while True:
        q = {**params, "file_type": "json", "limit": str(PAGE), "offset": str(offset)}
        url = URL + "?" + urllib.parse.urlencode({**q, "api_key": key})
        req = urllib.request.Request(url, headers={"User-Agent": "grimstrade-research/0.1"})
        with urllib.request.urlopen(req, timeout=120) as r:
            page = json.load(r)
        time.sleep(PAUSE)
        obs = page.pop("observations", [])
        head = head or page
        observations += obs
        if len(obs) < PAGE:
            break
        offset += PAGE
    head["observations"] = observations
    public = URL + "?" + urllib.parse.urlencode(params)
    return json.dumps(head).encode(), public


def main() -> None:
    root = cache_root()
    start_job(root, "fred")
    key = api_key()
    today = datetime.now(UTC).date().isoformat()
    errors = 0
    jobs: list[tuple[str, dict[str, str]]] = [
        (f"fred/api/latest/{s}/{today}.json", {"series_id": s}) for s in FRED
    ]
    jobs += [
        (
            f"fred/api/vintages/{s}.json",
            {"series_id": s, "realtime_start": "1776-07-04", "realtime_end": "9999-12-31"},
        )
        for s in ALFRED
    ]
    for rel, params in jobs:
        if (root / rel).exists():
            continue
        try:
            data, public = fetch_all(key, params)
            write_once(root, rel, data, public)
            n = len(json.loads(data)["observations"])
            print(f"{time.strftime('%H:%M:%S')} {rel}: {n} rows", flush=True)
        except Exception as e:  # noqa: BLE001 - log and go on; a re-run retries
            errors += 1
            print(f"FAIL {rel}: {type(e).__name__} {getattr(e, 'code', '')}", flush=True)
    print(f"DONE errors={errors}", flush=True)


if __name__ == "__main__":
    main()
