"""Pure rules of the survey-3 card `xtsmom` (research/cards/xtsmom.md): the trailing return of a
10-year par bond built from a daily yield series, as a look-ahead-safe step. No data access."""

from __future__ import annotations

import bisect
import math
from collections.abc import Sequence
from datetime import date, timedelta

import numpy as np

GAP_DAYS = 10  # a return across a longer gap in the yield series counts as 0


def duration(y: float, n: int) -> float:
    """Modified duration of a par bond of maturity `n` years at yield `y` (semi-annual)."""
    return (1 - (1 + y / 2) ** (-2 * n)) / y if y > 0 else float(n)


def bond_returns(days: Sequence[date], yields_pct: Sequence[float], n: int = 10) -> np.ndarray:
    """Return of a par bond over the interval ending on each observation: -duration x change in
    yield + carry for the calendar days elapsed (wide-1 step 4). Entry 0 and gaps are 0."""
    y = np.asarray(yields_pct, dtype=float) / 100
    out = np.zeros(len(days))
    for i in range(1, len(days)):
        gap = (days[i] - days[i - 1]).days
        if gap <= GAP_DAYS:
            out[i] = -duration(y[i - 1], n) * (y[i] - y[i - 1]) + y[i - 1] * gap / 365
    return out


def trailing(days: Sequence[date], rets: np.ndarray, lookback: int) -> list[float]:
    """For each observation i: the sum of the returns of observations in (days[i] - lookback,
    days[i]]; NaN while the series is shorter than the look-back. Reads entries 0..i only."""
    cs = np.cumsum(rets)
    out = []
    for i, t in enumerate(days):
        start = t - timedelta(days=lookback)
        if days[0] > start:
            out.append(math.nan)
            continue
        j = bisect.bisect_right(days, start)  # first observation after the window start
        out.append(float(cs[i] - cs[j - 1]))
    return out


def usable_from(days: Sequence[date]) -> list[date]:
    """A daily market observation for day x is used from x + 1 (protocol, "Macro tests")."""
    return [d + timedelta(days=1) for d in days]
