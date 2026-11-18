"""The project-wide tries register (`grimstrade.register`): every try on every pushed branch,
counted once, kept when its branch goes, and the bar a new pick must clear."""

import math
import subprocess
from pathlib import Path
from statistics import NormalDist

import pytest

from grimstrade import ledger, register, stats

HEAD = (
    "# Tries\n\n- `kind`: `variant`, `baseline`, ...\n\n"
    "| UTC time | Idea | Variant | Kind | Period | From | To | Sharpe | Return |\n"
    "|---|---|---|---|---|---|---|---:|---:|\n"
)
A = "| 2026-11-13 01:00 | trend | tsmom12 | baseline | train | 1994-02-01 | 2025-11-09 | 1.05 | 9 |"
B = "| 2026-11-13 02:00 | trend | tsmom6 | variant | train | 1994-02-01 | 2025-11-09 | 0.95 | 8 |"
C = "| 2026-11-14 01:00 | carry | band | variant | train | 2021-02-20 | 2025-11-09 | 0.79 | 3 |"
D = "| 2026-11-14 02:00 | carry | band | variant | heldout | 2025-01-01 | 2025-11-09 | -0.65 | 1 |"
E = "| 2026-11-15 01:00 | planted | signal | control | train | 1994-02-01 | 2025-11-09 | 2.0 | 1 |"
F = "| 2026-11-15 02:00 | screen | forecast | screen | train | 2000-01-01 | 2020-12-31 | - | - |"
G = "| 2026-11-15 03:00 | broken |"
PLANTED = "| 2026-11-16 01:00 | planted | x | variant | train | 2000-01-01 | 2020-12-31 | 5.0 | 1 |"
LOCAL = "| 2026-11-16 02:00 | local | y | variant | train | 2000-01-01 | 2020-12-31 | 0.1 | 1 |"


def git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def push(repo: Path, branch: str, files: dict[str, str], remote: bool = True) -> None:
    """Commit `files` on top of main and file the commit as origin's `branch` (as a fetch
    would), or as a local branch only."""
    git(repo, "checkout", "-q", "--detach", "main")
    for rel, text in files.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", branch)
    git(repo, "update-ref", f"refs/{'remotes/origin' if remote else 'heads'}/{branch}", "HEAD")
    git(repo, "checkout", "-q", "main")


def tries_md(*rows: str) -> dict[str, str]:
    return {"research/tries.md": HEAD + "".join(r + "\n" for r in rows)}


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "commit", "-q", "--allow-empty", "-m", "start")
    push(tmp_path, "main", tries_md(A, B))
    push(tmp_path, "carry-2", tries_md(A, B, C, C, D))  # C was logged twice: a re-run
    push(tmp_path, "screen-1", tries_md(A, C, E, F, G))  # shares A and one C through history
    trail = {"ledger/tries.jsonl": '{"name":"a"}\n{"name":"b"}\n\n{"name":"c"}\n'}
    push(tmp_path, "paper-trail", {**trail, **tries_md(PLANTED)})
    push(tmp_path, "local-1", tries_md(LOCAL), remote=False)  # not pushed: not in the register
    git(tmp_path, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
    return tmp_path


def test_every_pushed_try_is_counted_once(repo: Path) -> None:
    s = register.regenerate(repo)
    # A, B, C twice, D, E, F. Not G (no Sharpe column), the record's or the unpushed one.
    assert s.tries == 7
    assert s.families == 4
    assert s.selectable == 4  # A, B, C, C: variants or baselines on train data
    assert s.without_sharpe == 1
    assert s.live == 3
    assert s.n == 7
    assert s.branches == 3
    lines = (repo / register.REGISTER).read_text().splitlines()
    assert len(lines) == 7
    ids = [ln.split('"id":"')[1].split('"')[0] for ln in lines]
    assert sum(i.endswith("-2") for i in ids) == 1  # C's second occurrence
    bar = (repo / register.BAR).read_text()
    assert "| **N for a new pick** (selectable + live) | **7** |" in bar
    assert "| Distinct tries, project-wide (`research/register/tries.jsonl`) | **7** |" in bar


def test_regenerating_is_stable(repo: Path) -> None:
    register.regenerate(repo)
    first = (repo / register.REGISTER).read_bytes(), (repo / register.BAR).read_bytes()
    register.regenerate(repo)
    assert ((repo / register.REGISTER).read_bytes(), (repo / register.BAR).read_bytes()) == first


def test_a_deleted_branch_keeps_its_tries(repo: Path) -> None:
    register.regenerate(repo)
    git(repo, "update-ref", "-d", "refs/remotes/origin/carry-2")
    s = register.regenerate(repo)
    assert s.tries == 7 and s.selectable == 4  # D and the second C live only in the register
    # The register committed on a branch counts too, even with no copy on disk.
    push(repo, "register-1", {str(register.REGISTER): (repo / register.REGISTER).read_text()})
    assert not (repo / register.REGISTER).exists()  # committed there, gone from main's tree
    assert register.regenerate(repo).tries == 7


def test_a_hand_edited_register_line_is_refused(repo: Path) -> None:
    register.regenerate(repo)
    path = repo / register.REGISTER
    path.write_text(path.read_text().replace('"sharpe":0.79', '"sharpe":1.79', 1))
    with pytest.raises(register.RegisterError, match="does not match"):
        register.regenerate(repo)
    path.write_text("not json\n")
    with pytest.raises(register.RegisterError, match="not a register line"):
        register.regenerate(repo)


def test_the_scoreboard_counts_the_register(repo: Path) -> None:
    register.regenerate(repo)
    for branch in ("carry-2", "screen-1"):
        git(repo, "update-ref", "-d", f"refs/remotes/origin/{branch}")
    # Distinct (idea, variant): trend tsmom12 and tsmom6, carry band, planted signal, screen
    # forecast from the register on disk, plus the unpushed local branch's row.
    assert ledger.research_tries(repo) == 6
    assert sorted(ledger.research_sharpes(repo)) == [0.1, 0.79, 0.95]


def test_the_bar_matches_dsr_1() -> None:
    """dsr-1 (research/dsr-1.md): 947 selectable tries; as 96 independent ones (rho 0.9) a new
    rule needs z >= 4.2, +0.27 Sharpe close to `tsmom12` and +0.50 far; all independent
    +0.32 / +0.59."""
    s = register.Summary(7, 1, [], 0, 936, 11, "-", 1, None, None, [])
    assert s.n == 947
    by = {b.label: b for b in s.bar()}
    assert by["rho 0.9"].n == pytest.approx(95.6)
    assert by["rho 0.9"].z_dsr == pytest.approx(4.2, abs=0.05)
    assert by["rho 0.9"].z_dsr * register.SE_CLOSE == pytest.approx(0.27, abs=0.005)
    assert by["rho 0.9"].z_dsr * register.SE_FAR == pytest.approx(0.50, abs=0.005)
    assert by["independent"].z_dsr * register.SE_CLOSE == pytest.approx(0.32, abs=0.005)
    assert by["independent"].z_dsr * register.SE_FAR == pytest.approx(0.59, abs=0.005)
    assert by["independent"].p_bonferroni == pytest.approx(0.05 / 947)
    assert NormalDist().cdf(by["independent"].z_bonferroni) == pytest.approx(1 - 0.05 / 947)
    # The same E[max Z] as the scoreboard's deflated Sharpe.
    assert register.max_z(100) == pytest.approx(stats.expected_max_sharpe(100, 1.0))


def test_the_sharpe_needed_against_zero_passes_exactly() -> None:
    days, v, n = 3_653, 0.1, 50.0
    need = register.sharpe_needed(n, v, days) / math.sqrt(365)
    sr0 = math.sqrt(v / 365) * register.max_z(n)
    psr = stats.probabilistic_sharpe(stats.Moments(days, need, 0.0, 3.0), sr0)
    assert psr == pytest.approx(0.95, abs=1e-6)
