"""The forward-test ledger: append-only JSONL, committed before outcomes exist.

- `ledger/decisions.jsonl`: one line per decision (UTC time, strategy, weights, prices seen,
  last bar date seen per asset, reason).
- `ledger/tries.jsonl`: one line per strategy ever tried, live or dead (for the deflated Sharpe).

Git history is the tamper evidence: `check_append_only` fails if any committed line was changed.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Iterable, Mapping
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


# --- the research lane's tries (research/ on main and on research-* branches) ---

RESEARCH_TRIES = "research/tries.md"
RESEARCH_IDEAS = "research/ideas.md"
_TRIED = re.compile(r"\b(testing|tested|live|dead)\b", re.IGNORECASE)


def _research_texts(repo: Path, rel: str) -> list[str]:
    """`rel` from the working tree and from every local or remote `research-*` branch."""
    texts = []
    if (repo / rel).exists():
        texts.append((repo / rel).read_text())
    try:
        refs = _git(
            repo, "for-each-ref", "--format=%(refname)", "refs/heads/research-*",
            "refs/remotes/*/research-*",
        ).decode().split()  # fmt: skip
    except (subprocess.CalledProcessError, FileNotFoundError):
        return texts
    for ref in refs:
        try:
            texts.append(_git(repo, "show", f"{ref}:{rel}").decode())
        except subprocess.CalledProcessError:
            continue  # branch without the file
    return texts


def _table_rows(text: str) -> list[list[str]]:
    """Data rows of every markdown table (header and separator rows dropped), plus bullets."""
    rows: list[list[str]] = []
    in_table = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not in_table:
                in_table = True  # the header row
            elif not all(set(c) <= set("-: ") for c in cells):
                rows.append(cells)
            continue
        in_table = False
        if s.startswith(("- ", "* ")):
            rows.append([s[2:].strip()])
    return rows


def research_tries(repo: Path) -> int:
    """How many strategy variants the research lane has tried (rule in docs/DECISIONS.md).

    Distinct (idea, variant) rows of `research/tries.md`, the union over the working tree and all
    `research-*` branches; at least the number of ideas in `research/ideas.md` whose status shows
    they were tested (testing, live or dead).
    """
    variants: set[tuple[str, ...]] = set()
    for text in _research_texts(repo, RESEARCH_TRIES):
        for cells in _table_rows(text):
            key = cells[1:3] if len(cells) >= 4 else cells  # date | idea | variant | period
            variants.add(tuple(c.lower() for c in key))
    ideas: set[str] = set()
    for text in _research_texts(repo, RESEARCH_IDEAS):
        for cells in _table_rows(text):
            if _TRIED.search(" ".join(cells)):
                ideas.add(cells[0].lower())
    return max(len(variants), len(ideas))


def total_tries(root: Path, repo: Path, also: Iterable[str] = ()) -> int:
    """Every strategy tried anywhere: the ledger's tries (plus any names in `also` not yet
    registered, e.g. live strategies before their first run) and the research lane's."""
    names = {r["name"] for r in _read(root / TRIES)} | set(also)
    return len(names) + research_tries(repo)


def _git(cwd: Path, *args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True).stdout


def check_append_only(path: Path) -> int:
    """Raise LedgerTampered if any committed version of `path` is not a prefix of the next one,
    or of the file on disk. Returns how many committed versions were checked (0 outside git)."""
    cwd = path.resolve().parent
    while not cwd.exists():
        cwd = cwd.parent
    try:
        top = Path(_git(cwd, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0
    rel = path.resolve().relative_to(top).as_posix()
    try:
        _git(top, "rev-parse", "--verify", "-q", "HEAD")
    except subprocess.CalledProcessError:
        return 0  # a branch with no commits yet (the first run's fresh paper-trail)
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
