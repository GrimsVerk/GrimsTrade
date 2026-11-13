"""The short-1 simulator (research/lib/short_engine.py) books shorts and funding the way the
card in research/short-1.md says.

- A short gains when the price falls and loses when it rises, by its weight.
- Positive funding: longs pay it, shorts receive it, in proportion to the weight.
- A position decided at the close of day t earns nothing from day t's own move.
- Entering costs the cost per side on the absolute weight change, long or short.
- Market-neutral weights: +0.5 / -0.5 split over the top and bottom thirds.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _se() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("short_engine")
    finally:
        sys.path.remove(str(LIB))


def test_short_gains_on_fall_and_receives_funding() -> None:
    se = _se()
    px = np.array([[100.0], [100.0], [90.0], [99.0]])
    fund = np.array([[0.0], [0.0], [0.001], [0.002]])
    tg = np.array([[-1.0]])
    run = se.simulate(px, fund, tg, np.array([1]), 0.0, 0)
    # day 1 is the entry close: no return from its own move
    assert run.r[0] == 0.0
    # day 2: price -10%, short 1x gains 10%, receives 0.1% funding
    assert np.isclose(run.r[1], 0.10 + 0.001)
    assert np.isclose(run.funding[1], 0.001)


def test_long_pays_funding_and_cost_is_per_unit_change() -> None:
    se = _se()
    px = np.full((4, 2), 100.0)
    fund = np.full((4, 2), 0.001)
    tg = np.array([[0.5, -0.5]])
    run = se.simulate(px, fund, tg, np.array([0]), 0.001, 0)
    # funding nets out (long pays 0.05%, short receives 0.05%): flat prices, zero return
    assert np.allclose(run.r[1:], 0.0) and np.allclose(run.funding, 0.0)
    tg2 = np.array([[1.0, 0.0]])
    run2 = se.simulate(px, None, tg2, np.array([0]), 0.001, 0)
    run3 = se.simulate(px, fund, tg2, np.array([0]), 0.001, 0)
    # the first entry's cost (10 bps) lands on the first returned day
    assert np.isclose(run2.r[0], -0.001) and np.allclose(run2.r[1:], 0.0)
    assert np.isclose(run3.r[0], (1 - 0.001) ** 2 - 1)
    assert np.allclose(run3.r[1:], -0.001, atol=1e-5)  # weight drifts as equity pays
    # entry cost: |0.5| + |-0.5| = 1 unit x 10 bps, booked on the entry day
    px[0] = [100.0, 100.0]
    run4 = se.simulate(px, None, tg, np.array([1]), 0.001, 0)
    assert np.isclose(run4.r[0], -0.001)


def test_long_short_weights() -> None:
    se = _se()
    sig = np.array([5.0, 1.0, 3.0, 2.0, 4.0, 0.0])
    m = np.ones(6, bool)
    w = se.long_short(sig, m)
    assert np.isclose(w.sum(), 0.0) and np.isclose(np.abs(w).sum(), 1.0)
    assert w[0] > 0 and w[4] > 0 and w[1] < 0 and w[5] < 0 and w[2] == 0 and w[3] == 0


def test_spells_merge_short_gaps() -> None:
    se = _se()
    neg = np.zeros(200, bool)
    neg[0:40] = True
    neg[50:90] = True  # gap of 10 days: same spell
    neg[150:160] = True  # too short
    assert se.spells(neg) == 1
