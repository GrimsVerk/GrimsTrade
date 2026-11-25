"""breadth-anatomy-1: the weight rules of the counterfactual books and the blend arithmetic,
without the harness (tests import only this file). Card `research/cards/breadth-anatomy-1.md`.

Descriptive only: the `K` (coins at the six's weight) and `rw` (inverse-vol) weights exist to
split `breadth-book-1`'s Sharpe gap, not as candidate books.
"""

from __future__ import annotations

import math
from collections.abc import Collection, Mapping, Sequence

import numpy as np


def coin_fixed_weights(
    eligible: Sequence[str], on: Collection[str], six: Collection[str], coins: Collection[str]
) -> dict[str, float]:
    """Weights of a `K` book: each eligible coin slot gets 1 / (eligible six assets), as in the
    six; the six's ETF budget that day, (eligible six ETFs) / (eligible six assets), is split
    equally over all eligible ETFs of the set. Only assets whose signal is on are held."""
    six_el = [s for s in eligible if s in six]
    if not six_el:
        return {}
    n6 = len(six_el)
    coin_el = [s for s in eligible if s in coins]
    etf_el = [s for s in eligible if s not in coins]
    budget = (n6 - len([s for s in six_el if s in coins])) / n6
    out = {s: 1 / n6 for s in coin_el if s in on}
    if etf_el:
        out.update({s: budget / len(etf_el) for s in etf_el if s in on})
    return out


def inverse_vol_weights(
    eligible: Sequence[str], on: Collection[str], vol: Mapping[str, float]
) -> dict[str, float]:
    """Weights of an `rw` book: slot (1 / vol_i) / sum over eligible j of (1 / vol_j), held while
    the signal is on. Assets without a finite positive vol are left out of the sum."""
    inv = {s: 1 / vol[s] for s in eligible if math.isfinite(vol.get(s, math.nan)) and vol[s] > 0}
    tot = sum(inv.values())
    return {s: x / tot for s, x in inv.items() if s in on} if tot > 0 else {}


def sharpe(r: np.ndarray, per_year: float = 365) -> float:
    sd = r.std()
    return float(r.mean() / sd * math.sqrt(per_year)) if sd > 0 else 0.0


def mix_sharpe(a: np.ndarray, ref: np.ndarray, w: float) -> float:
    """Sharpe of the static daily mix w x a + (1 - w) x ref."""
    return sharpe(w * a + (1 - w) * ref)


def best_weight(a: np.ndarray, ref: np.ndarray, steps: int = 1000) -> tuple[float, float]:
    """(w*, SR(w*)): the weight on `a` in [0, 1] that maximises the static mix's Sharpe."""
    grid = np.linspace(0, 1, steps + 1)
    srs = [mix_sharpe(a, ref, float(w)) for w in grid]
    k = int(np.argmax(srs))
    return float(grid[k]), float(srs[k])


def marginal_gain(sr_a: float, sr_ref: float, rho: float) -> float:
    """SR_a - rho x SR_ref: a small weight on `a` raises the mix's Sharpe iff this is > 0."""
    return sr_a - rho * sr_ref


def corr_masked(x: np.ndarray, y: np.ndarray, mask: np.ndarray) -> float:
    m = mask & np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3 or x[m].std() == 0 or y[m].std() == 0:
        return math.nan
    return float(np.corrcoef(x[m], y[m])[0, 1])


def pairwise_corr(x: np.ndarray, valid: np.ndarray, rows: np.ndarray | None = None) -> np.ndarray:
    """Correlation matrix of the columns of x, each pair over the rows where both are valid
    (and `rows`, if given)."""
    n = x.shape[1]
    sel = np.ones(x.shape[0], bool) if rows is None else rows
    out = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            out[i, j] = out[j, i] = corr_masked(x[:, i], x[:, j], sel & valid[:, i] & valid[:, j])
    return out


def mean_offdiag(c: np.ndarray, a: Sequence[int], b: Sequence[int] | None = None) -> float:
    """Mean correlation within group a (b None) or between groups a and b."""
    if b is None:
        v = [c[i, j] for k, i in enumerate(a) for j in a[k + 1 :]]
    else:
        v = [c[i, j] for i in a for j in b]
    v = [x for x in v if math.isfinite(x)]
    return float(np.mean(v)) if v else math.nan
