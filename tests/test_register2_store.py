"""register-7 (card: the addendum of research/register-4.md): `research/register2.py` reads its
harness from a commit, not a named branch; the returns store only grows and holds one series
per try (re-runs are not added, a new live code version is a new series, `estimate` uses one
per live strategy); robustness-only curves are not stored by default; the budget never drops a
stored row."""

from __future__ import annotations

import importlib.util
import json
import math
import subprocess
import sys
from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from grimstrade import returnstore

ROOT = Path(__file__).resolve().parents[1]
START = date(2012, 1, 2)


@pytest.fixture
def r2() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    spec = importlib.util.spec_from_file_location("register2", ROOT / "research" / "register2.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    try:
        spec.loader.exec_module(mod)
        yield mod
    finally:
        sys.modules.pop(spec.name, None)


def series(r2: ModuleType, source: str, idea: str, variant: str, drift: float) -> Any:
    days = [START + timedelta(days=k) for k in range(400)]
    eq = [(d, 100 * (1 + drift) ** k * (1 + 0.01 * math.sin(k))) for k, d in enumerate(days)]
    return r2.series_of(source, idea, variant, eq)


def reg(ident: str, s: Any, kind: str, sharpe: float | None = None) -> dict[str, Any]:
    return {
        "id": ident, "idea": s.idea, "variant": s.variant, "kind": kind, "period": "train",
        "from": s.start, "sharpe": round(s.sharpe, 2) if sharpe is None else sharpe,
    }  # fmt: skip


def test_a_live_rerun_of_a_stored_code_version_is_not_added(r2: ModuleType) -> None:
    a = "live@code-aaaaaaaaaaaa-sim-111111111111"
    b = "live@code-bbbbbbbbbbbb-sim-111111111111"
    stored = [r2.to_row(series(r2, a, "live", "ts_momentum", 0.0004))]
    drift = r2.to_row(series(r2, a, "live", "ts_momentum", 0.00041))  # other prices, same code
    new_code = r2.to_row(series(r2, b, "live", "ts_momentum", 0.00039))
    skipped: dict[str, int] = {}
    got = r2.to_store([drift, new_code], [], stored, skipped=skipped)
    assert got == [new_code]  # the new version is a new series; the stored one stays
    assert skipped == {"live re-runs of a stored code version": 1}


def test_estimate_counts_each_live_strategy_once(
    r2: ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    old, a, b = "live@0123456789ab", "live@code-a-sim-s", "live@code-b-sim-s"

    def s(src: str, name: str) -> Any:
        return series(r2, src, "live", name, 0.0004)

    lives = [s(old, "x"), s(a, "x"), s(b, "x"), s(old, "y"), s(a, "y"), s(old, "z")]
    lives += [s(a, "w"), s(b, "w")]
    picked = r2.pick_live(lives, {"x": b, "y": b, "z": b, "w": "live@code-c-sim-s", "v": b})
    # x: the current code's version; y: the versioned one beats the pre-register-7 tag;
    # z: its only series; w: two versions, neither current, so none; v: nothing stored.
    assert [(p.variant, p.source) for p in picked] == [("x", b), ("y", a), ("z", old)]
    err = capsys.readouterr().err
    assert "not of the current code (2): y, z" in err
    assert "none current (1): w" in err
    assert "no stored series (1): v" in err
    one = [s(old, "x")]
    assert r2.pick_live(one, {"x": old}) == one  # the store as committed: unchanged


def test_live_tags_follow_the_strategy_code_and_the_simulator(r2: ModuleType) -> None:
    from grimstrade import run_daily
    from grimstrade.strategies import LIVE

    tags = r2.live_tags()
    assert set(tags) == set(LIVE)
    sim = r2.sim_hash()
    for name, tag in tags.items():
        assert tag == f"live@code-{run_daily.fingerprint(LIVE[name])}-sim-{sim}"
        assert r2.kind(tag) == "live"


def test_a_baseline_rerun_is_added_only_for_a_row_without_a_series(r2: ModuleType) -> None:
    base = series(r2, "harness@aaa", "baselines", "ew", 0.0003)
    rows = [reg("b-1", base, "baseline")]
    stored = [r2.to_row(base)]
    drift = series(r2, "harness@bbb", "baselines", "ew", 0.000301)  # other commit, same row
    assert r2.fit_ids(drift, r2._by_key(rows)) == ["b-1"]
    skipped: dict[str, int] = {}
    assert r2.to_store([r2.to_row(drift)], rows, stored, skipped=skipped) == []
    assert skipped == {"baseline re-runs": 1}
    changed = series(r2, "harness@bbb", "baselines", "ew", 0.0006)  # a changed harness...
    rows.append(reg("b-2", changed, "baseline"))  # ...logged a new baseline row
    assert r2.to_store([r2.to_row(changed)], rows, stored) == [r2.to_row(changed)]
    first = series(r2, "harness@bbb", "baselines", "sma", 0.0002)  # never stored: added
    assert r2.to_store([r2.to_row(first)], rows, stored) == [r2.to_row(first)]


def test_robustness_only_curves_are_not_stored_by_default(r2: ModuleType) -> None:
    rob = series(r2, "curve", "trend", "rob", 0.0004)
    both = series(r2, "curve", "trend", "both", 0.0003)
    stray = series(r2, "curve", "trend", "stray", 0.0002)
    rows = [
        reg("r-1", rob, "robustness"),
        reg("r-2", both, "robustness"),
        reg("v-1", both, "variant"),
        reg("s-1", stray, "variant", sharpe=9.99),
    ]
    local = [r2.to_row(x) for x in (rob, both, stray)]
    skipped: dict[str, int] = {}
    assert [r.variant for r in r2.to_store(local, rows, skipped=skipped)] == ["both"]
    assert skipped == {"robustness-only curves": 1, "curves that fit no register row": 1}
    assert [r.variant for r in r2.to_store(local, rows, robustness=True)] == ["both", "rob"]


def test_export_over_the_budget_keeps_every_stored_row(
    r2: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store, work, register = tmp_path / "returns", tmp_path / "work", tmp_path / "tries.jsonl"
    monkeypatch.setattr(r2, "STORE", store)
    monkeypatch.setattr(r2, "WORK", work)
    monkeypatch.setattr(r2, "REGISTER", register)
    old = series(r2, "curve", "trend", "old", 0.0001)  # stored, fits only a control row
    sel = series(r2, "curve", "trend", "sel", 0.0004)
    ctl = series(r2, "curve", "trend", "ctl", 0.0003)
    rows = [reg("o-1", old, "control"), reg("s-1", sel, "variant"), reg("c-1", ctl, "control")]
    register.write_text("".join(json.dumps(x) + "\n" for x in rows))
    returnstore.write(store, [r2.to_row(old)])
    r2.save(work / "curves.jsonl", [sel, ctl])
    monkeypatch.setattr(returnstore, "BUDGET", 1)  # everything is over it
    r2.export()
    assert sorted(r.variant for r in returnstore.read(store)) == ["old", "sel"]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
        cwd=repo, check=True, capture_output=True, text=True,
    ).stdout  # fmt: skip


def test_tree_reads_a_commit_and_survives_a_deleted_branch(
    r2: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "repo"
    (repo / "research" / "lib").mkdir(parents=True)
    (repo / "src").mkdir()
    (repo / "src" / "m.py").write_text("x = 1\n")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "no harness")
    bare = git(repo, "rev-parse", "HEAD").strip()
    (repo / "research" / "lib" / "baselines.py").write_text("IDEA = 'baselines'\n")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "harness")
    sha = git(repo, "rev-parse", "HEAD").strip()
    git(repo, "branch", "summary-x")
    monkeypatch.setattr(r2, "ROOT", repo)
    monkeypatch.setattr(r2, "WORK", repo / "research" / "data" / "register2")
    assert r2.commit_of("summary-x") == sha
    git(repo, "branch", "-D", "summary-x")
    with pytest.raises(SystemExit, match="not a commit"):
        r2.commit_of("summary-x")
    with pytest.raises(SystemExit, match="no research/lib/baselines.py"):
        r2.commit_of(bare)
    out = r2.tree()  # default: HEAD, this checkout
    assert out.name == sha[:12]
    assert (out / "research" / "lib" / "baselines.py").read_text() == "IDEA = 'baselines'\n"
    assert r2.tree(sha) == out
