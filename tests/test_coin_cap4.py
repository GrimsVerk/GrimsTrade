"""The coin-cap-4 core (research/lib/coin_cap4_core.py) behaves as the card says.

- The price-drawdown condition at row t does not change when prices from row t - shift + 1 on
  are scrambled (no look-ahead), and an unknown high is not held.
- The band is matched on time held only, ties to the smaller band.
- Time under water is the longest run below the running high and does not change with scale.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
k4: Any = importlib.import_module("coin_cap4_core")


def test_price_dd_no_look_ahead() -> None:
    rng = np.random.default_rng(1)
    px = np.exp(np.cumsum(rng.normal(0, 0.05, (800, 3)), axis=0))
    t, shift = 600, 1
    a = k4.pstop_ok(k4.price_dd(px, shift), 0.25)
    px2 = px.copy()
    px2[t - shift + 1 :] = rng.random((800 - t + shift - 1, 3)) * 100
    b = k4.pstop_ok(k4.price_dd(px2, shift), 0.25)
    assert (a[: t + 1] == b[: t + 1]).all()
    assert not a[0].any()  # unknown (lagged) value: not held


def test_price_dd_definition() -> None:
    px = np.array([[100.0], [80.0], [90.0], [70.0]])
    dd = k4.price_dd(px, 0)
    assert np.allclose(dd[:, 0], [0.0, -0.2, -0.1, -0.3])
    assert (k4.pstop_ok(dd, 0.2)[:, 0] == [True, True, True, False]).all()


def test_match_x_closest_and_ties() -> None:
    assert k4.match_x(lambda x: x, 0.253) == 0.25
    assert k4.match_x(lambda x: 0.5, 0.3) == 0.10  # all tie: the smallest band


def test_tuw() -> None:
    r = np.array([0.1, -0.2, 0.05, 0.05, 0.2, -0.1, 0.0])
    # path 0, .1, -.1, -.05, 0, .2, .1, .1 -> under on days 2-4 (3) and 6-7 (2)
    assert k4.tuw(r) == 3
    assert k4.tuw(0.4 * r) == k4.tuw(r)
    assert k4.tuw(np.zeros(5)) == 0
    eq = np.array([1.0, 1.2, 1.0, 1.1, 1.3, 1.25])
    best, deep = k4.equity_tuw(eq)
    assert best == 2 and abs(deep - 1 / 6) < 1e-12
