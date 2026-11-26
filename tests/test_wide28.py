"""Offline tests for research/lib/wide28.py (W45 `arms-fear`)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "lib"))

import wide28 as w  # type: ignore[import-not-found]  # noqa: E402


def test_parse_nics_sums_states_and_treats_empty_as_zero() -> None:
    rows = [
        {"month": "2000-01", "handgun": "10", "long_gun": "5", "multiple": "", "totals": "99"},
        {"month": "2000-01", "handgun": "1", "long_gun": "", "multiple": "2", "totals": "1"},
        {"month": "2000-02", "handgun": "3", "long_gun": "3", "multiple": "3", "totals": "9"},
    ]
    s = w.parse_nics(rows)
    assert s == {w.mi(2000, 1): 18.0, w.mi(2000, 2): 9.0}
    assert w.parse_nics(rows, ("totals",))[w.mi(2000, 1)] == 100.0


def test_dose_is_three_month_yoy_log_growth() -> None:
    base = w.mi(2000, 1)
    s = {base + i: 100.0 for i in range(15)}
    s[base + 12] = s[base + 13] = s[base + 14] = 200.0
    d = w.dose_series(s)
    assert set(d) == {base + 14}
    assert math.isclose(d[base + 14], math.log(2.0))
    d1 = w.dose_series(s, window=1)
    assert set(d1) == {base + 12, base + 13, base + 14}


def test_dose_needs_every_month() -> None:
    base = w.mi(2000, 1)
    s = {base + i: 100.0 for i in range(15) if i != 1}
    assert w.dose_series(s) == {}


def test_parse_daily_groups_by_month_and_cuts_train() -> None:
    text = "header\n20251031,  1.00, 0, 0, 0\n20251103, 2.00,0,0,0\n20251030,-0.5,0,0,0\n"
    d = w.parse_daily(text)
    assert d == {w.mi(2025, 10): [1.0, -0.5]}


def test_build_uses_no_return_after_entry_month_plus_horizon() -> None:
    m0 = w.mi(2010, 1)
    mkt = {m0 + i: float(i) for i in range(-12, 8)}
    daily = {m0 + i: [1.0, 1.0] for i in range(-2, 3)}
    spec = w.Spec(first=m0, last=m0)
    rows = w.build(mkt, daily, spec)
    y, c = rows[m0]
    assert y == 2.0 + 3.0 + 4.0  # months m+2 .. m+4
    assert c["c1"] == 1.0  # month m+1
    assert c["c12"] == sum(range(-10, 2))
    assert math.isclose(c["rv"], math.log(6.0))
    # a missing future month drops the row
    del mkt[m0 + 4]
    assert w.build(mkt, daily, spec) == {}


def test_build_drop_window() -> None:
    m0 = w.mi(2010, 1)
    mkt = {m0 + i: 0.5 for i in range(-12, 10)}
    daily = {m0 + i: [1.0] for i in range(-2, 5)}
    rows = w.build(mkt, daily, w.Spec(first=m0, last=m0 + 2, drop=(m0 + 1, m0 + 1)))
    assert sorted(rows) == [m0, m0 + 2]


def test_fit_recovers_planted_slope() -> None:
    rng = np.random.default_rng(0)
    rows = {}
    dose = {}
    for m in range(200):
        d = float(rng.normal())
        dose[m] = d
        c = {"c12": float(rng.normal()), "c1": float(rng.normal()), "rv": float(rng.normal())}
        rows[m] = (2.0 * d + 0.1 * float(rng.normal()), c)
    b, t, n = w.fit(rows, dose, w.Spec(lags=0))
    assert n == 200
    assert abs(b - 2.0) < 0.05
    assert t > 20
