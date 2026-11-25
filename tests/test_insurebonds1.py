"""insure-bonds-1: yield-to-total-return rebuilds, loaders, splice runs, threshold ladder, AAFT."""

from __future__ import annotations

import importlib.util
import math
import sys
from datetime import date
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "insurebonds1.py"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    spec = importlib.util.spec_from_file_location("insurebonds1_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_par_bond_unchanged_yield_earns_about_the_coupon(m: ModuleType) -> None:
    # at an unchanged yield a par bond stays near par: the month's return is ~ y / 12
    r = m.par_return(6.0, 6.0)
    assert r == pytest.approx(0.06 / 12, abs=2e-4)


def test_par_bond_loses_about_duration_times_the_yield_rise(m: ModuleType) -> None:
    r = m.par_return(5.0, 6.0)  # +1 point on a 10-year par bond: modified duration ~ 7.7
    assert -0.08 < r - 0.05 / 12 < -0.07


def test_perpetuity_return_is_price_change_plus_coupon(m: ModuleType) -> None:
    assert m.perp_return(4.0, 5.0) == pytest.approx(4 / 5 - 1 + 4 / 1200)
    assert m.price_return(4.0, 5.0) == pytest.approx(-0.2)


def test_total_return_levels_restart_after_a_missing_month(m: ModuleType) -> None:
    y = {m.ym(1900, 1): 4.0, m.ym(1900, 2): 4.0, m.ym(1900, 4): 5.0, m.ym(1900, 5): 5.0}
    lev = m.tr_levels(y, m.perp_return)
    assert lev[m.ym(1900, 1)] == 1.0
    assert lev[m.ym(1900, 2)] == pytest.approx(1 + 4 / 1200)
    assert lev[m.ym(1900, 4)] == 1.0  # new run: never bridged over the gap
    assert m.ym(1900, 3) not in lev


def test_wide_year_sheet_parser_keeps_window_and_skips_blanks(m: ModuleType) -> None:
    rows = [
        ["", "JAN", "FEB"],
        [1821.0, 5.0] + [5.0] * 11 + [5.0],
        [1822.0, None, 4.5, "4.6"] + [None] * 9 + [4.5],
        ["1985", 9.0],
    ]
    out = m.parse_wide_years(rows, m.ym(1822, 1), m.ym(1984, 12))
    assert out == {m.ym(1822, 2): 4.5, m.ym(1822, 3): 4.6}  # column 13 (annual) never read


def test_match_runs_labels_months_by_the_matching_source(m: ModuleType) -> None:
    a = {k: 1.0 + 0.01 * k for k in range(6)}
    b = {k: 2.0 + 0.03 * k * k for k in range(6)}
    sp = {k: (a[k] if k <= 2 else a[2] * b[k] / b[2]) for k in range(6)}
    runs = m.match_runs({"A": a, "B": b, "spliced": sp})
    assert runs == [("A", 1, 2), ("B", 3, 5)]


def test_threshold_ladder_picks_largest_rung_with_enough_falls(m: ModuleType) -> None:
    assert m.pick_threshold({0.25: 2, 0.20: 8, 0.15: 9, 0.10: 12}) == 0.20
    assert m.pick_threshold({0.25: 0, 0.20: 0, 0.15: 0, 0.10: 2}) == 0.10  # card default
    assert m.pick_threshold({0.10: 2, 0.075: 7, 0.05: 11}, m.LADDER_A) == 0.05
    assert m.neighbours(0.10) == [0.15]
    assert m.neighbours(0.20) == [0.25, 0.15]


def test_aaft_keeps_the_values_and_changes_the_order(m: ModuleType) -> None:
    rng = np.random.default_rng(0)
    x = rng.standard_t(3, 240) * 0.01
    s = m.aaft_path(np.random.default_rng(1), x)
    assert np.allclose(np.sort(s), np.sort(x))
    assert not np.allclose(s, x)


def test_world_gap_uses_the_given_threshold(m: ModuleType) -> None:
    # a smooth 3% fall and a 3% rise, twice, on a trending world: no 25% fall exists, but 2%
    # falls do; the gap must be finite at 2% and NaN (no fall) at 25%
    months = list(range(m.ym(1900, 1), m.ym(1900, 1) + 200))
    x = np.full(199, 0.004)
    x[80:90] = -0.003
    x[150:160] = -0.003
    raw = m.Raw("t", months, np.zeros(200, dtype=int), x)
    rng = np.random.default_rng(0)
    assert math.isnan(m.world_gap([raw], [x], rng, 0.25))
    assert math.isfinite(m.world_gap([raw], [x], np.random.default_rng(0), 0.02))


def test_float_noise_in_insurance_is_a_tie(m: ModuleType) -> None:
    # a world where the rule is in throughout a one-month fall: I must be exactly 0
    months = list(range(m.ym(1900, 1), m.ym(1900, 1) + 120))
    r = np.full(120, 0.003)
    r[0] = np.nan
    r[100] = -0.08  # one-month fall while the 12-month trend is up
    s = m.i17.build_seg("t", months, r)
    ev = m.evaluate("t", [s], 0.05, 0.05)
    assert [e.ins for e in ev.eps] == [0.0]
    assert ev.k == 0


def test_noise_in_rebound_and_cash_rate_net_is_zeroed(m: ModuleType) -> None:
    ep = m.i1.Episode("t", date(1900, 1, 31), date(1900, 2, 28), 0.05, -5.0, -5.0, 1.2e-14,
                      -2.8e-14, ins_tb=3e-15, net_tb=-1e-14)  # fmt: skip

    class _Ev:
        eps = [ep]

    orig = m.i17.evaluate
    try:
        m.i17.evaluate = lambda *a, **k: _Ev()
        ev = m.evaluate("t", [], 0.05, 0.05)
    finally:
        m.i17.evaluate = orig
    e = ev.eps[0]
    assert (e.ins, e.rebound, e.net, e.ins_tb, e.net_tb) == (0.0, 0.0, 0.0, 0.0, 0.0)
    assert m.i1.sign_test([e.net])[1] == 0  # a tie, dropped by the sign test
