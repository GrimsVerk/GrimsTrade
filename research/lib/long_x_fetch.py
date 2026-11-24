"""Fetch the data-long-3 raw files into the git-ignored cache (research/data-long-3.md).

    uv run python -I research/lib/long_x_fetch.py            # everything not yet cached
    uv run python -I research/lib/long_x_fetch.py --list     # print the plan only

Keyless public sources only. Every file is written once through `grimstrade.cache.write_once`
(manifest line with URL, time, size, SHA-256) under `<cache_root>/data-long-3/`. Nothing here is
committed. The cache root is `research/macro.local.json` (git-ignored, copy the `.example`) or
GRIMSTRADE_DATA.

- ALFRED (St. Louis Fed), vintage 2025-11-10: each series as it was known on that day, so no
  observation of the held-out year (from 2025-11-11) and no later revision is ever on disk.
  `alfred/<vintage>/<ID>.csv`. Plain fredgraph.csv did not answer from this machine (2026-11-18
  and 2026-11-24); ALFRED's graph CSV did.
- World Bank Pink Sheet monthly history (CC BY 4.0): `worldbank/<date>/CMO-Historical-Data-
  Monthly.xlsx`. The file runs to the latest month; the loader cuts at 2025-10.
- Yahoo daily chart JSON for the CurrencyShares trusts (validation only, 2025-11-10 last bar):
  `yahoo/<date>/<T>.json`.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from grimstrade import cache  # noqa: E402

VINTAGE = "2025-11-10"
SNAP = "2026-11-24"
UA = "Mozilla/5.0 (daily-bar research script)"
ALFRED = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={id}&vintage_date={v}"
PINK = (
    "https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021/"
    "related/CMO-Historical-Data-Monthly.xlsx"
)
# period2 = 2025-11-11 00:00 UTC: the last daily bar is 2025-11-10
YAHOO = (
    "https://query2.finance.yahoo.com/v8/finance/chart/{t}"
    "?period1=0&period2=1762819200&interval=1d&events=div"
)

# Fed H.15 Treasury constant maturity and bills
RATES_US = [
    "DGS1", "DGS2", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30",
    "GS1", "GS2", "GS5", "GS7", "GS10", "GS20", "GS30", "DTB3", "TB3MS",
]  # fmt: skip
# Fed H.10 noon buying rates in New York (daily)
FX = [
    "DEXJPUS", "DEXUSUK", "DEXSZUS", "DEXCAUS", "DEXGEUS", "DEXUSEU",
    "DEXUSAL", "DEXUSNZ", "DEXSDUS", "DEXNOUS",
]  # fmt: skip
# OECD Main Economic Indicators via FRED: 3-month interbank, call money, 10y government
COUNTRIES = ["JP", "GB", "CH", "CA", "DE", "EZ", "AU", "NZ", "SE", "NO", "US"]
OECD = (
    [f"IR3TIB01{c}M156N" for c in COUNTRIES]
    + [f"IRSTCI01{c}M156N" for c in COUNTRIES]
    + [f"IRLTLT01{c}M156N" for c in COUNTRIES]
)
# BLS producer prices (commodity groups) and EIA/Dow Jones oil
COMMOD = ["PPIACO", "WPU10", "WPU05", "WPU01", "WPU0211", "WTISPLC", "DCOILWTICO"]
YAHOO_ETFS = ["FXE", "FXY", "FXB", "FXF", "FXC", "FXA"]


def cache_root() -> Path:
    env = os.environ.get("GRIMSTRADE_DATA")
    if env:
        return Path(env).expanduser()
    cfg = ROOT / "research" / "macro.local.json"
    return Path(json.loads(cfg.read_text())["cache_root"]).expanduser()


def _get(url: str, tries: int = 3) -> bytes:
    # The St. Louis Fed's CDN resets requests with browser-like or "research script" agents
    # (seen 2026-11-24) and answers urllib's default agent; Yahoo wants a browser-like one.
    headers = {"User-Agent": UA} if "yahoo" in url else {}
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as r:
                data: bytes = r.read()
            return data
        except Exception as e:  # noqa: BLE001 - report and retry, then give up
            print(f"  try {k + 1}: {e}")
            time.sleep(3 * (k + 1))
    raise RuntimeError(f"failed: {url}")


def plan() -> list[tuple[str, str]]:
    out = [
        (f"data-long-3/alfred/{VINTAGE}/{s}.csv", ALFRED.format(id=s, v=VINTAGE))
        for s in RATES_US + FX + OECD + COMMOD
    ]
    out.append((f"data-long-3/worldbank/{SNAP}/CMO-Historical-Data-Monthly.xlsx", PINK))
    out += [(f"data-long-3/yahoo/{SNAP}/{t}.json", YAHOO.format(t=t)) for t in YAHOO_ETFS]
    return out


def main() -> None:
    root = cache_root()
    failed = []
    for rel, url in plan():
        if "--list" in sys.argv:
            print(rel, url)
            continue
        if (root / rel).exists():
            continue
        try:
            data = _get(url)
        except RuntimeError as e:
            failed.append(rel)
            print(e)
            continue
        if rel.endswith(".csv") and not data.startswith(b"observation_date"):
            failed.append(rel)
            print(f"not a series csv: {rel} ({data[:60]!r})")
            continue
        cache.write_once(root, rel, data, url)
        print(f"ok {rel} {len(data)}", flush=True)
        time.sleep(1.0)
    print("failed:", failed)


if __name__ == "__main__":
    main()
