"""The forward-test ledger: append-only JSONL, committed before outcomes exist.

- `ledger/decisions.jsonl`: one line per decision (UTC time, strategy, weights, prices seen,
  last bar date seen per asset, reason).
- `ledger/tries.jsonl`: one line per strategy ever tried, live or dead (for the deflated Sharpe).

Git history is the tamper evidence: `check_append_only` fails if any committed line was changed.
"""

from __future__ import annotations

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
    """Raise LedgerTampered if any committed version of `path` is not a prefix of the next one,
    or of the file on disk. Returns how many committed versions were checked (0 outside git)."""
    cwd = path.parent if path.parent.exists() else Path(".")
    try:
        top = Path(_git(cwd, "rev-parse", "--show-toplevel").decode().strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0
    rel = path.resolve().relative_to(top.resolve()).as_posix()
    commits = _git(top, "log", "--format=%H", "--reverse", "--", rel).decode().split()
    versions = []
    for c in commits:
        try:
            versions.append((c[:10], _git(top, "show", f"{c}:{rel}")))
        except subprocess.CalledProcessError:
            versions.append((c[:10], b""))  # deleted in this commit
    if path.exists():
        versions.append(("working tree", path.read_bytes()))
    for (_, old), (where, new) in zip(versions, versions[1:], strict=False):
        if not new.startswith(old):
            raise LedgerTampered(f"{rel}: earlier lines were changed or removed at {where}")
    return len(commits)
