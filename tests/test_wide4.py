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


def _coupons() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide4_coupons")
    finally:
        sys.path.remove(str(LIB))


def test_coupon_dates_follow_the_maturity_day_and_month_end() -> None:
    m = _coupons()
    assert m.coupon_dates(date(2030, 2, 15), date(2028, 2, 15)) == [
        date(2028, 8, 15),
        date(2029, 2, 15),
        date(2029, 8, 15),
        date(2030, 2, 15),
    ]
    # a note maturing on 30 April pays on 31 October and 30 April
    assert m.coupon_dates(date(2027, 4, 30), date(2026, 4, 30)) == [
        date(2026, 10, 31),
        date(2027, 4, 30),
    ]


def test_payments_net_coupons_principal_and_settlements() -> None:
    m = _coupons()
    tr = [
        m.Tranche(date(2028, 2, 1), date(2028, 2, 15), 10.0),
        m.Tranche(date(2028, 4, 1), date(2028, 4, 15), 5.0),
    ]
    rows = m.payments({"X": (date(2029, 2, 15), 4.0, tr)})
    by = {(d, k): a for d, k, a, *_ in rows}
    assert by[(date(2028, 2, 15), "settle")] == -10.0
    assert abs(by[(date(2028, 8, 15), "coupon")] - 15.0 * 0.02) < 1e-12
    assert by[(date(2029, 2, 15), "principal")] == 15.0


def test_dose_counts_only_what_was_announced() -> None:
    r = _rules()
    pays = [
        r.Payment(date(2024, 5, 15), "principal", 30.0, date(2014, 5, 1)),
        r.Payment(date(2024, 5, 15), "settle", -20.0, date(2024, 5, 8)),
        r.Payment(date(2024, 5, 15), "settle", -50.0, date(2024, 5, 16)),
    ]
    assert r.net_dose(pays, date(2024, 5, 15), date(2024, 5, 14)) == 10.0
    cal = _weekdays(date(2024, 5, 1), date(2024, 5, 31))
    ds = r.mid_month_doses(cal, pays, date(2024, 5, 1), date(2024, 5, 31))
    assert len(ds) == 1
    j, (net, _) = next(iter(ds.items()))
    assert cal[j] == date(2024, 5, 15) and net == 10.0
    on = r.overlay_sessions(cal, ds, True)
    assert sorted(on) == [date(2024, 5, d) for d in (14, 15, 16, 17)]
    assert r.overlay_sessions(cal, ds, False) == set()


def test_hc1_slope_recovers_a_line() -> None:
    r = _rules()
    x = np.arange(20, dtype=float)
    y = 3.0 * x + 1.0 + np.where(np.arange(20) % 2 == 0, 0.5, -0.5)
    b, t = r.hc1_slope(x, y)
    assert abs(b - 3.0) < 0.05 and t > 50
