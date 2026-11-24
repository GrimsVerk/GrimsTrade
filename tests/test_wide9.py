"""The wide-9 functions compute what research/wide-9.md says they do."""

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
        return importlib.import_module("wide9_events")
    finally:
        sys.path.remove(str(LIB))


def _daily(start: date, end: date) -> list[date]:
    out, d = [], start
    while d <= end:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def test_season_end_and_parse_oni() -> None:
    ev = _ev()
    assert ev.season_end("DJF", 1950) == (1950, 2)
    assert ev.season_end("OND", 1950) == (1950, 12)
    assert ev.season_end("NDJ", 1950) == (1951, 1)
    text = " SEAS  YR   TOTAL   ANOM\n  DJF 1950  25.01  -1.32\n  NDJ 2015  29.00   2.60\n"
    assert ev.parse_oni(text) == {(1950, 2): -1.32, (2016, 1): 2.6}


def test_dose_uses_season_ending_the_month_before_and_shifts_years() -> None:
    ev = _ev()
    oni = {(2016, 2): 2.5, (2014, 2): 0.1, (2015, 12): 2.4}
    assert ev.dose(oni, (2016, 3)) == 2.5  # end of March uses DJF
    assert ev.dose(oni, (2016, 1)) == 2.4  # end of January uses OND of the year before
    assert ev.dose(oni, (2016, 3), 2) == 0.1
    assert math.isnan(ev.dose(oni, (2016, 4)))


def test_horizon_return_month_ends_and_train_cut() -> None:
    ev = _ev()
    days = _daily(date(2020, 1, 1), date(2021, 3, 31))
    logc = np.arange(len(days), dtype=float)
    i, j = days.index(date(2020, 1, 31)), days.index(date(2020, 7, 31))
    assert ev.horizon_return(days, logc, (2020, 1), 6, date(2021, 3, 31)) == j - i
    assert math.isnan(ev.horizon_return(days, logc, (2020, 1), 6, date(2020, 7, 30)))
    assert math.isnan(ev.horizon_return(days, logc, (2020, 12), 6, date(2025, 1, 1)))
    gap = [d for d in days if (d.year, d.month) != (2020, 7)]
    assert math.isnan(ev.horizon_return(gap, np.zeros(len(gap)), (2020, 1), 6, date(2022, 1, 1)))


def test_months_rank_bins_and_spread() -> None:
    ev = _ev()
    assert ev.months((2013, 11), (2014, 2)) == [(2013, 11), (2013, 12), (2014, 1), (2014, 2)]
    assert ev.rank_highest(2.0, [1.0, 3.0, 2.0]) == 2
    got = [
        [name for name, lo, hi in ev.ONI_BINS if ev.in_bin(x, lo, hi)]
        for x in (-1.0, -0.5, 0.0, 0.5, 1.0)
    ]
    assert got == [
        ["x <= -1.0"],
        ["-1.0 < x <= -0.5"],
        ["-0.5 < x < 0.5"],
        ["0.5 <= x < 1.0"],
        ["x >= 1.0"],
    ]
    sd, share = ev.null_spread([-3.0, -1.0, 1.0, 3.0])
    assert abs(sd - np.std([-3, -1, 1, 3], ddof=1)) < 1e-12 and share == 0.5


def test_fork_list_and_legs() -> None:
    ev = _ev()
    assert len(ev.FORKS) == 15 and sum(s for _, _, s in ev.FORKS) == 5
    assert all(d <= date(2025, 11, 10) for _, d, _ in ev.FORKS)
    d0 = date(2022, 9, 15)
    e = {d0 + timedelta(days=k): 0.01 * k for k in range(-30, 30)}
    pre, post = ev.legs(e, d0)
    assert abs(pre - 0.10) < 1e-12 and abs(post - 0.10) < 1e-12  # E(d-1)-E(d-11), E(d+9)-E(d-1)
    del e[d0 + timedelta(days=9)]
    assert ev.legs(e, d0) is None


def test_one_sample_t_and_slope() -> None:
    ev = _ev()
    m, t = ev.one_sample_t([1.0, 2.0, 3.0])
    assert m == 2.0 and abs(t - 2.0 / (1.0 / math.sqrt(3))) < 1e-12
    assert math.isnan(ev.one_sample_t([1.0])[1])
    assert abs(ev.ols_slope([0, 0, 1, 1], [1.0, 3.0, 5.0, 7.0]) - 4.0) < 1e-12
    assert math.isnan(ev.ols_slope([1, 1], [1.0, 2.0]))
