"""Offline tests of wide-26's pure functions (W43 `drought-food-margin`)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "lib"))
import wide26_events as ev  # type: ignore[import-not-found]  # noqa: E402

BLOCK = """header line
  Average Value Weighted Returns -- Monthly
,Agric,Food ,Meals
196001,   1.00,  -99.99,   3.00
196002,   2.00,   4.00,   5.00
196003,   0.50,   1.50,   2.50

  Average Equal Weighted Returns -- Monthly
,Agric,Food ,Meals
196001,   9.00,   9.00,   9.00
"""

FACTORS = """This file was created by ...
,Mkt-RF,SMB,HML,RF
196001,   -6.98,    2.09,    2.78,    0.33
196002,    1.16,    0.51,   -1.99,    0.29

 Annual Factors: January-December
,Mkt-RF,SMB,HML,RF
  1960,   -1.00,    0.00,    0.00,    2.00
"""


def test_parse_block_reads_one_block_and_marks_missing() -> None:
    names, rows = ev.parse_block(BLOCK, "Average Value Weighted Returns -- Monthly", 10**9)
    assert names == ["Agric", "Food", "Meals"]
    jan = ev.yyyymm_index("196001")
    assert sorted(rows) == [jan, jan + 1, jan + 2]
    assert math.isnan(rows[jan][1]) and rows[jan + 1] == [2.0, 4.0, 5.0]


def test_parse_block_cuts_after_last() -> None:
    jan = ev.yyyymm_index("196001")
    _, rows = ev.parse_block(BLOCK, "Average Value Weighted Returns -- Monthly", jan + 1)
    assert sorted(rows) == [jan, jan + 1]


def test_parse_factors_monthly_only() -> None:
    f = ev.parse_factors(FACTORS, 10**9)
    jan = ev.yyyymm_index("196001")
    assert f == {jan: (-6.98, 0.33), jan + 1: (1.16, 0.29)}


def test_beta_recovers_slope_and_needs_full_window() -> None:
    rng = np.random.default_rng(0)
    mkt = {m: float(v) for m, v in enumerate(rng.normal(0, 4, 100))}
    ex = {m: 0.5 + 0.7 * mkt[m] for m in mkt}
    assert ev.beta(ex, mkt, 80) == pytest.approx(0.7)
    assert math.isnan(ev.beta(ex, mkt, 30))  # needs months -29 .. 30
    gap = dict(ex)
    del gap[50]
    assert math.isnan(ev.beta(gap, mkt, 80))


def test_outcome_window_starts_two_months_after_the_dose() -> None:
    mkt = {m: 1.0 if m % 2 else -1.0 for m in range(200)}
    ex = {m: 2.0 * mkt[m] + (10.0 if m in (102, 103, 104) else 0.0) for m in range(200)}
    # beta ends at m+1 = 101, before the bump: exactly 2
    assert ev.outcome(ex, mkt, 100) == pytest.approx(30.0)
    assert ev.outcome(ex, mkt, 100, adjust="none") == pytest.approx(30.0 + 2 * (-1 + 1 - 1))
    assert ev.outcome(ex, mkt, 100, adjust="raw") == pytest.approx(30.0 + (-1 + 1 - 1))
    assert math.isnan(ev.outcome(ex, mkt, 198))


def test_shift_dose_moves_later() -> None:
    d = {10: 1.0, 11: 2.0}
    assert ev.shift_dose(d, 13) == {23: 1.0, 24: 2.0}
    assert ev.shift_dose(d, -13) == {-3: 1.0, -2: 2.0}


def test_drying_and_acf() -> None:
    p = {m: float(-m) for m in range(10)}
    assert ev.drying(p) == {m: 3.0 for m in range(3, 10)}
    ar = {m: float(v) for m, v in enumerate(np.cumsum(np.ones(50)))}
    assert ev.acf1(ar) > 0.9
    alt = {m: (1.0 if m % 2 else -1.0) for m in range(50)}
    assert ev.acf1(alt) < -0.9


def test_regress_finds_a_planted_slope() -> None:
    rng = np.random.default_rng(1)
    months = list(range(600))
    dose = {m: float(v) for m, v in zip(months, rng.normal(0, 2, 600), strict=True)}
    y = {m: -0.5 * dose[m] + float(rng.normal(0, 1)) for m in months}
    b, t, n = ev.regress(months, y, dose, 3)
    assert n == 600 and b == pytest.approx(-0.5, abs=0.05) and t < -10


def test_rank_and_spread() -> None:
    assert ev.rank_lowest(-3.0, [-1.0, 0.0, 2.0]) == 1
    assert ev.rank_lowest(0.5, [-1.0, 0.0, 2.0]) == 3
    sd, share, *_ = ev.null_spread([-2.5, 0.0, 2.5, math.nan])
    assert share == pytest.approx(2 / 3) and sd == pytest.approx(2.5)


def _o(s: str) -> int:
    from datetime import date

    return date.fromisoformat(s).toordinal()


def test_knockout_events_first_loss_shootout_and_group_exit() -> None:
    t = "FIFA World Cup"
    m = [
        (_o("2018-06-14"), "A", "B", 1, 0, t),
        (_o("2018-06-19"), "A", "C", 1, 1, t),
        (_o("2018-06-24"), "C", "A", 0, 2, t),
        (_o("2018-06-20"), "B", "D", 0, 1, t),
        (_o("2018-06-25"), "D", "B", 2, 2, t),
        (_o("2018-07-01"), "A", "E", 1, 1, t),  # A wins on penalties: 4th match
        (_o("2018-07-06"), "A", "F", 0, 2, t),  # A loses QF: elimination
        (_o("2018-07-14"), "A", "G", 0, 1, t),  # third-place match: not a second event
        (_o("2018-07-01"), "X", "Y", 3, 0, "Friendly"),
    ]
    so = {(_o("2018-07-01"), "A", "E"): "A"}
    ev_ = ev.knockout_events(m, so)
    a = [(k, n) for team, _, k, n, _ in ev_ if team == "A"]
    assert a == [("win", 4), ("elim", 5)]
    b = [(k, n) for team, _, k, n, _ in ev_ if team == "B"]
    assert b == [("group", 3)]
    assert not any(team == "X" for team, *_ in ev_)


def test_next_session_dose_lands_after_the_match_day() -> None:
    dates = np.array([_o("2018-07-05"), _o("2018-07-06"), _o("2018-07-09")])
    # Friday match -> Monday session; Thursday match -> Friday session
    d = ev.next_session_dose(dates, [(_o("2018-07-06"), 1.0), (_o("2018-07-05"), 2.0)])
    assert list(d) == [0.0, 2.0, 1.0]
    assert list(ev.next_session_dose(dates, [(_o("2018-07-09"), 1.0)])) == [0.0, 0.0, 0.0]
    assert list(ev.next_session_dose(dates, [(_o("2018-07-03"), 1.0)], shift=1)) == [1.0, 0, 0]


def test_session_rows_subtract_the_world() -> None:
    dates = np.arange(100, 110)
    logc = np.log(np.arange(1.0, 11.0))
    other = (dates.copy(), np.zeros(10) + 0.01 * np.arange(10))
    s, y, raw, per = ev.session_rows(dates, logc, [other], 100, 109)
    assert list(s) == list(range(1, 10))
    assert raw[0] == pytest.approx(math.log(2.0))
    assert y[0] == pytest.approx(math.log(2.0) - 0.01)
    s2, _, raw2, _ = ev.session_rows(dates, logc, [other], 100, 109, after=1)
    assert list(s2) == list(range(1, 9)) and raw2[0] == pytest.approx(math.log(3.0))
