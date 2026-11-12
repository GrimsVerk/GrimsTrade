"""Honesty audit 2026-11: ways the ledger can lie that `check_append_only` does not catch.

Each xfail test demonstrates one finding in docs/audits/honesty-2026-11.md and turns green when
that finding is fixed (strict: an unexpected pass fails the suite, so the marker gets removed).
"""

import subprocess
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from grimstrade import gym, ledger, report
from grimstrade.data import Bar, History

DAY1 = date(2026, 11, 1)


def git(repo: Path, *args: str, when: datetime | None = None) -> str:
    env = None
    if when is not None:
        stamp = when.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        env = {"GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp, "PATH": "/usr/bin:/bin"}
    out = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )
    return out.stdout.decode().strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q", "-b", "paper-trail")
    return tmp_path


def at(d: date, hh: int = 22, mm: int = 30) -> datetime:
    return datetime(d.year, d.month, d.day, hh, mm, tzinfo=UTC)


def btc(opens_closes: list[tuple[float, float]]) -> list[Bar]:
    return [
        Bar(DAY1 + timedelta(days=i), o, max(o, c), min(o, c), c, 1.0)
        for i, (o, c) in enumerate(opens_closes)
    ]


def decide(repo: Path, when: datetime, strategy: str, weights: dict[str, float]) -> None:
    seen: History = {"BTC": [Bar(when.date() - timedelta(days=1), 1, 1, 1, 100.0, 1)]}
    ledger.write_decision(repo, when, strategy, weights, seen, "test")


def commit(repo: Path, message: str, when: datetime) -> None:
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", message, when=when)


@pytest.mark.xfail(
    strict=True,
    reason="audit L1: a decision appended after the outcome, stamped with an earlier time, is "
    "accepted and filled at the old open (append-only is not the same as written-in-time)",
)
def test_a_backdated_decision_is_not_credited(repo: Path) -> None:
    # BTC: flat on day 1, opens day 2 at 100 and then doubles by the close of day 3.
    history: History = {"BTC": btc([(100, 100), (100, 150), (150, 200), (200, 200)])}
    # Day 1, 22:30: the honest run. Everyone stays in cash. Committed the same minute.
    decide(repo, at(DAY1), "honest", {})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))

    # Day 4: BTC has doubled. Someone appends a line that claims "on day 1 at 22:31 I went all in".
    decide(repo, at(DAY1, 22, 31), "cheat", {"BTC": 1.0})
    commit(repo, "Daily run day 4", when=at(DAY1 + timedelta(days=3), 22, 31))

    # The append-only check is satisfied: nothing that was committed has changed.
    ledger.check_append_only(repo / ledger.DECISIONS)
    # ...and the scoreboard books the hindsight trade at the day-2 open, doubling the money.
    results = report.live_results(repo, history)
    cheat = report.score("cheat", results["cheat"])
    assert cheat.total_return > 0.9

    # What honesty needs: a line whose time is days older than the commit that first carried it
    # must not count. (Today nothing compares a decision's time with when it was committed.)
    assert cheat.total_return == pytest.approx(0.0) or cheat.equity == gym.START_CASH


def _honest_two_days(repo: Path) -> Path:
    """Two honest daily commits: day 1 `s` goes all in on BTC, day 2 it holds."""
    decide(repo, at(DAY1), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    decide(repo, at(DAY1 + timedelta(days=1)), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    return repo / ledger.DECISIONS


@pytest.mark.xfail(
    strict=True,
    reason="audit L2: history can be rewritten with an ordinary (fast-forward) push: a merge "
    "that takes the forged side makes `git log -- file` skip the honest side",
)
def test_a_rewrite_hidden_behind_a_merge_is_caught(repo: Path) -> None:
    path = _honest_two_days(repo)
    honest_head = git(repo, "rev-parse", "HEAD")
    # BTC crashed, so the forger wants day 1 to say "stayed in cash". Build a parallel history
    # with the forged file, then merge the honest branch into it keeping the forged content.
    git(repo, "checkout", "-q", "--orphan", "forged")
    path.write_text(path.read_text().replace('"weights":{"BTC":1.0}', '"weights":{}'))
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    git(repo, "merge", "-q", "-s", "ours", "--allow-unrelated-histories", "-m", "sync", honest_head)
    # The result descends from the honest head, so pushing it is a plain fast-forward:
    # no force-push, and "block force pushes" on the branch would not stop it.
    git(repo, "merge-base", "--is-ancestor", honest_head, "HEAD")
    assert all(r["weights"] == {} for r in ledger.decisions(repo))  # the record now lies

    with pytest.raises(ledger.LedgerTampered):
        ledger.check_append_only(path)


def test_a_force_pushed_history_passes_the_check(repo: Path) -> None:
    """Audit L3, the limit of any check that only reads the branch: if the whole history is
    replaced (force-push, or delete + recreate), the new history is self-consistent and nothing
    inside it can show the old one existed. Only an outside witness can (GitHub's activity log,
    a branch ruleset). This test documents the limit; the guard is tested in
    test_audit_workflow.py."""
    path = _honest_two_days(repo)
    git(repo, "checkout", "-q", "--orphan", "rewritten")
    path.write_text(path.read_text().replace('"weights":{"BTC":1.0}', '"weights":{}'))
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    git(repo, "branch", "-q", "-M", "paper-trail")  # what `push --force` leaves on the remote
    assert ledger.check_append_only(path) == 1


@pytest.mark.xfail(
    strict=True,
    reason="audit L4: stored bars are part of the record (the scoreboard is recomputed from them "
    "every run) but nothing checks that committed rows in data/bars/ stay unchanged",
)
def test_a_rewritten_bar_is_caught(repo: Path) -> None:
    from grimstrade import data, run_daily

    data.append(repo, "BTC", btc([(100, 100), (100, 100), (100, 100)]))
    decide(repo, at(DAY1), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    before = report.score("s", report.live_results(repo, data.load_all(repo))["s"])

    # Lower the price `s` paid at the day-2 open from 100 to 50. One edited cell.
    bars = data.bars_path(repo, "BTC")
    lines = bars.read_text().splitlines(keepends=True)
    assert lines[2].startswith("2026-11-02,100.0,")
    lines[2] = lines[2].replace("2026-11-02,100.0,", "2026-11-02,50.0,")
    bars.write_text("".join(lines))
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    after = report.score("s", report.live_results(repo, data.load_all(repo))["s"])
    assert before.total_return < 0 and after.total_return > 0.9  # a loss became +99%

    def offline(url: str) -> bytes:
        raise OSError("offline")

    with pytest.raises(ledger.LedgerTampered):
        run_daily.run(repo, at(DAY1 + timedelta(days=2)), offline)


def test_outside_a_git_checkout_the_check_silently_checks_nothing(tmp_path: Path) -> None:
    """Audit L6 (low): `--root` pointing at a plain folder (or at a gitignored `trail/` that is
    not a worktree) makes `check_append_only` return 0 without complaint, and the runner ignores
    the return value. A rewritten ledger there is never noticed."""
    decide(tmp_path, at(DAY1), "s", {"BTC": 1.0})
    path = tmp_path / ledger.DECISIONS
    path.write_text(path.read_text().replace('"BTC":1.0', '"BTC":0.5'))
    assert ledger.check_append_only(path) == 0


@pytest.mark.xfail(
    strict=True,
    reason="audit L7: a decision line does not say which code made it, so a strategy can be "
    "changed under the same name and keep one unbroken track record (and one try)",
)
def test_a_decision_records_the_code_version(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_SHA", "8e26333a0000000000000000000000000000beef")
    decide(repo, at(DAY1), "s", {"BTC": 1.0})
    (row,) = ledger.decisions(repo)
    assert row["code"] == "8e26333a0000000000000000000000000000beef"
