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


# --- W13 festival dates (from memory; tests check each against wide-6's mean new moons) ---

LUNAR_NEW_YEAR = [date.fromisoformat(s) for s in [
    "2005-02-09", "2006-01-29", "2007-02-18", "2008-02-07", "2009-01-26", "2010-02-14",
    "2011-02-03",
    "2012-01-23", "2013-02-10", "2014-01-31", "2015-02-19", "2016-02-08", "2017-01-28",
    "2018-02-16",
    "2019-02-05", "2020-01-25", "2021-02-12", "2022-02-01", "2023-01-22", "2024-02-10",
    "2025-01-29",
]]  # fmt: skip
DIWALI = [date.fromisoformat(s) for s in [
    "2004-11-12", "2005-11-01", "2006-10-21", "2007-11-09", "2008-10-28", "2009-10-17",
    "2010-11-05",
    "2011-10-26", "2012-11-13", "2013-11-03", "2014-10-23", "2015-11-11", "2016-10-30",
    "2017-10-19",
    "2018-11-07", "2019-10-27", "2020-11-14", "2021-11-04", "2022-10-24", "2023-11-12",
    "2024-11-01",
    "2025-10-20",
]]  # fmt: skip
DHANTERAS = [d - timedelta(days=2) for d in DIWALI]


def run_flags(days: Sequence[date], fest: Sequence[date], n: int) -> np.ndarray:
    """1.0 on each of the n trading days strictly before each festival day, else 0.0. A
    festival after the last day is skipped (its run is not known to be complete)."""
    out = np.zeros(len(days))
    for f in fest:
        j = bisect.bisect_left(days, f)  # first day >= f
        if j < len(days):
            out[max(0, j - n) : j] = 1.0
    return out


def month_matrix(days: Sequence[date]) -> np.ndarray:
    x = np.zeros((len(days), 12))
    for n, d in enumerate(days):
        x[n, d.month - 1] = 1.0
    return x


# --- W12 RMD waiver years ---

RMD_WAIVED = (2009, 2020)


def december_window(
    days: Sequence[date], logc: np.ndarray, y: int, n: int = 10, first: bool = False
) -> tuple[float, float] | None:
    """(excess, raw) log return over the last n (or first n) trading sessions of December y.
    Raw = close of the session before the window to its last close. Excess = raw minus n
    times the mean daily log return over year y's other sessions. None if the year's bars
    are incomplete (no close before 1 January y, or December has fewer than n + 1 sessions)."""
    i_prev = last_on_or_before(days, date(y - 1, 12, 31))
    i_end = last_on_or_before(days, date(y, 12, 31))
    dec = [i for i in range(i_prev + 1, i_end + 1) if days[i].month == 12]
    if i_prev < 0 or len(dec) < n + 1 or days[i_end].month != 12:
        return None
    w = dec[:n] if first else dec[-n:]
    raw = float(logc[w[-1]] - logc[w[0] - 1])
    rets = np.diff(logc[i_prev : i_end + 1])  # rets[k] = return of day i_prev + 1 + k
    inside = {i - i_prev - 1 for i in w}
    other = [rets[k] for k in range(len(rets)) if k not in inside]
    return raw - n * float(np.mean(other)), raw


def pair_permutation(x: dict[int, float], treat: Sequence[int]) -> tuple[float, float]:
    """D = mean x over the treated years minus mean over the rest, and the exact one-sided
    p: share of all equal-sized sets of years whose mean x is at or above the treated set's."""
    from itertools import combinations

    years = sorted(x)
    t = [y for y in treat if y in x]
    if not t or len(t) == len(years):
        return math.nan, math.nan
    rest = [x[y] for y in years if y not in t]
    d = float(np.mean([x[y] for y in t]) - np.mean(rest))
    m = float(np.mean([x[y] for y in t]))
    sets = [float(np.mean(c)) for c in combinations([x[y] for y in years], len(t))]
    return d, sum(s >= m - 1e-15 for s in sets) / len(sets)
