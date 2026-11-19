"""Lane weather-1: pure functions for the HDD-surprise gate (card `research/weather-1.md`).

No I/O, no network: parsing of the CPC degree-day files, the rolling normal, the weekly dose,
the entry/exit bars and the winter derangements. The runner is `weather1_hdd.py`.
"""

from __future__ import annotations

import bisect
import math
from collections.abc import Mapping, Sequence
from datetime import date, timedelta

import numpy as np

LAST_WEATHER_DAY = date(2025, 11, 9)  # the parser drops every later day (held-out year)
SEASON_MONTHS = (11, 12, 1, 2, 3)
NORMAL_YEARS = 20
NORMAL_HALF_WINDOW = 7
ENTRY_LAG_DAYS = 4
HOLD = 5
SEED = 20261119


def parse_cpc(text: str, region: str = "CONUS") -> dict[date, float]:
    """Daily degree days of one region from a CPC `daily_data/<year>/*.txt` file.

    Layout: three header lines, then `Region|YYYYMMDD|...`, then one `|`-separated row per
    region. Days after LAST_WEATHER_DAY and non-numeric cells are dropped.
    """
    days: list[date] = []
    out: dict[date, float] = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.split("|")]
        if cells[0] == "Region":
            days = [date(int(c[:4]), int(c[4:6]), int(c[6:8])) for c in cells[1:] if c]
        elif cells[0] == region and days:
            for d, c in zip(days, cells[1:], strict=False):
                if d > LAST_WEATHER_DAY:
                    continue
                try:
                    v = float(c)
                except ValueError:
                    continue
                if v >= 0:
                    out[d] = v
    return out


def _same_day(year: int, d: date) -> date:
    if d.month == 2 and d.day == 29:
        return date(year, 2, 28)
    return date(year, d.month, d.day)


def normal(hdd: Mapping[date, float], d: date) -> float:
    """Mean HDD on the same calendar day +-7 days in each of the 20 previous years.

    NaN unless every one of the 20 years has at least one value in its window.
    """
    vals: list[float] = []
    for j in range(d.year - NORMAL_YEARS, d.year):
        c = _same_day(j, d)
        got = [
            hdd[c + timedelta(days=k)]
            for k in range(-NORMAL_HALF_WINDOW, NORMAL_HALF_WINDOW + 1)
            if (c + timedelta(days=k)) in hdd
        ]
        if not got:
            return math.nan
        vals.extend(got)
    return float(np.mean(vals))


def dose(hdd: Mapping[date, float], friday: date, norm_cache: dict[date, float]) -> float:
    """Sum of (HDD - normal) over Saturday friday-6 .. friday; NaN if any day is missing."""
    s = 0.0
    for k in range(6, -1, -1):
        d = friday - timedelta(days=k)
        if d not in hdd:
            return math.nan
        if d not in norm_cache:
            norm_cache[d] = normal(hdd, d)
        n = norm_cache[d]
        if math.isnan(n):
            return math.nan
        s += hdd[d] - n
    return s


def winter_of(d: date) -> int:
    """Year of the November that starts d's winter (Jan-Mar belong to the previous year)."""
    return d.year if d.month >= 11 else d.year - 1


def season_fridays(first_winter: int, last_winter: int) -> list[date]:
    """Every Friday in Nov..Mar of winters first_winter .. last_winter."""
    d = date(first_winter, 11, 1)
    d += timedelta(days=(4 - d.weekday()) % 7)
    out = []
    end = date(last_winter + 1, 3, 31)
    while d <= end:
        if d.month in SEASON_MONTHS:
            out.append(d)
        d += timedelta(days=7)
    return out


def entry_exit(
    days: Sequence[date], friday: date, last_bar: date, hold: int = HOLD
) -> tuple[int, int] | None:
    """(entry, exit) bar indexes: first bar on/after friday + 4 days, exit `hold` bars later."""
    i = bisect.bisect_left(days, friday + timedelta(days=ENTRY_LAG_DAYS))
    j = i + hold
    if j >= len(days) or days[j] > last_bar:
        return None
    return i, j


def same_week_bars(days: Sequence[date], friday: date) -> tuple[int, int] | None:
    """(start, end) bars of the dose week: last bar before its Saturday, last bar <= friday."""
    a = bisect.bisect_left(days, friday - timedelta(days=6)) - 1
    b = bisect.bisect_right(days, friday) - 1
    if a < 0 or b <= a:
        return None
    return a, b


def offset(friday: date) -> int:
    """Days since November 1 of the Friday's winter."""
    return (friday - date(winter_of(friday), 11, 1)).days


def placebo_friday(
    friday: date, winter: int, by_winter: Mapping[int, Sequence[date]]
) -> date | None:
    """The Friday of `winter` at the same offset from Nov 1 as `friday` (within +-3 days)."""
    o = offset(friday)
    for f in by_winter.get(winter, ()):
        if abs(offset(f) - o) <= 3:
            return f
    return None


def derangements(n: int, count: int, seed: int = SEED) -> list[tuple[int, ...]]:
    """`count` distinct permutations of range(n) with no fixed point, from default_rng(seed)."""
    rng = np.random.default_rng(seed)
    seen: set[tuple[int, ...]] = set()
    out: list[tuple[int, ...]] = []
    while len(out) < count:
        p = tuple(int(v) for v in rng.permutation(n))
        if any(p[i] == i for i in range(n)) or p in seen:
            continue
        seen.add(p)
        out.append(p)
    return out
