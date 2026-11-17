"""Carry-3's cost model, shapes and held-out guard do what the card in research/carry-3.md says.

- The cost per side rises with the size of the trade and of the account; no trade, no cost.
- The copied simulator gives short-1's returns when costs are flat and rebalances are full.
- An order below the smallest order is not made, except closing a position.
- The band: a coin enters in a leg's third, stays inside the leg's half, leaves outside it;
  a held weight near its target is left alone.
- The held-out guard writes its claim once and refuses a second look.
- Panels drop everything after the train cut unless the held-out grid is asked for.
- The order-book reader prices a market order by walking the book.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _mod(name: str) -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module(name)
    finally:
        sys.path.remove(str(LIB))


def _model() -> Any:
    cc = _mod("carry3_cost")
    return cc, cc.CostModel("binance", cc.SpreadFit(a=6.0, b=-0.3, lo=1e6, hi=1e10))


def test_cost_rises_with_size_and_is_zero_without_trading() -> None:
    cc, cm = _model()
    sizes = [10.0, 100.0, 1_000.0, 10_000.0, 100_000.0]
    costs = [cm.per_side(q, 2e7, 0.05) for q in sizes]
    assert all(b > a for a, b in zip(costs, costs[1:], strict=False))
    assert costs[0] > cc.FEES["binance"][1]  # never below the taker fee
    # a thinner coin costs more; a larger account pays more for the same weight change
    assert cm.per_side(1_000.0, 5e6, 0.05) > cm.per_side(1_000.0, 5e8, 0.05)
    dw = np.array([0.01, -0.02, 0.0])
    adv = np.array([1e7, 5e7, 1e9])
    vol = np.array([0.05, 0.06, 0.03])
    small = cm.parts(dw, adv, vol, 1.0).sum()
    large = cm.but(account=1_000_000.0).parts(dw, adv, vol, 1.0).sum()
    assert large > small > 0
    assert cm.parts(np.zeros(3), adv, vol, 1.0).sum() == 0.0
    assert cm.per_side(0.0, 1e7, 0.05) == 0.0
    # stress doubles spread and impact, not the fee; a flat model ignores size
    base, x2 = cm.parts(dw, adv, vol, 1.0), cm.but(stress=2.0).parts(dw, adv, vol, 1.0)
    assert np.isclose(x2[0], base[0]) and np.allclose(x2[1:], 2 * base[1:])
    assert np.isclose(cm.but(flat=0.001).parts(dw, adv, vol, 1.0).sum(), 0.03 * 0.001)
    # maker fills are cheaper than taker fills; a missing ADV is priced, not free
    assert cm.but(maker_share=0.6).parts(dw, adv, vol, 1.0).sum() < small
    assert np.isfinite(cm.parts(dw, np.full(3, np.nan), vol, 1.0)).all()


def test_engine_matches_short1_and_charges_nothing_without_turnover() -> None:
    ce, se = _mod("carry3_engine"), _mod("short_engine")
    rng = np.random.default_rng(0)
    px = 100 * np.cumprod(1 + rng.normal(0, 0.03, (60, 6)), axis=0)
    fund = rng.normal(0, 0.0005, (60, 6))
    base = np.arange(5, 55, 7)
    tg = np.array([se.long_short(rng.normal(size=6), np.ones(6, bool)) for _ in base])
    ref = se.simulate(px, fund, tg, base, 0.001, 5)

    def flat(t: int, dw: np.ndarray) -> np.ndarray:
        return np.array([float(np.abs(dw).sum()) * 0.001, 0.0, 0.0])

    run = ce.simulate(px, fund, base, lambda k, t, w: tg[k], flat, 5)
    assert np.allclose(run.r, ref.r, atol=1e-14) and np.allclose(run.funding, ref.funding)
    # a book that never changes its wanted weights after entry, with no drift: one cost only
    px2 = np.full((30, 2), 50.0)
    hold = ce.simulate(
        px2, None, np.arange(0, 28, 7), lambda k, t, w: np.array([0.5, -0.5]), flat, 0
    )
    assert np.isclose(hold.cost.sum(), 0.001) and np.isclose(hold.traded.sum(), 1.0)
    assert np.allclose(hold.r[1:], 0.0)
    # no trade at all: no cost, no return
    idle = ce.simulate(px2, None, np.arange(0, 28, 7), lambda k, t, w: np.zeros(2), flat, 0)
    assert idle.cost.sum() == 0.0 and np.allclose(idle.r, 0.0)


def test_orders_below_the_smallest_order_are_skipped_except_exits() -> None:
    ce = _mod("carry3_engine")
    px = np.full((10, 3), 10.0)
    wanted = [np.array([0.5, 0.004, -0.5]), np.array([0.503, 0.0, 0.0])]

    def none(t: int, dw: np.ndarray) -> np.ndarray:
        return np.zeros(3)

    run = ce.simulate(
        px, None, np.array([0, 5]), lambda k, t, w: wanted[k], none, 0, np.full(10, 0.01)
    )
    # entry of 0.004 skipped; later the 0.003 top-up is skipped, the exit of -0.5 is made
    assert np.isclose(run.traded[0], 1.0)
    assert np.isclose(run.traded[4], 0.5)
    assert np.isclose(run.gross[-1], 0.5)


def test_band_enters_in_the_third_and_leaves_outside_the_half() -> None:
    ce = _mod("carry3_engine")
    sig = np.arange(15, 0, -1).astype(float)  # coin 0 ranks first ... coin 14 last
    m = np.ones(15, bool)
    w0 = ce.band_weights(sig, m, np.zeros(15))
    assert np.allclose(w0[:5], 0.1) and np.allclose(w0[10:], -0.1) and np.allclose(w0[5:10], 0)
    # coin 0 slips to rank 6 (inside the top half of 7): it stays long; coin 5 moves up and enters
    sig2 = sig.copy()
    sig2[0], sig2[5] = 9.5, 15.5
    w1 = ce.band_weights(sig2, m, w0)
    assert (w1 > 0).sum() == 6 and w1[0] > 0
    # held members are within 25% of the new target (0.1 vs 1/12): left alone; the entry is new
    assert np.allclose(w1[:5], 0.1) and np.isclose(w1[5], 1 / 12)
    assert np.allclose(w1[10:], -0.1)
    # coin 0 falls to the bottom: closed and, being in the bottom third, opened short
    sig3 = sig2.copy()
    sig3[0] = 0.5
    w2 = ce.band_weights(sig3, m, w1)
    assert w2[0] < 0
    # coin 1 falls just below the top half: closed, not shorted
    sig4 = sig2.copy()
    sig4[1] = 7.5
    assert ce.band_weights(sig4, m, w1)[1] == 0.0
    # a weight far from its target is traded back to it; a coin outside the universe is closed
    drift = w0.copy()
    drift[1] = 0.2
    assert np.isclose(ce.band_weights(sig, m, drift)[1], 0.1)
    m2 = m.copy()
    m2[2] = False
    assert ce.band_weights(sig, m2, w0)[2] == 0.0
    # unchanged ranks and weights: nothing to trade
    assert np.allclose(ce.band_weights(sig, m, w0), w0)


def test_heldout_guard_refuses_a_second_look(tmp_path: Path) -> None:
    ce = _mod("carry3_engine")
    tries = tmp_path / "tries.md"
    tries.write_text(
        "| when | idea | variant | kind | period | from | to | sharpe | ret | dd | turn |\n"
        "| 2026-11-17 10:00 | carry-3-pooled | band | variant | train | a | b | 1 | 1 | 1 | 1 |\n"
        "| 2026-11-13 09:00 | breadth-1-cm | x | variant | heldout | a | b | 1 | 1 | 1 | 1 |\n"
    )
    assert not ce.heldout_used(tries)
    ce.claim_heldout(tries, "2026-11-18 00:00")
    assert ce.heldout_used(tries) and ce.CLAIM in tries.read_text()
    with pytest.raises(RuntimeError, match="already spent"):
        ce.claim_heldout(tries, "2026-11-18 00:01")
    assert tries.read_text().count(ce.CLAIM) == 1


def test_panel_cuts_at_train_unless_heldout_grid() -> None:
    cp = _mod("carry3_panel")
    g = cp.Grid()
    d = 86400
    day_s = np.array([g.t0 + i * d for i in range(5)] + [g.cut, g.cut + d])
    close = np.arange(1.0, 8.0)
    ft = np.array([g.t0 + 3 * d, g.cut + 3600])
    fr = np.array([0.001, 0.5])
    acc = cp.Acc(g)
    acc.add("X", day_s, close + 1, close - 0.5, close, close * 1e6, ft, fr)
    assert np.isfinite(acc.cols["px"][0]).sum() == 5 and acc.cols["fsim"][0].sum() < 0.01
    assert acc.cols["fsim"][0][2] == 0.001  # the 00:00 event of day 3 is paid on return day 2
    assert acc.cols["hi"][0][0] == 2.0 and acc.cols["lo"][0][0] == 0.5
    held = cp.Acc(cp.Grid(cp.HELD_LAST_BAR))
    held.add("X", day_s, close + 1, close - 0.5, close, close * 1e6, ft, fr)
    assert np.isfinite(held.cols["px"][0]).sum() == 7 and held.cols["fsim"][0].sum() > 0.4
    with pytest.raises(ValueError):
        cp.Grid(cp.HELD_LAST_BAR.replace(year=2027))


def test_book_walk_and_spread_fit() -> None:
    cc = _mod("carry3_cost")
    bids = [(99.0, 1.0), (98.0, 10.0)]
    asks = [(101.0, 1.0), (102.0, 10.0)]
    assert cc.walk(asks, 50.5) == 101.0
    assert cc.walk(asks, 1e9) is None
    m = cc.measure(bids, asks)
    assert np.isclose(m["hs"], 0.01)
    assert m["slip300"] > m["hs"] and "slip10000" not in m  # 10,000 USD does not fit this book
    assert cc.measure(asks, bids) == {}  # crossed book: ignored
    vol = np.geomspace(1e6, 1e10, 50)
    hs = np.exp(6.0 - 0.3 * np.log(vol)) / 1e4
    fit = cc.fit_spread(vol, hs)
    assert np.isclose(fit.a, 6.0) and np.isclose(fit.b, -0.3)
    assert cc.fit_spread(vol[:10], hs[:10]) is None  # fewer than 30 coins: the card's fallback
    assert fit.half_spread(np.array([1.0]))[0] == fit.half_spread(np.array([1e6]))[0]
