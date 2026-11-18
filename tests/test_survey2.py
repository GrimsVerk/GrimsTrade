"""The survey-2 rule labels FOMC-cycle weeks as its card says (research/cards/fomc-cycle.md)."""

from __future__ import annotations

import importlib
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _rules() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("survey2_rules")
    finally:
        sys.path.remove(str(LIB))


def test_weeks_around_one_meeting() -> None:
    r = _rules()
    d0 = date(2024, 1, 31)  # a Wednesday
    days = [d0, date(2024, 3, 20)]
    assert r.label(date(2024, 1, 30), days) is True  # day -1: week 0
    assert r.label(date(2024, 1, 29), days) is False  # day -2: week -1
    assert r.label(d0, days) is True  # day 0
    assert r.label(date(2024, 2, 5), days) is True  # day 3 (weekend skipped)
    assert r.label(date(2024, 2, 6), days) is False  # day 4: week 1
    assert r.label(date(2024, 2, 12), days) is False  # day 8
    assert r.label(date(2024, 2, 13), days) is True  # day 9: week 2
    assert r.label(date(2024, 3, 12), days) is False  # day -6 of the next meeting
    assert r.label(date(2024, 3, 19), days) is True  # day -1 of the next meeting


def test_late_days_and_before_first_meeting() -> None:
    r = _rules()
    d0 = date(2024, 1, 31)
    far = d0 + timedelta(days=120)
    assert r.label(date(2024, 1, 23), [d0]) is False  # day -6 of the first meeting
    assert r.label(date(2024, 1, 22), [d0]) is None  # before it: no label
    k34 = date(2024, 3, 19)  # 34 weekdays after d0, next meeting far away
    assert r.weekdays_between(d0, k34) == 34
    assert r.label(k34, [d0, far]) is False
    assert r.label(k34 - timedelta(days=1), [d0, far]) is True  # day 33: week 6


def test_next_session_skips_holidays() -> None:
    r = _rules()
    cal = [date(2024, 12, 24), date(2024, 12, 26), date(2024, 12, 27)]
    assert r.next_session(cal, date(2024, 12, 24)) == date(2024, 12, 26)
    assert r.next_session(cal, date(2024, 12, 27)) is None
