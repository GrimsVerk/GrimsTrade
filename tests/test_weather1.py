"""The weather-1 functions compute what research/weather-1.md says they do."""

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
        return importlib.import_module("weather1_events")
    finally:
        sys.path.remove(str(LIB))


def test_parse_cpc_reads_conus_and_drops_held_out_days() -> None:
    ev = _ev()
    text = (
        "Product: Daily Heating Degree Days\nRegions: x\nWeights: Utility Gas\n"
        "Region|20251108|20251109|20251110\n1|5|6|7\nCONUS|10|11|-999\n"
    )
    assert ev.parse_cpc(text) == {date(2025, 11, 8): 10.0, date(2025, 11, 9): 11.0}


def _flat(start: date, end: date, v: float) -> dict[date, float]:
    out, d = {}, start
    while d <= end:
        out[d] = v
        d += timedelta(days=1)
    return out


def test_normal_uses_only_the_20_previous_years() -> None:
    ev = _ev()
    hdd = _flat(date(1990, 1, 1), date(2010, 12, 31), 10.0)
    hdd.update(_flat(date(2010, 1, 1), date(2010, 12, 31), 99.0))  # same year: must not count
    assert ev.normal(hdd, date(2010, 1, 15)) == 10.0
    assert math.isnan(ev.normal(hdd, date(2009, 1, 15)))  # 1989 missing


def test_dose_sums_seven_days_to_friday() -> None:
    ev = _ev()
    hdd = _flat(date(1990, 1, 1), date(2010, 12, 31), 10.0)
    fri = date(2010, 1, 15)
    for k in range(7):
        hdd[fri - timedelta(days=k)] = 13.0
    assert ev.dose(hdd, fri, {}) == 21.0
    hdd[fri - timedelta(days=7)] = 50.0  # the Friday before: outside the window
    assert ev.dose(hdd, fri, {}) == 21.0


def test_entry_is_at_least_four_days_after_friday() -> None:
    ev = _ev()
    fri = date(2020, 1, 10)
    days = [
        fri + timedelta(days=k) for k in range(0, 30) if (fri + timedelta(days=k)).weekday() < 5
    ]
    i, j = ev.entry_exit(days, fri, date(2020, 12, 31))
    assert days[i] == date(2020, 1, 14) and j == i + 5
    assert ev.entry_exit(days, fri, date(2020, 1, 20)) is None


def test_season_and_placebo_friday() -> None:
    ev = _ev()
    fr = ev.season_fridays(2010, 2011)
    assert all(f.weekday() == 4 and f.month in (11, 12, 1, 2, 3) for f in fr)
    by: dict[int, list[date]] = {}
    for f in fr:
        by.setdefault(ev.winter_of(f), []).append(f)
    g = ev.placebo_friday(date(2010, 12, 3), 2011, by)
    assert g is not None and ev.winter_of(g) == 2011 and abs(ev.offset(g) - 32) <= 3


def test_derangements_have_no_fixed_point_and_are_distinct() -> None:
    ev = _ev()
    ps = ev.derangements(18, 40)
    assert len(set(ps)) == 40
    assert all(all(p[i] != i for i in range(18)) for p in ps)
    assert ps == ev.derangements(18, 40)
