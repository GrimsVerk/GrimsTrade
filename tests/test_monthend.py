"""The month-end-bonds rule (research/lib/monthend_rules.py) does what its card says: held for
the last four sessions of a month (bought after the close of T-4, sold after the close of T),
and never when the month's end is not yet in the calendar."""

from __future__ import annotations

import importlib
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _rules() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("monthend_rules")
    finally:
        sys.path.remove(str(LIB))


def _weekdays(start: date, n: int) -> list[date]:
    out: list[date] = []
    d = start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def test_held_for_exactly_the_last_four_sessions() -> None:
    r = _rules()
    cal = _weekdays(date(2024, 1, 1), 70)  # January to early April 2024
    t = max(i for i, d in enumerate(cal) if d.month == 2)  # last session of February
    assert [r.last_four(cal, t - k) for k in range(6)] == [True] * 4 + [False] * 2
    assert not r.last_four(cal, t + 1)
    # bought after the close of T-4, held through T, sold after the close of T
    assert [i for i in range(t - 8, t + 3) if r.holds_after(cal, i)] == [t - 4, t - 3, t - 2, t - 1]
    # four of every month's sessions, whatever the month's length
    feb = [i for i, d in enumerate(cal) if d.month == 2]
    assert sum(r.last_four(cal, i) for i in feb) == 4


def test_unknown_month_end_is_never_held() -> None:
    r = _rules()
    cal = _weekdays(date(2024, 1, 1), 70)
    assert not r.last_four(cal, len(cal) - 1)
    assert not r.holds_after(cal, len(cal) - 1) and not r.holds_after(cal, len(cal) - 2)
    # cutting the calendar later never changes an earlier answer that was True
    short = cal[:45]
    for i in range(len(short)):
        if r.last_four(short, i):
            assert r.last_four(cal, i)


def test_window_return_is_open_of_t_minus_3_to_open_of_next_month() -> None:
    r = _rules()
    cal = _weekdays(date(2024, 1, 1), 70)
    opens = [100.0]
    for i in range(len(cal) - 1):  # the session from open i to open i+1 earns 1% in the window
        opens.append(opens[-1] * (1.01 if r.last_four(cal, i) else 1.0))
    ev = r.window_returns(cal, opens)
    assert [d.month for d, _ in ev] == [1, 2, 3]
    assert all(np.isclose(x, 1.01**4 - 1) for _, x in ev)
