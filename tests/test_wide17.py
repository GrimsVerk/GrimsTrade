"""The wide-17 functions compute what research/cards/wide-17.md says they do."""

from __future__ import annotations

import importlib
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide17_events")
    finally:
        sys.path.remove(str(LIB))


def test_w29_shifts_are_forty_both_ways_never_a_whole_year() -> None:
    s = _ev().SHIFTS_W29
    assert len(s) == 40 and len(set(s)) == 40
    assert all(13 <= abs(k) <= 89 and abs(k) % 12 != 0 for k in s)
    assert sum(k > 0 for k in s) == 20


def test_month_index_round_trips_to_the_last_day() -> None:
    ev = _ev()
    assert ev.month_index(date(2000, 1, 15)) == 24000
    assert ev.month_last_day(ev.month_index(date(2024, 2, 3))) == date(2024, 2, 29)
    assert ev.month_last_day(ev.month_index(date(2025, 12, 1))) == date(2025, 12, 31)


def test_parse_gistemp_skips_missing_and_months_after_the_cut() -> None:
    ev = _ev()
    text = (
        "Land-Ocean: Global Means\n"
        "Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D\n"
        "2025,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,***,***\n"
    )
    a = ev.parse_gistemp(text, date(2025, 10, 31))
    m = ev.month_index(date(2025, 1, 1))
    assert a[m] == 1.1 and a[m + 9] == 2.0
    assert m + 10 not in a and m + 11 not in a  # November after the cut, December missing


def test_temp_dose_is_last_year_minus_the_decade_before() -> None:
    ev = _ev()
    a = {m: 0.0 for m in range(132)}
    for m in range(120, 132):
        a[m] = 1.2
    d = ev.temp_dose(a)
    assert set(d) == {131}  # the only month with 131 months behind it
    assert math.isclose(d[131], 1.2)
    inn = ev.temp_innovation(a)
    assert math.isclose(inn[120], 1.2)
    assert math.isclose(inn[121], 1.2 - 1.2 / 120)


def test_month_return_needs_bars_inside_their_months_and_before_last() -> None:
    ev = _ev()
    sys.path.insert(0, str(LIB))
    try:
        closes = importlib.import_module("wide13_events").Closes
    finally:
        sys.path.remove(str(LIB))
    px = closes({date(2020, 1, 31): 100.0, date(2020, 2, 28): 110.0, date(2020, 4, 30): 120.0})
    jan = ev.month_index(date(2020, 1, 1))
    assert math.isclose(ev.month_return(px, jan, jan + 1, date(2025, 1, 1)), math.log(1.1))
    assert math.isnan(ev.month_return(px, jan + 1, jan + 2, date(2025, 1, 1)))  # no March bar
    assert math.isnan(ev.month_return(px, jan, jan + 1, date(2020, 2, 27)))  # exit after last


def test_don_pages_cut_after_last_and_weeks_run_saturday_to_friday() -> None:
    ev = _ev()
    page = json.dumps(
        {
            "value": [
                {"PublicationDate": "2025-10-31T00:00:00Z", "Title": "a"},
                {"PublicationDate": "2025-11-01T00:00:00Z", "Title": "b"},
                {"PublicationDate": "bad", "Title": "c"},
                {"PublicationDate": "2025-10-25T00:00:00Z", "Title": "d"},
            ]
        }
    )
    days = ev.parse_don_pages([page], date(2025, 10, 31))
    assert sorted(days) == [date(2025, 10, 25), date(2025, 10, 31)]
    n = ev.weekly_counts(days, [date(2025, 10, 24), date(2025, 10, 31)])
    assert n == {date(2025, 10, 24): 0, date(2025, 10, 31): 2}  # Saturday 25th: next week


def test_outbreak_dose_detrends_by_the_52_weeks_before() -> None:
    ev = _ev()
    f0 = date(2004, 1, 9)
    weeks = [f0 + timedelta(days=7 * i) for i in range(54)]
    counts = {f: 1 for f in weeks}
    counts[weeks[52]] = 4
    x = ev.outbreak_dose(counts)
    assert set(x) == {weeks[52], weeks[53]}
    z1, z4 = 2 * math.sqrt(1.375), 2 * math.sqrt(4.375)
    assert math.isclose(x[weeks[52]], z4 - z1)
    assert math.isclose(x[weeks[53]], z1 - (51 * z1 + z4) / 52)
