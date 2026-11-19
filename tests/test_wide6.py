"""The wide-6 gate functions compute what research/wide-6.md says they do."""

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
        return importlib.import_module("wide6_rules")
    finally:
        sys.path.remove(str(LIB))


def test_rolling_ac1_matches_direct_correlation() -> None:
    r = _rules()
    x = np.random.default_rng(1).standard_normal(300)
    w = 50
    got = r.rolling_ac1(x, w)
    assert np.isnan(got[: w - 1]).all()
    for i in (w - 1, 120, 299):
        win = x[i - w + 1 : i + 1]
        want = np.corrcoef(win[:-1], win[1:])[0, 1]
        assert abs(got[i] - want) < 1e-10


def test_rolling_ac1_sees_persistence() -> None:
    r = _rules()
    rng = np.random.default_rng(2)
    e = rng.standard_normal(2000)
    ar = np.zeros(2000)
    for i in range(1, 2000):
        ar[i] = 0.8 * ar[i - 1] + e[i]
    assert r.rolling_ac1(ar, 500)[-1] > 0.7
    assert abs(r.rolling_ac1(e, 500)[-1]) < 0.15


def test_rolling_var_and_mean() -> None:
    r = _rules()
    x = np.arange(10.0)
    v = r.rolling_var(x, 4)
    assert np.isnan(v[2]) and abs(v[3] - np.var(x[:4], ddof=1)) < 1e-12
    assert abs(r.trailing_mean(x, 4)[9] - 7.5) < 1e-12


def test_kendall_trend_sign_and_lookback() -> None:
    r = _rules()
    s = np.concatenate([np.arange(20.0), np.arange(20.0)[::-1]])
    assert r.kendall_trend(s, 19, 20) == 1.0
    assert r.kendall_trend(s, 39, 20) == -1.0
    assert np.isnan(r.kendall_trend(s, 5, 20))


def test_forward_max_drawdown_uses_only_the_window() -> None:
    r = _rules()
    logc = np.log(np.array([100, 110, 99, 105, 50, 200.0]))
    # from bar 0 over 3 bars: peak 110 then 99
    assert abs(r.forward_max_drawdown(logc, 0, 3) - np.log(110 / 99)) < 1e-12
    # the crash at bar 4 is outside this window
    assert r.forward_max_drawdown(logc, 0, 3) < 0.2
    assert np.isnan(r.forward_max_drawdown(logc, 3, 3))


def test_ols_dk_recovers_slope() -> None:
    r = _rules()
    rng = np.random.default_rng(3)
    n = 2000
    z = rng.standard_normal(n)
    y = 1.0 + 0.5 * z + rng.standard_normal(n)
    x = np.column_stack([np.ones(n), z])
    beta, t = r.ols_dk(y, x, list(range(n)), 5)
    assert abs(beta[1] - 0.5) < 0.06 and t[1] > 15
    # pure noise: |t| small
    beta, t = r.ols_dk(rng.standard_normal(n), x, list(range(n)), 5)
    assert abs(t[1]) < 3.5


def test_moon_dates_match_known_new_moons() -> None:
    r = _rules()
    # 2024-04-08 total solar eclipse (new moon 18:21 UTC); 2017-08-21 eclipse (18:30 UTC)
    for known in (date(2024, 4, 8), date(2017, 8, 21)):
        got = r.moon_dates(known - timedelta(days=10), known + timedelta(days=10), 0.0)
        assert len(got) == 1 and abs((got[0] - known).days) <= 1
    # 2025-03-14 total lunar eclipse (full moon 06:55 UTC)
    got = r.moon_dates(date(2025, 3, 4), date(2025, 3, 24), 0.5)
    assert len(got) == 1 and abs((got[0] - date(2025, 3, 14)).days) <= 1


def test_moon_period_splits_cycle() -> None:
    r = _rules()
    days = [date(2024, 1, 1) + timedelta(days=i) for i in range(365)]
    p = r.moon_period(days, 7)
    assert (p == 1).sum() > 150 and (p == -1).sum() > 150 and (p == 0).sum() < 20
    near = r.moon_period([date(2024, 4, 8)], 3)
    assert near[0] == 1
    shifted = r.moon_period([date(2024, 4, 8)], 3, shift=15)
    assert shifted[0] == -1 or shifted[0] == 0
