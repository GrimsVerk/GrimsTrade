"""insure-3: fetch CBOE option-strategy benchmark indices and the S&P 500 total return (keyless).

    uv run python -I research/lib/fetch_insure3.py

Writes into the data cache (`macro.local.json` -> cache_root), never into git:
- `insure-3/raw-<day>/cboe/<name>.csv`: CBOE's public daily history files. They come as whole
  files up to today, so rows after LAST are dropped here, before anything is written: no
  held-out bar is stored. CBOE's terms (cboe.com/terms, section 2) allow one copy for personal
  non-commercial use and forbid redistribution: raw levels stay in the cache, git gets only
  derived statistics.
- `insure-3/raw-<day>/yahoo/SP500TR.json`: Yahoo chart API, daily, period2 = 2025-11-01.
A refused source (any HTTP error) is reported and skipped, never retried another way.
Downloads are untrusted data: this script only saves bytes (and drops late CSV lines by their
date field); readers parse them with `python -I`.
"""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from macro import cache_root  # noqa: E402

DAY = "2026-11-24"
LAST = date(2025, 10, 31)
USER_AGENT = "Mozilla/5.0 (daily-bar research script)"
CBOE = ["PPUT", "PUT", "BXM", "CLL", "VXTH", "SPXTR"]
CBOE_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/{n}_History.csv"
SP500TR = (
    "https://query1.finance.yahoo.com/v8/finance/chart/%5ESP500TR"
    "?period1=-2208988800&period2=1761955200&interval=1d"
)


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:  # follows the 307 to cdn-api
        body: bytes = resp.read()
        return body


def truncate_csv(text: str, last: date = LAST) -> str:
    """Header plus the rows dated on or before `last` (CBOE dates are MM/DD/YYYY)."""
    lines = text.splitlines()
    keep = [lines[0]]
    for line in lines[1:]:
        cell = line.split(",", 1)[0].strip()
        try:
            d = datetime.strptime(cell, "%m/%d/%Y").date()
        except ValueError:
            continue
        if d <= last:
            keep.append(line)
    return "\n".join(keep) + "\n"


def main() -> None:
    root = cache_root() / "insure-3" / f"raw-{DAY}"
    (root / "cboe").mkdir(parents=True, exist_ok=True)
    (root / "yahoo").mkdir(parents=True, exist_ok=True)
    for n in CBOE:
        out = root / "cboe" / f"{n}.csv"
        if out.exists():
            continue
        try:
            body = get(CBOE_URL.format(n=n)).decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            print(f"{n}: refused, HTTP {e.code} (recorded, not retried)")
            continue
        if not body.startswith("DATE,"):
            print(f"{n}: not a CSV ({body[:40]!r}), skipped")
            continue
        out.write_text(truncate_csv(body))
        print(f"{n}: {len(out.read_text().splitlines()) - 1} rows kept")
    out = root / "yahoo" / "SP500TR.json"
    if not out.exists():
        out.write_bytes(get(SP500TR))
        print(f"SP500TR: {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
