"""The coin-cap-2 core (research/lib/coin_cap2_core.py) counts episodes and falls as the card says.

- All coin falls of one market fall are one episode; coin-own falls more than 30 days apart are
  separate episodes, closer ones one.
- The deepest fall of a P&L path has both ends inside the window and scales with the slot.
- The sign test and the window follow their definitions.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
k2: Any = importlib.import_module("coin_cap2_core")


def test_common_falls_are_one_episode() -> None:
    market = [(1000, 1200)]
    falls = [k2.Fall(j, 950 + 10 * j, 1300, -1) for j in range(20)]  # tops 950 .. 1140
    keys, order = k2.episodes(falls, market)
    assert set(keys) == {"market-0"} and order == ["market-0"]
    assert k2.effective_number(keys) == pytest.approx(1.0)


def test_coin_own_falls_split_on_gaps() -> None:
    market = [(1000, 1200)]
    falls = [
        k2.Fall(0, 100, 150, 200),
        k2.Fall(1, 120, 160, 210),  # 20 days after the first: same run
        k2.Fall(2, 400, 450, 500),  # far from both: a new run
        k2.Fall(3, 939, 990, -1),  # 61 days before the market top: coin-own
        k2.Fall(4, 1201, 1300, -1),  # after the market low: coin-own, 262 days after the last
    ]
    keys, order = k2.episodes(falls, market)
    assert keys == ["own-0", "own-0", "own-1", "own-2", "own-3"]
    assert order == ["own-0", "own-1", "own-2", "own-3"]


def test_order_is_by_first_top() -> None:
    keys, order = k2.episodes(
        [k2.Fall(0, 2000, 2100, -1), k2.Fall(1, 1050, 1100, -1)], [(1000, 1200)]
    )
    assert order == ["market-0", "own-0"]


def test_deepest_fall() -> None:
    r = np.array([0.1, 0.1, -0.3, 0.05, -0.1, 0.4])
    assert k2.deepest_fall(r) == pytest.approx(0.35)
    assert k2.deepest_fall(0.4 * r) == pytest.approx(0.4 * 0.35)  # a cap scales M exactly
    assert k2.deepest_fall(np.array([-0.2, 0.1])) == pytest.approx(0.2)  # from 0 at the start
    assert k2.deepest_fall(np.array([0.1, 0.2])) == 0.0


def test_window() -> None:
    assert k2.window(k2.Fall(0, 500, 600, 700), 5000) == (409, 700)
    assert k2.window(k2.Fall(0, 50, 600, 2000), 5000) == (0, 965)  # at most a year after the low
    assert k2.window(k2.Fall(0, 500, 600, -1), 800) == (409, 799)  # open: end of data


def test_sign_p_and_index() -> None:
    assert k2.sign_p(10, 10) == pytest.approx(1 / 1024)
    assert k2.sign_p(0, 5) == pytest.approx(1.0)
    assert k2.sign_p(7, 10) == pytest.approx(176 / 1024)
    ret = np.array([[0.1, -0.1], [0.2, 0.5]])
    member = np.array([[True, True], [True, False]])
    assert k2.market_index(ret, member) == pytest.approx([1.0, 1.2])
