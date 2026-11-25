"""The forward-test ledger: append-only JSONL, committed before outcomes exist.

- `ledger/decisions.jsonl`: one line per decision (UTC time, strategy, weights, prices seen,
  last bar date seen per asset, reason, commit of the code that decided).
- `ledger/tries.jsonl`: one line per strategy ever tried, live or dead (for the deflated Sharpe).
- `ledger/problems.jsonl`: one line per run that reported problems, with what they were.
- `ledger/research_tries.jsonl`: every research-lane try ever seen (idea, variant, Sharpe), so none
  can disappear from the count.

Git history is the tamper evidence: `check_append_only` fails if any committed line was changed.
"""

from __future__ import annotations

import bisect
import contextlib
import functools
import json
import math
import os
import subprocess
from collections.abc import Iterable, Mapping
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from grimstrade.data import History, ends_mid_line

DECISIONS = Path("ledger/decisions.jsonl")
TRIES = Path("ledger/tries.jsonl")
RESEARCH_FLOOR = Path("ledger/research_tries.jsonl")
PROBLEMS = Path("ledger/problems.jsonl")
# Rewrites of the record branch that a person accepted (scripts/check-trail-activity.sh), and
# what the last run could check of the branch's history (not append-only: one line, rewritten).
ACCEPTED_REWRITES = Path("ledger/acknowledged-rewrites.txt")
WITNESS = Path("state/witness.txt")
APPEND_ONLY = (DECISIONS, TRIES, RESEARCH_FLOOR, PROBLEMS, ACCEPTED_REWRITES)


class LedgerTampered(Exception):
    pass


def _append(path: Path, entry: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # A file that lost its final newline (a write cut short, a hand edit) would glue the new line
    # onto the last one, and that can't be repaired later without "rewriting" the record.
    start = "\n" if ends_mid_line(path) else ""
    with path.open("a") as f:
        f.write(start + json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")


def _read(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def iso(t: datetime) -> str:
    if t.tzinfo is None:  # astimezone() would silently read it as this machine's local time
        raise ValueError("a time written to the record must carry its time zone")
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
    code_hash: str | None = None,
) -> dict[str, Any]:
    entry = {
        "time": iso(time),
        "strategy": strategy,
        "weights": dict(weights),
        "prices": {s: b[-1].close for s, b in seen.items() if b},
        "data_through": {s: b[-1].date.isoformat() for s, b in seen.items() if b},
        "reason": reason,
    }
    # Which code decided: the commit the daily job runs (GitHub sets GITHUB_SHA). A strategy can
    # change under the same name; this is what lets a reader see where its record really starts.
    code = os.environ.get("GITHUB_SHA")
    if code:
        entry["code"] = code
    # ...and a fingerprint of the strategy's own code (`run_daily.fingerprint`): the commit changes
    # with every merge, this only when the strategy does. The scoreboard flags such a change.
    if code_hash:
        entry["code_hash"] = code_hash
    _append(root / DECISIONS, entry)
    return entry


def decisions(root: Path, strategy: str | None = None) -> list[dict[str, Any]]:
    rows = _read(root / DECISIONS)
    return [r for r in rows if strategy is None or r["strategy"] == strategy]


def register_try(
    root: Path,
    name: str,
    note: str,
    now: datetime,
    *,
    weeks: int | None = None,
    skew: float | None = None,
    excess_kurtosis: float | None = None,
) -> bool:
    """Count a strategy as tried. Returns False if it was already counted.

    Optional, for the deflated Sharpe (record length T and the shape of the returns): `weeks`,
    the length of the record the try was judged on, in weeks, and the `skew` and
    `excess_kurtosis` (0 for normal returns) of its weekly returns. Written only when given, so
    older lines and callers stay valid; a line never gains them later (append-only)."""
    if any(r["name"] == name for r in _read(root / TRIES)):
        return False
    entry: dict[str, Any] = {"name": name, "first_tried": iso(now), "note": note}
    if weeks is not None:
        if isinstance(weeks, bool) or not isinstance(weeks, int) or weeks < 1:
            raise ValueError(f"weeks must be a positive whole number, not {weeks!r}")
        entry["weeks"] = weeks
    for key, value in (("skew", skew), ("excess_kurtosis", excess_kurtosis)):
        if value is not None:
            if not math.isfinite(value):
                raise ValueError(f"{key} must be finite, not {value!r}")
            entry[key] = float(value)
    _append(root / TRIES, entry)
    return True


def try_moments(root: Path) -> dict[str, dict[str, float]]:
    """The optional record length and shape fields of each counted strategy that has any."""
    keys = ("weeks", "skew", "excess_kurtosis")
    out = {}
    for r in _read(root / TRIES):
        got = {k: r[k] for k in keys if k in r}
        if got:
            out[r["name"]] = got
    return out


def record_problems(root: Path, now: datetime, problems: Iterable[str]) -> None:
    """Keep a run's problems (a source that failed, a strategy that raised, stale or revised
    data) in the record itself. Otherwise they exist only in that run's log, and later "held its
    position", "crashed" and "had no data" all look the same."""
    found = list(problems)
    if found:
        _append(root / PROBLEMS, {"time": iso(now), "problems": found})


def problem_runs(root: Path) -> list[dict[str, Any]]:
    return _read(root / PROBLEMS)


def tries(root: Path) -> int:
    return len(_read(root / TRIES))


# --- the research lane's tries (research/ on every branch, and the committed register) ---

RESEARCH_TRIES = "research/tries.md"
RESEARCH_IDEAS = "research/ideas.md"
# Every try ever seen on any branch, one JSON line each (`grimstrade.register` writes it).
RESEARCH_REGISTER = "research/register/tries.jsonl"
# Every local and remote branch. Research lanes are named freely (`carry-2`, `eu-4`, ...): a list
# of name patterns stopped counting the moment lanes stopped using it (dsr-1, 2026-11-18).
_RESEARCH_REFS = ("refs/heads", "refs/remotes")
RECORD_BRANCH = "paper-trail"  # the record itself, never a research branch


def research_refs(repo: Path, prefixes: Iterable[str] = _RESEARCH_REFS) -> list[str]:
    """Every local and remote branch of `repo` (or those under `prefixes`) except the record
    branch and symbolic refs (`origin/HEAD`). [] outside git."""
    try:
        out = _git(repo, "for-each-ref", "--format=%(refname) %(symref)", *prefixes)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    refs = []
    for line in out.decode().splitlines():
        ref, _, symref = line.partition(" ")
        if ref and not symref and ref.rsplit("/", 1)[-1] != RECORD_BRANCH:
            refs.append(ref)
    return refs


def _research_texts(repo: Path, rel: str) -> list[str]:
    """`rel` from the working tree and every branch (`research_refs`), each distinct text once."""
    texts = []
    if (repo / rel).exists():
        texts.append((repo / rel).read_text(errors="replace"))
    refs = research_refs(repo)
    try:
        # Branches share files through their history: read each distinct version once.
        blobs = {b for b, _ in _blobs(repo, refs, rel).values() if b} if refs else set()
        # Any branch is read, so a stray non-UTF-8 byte must not stop the daily run.
        texts += [_git(repo, "cat-file", "blob", b).decode(errors="replace") for b in sorted(blobs)]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return list(dict.fromkeys(texts))


def _register_rows(repo: Path) -> list[dict[str, str]]:
    """The committed register's tries, in the shape of a `research/tries.md` table row. A line
    that is not a JSON object with an idea is skipped: the tables are still read, and a bad line
    must not stop the daily run."""
    rows = []
    for text in _research_texts(repo, RESEARCH_REGISTER):
        for line in text.splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if not isinstance(r, dict) or not isinstance(r.get("idea"), str):
                continue
            sharpe = r.get("sharpe")
            rows.append(
                {
                    "idea": r["idea"],
                    "variant": str(r.get("variant") or ""),
                    "kind": str(r.get("kind") or "variant"),
                    "period": str(r.get("period") or "train"),
                    "sharpe": "" if sharpe is None else str(sharpe),
                }
            )
    return rows


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
    tables = [r for t in _research_texts(repo, RESEARCH_TRIES) for r in _table_rows(t)]
    return tables + _register_rows(repo)


Key = tuple[str, str | None]  # (idea, variant); variant None = an idea tried without a logged row


def _visible_research(repo: Path) -> dict[Key, float | None]:
    """The research tries visible now, each with its train Sharpe if logged.

    Distinct (idea, variant) rows of `research/tries.md` and of the register
    `research/register/tries.jsonl` (any kind: baselines and robustness runs count too), plus the
    ideas in `research/ideas.md` past status `new` (as (idea, None)). All are read from the
    working tree and every local and remote branch except the record's, and unioned.
    """
    out: dict[Key, float | None] = {}
    for r in _variant_rows(repo):
        key: Key = (r.get("idea", "").strip().lower(), r.get("variant", "").strip().lower())
        sharpe = None
        kind, period = r.get("kind", "variant").lower(), r.get("period", "train").lower()
        if kind == "variant" and period == "train":
            with contextlib.suppress(ValueError):
                sharpe = float(r.get("sharpe", ""))
            if sharpe is not None and not math.isfinite(sharpe):
                sharpe = None  # never write NaN/inf into the append-only record
        if out.get(key) is None:
            out[key] = sharpe
    for text in _research_texts(repo, RESEARCH_IDEAS):
        for r in _table_rows(text):
            status = r.get("status", "").strip().lower()
            idea = r.get("idea", "").strip().lower()
            if idea and status and not status.startswith("new"):
                out.setdefault((idea, None), None)
    return out


def _recorded_research(root: Path) -> dict[Key, float | None]:
    out: dict[Key, float | None] = {}
    for r in _read(root / RESEARCH_FLOOR):
        key: Key = (r["idea"], r["variant"])
        sharpe = r.get("sharpe")
        # json reads NaN and Infinity; one such line would switch off the spread of the tries'
        # Sharpes in the deflated Sharpe (max(x, nan) is x).
        if not isinstance(sharpe, int | float) or not math.isfinite(sharpe):
            sharpe = None
        if out.get(key) is None:
            out[key] = sharpe
    return out


def _research(repo: Path, root: Path | None) -> dict[Key, float | None]:
    seen = _recorded_research(root) if root is not None else {}
    for key, sharpe in _visible_research(repo).items():
        if seen.get(key) is None:
            seen[key] = sharpe
    return seen


def record_research(root: Path, repo: Path, now: datetime) -> int:
    """Append every research try (and newly logged Sharpe) not yet in
    `ledger/research_tries.jsonl`, so a deleted or unfetched branch can never hide a try. Returns
    how many lines were appended. The daily runner calls this; reports only read."""
    recorded = _recorded_research(root)
    added = 0
    for key, sharpe in sorted(_visible_research(repo).items(), key=str):
        if key in recorded and (sharpe is None or recorded[key] is not None):
            continue
        entry = {"idea": key[0], "variant": key[1], "sharpe": sharpe, "seen": iso(now)}
        _append(root / RESEARCH_FLOOR, entry)
        added += 1
    return added


def research_tries(repo: Path, root: Path | None = None) -> int:
    """How many strategy variants the research lane has tried (rule in docs/DECISIONS.md): every
    (idea, variant) visible now or recorded under `root`, plus tried ideas with no variant row."""
    keys = _research(repo, root)
    logged = {idea for idea, variant in keys if variant is not None}
    return sum(1 for idea, variant in keys if variant is not None or idea not in logged)


def research_sharpes(repo: Path, root: Path | None = None) -> list[float]:
    """Annualised train Sharpe of each research variant (Kind `variant`), visible or recorded."""
    return [s for s in _research(repo, root).values() if s is not None]


def total_tries(root: Path, repo: Path, also: Iterable[str] = ()) -> int:
    """Every strategy tried anywhere: the ledger's tries (plus any names in `also` not yet
    registered, e.g. live strategies before their first run) and the research lane's, visible or
    recorded. Read-only."""
    names = {r["name"] for r in _read(root / TRIES)} | set(also)
    # A name that only exists in the decisions (written by hand) gets a row: it is a try too.
    names |= {r["strategy"] for r in _read(root / DECISIONS)}
    return len(names) + research_tries(repo, root)


# --no-replace-objects: a replace ref in the checking clone must not show git another history.
_GIT = ("git", "--no-replace-objects")


def _git(cwd: Path, *args: str) -> bytes:
    return subprocess.run([*_GIT, *args], cwd=cwd, check=True, capture_output=True).stdout


# Clocks of two honest machines can differ a little (seconds).
SKEW = 300


def check_history(root: Path, now: datetime) -> None:
    """Raise LedgerTampered unless the record's history can be believed as a whole: it is one
    line of commits, no commit is dated before the one under it and none after `now`. (That all
    of it is there, not a shallow clone, is checked wherever git is asked: `_locate`.)

    The file checks below cannot see these. The daily job never merges, and a merge can carry a
    back-dated commit in beside the record: its file is a pure append to both parents, yet every
    line in it would count from the forged date. Commit dates are written by whoever commits;
    a date that runs backwards or lies in the future is a lie that shows from inside.

    Only for a folder that is the top of its own checkout (the paper-trail worktree)."""
    where = _locate(root / DECISIONS)
    if where is None or where[0] != root.resolve():
        return
    top = where[0]
    log = _git(top, "rev-list", "--parents", "--timestamp", "HEAD").decode().splitlines()
    rows = [r.split() for r in log if r]  # timestamp, commit, parents...
    made = {commit: int(stamp) for stamp, commit, *_ in rows}
    for stamp, commit, *parents in rows:
        if len(parents) > 1:
            raise LedgerTampered(f"history: {commit[:10]} is a merge; the record never merges")
        if int(stamp) > now.timestamp() + SKEW:
            raise LedgerTampered(f"history: {commit[:10]} is dated in the future")
        if any(int(stamp) < made[p] - SKEW for p in parents if p in made):
            raise LedgerTampered(f"history: {commit[:10]} is dated before the commit under it")


def refuse_links(root: Path, rel: Path) -> None:
    """Raise LedgerTampered if a record file, or a folder on the way to it, is a symbolic link.
    Every check would follow the link and vouch for the history of whatever it points at: one
    ordinary commit could swap a whole file for another that "only ever grew"."""
    for part in (rel, *rel.parents):
        if part != Path() and (root / part).is_symlink():
            raise LedgerTampered(f"{part.as_posix()}: is a symbolic link")


def check_lines(root: Path, rel: Path) -> None:
    """Raise LedgerTampered at a line of the JSON-lines record file `rel` that is not one whole
    JSON object: what a write cut short (a killed job, a full disk) leaves behind. Such a line
    stays for good, as the file is append-only, and every reader would crash on it part way
    through a run, after the bars were stored and before anything was decided."""
    path = root / rel
    if not path.exists():
        return
    try:
        lines = path.read_text().splitlines()  # as `_read` and the other readers split them
    except ValueError as e:  # not UTF-8
        raise LedgerTampered(f"{rel.as_posix()}: unreadable ({e})") from e
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            whole = isinstance(json.loads(line), dict)
        except ValueError:
            whole = False
        if not whole:
            raise LedgerTampered(
                f"{rel.as_posix()} line {n}: not one whole JSON object (a write cut short?)"
            )


def check_append_only(path: Path) -> int:
    """Raise LedgerTampered unless `path` only ever grew: in every commit reachable from HEAD its
    content must start with its content in each parent (merges included, so a rewrite can't hide
    on a side branch), and the file on disk must start with HEAD's. Returns how many commits
    changed the file (0 outside git)."""
    where = _locate(path)
    if where is None:
        return 0
    top, rel, head = where
    # Every commit with its parents. Not `git log -- file`: that skips one side of a merge.
    graph = [
        line.split() for line in _git(top, "rev-list", "--parents", "HEAD").decode().split("\n")
    ]
    graph = [g for g in graph if g]
    blob = {c: b for c, (b, _) in _blobs(top, [g[0] for g in graph], rel).items()}

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


def _locate(path: Path) -> tuple[Path, str, str] | None:
    """(repo top, `path` relative to it, HEAD commit); None outside git or on a branch with no
    commits yet (the first run's fresh paper-trail)."""
    # Inside the checkout nothing on the way to the file may be a symbolic link (see
    # `refuse_links`); the checkout is the nearest folder above the file with a `.git` in it.
    lexical = Path(os.path.abspath(path))
    inside = next((p for p in lexical.parents if (p / ".git").exists()), None)
    if inside is not None:
        refuse_links(inside, lexical.relative_to(inside))
    cwd = path.resolve().parent
    while not cwd.exists():
        cwd = cwd.parent
    try:
        top = Path(_git(cwd, "rev-parse", "--show-toplevel").decode().strip()).resolve()
        head = _git(top, "rev-parse", "--verify", "-q", "HEAD").decode().strip()
        shallow = _git(top, "rev-parse", "--is-shallow-repository").strip() == b"true"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    if shallow:  # git would vouch only for the commits it has, and date old lines to the oldest
        raise LedgerTampered("a shallow clone: the record's whole history is needed to check it")
    return top, path.resolve().relative_to(top).as_posix(), head


def _blobs(top: Path, commits: list[str], rel: str) -> dict[str, tuple[str, int]]:
    """(blob id, size in bytes) of `rel` in each commit, ("", 0) where the file is absent, in one
    git call."""
    query = "".join(f"{c}:{rel}\n" for c in commits).encode()
    out = subprocess.run(
        [*_GIT, "cat-file", "--batch-check"], cwd=top, check=True, capture_output=True, input=query
    ).stdout.decode()
    found = {}
    for commit, line in zip(commits, out.splitlines(), strict=True):
        fields = line.split()
        is_file = len(fields) == 3 and fields[1] == "blob"
        found[commit] = (fields[0], int(fields[2])) if is_file else ("", 0)
    return found


# --- when a decision counts from ---

# A decision that reaches the record later than this after its own timestamp is called late.
LATE = timedelta(minutes=30)


def _lines_recorded(path: Path, first_parent: bool = False) -> list[tuple[bytes, datetime | None]]:
    """Each non-blank line of `path` on disk with the time of the earliest commit that holds it
    (its committer time, or its parents' if that is later); None if it is not committed yet (or
    outside git). `first_parent`: walk HEAD's first-parent chain only, so a line merged in from a
    side branch counts from the merge, not from the (author-chosen) side commit; for files that
    live on a branch with merges (the decisions ledger has none: `check_history`). Relies on the
    file being
    append-only (`check_append_only`): a commit's new lines are the bytes past its parents'.

    Everything is counted in bytes and split at "\n" only, exactly as git stores the file. (Text
    mode reads "\r\n" as one character: padding with such lines then moved a line's position
    back into an older commit.)"""
    data = path.read_bytes() if path.exists() else b""
    lines, ends, pos = [], [], 0
    for chunk in data.split(b"\n"):
        if chunk.strip():
            lines.append(chunk)
            # Its last byte, not its newline: a line whose newline went missing is completed by
            # the next run's, and must not be re-dated to that run.
            ends.append(pos + len(chunk))
        pos += len(chunk) + 1
    times: list[datetime | None] = [None] * len(ends)
    where = _locate(path)
    if where is None:
        return list(zip(lines, times, strict=True))
    top, rel, _ = where
    walk = ["--first-parent"] if first_parent else []
    log = _git(top, "rev-list", *walk, "--topo-order", "--parents", "--timestamp", "HEAD")
    rows = [r.split() for r in log.decode().splitlines() if r]  # timestamp, commit, parents...
    if first_parent:  # only the chain's own parent: a merged side branch is not on the path
        rows = [r[:3] for r in rows]
    size = {c: n for c, (_, n) in _blobs(top, [r[1] for r in rows], rel).items()}
    # A commit's date is written by whoever commits, but a commit cannot be older than its
    # parents: it counts from the latest time on its path. A back-dated commit on top of the
    # record then gains nothing before the commit under it.
    made: dict[str, int] = {}
    for stamp, commit, *parents in reversed(rows):  # topo order lists children first
        made[commit] = max([int(stamp), *(made.get(p, 0) for p in parents)])
    # Bytes (lo, hi] of the file first appear in this commit.
    spans = []
    for _, commit, *parents in rows:
        lo = max((size[p] for p in parents), default=0)
        if size[commit] > lo:
            spans.append((made[commit], lo, size[commit]))
    for seconds, lo, hi in sorted(spans):  # earliest commit first: it wins
        for i in range(bisect.bisect_right(ends, lo), bisect.bisect_right(ends, hi)):
            if times[i] is None:  # (a date past year 9999 must not crash every reader)
                times[i] = datetime.fromtimestamp(min(seconds, 253402300799), tz=UTC)
    return list(zip(lines, times, strict=True))


def recorded_at(path: Path, first_parent: bool = False) -> list[datetime | None]:
    """When each non-blank line of `path` was first committed (None: not yet); `first_parent`
    as in `_lines_recorded`."""
    return [at for _, at in _lines_recorded(path, first_parent)]


def in_force(root: Path) -> tuple[list[tuple[datetime, dict[str, Any]]], int]:
    """Every decision that counts, with the time it counts from, and how many were late.

    The ledger's promise is "written before the outcome exists", and only the commit shows when
    a line was written. So a committed decision counts from its commit time if that is later than
    its own timestamp (in a normal run: seconds). A line appended afterwards with an old
    timestamp gains nothing: it takes effect when it reached the record. Lines not committed yet
    (today's run, before its commit) keep their timestamp. A decision is left out if a later
    line of the same strategy counts from the same moment or earlier: it was never provably in
    force. `late` = lines recorded more than LATE after their own timestamp."""
    refuse_links(root, DECISIONS)
    kept: dict[str, list[tuple[datetime, dict[str, Any]]]] = {}
    late = 0
    # Rows are parsed from the very bytes whose position gave `at`: no second way of splitting
    # the file into lines that could disagree with it.
    for raw, at in _lines_recorded(root / DECISIONS):
        row: dict[str, Any] = json.loads(raw)
        stamped = parse_time(row["time"])
        counts_from = max(stamped, at) if at is not None else stamped
        late += counts_from - stamped > LATE
        mine = kept.setdefault(row["strategy"], [])
        while mine and mine[-1][0] >= counts_from:
            mine.pop()
        mine.append((counts_from, row))
    return sorted((d for ds in kept.values() for d in ds), key=lambda d: d[0]), late
