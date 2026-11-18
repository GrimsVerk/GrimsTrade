"""The wide-5 rules do what their cards say (research/cards/dealer-backlog.md,
research/cards/extension-dose.md)."""

from __future__ import annotations

import importlib
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _rules() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide5_rules")
    finally:
        sys.path.remove(str(LIB))


def _weekdays(a: date, b: date) -> list[date]:
    out, d = [], a
    while d <= b:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def _auction(r: Any, cusip: str, years: int, day: date, mat: date, amt: float = 10.0,
             dealer: float | None = None) -> Any:  # fmt: skip
    return r.Auction(cusip, years, day - timedelta(days=7), day, day + timedelta(days=5), mat,
                     amt, amt if dealer is not None else None, dealer)  # fmt: skip


def test_dealer_surprise_is_share_minus_median_of_previous_auctions() -> None:
    r = _rules()
    shares = [40, 50, 60, 30, 20, 10, 80]  # % of competitive awards
    aucs = [_auction(r, f"C{i}", 30, date(2010, 1, 1) + timedelta(days=30 * i),
                     date(2040, 1, 1), 10.0, s / 10) for i, s in enumerate(shares)]  # fmt: skip
    aucs.append(_auction(r, "TEN", 10, date(2010, 3, 1), date(2020, 3, 1), 10.0, 9.0))
    got = r.dealer_surprises(aucs, "long", window=12, min_prev=6)
    assert len(got) == 1  # only the 7th has six predecessors; the 10-year is another group
    assert got[0][0] == aucs[6].auction
    assert got[0][1] == pytest.approx(80 - 35)  # median of 40, 50, 60, 30, 20, 10


def test_backlog_holds_five_sessions_from_the_auction_close() -> None:
    r = _rules()
    cal = _weekdays(date(2015, 1, 5), date(2015, 2, 27))
    a, b = cal[3], cal[20]
    on = r.backlog_sessions(cal, [(a, 2.0), (b, -1.0), (date(2015, 1, 10), 5.0)], True)
    assert on == set(cal[3:8])  # Saturday's 'auction' is no session and is dropped
    assert r.backlog_sessions(cal, [(a, 2.0), (b, -1.0)], False) == set(cal[20:25])


def test_extension_is_positive_when_a_new_long_bond_settles() -> None:
    r = _rules()
    old = _auction(r, "OLD", 30, date(2010, 1, 10), date(2035, 6, 30), 20.0)
    new = _auction(r, "NEW", 30, date(2010, 2, 9), date(2040, 2, 15), 20.0)
    e = r.extension([old, new], date(2010, 1, 31), date(2010, 2, 28), date(2010, 2, 22), 20, 99)
    assert e > 0
    # held after the decision day: not known, so no extension at all
    late = r.extension([old, new], date(2010, 1, 31), date(2010, 2, 28), date(2010, 2, 8), 20, 99)
    assert late == pytest.approx(0.0)


def test_extension_counts_bonds_aging_out_of_the_bucket() -> None:
    r = _rules()
    short = _auction(r, "S", 30, date(2000, 1, 10), date(2030, 2, 15), 10.0)  # 20y left mid-Feb
    long = _auction(r, "L", 30, date(2000, 1, 10), date(2039, 1, 1), 10.0)
    e = r.extension([short, long], date(2010, 1, 31), date(2010, 2, 28), date(2010, 2, 22), 20, 99)
    assert e > 0  # the short one leaves, the average maturity rises


def test_classify_uses_only_previous_months_and_sessions_are_t4_to_t1() -> None:
    r = _rules()
    doses = {10 * k + 9: float(k % 3) for k in range(30)}
    cls = r.classify(doses, window=24)
    assert sorted(cls) == [10 * k + 9 for k in range(24, 30)]
    assert cls[249] is False  # k=24: 0 against a median of 1
    assert cls[259] is False  # k=25: 1 is not above 1
    assert cls[269] is True  # k=26: 2
    cal = _weekdays(date(2020, 1, 1), date(2021, 12, 31))
    assert r.ext_sessions(cal, {269: True, 259: False}, True) == set(cal[265:269])


def test_open_excess_subtracts_the_average_window() -> None:
    r = _rules()
    opens = np.exp(np.arange(10) * 0.01)
    ex = r.open_excess(opens, [0, 3, 8], 2, 0)
    assert ex[0] == pytest.approx(0.0) and ex[1] == pytest.approx(0.0)
    assert np.isnan(ex[2])
