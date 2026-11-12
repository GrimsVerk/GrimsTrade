"""Honesty audit 2026-11: the daily workflow and its two guard scripts.

The workflow itself can't run in tests; its risky steps live in scripts that can:
`scripts/checkout-trail.sh` (audit L5) and `scripts/check-trail-activity.sh` (audit L1, L3).
The scripts run here against throwaway git repos and a fake `gh`, offline.
"""

import os
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
DAILY = ROOT / ".github" / "workflows" / "daily.yml"
CHECKOUT = ROOT / "scripts" / "checkout-trail.sh"
ACTIVITY = ROOT / "scripts" / "check-trail-activity.sh"
T0 = datetime(2026, 11, 11, 22, 0, 51, tzinfo=UTC)
ZERO = "0" * 40
BOT = "github-actions[bot]"


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
    ours = {k: v for k, v in os.environ.items() if k != "GITHUB_SHA"}  # set in CI: not this repo's
    return subprocess.run(["bash", str(CHECKOUT)], cwd=work, capture_output=True, env=ours | env)


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


def test_a_tag_or_another_branch_is_not_taken_for_the_record(clone: Path) -> None:
    """Second review: `git fetch origin paper-trail:paper-trail` resolves a tag of that name
    first, so the job would run on the tag's history while the outside check looked at the
    branch. And `ls-remote --heads origin paper-trail` also matches `backup/paper-trail`."""
    origin = clone.parent / "origin"
    tip = git(origin, "rev-parse", "paper-trail")
    git(origin, "checkout", "-q", "paper-trail")
    forged = commit(origin, "forged line", T0)
    git(origin, "tag", "paper-trail", forged)
    git(origin, "reset", "-q", "--hard", tip)
    git(origin, "checkout", "-q", "main")
    done = checkout(clone)
    assert done.returncode == 0, done.stderr
    assert git(clone / "trail", "rev-parse", "HEAD") == tip
    # Another branch whose name ends the same way does not count as the record existing.
    git(origin, "tag", "-d", "paper-trail")
    git(origin, "branch", "-m", "paper-trail", "backup/paper-trail")
    git(clone, "worktree", "remove", "--force", "trail")
    git(clone, "branch", "-D", "paper-trail")
    missing = checkout(clone)
    assert missing.returncode == 1 and b"origin has no paper-trail branch" in missing.stderr


def test_only_the_tip_of_main_writes_the_record(clone: Path) -> None:
    """Second review: re-running an old run executes that run's commit and workflow file (for 30
    days), so merged guards do not protect against it. The checkout refuses unless the commit
    the job runs is main's newest."""
    origin = clone.parent / "origin"
    old = git(origin, "rev-parse", "main")
    assert checkout(clone, GITHUB_SHA=old).returncode == 0
    git(clone, "worktree", "remove", "--force", "trail")
    commit(origin, "newer code", T0)
    stale = checkout(clone, GITHUB_SHA=old)
    assert stale.returncode == 1 and b"Only the newest code on main" in stale.stderr
    assert not (clone / "trail").exists()


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
    tmp_path: Path,
    trail: Path,
    events: list[tuple[Any, ...]] | None,
    cut_short: bool = False,
    **env: str,
) -> subprocess.CompletedProcess[bytes]:
    """Run the script with a fake `gh` that prints `events` (time, type, before, after and, if
    it is not the daily job, who) the way the real call's --jq does, newest first; `None` makes
    gh fail, `cut_short` makes it fail after printing (a later page that did not arrive)."""
    fake = tmp_path / "bin"
    fake.mkdir(exist_ok=True)
    if events is None:
        body = "#!/bin/sh\nexit 1\n"
    else:
        rows = [
            f"{iso(t)}\t{kind}\t{(*who, BOT)[0]}\t{before}\t{after}"
            for t, kind, before, after, *who in events
        ]
        (tmp_path / "events.tsv").write_text("".join(r + "\n" for r in reversed(rows)))
        body = f'#!/bin/sh\ncat "{tmp_path / "events.tsv"}"\n' + "exit 1\n" * cut_short
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
    assert forced.returncode == 2 and b"force_push by github-actions[bot]" in forced.stdout
    again = [created, (T0 + timedelta(hours=3), "branch_deletion", a, ZERO), created]
    recreated = activity(tmp_path, trail, again)
    assert recreated.returncode == 2 and b"created 2 times" in recreated.stdout
    # Once a person has looked and set TRAIL_REVIEWED_UNTIL past the event, the job runs again,
    # but the event is not forgotten: it goes into the trail and onto the scoreboard, every run.
    reviewed = iso(T0 + timedelta(hours=4))
    events = [created, (T0 + timedelta(hours=3), "force_push", a, a)]
    accepted = activity(tmp_path, trail, events, TRAIL_REVIEWED_UNTIL=reviewed)
    assert accepted.returncode == 0 and b"::warning::" in accepted.stdout
    note = trail / "ledger" / "acknowledged-rewrites.txt"
    assert note.read_text() == "force_push by github-actions[bot] at 2026-11-12T01:00:51Z\n"
    from grimstrade import report

    board = report.render(trail, {}, tmp_path)
    assert "written to by someone other than the daily job (1 event), and a person" in board
    assert "force_push by github-actions[bot] at 2026-11-12T01:00:51Z" in board
    # A later, new force-push stops the job again; the variable is not a blanket off-switch...
    events.append((T0 + timedelta(days=2), "force_push", a, a))
    assert activity(tmp_path, trail, events, TRAIL_REVIEWED_UNTIL=reviewed).returncode == 2
    # ...and it cannot be set to the future to wave everything through.
    future = activity(tmp_path, trail, events, TRAIL_REVIEWED_UNTIL="2099-01-01T00:00:00Z")
    assert future.returncode == 2 and b"is in the future" in future.stdout
    # Found by the second reviewer: the note used to be rebuilt from GitHub's answer on every
    # run, so it vanished if that answer ever stopped listing the event. It is kept for good.
    assert activity(tmp_path, trail, [created]).returncode == 0
    assert "force_push by github-actions[bot]" in note.read_text()
    assert "the daily job (1 event), and a person" in report.render(trail, {}, tmp_path)
    # The owner's page says it too (it used to say nothing).
    from grimstrade import data, ledger, weekly
    from grimstrade.data import Bar

    bars = [Bar(T0.date() + timedelta(days=i), 1.0, 1.0, 1.0, 1.0, 1.0) for i in range(3)]
    data.append(trail, "BTC", bars)
    ledger.write_decision(trail, T0, "buy_hold_btc", {"BTC": 1.0}, {"BTC": bars[:1]}, "t")
    page = weekly.render(trail, data.load_all(trail), tmp_path)
    assert "**Warning:** the record branch was rewritten, back-dated or written to" in page
    assert "the daily job (1 accepted event); see the end of `scoreboard.md`" in page


def test_a_planted_symlink_cannot_swallow_the_accepted_rewrite(tmp_path: Path, trail: Path) -> None:
    """Second review, high: with `ledger/acknowledged-rewrites.txt` (then under state/) pushed as
    a link to /dev/null, the script wrote the accepted event into the void and reported success;
    the scoreboard said nothing. A force-push plus the variable plus this link was a silent
    off-switch."""
    a = commit(trail, "day 1", T0)
    (trail / "ledger").mkdir()
    (trail / "ledger" / "acknowledged-rewrites.txt").symlink_to("/dev/null")
    events = [
        (T0 + timedelta(seconds=1), "branch_creation", ZERO, a),
        (T0 + timedelta(hours=3), "force_push", a, a),
    ]
    done = activity(tmp_path, trail, events, TRAIL_REVIEWED_UNTIL=iso(T0 + timedelta(hours=4)))
    assert done.returncode == 2 and b"is a symlink" in done.stdout


def test_a_review_date_must_be_plain_utc(tmp_path: Path, trail: Path) -> None:
    """Second review: the variable is compared as text. A local-time value such as
    01:30:00+01:00 (00:30 UTC) accepted a force-push made at 01:00 UTC, after that instant."""
    a = commit(trail, "day 1", T0)
    events = [
        (T0 + timedelta(seconds=1), "branch_creation", ZERO, a),
        (T0 + timedelta(hours=3), "force_push", a, a),
    ]
    local = activity(tmp_path, trail, events, TRAIL_REVIEWED_UNTIL="2026-11-12T01:30:00+01:00")
    assert local.returncode == 2 and b"must look like" in local.stdout


def test_an_event_without_an_actor_is_still_read_right(tmp_path: Path, trail: Path) -> None:
    """Second review: an empty actor field made every later column shift by one, so the commit
    ids were read from the wrong place."""
    a = commit(trail, "day 1", T0)
    b = commit(trail, "day 2", T0 + timedelta(days=1))
    events = [
        (T0 + timedelta(seconds=1), "branch_creation", ZERO, a),
        (T0 + timedelta(days=1, seconds=1), "push", a, b, ""),
    ]
    done = activity(tmp_path, trail, events)
    assert done.returncode == 2 and b"push by (no actor) at 2026-11-12T22:00:52Z" in done.stdout


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


def test_a_push_by_anyone_but_the_daily_job_stops_the_job(tmp_path: Path, trail: Path) -> None:
    """Audit L3 (second pass): the guard looked at how the branch was written, not by whom. An
    agent or a person with write access could push a well-formed, on-time commit (a decision in
    a live strategy's name, say) and the job ran on. Only the daily job writes the record."""
    t0 = T0 - timedelta(days=30)  # all of it well in the past: the script reads the real clock
    a = commit(trail, "day 1", t0)
    b = commit(trail, "day 2", t0 + timedelta(days=1))
    created = (t0 + timedelta(seconds=1), "branch_creation", ZERO, a)
    by_hand = [created, (t0 + timedelta(days=1, seconds=1), "push", a, b, "GrimsBot")]
    done = activity(tmp_path, trail, by_hand)
    assert done.returncode == 2 and b"push by GrimsBot at 2026-10-13T22:00:52Z" in done.stdout
    # A person can accept it; it then stays on the scoreboard like any other accepted event.
    seen = activity(tmp_path, trail, by_hand, TRAIL_REVIEWED_UNTIL=iso(t0 + timedelta(days=2)))
    assert seen.returncode == 0
    assert "push by GrimsBot" in (trail / "ledger" / "acknowledged-rewrites.txt").read_text()
    # Commits that arrive by a merged pull request are checked like pushed ones: this one is
    # by the daily job but back-dated by three days.
    c = commit(trail, "day 3", t0 + timedelta(days=2))
    honest = [created, (t0 + timedelta(days=1, seconds=1), "push", a, b)]
    merged = [*honest, (t0 + timedelta(days=5), "pr_merge", b, c)]
    late = activity(tmp_path, trail, merged)
    assert late.returncode == 2 and b"but reached GitHub at 2026-10-17" in late.stdout
    # A commit GitHub received that is no longer in the record means the record was replaced.
    gone = [*honest, (t0 + timedelta(days=2, seconds=1), "push", b, "f" * 40)]
    lost = activity(tmp_path, trail, gone)
    assert lost.returncode == 2 and b"is not in the record" in lost.stdout


def test_an_accepted_backdated_commit_is_dated_by_githubs_clock(
    tmp_path: Path, trail: Path
) -> None:
    """Audit L14 (second review): once a person had accepted a back-dated push, its lines went
    on counting from the date the commit claims. The script writes down when GitHub received
    it, and the ledger dates the commit's lines by that."""
    from grimstrade import ledger

    t0 = T0 - timedelta(days=30)  # well in the past: the script reads the real clock
    a = commit(trail, "day 1", t0)
    b = commit(trail, "day 2, written on day 4", t0 + timedelta(days=1))
    arrived = t0 + timedelta(days=3)
    events = [(t0 + timedelta(seconds=1), "branch_creation", ZERO, a), (arrived, "push", a, b)]
    assert ledger.recorded_at(trail / "ledger.jsonl") == [t0, t0 + timedelta(days=1)]
    done = activity(tmp_path, trail, events, TRAIL_REVIEWED_UNTIL=iso(t0 + timedelta(days=4)))
    assert done.returncode == 0 and b"accepted" in done.stdout
    assert ledger.recorded_at(trail / "ledger.jsonl") == [t0, arrived]


def test_when_github_cannot_be_asked_the_job_goes_on_with_a_warning(
    tmp_path: Path, trail: Path
) -> None:
    commit(trail, "day 1", T0)
    done = activity(tmp_path, trail, None)
    assert done.returncode == 0 and b"::warning::" in done.stdout
    # An empty answer is not agreement either.
    empty = activity(tmp_path, trail, [])
    assert empty.returncode == 0 and b"nothing was checked" in empty.stdout
    # Second review: such a run used to leave no trace; the scoreboard looked like any other.
    from grimstrade import report

    board = report.render(trail, {}, tmp_path)
    assert "**The last run could not check the record branch against GitHub's log:**" in board
    assert "GitHub's activity log came back empty" in board
    # ...and it clears once a run can check again.
    a = git(trail, "rev-parse", "HEAD")
    assert activity(tmp_path, trail, [(T0, "branch_creation", ZERO, a)]).returncode == 0
    assert "could not check the record branch" not in report.render(trail, {}, tmp_path)


def test_a_force_push_in_an_answer_that_was_cut_short_still_stops_the_job(
    tmp_path: Path, trail: Path
) -> None:
    """Second review: when `gh` failed after printing its first page, everything was thrown
    away and the job ran on, even with a force-push in the rows that had arrived."""
    a = commit(trail, "day 1", T0)
    events = [
        (T0 + timedelta(seconds=1), "branch_creation", ZERO, a),
        (T0 + timedelta(hours=3), "force_push", a, a),
    ]
    done = activity(tmp_path, trail, events, cut_short=True)
    assert done.returncode == 2 and b"force_push" in done.stdout
    # With nothing wrong in what arrived the job goes on, and says the check was partial.
    partial = activity(tmp_path, trail, events[:1], cut_short=True)
    assert partial.returncode == 0 and b"only part of the" in partial.stdout
    assert "NOT fully checked" in (trail / "state" / "witness.txt").read_text()
