"""breadth-anatomy-1's counterfactual weights and blend arithmetic (research/lib/banat1_core.py).

- `K` weights give each coin the six's slot and split the six's ETF budget over all ETFs.
- `rw` weights are inverse-vol proportions over the eligible set, held only when on.
- The static-mix Sharpe, its best weight and the marginal test agree with the closed form.
"""

from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
ac: Any = importlib.import_module("banat1_core")

SIX = ["SPY", "QQQ", "GLD", "TLT", "BTC", "ETH"]
COINS = {"BTC", "ETH"}


def test_coin_weights_match_the_six_and_etf_budget_is_shared() -> None:
    el = [*SIX, "EEM", "FXE", "SHY", "USO"]
    w = ac.coin_fixed_weights(el, set(el), SIX, COINS)
    assert math.isclose(w["BTC"], 1 / 6) and math.isclose(w["ETH"], 1 / 6)
    assert all(math.isclose(w[s], (4 / 6) / 8) for s in el if s not in COINS)
    assert math.isclose(sum(w.values()), 1.0)


def test_coin_weights_before_eth_is_eligible_and_when_off() -> None:
    el = ["SPY", "QQQ", "GLD", "TLT", "BTC", "EEM"]
    w = ac.coin_fixed_weights(el, {"BTC", "EEM"}, SIX, COINS)
    assert w == {"BTC": 1 / 5, "EEM": (4 / 5) / 5}
    # no coin eligible: the book is equal weight over the ETFs
    w0 = ac.coin_fixed_weights(["SPY", "TLT", "EEM"], {"SPY", "TLT", "EEM"}, SIX, COINS)
    assert all(math.isclose(x, 1 / 3) for x in w0.values())


def test_inverse_vol_weights() -> None:
    vol = {"A": 0.1, "B": 0.2, "C": 0.4, "D": math.nan}
    w = ac.inverse_vol_weights(["A", "B", "C", "D"], {"A", "C", "D"}, vol)
    tot = 10 + 5 + 2.5
    assert set(w) == {"A", "C"}
    assert math.isclose(w["A"], 10 / tot) and math.isclose(w["C"], 2.5 / tot)


def _pair(rho: float, sa: float, sr: float, n: int = 20000) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(1)
    z1, z2 = rng.standard_normal(n), rng.standard_normal(n)
    ref = z1
    a = rho * z1 + math.sqrt(1 - rho**2) * z2
    # exact planted means: demean, then add mean = target Sharpe x sd (per-period units)
    ref = (ref - ref.mean()) / ref.std() + sr
    a = (a - a.mean()) / a.std() + sa
    return a, ref


def test_marginal_test_sign_matches_a_small_weight() -> None:
    for rho, sa in ((0.5, 0.2), (0.5, 0.8), (0.0, 0.1), (0.8, 0.5)):
        a, ref = _pair(rho, sa * 0.01, 1.0 * 0.01)
        r = float(np.corrcoef(a, ref)[0, 1])
        g = ac.marginal_gain(ac.sharpe(a), ac.sharpe(ref), r)
        up = ac.mix_sharpe(a, ref, 0.01) > ac.mix_sharpe(a, ref, 0.0)
        assert (g > 0) == up


def test_best_weight_matches_closed_form() -> None:
    a, ref = _pair(0.3, 0.005, 0.01)
    w, s = ac.best_weight(a, ref)
    # equal vols: tangency weights proportional to inv(C) mu
    c = np.corrcoef(a, ref)
    x = np.linalg.solve(c, np.array([a.mean() / a.std(), ref.mean() / ref.std()]))
    wa = (x[0] / a.std()) / (x[0] / a.std() + x[1] / ref.std())
    assert abs(w - wa) < 0.002
    closed = math.sqrt(ac.sharpe(ref) ** 2 + (ac.sharpe(a) - c[0, 1] * ac.sharpe(ref)) ** 2
                       / (1 - c[0, 1] ** 2))  # fmt: skip
    assert abs(s - closed) < 1e-3 * closed


def test_pairwise_corr_uses_only_valid_rows() -> None:
    x = np.column_stack([np.arange(10.0), np.arange(10.0) ** 2, np.r_[np.zeros(5), np.arange(5.0)]])
    valid = np.ones_like(x, bool)
    valid[:5, 2] = False
    c = ac.pairwise_corr(x, valid)
    assert math.isclose(c[0, 2], 1.0)
    assert ac.mean_offdiag(c, [0], [2]) == c[0, 2]
