"""Statistics for judging a backtest honestly. Daily returns, 365 days a year, zero risk-free
rate (the repo's convention, see docs/DECISIONS.md)."""

from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

DAYS = 365
_N = NormalDist()
EULER = 0.5772156649015329


def sharpe(r: np.ndarray) -> float:
    sd = r.std()
    return float(r.mean() / sd * math.sqrt(DAYS)) if sd > 0 else 0.0


def cagr(r: np.ndarray) -> float:
    return float(np.exp(np.log1p(r).sum() * DAYS / len(r)) - 1)


def vol(r: np.ndarray) -> float:
    return float(r.std() * math.sqrt(DAYS))


def max_drawdown(r: np.ndarray) -> float:
    eq = np.concatenate([[1.0], np.cumprod(1 + r)])
    return float((1 - eq / np.maximum.accumulate(eq)).max())


def sharpe_se(r: np.ndarray) -> float:
    """Standard error of the annualised Sharpe, with skew and kurtosis (Mertens 2002; reduces to
    Lo 2002's sqrt((1 + SR^2/2)/T) for normal returns)."""
    sr = r.mean() / r.std()
    z = (r - r.mean()) / r.std()
    skew, kurt = float((z**3).mean()), float((z**4).mean())
    var = (1 - skew * sr + (kurt - 1) / 4 * sr**2) / (len(r) - 1)
    return float(math.sqrt(var) * math.sqrt(DAYS))


def psr(r: np.ndarray, benchmark_annual: float = 0.0) -> float:
    """Probabilistic Sharpe ratio: P(true Sharpe > benchmark), Bailey & Lopez de Prado."""
    se = sharpe_se(r)
    return _N.cdf((sharpe(r) - benchmark_annual) / se) if se > 0 else 0.0


def expected_max_sharpe(n_trials: int, sharpe_var_annual: float) -> float:
    """Expected best annualised Sharpe among n_trials unskilled strategies whose Sharpe estimates
    have the given variance (Bailey & Lopez de Prado 2014, the False Strategy theorem)."""
    if n_trials < 2:
        return 0.0
    a = _N.inv_cdf(1 - 1 / n_trials)
    b = _N.inv_cdf(1 - 1 / (n_trials * math.e))
    return math.sqrt(sharpe_var_annual) * ((1 - EULER) * a + EULER * b)


def deflated_sharpe(r: np.ndarray, n_trials: int, sharpe_var_annual: float) -> float:
    """P(true Sharpe > the best Sharpe luck alone would give over n_trials)."""
    return psr(r, expected_max_sharpe(n_trials, sharpe_var_annual))


def _stationary_indices(n: int, mean_block: float, rng: np.random.Generator) -> np.ndarray:
    """Politis-Romano stationary bootstrap indices (geometric block lengths, wrap-around)."""
    restart = rng.random(n) < 1 / mean_block
    restart[0] = True
    pos = np.arange(n)
    last = np.maximum.accumulate(np.where(restart, pos, 0))  # position of the latest restart
    starts = rng.integers(n, size=n)
    idx: np.ndarray = (starts[last] + pos - last) % n
    return idx


def sharpe_diff_boot(
    a: np.ndarray, b: np.ndarray, draws: int = 2000, mean_block: float = 20, seed: int = 0
) -> tuple[float, float, float, float]:
    """Paired stationary bootstrap of Sharpe(a) - Sharpe(b) on the same days.

    Returns (difference, p, 5% quantile, 95% quantile), where p is the share of resamples in
    which a does NOT beat b (a one-sided bootstrap p-value for "a is better")."""
    if len(a) != len(b):
        raise ValueError("series must cover the same days")
    rng = np.random.default_rng(seed)
    diffs = np.empty(draws)
    for k in range(draws):
        i = _stationary_indices(len(a), mean_block, rng)
        diffs[k] = sharpe(a[i]) - sharpe(b[i])
    p = float((diffs <= 0).mean())
    lo, hi = float(np.quantile(diffs, 0.05)), float(np.quantile(diffs, 0.95))
    return sharpe(a) - sharpe(b), p, lo, hi
