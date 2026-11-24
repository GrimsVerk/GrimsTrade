"""Invest 1 signals use only data public at the decision (research/lib/invest1.py, card lags)."""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import replace
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
import pytest

PATH = Path(__file__).resolve().parents[1] / "research" / "lib" / "invest1.py"


@pytest.fixture(scope="module")
def inv() -> ModuleType:
    sys.path.insert(0, str(PATH.parent))
    spec = importlib.util.spec_from_file_location("invest1_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def synthetic(inv: Any, seed: int) -> Any:
    rng = np.random.default_rng(seed)
    n = inv.N
    S = rng.normal(0.007, 0.04, n)
    rf = np.abs(rng.normal(0.003, 0.001, n))
    y = 0.04 + np.cumsum(rng.normal(0, 0.001, n)) * 0.1
    P = 10 * np.exp(np.cumsum(rng.normal(0.003, 0.03, n)))
    E = P / 15 * np.exp(rng.normal(0, 0.1, n))
    CPI = 10 * np.exp(np.cumsum(rng.normal(0.002, 0.004, n)))
    return inv.Raw(P=P, E=E, CPI=CPI, y=y, rf=rf, S=S, B=inv.bond_returns(y), realtr=P.copy())


def scramble_after(inv: Any, raw: Any, t: int, seed: int) -> Any:
    """Replace every value the card forbids at the decision at the end of month t."""
    rng = np.random.default_rng(seed)

    def mess(a: np.ndarray, last_ok: int) -> np.ndarray:
        b = a.copy()
        b[last_ok + 1 :] = rng.uniform(0.5, 2.0, len(b) - last_ok - 1) * np.nanmean(a)
        return b

    y = mess(raw.y, t)
    return replace(
        raw,
        P=mess(raw.P, t),
        E=mess(raw.E, t - inv.LAG_E),
        CPI=mess(raw.CPI, t - inv.LAG_CPI),
        y=y,
        rf=mess(raw.rf, t),
        S=mess(raw.S, t),
        B=np.concatenate([raw.B[: t + 1], inv.bond_returns(y)[t + 1 :]]),
    )


@pytest.mark.parametrize("t_frac", [0.3, 0.6, 0.95])
def test_signals_ignore_the_future(inv: Any, t_frac: float) -> None:
    raw = synthetic(inv, 1)
    t = int(inv.N * t_frac)
    clean = inv.signals(raw)
    dirty = inv.signals(scramble_after(inv, raw, t, 2))
    for name, a in clean.items():
        assert a[t] == pytest.approx(dirty[name][t], nan_ok=True), name
        assert np.allclose(a[: t + 1], dirty[name][: t + 1], equal_nan=True), name
    p_clean = inv.pctile(clean["ecy"])
    p_dirty = inv.pctile(dirty["ecy"])
    assert np.array_equal(p_clean[: t + 1], p_dirty[: t + 1])


def test_lags_bind(inv: Any) -> None:
    """The last allowed month does move the signal (the lag is not longer than written)."""
    raw = synthetic(inv, 3)
    t = int(inv.N * 0.8)
    base = inv.signals(raw)
    E = raw.E.copy()
    E[t - inv.LAG_E] *= 3
    CPI = raw.CPI.copy()
    CPI[t - inv.LAG_CPI] *= 1.5
    assert inv.signals(replace(raw, E=E))["ey"][t] != base["ey"][t]
    assert inv.signals(replace(raw, CPI=CPI))["infl"][t] != base["infl"][t]


def test_weights_earn_the_next_month(inv: Any) -> None:
    """A rule that is all stocks only in month k earns month k+1's stock return."""
    n = inv.N
    S = np.zeros(n)
    rf = np.zeros(n)
    B = np.zeros(n)
    S[101] = 0.10
    ws = np.zeros(n)
    ws[100] = 1.0
    run = inv.simulate(ws, np.zeros(n), S, B, rf, 50, 150, cost=0.0)
    assert run.ret[101 - 50] == pytest.approx(0.10)
    assert run.ret.sum() == pytest.approx(0.10)
