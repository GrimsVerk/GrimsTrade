"""Pure functions for the wide-7 event-study gates (research/wide-7.md): calendar dates, the
last close on or before a date, and the per-asset-year numbers of the wash-sale echo gate. No
I/O here, so the tests can check each piece on made-up data."""

from __future__ import annotations

import bisect
import math
from collections.abc import Sequence
from datetime import date, timedelta

import numpy as np


def third_friday(year: int, month: int) -> date:
    d = date(year, month, 1)
    first_fri = d + timedelta(days=(4 - d.weekday()) % 7)
    return first_fri + timedelta(days=14)


def last_on_or_before(days: Sequence[date], d: date) -> int:
    """Index of the last day <= d, or -1 if none."""
    return bisect.bisect_right(days, d) - 1


def window_return(days: Sequence[date], logc: np.ndarray, a: date, b: date) -> float:
    """Log return from the last close on or before a to the last close on or before b; NaN if
    either is missing or both are the same bar."""
    i, j = last_on_or_before(days, a), last_on_or_before(days, b)
    if i < 0 or j <= i:
        return math.nan
    return float(logc[j] - logc[i])


def wash_sale_year(
    days: Sequence[date], logc: np.ndarray, y: int, last: date
) -> dict[str, float] | None:
    """The W14 numbers for one asset in tax year y, or None if the asset lacks the bars:
    YTD to the last bar of November, loss L = max(0, -YTD), and the returns over the echo
    window (S+31 .. S+45), the turn of the year (31 Dec .. 10 Jan) and the late placebo
    (S+46 .. S+60), S = third Friday of December. `last` = last day that may be read."""
    s = third_friday(y, 12)
    if s + timedelta(days=60) > last or not days or days[0] > date(y - 1, 12, 31):
        return None
    i0 = last_on_or_before(days, date(y - 1, 12, 31))
    i1 = last_on_or_before(days, date(y, 11, 30))
    if i0 < 0 or i1 <= i0 or days[i1] < date(y, 11, 1):
        return None
    ytd = float(logc[i1] - logc[i0])
    out = {
        "ytd": ytd,
        "loss": max(0.0, -ytd),
        "echo": window_return(days, logc, s + timedelta(days=30), s + timedelta(days=45)),
        "toy": window_return(days, logc, date(y, 12, 31), date(y + 1, 1, 10)),
        "late": window_return(days, logc, s + timedelta(days=45), s + timedelta(days=60)),
    }
    if any(math.isnan(v) for v in out.values()):
        return None
    return out


def year_dummies(years: Sequence[int]) -> np.ndarray:
    keys = sorted(set(years))
    pos = {k: n for n, k in enumerate(keys)}
    x = np.zeros((len(years), len(keys)))
    for n, y in enumerate(years):
        x[n, pos[y]] = 1.0
    return x
