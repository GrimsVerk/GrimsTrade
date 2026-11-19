"""coin-cap-4 core: the price-drawdown stop, its exposure-matched band, and time under water
(card: research/cards/coin-cap.md, "Fifth reading"). Pure numpy, no harness import, so the
tests can load it alone. Rows are calendar days, as in `cointop1_core`."""

from __future__ import annotations

from collections.abc import Callable

import breadth_xs as xs
import cointop1_core as core
import numpy as np

X_GRID = tuple(round(0.10 + 0.01 * i, 2) for i in range(41))  # 0.10 .. 0.50


def price_dd(px: np.ndarray, shift: int) -> np.ndarray:
    """close / highest close of the last 365 days - 1, from values stamped `shift` rows earlier
    or before (row t may be used at a decision on day t). NaN where unknown."""
    with np.errstate(invalid="ignore", divide="ignore"):
        return xs.lag(px / core.roll_max(px, 365) - 1, shift)


def pstop_ok(dd: np.ndarray, x: float) -> np.ndarray:
    """Within `x` of the one-year high in price; an unknown drawdown is not held."""
    with np.errstate(invalid="ignore"):
        return np.asarray(dd >= -x)


def match_x(time_held: Callable[[float], float], target: float) -> float:
    """The `x` of `X_GRID` whose time held is closest to `target` (ties: the smaller `x`).
    `time_held` maps a band to the pooled time held over the twin's (positions only)."""
    gaps = [(abs(time_held(x) - target), x) for x in X_GRID]
    return min(gaps)[1]


def tuw(r: np.ndarray) -> int:
    """Longest run of consecutive days on which the P&L path (running sum of `r`, from 0 before
    the first return) is below its running high. Scale-free: `tuw(f * r) == tuw(r)` for f > 0."""
    path = np.concatenate([[0.0], np.cumsum(r)])
    under = path < np.maximum.accumulate(path) - 1e-12
    best = run = 0
    for u in under[1:]:
        run = run + 1 if u else 0
        best = max(best, run)
    return best


def equity_tuw(eq: np.ndarray, deep: float = 0.10) -> tuple[int, float]:
    """For an equity curve (one value a day): the longest stretch of days below a previous high,
    and the share of days at least `deep` below it."""
    hi = np.maximum.accumulate(eq)
    under = eq < hi * (1 - 1e-12)
    best = run = 0
    for u in under:
        run = run + 1 if u else 0
        best = max(best, run)
    return best, float((eq <= hi * (1 - deep)).mean())
