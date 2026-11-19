"""The wide-13 functions compute what research/wide-13.md steps 2 and 3 say they do."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide13_events")
    finally:
        sys.path.remove(str(LIB))


def test_shifts_are_forty_odd_and_never_a_year() -> None:
    s = _ev().SHIFTS
    assert len(s) == 40 and len(set(s)) == 40
    assert all(27 <= abs(k) <= 103 and k % 2 != 0 and k % 52 != 0 for k in s)


def test_mondays_and_fridays() -> None:
    ev = _ev()
    m = ev.mondays(date(2026, 11, 1), date(2026, 11, 30))
    assert m == [date(2026, 11, d) for d in (2, 9, 16, 23, 30)]
    f = ev.fridays(date(2026, 11, 6), date(2026, 11, 20))
    assert f == [date(2026, 11, 6), date(2026, 11, 13), date(2026, 11, 20)]


def test_weekly_log_mean_uses_the_seven_days_ending_monday() -> None:
    ev = _ev()
    m = date(2026, 11, 16)  # a Monday
    daily = {m - timedelta(days=i): 7.0 * (i == 0) for i in range(7)}  # only Monday is 7
    daily[m - timedelta(days=7)] = 1000.0  # the Monday before: outside the window
    out = ev.weekly_log_mean(daily, [m, m - timedelta(days=7)])
    assert math.isclose(out[m], math.log(2.0))  # ln(1 + 7/7)
    assert m - timedelta(days=7) not in out  # its week has missing days


def test_failure_dose_weeks_assets_and_cutoff() -> None:
    ev = _ev()
    weeks = ev.fridays(date(2026, 1, 2), date(2026, 1, 30))
    fails = [
        (date(2026, 1, 9), 2_000.0),  # Friday, 2 million USD
        (date(2026, 1, 10), 3_000.0),  # Saturday: belongs to the week ending 16 January
        (date(2026, 1, 16), math.nan),  # unknown assets count 0
        (date(2026, 1, 23), 9_999_000.0),  # after `last`: never read
    ]
    x = ev.failure_dose(fails, weeks, last=date(2026, 1, 20))
    assert math.isclose(x[date(2026, 1, 9)], math.log1p(2.0))
    assert math.isclose(x[date(2026, 1, 16)], math.log1p(3.0))
    assert x[date(2026, 1, 2)] == 0.0
    assert date(2026, 1, 23) not in x  # week after `last` has no dose at all


def test_shifted_reads_the_dose_k_weeks_earlier() -> None:
    ev = _ev()
    d = {date(2026, 1, 2): 1.5}
    assert ev.shifted(d, date(2026, 1, 2) + timedelta(days=7 * 27), 27) == 1.5
    assert math.isnan(ev.shifted(d, date(2026, 1, 2), 27))


def test_window_return_clock_and_slack() -> None:
    ev = _ev()
    m = date(2026, 1, 5)  # Monday
    bars = {m + timedelta(days=9): 100.0, m + timedelta(days=37): 110.0}
    px = ev.Closes(bars)
    last = date(2026, 12, 31)
    assert math.isclose(ev.window_return(px, m, 9, 37, 7, last), math.log(1.1))
    # entry is the first bar on or after M + 9, never an earlier one
    px2 = ev.Closes({m + timedelta(days=8): 50.0, **bars})
    assert math.isclose(ev.window_return(px2, m, 9, 37, 7, last), math.log(1.1))
    # exit bar more than 7 days late, or after the last train bar: dropped
    late = ev.Closes({m + timedelta(days=9): 100.0, m + timedelta(days=45): 1.0})
    assert math.isnan(ev.window_return(late, m, 9, 37, 7, last))
    assert math.isnan(ev.window_return(px, m, 9, 37, 7, m + timedelta(days=30)))


def test_reaction_and_past_returns() -> None:
    ev = _ev()
    f = date(2026, 1, 9)  # Friday
    px = ev.Closes({f - timedelta(days=28): 80.0, f: 100.0, f + timedelta(days=3): 90.0})
    last = date(2026, 12, 31)
    assert math.isclose(ev.reaction_return(px, f, 3, last), math.log(0.9))
    assert math.isclose(ev.past_return(px, f, 28), math.log(100 / 80))
    assert math.isnan(ev.past_return(px, f, 364))  # no bar a year back
