"""The info-1 inputs are look-ahead safe (card in research/info-1.md, "As-of rule").

- A Friday sees only observations with obs + lag <= Friday, and none older than MAX_AGE days.
- The trailing helpers never use later observations: scrambling the future leaves the past
  unchanged.
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def inf() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("info1_features")
    finally:
        sys.path.remove(str(LIB))


def test_asof_respects_lag_and_age(inf: Any) -> None:
    obs = [date(2024, 1, 2), date(2024, 1, 9)]  # Tuesdays
    vals = np.array([1.0, 2.0])
    fridays = [date(2024, 1, 5), date(2024, 1, 12), date(2024, 1, 19), date(2024, 2, 9)]
    out = inf.asof(obs, vals, 4, fridays)
    # Jan 5: the Jan 2 report is usable only from Jan 6 -> nothing yet.
    assert np.isnan(out[0])
    # Jan 12: the Jan 9 report is not usable until Jan 13 -> still the Jan 2 one.
    assert out[1] == 1.0
    assert out[2] == 2.0
    # Feb 9: the latest report is 31 days old -> stale.
    assert np.isnan(out[3])


def test_asof_skips_missing_values(inf: Any) -> None:
    obs = [date(2024, 1, 1), date(2024, 1, 2)]
    out = inf.asof(obs, np.array([5.0, np.nan]), 1, [date(2024, 1, 5)])
    assert out[0] == 5.0


def test_trailing_helpers_ignore_the_future(inf: Any) -> None:
    rng = np.random.default_rng(1)
    days = [date(2020, 1, 1) + timedelta(days=i) for i in range(900)]
    v = np.exp(rng.standard_normal(900))
    w = v.copy()
    w[600:] = np.exp(rng.standard_normal(300)) * 50  # scramble the future
    cut = 600
    helpers: list[Callable[[np.ndarray], np.ndarray]] = [
        lambda x: inf.roll_mean(x, 7),
        lambda x: inf.roll_z(x, 156, 104),
        lambda x: inf.calendar_mean_ratio(days, x, 30, 365),
        lambda x: inf.calendar_mean_ratio_level(days, x, 365),
        lambda x: inf.calendar_change(days, x, 91),
    ]
    for f in helpers:
        a, b = f(v)[:cut], f(w)[:cut]
        assert np.array_equal(np.isnan(a), np.isnan(b))
        assert np.allclose(a[~np.isnan(a)], b[~np.isnan(b)])
