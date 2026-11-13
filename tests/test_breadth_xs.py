"""The breadth-1 cross-sectional engine (research/lib/breadth_xs.py) has no look-ahead and
charges costs the way the card says.

- A position decided on day t earns only returns after the close of t + skip.
- A signal that knows the coming holding return has IC 1; that return lagged by one holding
  period (what a real signal could know) does not.
- Costs: entering a full position costs exactly the cost per side once.
- Rolling helpers of breadth_books use only the current and earlier rows.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
import breadth_xs as xs  # noqa: E402

bb: Any = __import__("breadth_books")


def _prices(days: int, n: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.exp(np.cumsum(rng.normal(0, 0.02, (days, n)), axis=0))


def test_position_earns_only_after_its_base_day() -> None:
    px = np.ones((10, 1))
    px[3:] = 2.0  # the jump happens on day 3
    targets = np.ones((1, 1))
    # set at the close of day 3: the jump is before it, nothing is earned
    r = xs.simulate(px, targets, np.array([3]), np.zeros(1), 3)
    assert np.allclose(r, 0)
    # set at the close of day 2: the whole jump is earned on day 3
    r = xs.simulate(px, targets, np.array([2]), np.zeros(1), 2)
    assert np.isclose(r[0], 1.0) and np.allclose(r[1:], 0)


def test_entry_costs_one_side() -> None:
    px = np.ones((5, 1))
    r = xs.simulate(px, np.ones((1, 1)), np.array([1]), np.full(1, 0.003), 0)
    assert np.isclose(r[0], -0.003) and np.allclose(r[1:], 0)


def test_ic_alignment() -> None:
    px = _prices(400, 30)
    dec = np.arange(10, 390, 7)
    d, b, e = xs.schedule(len(px), dec, 1)
    fr = xs.fwd_logret(px, b, e)
    oracle = np.full(px.shape, np.nan)
    oracle[d] = fr
    elig = np.ones(px.shape, bool)
    assert xs.ic_stats(px, elig, oracle, dec, 1).mean > 0.99
    lagged = np.full(px.shape, np.nan)
    lagged[d[1:]] = fr[:-1]  # last period's return: known at the decision
    assert abs(xs.ic_stats(px, elig, lagged, dec, 1).mean) < 0.2


def test_rolling_helpers_do_not_look_ahead() -> None:
    a = _prices(200, 3)
    b = a.copy()
    b[120:] = 1e6  # scramble the future
    for f in (lambda x: bb.roll_mean(x, 30), lambda x: bb.roll_std(x, 30),
              lambda x: bb.roll_median(x, 30), lambda x: bb.logret(x, 28, 0)):  # fmt: skip
        assert np.allclose(f(a)[:120], f(b)[:120], equal_nan=True)
