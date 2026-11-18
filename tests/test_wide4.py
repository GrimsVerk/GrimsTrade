"""The wide-4 rules do what their cards say (research/cards/tax-drain.md)."""

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
        return importlib.import_module("wide4_rules")
    finally:
        sys.path.remove(str(LIB))


def _weekdays(a: date, b: date) -> list[date]:
    out, d = [], a
    while d <= b:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def test_tax_dates_and_2020_exception() -> None:
    r = _rules()
    d = r.statutory_dates(2019, 2020)
    assert date(2019, 4, 15) in d and date(2019, 12, 15) in d and len(d) == 9
    assert date(2020, 4, 15) not in d and date(2020, 6, 15) not in d
    assert date(2020, 7, 15) in d


def test_tax_session_is_first_on_or_after_the_15th() -> None:
    r = _rules()
    cal = _weekdays(date(2023, 1, 2), date(2023, 12, 29))
    js = r.tax_sessions(cal, r.statutory_dates(2023, 2023))
    # 2023-01-15 and 2023-04-15 fall on a Sunday and a Saturday
    assert [cal[j] for j in js][:2] == [date(2023, 1, 16), date(2023, 4, 17)]


def test_gate_covers_d_minus_2_to_d_plus_2_only_when_active() -> None:
    r = _rules()
    cal = _weekdays(date(2023, 6, 1), date(2023, 6, 30))
    js = r.tax_sessions(cal, [date(2023, 6, 15)])
    out = r.out_sessions(cal, js, (date(2020, 1, 1), date(2030, 1, 1)))
    assert sorted(out) == [date(2023, 6, d) for d in (13, 14, 15, 16, 19)]
    assert r.out_sessions(cal, js, (date(1990, 1, 1), date(2008, 9, 14))) == set()


def test_regimes() -> None:
    r = _rules()
    assert r.regime(date(2000, 4, 17)) == "A"
    assert r.regime(date(2008, 10, 15)) is None
    assert r.regime(date(2012, 6, 15)) == "B"
    assert r.regime(date(2019, 9, 16)) == "C"
    assert r.regime(date(2021, 3, 15)) == "B"
    assert r.regime(date(2023, 4, 17)) == "C"


def test_window_excess_finds_a_planted_dip() -> None:
    r = _rules()
    cal = _weekdays(date(2023, 1, 2), date(2023, 12, 29))
    js = r.tax_sessions(cal, r.statutory_dates(2023, 2023))
    level = np.full(len(cal), 100.0)
    for j in js:  # a 1% lower close at D+3 than at D-2, nothing anywhere else
        level[j - 1 : j + 4] = 99.0
    x = r.window_excess(cal, level, js, lambda d: True)
    assert len(x) == 5 and (x < -0.005).all()
    flat = r.window_excess(cal, np.full(len(cal), 50.0), js, lambda d: True, log=False)
    assert np.allclose(flat, 0.0)
