"""The coin-drift-1 core (research/lib/coindrift1_core.py) has no look-ahead and trades as the card
(research/cards/coin-drift-run.md) says.

- The account on day t does not change when prices after t are scrambled (targets fixed).
- The trend condition on day t uses no price stamped after t - 1, on real and placebo prices.
- Band semantics: a drifted slot is traded at k 0.06 and left at k 0.30; entries and full exits
  always trade; at k 0 and no costs the account is a daily reset to target.
- Fee tiers: a day's fee rate depends only on fills of the 30 days before it.
- P1 keeps each day's multiset of shuffled returns; P2 keeps the weekly market moves; both keep
  every coin's missing days.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
core: Any = importlib.import_module("coindrift1_core")


def _prices(days: int, n: int, seed: int = 0, vol: float = 0.04) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.exp(np.cumsum(rng.normal(0, vol, (days, n)), axis=0))


def _weekly(days: int, n: int, w: float) -> tuple[np.ndarray, np.ndarray]:
    base = np.arange(1, days, 7)
    return np.full((len(base), n), w), base


def test_account_ignores_later_prices() -> None:
    px = _prices(200, 6)
    targets, base = _weekly(200, 6, 1 / 6)
    t = 120
    later = px.copy()
    later[t + 1 :] *= np.exp(np.random.default_rng(5).normal(0, 0.5, later[t + 1 :].shape))
    for k in (0.06, 0.30):
        a = core.simulate(px, targets, base, k)
        b = core.simulate(later, targets, base, k)
        n = t - int(base[0])  # returns of rows first + 1 .. t
        np.testing.assert_allclose(a.rets[:n], b.rets[:n])
        assert not np.allclose(a.rets[n:], b.rets[n:])


def test_trend_condition_uses_only_earlier_prices() -> None:
    px = _prices(800, 5)
    px[:100, 2] = np.nan  # a coin that starts later
    t = 600
    later = px.copy()
    later[t:] *= 3.0  # prices stamped t and after
    a, b = core.trend_up(px), core.trend_up(later)
    assert (a[: t + 1] == b[: t + 1]).all()  # row t uses stamps up to t - 1
    assert not (a[t + 1 :] == b[t + 1 :]).all()
    elig = np.ones(px.shape, bool)
    cols = np.ones(5, bool)
    # P1 moves returns only across coins within a day: placebo prices to t - 1 come from real
    # returns to t - 1 only (same seed, same blocks). P2 moves whole weeks of the market in time
    # by design (that is the placebo); its rule still reads only placebo prices before the
    # decision, which `trend_up` above guarantees for any price matrix.
    p, q = core.shuffle_p1(px, elig, cols, 3), core.shuffle_p1(later, elig, cols, 3)
    np.testing.assert_allclose(p[:t], q[:t])
    assert (core.trend_up(p)[: t + 1] == core.trend_up(q)[: t + 1]).all()


def test_band_trims_a_drifted_slot_only_when_it_is_wide_enough() -> None:
    # two coins at 1/2 each; coin 0 rises 20% on day 2, so its slot is about 10% over target
    px = np.ones((5, 2))
    px[2:, 0] = 1.2
    targets = np.array([[0.5, 0.5]])
    base = np.array([1])
    narrow = core.simulate(px, targets, base, 0.06, costs=False)
    wide = core.simulate(px, targets, base, 0.30, costs=False)
    assert narrow.all_fills == 4  # two entries, then a trim and a top-up on day 2
    assert narrow.fills == 2
    assert wide.all_fills == 2  # the entries only
    assert wide.fills == 0


def test_entries_and_full_exits_always_trade() -> None:
    px = np.ones((6, 2))
    targets = np.array([[0.01, 0.0], [0.0, 0.0]])  # a tiny entry, then a full exit
    base = np.array([1, 3])
    acc = core.simulate(px, targets, base, 0.99, costs=False)
    assert acc.all_fills == 2 and acc.fills == 0
    # a stale price still lets a held coin be sold once its target is 0
    px2 = px.copy()
    px2[3:, 0] = np.nan
    acc2 = core.simulate(px2, targets, base, 0.99, costs=False)
    assert acc2.all_fills == 2


def test_zero_band_and_no_costs_is_a_daily_reset() -> None:
    px = _prices(60, 3, seed=2)
    w = np.array([0.3, 0.2, 0.4])
    targets = np.array([w])
    base = np.array([1])
    acc = core.simulate(px, targets, base, 0.0, costs=False)
    r = px[2:] / px[1:-1] - 1
    np.testing.assert_allclose(acc.rets, r @ w, rtol=1e-9, atol=1e-12)


def test_fee_tier_reads_only_the_30_days_before() -> None:
    assert core.fee_at(0.0) == 0.0080
    assert core.fee_at(2_500.0) == 0.0060
    assert core.fee_at(1e9) == 0.0005
    # day 10 buys (no volume before: 0.80%, about 9.9k traded: the 2.5k tier); day 11 sells
    # at 0.60%; a buy on day 40 still sees day 11's sale (0.60%), a buy on day 41 does not
    px = np.ones((50, 1))
    s = 1 + core.COIN.slip
    for buy_day, fee in ((40, 0.0060), (41, 0.0080)):
        targets = np.array([[1.0], [0.0], [1.0], [0.0]])
        base = np.array([10, 11, buy_day, buy_day + 1])
        acc = core.simulate(px, targets, base, 0.0, start_cash=10_000.0)
        assert np.isclose(1 + acc.rets[0], (2 - s) * (1 - 0.0060))  # day 11's sale
        assert np.isclose(1 + acc.rets[buy_day - 11], 1 / (s * (1 + fee)))


def test_shuffles_keep_cross_sections_and_missing_days() -> None:
    px = _prices(120, 6, seed=4)
    px[:30, 5] = np.nan  # starts late
    px[60:64, 4] = np.nan  # a gap
    elig = np.ones(px.shape, bool)
    cols = np.ones(6, bool)
    _, x = core._logret_rows(px)
    for fn in (core.shuffle_p1, core.shuffle_p2):
        p = fn(px, elig, cols, 7)
        assert (np.isfinite(p) == np.isfinite(px)).all()
        first_known = np.isfinite(px).argmax(0)
        cols_idx = np.arange(6)
        np.testing.assert_allclose(p[first_known, cols_idx], px[first_known, cols_idx])
    p1 = core.shuffle_p1(px, elig, cols, 7)
    _, y = core._logret_rows(p1)
    for s, S in core._blocks(px, elig, cols):
        for t in range(s, s + core.BLOCK):
            np.testing.assert_allclose(np.sort(y[t, S]), np.sort(x[t, S]))
    p2 = core.shuffle_p2(px, elig, cols, 7)
    _, z = core._logret_rows(p2)
    blocks = [(s, S) for s, S in core._blocks(px, elig, cols) if len(S) >= 2]
    real_m = sorted(round(float(x[s : s + core.BLOCK, S].mean()), 10) for s, S in blocks)
    plac_m = sorted(round(float(z[s : s + core.BLOCK, S].mean()), 10) for s, S in blocks)
    assert real_m == plac_m


def test_joint_boot_zero_for_identical_books() -> None:
    r = np.random.default_rng(0).normal(0.001, 0.02, 500)
    out = core.joint_boot(r, r, r[None, :], r[None, :], draws=50)
    assert out["d"] == 0.0 and out["excess"] == 0.0 and out["se"] == 0.0
