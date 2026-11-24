"""The wide-20 functions compute what research/cards/wide-20.md says they do."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide20_events")
    finally:
        sys.path.remove(str(LIB))


def test_forty_placebo_shifts_both_ways_never_zero() -> None:
    ev = _ev()
    assert len(ev.SHIFTS) == 40 and 0 not in ev.SHIFTS
    assert sorted(ev.SHIFTS) == [*range(-20, 0), *range(1, 21)]
    assert ev.STEP_DAYS % 7 != 0


def test_parse_events_keeps_day_precision_earliest_date_and_largest_toll() -> None:
    ev = _ev()
    text = (
        "item,date,precision,deaths\n"
        "Q1,2010-05-12T00:00:00Z,11,100\n"
        "Q1,2010-05-11T00:00:00Z,11,90\n"  # same item: earliest date, largest toll
        "Q2,2011-01-01T00:00:00Z,9,300\n"  # year precision: dropped
        "Q3,2012-03-04T00:00:00Z,11,40\n"  # under 50 deaths: dropped
        "Q4,not-a-date,11,80\n"  # bad date: skipped
        "Q5,2013-07-06T00:00:00Z,11,50\n"
    )
    assert ev.parse_events(text) == [(date(2010, 5, 11), 100.0), (date(2013, 7, 6), 50.0)]


def test_dose_lands_on_first_bar_on_or_after_the_accident_and_the_next() -> None:
    ev = _ev()
    bars = [date(2024, 1, d) for d in (5, 8, 9, 10)]  # Fri, Mon, Tue, Wed
    x = ev.dose(bars, [(date(2024, 1, 6), 100.0)])  # Saturday accident: Monday is day 0
    assert np.allclose(x, [0, 2, 2, 0])  # log2(100 / 25) = 2
    xb = ev.dose(bars, [(date(2024, 1, 6), 100.0)], days=(2, 3, 4), binary=True)
    assert np.allclose(xb, [0, 0, 0, 1])  # past the last bar is ignored
    x2 = ev.dose(bars, [(date(2024, 1, 5), 50.0), (date(2024, 1, 8), 50.0)])
    assert np.allclose(x2, [1, 2, 1, 0])  # overlapping events add


def test_shift_wraps_inside_the_window_and_keeps_tolls() -> None:
    ev = _ev()
    lo, hi = date(2008, 1, 1), date(2008, 3, 1)
    n = ev.span(lo, hi)
    assert n == (date(2008, 2, 29) - lo).days
    e = [(date(2008, 2, 20), 70.0)]
    got = ev.shift(e, 1, lo, hi)
    assert got == [(lo + timedelta(days=((date(2008, 2, 20) - lo).days + 23) % n), 70.0)]
    assert all(
        lo <= d < lo + timedelta(days=n) for k in ev.SHIFTS for d, _ in ev.shift(e, k, lo, hi)
    )


def test_window_drops_events_too_late_for_day_one() -> None:
    ev = _ev()
    es = [(date(2025, 10, 29), 60.0), (date(2025, 10, 30), 60.0), (date(2007, 12, 31), 60.0)]
    assert ev.in_window(es, date(2008, 1, 1), date(2025, 10, 31)) == [es[0]]


def test_ols_hc1_recovers_slope_and_rank_counts_ties_against() -> None:
    ev = _ev()
    x = np.array([0.0, 1, 0, 2, 0, 1, 0, 3])
    y = 0.5 - 0.2 * x + np.array([0.01, -0.02, 0.03, 0.0, -0.01, 0.02, -0.03, 0.01])
    b, t, n = ev.ols_hc1(x, y)
    assert n == 8 and abs(b + 0.2) < 0.02 and t < -5
    assert ev.rank_lowest(-2.0, [-3.0, -2.0, 1.0]) == 3
    sd, share, _, med, _ = ev.null_spread([-2.5, 0.0, 2.5])
    assert math.isclose(sd, 2.5) and math.isclose(share, 2 / 3) and med == 0.0
