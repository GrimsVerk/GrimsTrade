"""Pure functions for the wide-13 gates W25 `act-haven` and W26 `failure-premium`
(research/wide-13.md steps 2 and 3). No function here reads a file, a price or the network."""

from __future__ import annotations

import bisect
import math
from collections.abc import Iterable, Mapping, Sequence
from datetime import date, timedelta

import numpy as np

# Placebo shifts in weeks: odd 27..103 in steps of 4, both signs (40), as wide-11/12.
SHIFTS: list[int] = [s * k for k in range(27, 104, 4) for s in (1, -1)]


def mondays(lo: date, hi: date) -> list[date]:
    """Every Monday in lo .. hi."""
    d = lo + timedelta(days=(0 - lo.weekday()) % 7)
    out = []
    while d <= hi:
        out.append(d)
        d += timedelta(days=7)
    return out


def fridays(lo: date, hi: date) -> list[date]:
    """Every Friday in lo .. hi."""
    d = lo + timedelta(days=(4 - lo.weekday()) % 7)
    out = []
    while d <= hi:
        out.append(d)
        d += timedelta(days=7)
    return out


def weekly_log_mean(daily: Mapping[date, float], ends: Iterable[date]) -> dict[date, float]:
    """d(M) = ln(1 + mean of the daily values over M - 6 .. M), for each end day M with all
    seven days present and not NaN (the GPR file has no gaps; a gap leaves the week out)."""
    out: dict[date, float] = {}
    for m in ends:
        vals = [daily.get(m - timedelta(days=i), math.nan) for i in range(7)]
        if any(v != v for v in vals):
            continue
        out[m] = math.log(1.0 + sum(vals) / 7.0)
    return out


def failure_dose(
    failures: Iterable[tuple[date, float]], weeks: Sequence[date], last: date
) -> dict[date, float]:
    """x(F) = ln(1 + S(F)) for each Friday F in `weeks` with F <= `last`, where S(F) is the sum
    of total assets (thousands of USD; NaN counts 0) of the failures dated F - 6 .. F, in
    millions of USD. Failures dated after `last` are never read. 0 in weeks without one."""
    s: dict[date, float] = {f: 0.0 for f in weeks if f <= last}
    for day, assets_k in failures:
        if day > last:
            continue
        f = day + timedelta(days=(4 - day.weekday()) % 7)  # the Friday ending its week
        if f in s and assets_k == assets_k:
            s[f] += assets_k / 1000.0
    return {f: math.log1p(v) for f, v in s.items()}


def shifted(dose: Mapping[date, float], t: date, k: int) -> float:
    """dose_k(t) = dose(t - 7k days); NaN if missing."""
    return dose.get(t - timedelta(days=7 * k), math.nan)


class Closes:
    """Daily closes of one asset with first-on-or-after / last-on-or-before lookups."""

    def __init__(self, bars: Mapping[date, float]):
        self.days = sorted(bars)
        self.c = bars

    def first_on_or_after(self, d: date) -> date | None:
        i = bisect.bisect_left(self.days, d)
        return self.days[i] if i < len(self.days) else None

    def last_on_or_before(self, d: date) -> date | None:
        i = bisect.bisect_right(self.days, d)
        return self.days[i - 1] if i > 0 else None


def window_return(px: Closes, t: date, entry: int, exit_: int, slack: int, last: date) -> float:
    """ln(close of the first bar >= t + exit_ / close of the first bar >= t + entry). NaN if a
    bar is missing, the exit bar is after t + exit_ + slack or after `last`, or exit <= entry."""
    a = px.first_on_or_after(t + timedelta(days=entry))
    b = px.first_on_or_after(t + timedelta(days=exit_))
    if a is None or b is None or b > last or b > t + timedelta(days=exit_ + slack) or b <= a:
        return math.nan
    return math.log(px.c[b] / px.c[a])


def reaction_return(px: Closes, t: date, entry: int, last: date) -> float:
    """ln(close of the first bar >= t + entry / close of the last bar <= t): the move from the
    last close before the news to the first close after it. NaN if missing or after `last`."""
    a = px.last_on_or_before(t)
    b = px.first_on_or_after(t + timedelta(days=entry))
    if a is None or b is None or b > last or b > t + timedelta(days=entry + 7):
        return math.nan
    return math.log(px.c[b] / px.c[a])


def past_return(px: Closes, t: date, back_days: int) -> float:
    """ln(close of the last bar <= t / close of the last bar <= t - back_days)."""
    a = px.last_on_or_before(t - timedelta(days=back_days))
    b = px.last_on_or_before(t)
    if a is None or b is None or a == b:
        return math.nan
    return math.log(px.c[b] / px.c[a])


def quantiles(ts: Sequence[float]) -> tuple[float, float, float]:
    a = np.asarray(ts, dtype=float)
    q = np.quantile(a, [0.05, 0.5, 0.95])
    return float(q[0]), float(q[1]), float(q[2])
