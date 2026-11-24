"""The cointop-1 core (research/lib/cointop1_core.py) has no look-ahead and scores as the card says.

- `find_tops` on a hand-made series: a top is a high followed by a halving; a low is settled by
  a doubling; a rise the series ends on is "open", not a top.
- Rule inputs at row t do not change when later prices are scrambled.
- The breadth series for day d uses no price stamped after d - 1.
- A paper position set at the close of day b earns only the returns after b and pays its cost
  on b.
- The pooled score, the smoothed choice of a setting and the AUC, on numbers worked by hand.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
xs: Any = importlib.import_module("breadth_xs")  # no harness import: it changes global state
core: Any = importlib.import_module("cointop1_core")


def _prices(days: int, n: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.exp(np.cumsum(rng.normal(0, 0.04, (days, n)), axis=0))


def _scrambled(px: np.ndarray, after: int, seed: int = 1) -> np.ndarray:
    out = px.copy()
    rng = np.random.default_rng(seed)
    out[after + 1 :] = px[after + 1 :] * np.exp(rng.normal(0, 0.5, px[after + 1 :].shape))
    return out


def test_find_tops_hand_made() -> None:
    p = np.array([1.0, 2.0, 4.0, 3.0, 2.0, 1.0, 1.5, 2.0, 5.0])
    tops, open_high = core.find_tops(p)
    assert [(t.top, t.halved, t.low, t.settled) for t in tops] == [(2, 4, 5, 7)]
    assert open_high == 8  # the series ends on a rise: an open high, not a top


def test_find_tops_unsettled_low_and_gaps() -> None:
    p = np.array([np.nan, 10.0, np.nan, 4.0, 3.0, 5.0])
    tops, open_high = core.find_tops(p)
    assert [(t.top, t.halved, t.low, t.settled) for t in tops] == [(1, 3, 4, -1)]
    assert open_high == -1
    assert core.find_tops(np.full(5, np.nan)) == ([], -1)
    # a fall of less than half is not a top
    assert core.find_tops(np.array([1.0, 2.0, 1.1, 2.5]))[0] == []


def test_rule_inputs_ignore_later_prices() -> None:
    px = _prices(700, 5)
    t = 520
    other = _scrambled(px, t)
    fs: list[Any] = [
        lambda p: core.ewma_vol(p, 60),
        lambda p: core.dd_1y(p, core.ewma_vol(p, 60)),
        lambda p: core.zscore(p, core.ewma_vol(p, 60), 28),
        lambda p: core.roll_max(p, 365),
        lambda p: xs.logret(p, 91, 0),
    ]
    for f in fs:
        a, b = f(px), f(other)
        np.testing.assert_array_equal(a[: t + 1], b[: t + 1])
        assert not np.array_equal(a[t + 1 :], b[t + 1 :], equal_nan=True)


def test_rule_positions_ignore_later_prices() -> None:
    px = _prices(700, 5)
    t = 520
    other = _scrambled(px, t)

    def holds(p: np.ndarray) -> np.ndarray:
        vol = core.ewma_vol(p, 60)
        stop = core.stop_cond(xs.lag(core.dd_1y(p, vol), 1), 0.5)
        fade = core.fade_cond(xs.lag(xs.logret(p, 28, 0), 1))
        return np.stack([stop, fade])

    # lagged one day, so the position on day t + 1 is still made of prices stamped <= t
    np.testing.assert_array_equal(holds(px)[:, : t + 2], holds(other)[:, : t + 2])


def test_breadth_uses_no_price_after_the_day_before() -> None:
    px = _prices(400, 40)
    universe = np.ones(px.shape, bool)
    d = 300

    def share(p: np.ndarray) -> np.ndarray:
        out: np.ndarray = core.breadth_share(xs.lag(xs.logret(p, 28, 0), 1), universe)
        return out

    other = _scrambled(px, d - 1)
    a, b = share(px), share(other)
    np.testing.assert_array_equal(a[: d + 1], b[: d + 1])
    assert not np.array_equal(a[d + 1 :], b[d + 1 :])
    # what day d shows is the share of coins up over the 28 days ending d - 1
    want = (np.log(px[d - 1] / px[d - 29]) > 0).mean()
    assert a[d] == want


def test_breadth_needs_enough_coins_and_unknown_counts_as_met() -> None:
    r = np.array([[0.1, -0.1, 0.2, np.nan], [0.1, 0.1, np.nan, np.nan], [-1.0, -1.0, -1.0, 0.5]])
    universe = np.ones(r.shape, bool)
    share = core.breadth_share(r, universe, min_coins=3)
    np.testing.assert_allclose(share, [2 / 3, np.nan, 0.25])
    cond = core.breadth_cond(share, 4)
    assert cond.shape == (3, 4)
    assert cond[:, 0].tolist() == [True, True, False]


def test_paper_earns_only_after_the_set_day_and_pays_the_cost_once() -> None:
    px = np.array([[100.0], [110.0], [121.0], [133.1], [133.1], [146.41]])
    hold = np.array([[1.0], [0.0]])
    base = np.array([1, 3])
    ret, pos = core.paper(px, hold, base, cost=0.003)
    assert pos[:, 0].tolist() == [0, 0, 1, 1, 0, 0]
    np.testing.assert_allclose(ret[:, 0], [0, -0.003, 0.1, 1.1 * (1 - 0.003) - 1, 0, 0])


def test_paper_carries_a_stopped_price() -> None:
    px = np.array([[1.0], [2.0], [np.nan], [np.nan]])
    ret, _ = core.paper(px, np.array([[1.0]]), np.array([0]), cost=0.0)
    np.testing.assert_allclose(ret[:, 0], [0, 1.0, 0, 0])


def test_pooled_sharpe_and_coin_days() -> None:
    ret = np.array([[0.01, 9.0], [0.03, 9.0], [-0.02, 0.02]])
    mask = np.array([[True, False], [True, False], [True, True]])
    x = np.array([0.01, 0.03, -0.02, 0.02])
    assert np.isclose(core.pooled_sharpe(ret, mask), x.mean() / x.std() * np.sqrt(365))
    univ = np.array([[True, False], [False, False]])
    days = core.coin_days(univ, np.array([1, 4]), 7)
    # in force on days 2..4, plus the day on either side; the other coin never counts
    assert days[:, 0].tolist() == [False, True, True, True, True, True, False]
    assert not days[:, 1].any()


def test_pooled_boot_of_a_series_against_itself_is_zero() -> None:
    rng = np.random.default_rng(0)
    ret = rng.normal(0.001, 0.02, (300, 6))
    mask = np.ones(ret.shape, bool)
    d, p, lo, hi = core.pooled_boot(ret, ret, mask, draws=50)
    assert (d, lo, hi) == (0.0, 0.0, 0.0)
    assert p == 1.0
    d, p, _, _ = core.pooled_boot(ret + 0.01, ret, mask, draws=50)
    assert d > 0
    assert p == 0.0


def test_choose_smooths_and_breaks_ties_to_the_looser_setting() -> None:
    best, sm = core.choose([0.0, 3.0, 0.0, 2.5])
    np.testing.assert_allclose(sm, [1.5, 1.0, 5.5 / 3, 1.25])
    assert best == 2  # the lone spike at index 1 is not chosen
    assert core.choose([1.0, 1.0, 1.0, 1.0])[0] == 3


def test_auc() -> None:
    y = np.array([False, False, True, True])
    assert core.auc(np.array([1.0, 2.0, 3.0, 4.0]), y) == 1.0
    assert core.auc(np.array([4.0, 3.0, 2.0, 1.0]), y) == 0.0
    assert core.auc(np.array([1.0, 1.0, 1.0, 1.0]), y) == 0.5
    assert np.isnan(core.auc(np.array([1.0, 2.0]), np.array([True, True])))
