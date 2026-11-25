"""The wide-22 functions compute what research/cards/wide-22.md says they do."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide22_events")
    finally:
        sys.path.remove(str(LIB))


def test_forty_earlier_shifts_25_to_103_odd() -> None:
    ev = _ev()
    assert list(range(25, 104, 2)) == ev.SHIFTS
    assert len(ev.SHIFTS) == 40 and all(k > 0 for k in ev.SHIFTS)


def test_parse_mer_keeps_monthly_rows_of_one_series_up_to_the_cut() -> None:
    ev = _ev()
    text = (
        '"MSN","YYYYMM","Value","Column_Order","Description","Unit"\n'
        '"ESICPUS","197213","800.0","3","Industrial","Million Kilowatthours"\n'
        '"ESICPUS","197301","60.5","3","Industrial","Million Kilowatthours"\n'
        '"ESRCPUS","197301","40.0","1","Residential","Million Kilowatthours"\n'
        '"ESICPUS","197302","Not Available","3","Industrial","Million Kilowatthours"\n'
        '"ESICPUS","202510","70.0","3","Industrial","Million Kilowatthours"\n'
        '"ESICPUS","202511","71.0","3","Industrial","Million Kilowatthours"\n'
    )
    out = ev.parse_mer(text, "ESICPUS", date(2025, 10, 31))
    assert out == {1973 * 12: 60.5, 2025 * 12 + 9: 70.0}


def test_yoy_is_100_log_growth_on_the_same_month_a_year_earlier() -> None:
    ev = _ev()
    u = {0: 100.0, 1: 50.0, 12: 110.0, 14: 1.0}
    g = ev.yoy(u)
    assert set(g) == {12}
    assert math.isclose(g[12], 100 * math.log(1.1))


def test_parse_french_monthly_stops_before_the_annual_block() -> None:
    ev = _ev()
    lines = [
        "This file was created ...",
        ",Mkt-RF,SMB,HML,RF",
        "192607,    2.89,   -2.55,   -2.39,    0.22",
        "192608,    2.64,   -1.14,    3.81,    0.25",
        "202511,    1.00,    0.00,    0.00,    0.30",
        "",
        " Annual Factors: January-December ",
        ",Mkt-RF,SMB,HML,RF",
        "  1927,   29.47,   -2.46,   -3.75,    3.12",
        "192609,    9.99,    9.99,    9.99,    9.99",
    ]
    out = ev.parse_french_monthly(lines, date(2025, 10, 31))
    assert out == {1926 * 12 + 6: (2.89, 0.22), 1926 * 12 + 7: (2.64, 0.25)}


def test_shift_moves_the_dose_later_in_the_index_so_rows_get_an_earlier_dose() -> None:
    ev = _ev()
    d = {10: 1.0, 11: 2.0}
    s = ev.shifted(d, 25)
    assert s == {35: 1.0, 36: 2.0}  # row 35 gets the dose of month 10


def test_window_sum_ahead_and_trailing() -> None:
    ev = _ev()
    y = {m: float(m) for m in range(0, 30)}
    ahead = ev.window_sum(y, 3, 12)  # months m+3 .. m+14
    assert ahead[0] == sum(range(3, 15))
    assert max(ahead) == 15  # 15+14 = 29 is the last month
    trail = ev.window_sum(y, -9, 12)  # months m-9 .. m+2
    assert trail[9] == sum(range(0, 12))
    assert min(trail) == 9 and 8 not in trail


def test_phase_surrogates_keep_mean_and_spectrum_and_are_deterministic() -> None:
    ev = _ev()
    rng = np.random.default_rng(0)
    d = {100 + i: float(v) for i, v in enumerate(np.cumsum(rng.normal(size=64)))}
    d[500] = 9.0  # outside the longest run: ignored
    a = ev.phase_surrogates(d, n=3, seed=5)
    b = ev.phase_surrogates(d, n=3, seed=5)
    assert a == b and len(a) == 3
    x = np.array([d[m] for m in range(100, 164)])
    for s in a:
        assert sorted(s) == list(range(100, 164))
        v = np.array([s[m] for m in range(100, 164)])
        assert math.isclose(v.mean(), x.mean(), abs_tol=1e-9)
        assert np.allclose(np.abs(np.fft.rfft(v - v.mean())), np.abs(np.fft.rfft(x - x.mean())))
        assert not np.allclose(v, x)


def test_rank_lowest() -> None:
    ev = _ev()
    assert ev.rank_lowest(-3.0, [-1.0, 0.0, 2.0]) == 1
    assert ev.rank_lowest(0.5, [-1.0, 0.0, 2.0]) == 3
