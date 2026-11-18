"""Pure functions for the wide-9 event gates (research/wide-9.md)."""

from __future__ import annotations

import bisect
import calendar
import math
from collections.abc import Mapping, Sequence
from datetime import date

import numpy as np

# --- Step 1: W19 ENSO and commodities ---

SEASONS = ["DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ"]

Month = tuple[int, int]  # (year, month)


def season_end(label: str, year: int) -> Month:
    """The calendar month a CPC season ends in. CPC labels a season by the year of its first
    two months for NDJ (Nov-Dec of `year`, Jan of year + 1) and by the year of its last two
    for DJF (Dec of year - 1, Jan-Feb of `year`)."""
    m = SEASONS.index(label) + 2
    return (year + 1, m - 12) if m > 12 else (year, m)


def parse_oni(text: str) -> dict[Month, float]:
    """CPC's oni.ascii.txt (`SEAS YR TOTAL ANOM`) -> {month the season ends in: anomaly}."""
    out: dict[Month, float] = {}
    for line in text.splitlines():
        f = line.split()
        if len(f) != 4 or f[0] not in SEASONS:
            continue
        out[season_end(f[0], int(f[1]))] = float(f[3])
    return out


def add_months(ym: Month, k: int) -> Month:
    n = ym[0] * 12 + ym[1] - 1 + k
    return (n // 12, n % 12 + 1)


def dose(oni: Mapping[Month, float], decision: Month, k_years: int = 0) -> float:
    """x(M): the ONI of the season ending in month M-1, with the calendar moved k whole years
    earlier (year - k). NaN if the file has no such season."""
    y, m = add_months(decision, -1)
    return oni.get((y - k_years, m), math.nan)


def month_end_bar(days: Sequence[date], ym: Month) -> int | None:
    """Index of the last bar on or before the last day of month ym, if it lies in that month."""
    last = date(ym[0], ym[1], calendar.monthrange(*ym)[1])
    i = bisect.bisect_right(days, last) - 1
    if i < 0 or (days[i].year, days[i].month) != ym:
        return None
    return i


def horizon_return(
    days: Sequence[date], logc: np.ndarray, decision: Month, h: int, last_bar: date
) -> float:
    """y(M): log(close at the end of month M+h / close at the end of month M); NaN if either
    month-end bar is missing or the exit bar is after `last_bar`."""
    i, j = month_end_bar(days, decision), month_end_bar(days, add_months(decision, h))
    if i is None or j is None or days[j] > last_bar:
        return math.nan
    return float(logc[j] - logc[i])


def months(a: Month, b: Month) -> list[Month]:
    out, cur = [], a
    while cur <= b:
        out.append(cur)
        cur = add_months(cur, 1)
    return out


def rank_highest(true: float, others: Sequence[float]) -> int:
    """1 + the number of others strictly above `true` (1 = the highest)."""
    return 1 + sum(o > true for o in others)


ONI_BINS: list[tuple[str, float, float]] = [
    ("x <= -1.0", -math.inf, -1.0),
    ("-1.0 < x <= -0.5", -1.0, -0.5),
    ("-0.5 < x < 0.5", -0.5, 0.5),
    ("0.5 <= x < 1.0", 0.5, 1.0),
    ("x >= 1.0", 1.0, math.inf),
]


def in_bin(x: float, lo: float, hi: float) -> bool:
    """Bins of research/wide-9.md: La Nina bins closed above, El Nino bins closed below."""
    if hi <= -0.5:
        return lo < x <= hi
    if lo >= 0.5:
        return lo <= x < hi
    return lo < x < hi


def null_spread(ts: Sequence[float]) -> tuple[float, float]:
    """(standard deviation, share with |t| >= 2) of a list of placebo t values."""
    a = np.asarray(ts, dtype=float)
    return float(a.std(ddof=1)), float(np.mean(np.abs(a) >= 2))
