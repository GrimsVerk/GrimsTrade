"""The survey-7 functions compute what research/survey-7.md says they do."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("survey7_events")
    finally:
        sys.path.remove(str(LIB))


def test_month_returns_use_last_bar_of_each_month() -> None:
    ev = _ev()
    days = [date(2020, 1, 30), date(2020, 1, 31), date(2020, 2, 14), date(2020, 2, 28)]
    r = ev.month_returns(days, [0.0, 1.0, 5.0, 1.5])
    assert r == {(2020, 2): 0.5}


def test_last_friday() -> None:
    ev = _ev()
    assert ev.last_friday((2025, 10)) == date(2025, 10, 31)  # a Friday
    assert ev.last_friday((2025, 11)) == date(2025, 11, 28)
    assert ev.last_friday((2024, 3)) == date(2024, 3, 29)


def test_friday_return_falls_back_to_earlier_bar_within_gap() -> None:
    ev = _ev()
    # Good Friday 2024-03-29: the March close comes from Thursday 28th
    days = [date(2024, 2, 23), date(2024, 3, 28), date(2024, 4, 1)]
    assert ev.friday_return(days, [1.0, 1.3, 9.0], (2024, 3)) == 1.3 - 1.0
    # a close more than five days before the Friday is missing
    assert math.isnan(ev.friday_return([date(2024, 2, 1), date(2024, 3, 28)], [0, 1], (2024, 3)))


def test_signal_averages_same_month_lags_and_needs_five_years() -> None:
    ev = _ev()
    mret = {(y, 6): float(y - 2000) for y in range(2000, 2020)}
    mret.update({(y, 7): 100.0 for y in range(2000, 2020)})
    v, used = ev.signal(mret, (2020, 6))
    assert used == 20 and v == sum(range(20)) / 20
    v, used = ev.signal(mret, (2020, 7), s=1)  # lags 13, 25, ...: Junes, not Julys
    assert used == 20 and v == sum(range(20)) / 20
    v, used = ev.signal(mret, (2020, 6), a=3)  # j = 4 .. 23: years 2016 .. 1997
    assert used == 17 and v == sum(range(17)) / 17
    short = {(y, 6): 1.0 for y in range(2016, 2020)}
    assert math.isnan(ev.signal(short, (2020, 6))[0])


def test_signal_sees_nothing_from_the_last_eleven_months() -> None:
    ev = _ev()
    base = {(y, m): 0.0 for y in range(1990, 2020) for m in range(1, 13)}
    late = dict(base)
    for k in range(1, 12):
        late[ev.add_months((2020, 6), -k)] = 99.0
    for s, a in [(0, 0), *ev.PLACEBOS]:
        assert ev.signal(base, (2020, 6), s, a) == ev.signal(late, (2020, 6), s, a)


def test_placebo_family_is_forty_off_cycle_shifts() -> None:
    ev = _ev()
    assert len(ev.PLACEBOS) == 40 and len(set(ev.PLACEBOS)) == 40
    assert all(1 <= s <= 10 and 0 <= a <= 3 for s, a in ev.PLACEBOS)


def test_spread_top_minus_bottom_fifth() -> None:
    ev = _ev()
    syms = [f"A{i:02d}" for i in range(10)]
    sig = {x: float(i) for i, x in enumerate(syms)}
    ret = {x: float(i) for i, x in enumerate(syms)}
    y, n = ev.spread(sig, ret)  # k = 2: (8 + 9) / 2 - (0 + 1) / 2
    assert n == 10 and y == 8.0
    ret["A09"] = math.nan  # drops out: n = 9, k = 2
    y, n = ev.spread(sig, ret)
    assert n == 9 and y == (7 + 8) / 2 - (0 + 1) / 2
    few = {x: sig[x] for x in syms[:5]}
    assert math.isnan(ev.spread(few, ret)[0])


def test_spread_breaks_ties_by_name() -> None:
    ev = _ev()
    sig = {x: 0.0 for x in "ABCDEF"}
    ret = {x: float(i) for i, x in enumerate("ABCDEF")}
    assert ev.spread(sig, ret) == (5.0 - 0.0, 6)


def test_mean_t_and_rank() -> None:
    ev = _ev()
    m, t, n = ev.mean_t([1.0, 2.0, 3.0, math.nan])
    assert (m, n) == (2.0, 3) and abs(t - 2.0 / (1.0 / math.sqrt(3))) < 1e-12
    assert ev.rank_highest(2.0, [1.0, 3.0, 2.0]) == 2
    nul = ev.null_summary([-2.0, 0.0, 2.5, 1.0])
    assert nul["share2"] == 0.5 and nul["min"] == -2.0 and nul["max"] == 2.5


def test_months_and_add_months() -> None:
    ev = _ev()
    assert ev.add_months((2020, 1), -1) == (2019, 12)
    assert ev.months((2019, 11), (2020, 2)) == [(2019, 11), (2019, 12), (2020, 1), (2020, 2)]
