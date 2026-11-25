"""The wide-24 functions compute what research/cards/wide-24.md says they do."""

from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide24_events")
    finally:
        sys.path.remove(str(LIB))


def test_forty_shifts_both_ways_in_steps_of_23_days() -> None:
    ev = _ev()
    assert len(ev.SHIFTS) == 40
    assert 0 not in ev.SHIFTS
    assert sorted(ev.SHIFTS) == [23 * k for k in range(-20, 21) if k != 0]


def test_radius_follows_the_card() -> None:
    ev = _ev()
    assert math.isclose(ev.radius_km(6.5), 40.0)
    assert 66 < ev.radius_km(7.0) < 68
    assert 520 < ev.radius_km(9.0) < 540


def test_exposure_counts_places_within_the_hypocentral_radius() -> None:
    ev = _ev()
    e = ev.Event(0.0, 0.0, 0.0, 30.0, 6.5)  # R = 40 km, depth 30 km
    lat = np.array([0.0, 0.2, 2.0])  # 0 km, about 22 km, about 222 km
    lon = np.zeros(3)
    pop = np.array([100.0, 100.0, 800.0])
    # hypocentral: 30 km and sqrt(22^2 + 30^2) = 37 km inside, 222 km outside
    assert math.isclose(ev.exposure(e, lat, lon, pop), 20.0)
    deep = ev.Event(0.0, 0.0, 0.0, 45.0, 6.5)
    assert math.isclose(ev.exposure(deep, lat, lon, pop), 0.0)
    assert math.isclose(ev.exposure(e, lat, lon, pop, radius=300.0), 100.0)


def test_weight_is_log2_of_one_plus_share_and_binary_at_one_percent() -> None:
    ev = _ev()
    assert math.isclose(ev.weight(1.0), 1.0)
    assert math.isclose(ev.weight(3.0), 2.0)
    assert ev.weight(0.99, binary=True) == 0.0
    assert ev.weight(1.0, binary=True) == 1.0


def test_select_and_decluster() -> None:
    ev = _ev()
    day = 86400.0
    a = ev.Event(0.0, 0.0, 0.0, 10.0, 7.0)
    after = ev.Event(5 * day, 1.0, 0.0, 10.0, 6.5)  # 111 km, 5 days later, smaller: aftershock
    far = ev.Event(6 * day, 10.0, 0.0, 10.0, 6.5)  # 1,112 km: kept
    late = ev.Event(40 * day, 0.5, 0.0, 10.0, 6.2)  # 40 days later: kept
    bigger = ev.Event(7 * day, 0.5, 0.0, 10.0, 7.5)  # larger than a: kept
    deep = ev.Event(8 * day, 20.0, 0.0, 100.0, 7.0)
    small = ev.Event(9 * day, 30.0, 0.0, 10.0, 5.9)
    sel = ev.select([late, a, after, far, bigger, deep, small], -1.0, 100 * day)
    assert deep not in sel and small not in sel
    kept = ev.decluster(sel)
    assert after not in kept
    assert a in kept and far in kept and late in kept and bigger in kept


def test_dose_lands_on_first_session_on_or_after_the_day_and_shifts() -> None:
    ev = _ev()
    dates = np.array([10, 11, 14, 15])
    d = ev.dose(4, dates, [(12, 2.0), (11, 1.0), (30, 5.0), (5, 7.0)])
    assert list(d) == [0.0, 1.0, 2.0, 0.0]
    d2 = ev.dose(4, dates, [(12, 2.0)], shift=3)
    assert list(d2) == [0.0, 0.0, 0.0, 2.0]


def test_world_change_uses_last_close_and_stale_limit() -> None:
    ev = _ev()
    dj = np.array([1, 2, 3, 20])
    lj = np.log(np.array([100.0, 110.0, 121.0, 50.0]))
    w = ev.world_change(np.array([2, 2]), np.array([3, 19]), [(dj, lj)])
    assert math.isclose(w[0], math.log(1.1))
    assert math.isnan(w[1])  # last close on or before day 19 is day 3: stale


def test_rows_outcome_is_own_window_minus_world_and_controls_end_before() -> None:
    ev = _ev()
    n = 40
    dates = np.arange(100, 100 + n)
    logc = np.log(np.linspace(100.0, 140.0, n))
    other = (dates.copy(), np.zeros(n))  # flat world
    r = ev.rows(dates, logc, [other], 100, 100 + n, h=5)
    s = int(r.s[0])
    assert s == 21
    assert math.isclose(r.y[0], logc[s + 6] - logc[s + 1])
    assert math.isclose(r.r2[0], logc[s + 1] - logc[s - 1])
    assert math.isclose(r.r20[0], logc[s - 1] - logc[s - 21])
    assert int(r.period[0]) == int(dates[s + 1])
    assert int(r.s[-1]) + 1 + 5 <= n - 1


def test_rank_and_acf() -> None:
    ev = _ev()
    assert ev.rank_lowest(-3.0, [-1.0, 0.0, 2.0]) == 1
    assert ev.rank_lowest(0.5, [-1.0, 0.0, 2.0]) == 3
    x = np.array([1.0, -1.0] * 10)
    assert ev.acf1([x]) < -0.9
