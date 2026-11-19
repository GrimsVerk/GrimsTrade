"""The wide-10 functions compute what research/wide-10.md says they do."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide10_events")
    finally:
        sys.path.remove(str(LIB))


def _op(day: str, kind: str = "Outright Coupon Purchase", direction: str = "P") -> dict[str, Any]:
    return {
        "operationDate": day,
        "operationType": kind,
        "operationDirection": direction,
        "auctionStatus": "Results",
        "details": [
            {"securityDescription": "T 04.375 02/15/38", "parAmountAccepted": "1500000000"},
            {"securityDescription": "T 02.000 02/15/25", "parAmountAccepted": "2000000000"},
            {"securityDescription": "T 03.000 11/15/44", "parAmountAccepted": "0"},
        ],
    }


def test_shifts_are_forty_without_small_or_weekday_shifts() -> None:
    ev = _ev()
    s = ev.SHIFTS_W20
    assert len(s) == 40 and len(set(s)) == 40
    assert all(abs(k) >= 3 and abs(k) <= 27 and k % 5 != 0 for k in s)
    assert 3 in s and -27 in s and 5 not in s and 0 not in s


def test_keep_operation_only_coupon_purchases_with_results() -> None:
    ev = _ev()
    assert ev.keep_operation(_op("2014-01-02"))
    assert not ev.keep_operation(_op("2014-01-02", "Outright TIPS Purchase"))
    assert not ev.keep_operation(_op("2014-01-02", "Outright Bill Purchase"))
    assert not ev.keep_operation(_op("2014-01-02", direction="S"))
    op = _op("2014-01-02")
    op["auctionStatus"] = "Announcement"
    assert not ev.keep_operation(op)


def test_maturity_and_twenty_year_bucket() -> None:
    ev = _ev()
    assert ev.maturity("T 08.125 05/15/21") == date(2021, 5, 15)
    assert ev.maturity("T 04.375 02/15/38") == date(2038, 2, 15)
    assert ev.maturity("T 06.000 02/15/96") == date(1996, 2, 15)
    assert ev.maturity("garbage") is None
    assert ev.add_years(date(2016, 2, 29), 21) == date(2037, 2, 28)
    assert ev.in_bucket(date(2018, 2, 15), date(2038, 2, 15), 20, None)
    assert not ev.in_bucket(date(2018, 2, 16), date(2038, 2, 15), 20, None)
    assert ev.in_bucket(date(2018, 1, 1), date(2028, 1, 1), 7, 10)
    assert not ev.in_bucket(date(2018, 1, 1), date(2028, 1, 2), 7, 10)


def test_daily_par_sums_bucket_by_day_and_skips_other_types() -> None:
    ev = _ev()
    ops = [_op("2018-01-10"), _op("2018-01-10"), _op("2018-01-11", "Outright TIPS Purchase")]
    assert ev.daily_par(ops, 20, None) == {date(2018, 1, 10): 3.0}  # the 2038 bond, twice
    assert ev.daily_par(ops, 0, None) == {date(2018, 1, 10): 7.0}


def test_dose_series_and_shift() -> None:
    ev = _ev()
    days = [date(2018, 1, d) for d in (9, 10, 11)]
    x = ev.dose_series(days, {date(2018, 1, 10): math.e - 1})
    assert np.allclose(x, [0.0, 1.0, 0.0])
    a = np.array([1.0, 2.0, 3.0, 4.0])
    assert np.array_equal(ev.shifted(a, 1)[1:], [1.0, 2.0, 3.0]) and np.isnan(ev.shifted(a, 1)[0])
    assert np.array_equal(ev.shifted(a, -2)[:2], [3.0, 4.0]) and np.isnan(ev.shifted(a, -2)[3])
    assert np.array_equal(ev.shifted(a, 0), a)


def test_ols_hc1_slope_and_t() -> None:
    ev = _ev()
    rng = np.random.default_rng(0)
    x = rng.normal(size=500)
    y = 2.0 * x + rng.normal(size=500)
    b, t = ev.ols_hc1(x, y)
    assert abs(b - 2.0) < 0.15 and t > 20
    x2 = np.concatenate([x, [np.nan]])
    y2 = np.concatenate([y, [1.0]])
    assert ev.ols_hc1(x2, y2) == (b, t)


def test_rank_and_null_spread() -> None:
    ev = _ev()
    assert ev.rank_highest(2.0, [1.0, 3.0, 2.0]) == 2
    sd, share = ev.null_spread([-2.0, 0.0, 2.0, 1.0])
    assert share == 0.5 and sd > 0
