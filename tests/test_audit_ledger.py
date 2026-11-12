"""Honesty audit 2026-11: ways the ledger can lie that `check_append_only` does not catch.

Each xfail test demonstrates one finding in docs/audits/honesty-2026-11.md and turns green when
that finding is fixed (strict: an unexpected pass fails the suite, so the marker gets removed).
"""

import subprocess
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from grimstrade import ledger, report
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


def test_a_backdated_decision_is_not_credited(repo: Path) -> None:
    """Audit L1 (fixed): append-only is not the same as written-in-time. A line appended after
    the outcome, stamped with an earlier time, used to be filled at the old open. Now a decision
    counts from the moment its commit was made."""
    # BTC: flat on day 1, opens day 2 at 100, doubles by day 3, then stays at 200.
    history: History = {"BTC": btc([(100, 100), (100, 150), (150, 200), (200, 200), (200, 200)])}
    # Day 1, 22:30: the honest run. Everyone stays in cash. Committed the same minute.
    decide(repo, at(DAY1), "honest", {})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    # Day 4: BTC has doubled. Someone appends a line that claims "on day 1 at 22:31 I went all in".
    decide(repo, at(DAY1, 22, 31), "cheat", {"BTC": 1.0})
    commit(repo, "Daily run day 4", when=at(DAY1 + timedelta(days=3), 22, 31))

    # It is an append, so the append-only check has nothing to say...
    ledger.check_append_only(repo / ledger.DECISIONS)
    # ...but the order is filled at the first open after it was committed (day 5, at 200), not at
    # the day-2 open (100) it was aiming for: no profit from hindsight.
    (fill,) = report.live_results(repo, history)["cheat"].fills
    assert fill.time == datetime(2026, 11, 5, tzinfo=UTC)
    assert fill.price == pytest.approx(200 * 1.0005)
    assert report.score("cheat", report.live_results(repo, history)["cheat"]).total_return < 0
    # And the scoreboard says so.
    (_, late) = ledger.in_force(repo)
    assert late == 1
    assert "**Late decisions: 1.**" in report.render(repo, history)


def test_a_decision_counts_from_its_commit(repo: Path) -> None:
    """Audit T1 (fixed with L1): a late run stamped 23:59:30 whose commit lands after midnight
    is not filled at the 00:00 open that already existed when it was recorded."""
    history: History = {"BTC": btc([(100, 100), (200, 200), (300, 300), (300, 300)])}
    stamped = datetime(2026, 11, 1, 23, 59, 30, tzinfo=UTC)
    decide(repo, stamped, "s", {"BTC": 1.0})
    # Before the commit exists (the run itself, scoring its own fresh line): the timestamp counts.
    assert ledger.in_force(repo)[0][0][0] == stamped
    commit(repo, "Daily run", when=datetime(2026, 11, 2, 0, 0, 40, tzinfo=UTC))
    ((counts_from, _),), late = ledger.in_force(repo)
    assert counts_from == datetime(2026, 11, 2, 0, 0, 40, tzinfo=UTC) and late == 0
    (fill,) = report.live_results(repo, history)["s"].fills
    assert fill.time == datetime(2026, 11, 3, tzinfo=UTC) and fill.price == pytest.approx(300.15)


def test_normal_runs_and_one_commit_for_two_days(repo: Path) -> None:
    # Two ordinary runs, each committed a minute later: both count, in order, nothing is late.
    decide(repo, at(DAY1), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    decide(repo, at(DAY1 + timedelta(days=1)), "s", {})
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    counted, late = ledger.in_force(repo)
    assert [(t, r["weights"]) for t, r in counted] == [
        (at(DAY1, 22, 31), {"BTC": 1.0}),
        (at(DAY1 + timedelta(days=1), 22, 31), {}),
    ]
    assert late == 0
    # A sloppy local run: days 3 and 4 decided on time but committed together on day 4. Day 3's
    # line was never provably in force before day 4's replaced it, so only day 4's counts.
    decide(repo, at(DAY1 + timedelta(days=2)), "s", {"BTC": 0.5})
    decide(repo, at(DAY1 + timedelta(days=3)), "s", {"BTC": 0.25})
    decide(repo, at(DAY1 + timedelta(days=3)), "other", {})
    commit(repo, "two days at once", when=at(DAY1 + timedelta(days=3), 22, 31))
    counted, late = ledger.in_force(repo)
    assert [r["weights"] for _, r in counted if r["strategy"] == "s"] == [
        {"BTC": 1.0}, {}, {"BTC": 0.25},
    ]  # fmt: skip
    assert late == 1
    assert len(ledger.recorded_at(repo / ledger.DECISIONS)) == len(ledger.decisions(repo)) == 5


def test_outside_git_decisions_count_from_their_own_time(tmp_path: Path) -> None:
    decide(tmp_path, at(DAY1), "s", {"BTC": 1.0})
    assert ledger.in_force(tmp_path) == ([(at(DAY1), ledger.decisions(tmp_path)[0])], 0)
    assert ledger.in_force(tmp_path / "nothing-here") == ([], 0)


def _honest_two_days(repo: Path) -> Path:
    """Two honest daily commits: day 1 `s` goes all in on BTC, day 2 it holds."""
    decide(repo, at(DAY1), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    decide(repo, at(DAY1 + timedelta(days=1)), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    return repo / ledger.DECISIONS


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

    # Audit L2 (fixed): `git log -- file` skipped the honest side of that merge; the check now
    # compares every commit with each of its parents.
    with pytest.raises(ledger.LedgerTampered):
        ledger.check_append_only(path)


def test_honest_merges_and_a_deleted_working_file(repo: Path) -> None:
    path = _honest_two_days(repo)
    # A merge that brings in an unrelated side branch without touching the ledger is fine.
    git(repo, "checkout", "-q", "-b", "side")
    (repo / "note.txt").write_text("x")
    commit(repo, "side note", when=at(DAY1 + timedelta(days=1), 23, 0))
    git(repo, "checkout", "-q", "paper-trail")
    decide(repo, at(DAY1 + timedelta(days=2)), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 3", when=at(DAY1 + timedelta(days=2), 22, 31))
    git(repo, "merge", "-q", "--no-ff", "-m", "merge side", "side")
    assert ledger.check_append_only(path) == 3
    # Deleting the ledger from the working tree is a rewrite too.
    path.unlink()
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


def test_a_rewritten_bar_is_caught(repo: Path) -> None:
    """Audit L4 (fixed): stored bars are part of the record (the scoreboard is recomputed from
    them every run) but only the ledger files were checked for rewrites."""
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

    with pytest.raises(ledger.LedgerTampered, match="data/bars/BTC.csv"):
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
