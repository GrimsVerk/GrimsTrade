"""xs-century-1: rank weights, signals' timing, vol scaling, book weights, alpha statistic."""

from __future__ import annotations

import importlib.util
import math
import sys
from datetime import date
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

PATH = Path(__file__).resolve().parents[1] / "research" / "lib" / "xs_century.py"


@pytest.fixture(scope="module")
def xc() -> ModuleType:
    spec = importlib.util.spec_from_file_location("xs_century_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_rank_weights_dollar_neutral_and_ordered(xc: ModuleType) -> None:
    w = xc.rank_weights({"a": 0.3, "b": -0.1, "c": 0.0, "d": 0.9, "e": 0.3})
    assert sum(v for v in w.values() if v > 0) == pytest.approx(1.0)
    assert sum(v for v in w.values() if v < 0) == pytest.approx(-1.0)
    assert w["a"] == pytest.approx(w["e"])
    assert w["d"] > w["a"] > w["c"] > w["b"]
    assert xc.rank_weights({"a": 1.0, "b": 2.0, "c": 3.0}) == {}  # fewer than 4 assets
    assert xc.rank_weights({k: 1.0 for k in "abcd"}) == {}  # no spread


def test_momentum_skips_the_lag_months(xc: ModuleType) -> None:
    t = date(2000, 12, 1)
    ret = {xc.add_months(t, -k): 0.0 for k in range(1, 20)}
    ret[xc.add_months(t, -1)] = 0.5  # the skipped month must not count
    assert xc.momentum(ret, t, 2) == pytest.approx(0.0)
    ret[xc.add_months(t, -12)] = 0.1  # the oldest month of the 12-1 window counts
    assert xc.momentum(ret, t, 2) == pytest.approx(0.1)
    ret[xc.add_months(t, -13)] = 0.7  # outside the window
    assert xc.momentum(ret, t, 2) == pytest.approx(0.1)
    del ret[xc.add_months(t, -5)]
    assert xc.momentum(ret, t, 2) is None


def test_value_signals_use_only_lagged_data(xc: ModuleType) -> None:
    t = date(2010, 6, 1)
    y = {xc.add_months(t, -k): 5.0 for k in range(0, 80)}
    y[t] = 99.0  # future-ish values must not matter at lag 3
    y[xc.add_months(t, -1)] = 99.0
    y[xc.add_months(t, -3)] = 6.0
    assert xc.yield_change_value(y, t, 3) == pytest.approx(1.0)
    px = {xc.add_months(t, -k): 100.0 for k in range(0, 80)}
    px[xc.add_months(t, -2)] = 50.0  # the price halved: cheap, positive value
    assert xc.reversal_value(px, t, 2) == pytest.approx(math.log(2.0))
    px[t] = 1.0
    assert xc.reversal_value(px, t, 2) == pytest.approx(math.log(2.0))


def test_vol_scale_targets_ten_percent_and_caps(xc: ModuleType) -> None:
    assert xc.vol_scale([0.01] * 23) is None
    h = [0.02, -0.02] * 18
    sd = float(np.std(h, ddof=1)) * math.sqrt(12)
    assert xc.vol_scale(h) == pytest.approx(0.10 / sd)
    assert xc.vol_scale([0.001, -0.001] * 18) == 4.0


def test_constructed_sleeve_uses_past_vol_and_charges_turnover(xc: ModuleType) -> None:
    ms = xc.months(date(2000, 1, 1), date(2003, 12, 1))
    rets = {a: {m: 0.01 * (i + 1) * (1 if j % 2 else -1) for j, m in enumerate(ms)}
            for i, a in enumerate("abcd")}  # fmt: skip
    sig = {m: {"a": 1.0, "b": 2.0, "c": 3.0, "d": 4.0} for m in ms}
    out = xc.constructed_sleeve(sig, rets, cost=0.001)
    first = min(out)
    assert first == ms[24]  # 24 months of raw history before the first scaled month
    net, gross, raw = out[first]
    assert net < gross  # entering costs turnover
    net2, gross2, _ = out[ms[25]]
    assert net2 == pytest.approx(gross2, abs=1e-12) or net2 < gross2


def test_book_equal_weights_classes_then_sleeves(xc: ModuleType) -> None:
    m1, m2 = date(2000, 1, 1), date(2000, 2, 1)
    b = xc.book({"A": [{m1: 0.02, m2: 0.02}, {m1: 0.04}], "B": [{m2: 0.10}]})
    assert b[m1] == pytest.approx(0.03)
    assert b[m2] == pytest.approx((0.02 + 0.10) / 2)


def test_alpha_recovers_planted_ir_and_ignores_beta(xc: ModuleType) -> None:
    rng = np.random.default_rng(1)
    n = 1200
    t = rng.normal(0.005, 0.04, n)
    e = rng.normal(0.0, 0.02, n)
    a = 0.6 / math.sqrt(12) * 0.02  # IR 0.6
    s = xc.score(a + 0.5 * t + e, t, draws=400)
    assert s["b"] == pytest.approx(0.5, abs=0.05)
    assert s["ir"] == pytest.approx(0.6, abs=0.25)
    assert s["z"] == pytest.approx(0.6 * math.sqrt(100), abs=2.5)
    assert s["z"] <= max(s["z_nw"], s["z_boot"]) + 1e-12
    lev = xc.score(2.0 * t, t, draws=200)
    assert abs(lev["a"]) < 1e-12 and lev["b"] == pytest.approx(2.0)
    noise = xc.score(rng.normal(0, 0.02, n), t, draws=200)
    assert abs(noise["z"]) < 3.0
