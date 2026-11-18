"""The wide-7 gate functions compute what research/wide-7.md says they do."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _rules() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide7_rules")
    finally:
        sys.path.remove(str(LIB))


def test_third_friday() -> None:
    r = _rules()
    assert r.third_friday(2024, 12) == date(2024, 12, 20)
    assert r.third_friday(2021, 12) == date(2021, 12, 17)
    assert r.third_friday(2020, 12) == date(2020, 12, 18)  # Dec 2020 starts on a Tuesday


def test_last_on_or_before_and_window_return() -> None:
    r = _rules()
    days = [date(2020, 1, 2), date(2020, 1, 3), date(2020, 1, 6)]
    logc = np.log(np.array([100.0, 110.0, 121.0]))
    assert r.last_on_or_before(days, date(2020, 1, 1)) == -1
    assert r.last_on_or_before(days, date(2020, 1, 5)) == 1
    got = r.window_return(days, logc, date(2020, 1, 2), date(2020, 1, 6))
    assert abs(got - math.log(1.21)) < 1e-12
    assert math.isnan(r.window_return(days, logc, date(2020, 1, 4), date(2020, 1, 5)))


def _daily(start: date, n: int) -> list[date]:
    return [start + timedelta(days=k) for k in range(n)]


def test_wash_sale_year_dose_and_windows() -> None:
    r = _rules()
    days = _daily(date(2019, 12, 1), 500)
    # price falls 20% (log) over 2020 to the end of November, then +1 log-unit per day after
    logc = np.zeros(len(days))
    for k, d in enumerate(days):
        if d <= date(2019, 12, 31):
            logc[k] = 0.0
        elif d <= date(2020, 11, 30):
            logc[k] = -0.2 * (d - date(2019, 12, 31)).days / 335
        else:
            logc[k] = -0.2 + 0.001 * (d - date(2020, 11, 30)).days
    v = r.wash_sale_year(days, logc, 2020, date(2021, 12, 31))
    assert v is not None
    assert abs(v["ytd"] + 0.2) < 1e-9 and abs(v["loss"] - 0.2) < 1e-9
    assert abs(v["echo"] - 0.015) < 1e-9  # 15 calendar days at +0.001
    assert abs(v["toy"] - 0.010) < 1e-9
    assert abs(v["late"] - 0.015) < 1e-9


def test_wash_sale_year_respects_last_day_and_history() -> None:
    r = _rules()
    days = _daily(date(2019, 12, 1), 500)
    logc = np.zeros(len(days))
    # window would end after the last readable day
    assert r.wash_sale_year(days, logc, 2020, date(2021, 1, 31)) is None
    # no close before the tax year starts
    assert r.wash_sale_year(days[40:], logc[40:], 2020, date(2021, 12, 31)) is None
    # gains give zero loss
    up = np.linspace(0, 1, len(days))
    v = r.wash_sale_year(days, up, 2020, date(2021, 12, 31))
    assert v is not None and v["loss"] == 0.0 and v["ytd"] > 0


def test_year_dummies() -> None:
    r = _rules()
    x = r.year_dummies([2001, 2000, 2001])
    assert x.tolist() == [[0.0, 1.0], [1.0, 0.0], [0.0, 1.0]]


def test_festival_dates_sit_on_new_moons() -> None:
    r = _rules()
    sys.path.insert(0, str(LIB))
    try:
        r6 = importlib.import_module("wide6_rules")
    finally:
        sys.path.remove(str(LIB))
    nm = r6.moon_dates(date(2004, 1, 1), date(2026, 12, 31), 0.0)

    def off(d: date) -> int:
        return int(min(((d - m).days for m in nm), key=abs))

    assert all(off(d) in (0, 1) for d in r.LUNAR_NEW_YEAR)
    assert all(off(d) in (0, -1, -2) for d in r.DIWALI)
    assert all(date(d.year, 1, 21) <= d <= date(d.year, 2, 20) for d in r.LUNAR_NEW_YEAR)
    assert all(date(d.year, 10, 15) <= d <= date(d.year, 11, 15) for d in r.DIWALI)


def test_run_flags_marks_sessions_strictly_before() -> None:
    r = _rules()
    days = [date(2020, 1, k) for k in (2, 3, 6, 7, 8, 9, 10)]
    f = r.run_flags(days, [date(2020, 1, 8)], 2)
    assert f.tolist() == [0, 0, 1, 1, 0, 0, 0]
    assert r.run_flags(days, [date(2020, 1, 1)], 3).sum() == 0
    assert r.month_matrix([date(2020, 3, 1)])[0, 2] == 1.0
    assert r.run_flags(days, [date(2020, 1, 20)], 3).sum() == 0  # after the last day: skipped
