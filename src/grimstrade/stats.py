"""The deflated Sharpe ratio (Bailey & López de Prado 2014, "The deflated Sharpe ratio:
correcting for selection bias, backtest overfitting and non-normality", JPM).

Try enough strategies and the best one looks good by luck alone. The DSR is the probability that
a strategy's true Sharpe ratio is above zero, after allowing for (a) how many strategies were tried
(the best of N lucky draws is expected to have Sharpe SR0 > 0) and (b) short records with fat
tails or skew. All Sharpe ratios here are per period (daily), not annualised.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from statistics import NormalDist

EULER_GAMMA = 0.5772156649015329
_N = NormalDist()


@dataclass(frozen=True)
class Moments:
    periods: int  # T, number of returns
    sharpe: float  # per period
    skew: float
    kurtosis: float  # not excess: 3 for a normal distribution


def moments(returns: Sequence[float]) -> Moments | None:
    """Per-period Sharpe, skew and kurtosis (population moments). None if under 2 returns or
    no variation."""
    t = len(returns)
    if t < 2:
        return None
    mean = math.fsum(returns) / t
    m2 = math.fsum((r - mean) ** 2 for r in returns) / t
    if m2 <= 0:
        return None
    sd = math.sqrt(m2)
    m3 = math.fsum((r - mean) ** 3 for r in returns) / t
    m4 = math.fsum((r - mean) ** 4 for r in returns) / t
    return Moments(t, mean / sd, m3 / sd**3, m4 / m2**2)


def expected_max_sharpe(trials: int, sharpe_variance: float) -> float:
    """SR0: the Sharpe the best of `trials` independent zero-skill strategies is expected to
    show, given the variance of Sharpe estimates across trials (eq. in Bailey & LdP 2014)."""
    if trials < 2 or sharpe_variance <= 0:
        return 0.0
    z1 = _N.inv_cdf(1 - 1 / trials)
    z2 = _N.inv_cdf(1 - 1 / (trials * math.e))
    return math.sqrt(sharpe_variance) * ((1 - EULER_GAMMA) * z1 + EULER_GAMMA * z2)


def probabilistic_sharpe(m: Moments, benchmark: float) -> float:
    """PSR: probability the true per-period Sharpe exceeds `benchmark`, given the record's length,
    skew and kurtosis (Bailey & López de Prado 2012)."""
    denom = 1 - m.skew * m.sharpe + (m.kurtosis - 1) / 4 * m.sharpe**2
    if denom <= 0 or m.periods < 2:
        return 0.5
    return _N.cdf((m.sharpe - benchmark) * math.sqrt(m.periods - 1) / math.sqrt(denom))


def null_sharpe_variance(periods: int) -> float:
    """Variance of a Sharpe estimate over `periods` returns when the true Sharpe is zero."""
    return 1 / periods if periods > 0 else 0.0


def deflated_sharpe(m: Moments, trials: int, sharpe_variance: float) -> float:
    """DSR = PSR against SR0, the expected best Sharpe of `trials` zero-skill tries."""
    return probabilistic_sharpe(m, expected_max_sharpe(trials, sharpe_variance))
