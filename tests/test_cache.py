import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from grimstrade.cache import cache_root, sha256, write_once


def test_write_once_records_checksum_and_refuses_overwrite(tmp_path: Path) -> None:
    t = datetime(2026, 11, 12, 15, 0, tzinfo=UTC)
    write_once(tmp_path, "a/b.json", b"{}", "https://x", t)
    line = json.loads((tmp_path / "manifest.jsonl").read_text())
    assert line == {
        "path": "a/b.json",
        "fetched_at": "2026-11-12T15:00:00Z",
        "url": "https://x",
        "bytes": 2,
        "sha256": sha256(b"{}"),
    }
    with pytest.raises(FileExistsError):
        write_once(tmp_path, "a/b.json", b"other", "https://x", t)
    assert (tmp_path / "a/b.json").read_bytes() == b"{}"


def test_cache_root_reads_local_config(tmp_path: Path) -> None:
    cfg = tmp_path / "local.toml"
    cfg.write_text('[cache]\nroot = "/srv/cache"\n')
    assert cache_root(cfg) == Path("/srv/cache")
    with pytest.raises(SystemExit):
        cache_root(tmp_path / "missing.toml")
