import subprocess
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from grimstrade import ledger
from grimstrade.data import Bar
from grimstrade.strategies import LIVE

T = datetime(2026, 11, 10, 22, 30, tzinfo=UTC)
REPO_ROOT = Path(__file__).resolve().parent.parent


def git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    return tmp_path


def decide_and_commit(repo: Path, strategy: str) -> None:
    seen = {"BTC": [Bar(date(2026, 11, 9), 1, 1, 1, 100.0, 1)]}
    ledger.write_decision(repo, T, strategy, {"BTC": 1.0}, seen, "test")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", strategy)


def test_a_branch_with_no_commits_yet_passes(repo: Path) -> None:
    # The first daily run starts on a fresh orphan paper-trail branch with no commits.
    assert ledger.check_append_only(repo / ledger.DECISIONS) == 0
    seen = {"BTC": [Bar(date(2026, 11, 9), 1, 1, 1, 100.0, 1)]}
    ledger.write_decision(repo, T, "a", {"BTC": 1.0}, seen, "test")
    assert ledger.check_append_only(repo / ledger.DECISIONS) == 0


def test_appending_passes_the_history_check(repo: Path) -> None:
    decide_and_commit(repo, "a")
    decide_and_commit(repo, "b")
    assert ledger.check_append_only(repo / ledger.DECISIONS) == 2
    rows = ledger.decisions(repo)
    assert [r["strategy"] for r in rows] == ["a", "b"]
    assert rows[0]["prices"] == {"BTC": 100.0}
    assert rows[0]["data_through"] == {"BTC": "2026-11-09"}
    assert rows[0]["time"] == "2026-11-10T22:30:00Z"


def test_rewriting_a_committed_line_fails(repo: Path) -> None:
    decide_and_commit(repo, "a")
    path = repo / ledger.DECISIONS
    path.write_text(path.read_text().replace('"BTC":1.0', '"BTC":0.5'))
    with pytest.raises(ledger.LedgerTampered):
        ledger.check_append_only(path)  # caught in the working tree
    git(repo, "commit", "-qam", "rewrite")
    with pytest.raises(ledger.LedgerTampered):
        ledger.check_append_only(path)  # and in history


def test_deleting_a_committed_line_fails(repo: Path) -> None:
    decide_and_commit(repo, "a")
    decide_and_commit(repo, "b")
    path = repo / ledger.DECISIONS
    path.write_text(path.read_text().splitlines(keepends=True)[1])
    git(repo, "commit", "-qam", "drop first line")
    with pytest.raises(ledger.LedgerTampered):
        ledger.check_append_only(path)


def test_the_real_ledgers_are_append_only() -> None:
    # On the paper-trail checkout (trail/) or wherever the ledger lives.
    for root in (REPO_ROOT, REPO_ROOT / "trail"):
        for rel in (ledger.DECISIONS, ledger.TRIES):
            if (root / rel).exists():
                ledger.check_append_only(root / rel)


def test_tries_count_each_strategy_once(tmp_path: Path) -> None:
    assert ledger.register_try(tmp_path, "x", "", T)
    assert not ledger.register_try(tmp_path, "x", "", T)
    assert ledger.register_try(tmp_path, "y", "", T)
    assert ledger.tries(tmp_path) == 2


def test_live_strategies_give_valid_weights() -> None:
    from grimstrade.gym import validate

    full = {s: [Bar(date(2026, 11, 9), 1, 1, 1, 1, 1)] for s in ("BTC", "ETH", "SPY", "TLT")}
    for decide in LIVE.values():
        for history in ({}, full):
            weights, reason = decide(history)
            validate(weights)
            assert reason
