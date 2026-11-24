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
- World Bank Pink Sheet monthly history (CC BY 4.0) is NOT fetched by this script: its CDN
  refused the script's agent (HTTP 403, 2026-11-24) and answers browsers. Download `PINK` by
  hand in a browser into `<cache_root>/data-long-3/worldbank/<date>/CMO-Historical-Data-
  Monthly.xlsx`; `long_x.parse_pink` reads it (cut at 2025-10).
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
# Fed H.10 noon buying rates in New York (daily). The daily mark (DEXGEUS) is not on ALFRED
# (404) nor in the Fed's H.10 package; EXGEUS is its monthly average, 1971-01 to 2001-12.
FX = [
    "DEXJPUS", "DEXUSUK", "DEXSZUS", "DEXCAUS", "EXGEUS", "DEXUSEU",
    "DEXUSAL", "DEXUSNZ", "DEXSDUS", "DEXNOUS",
]  # fmt: skip
# OECD Main Economic Indicators via FRED: 3-month interbank, call money, 10y government
COUNTRIES = ["JP", "GB", "CH", "CA", "DE", "EZ", "AU", "NZ", "SE", "NO", "US"]
OECD = (
    [f"IR3TIB01{c}M156N" for c in COUNTRIES]
    + [f"IRSTCI01{c}M156N" for c in COUNTRIES]
    + [f"IRLTLT01{c}M156N" for c in COUNTRIES]
)
# IMF International Financial Statistics via FRED (monthly; fill the OECD short-rate gaps
# before the mid-1980s): discount rate, Treasury bill rate (money market INTMMR*: 404)
IMF = [
    f"{k}{c}M193N"
    for k in ("INTDSR", "INTGST")
    for c in ("JP", "GB", "CH", "CA", "DE", "AU", "NZ", "SE", "NO", "US")
]
# BLS producer prices (commodity groups) and EIA/Dow Jones oil
# BLS PPI (price on the Tuesday of the week with the 13th, not a monthly average):
# all commodities, farm products, grains, wheat, slaughter livestock, coal, natural gas, crude
# petroleum, metals, iron and steel, nonferrous metals, primary nonferrous metals
COMMOD = [
    "PPIACO", "WPU01", "WPU012", "WPU0121", "WPU013", "WPU051", "WPU0531", "WPU0561",
    "WPU10", "WPU101", "WPU102", "WPU1022", "WTISPLC", "DCOILWTICO",
]  # fmt: skip
# IMF Primary Commodity Prices via FRED (monthly averages, from 1990): cross-checks only
IMF_PCPS = ["POILWTIUSDM", "PCOPPUSDM", "PWHEAMTUSDM", "PMAIZMTUSDM", "PNGASUSUSDM"]
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
        for s in RATES_US + FX + OECD + COMMOD + IMF + IMF_PCPS
    ]
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
