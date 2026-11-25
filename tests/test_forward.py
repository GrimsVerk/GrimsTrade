"""The forward registry: a frozen rule is judged only on what happens after its freeze."""

from __future__ import annotations

import json
import math
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
    """A true annual Sharpe of 0.79 on weekly bars: the iid closed form n = 1 + ((z_a + z_b) /
    sr)^2 gives ~7 years at alpha 0.10 (rl-6's number) and ~12.6 at 0.025; the one-year HAC
    test's wider critical value (fixed-b, b = 51 / n) adds 1-2 years."""
    n10 = forward.min_periods_sharpe(0.79, 52, alpha=0.10, power=0.8)
    n025 = forward.min_periods_sharpe(0.79, 52, alpha=0.025, power=0.8)
    sr = 0.79 / 52**0.5
    iid10 = 1 + ((forward._z(0.10, 0.8)) / sr) ** 2
    iid025 = 1 + ((forward._z(0.025, 0.8)) / sr) ** 2
    assert 7.0 < iid10 / 52 < 7.5 and 12.4 < iid025 / 52 < 12.8
    assert iid10 < n10 < 1.25 * iid10 and iid025 < n025 < 1.2 * iid025
    assert n025 == forward.min_periods_sharpe(0.79, 52, alpha=0.025) == 750
    fat = forward.min_periods_sharpe(0.79, 52, alpha=0.10, power=0.8, skew=-1, kurtosis=8)
    assert fat > n10  # fat tails and negative skew need more data, never less


def test_mean_sample_scales_with_the_square_of_noise_over_effect() -> None:
    small = forward.min_events_mean(12, 107, alpha=0.10)
    big = forward.min_events_mean(24, 107, alpha=0.10)
    assert abs(small / big - 4) < 0.1
    # (1.645 * 10)^2 = 271 with a normal critical value; with no lags (per_year 1) the test is
    # the t-test, whose t(272) critical value 1.6505 asks for 273
    assert forward.min_events_mean(10, 100, alpha=0.05, power=0.5) == 273


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


def test_a_registry_line_without_frozen_at_is_refused(repo: Path) -> None:
    # A proposal (an `entry` row) pasted into the registry by hand: no freeze time, refused.
    forward.freeze(reg(repo), row(repo), T0)
    ledger._append(reg(repo), row(repo, "pasted@1"))
    with pytest.raises(forward.MissingFreezeTime, match="pasted@1"):
        forward.read(reg(repo))
    with pytest.raises(forward.MissingFreezeTime):
        forward.freeze(reg(repo), row(repo, "r@2"), T0 + timedelta(hours=1))


def test_a_malformed_frozen_at_is_refused(repo: Path) -> None:
    ledger._append(reg(repo), {**row(repo), "frozen_at": "2026-11-19 12:00"})
    with pytest.raises(forward.MissingFreezeTime):
        forward.read(reg(repo))
    reg(repo).write_text("")
    ledger._append(reg(repo), {**row(repo), "frozen_at": None})
    with pytest.raises(forward.MissingFreezeTime):
        forward.read(reg(repo))


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


def test_a_back_dated_side_branch_counts_from_its_merge(repo: Path) -> None:
    # A side branch from the old base, committed with an old date, then merged into main: the
    # line counts from the merge on main's first-parent chain, not from the side commit's date.
    base = git(repo, "rev-parse", "HEAD")
    (repo / "other.txt").write_text("main moves on\n")
    commit(repo, T0 + timedelta(days=40))
    git(repo, "checkout", "-q", "-b", "side", base)
    forward.freeze(reg(repo), row(repo), T0 - timedelta(hours=1))
    commit(repo, T0 - timedelta(hours=1))  # back-dated, just after its base
    git(repo, "checkout", "-q", "main")
    merged = T0 + timedelta(days=41)
    git(repo, "merge", "-q", "--no-ff", "-m", "m", "side", when=merged)
    assert forward.freeze_times(reg(repo))["r@1"] == merged


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


# --- observation files are append-only ---


def obs_file(repo: Path, rule_id: str = "r@1") -> Path:
    return repo / "research/forward/obs" / f"{rule_id}.jsonl"


def write_obs(path: Path, r: dict[str, Any], starts: list[datetime], values: list[float]) -> None:
    for o in obs(r, starts, values):
        ledger._append(
            path,
            {
                "start": ledger.iso(o.start),
                "end": ledger.iso(o.end),
                "value": o.value,
                "rule_hash": o.rule_hash,
            },
        )


def test_appending_observations_passes(repo: Path) -> None:
    r, frozen = committed(repo)
    path = obs_file(repo)
    assert forward.read_obs(path) == []  # no file yet
    start = frozen + timedelta(days=1)
    write_obs(path, r, days(start, 3), [1.0, -1.0, 1.0])
    commit(repo, T0 + timedelta(days=7))
    write_obs(path, r, days(start + timedelta(days=6), 2), [1.0, 1.0])  # uncommitted append
    assert len(forward.read_obs(path)) == 5
    commit(repo, T0 + timedelta(days=14))
    got = forward.read_obs(path)
    assert [o.value for o in got] == [1.0, -1.0, 1.0, 1.0, 1.0]
    assert forward.score(r, frozen, got).n == 5


def test_an_edited_committed_observation_is_refused(repo: Path) -> None:
    r, frozen = committed(repo)
    path = obs_file(repo)
    write_obs(path, r, days(frozen + timedelta(days=1), 3), [1.0, -1.0, 1.0])
    commit(repo, T0 + timedelta(days=7))
    path.write_text(path.read_text().replace('"value":-1.0', '"value":1.0'))  # a loss turned win
    with pytest.raises(ledger.LedgerTampered):
        forward.read_obs(path)
    commit(repo, T0 + timedelta(days=8))  # committing the edit does not launder it
    with pytest.raises(ledger.LedgerTampered):
        forward.read_obs(path)


def test_a_removed_committed_observation_is_refused(repo: Path) -> None:
    r, frozen = committed(repo)
    path = obs_file(repo)
    write_obs(path, r, days(frozen + timedelta(days=1), 3), [1.0, -1.0, 1.0])
    commit(repo, T0 + timedelta(days=7))
    lines = path.read_text().splitlines(keepends=True)
    path.write_text(lines[0] + lines[2])  # the loss dropped
    with pytest.raises(ledger.LedgerTampered):
        forward.read_obs(path)
    path.unlink()  # the whole file deleted
    with pytest.raises(ledger.LedgerTampered):
        forward.read_obs(path)


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
    with pytest.raises(forward.MissingFreezeTime):  # a proposal is not a registry
        forward.read(CANDIDATES)


def test_table_lists_each_rule() -> None:
    rows = [json.loads(x) for x in CANDIDATES.read_text().splitlines() if x.strip()]
    out = forward.table(rows)
    assert all(f"`{r['id']}`" in out for r in rows)


# --- the dependence-robust standard error (DECISIONS 2026-11-25, forward-se-1) ---


def lcg_normals(n: int, seed: int) -> list[float]:
    """Deterministic approximately normal values (sum of 12 uniforms from a fixed LCG)."""
    x, out = seed, []
    for _ in range(n):
        s = 0.0
        for _ in range(12):
            x = (1103515245 * x + 12345) % 2**31
            s += x / 2**31
        out.append(s - 6)
    return out


def ar1(e: list[float], phi: float) -> list[float]:
    out, prev = [], 0.0
    for v in e:
        prev = phi * prev + v
        out.append(prev)
    return out


def iid_t(values: list[float]) -> float:
    n = len(values)
    m = sum(values) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in values) / (n - 1))
    return m / (sd / math.sqrt(n))


def test_the_lag_rule_is_one_year_of_observations_capped_at_a_quarter_of_the_window() -> None:
    assert forward.lag(520, 52) == 51
    assert forward.lag(5200, 52) == 51
    assert forward.lag(625, 8) == 7
    assert forward.lag(100, 52) == 25  # n / 4 cap
    assert forward.lag(1000, 1.6) == 1
    assert forward.lag(1000, 1) == 0


def test_t_distribution_matches_known_values() -> None:
    assert forward.t_ppf(0.975, 9) == pytest.approx(2.2622, abs=1e-4)
    assert forward.t_ppf(0.95, 1) == pytest.approx(6.3138, abs=1e-4)
    assert forward.t_sf(0.0, 4) == pytest.approx(0.5)
    assert forward.t_sf(2.0, 3) == pytest.approx(0.069663, abs=1e-6)
    assert forward.t_sf(-1.2, 7) == pytest.approx(1 - forward.t_sf(1.2, 7))
    assert forward.t_sf(1.96, 1e8) == pytest.approx(0.025, abs=1e-4)


def test_fixed_b_critical_value_matches_kiefer_vogelsang() -> None:
    """Kiefer and Vogelsang (2005) Bartlett 97.5% critical value 1.96 + 2.9694 b + 0.4160 b^2
    - 0.5324 b^3: within 1% at b = 0.1 and 0.01; with no lags, the t quantile."""
    for n in (520, 5200):
        b = 51 / n
        kv = 1.96 + 2.9694 * b + 0.4160 * b**2 - 0.5324 * b**3
        assert forward.critical(n, 52, 0.025) == pytest.approx(kv, rel=0.01)
    assert forward.critical(30, 1, 0.025) == pytest.approx(forward.t_ppf(0.975, 29))


def test_on_iid_data_the_verdict_is_the_old_one() -> None:
    """Independent values: the HAC statistic is the iid t within a few per cent and the p-value
    within 0.01 of the old normal-approximation p."""
    for seed in (1, 2, 3):
        x = [v + 0.08 for v in lcg_normals(5200, seed)]
        t, p = forward.hac_t(x, 52)  # type: ignore[misc]
        old_t = iid_t(x)
        assert t == pytest.approx(old_t, rel=0.08)
        assert p == pytest.approx(1 - forward._N.cdf(old_t), abs=0.01)
    x = lcg_normals(400, 7)
    t0, p0 = forward.hac_t(x, 1)  # type: ignore[misc]
    assert t0 == pytest.approx(iid_t(x))  # no lags: exactly the t-test
    assert p0 == pytest.approx(forward.t_sf(iid_t(x), 399))


def test_dependent_data_get_a_wider_standard_error() -> None:
    """AR(1) phi 0.5 (long-run variance 4 times the variance) and 52-week blocks of a shared
    level: the HAC standard error is wider than the iid one, by about the theory's factor."""
    x = ar1(lcg_normals(5200, 11), 0.5)
    t, _ = forward.hac_t(x, 52)  # type: ignore[misc]
    ratio = iid_t(x) / t  # = SE_hac / SE_iid
    assert 1.5 < ratio < 2.0  # sqrt((1 + phi) / (1 - phi)) = 1.73; Bartlett at 51 lags 1.71
    levels = lcg_normals(100, 12)
    noise = lcg_normals(5200, 13)
    blocks = [levels[i // 52] * 0.3 + noise[i] for i in range(5200)]
    tb, _ = forward.hac_t(blocks, 52)  # type: ignore[misc]
    assert iid_t(blocks) / tb > 1.5  # lrv about 1 + 52 * 0.09 = 5.7 times the variance
    # the same data read as a monthly series (11 lags) see less of the dependence
    tm, _ = forward.hac_t(blocks, 12)  # type: ignore[misc]
    assert abs(tm) > abs(tb)


def test_a_dependent_record_that_the_iid_test_passes_can_fail(repo: Path) -> None:
    """The score itself uses the robust p: a positive-drift AR(1) record whose iid p is below
    alpha but whose HAC p is not gets "fail"."""
    plan = forward.Plan("mean", effect=0.1, per_year=52, alpha=0.025, sd=1.0)
    forward.freeze(reg(repo), row(repo, "m@1", plan), T0)
    commit(repo, T0 + timedelta(minutes=5))
    r = forward.read(reg(repo))[0]
    frozen = forward.freeze_times(reg(repo))["m@1"]
    need = r["min_sample"]
    x = [v + 0.11 for v in ar1(lcg_normals(need, 21), 0.6)]
    assert 1 - forward._N.cdf(iid_t(x)) < 0.025  # the old verdict would pass
    s = forward.score(r, frozen, obs(r, days(T0 + timedelta(days=1), need), x))
    assert s.p is not None and s.p > 0.025 and s.verdict == "fail"


def test_lrv_scales_the_sample_and_is_recorded() -> None:
    base = forward.Plan("sharpe", effect=1.0, per_year=52)
    wide = forward.Plan("sharpe", effect=1.0, per_year=52, lrv=2.0)
    n1, n2 = forward.min_sample(base), forward.min_sample(wide)
    assert 1.7 < n2 / n1 < 2.0  # twice the variance, less fixed-b penalty at the larger n
    with pytest.raises(ValueError):
        forward.Plan("sharpe", effect=1.0, per_year=52, lrv=0.8)
    e = forward.entry(
        "x@1", code={"a.py": "0"}, code_ref="HEAD", params={}, data={}, plan=wide, source="t"
    )
    assert e["lrv"] == 2.0 and e["se"] == forward.SE_RULE and e["min_sample"] == n2
    assert forward.plan_of({k: v for k, v in e.items() if k != "lrv"}).lrv == 1.0  # old lines
