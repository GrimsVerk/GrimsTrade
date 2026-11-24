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
    few, many = (report.deflate([good, short], report.Trials(n)) for n in (2, 200))
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


TRIES_REAL = """# Tries

- `period`: `train` or `heldout`.
- `kind`: `variant`, `baseline`, `robustness`.

| UTC time | Idea | Variant | Kind | Period | From | To | Sharpe | Return | Max DD | Turnover/yr |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 11-12T01:00 | kelly | full | variant | train | 2020 | 2023 | 0.9 | 1 | 1 | 1 |

| 11-12T01:05 | kelly | half | variant | train | 2020 | 2023 | 0.5 | 1 | 1 | 1 |
| 11-12T01:06 | kelly | half | variant | heldout | 2024 | 2025 | -2.0 | 1 | 1 | 1 |
| 11-12T01:07 | kelly | buy-hold | baseline | train | 2020 | 2023 | 3.0 | 1 | 1 | 1 |
"""

IDEAS_REAL = """# Ideas

Status: `new`, `testing`, `live`, `dead`.

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| kelly | sizing | dead | k.md | costs |
| hmm | regimes | rejected: costs | h.md | |
| tda | topology | killed | t.md | |
| lstm | ml | new | | |
"""


def _research(tmp_path: Path, tries: str = TRIES_REAL, ideas: str = IDEAS_REAL) -> None:
    (tmp_path / "research").mkdir(exist_ok=True)
    (tmp_path / "research" / "tries.md").write_text(tries)
    (tmp_path / "research" / "ideas.md").write_text(ideas)


def test_research_tries_on_the_real_file_layout(tmp_path: Path) -> None:
    _research(tmp_path)
    # Variants (kelly full, half, buy-hold; a blank line inside the table loses none, bullets are
    # not tries) plus tested ideas without a logged variant (hmm, tda; any status but `new`).
    assert ledger.research_tries(tmp_path) == 3 + 2


def test_research_tries_reads_main_too(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q", "-b", "main")
    _research(tmp_path)
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "research merged")
    git(tmp_path, "checkout", "-qb", "m1")
    git(tmp_path, "rm", "-rq", "research")
    git(tmp_path, "commit", "-qm", "a branch without research/")
    assert ledger.research_tries(tmp_path) == 5


def test_recorded_research_tries_survive_a_deleted_branch(tmp_path: Path) -> None:
    repo, root = tmp_path / "repo", tmp_path / "trail"
    repo.mkdir()
    _research(repo)
    assert ledger.total_tries(root, repo) == 5
    assert not (root / ledger.RESEARCH_FLOOR).exists()  # counting is read-only
    now = datetime(2026, 11, 12, 22, 30, tzinfo=UTC)
    assert ledger.record_research(root, repo, now) == 6  # kelly is in both files: counted once
    assert ledger.record_research(root, repo, now) == 0
    # The branch is deleted; another logs different tries. Both sets count.
    other = TRIES_REAL.replace("kelly", "carry")
    _research(repo, tries=other, ideas="")
    assert ledger.research_tries(repo) == 3
    assert ledger.research_tries(repo, root) == 5 + 3
    assert sorted(ledger.research_sharpes(repo, root)) == [0.5, 0.5, 0.9, 0.9]
    ledger.record_research(root, repo, now)
    assert ledger.check_append_only(root / ledger.RESEARCH_FLOOR) == 0


def _branch_with_tries(
    repo: Path, branch: str, tries: str, path: str = "research/tries.md"
) -> None:
    """Commit `tries` at `path` on a new branch `branch` off main, then go back to main."""
    git(repo, "checkout", "-q", "main")
    git(repo, "checkout", "-qb", branch)
    (repo / path).parent.mkdir(parents=True, exist_ok=True)
    (repo / path).write_text(tries)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", f"tries on {branch}")
    git(repo, "checkout", "-q", "main")


def _table(*rows: str) -> str:
    head = "| UTC time | Idea | Variant | Kind | Period | From | To | Sharpe |\n"
    head += "|---|---|---|---|---|---|---|---:|\n"
    return head + "".join(
        f"| 2026-11-14 01:00 | {r} | variant | train | 2020 | 2023 | 0.7 |\n" for r in rows
    )


def test_research_tries_read_every_branch_whatever_its_name(tmp_path: Path) -> None:
    """dsr-1 (2026-11-18): the count read only `main` and `research-*` branches, so lanes named
    `carry-2`, `eu-4`, ... after 2026-11-13 were never counted (307 tries seen, 2,811 logged)."""
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "start")
    _branch_with_tries(tmp_path, "carry-2", _table("carry | band", "carry | flat"))
    # A lane pushed by another machine: only its remote-tracking branch is here.
    _branch_with_tries(tmp_path, "eu-4", _table("eu | top3"))
    git(tmp_path, "update-ref", "refs/remotes/origin/eu-4", "eu-4")
    git(tmp_path, "branch", "-qD", "eu-4")
    git(tmp_path, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/eu-4")
    assert not (tmp_path / "research").exists()  # main's working tree has no research/
    assert ledger.research_tries(tmp_path) == 3
    assert sorted(ledger.research_sharpes(tmp_path)) == [0.7, 0.7, 0.7]


def test_a_branch_with_a_non_utf8_tries_file_does_not_stop_the_count(tmp_path: Path) -> None:
    """Every branch is read, so one stray byte on any of them must not stop the daily run."""
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "start")
    _branch_with_tries(tmp_path, "carry-2", _table("carry | band"))
    git(tmp_path, "checkout", "-q", "-b", "stray", "main")
    (tmp_path / "research").mkdir(exist_ok=True)
    (tmp_path / "research" / "tries.md").write_bytes(b"\xff\xfe not utf-8\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "stray")
    git(tmp_path, "checkout", "-q", "main")
    assert ledger.research_tries(tmp_path) == 1


def test_the_record_branch_is_not_a_research_branch(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "start")
    _branch_with_tries(tmp_path, "paper-trail", _table("planted | x"))
    git(tmp_path, "update-ref", "refs/remotes/origin/paper-trail", "paper-trail")
    assert ledger.research_refs(tmp_path) == ["refs/heads/main"]
    assert ledger.research_tries(tmp_path) == 0


def test_the_committed_register_counts_its_tries(tmp_path: Path) -> None:
    """`research/register/tries.jsonl` (written by `grimstrade.register`) keeps tries whose
    branch is gone; the count reads it like a tries table, on every branch."""
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "start")

    def line(variant: str, kind: str, sharpe: str) -> str:
        return (
            f'{{"idea": "gone", "variant": "{variant}", "kind": "{kind}", "period": "train", '
            f'"sharpe": {sharpe}}}'
        )

    register = "\n".join(
        [
            line("a", "variant", "0.4"),
            line("a", "variant", "0.4"),
            line("b", "robustness", "9"),
            line("c", "variant", "null"),
            "not json",
            "[1, 2]",
        ]
    )
    _branch_with_tries(tmp_path, "register-1", register + "\n", ledger.RESEARCH_REGISTER)
    assert ledger.research_tries(tmp_path) == 3  # a, b, c: the same (idea, variant) once
    assert ledger.research_sharpes(tmp_path) == [0.4]  # train variants only, as for tables


def test_research_sharpes_are_train_variants_only(tmp_path: Path) -> None:
    _research(tmp_path)
    assert sorted(ledger.research_sharpes(tmp_path)) == [0.5, 0.9]


def test_non_finite_research_sharpes_are_ignored(tmp_path: Path) -> None:
    tries = TRIES_REAL.replace("| 0.9 |", "| inf |").replace("| 0.5 |", "| nan |")
    _research(tmp_path, tries=tries)
    assert ledger.research_sharpes(tmp_path) == []
    assert ledger.research_tries(tmp_path) == 5


def test_research_sharpes_widen_the_luck_benchmark() -> None:
    good = report.score("good", equity_result([0.004, -0.002] * 100))
    alone = report.deflate([good], report.Trials(50))[0].dsr
    spread = report.deflate([good], report.Trials(50, (-3.0, 0.0, 3.0)))[0].dsr
    assert alone is not None and spread is not None and spread < alone
