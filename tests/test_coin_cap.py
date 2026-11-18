"""The coin-cap core (research/lib/coin_cap_core.py) does what the card says and has no look-ahead.

- The cap never raises a coin weight, never leaves the coins above the cap or the book above 1,
  and changes nothing when the cap does not bind.
- The walk-forward pick for a year does not change when returns in or after that year are
  scrambled, and the stitched series before that year is unchanged too.
"""

from __future__ import annotations

import importlib
import sys
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
core: Any = importlib.import_module("coin_cap_core")  # no harness import: it changes global state

COINS = frozenset({"BTC", "ETH"})


def test_cap_cash_and_rest() -> None:
    w = {"BTC": 1 / 6, "ETH": 1 / 6, "SPY": 1 / 6, "GLD": 1 / 6}
    cash = core.cap_coins(w, COINS, 0.10, "cash")
    assert cash["BTC"] == pytest.approx(0.05) and cash["ETH"] == pytest.approx(0.05)
    assert cash["SPY"] == pytest.approx(1 / 6) and sum(cash.values()) == pytest.approx(0.10 + 1 / 3)
    rest = core.cap_coins(w, COINS, 0.10, "rest")
    assert rest["BTC"] == pytest.approx(0.05) and sum(rest.values()) == pytest.approx(
        sum(w.values())
    )
    assert rest["SPY"] == pytest.approx(rest["GLD"]) and rest["SPY"] > 1 / 6


def test_cap_never_raises_coins_or_levers() -> None:
    rng = np.random.default_rng(0)
    syms = ["BTC", "ETH", "SPY", "TLT", "GLD", "QQQ"]
    for _ in range(300):
        held = [s for s in syms if rng.random() < 0.6]
        w = {s: 1 / 6 for s in held}
        for cap in (0.10, 0.15, 0.20, 0.25):
            for mode in ("cash", "rest"):
                out = core.cap_coins(w, COINS, cap, mode)
                assert set(out) == set(w)
                assert sum(out[s] for s in out if s in COINS) <= cap + 1e-12
                assert all(out[s] <= w[s] + 1e-12 for s in out if s in COINS)
                assert sum(out.values()) <= sum(w.values()) + 1e-12 <= 1 + 1e-9
        assert core.cap_coins(w, COINS, 1.0, "rest") == w
    assert core.cap_coins({"BTC": 0.5}, COINS, 0.2, "rest") == {"BTC": pytest.approx(0.2)}
    with pytest.raises(ValueError):
        core.cap_coins({}, COINS, 0.2, "other")


def test_walk_forward_ignores_the_future() -> None:
    rng = np.random.default_rng(1)
    start = date(2013, 1, 1).toordinal()
    n = 365 * 8
    ords = np.arange(start, start + n)
    order = ["a", "b", "c"]
    rets = {k: rng.normal(0.0005, 0.02, n) for k in order}
    years = range(2015, 2021)
    picks, out = core.walk_forward(ords, rets, order, years, "b")
    cut = date(2018, 1, 1).toordinal()
    later = ords >= cut
    other = {k: np.where(later, rng.normal(0, 0.05, n), v) for k, v in rets.items()}
    picks2, out2 = core.walk_forward(ords, other, order, years, "b")
    assert all(picks[y] == picks2[y] for y in range(2015, 2019))  # 2018's pick uses < 2018 only
    assert np.array_equal(out[~later], out2[~later])
    # before the first year the default is carried
    first = ords < date(2015, 1, 1).toordinal()
    assert np.array_equal(out[first], rets["b"][first])
    # each year's stitched returns are the pick's own
    m = (ords >= date(2016, 1, 1).toordinal()) & (ords < date(2017, 1, 1).toordinal())
    assert np.array_equal(out[m], rets[picks[2016]][m])


def test_score_by_hand() -> None:
    r = np.array([0.1, -0.5, 0.2])
    growth = float(np.log1p(r).mean() * 365)
    assert core.score(r) == pytest.approx(growth / 0.5)
    assert core.score(np.array([0.01, 0.01])) == float("-inf")  # no loss: no ratio
