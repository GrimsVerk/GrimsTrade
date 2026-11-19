"""The ann-1 event study measures the windows research/ann-1.md names, keyed by day 0."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date, datetime, time
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("ann1_event")
    finally:
        sys.path.remove(str(LIB))


def _series(ev: Any) -> Any:
    days = [date(2020, 1, d) for d in (6, 7, 8, 9, 10)]
    opens = np.array([100.0, 101.0, 102.0, 104.0, 108.0])
    closes = np.array([100.5, 101.5, 103.0, 106.0, 107.0])
    return ev.Series(days, opens, closes)


def test_windows_are_keyed_by_day_zero() -> None:
    ev = _ev()
    s = _series(ev)
    d0 = date(2020, 1, 8)  # index 2
    for kind, want in [
        ("cc0", 103.0 / 101.5 - 1),  # close day -1 -> close day 0
        ("cc-1", 101.5 / 100.5 - 1),  # close day -2 -> close day -1
        ("oo0", 104.0 / 102.0 - 1),  # open day 0 -> open day +1
        ("oo-1", 104.0 / 101.0 - 1),  # open day -1 -> open day +1
    ]:
        keys, vals = ev.window_returns(s, kind)
        assert math.isclose(vals[keys.index(d0)], want)


def test_windows_that_do_not_fit_are_left_out() -> None:
    ev = _ev()
    s = _series(ev)
    assert ev.window_returns(s, "cc-1")[0][0] == date(2020, 1, 8)
    assert ev.window_returns(s, "oo0")[0][-1] == date(2020, 1, 9)


def test_split_and_welch() -> None:
    ev = _ev()
    keys = [date(2020, 1, d) for d in range(1, 9)]
    vals = np.array([1.0, 3.0, 0.0, 0.0, 1.0, 1.0, 9.0, 9.0])
    events = {date(2020, 1, 1), date(2020, 1, 2), date(2020, 1, 8)}
    ev_vals, other = ev.split(keys, vals, events, date(2020, 1, 1), date(2020, 1, 6))
    assert ev_vals == [1.0, 3.0]
    assert other == [0.0, 0.0, 1.0, 1.0]
    st = ev.welch(ev_vals, other)
    se = math.sqrt(2.0 / 2 + (1 / 3) / 4)
    assert st.n == 2 and math.isclose(st.diff, 1.5) and math.isclose(st.t, 1.5 / se)


def test_price_before_uses_last_regular_bar_before_the_cut() -> None:
    ev = _ev()
    tz = ev.NY
    d = date(2020, 1, 8)
    bars = [
        (datetime.combine(d, time(9, 0), tz), 1.0),  # pre-market: ignored
        (datetime.combine(d, time(13, 53), tz), 2.0),
        (datetime.combine(d, time(13, 54), tz), 3.0),
        (datetime.combine(d, time(13, 55), tz), 4.0),  # starts at the cut: ignored
    ]
    assert ev.price_before(bars, d) == 3.0
    assert math.isnan(ev.price_before(bars, date(2020, 1, 9)))
