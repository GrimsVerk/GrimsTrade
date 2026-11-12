"""The forward-test ledger: append-only JSONL, committed before outcomes exist.

- `ledger/decisions.jsonl`: one line per decision (UTC time, strategy, weights, prices seen,
  last bar date seen per asset, reason).
- `ledger/tries.jsonl`: one line per strategy ever tried, live or dead (for the deflated Sharpe).

Git history is the tamper evidence: `check_append_only` fails if any committed line was changed.
"""

from __future__ import annotations

import functools
import json
import subprocess
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from grimstrade.data import History

DECISIONS = Path("ledger/decisions.jsonl")
TRIES = Path("ledger/tries.jsonl")


class LedgerTampered(Exception):
    pass


def _append(path: Path, entry: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")


def _read(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def iso(t: datetime) -> str:
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_time(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def write_decision(
    root: Path,
    time: datetime,
    strategy: str,
    weights: Mapping[str, float],
    seen: History,
    reason: str,
) -> dict[str, Any]:
    entry = {
        "time": iso(time),
        "strategy": strategy,
        "weights": dict(weights),
        "prices": {s: b[-1].close for s, b in seen.items() if b},
        "data_through": {s: b[-1].date.isoformat() for s, b in seen.items() if b},
        "reason": reason,
    }
    _append(root / DECISIONS, entry)
    return entry


def decisions(root: Path, strategy: str | None = None) -> list[dict[str, Any]]:
    rows = _read(root / DECISIONS)
    return [r for r in rows if strategy is None or r["strategy"] == strategy]


def register_try(root: Path, name: str, note: str, now: datetime) -> bool:
    """Count a strategy as tried. Returns False if it was already counted."""
    if any(r["name"] == name for r in _read(root / TRIES)):
        return False
    _append(root / TRIES, {"name": name, "first_tried": iso(now), "note": note})
    return True


def tries(root: Path) -> int:
    return len(_read(root / TRIES))


def _git(cwd: Path, *args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True).stdout


def check_append_only(path: Path) -> int:
    """Raise LedgerTampered unless `path` only ever grew: in every commit reachable from HEAD its
    content must start with its content in each parent (merges included, so a rewrite can't hide
    on a side branch), and the file on disk must start with HEAD's. Returns how many commits
    changed the file (0 outside git)."""
    cwd = path.resolve().parent
    while not cwd.exists():
        cwd = cwd.parent
    try:
        top = Path(_git(cwd, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0
    rel = path.resolve().relative_to(top).as_posix()
    try:
        head = _git(top, "rev-parse", "--verify", "-q", "HEAD").decode().strip()
    except subprocess.CalledProcessError:
        return 0  # a branch with no commits yet (the first run's fresh paper-trail)
    # Every commit with its parents. Not `git log -- file`: that skips one side of a merge.
    graph = [
        line.split() for line in _git(top, "rev-list", "--parents", "HEAD").decode().split("\n")
    ]
    graph = [g for g in graph if g]
    blob = _blobs(top, [g[0] for g in graph], rel)

    @functools.lru_cache(maxsize=4)  # a child's version is the next commit's parent version
    def read(blob_id: str) -> bytes:
        return _git(top, "cat-file", "blob", blob_id) if blob_id else b""  # "" = file absent

    changed = 0
    for commit, *parents in graph:
        if all(blob[commit] != blob[p] for p in parents) and blob[commit]:
            changed += 1
        for parent in parents:
            if blob[parent] != blob[commit] and not read(blob[commit]).startswith(
                read(blob[parent])
            ):
                raise LedgerTampered(
                    f"{rel}: earlier lines were changed or removed at {commit[:10]}"
                )
    on_disk = path.read_bytes() if path.exists() else b""
    if not on_disk.startswith(read(blob[head])):
        raise LedgerTampered(f"{rel}: earlier lines were changed or removed at working tree")
    return changed


def _blobs(top: Path, commits: list[str], rel: str) -> dict[str, str]:
    """Blob id of `rel` in each commit ("" where the file is absent), in one git call."""
    query = "".join(f"{c}:{rel}\n" for c in commits).encode()
    out = subprocess.run(
        ["git", "cat-file", "--batch-check"], cwd=top, check=True, capture_output=True, input=query
    ).stdout.decode()
    ids = {}
    for commit, line in zip(commits, out.splitlines(), strict=True):
        fields = line.split()
        ids[commit] = fields[0] if len(fields) == 3 and fields[1] == "blob" else ""
    return ids
