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
