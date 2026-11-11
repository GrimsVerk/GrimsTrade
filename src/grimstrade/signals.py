"""Small, shared building blocks for strategies: trailing returns and volatility.

Everything here works on bars a strategy was allowed to see (closed before its decision), so it
can't add look-ahead. Calendar-day lookbacks keep crypto (7 days/week) and ETFs (5) comparable.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import date, timedelta

from grimstrade.data import CRYPTO, ETF, Bar

# Bars per year, to annualise volatility per asset class.
BARS_PER_YEAR: dict[str, int] = {CRYPTO: 365, ETF: 252}


def close_on_or_before(bars: Sequence[Bar], d: date) -> float | None:
    """Close of the last bar dated on or before `d`, or None if there is none."""
    for b in reversed(bars):
        if b.date <= d:
            return b.close
    return None


def trailing_return(bars: Sequence[Bar], days: int, end: date | None = None) -> float | None:
    """Return from the close `days` calendar days before `end` to the close at `end`.

    `end` defaults to the last bar's date. None if history doesn't reach back that far.
    """
    if not bars:
        return None
    end = end or bars[-1].date
    if bars[0].date > end - timedelta(days=days):
        return None
    now, then = close_on_or_before(bars, end), close_on_or_before(bars, end - timedelta(days=days))
    if now is None or then is None or then <= 0:
        return None
    return now / then - 1


def daily_returns(bars: Sequence[Bar]) -> list[float]:
    """Close-to-close returns, one per bar after the first."""
    return [b.close / a.close - 1 for a, b in zip(bars, bars[1:], strict=False) if a.close > 0]


def realized_vol(returns: Sequence[float], per_year: int) -> float | None:
    """Annualised sample standard deviation of `returns` (None if fewer than 2)."""
    n = len(returns)
    if n < 2:
        return None
    mean = math.fsum(returns) / n
    var = math.fsum((r - mean) ** 2 for r in returns) / (n - 1)
    return math.sqrt(var * per_year)


def ewma_vol(returns: Sequence[float], center_of_mass: float, per_year: int) -> float | None:
    """Annualised exponentially weighted volatility, as in Moskowitz, Ooi & Pedersen (2012).

    Weights (1 - d) * d**i on the i-th most recent squared deviation from the weighted mean, with
    d / (1 - d) = center_of_mass. None if fewer than 2 returns.
    """
    if len(returns) < 2:
        return None
    d = center_of_mass / (center_of_mass + 1)
    weights = [(1 - d) * d**i for i in range(len(returns))]
    recent_first = list(reversed(returns))
    total = math.fsum(weights)
    mean = math.fsum(w * r for w, r in zip(weights, recent_first, strict=True)) / total
    var = math.fsum(w * (r - mean) ** 2 for w, r in zip(weights, recent_first, strict=True)) / total
    return math.sqrt(var * per_year)
