"""The forward registry: a frozen rule is judged only on what happens after its freeze."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from grimstrade import forward, ledger

T0 = datetime(2026, 11, 19, 12, 0, tzinfo=UTC)
CANDIDATES = Path(__file__).resolve().parents[1] / forward.CANDIDATES


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


def commit(repo: Path, when: datetime) -> None:
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "x", when=when)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q", "-b", "main")
    (tmp_path / "rule.py").write_text("def decide():\n    return 1\n")
    commit(tmp_path, T0 - timedelta(days=1))
    return tmp_path


PLAN = forward.Plan("win_rate", effect=0.9, per_year=4, alpha=0.10, power=0.8)


def row(
    repo: Path, rule_id: str = "r@1", plan: forward.Plan = PLAN, **params: Any
) -> dict[str, Any]:
    return forward.entry(
        rule_id,
        code=forward.code_hashes(repo, ["rule.py"]),
        code_ref="HEAD",
        params=params or {"k": 1},
        data={"source": "test"},
        plan=plan,
        source="test",
    )


def reg(repo: Path) -> Path:
    return repo / forward.REGISTRY


def obs(r: dict[str, Any], starts: list[datetime], values: list[float]) -> list[forward.Obs]:
    return [
        forward.Obs(s, s + timedelta(days=1), v, r["rule_hash"])
        for s, v in zip(starts, values, strict=True)
    ]


def days(first: datetime, n: int) -> list[datetime]:
    return [first + timedelta(days=2 * i) for i in range(n)]


# --- power and minimum sample ---


def test_sharpe_sample_matches_the_closed_form_and_rl6() -> None:
    """A true annual Sharpe of 0.79 on weekly bars: ~7 years at alpha 0.10 (rl-6's number),
    ~12.6 at 0.025. Normal returns: n = 1 + ((z_a + z_b) / sr)^2, sr per period."""
    n10 = forward.min_periods_sharpe(0.79, 52, alpha=0.10, power=0.8)
    n025 = forward.min_periods_sharpe(0.79, 52, alpha=0.025, power=0.8)
    assert 7.0 < n10 / 52 < 7.5
    assert 12.4 < n025 / 52 < 12.8
    fat = forward.min_periods_sharpe(0.79, 52, alpha=0.10, power=0.8, skew=-1, kurtosis=8)
    assert fat > n10  # fat tails and negative skew need more data, never less


def test_mean_sample_scales_with_the_square_of_noise_over_effect() -> None:
    small = forward.min_events_mean(12, 107, alpha=0.10)
    big = forward.min_events_mean(24, 107, alpha=0.10)
    assert abs(small / big - 4) < 0.1
    assert forward.min_events_mean(10, 100, alpha=0.05, power=0.5) == 271  # (1.645 * 10)^2


def test_win_rate_sample_is_the_first_n_with_enough_exact_power() -> None:
    # By hand: n = 7, alpha 0.10 -> reject at >= 6 wins (P = 8/128 under 1/2); power at 0.9 is
    # 0.9^7 + 7 * 0.9^6 * 0.1 = 0.85. At n = 6 it needs 6 of 6: 0.53.
    assert forward.min_trials_win_rate(0.9, alpha=0.10, power=0.8) == 7
    assert forward.binom_tail(3, 3, 0.5) == pytest.approx(0.125)
    assert forward.binom_tail(0, 5, 0.3) == 1.0
    n = forward.min_trials_win_rate(0.714, alpha=0.025, power=0.8)
    c = forward._critical(n, 0.025)
    assert forward.binom_tail(c, n, 0.5) <= 0.025
    assert forward.binom_tail(c, n, 0.714) >= 0.8


def test_a_plan_that_cannot_be_tested_is_refused() -> None:
    with pytest.raises(ValueError):
        forward.Plan("mean", effect=1, per_year=8)  # no sd
    with pytest.raises(ValueError):
        forward.Plan("win_rate", effect=0.4, per_year=1)  # below a coin flip
    with pytest.raises(ValueError):
        forward.Plan("sharpe", effect=-0.5, per_year=52)
    with pytest.raises(ValueError):
        forward.Plan("hit", effect=0.5, per_year=52)


# --- freezing and append-only ---


def test_freeze_appends_and_refuses_the_same_id_again(repo: Path) -> None:
    line = forward.freeze(reg(repo), row(repo), T0)
    assert line["frozen_at"] == "2026-11-19T12:00:00Z"
    assert line["min_sample"] == 7
    with pytest.raises(forward.AlreadyFrozen):
        forward.freeze(reg(repo), row(repo, k=2), T0 + timedelta(hours=1))  # changed rule, old id
    forward.freeze(reg(repo), row(repo, "r@2", k=2), T0 + timedelta(hours=1))
    assert [r["id"] for r in forward.read(reg(repo))] == ["r@1", "r@2"]


def test_a_rewritten_committed_line_stops_the_registry(repo: Path) -> None:
    forward.freeze(reg(repo), row(repo), T0)
    commit(repo, T0 + timedelta(minutes=5))
    text = reg(repo).read_text().replace('"alpha":0.1', '"alpha":0.2')
    reg(repo).write_text(text)
    with pytest.raises(ledger.LedgerTampered):
        forward.freeze(reg(repo), row(repo, "r@2"), T0 + timedelta(hours=1))
    with pytest.raises(ledger.LedgerTampered):
        forward.freeze_times(reg(repo))


def test_a_line_edited_before_its_commit_fails_its_own_hash(repo: Path) -> None:
    forward.freeze(reg(repo), row(repo), T0)
    text = reg(repo).read_text().replace('"k":1', '"k":5')
    reg(repo).write_text(text)
    with pytest.raises(forward.HashMismatch):
        forward.read(reg(repo))


def test_a_doctored_min_sample_is_refused(repo: Path) -> None:
    r = row(repo)
    r["min_sample"] = 3  # smaller than the plan needs: an early verdict
    with pytest.raises(ValueError):
        forward.freeze(reg(repo), r, T0)


# --- freeze time ---


def test_an_uncommitted_freeze_cannot_be_scored(repo: Path) -> None:
    r = forward.freeze(reg(repo), row(repo), T0)
    frozen = forward.freeze_times(reg(repo))["r@1"]
    assert frozen is None
    with pytest.raises(forward.NotFrozen):
        forward.score(r, frozen, obs(r, days(T0 + timedelta(days=1), 3), [1, 1, 1]))


def test_freeze_counts_from_its_commit_when_that_is_later(repo: Path) -> None:
    forward.freeze(reg(repo), row(repo), T0)  # stamped T0 ...
    late = T0 + timedelta(days=30)
    commit(repo, late)  # ... but only provably written a month later
    assert forward.freeze_times(reg(repo))["r@1"] == late


# --- scoring ---


def committed(repo: Path) -> tuple[dict[str, Any], datetime]:
    r = forward.freeze(reg(repo), row(repo), T0)
    commit(repo, T0 + timedelta(minutes=5))
    frozen = forward.freeze_times(reg(repo))["r@1"]
    assert frozen == T0 + timedelta(minutes=5)
    return r, frozen


def test_a_bar_that_starts_before_the_freeze_is_refused(repo: Path) -> None:
    r, frozen = committed(repo)
    early = obs(r, [frozen - timedelta(minutes=1)], [1.0])  # ends after, starts before
    with pytest.raises(forward.LookAhead):
        forward.score(r, frozen, early + obs(r, days(frozen + timedelta(days=1), 7), [1] * 7))
    ok = forward.score(r, frozen, obs(r, [frozen], [1.0]))  # starting exactly at it is fine
    assert ok.n == 1


def test_observations_from_other_code_are_refused(repo: Path) -> None:
    r, frozen = committed(repo)
    other = [forward.Obs(frozen, frozen + timedelta(days=1), 1.0, "0" * 64)]
    with pytest.raises(forward.HashMismatch):
        forward.score(r, frozen, other)


def test_overlapping_observations_are_refused(repo: Path) -> None:
    r, frozen = committed(repo)
    two = obs(r, [frozen, frozen + timedelta(hours=12)], [1.0, 1.0])
    with pytest.raises(ValueError):
        forward.score(r, frozen, two)


def test_verdict_waits_for_the_minimum_and_reads_only_the_first_n(repo: Path) -> None:
    r, frozen = committed(repo)
    start = frozen + timedelta(days=1)
    waiting = forward.score(r, frozen, obs(r, days(start, 6), [1.0] * 6))
    assert waiting.verdict == "waiting"  # 6 of 6 wins, still not judged before n = 7
    passed = forward.score(r, frozen, obs(r, days(start, 7), [1.0] * 6 + [-1.0]))
    assert passed.verdict == "pass"  # 6 of 7: p = 8/128 < 0.10
    later = forward.score(r, frozen, obs(r, days(start, 20), [1.0] * 6 + [-1.0] * 14))
    assert later.verdict == "pass" and later.n == 20  # later losses never undo the verdict
    failed = forward.score(r, frozen, obs(r, days(start, 20), [1.0] * 5 + [-1.0] * 2 + [1.0] * 13))
    assert failed.verdict == "fail"  # 5 of the first 7; later wins never rescue it


def test_sharpe_and_mean_scores(repo: Path) -> None:
    plans = {
        "s@1": forward.Plan("sharpe", effect=1.0, per_year=52, alpha=0.10),
        "m@1": forward.Plan("mean", effect=0.01, per_year=52, alpha=0.10, sd=0.02),
    }
    for rule_id, plan in plans.items():
        forward.freeze(reg(repo), row(repo, rule_id, plan), T0)
    commit(repo, T0 + timedelta(minutes=5))
    frozen = forward.freeze_times(reg(repo))
    values = [0.02, -0.01, 0.03, 0.0, 0.01, 0.02, -0.005, 0.015]
    for r in forward.read(reg(repo)):
        start = T0 + timedelta(days=1)
        s = forward.score(r, frozen[r["id"]], obs(r, days(start, len(values)), values))
        assert s.verdict == "waiting", r["id"]
        assert s.estimate is not None and s.estimate > 0
        assert s.p is not None and 0 < s.p < 0.5


# --- the frozen code ---


def test_changed_or_missing_code_is_a_hash_mismatch(repo: Path) -> None:
    r = row(repo)
    forward.check_code(r, repo)  # unchanged: fine
    forward.check_code(r, repo, ref="HEAD")
    (repo / "rule.py").write_text("def decide():\n    return 2\n")
    with pytest.raises(forward.HashMismatch):
        forward.check_code(r, repo)
    (repo / "rule.py").unlink()
    with pytest.raises(forward.HashMismatch):
        forward.check_code(r, repo)


# --- the proposals in the repo ---


def test_proposals_are_not_frozen_and_their_numbers_are_the_calculators() -> None:
    rows = [json.loads(x) for x in CANDIDATES.read_text().splitlines() if x.strip()]
    assert len(rows) == 4
    for r in rows:
        assert "frozen_at" not in r
        assert "not frozen" in r["status"].lower()
        assert r["rule_hash"] == forward.rule_hash(r["code"], r["params"], r["data"])
        assert r["min_sample"] == forward.min_sample(forward.plan_of(r))
        assert r["years_needed"] == round(forward.years_needed(forward.plan_of(r)), 1)


def test_table_lists_each_rule() -> None:
    rows = [json.loads(x) for x in CANDIDATES.read_text().splitlines() if x.strip()]
    out = forward.table(rows)
    assert all(f"`{r['id']}`" in out for r in rows)
