"""The gate-power functions compute what research/gate-power.md says they do."""

from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _gp() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("gatepower")
    finally:
        sys.path.remove(str(LIB))


def _e11() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide11_events")
    finally:
        sys.path.remove(str(LIB))


def test_dk_fit_matches_the_gates_ols_dk() -> None:
    gp, e11 = _gp(), _e11()
    rng = np.random.default_rng(1)
    n = 300
    week = np.repeat(np.arange(150), 2)
    week = np.delete(week, [10, 11])  # a missing week: lags count week distance
    a = (np.arange(len(week)) % 2).astype(float)
    dose = rng.normal(size=len(week))
    dose[5] = np.nan
    ctrl = rng.normal(size=len(week))
    y = 0.3 * dose + rng.normal(size=len(week))
    cols = [a, 1 - a, dose, ctrl]
    b_slow, t_slow, _ = e11.ols_dk(cols, y, week, 4)
    b, t = gp.dk_fit(np.column_stack(cols), y, week, 4, 2)
    assert n > 0
    assert math.isclose(b, b_slow[2], rel_tol=1e-12)
    assert math.isclose(t, t_slow[2], rel_tol=1e-10)


def test_position_is_trailing_mean_with_unit_sd() -> None:
    gp = _gp()
    z = np.array([np.nan, 1.0, 0.0, 2.0, 0.0, 0.0])
    x = gp.position(z, 2, np.ones(6, dtype=bool))
    raw = np.array([0.0, 0.5, 0.5, 1.0, 1.0, 0.0])
    assert np.allclose(x, raw / raw.std())


def test_window_sum_and_bounds() -> None:
    gp = _gp()
    r = np.arange(10, dtype=float)
    out = gp.window_sum(r, np.array([0, 3, 8, -1]), 3)
    assert out[0] == 3 and out[1] == 12
    assert math.isnan(out[2]) and math.isnan(out[3])


def test_pass_rule_and_rank() -> None:
    gp = _gp()
    pl = [0.5] * 38 + [2.5, 3.0]
    assert not gp.passes(0.1, 2.2, pl)  # rank 3
    assert gp.passes(0.1, 2.7, pl)  # rank 2
    assert not gp.passes(-0.1, 3.5, pl)  # wrong sign
    assert not gp.passes(0.1, 1.9, [0.0] * 40)  # t below 2


def test_mde_interpolates_and_reports_nan() -> None:
    gp = _gp()
    fs = [0.0, 0.1, 0.2]
    assert math.isclose(gp.mde(fs, [0.05, 0.5, 0.9]), 0.1 + 0.3 / 0.4 * 0.1)
    assert math.isnan(gp.mde(fs, [0.05, 0.2, 0.5]))


def test_ir_and_added_sharpe() -> None:
    gp = _gp()
    assert math.isclose(gp.ir(0.1, 52), 0.1 * math.sqrt(52))
    assert math.isclose(gp.added_sharpe(math.sqrt(1.35**2 - 1.05**2)), 0.30)


def test_n_eff_of_white_noise_and_of_a_persistent_series() -> None:
    gp = _gp()
    rng = np.random.default_rng(2)
    e = rng.normal(size=4000)
    assert 3000 < gp.n_eff(e) <= 4000
    ar = np.zeros(4000)
    for i in range(1, 4000):
        ar[i] = 0.9 * ar[i - 1] + e[i]
    assert gp.n_eff(ar) < 400  # 1 + 2 * 0.9 / 0.1 = 19 -> about 210


def test_simulate_finds_a_large_planted_effect_and_not_a_zero_one() -> None:
    gp = _gp()
    rng = np.random.default_rng(3)
    n = 400
    noise = rng.normal(size=(20, n)) * 0.02
    z = rng.normal(size=n)
    pos = gp.position(z, 1, np.ones(n, dtype=bool))
    rows = np.arange(n)
    period = rows.astype(float)

    def fit(dose: Any, y: Any, ctrl: Any, m: Any) -> tuple[float, float]:
        x = np.column_stack([np.ones(n), dose])
        return gp.dk_fit(x, y, period, 0, 1)  # type: ignore[no-any-return]

    shifts = [np.roll(z, k) for k in range(20, 60)]
    d = gp.Design(
        "toy",
        ["A"],
        lambda s: {"A": noise[s]},
        {"A": 0.02},
        {"A": pos},
        np.zeros(n, dtype=int),
        rows,
        1,
        z,
        shifts,
        None,
        fit,
    )
    res = gp.simulate(d, fs=(0.0, 0.5), n_sim=20)
    assert res.rate_old[1] >= 0.9
    assert res.rate_old[0] <= 0.2
    assert len(res.null_old) == 20 * 40
