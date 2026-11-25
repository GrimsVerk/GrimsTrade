"""The wide-23 functions compute what research/cards/wide-23.md says they do."""

from __future__ import annotations

import importlib
import json
import math
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide23_events")
    finally:
        sys.path.remove(str(LIB))


def _ts(d: date) -> int:
    return int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp())


def test_forty_earlier_shifts_as_the_card_writes_them() -> None:
    ev = _ev()
    assert [23 * k for k in range(1, 41)] == ev.SHIFTS  # 23 .. 920 days, earlier doses only
    # The step is not a multiple of a week; five shifts (k = 7, 14, ..., 35) are whole weeks.
    assert sum(1 for k in ev.SHIFTS if k % 7 == 0) == 5


def test_parse_drops_small_missing_and_late_events_and_splits_exchanges() -> None:
    ev = _ev()
    rows = [
        {"date": _ts(date(2022, 3, 23)), "amount": 624e6, "targetType": "Chain"},
        {"date": _ts(date(2022, 3, 24)), "amount": 9.9e6, "targetType": "DeFi Protocol"},
        {"date": _ts(date(2022, 3, 25)), "amount": None, "targetType": "DeFi Protocol"},
        {"date": _ts(date(2024, 5, 31)), "amount": 305e6, "targetType": "CEX"},
        {"date": _ts(date(2025, 11, 1)), "amount": 50e6, "targetType": "DeFi Protocol"},
        "junk",
    ]
    e = ev.parse_hacks(json.dumps(rows), date(2025, 10, 31))
    assert [(date.fromordinal(d), a) for d, a, _ in e] == [
        (date(2022, 3, 23), 624e6),
        (date(2024, 5, 31), 305e6),
    ]
    g, x = ev.split(e)
    assert [t for *_, t in g] == ["Chain"] and [t for *_, t in x] == ["CEX"]


def test_dose_sums_log2_weights_per_day_and_shifts_to_earlier_days() -> None:
    ev = _ev()
    d0 = date(2023, 1, 10).toordinal()
    e = [(d0, 10e6, "DeFi"), (d0, 40e6, "DeFi"), (d0 + 5, 160e6, "Token")]
    dz = ev.dose(e)
    assert math.isclose(dz[d0], 1.0 + 3.0) and math.isclose(dz[d0 + 5], 5.0)
    assert ev.dose(e, binary=True)[d0] == 2.0
    assert ev.dose(e, min_usd=50e6) == {d0 + 5: 5.0}
    # D_k(d) = D(d - k): the dose k days earlier lands on day d.
    assert ev.at(dz, d0 + 23, 23) == dz[d0] and ev.at(dz, d0 + 1, 23) == 0.0


def test_rows_need_every_close_and_end_by_the_cut() -> None:
    ev = _ev()
    c = {d: 100.0 + d for d in range(0, 60)}
    rs = ev.rows(c, last=50)
    assert rs[0] == 29 and rs[-1] == 42
    del c[35]
    rs = ev.rows(c, last=50)
    assert all(not (d - 29 <= 35 <= d + 8) for d in rs)
    assert math.isclose(ev.logret(c, 1, 2), math.log(102 / 101))
    assert math.isnan(ev.logret(c, 35, 36))


def test_ols_nw_recovers_a_slope_and_zero_lags_is_white() -> None:
    ev = _ev()
    rng = np.random.default_rng(0)
    x = rng.normal(size=500)
    y = 0.5 * x + rng.normal(size=500)
    b, t = ev.ols_nw([x], y, 0)
    assert abs(b[1] - 0.5) < 0.1 and t[1] > 8
    b7, t7 = ev.ols_nw([x], y, 7)
    assert np.allclose(b, b7) and t7[1] > 6


def test_surrogates_keep_spectrum_or_weights_and_are_deterministic() -> None:
    ev = _ev()
    x = np.zeros(100)
    x[[3, 40, 77]] = [1.0, 2.0, 5.0]
    ph = ev.phase_surrogates(x, n=3)
    assert len(ph) == 3 and all(len(s) == 100 for s in ph)
    for s in ph:
        assert np.allclose(np.abs(np.fft.rfft(s - s.mean())), np.abs(np.fft.rfft(x - x.mean())))
    assert np.allclose(ph[0], ev.phase_surrogates(x, n=3)[0])
    dy = ev.day_surrogates(x, n=3)
    for s in dy:
        assert sorted(s[s != 0]) == [1.0, 2.0, 5.0]
    assert np.array_equal(dy[1], ev.day_surrogates(x, n=3)[1])


def test_rank_counts_ties_against_the_true_t() -> None:
    ev = _ev()
    assert ev.rank_lowest(-2.5, [-3.0, -2.5, 0.0]) == 3
    assert ev.rank_lowest(-4.0, [-3.0, 1.0]) == 1
