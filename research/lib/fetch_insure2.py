"""insure-2 step 2: fetch non-US stock index history (keyless, public). Raw files only.

    uv run python -I research/lib/fetch_insure2.py

Writes into the data cache (`macro.local.json` -> cache_root), never into git:
- `insure-2/raw-<day>/yahoo/<ticker>.json`: Yahoo chart API, daily, from each index's first day
  to 2025-10-31 (period2 = 2025-11-01 00:00 UTC, so nothing in the held-out year is downloaded).
- `insure-2/raw-<day>/french/<file>.zip`: Ken French data library, regional daily factor files
  (market = Mkt-RF + RF, US dollars, dividends included, from 1990-07).
Downloads are untrusted data: this script only saves bytes; readers parse them with `python -I`.
"""

from __future__ import annotations

import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from macro import cache_root  # noqa: E402

DAY = "2026-11-18"
PERIOD1 = -2208988800  # 1900-01-01
PERIOD2 = 1761955200  # 2025-11-01 00:00 UTC
USER_AGENT = "Mozilla/5.0 (daily-bar research script)"
# Candidates (national headline indices with long daily history on Yahoo); which ones enter the
# study is fixed by the card's rule (first day, data checks), not here.
TICKERS = [
    "^N225", "^GSPTSE", "^FTSE", "^GDAXI", "^FCHI", "^SSMI", "^AEX", "^IBEX", "^AORD", "^HSI",
    "^STI", "^BFX", "^ATX", "^OMX", "^OSEAX", "^NZ50", "FTSEMIB.MI", "^KS11", "^TWII", "^BVSP",
    "^MXX", "^JKSE", "^KLSE", "^BSESN", "^TA125.TA",
]  # fmt: skip
FRENCH = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
FRENCH_FILES = [
    "Developed_ex_US_3_Factors_Daily_CSV.zip",
    "Europe_3_Factors_Daily_CSV.zip",
    "Japan_3_Factors_Daily_CSV.zip",
    "Asia_Pacific_ex_Japan_3_Factors_Daily_CSV.zip",
    "North_America_3_Factors_Daily_CSV.zip",
]


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body: bytes = resp.read()
                return body
        except Exception as e:  # noqa: BLE001 - retry any transient failure
            if attempt == 3:
                raise
            print(f"  retry after {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    raise AssertionError("unreachable")


def main() -> None:
    root = cache_root() / "insure-2" / f"raw-{DAY}"
    (root / "yahoo").mkdir(parents=True, exist_ok=True)
    (root / "french").mkdir(parents=True, exist_ok=True)
    for tk in TICKERS:
        out = root / "yahoo" / f"{tk.lstrip('^')}.json"
        if out.exists():
            continue
        url = (
            "https://query1.finance.yahoo.com/v8/finance/chart/"
            f"{urllib.parse.quote(tk)}?period1={PERIOD1}&period2={PERIOD2}&interval=1d"
        )
        try:
            out.write_bytes(get(url))
            print(f"{tk}: {out.stat().st_size} bytes")
        except Exception as e:  # noqa: BLE001 - a missing index is reported, not fatal
            print(f"{tk}: FAILED {e}", file=sys.stderr)
        time.sleep(1)
    for f in FRENCH_FILES:
        out = root / "french" / f
        if not out.exists():
            out.write_bytes(get(FRENCH + f))
            print(f"{f}: {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
