"""Download the keyless inputs of lane weather-2 (card `research/weather-2.md`), resumable.

    uv run python -I scripts/fetch_weather2.py

Writes under `<cache_root>/weather-2/` (`research/macro.local.json`, or GRIMSTRADE_DATA):
- `cpc-gis/{610,814}temp_YYYYMMDD.zip`: CPC 6-10 and 8-14 day temperature outlook
  shapefiles, issue dates 2012-09-11 .. 2025-11-09, only days from October 20 to March 31
  (the season needs issues back to late October). No issue after 2025-11-09 is requested.
- `census/CenPop2010_Mean_ST.txt`: 2010 state population centroids.

Every file is written once (temp file + rename); a rerun skips files already there. A
missing file (HTTP 404) is recorded in `cpc-gis/missing.txt` and not retried. The files are
untrusted data: nothing here opens them; the parser reads them with `python -I`.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from pathlib import Path

UA = "research-script/0.1 (python urllib)"
PAUSE_S = 0.25
WORKERS = 4  # polite: four connections at a time
GIS = "https://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/"
CENSUS = "https://www2.census.gov/geo/docs/reference/cenpop2010/CenPop2010_Mean_ST.txt"
FIRST = date(2012, 9, 11)
LAST = date(2025, 11, 9)  # held-out cut: never request a later issue


def cache_root() -> Path:
    env = os.environ.get("GRIMSTRADE_DATA")
    if env:
        return Path(env).expanduser()
    cfg = Path(__file__).resolve().parents[1] / "research" / "macro.local.json"
    return Path(json.loads(cfg.read_text())["cache_root"]).expanduser()


def in_season(d: date) -> bool:
    return d.month in (11, 12, 1, 2, 3) or (d.month == 10 and d.day >= 20)


def jobs() -> list[tuple[str, str]]:
    out = [("census/CenPop2010_Mean_ST.txt", CENSUS)]
    d = FIRST
    while d <= LAST:
        if in_season(d):
            for lead in ("610", "814"):
                name = f"{lead}temp_{d:%Y%m%d}.zip"
                out.append((f"cpc-gis/{name}", GIS + name))
        d += timedelta(days=1)
    return out


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return bytes(r.read())


def get_one(root: Path, rel: str, url: str) -> str:
    """'new', 'missing' or 'bad'; writes the file once (temp file + rename)."""
    dest = root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        body = fetch(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "missing"
        raise
    finally:
        time.sleep(PAUSE_S)
    if body[:2] != b"PK" and rel.endswith(".zip"):
        print("not a zip, skipped:", url, file=sys.stderr)
        return "bad"
    tmp = dest.with_suffix(dest.suffix + ".part")
    tmp.write_bytes(body)
    tmp.rename(dest)
    return "new"


def main() -> None:
    root = cache_root() / "weather-2"
    missing_path = root / "cpc-gis" / "missing.txt"
    missing_path.parent.mkdir(parents=True, exist_ok=True)
    missing = set(missing_path.read_text().split()) if missing_path.exists() else set()
    todo = [(r, u) for r, u in jobs() if not (root / r).exists() and r not in missing]
    counts = {"new": 0, "missing": 0, "bad": 0}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(get_one, root, r, u): r for r, u in todo}
        for fut in as_completed(futs):
            res = fut.result()
            counts[res] += 1
            if res == "missing":
                with missing_path.open("a") as f:
                    f.write(futs[fut] + "\n")
    print(f"todo {len(todo)}: {counts}")


if __name__ == "__main__":
    main()
