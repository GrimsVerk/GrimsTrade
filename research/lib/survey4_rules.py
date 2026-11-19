"""Pure rules of the survey-4 cards (`cards/ts-carry.md`, `cards/halloween.md`): dividends from
adjusted vs raw closes, the trailing dividend yield, a running mean, and the winter-week test.
No data access; every function reads only entries up to the one it returns."""

from __future__ import annotations

import bisect
import math
from collections.abc import Sequence
from datetime import date, timedelta

import numpy as np

EX_TOL = 1e-5  # a change of the adjustment factor larger than this marks an ex-dividend date
WINTER = {11, 12, 1, 2, 3, 4}


def dividends(
    days: Sequence[date], raw_close: Sequence[float], adj_close: Sequence[float]
) -> list[tuple[date, float]]:
    """(ex-date, cash dividend) pairs. With f = adj / raw, Yahoo's adjustment gives
    f(t-1) = f(t) x (1 - D(t) / raw(t-1)), so D(t) = raw(t-1) x (1 - f(t-1) / f(t))."""
    out = []
    for t in range(1, len(days)):
        f0 = adj_close[t - 1] / raw_close[t - 1]
        f1 = adj_close[t] / raw_close[t]
        ratio = f0 / f1
        if abs(ratio - 1) > EX_TOL:
            out.append((days[t], raw_close[t - 1] * (1 - ratio)))
    return out


def trailing_yield(
    days: Sequence[date],
    raw_close: Sequence[float],
    divs: Sequence[tuple[date, float]],
    window: int = 365,
) -> np.ndarray:
    """At each session d: sum of dividends with ex-date in (d - window, d] / raw close(d). NaN
    until the series has `window` days of history."""
    ex = [d for d, _ in divs]
    cs = np.concatenate([[0.0], np.cumsum([x for _, x in divs])])
    out = np.full(len(days), math.nan)
    for i, d in enumerate(days):
        if d - timedelta(days=window) < days[0]:
            continue
        hi = bisect.bisect_right(ex, d)
        lo = bisect.bisect_right(ex, d - timedelta(days=window))
        out[i] = (cs[hi] - cs[lo]) / raw_close[i]
    return out


def running_mean(values: Sequence[float]) -> np.ndarray:
    """Mean of the non-NaN values up to and including each entry (NaN before the first)."""
    out = np.full(len(values), math.nan)
    s, n = 0.0, 0
    for i, v in enumerate(values):
        if not math.isnan(v):
            s += v
            n += 1
        if n:
            out[i] = s / n
    return out


def next_monday(d: date) -> date:
    return d + timedelta(days=7 - d.weekday())


def winter_week(decision: date) -> bool:
    """The week after a decision on `decision` is a winter week if the Monday after it falls in
    November to April (`cards/halloween.md`)."""
    return next_monday(decision).month in WINTER
