"""jst-gates-1: doses, drop rule, the pooled statistic and the three nulls (synthetic data)."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "jstgates1.py"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    spec = importlib.util.spec_from_file_location("jstgates1_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_hamilton_residual_zero_on_exact_relation_and_starts_after_burn_in(m: ModuleType) -> None:
    rng = np.random.default_rng(0)
    c = {1870 + i: float(v) for i, v in enumerate(rng.normal(size=40).cumsum())}
    # make c(t) an exact linear function of c(t-2), c(t-3) from 1873 on
    for t in range(1873, 1910):
        c[t] = 0.1 + 0.6 * c[t - 2] + 0.3 * c[t - 3]
    cc = m.hamilton(c)
    assert min(cc) == 1880  # 8 pairs: s = 1873..1880
    assert all(abs(v) < 1e-8 for v in cc.values())


def test_trail_dev_needs_eight_of_ten_and_uses_past_only(m: ModuleType) -> None:
    s = {t: float(t) for t in range(1870, 1900) if t not in (1875, 1876, 1877)}
    d = m.trail_dev(s)
    # 1880 has 7 past values in 1870..1879 (three missing): no dose
    assert 1880 not in d
    assert 1885 not in d  # 7 of 10
    assert d[1887] == pytest.approx(1887 - np.mean(range(1878, 1887)))  # 9 of 10


def test_zscore_and_rank(m: ModuleType) -> None:
    z = m.zscore({t: float(t) for t in range(1880, 1890)}, 1880, 1889)
    assert np.mean(list(z.values())) == pytest.approx(0.0)
    assert np.std(list(z.values())) == pytest.approx(1.0)
    assert m.rank_low(-2.0, [-3.0, -1.0, 0.0, math.nan]) == 2


def test_drop_rule_covers_wars_interpolation_and_hyperinflation(m: ModuleType) -> None:
    assert m.dropped("USA", 1916, frozenset())
    assert m.dropped("CHE", 1916, frozenset())
    assert m.dropped("ESP", 1938, frozenset())
    assert m.dropped("DEU", 1923, frozenset({1923}))
    assert not m.dropped("USA", 1925, frozenset())
    assert m.suspect("NOR", 1905) and not m.suspect("NOR", 1925)


Panel = dict[str, dict[int, float]]


def panel(
    rng: np.random.Generator, beta: float, n_c: int = 8, years: range = range(1871, 1960)
) -> tuple[Panel, Panel, Panel]:
    z: Panel = {f"C{i}": {} for i in range(n_c)}
    y: Panel = {f"C{i}": {} for i in range(n_c)}
    dp: Panel = {f"C{i}": {} for i in range(n_c)}
    for c in z:
        x = 0.0
        for t in years:
            x = 0.5 * x + rng.normal()
            z[c][t] = x
            dp[c][t] = 0.04 + 0.01 * rng.normal()
        for t in years:
            y[c][t] = 0.03 + beta * z[c].get(t - 1, 0.0) + 0.15 * rng.normal()
    return y, z, dp


def test_stat_finds_a_planted_negative_slope_and_shift_breaks_it(m: ModuleType) -> None:
    rng = np.random.default_rng(1)
    y, z, dp = panel(rng, beta=-0.06)
    countries = sorted(y)
    rows = m.base_rows(countries, list(range(1880, 1960)), y, z, dp, None, {})
    des = m.Design(rows, dp, None)
    f = m.stat(des, y, z)
    assert f.b < -0.03 and f.t < -4
    assert abs(m.stat(des, y, z, 7).t) < 4


def test_phase_surrogates_keep_amplitudes_and_cross_country_correlation(m: ModuleType) -> None:
    rng = np.random.default_rng(2)
    base = rng.normal(size=64).cumsum()
    z = {"A": {1880 + i: float(v) for i, v in enumerate(base)},
         "B": {1880 + i: float(v + 0.1 * rng.normal()) for i, v in enumerate(base)}}  # fmt: skip
    s = m.phase_panel(z, ["A", "B"], 1880, 1943, 5, 0)
    a = np.array(list(z["A"].values()))
    for p in s:
        sa = np.array([p["A"][t] for t in sorted(p["A"])])
        sb = np.array([p["B"][t] for t in sorted(p["B"])])
        assert np.allclose(np.abs(np.fft.rfft(sa - sa.mean())), np.abs(np.fft.rfft(a - a.mean())))
        assert np.corrcoef(sa, sb)[0, 1] > 0.9
        assert not np.allclose(sa, a)


def test_bootstrap_under_null_is_roughly_centred(m: ModuleType) -> None:
    rng = np.random.default_rng(3)
    y, z, dp = panel(rng, beta=0.0)
    countries = sorted(y)
    rows = m.base_rows(countries, list(range(1880, 1960)), y, z, dp, None, {})
    des = m.Design(rows, dp, None)
    ts = m.bootstrap(des, y, z, countries, 1871, 1959, {}, seed=0, b=60)
    assert len(ts) == 60
    assert abs(float(np.median(ts))) < 0.8
    assert 0.5 < float(np.std(ts)) < 2.0
