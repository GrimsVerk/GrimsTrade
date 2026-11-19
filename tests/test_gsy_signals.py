"""The GSY run-up signals (research/lib/gsy_signals.py) use only bars up to the decision and
count run-ups, flags and crashes the way the card (research/cards/gsy-runup.md) says."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
g: Any = importlib.import_module("gsy_signals")


def _daily(n: int, seed: int, drift: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    ords = 700_000 + np.arange(n) + np.arange(n) // 5 * 2  # weekdays only
    close = 100 * np.exp(np.cumsum(rng.normal(drift, 0.02, n)))
    return ords.astype(np.int64), close


def test_runup_needs_raw_and_net_of_market() -> None:
    ords = np.arange(800_000, 800_000 + 1000, dtype=np.int64)
    ind = np.where(ords - ords[0] >= 730, 250.0, 100.0)  # +150% after two years
    flat = np.full(len(ords), 100.0)
    up = np.where(ords - ords[0] >= 730, 220.0, 100.0)  # market +120%
    ru_flat = g.runup(ords, ind, ords, flat, 1.0)
    assert not ru_flat[:730].any()
    assert ru_flat[730]
    assert not g.runup(ords, ind, ords, flat, 1.5 + 1e-9)[730]
    assert not g.runup(ords, ind, ords, up, 1.0)[730]  # only +30% net of market


def test_flag_lasts_two_years_after_the_last_runup() -> None:
    ords = np.arange(0, 2000, dtype=np.int64)
    ru = np.zeros(2000, bool)
    ru[100] = ru[300] = True
    f = g.flag_active(ords, ru)
    assert not f[99] and f[100] and f[300 + 730] and not f[300 + 731]


def test_signals_are_causal() -> None:
    ords, close = _daily(1500, 1, 0.002)
    m_ords, m_close = _daily(1500, 2)
    rng = np.random.default_rng(3)
    k = 1100
    junk = close.copy()
    junk[k:] = close[k - 1] * np.exp(rng.normal(0, 0.2, 1500 - k))  # a different future
    mjunk = m_close.copy()
    mjunk[k:] = m_close[k - 1] * 3

    def all_signals(c: np.ndarray, m: np.ndarray) -> list[np.ndarray]:
        ru = g.runup(ords, c, m_ords, m, 0.5)
        return [ru, g.flag_active(ords, ru), g.below_sma(ords, c), g.vol_rising(ords, c)]

    for a, b in zip(all_signals(close, m_close), all_signals(junk, mjunk), strict=True):
        assert np.array_equal(a[:k], b[:k])


def test_below_sma_and_vol_rising() -> None:
    ords = np.arange(0, 1000, dtype=np.int64)
    rising = 100 + np.arange(1000.0)
    assert not g.below_sma(ords, rising).any()
    assert g.below_sma(ords, rising[::-1].copy())[400]
    step = np.tile([0.001, -0.001], 500)
    late = step.copy()
    late[800:] *= 50  # rough from bar 800
    early = step.copy()
    early[400:600] *= 50  # rough 400..599, calm after
    assert g.vol_rising(ords, np.exp(np.cumsum(late)))[900]
    assert not g.vol_rising(ords, np.exp(np.cumsum(early)))[900]


def test_crashes_one_per_peak() -> None:
    ords = np.arange(8, dtype=np.int64)
    close = np.array([100, 120, 90, 70, 60, 80, 47, 30.0])
    out = g.crashes(ords, close)
    # 120 -> 70 is the first crash; the peak restarts at 70, then 80 -> 47 is the second.
    assert [(c.peak, c.x) for c in out] == [(1, 3), (5, 6)]


def test_episodes_first_month_and_window() -> None:
    n = 80
    ret = np.zeros((n, 1))
    ret[1:25, 0] = 2.2 ** (1 / 24) - 1  # +120% over months 1..24
    ret[30:40, 0] = -0.06  # -46% from month 29
    mkt = np.zeros(n)
    idx = g.index_of(ret)
    mk = g.index_of(mkt[:, None])[:, 0]
    eps, base, _, _ = g.episodes(idx, mk, 1.0, 24, 50)
    assert [e.month for e in eps] == [24]  # months 25..48 hold no new episode
    assert eps[0].crash and eps[0].strict
    assert base == 27  # rows 24..50, each with 24 months after
