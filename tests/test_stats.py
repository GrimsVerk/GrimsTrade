"""Deflated Sharpe and the count of strategies tried (the record's plus the research lane's)."""

import math
import subprocess
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from grimstrade import ledger, report, stats
from grimstrade.gym import Result
from grimstrade.stats import Moments


def test_matches_the_papers_worked_example() -> None:
    # Bailey & López de Prado 2014, section 4: annualised SR 2.5 over 5 years of daily returns,
    # skew -3, kurtosis 10, 100 trials whose annualised Sharpes have variance 0.5.
    var = 0.5 / 250
    assert stats.expected_max_sharpe(100, var) == pytest.approx(0.1132, abs=1e-4)
    m = Moments(1250, 2.5 / math.sqrt(250), -3, 10)
    assert stats.deflated_sharpe(m, 100, var) == pytest.approx(0.9004, abs=1e-4)


def test_more_tries_raise_the_bar() -> None:
    m = Moments(500, 0.08, 0.0, 3.0)
    one, ten, thousand = (stats.deflated_sharpe(m, n, 1 / 500) for n in (1, 10, 1000))
    assert one > ten > thousand
    assert stats.expected_max_sharpe(1, 1 / 500) == 0.0
    assert one == pytest.approx(stats.probabilistic_sharpe(m, 0.0))


def test_fat_left_tails_lower_confidence() -> None:
    normal = Moments(500, 0.08, 0.0, 3.0)
    crashy = Moments(500, 0.08, -2.0, 12.0)
    assert stats.probabilistic_sharpe(crashy, 0.0) < stats.probabilistic_sharpe(normal, 0.0)


def test_moments_of_a_symmetric_series() -> None:
    m = stats.moments([0.01, -0.01, 0.02, -0.02] * 10)
    assert m is not None
    assert m.sharpe == pytest.approx(0.0) and m.skew == pytest.approx(0.0)
    assert stats.moments([0.01] * 5) is None


def equity_result(daily: list[float]) -> Result:
    eq, e = [], 10_000.0
    d0 = date(2026, 1, 1)
    for i, r in enumerate([0.0, *daily]):
        e *= 1 + r
        eq.append((d0 + timedelta(days=i), e))
    return Result(cash=0, positions={}, equity=eq)


def test_deflate_needs_thirty_days_and_penalises_tries() -> None:
    good = report.score("good", equity_result([0.004, -0.002] * 100))
    short = report.score("short", equity_result([0.004, -0.002] * 10))
    few, many = report.deflate([good, short], 2), report.deflate([good, short], 200)
    assert few[1].dsr is None
    assert few[0].dsr is not None and many[0].dsr is not None
    assert few[0].dsr > many[0].dsr


# --- counting the research lane's tries ---


def git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


TRIES_V1 = """# Tries

| date | idea | variant | period |
|---|---|---|---|
| 2026-11-12 | kelly | half kelly | train |
| 2026-11-12 | kelly | half kelly | held-out |
| 2026-11-12 | hmm | 2 states | train |
"""


def test_research_tries_counts_distinct_variants_across_branches(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q", "-b", "main")
    assert ledger.research_tries(tmp_path) == 0
    (tmp_path / "research").mkdir()
    (tmp_path / "research" / "tries.md").write_text(TRIES_V1)
    # The held-out check of a variant is not a new try.
    assert ledger.research_tries(tmp_path) == 2
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "v1")
    git(tmp_path, "checkout", "-qb", "research-1")
    tries_v2 = TRIES_V1 + "| 2026-11-13 | tda | h1 | train |\n"
    (tmp_path / "research" / "tries.md").write_text(tries_v2)
    git(tmp_path, "commit", "-qam", "v2")
    git(tmp_path, "checkout", "-q", "main")
    # main's working tree has 2; the research-1 branch adds a third.
    assert ledger.research_tries(tmp_path) == 3


def test_research_ideas_count_when_tries_are_not_logged(tmp_path: Path) -> None:
    (tmp_path / "research").mkdir()
    (tmp_path / "research" / "ideas.md").write_text(
        "| idea | status |\n|---|---|\n| kelly | dead: costs |\n| hmm | testing |\n| tda | new |\n"
    )
    assert ledger.research_tries(tmp_path) == 2
    ledger.register_try(tmp_path, "x", "", datetime(2026, 11, 12, tzinfo=UTC))
    assert ledger.total_tries(tmp_path, tmp_path) == 3
