"""The forward-test ledger: append-only JSONL, committed before outcomes exist.

- `ledger/decisions.jsonl`: one line per decision (UTC time, strategy, weights, prices seen,
  last bar date seen per asset, reason).
- `ledger/tries.jsonl`: one line per strategy ever tried, live or dead (for the deflated Sharpe).
- `ledger/research_tries.jsonl`: each new high of the research lane's try count (it never shrinks).

Git history is the tamper evidence: `check_append_only` fails if any committed line was changed.
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from grimstrade.data import History

DECISIONS = Path("ledger/decisions.jsonl")
TRIES = Path("ledger/tries.jsonl")
RESEARCH_FLOOR = Path("ledger/research_tries.jsonl")
APPEND_ONLY = (DECISIONS, TRIES, RESEARCH_FLOOR)


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
_RESEARCH_REFS = ("refs/heads/main", "refs/remotes/*/main", "refs/heads/research-*",
                  "refs/remotes/*/research-*")  # fmt: skip


def _research_texts(repo: Path, rel: str) -> list[str]:
    """`rel` from the working tree, `main` and every local or remote `research-*` branch."""
    texts = []
    if (repo / rel).exists():
        texts.append((repo / rel).read_text())
    try:
        refs = _git(repo, "for-each-ref", "--format=%(refname)", *_RESEARCH_REFS).decode().split()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return texts
    for ref in refs:
        try:
            texts.append(_git(repo, "show", f"{ref}:{rel}").decode())
        except subprocess.CalledProcessError:
            continue  # branch without the file
    return texts


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _is_separator(cells: list[str]) -> bool:
    return all(c and set(c) <= set("-: ") for c in cells)


def _table_rows(text: str) -> list[dict[str, str]]:
    """Data rows of every markdown table, keyed by lower-cased header. A header is the row just
    above a `|---|` separator; it stays in force across blank lines until the next header."""
    lines = [line.strip() for line in text.splitlines()]
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for i, s in enumerate(lines):
        if not s.startswith("|"):
            continue
        cells = _cells(s)
        if _is_separator(cells):
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if nxt.startswith("|") and _is_separator(_cells(nxt)):
            header = [c.lower() for c in cells]
        elif header is not None:
            rows.append(dict(zip(header, cells, strict=False)))
    return rows


def _variant_rows(repo: Path) -> list[dict[str, str]]:
    return [r for t in _research_texts(repo, RESEARCH_TRIES) for r in _table_rows(t)]


def research_tries(repo: Path) -> int:
    """How many strategy variants the research lane has tried (rule in docs/DECISIONS.md).

    Distinct (idea, variant) rows of `research/tries.md` (any kind: baselines and robustness runs
    count too), plus the ideas in `research/ideas.md` past status `new` that have no such row. Both
    files are read from the working tree, `main` and every `research-*` branch, and unioned.
    """
    variants = {
        (r.get("idea", "").lower(), r.get("variant", "").lower()) for r in _variant_rows(repo)
    }
    logged = {idea for idea, _ in variants}
    tried: set[str] = set()
    for text in _research_texts(repo, RESEARCH_IDEAS):
        for r in _table_rows(text):
            status = r.get("status", "").strip().lower()
            idea = r.get("idea", "").strip().lower()
            if idea and status and not status.startswith("new"):
                tried.add(idea)
    return len(variants) + len(tried - logged)


def research_sharpes(repo: Path) -> list[float]:
    """Annualised Sharpe of each research variant (`kind` variant, `train` period, as logged)."""
    out: dict[tuple[str, str], float] = {}
    for r in _variant_rows(repo):
        if r.get("kind", "variant").lower() != "variant":
            continue
        if r.get("period", "train").lower() != "train":
            continue
        try:
            sharpe = float(r.get("sharpe", ""))
        except ValueError:
            continue
        out[(r.get("idea", "").lower(), r.get("variant", "").lower())] = sharpe
    return list(out.values())


def research_floor(root: Path, count: int) -> int:
    """Never let the research count shrink (a deleted or unfetched branch would hide tries):
    record `count` in `ledger/research_tries.jsonl` if it is a new high, return the high."""
    high = max((int(r["count"]) for r in _read(root / RESEARCH_FLOOR)), default=0)
    if count > high:
        _append(root / RESEARCH_FLOOR, {"count": count})
    return max(count, high)


def total_tries(root: Path, repo: Path, also: Iterable[str] = ()) -> int:
    """Every strategy tried anywhere: the ledger's tries (plus any names in `also` not yet
    registered, e.g. live strategies before their first run) and the research lane's (never less
    than its recorded high)."""
    names = {r["name"] for r in _read(root / TRIES)} | set(also)
    return len(names) + research_floor(root, research_tries(repo))


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
