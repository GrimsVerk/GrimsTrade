"""Local raw-data cache (git-ignored, outside the repo): write-once files plus a manifest.

The cache root comes from `local.toml` (git-ignored; copy `local.example.toml`). Every file is
written once through a temp file and a rename, never edited, and gets a manifest line with its
fetch time, source URL, size and SHA-256. See docs/data-sources.md section 9 and
docs/data-inventory.md.
"""

from __future__ import annotations

import hashlib
import json
import os
import tomllib
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LOCAL_CONFIG = REPO / "local.toml"
MANIFEST = "manifest.jsonl"


def cache_root(config: Path = LOCAL_CONFIG) -> Path:
    """Cache root from the local config (`[cache] root = "~/data/grimstrade"`)."""
    if not config.exists():
        raise SystemExit(f"{config} missing: copy local.example.toml to local.toml and edit it")
    with config.open("rb") as f:
        root = tomllib.load(f)["cache"]["root"]
    return Path(os.path.expanduser(str(root)))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_once(
    root: Path, rel: str, data: bytes, url: str, fetched_at: datetime | None = None
) -> Path:
    """Write `data` to `root/rel` and append its manifest line. Refuses to overwrite."""
    path = root / rel
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".part")
    tmp.write_bytes(data)
    tmp.rename(path)
    stamp = (fetched_at or datetime.now(UTC)).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = {
        "path": rel,
        "fetched_at": stamp,
        "url": url,
        "bytes": len(data),
        "sha256": sha256(data),
    }
    with (root / MANIFEST).open("a") as f:
        f.write(json.dumps(line, sort_keys=True) + "\n")
    return path
