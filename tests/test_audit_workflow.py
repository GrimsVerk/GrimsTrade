"""Honesty audit 2026-11: the daily workflow and its two guard scripts.

The workflow itself can't run in tests; its risky steps live in scripts that can:
`scripts/checkout-trail.sh` (audit L5) and `scripts/check-trail-activity.sh` (audit L1, L3).
The scripts run here against throwaway git repos and a fake `gh`, offline.
"""

import os
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DAILY = ROOT / ".github" / "workflows" / "daily.yml"
CHECKOUT = ROOT / "scripts" / "checkout-trail.sh"
ACTIVITY = ROOT / "scripts" / "check-trail-activity.sh"
T0 = datetime(2026, 11, 11, 22, 0, 51, tzinfo=UTC)
ZERO = "0" * 40


def git(repo: Path, *args: str, when: datetime | None = None) -> str:
    env = dict(os.environ)
    if when is not None:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = when.strftime("%Y-%m-%dT%H:%M:%SZ")
    out = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )
    return out.stdout.decode().strip()


def commit(repo: Path, text: str, when: datetime) -> str:
    with (repo / "ledger.jsonl").open("a") as f:
        f.write(text + "\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", text, when=when)
    return git(repo, "rev-parse", "HEAD")


def test_the_workflow_uses_the_guards_and_only_runs_code_from_main() -> None:
    text = DAILY.read_text()
    # Audit L8: a manual start can pick any branch; unmerged code must not write the record.
    assert "if: github.ref == 'refs/heads/main'" in text
    assert "scripts/checkout-trail.sh" in text and "git worktree add --orphan" not in text
    assert text.index("scripts/check-trail-activity.sh trail") < text.index("grimstrade.run_daily")


# --- scripts/checkout-trail.sh (audit L5) ---


@pytest.fixture
def clone(tmp_path: Path) -> Path:
    """A code checkout whose origin has `main` and `paper-trail`, like the job's workspace."""
    origin = tmp_path / "origin"
    origin.mkdir()
    git(origin, "init", "-q", "-b", "main")
    commit(origin, "code", T0)
    git(origin, "checkout", "-q", "--orphan", "paper-trail")
    commit(origin, "day 1", T0)
    git(origin, "checkout", "-q", "main")
    git(tmp_path, "clone", "-q", str(origin), "work")
    return tmp_path / "work"


def checkout(work: Path, **env: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["bash", str(CHECKOUT)], cwd=work, capture_output=True, env={**os.environ, **env}
    )


def test_checkout_puts_the_existing_record_in_trail(clone: Path) -> None:
    assert checkout(clone).returncode == 0
    assert (clone / "trail" / "ledger.jsonl").read_text() == "code\nday 1\n"
    assert git(clone / "trail", "branch", "--show-current") == "paper-trail"


def test_a_missing_branch_stops_the_job_unless_a_new_record_is_asked_for(clone: Path) -> None:
    git(clone.parent / "origin", "branch", "-q", "-D", "paper-trail")  # the record was deleted
    refused = checkout(clone)
    assert refused.returncode == 1 and b"origin has no paper-trail branch" in refused.stderr
    assert not (clone / "trail").exists()
    # The very first run: the owner starts it by hand and asks for a new record.
    assert checkout(clone, START_NEW_RECORD="true").returncode == 0
    assert list((clone / "trail").iterdir()) == [clone / "trail" / ".git"]


def test_an_unreachable_remote_never_starts_a_new_record(clone: Path) -> None:
    git(clone, "remote", "set-url", "origin", str(clone.parent / "gone"))
    for env in ({}, {"START_NEW_RECORD": "true"}):
        failed = checkout(clone, **env)
        assert failed.returncode == 1 and b"could not reach origin" in failed.stderr
        assert not (clone / "trail").exists()


# --- scripts/check-trail-activity.sh (audit L1, L3) ---


def iso(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def activity(
    tmp_path: Path, trail: Path, events: list[tuple[datetime, str, str, str]] | None, **env: str
) -> subprocess.CompletedProcess[bytes]:
    """Run the script with a fake `gh` that prints `events` (time, type, before, after) the way
    the real call's --jq does, newest first; `None` makes gh fail."""
    fake = tmp_path / "bin"
    fake.mkdir(exist_ok=True)
    if events is None:
        body = "#!/bin/sh\nexit 1\n"
    else:
        rows = [
            f"{iso(t)}\t{kind}\tsomeone\t{before}\t{after}" for t, kind, before, after in events
        ]
        (tmp_path / "events.tsv").write_text("".join(r + "\n" for r in reversed(rows)))
        body = f'#!/bin/sh\ncat "{tmp_path / "events.tsv"}"\n'
    (fake / "gh").write_text(body)
    (fake / "gh").chmod(0o755)
    full = {**os.environ, "PATH": f"{fake}:{os.environ['PATH']}", "GITHUB_REPOSITORY": "o/r", **env}
    return subprocess.run(["bash", str(ACTIVITY), str(trail)], capture_output=True, env=full)


@pytest.fixture
def trail(tmp_path: Path) -> Path:
    repo = tmp_path / "trail"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "paper-trail")
    return repo


def test_an_honest_history_agrees_with_githubs_log(tmp_path: Path, trail: Path) -> None:
    a = commit(trail, "day 1", T0)
    b = commit(trail, "day 2", T0 + timedelta(days=1))
    events = [
        (T0 + timedelta(seconds=1), "branch_creation", ZERO, a),
        (T0 + timedelta(days=1, seconds=1), "push", a, b),
    ]
    done = activity(tmp_path, trail, events)
    assert done.returncode == 0 and b"agrees" in done.stdout


def test_a_force_push_or_a_recreated_branch_stops_the_job(tmp_path: Path, trail: Path) -> None:
    a = commit(trail, "day 1", T0)
    created = (T0 + timedelta(seconds=1), "branch_creation", ZERO, a)
    forced = activity(tmp_path, trail, [created, (T0 + timedelta(hours=3), "force_push", a, a)])
    assert forced.returncode == 2 and b"force_push by someone" in forced.stdout
    again = [created, (T0 + timedelta(hours=3), "branch_deletion", a, ZERO), created]
    recreated = activity(tmp_path, trail, again)
    assert recreated.returncode == 2 and b"created 2 times" in recreated.stdout
    # Once a person has looked and set TRAIL_REVIEWED_UNTIL past the event, the job runs again,
    # but the event is not forgotten: it goes into the trail and onto the scoreboard, every run.
    reviewed = iso(T0 + timedelta(hours=4))
    events = [created, (T0 + timedelta(hours=3), "force_push", a, a)]
    accepted = activity(tmp_path, trail, events, TRAIL_REVIEWED_UNTIL=reviewed)
    assert accepted.returncode == 0 and b"::warning::" in accepted.stdout
    note = trail / "state" / "acknowledged-rewrites.txt"
    assert note.read_text() == "force_push by someone at 2026-11-12T01:00:51Z\n"
    from grimstrade import report

    board = report.render(trail, {}, tmp_path)
    assert "**The record branch itself was rewritten or back-dated (1 event)" in board
    assert "force_push by someone at 2026-11-12T01:00:51Z" in board
    # A later, new force-push stops the job again; the variable is not a blanket off-switch...
    events.append((T0 + timedelta(days=2), "force_push", a, a))
    assert activity(tmp_path, trail, events, TRAIL_REVIEWED_UNTIL=reviewed).returncode == 2
    # ...and it cannot be set to the future to wave everything through.
    future = activity(tmp_path, trail, events, TRAIL_REVIEWED_UNTIL="2099-01-01T00:00:00Z")
    assert future.returncode == 2 and b"is in the future" in future.stdout
    # With nothing accepted the note disappears.
    assert activity(tmp_path, trail, [created]).returncode == 0 and not note.exists()


def test_a_backdated_commit_stops_the_job(tmp_path: Path, trail: Path) -> None:
    a = commit(trail, "day 1", T0)
    # Pushed on day 4, but the commit claims it was made on day 2: decisions in it would count
    # from a time before anyone outside could have seen them.
    b = commit(trail, "day 2, written on day 4", T0 + timedelta(days=1))
    events = [
        (T0 + timedelta(seconds=1), "branch_creation", ZERO, a),
        (T0 + timedelta(days=3), "push", a, b),
    ]
    done = activity(tmp_path, trail, events)
    assert done.returncode == 2
    assert b"says it was made at 2026-11-12T22:00:51Z but reached GitHub at 2026-11-14" in (
        done.stdout
    )


def test_when_github_cannot_be_asked_the_job_goes_on_with_a_warning(
    tmp_path: Path, trail: Path
) -> None:
    commit(trail, "day 1", T0)
    done = activity(tmp_path, trail, None)
    assert done.returncode == 0 and b"::warning::" in done.stdout
    # An empty answer is not agreement either.
    empty = activity(tmp_path, trail, [])
    assert empty.returncode == 0 and b"nothing was checked" in empty.stdout
