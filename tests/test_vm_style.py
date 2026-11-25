"""vm-style-1: realised volatility, the DMU estimator, and the out-of-sample walk."""

from __future__ import annotations

import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

PATH = Path(__file__).resolve().parents[1] / "research" / "lib" / "vm_style.py"


@pytest.fixture(scope="module")
def vm() -> ModuleType:
    spec = importlib.util.spec_from_file_location("vm_style_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def months(n: int, first: date = date(1950, 1, 1)) -> list[date]:
    out, d = [], first
    for _ in range(n):
        out.append(d)
        d = date(d.year + d.month // 12, d.month % 12 + 1, 1)
    return out


def test_realised_sd_is_per_calendar_month(vm: ModuleType) -> None:
    d0 = date(2000, 1, 3)
    daily = [(d0 + timedelta(days=i), r) for i, r in enumerate([0.01, -0.01, 0.02, 0.0, 0.01])]
    daily += [(date(2000, 2, 1) + timedelta(days=i), 0.003) for i in range(6)]
    sd = vm.realised_sd(daily)
    assert sd[date(2000, 1, 1)] == pytest.approx(np.std([0.01, -0.01, 0.02, 0.0, 0.01], ddof=1))
    assert sd[date(2000, 2, 1)] == pytest.approx(0.0)


def test_conditioner_is_lagged_one_month(vm: ModuleType) -> None:
    z = vm.conditioner({date(2000, 1, 1): 0.02}, 1.0)
    assert z == {date(2000, 2, 1): pytest.approx(50.0)}
    z2 = vm.conditioner({date(2000, 1, 1): 0.02}, 2.0)
    assert z2[date(2000, 2, 1)] == pytest.approx(2500.0)


def test_trailing_sd_needs_full_window(vm: ModuleType) -> None:
    ms = months(7)
    s = vm.trailing_sd({m: float(i) for i, m in enumerate(ms)}, 6)
    assert set(s) == {ms[5], ms[6]}
    assert s[ms[5]] == pytest.approx(np.std(range(6), ddof=1))


def test_fit_eta_matches_unconstrained_mv_when_interior(vm: ModuleType) -> None:
    cov = np.array([[0.04, 0.01], [0.01, 0.09]])
    m = np.array([0.02, 0.03])
    eta = vm.fit_eta(m, cov, 5.0)
    assert eta == pytest.approx(np.linalg.solve(cov, m) / 5.0, rel=1e-6)


def test_fit_eta_clips_negative_weights_and_obeys_kkt(vm: ModuleType) -> None:
    cov = np.array([[0.04, 0.03], [0.03, 0.04]])
    m = np.array([0.02, 0.001])  # unconstrained MV shorts asset 2
    eta = vm.fit_eta(m, cov, 5.0)
    assert eta[1] == pytest.approx(0.0, abs=1e-12)
    grad = m - 5.0 * cov @ eta
    assert grad[0] == pytest.approx(0.0, abs=1e-9)
    assert grad[1] <= 1e-12


def synth(n: int, seed: int = 1) -> tuple[dict[str, dict[date, float]], dict[date, float]]:
    rng = np.random.default_rng(seed)
    ms = months(n)
    sd = np.exp(rng.normal(-4.0, 0.4, n))
    zz = {ms[i]: 1.0 / sd[i - 1] for i in range(1, n)}
    # Moreira-Muir's case: constant mean, risk proportional to last month's market vol, so the
    # risk-return trade-off weakens with vol and the managed copy r z has the higher Sharpe
    r = {ms[i]: 0.005 + sd[i - 1] * rng.normal(0, 1.0) for i in range(1, n)}
    return {"f": r}, zz


def test_walk_has_no_look_ahead(vm: ModuleType) -> None:
    sl, zz = synth(200)
    sc = {"f": dict.fromkeys(sl["f"], 1.0)}
    kap = {"f": 0.0}
    _, th = vm.walk(sl, sc, kap, {"f": zz}, min_hist=60)
    t = sorted(th)[10]
    bumped = {"f": dict(sl["f"])}
    bumped["f"][t] += 1.0
    _, th2 = vm.walk(bumped, sc, kap, {"f": zz}, min_hist=60)
    assert th2[t] == pytest.approx(th[t])
    later = sorted(th)[11]
    assert th2[later] != pytest.approx(th[later])


def test_walk_finds_vol_timing_and_charges_scaling_trades(vm: ModuleType) -> None:
    sl, zz = synth(400)
    sc = {"f": dict.fromkeys(sl["f"], 1.0)}
    out, th = vm.walk(sl, sc, {"f": 0.0}, {"f": zz}, min_hist=120)
    first = min(out)
    assert first == sorted(sl["f"])[120]
    vals = np.array([th[t]["f"] for t in sorted(th)])
    zs = np.array([zz[t] for t in sorted(th)])
    assert np.corrcoef(vals, zs)[0, 1] > 0.8  # weights move with 1 / vol
    out_c, th_c = vm.walk(sl, sc, {"f": 0.01}, {"f": zz}, min_hist=120)
    t1, t2 = sorted(th_c)[5], sorted(th_c)[6]
    want = 0.01 * 2.0 * abs(th_c[t2]["f"] - th_c[t1]["f"])
    assert out_c[t2][2] == pytest.approx(want)
    assert out_c[t2][0] == pytest.approx(out_c[t2][1] - want)


def test_umv_weights_are_constant_in_vol(vm: ModuleType) -> None:
    sl, zz = synth(300)
    sc = {"f": dict.fromkeys(sl["f"], 1.0)}
    out, th = vm.walk(sl, sc, {"f": 0.0}, None, min_hist=120)
    ts = sorted(th)
    # expanding-window MV weight changes only slowly: no month-to-month jump with z
    steps = np.abs(np.diff([th[t]["f"] for t in ts]))
    assert steps.max() < 0.2 * abs(th[ts[0]]["f"]) + 1e-9
    assert len(out) == len(ts)


def test_late_sleeve_enters_after_min_hist_and_shrinks_window(vm: ModuleType) -> None:
    ms = months(300)
    rng = np.random.default_rng(3)
    a = {m: 0.005 + rng.normal(0, 0.03) for m in ms}
    b = {m: 0.005 + rng.normal(0, 0.03) for m in ms[150:]}
    sc = {"a": dict.fromkeys(ms, 1.0), "b": dict.fromkeys(ms, 1.0)}
    _, th = vm.walk({"a": a, "b": b}, sc, {"a": 0.0, "b": 0.0}, None, min_hist=60)
    assert "b" not in th[ms[209]]
    assert "b" in th[ms[210]]
