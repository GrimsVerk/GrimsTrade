"""Download the keyless sources for research run info-1 into the raw-data cache (resumable).

    uv run python -I scripts/fetch_info1.py

Cache root from `[cache] root` in the git-ignored `local.toml` (copy `local.example.toml`).
Every file is written once (temp file + rename); a rerun skips files already there. One line
per new file is appended to `<root>/manifest.jsonl` (path, fetched_at, url, bytes, sha256), as
ingest-1 does. Whole-history files go in a dated folder so later snapshots sit beside them.
Never commit the downloaded files. A source that answers with an HTML page (bot check, login)
instead of data is skipped and reported, never worked around.

Sources:
- CFTC Commitments of Traders, futures only: legacy report (1986-) and Traders in Financial
  Futures (2006-), yearly zips from cftc.gov/files/dea/history.
- Cboe put/call ratio history (total, equity, index), cdn.cboe.com (about 2006-2019).
- AAII sentiment survey: not fetched (aaii.com answered 403 to a plain client, 2026-11-13).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import tomllib
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

UA = "grimstrade-research/0.1 (personal non-commercial research; python urllib)"
PAUSE_S = 2.0
TODAY = datetime.now(UTC).date().isoformat()
CFTC = "https://www.cftc.gov/files/dea/history/"
CBOE = "https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/"


def cache_root() -> Path:
    cfg = Path(__file__).resolve().parents[1] / "local.toml"
    with cfg.open("rb") as f:
        return Path(tomllib.load(f)["cache"]["root"]).expanduser()


def jobs() -> list[tuple[str, str]]:
    """(relative path, url). COT yearly files are final once the year is over, so they are
    not dated; the current year's file and the snapshots are dated."""
    out = [
        ("cftc/legacy/deacot1986_2016.zip", CFTC + "deacot1986_2016.zip"),
        ("cftc/tff/fin_fut_txt_2006_2016.zip", CFTC + "fin_fut_txt_2006_2016.zip"),
    ]
    for y in range(2017, 2026):
        out.append((f"cftc/legacy/deacot{y}.zip", CFTC + f"deacot{y}.zip"))
        out.append((f"cftc/tff/fut_fin_txt_{y}.zip", CFTC + f"fut_fin_txt_{y}.zip"))
    for name in ("totalpc.csv", "equitypc.csv", "indexpc.csv"):
        out.append((f"cboe-pc/{TODAY}/{name}", CBOE + name))
    return out


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return bytes(r.read())


def looks_like_html(body: bytes) -> bool:
    head = body[:512].lstrip().lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html")


def save(root: Path, rel: str, url: str, body: bytes) -> None:
    dst = root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".part")
    tmp.write_bytes(body)
    os.replace(tmp, dst)
    line = {
        "bytes": len(body),
        "fetched_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "path": rel,
        "sha256": hashlib.sha256(body).hexdigest(),
        "url": url,
    }
    data = (json.dumps(line, sort_keys=True) + "\n").encode()
    fd = os.open(root / "manifest.jsonl", os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, data)  # one write per line: O_APPEND keeps lines whole
    finally:
        os.close(fd)


def main() -> int:
    root = cache_root()
    errors = 0
    for rel, url in jobs():
        if (root / rel).exists():
            print(f"skip {rel}")
            continue
        try:
            body = fetch(url)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"FAIL {url}: {e}")
            errors += 1
            time.sleep(PAUSE_S)
            continue
        if looks_like_html(body):
            print(f"SKIP {url}: got an HTML page (login or bot check?), not saved")
            errors += 1
        else:
            save(root, rel, url, body)
            print(f"ok   {rel} ({len(body)} bytes)")
        time.sleep(PAUSE_S)
    print(f"DONE errors={errors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
