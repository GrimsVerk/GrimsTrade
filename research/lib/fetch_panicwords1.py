"""panic-words-1: fetch the American Stories yearly files (keyless, CC-BY 4.0). Raw bytes only.

    uv run python -I research/lib/fetch_panicwords1.py [first_year last_year]

American Stories (Dell et al. 2023, Hugging Face `dell-research-harvard/AmericanStories`) is
article-level text from the public-domain Chronicling America newspaper scans of the Library of
Congress. The loc.gov JSON API (the planned source) answered every scripted request with a
Cloudflare challenge on 2026-11-25 (`cf-mitigated: challenge`); it was not worked around.

Writes `panic-words-1/americanstories/faro_<year>.tar.gz` into the data cache
(`macro.local.json` -> cache_root), never into git. One file at a time, a pause between files,
back-off on 429/5xx. Downloads are untrusted data: this script only saves bytes; the counter
parses them with `python -I`.
"""

from __future__ import annotations

import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from macro import cache_root  # noqa: E402

BASE = "https://huggingface.co/datasets/dell-research-harvard/AmericanStories/resolve/main/"
USER_AGENT = "research-script/0.1 (keyless)"
FIRST, LAST = 1925, 1963  # 1925 gives the 12-month baseline before the first dose month


def fetch(year: int, out: Path) -> None:
    url = f"{BASE}faro_{year}.tar.gz"
    part = out.with_suffix(".part")
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as resp, part.open("wb") as f:
                while chunk := resp.read(1 << 20):
                    f.write(chunk)
            part.rename(out)
            return
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt == 4:
                raise
            wait = 60 * (attempt + 1)
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == 4:
                raise
            wait = 30 * (attempt + 1)
        print(f"  {year}: retry in {wait}s", file=sys.stderr)
        time.sleep(wait)


def main() -> None:
    first, last = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (FIRST, LAST)
    root = cache_root() / "panic-words-1" / "americanstories"
    root.mkdir(parents=True, exist_ok=True)
    for year in range(first, last + 1):
        out = root / f"faro_{year}.tar.gz"
        if out.exists():
            continue
        t0 = time.time()
        fetch(year, out)
        print(f"{year}: {out.stat().st_size} bytes in {time.time() - t0:.0f}s", flush=True)
        time.sleep(2)


if __name__ == "__main__":
    main()
