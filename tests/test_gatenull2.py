"""The gate-null-2 functions compute what research/cards/gate-null-2.md says they do."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _mod(name: str) -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module(name)
    finally:
        sys.path.remove(str(LIB))


def test_nw_slope_t_equals_the_gates_own_driscoll_kraay() -> None:
    g, e11 = _mod("gatenull2"), _mod("wide11_events")
    rng = np.random.default_rng(5)
    n = 240
    x = g.ar1(rng, n, 0.9)
    y = 0.1 * x + rng.standard_normal(n)
    for lags in (0, 3, 12):
        b, t = g.nw_slope_t(y, np.column_stack([x, x[::-1]]), lags)
        bb, tt, _ = e11.ols_dk([np.ones(n), x], y, np.arange(n), lags)
        assert abs(b[0] - bb[1]) < 1e-10
        assert abs(t[0] - tt[1]) < 1e-8


def test_surrogates_keep_what_they_promise() -> None:
    g = _mod("gatenull2")
    rng = np.random.default_rng(1)
    x = g.ar1(rng, 301, 0.95)
    ph = g.phase_surrogates(rng, x, 5)
    assert ph.shape == (301, 5)
    amp = np.abs(np.fft.rfft(x - x.mean()))
    for j in range(5):
        assert np.allclose(np.abs(np.fft.rfft(ph[:, j] - ph[:, j].mean())), amp, atol=1e-8)
        assert abs(ph[:, j].mean() - x.mean()) < 1e-10
    ia = g.iaaft_surrogates(rng, x, 5)
    for j in range(5):
        assert np.array_equal(np.sort(ia[:, j]), np.sort(x))  # same values
        assert g.acf1(ia[:, j]) > 0.8  # persistence kept
        assert not np.array_equal(ia[:, j], x)
    bb = g.block_bootstrap(rng, x, 3, 24)
    assert bb.shape == (301, 3) and set(np.round(bb.ravel(), 12)) <= set(np.round(x, 12))
    ro = g.rotations(rng, x, 40, 24)
    assert ro.shape == (301, 40)
    assert all(np.array_equal(np.sort(ro[:, j]), np.sort(x)) for j in range(40))


def test_shifted_and_rank() -> None:
    g = _mod("gatenull2")
    ext = np.arange(g.PRE + 10 + g.POST, dtype=float)
    m = g.shifted(ext, [25, -13], g.PRE, 10)
    assert m[0, 0] == g.PRE - 25 and m[0, 1] == g.PRE + 13
    assert g.rank_high(1.0, np.array([0.0, 2.0, 1.0])) == 2  # only 2.0 is above: rank 2
    assert list(g.rank_high(np.array([3.0, -1.0]), np.array([[0.0, 1.0], [0.0, 1.0]]))) == [1, 3]


def test_surrogate_doses_and_record() -> None:
    g = _mod("gatenull2")
    d = {m: float(v) for m, v in enumerate(g.ar1(np.random.default_rng(3), 200, 0.9))}
    a, b = g.surrogate_doses(d, "iaaft", 4), g.surrogate_doses(d, "iaaft", 4)
    assert a == b  # deterministic
    assert set(a[0]) == set(d) and sorted(a[0].values()) == sorted(d.values())
    rec = g.rescore_record(
        "Wx", "", -1, -3.0, 1, -3.0, [0.0] * 40, [-3.5] + [0.0] * 39, [], [1.0, 2.0, 1.5]
    )
    assert rec["shift_rank"] == 1 and rec["shift_pass"] is True
    assert rec["phase_rank"] == 2 and rec["phase_pass"] is True
    assert "iaaft_rank" not in rec
