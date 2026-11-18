"""The survey-3 rule builds the bond signal as its card says (research/cards/xtsmom.md)."""

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
        return importlib.import_module("survey3_rules")
    finally:
        sys.path.remove(str(LIB))


def test_bond_return_is_carry_minus_duration_times_yield_change() -> None:
    r = _rules()
    days = [date(2020, 1, 1), date(2020, 1, 2), date(2020, 1, 3), date(2020, 2, 3)]
    ret = r.bond_returns(days, [4.0, 4.0, 4.1, 4.1])
    assert ret[0] == 0
    assert math.isclose(ret[1], 0.04 / 365)  # flat yield: one day of carry
    assert ret[2] < 0  # yield up: price down, far more than a day's carry
    assert math.isclose(ret[2], -r.duration(0.04, 10) * 0.001 + 0.04 / 365)
    assert ret[3] == 0  # a gap of more than ten days counts as nothing


def test_trailing_sums_only_the_window_and_waits_for_history() -> None:
    r = _rules()
    days = [date(2020, 1, 1) + timedelta(days=i) for i in range(10)]
    rets = np.arange(10, dtype=float)
    tr = r.trailing(days, rets, 3)
    assert all(math.isnan(x) for x in tr[:3])  # shorter than the look-back
    assert tr[3] == 1 + 2 + 3  # (day 0, day 3]: the return ending on day 0 is outside
    assert tr[9] == 7 + 8 + 9


def test_trailing_never_reads_later_observations() -> None:
    r = _rules()
    days = [date(2020, 1, 1) + timedelta(days=i) for i in range(20)]
    rets = np.linspace(-1, 1, 20)
    a = r.trailing(days, rets, 5)
    changed = rets.copy()
    changed[12:] = 99.0
    b = r.trailing(days, changed, 5)
    assert all(math.isnan(x) for x in a[:5] + b[:5])
    assert a[5:12] == b[5:12]


def test_an_observation_is_used_from_the_next_day() -> None:
    r = _rules()
    assert r.usable_from([date(2024, 3, 1)]) == [date(2024, 3, 2)]
