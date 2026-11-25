"""stale-checks-1: loaders, Working's formula, the year-older signal and the lagged nulls."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "stalechecks1.py"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    spec = importlib.util.spec_from_file_location("stalechecks1_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_working_formula(m: ModuleType) -> None:
    assert m.working_rho(1) == 0.0
    assert m.working_rho(25) == pytest.approx(624 / 2502)
    assert m.working_rho(10_000) == pytest.approx(0.25, abs=1e-6)


def test_simulated_rho_matches_working_for_the_mean_and_zero_for_the_close(m: ModuleType) -> None:
    mean, mid, last = m.sim_rho(40_000, steps=25, seed=1)
    assert mean == pytest.approx(m.working_rho(25), abs=0.02)
    assert abs(last) < 0.02
    assert mid > 0.1  # the high-low midrange is smoothed too


def test_schwert_loader(m: ModuleType, tmp_path: Path) -> None:
    p = tmp_path / "s.csv"
    p.write_text("year,month,index\n1885,2,1.05773\n1914,12,6.53305\n")
    assert m.load_schwert(p) == {m.ym(1885, 2): 1.05773, m.ym(1914, 12): 6.53305}


def test_shiller_total_return_adds_a_twelfth_of_the_dividend(m: ModuleType) -> None:
    mon = {(1885, 2): (10.0, 1.2), (1885, 3): (11.0, 1.2)}
    lev = m.shiller_tr(mon, m.ym(1885, 2), m.ym(1885, 3))
    assert lev[m.ym(1885, 3)] == pytest.approx((11.0 + 0.1) / 10.0)


def test_window_drops_the_1914_closure(m: ModuleType) -> None:
    lev = {m.ym(1914, k): 1.0 for k in range(1, 13)}
    out = m.window(lev)
    assert sorted(out) == [m.ym(1914, k) for k in (1, 2, 3, 4, 5, 6, 7, 12)]


def _seg(m: ModuleType, pos: list[float]) -> Any:
    n = len(pos)
    return m.ins.Seg(
        "AAA", list(range(1900, 1901 + n)), np.full(n, 0.05), np.zeros(n), np.zeros(n),
        np.array(pos),
    )  # fmt: skip


def test_trimmed_lag2_uses_the_signal_a_year_older(m: ModuleType) -> None:
    s = _seg(m, [1.0, 0.0, 1.0, 1.0, 0.0])  # pos[i]: signal of year years[i+1] - 1
    l1, l2 = m.trimmed([s], 1)[0], m.trimmed([s], 2)[0]
    assert l1.years == l2.years == s.years[1:]
    assert list(l1.pos) == [0.0, 1.0, 1.0, 0.0]
    assert list(l2.pos) == [1.0, 0.0, 1.0, 1.0]  # the year before's position
    assert len(l2.r) == len(l2.pos) == len(l2.years) - 1


def test_lagged_null_runs_and_is_deterministic(m: ModuleType) -> None:
    rng = np.random.default_rng(3)
    x = np.cumsum(rng.normal(0.0, 0.08, 240))
    lev = {m.ym(1880, 1) + i: float(math.exp(v)) for i, v in enumerate(x)}
    st = m.one_period("t", lev, "test")
    g1 = m.null_gaps(lev, st, "ar1", 1, 4, 0)
    g2 = m.null_gaps(lev, st, "ar1", 1, 4, 0)
    assert g1.shape == (4,)
    np.testing.assert_array_equal(g1, g2)
    gb = m.null_gaps(lev, st, "bb", 0, 3, 0)
    assert gb.shape == (3,)


def test_readings_follow_the_card(m: ModuleType) -> None:
    assert m.reading_a(0.12).startswith("averaging inflates")
    assert m.reading_a(-0.03).startswith("no measurable")
    assert m.reading_a(0.07).startswith("small")


@pytest.fixture(scope="module")
def ocr() -> ModuleType:
    p = ROOT / "research" / "lib" / "stalechecks1_ocr.py"
    spec = importlib.util.spec_from_file_location("stalechecks1_ocr_under_test", p)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_ocr_tokens_get_their_decimal_point(ocr: ModuleType) -> None:
    assert ocr.norm("1.27T19", None) is None  # a letter inside: not 6 digits after cleaning
    assert ocr.norm("211315", 2.05) == pytest.approx(2.11315)
    assert ocr.norm("108301", 10.4414) == pytest.approx(10.8301)  # 4 decimals above 10
    assert ocr.norm("10.1598", 9.7) == pytest.approx(10.1598)
    assert ocr.norm("72", 2.9) is None


def test_vote_flags_disagreement_and_large_moves(ocr: ModuleType) -> None:
    years = range(ocr.FIRST, ocr.LAST + 1)
    good = {y: [["1.00000", "1.00000"]] * 12 for y in years}
    pages = [{y: ["1.00000"] * 12 for y in years} for _ in range(3)]
    pages[0][1914] = ["1.00000"] * 8
    res, flags = ocr.vote(good, pages)
    assert flags == []
    assert res[1914][7:11] == [None] * 4
    bad = {y: [list(c) for c in r] for y, r in good.items()}
    bad[1900][0] = ["1.20000", "1.20000"]  # +18% move, and only 2 of 5 readings
    _, flags = ocr.vote(bad, pages)
    assert (1900, 1) in flags


def test_corrections_cover_the_lanes_flagged_cells(ocr: ModuleType) -> None:
    fix = ocr.corrections()
    assert len(fix) == 74
    assert fix[(1919, 1)] == pytest.approx(9.73197)
    assert all(ocr.FIRST <= y <= ocr.LAST and 1 <= mo <= 12 for y, mo in fix)
    assert not any(k in ocr.CLOSED for k in fix)


def test_main_fails_clearly_without_the_transcription(
    m: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GRIMSTRADE_DATA", str(tmp_path))
    with pytest.raises(SystemExit, match="stalechecks1_ocr.py"):
        m.main([])
