"""Pure functions for the survey-7 `seasonal-20y` gate (research/survey-7.md)."""

from __future__ import annotations

import bisect
import calendar
import math
from collections.abc import Mapping, Sequence
from datetime import date, timedelta

import numpy as np

Month = tuple[int, int]  # (year, month)

YEARS = 20  # annual lags averaged
MIN_YEARS = 5  # fewest lags an asset needs for a signal
MIN_N = 6  # fewest assets in a month's cross-section
MAX_GAP = 5  # a Friday's close may come from a bar at most this many days earlier

# The placebo family of research/survey-7.md: lags 12j + s, j = 1 + a .. 20 + a.
PLACEBOS: list[tuple[int, int]] = [(s, a) for s in range(1, 11) for a in range(4)]


def add_months(ym: Month, k: int) -> Month:
    n = ym[0] * 12 + ym[1] - 1 + k
    return (n // 12, n % 12 + 1)


def months(a: Month, b: Month) -> list[Month]:
    out, cur = [], a
    while cur <= b:
        out.append(cur)
        cur = add_months(cur, 1)
    return out


def month_returns(days: Sequence[date], logc: Sequence[float]) -> dict[Month, float]:
    """r(m) = log close of the last bar of month m minus that of month m - 1 (both months must
    have bars). Every month present in `days` is treated as complete: callers cut the sample."""
    last: dict[Month, float] = {}
    for d, x in zip(days, logc, strict=True):
        last[(d.year, d.month)] = float(x)
    return {m: v - last[add_months(m, -1)] for m, v in last.items() if add_months(m, -1) in last}


def last_friday(ym: Month) -> date:
    """F(M): the last Friday on or before the last calendar day of month M."""
    d = date(ym[0], ym[1], calendar.monthrange(*ym)[1])
    return d - timedelta(days=(d.weekday() - 4) % 7)


def close_on_or_before(days: Sequence[date], logc: Sequence[float], d: date) -> float:
    """Log close of the last bar on or before d, if it is at most MAX_GAP days earlier."""
    i = bisect.bisect_right(days, d) - 1
    if i < 0 or (d - days[i]).days > MAX_GAP:
        return math.nan
    return float(logc[i])


def friday_return(days: Sequence[date], logc: Sequence[float], ym: Month) -> float:
    """R(M): close on or before F(M) minus close on or before F(M - 1), in logs."""
    a = close_on_or_before(days, logc, last_friday(add_months(ym, -1)))
    b = close_on_or_before(days, logc, last_friday(ym))
    return b - a


def signal(mret: Mapping[Month, float], ym: Month, s: int = 0, a: int = 0) -> tuple[float, int]:
    """(S, years used): mean of r over the months 12j + s before `ym`, j = 1 + a .. 20 + a,
    as many as exist; NaN if fewer than MIN_YEARS."""
    vals = [
        mret[m] for j in range(1 + a, YEARS + a + 1) if (m := add_months(ym, -(12 * j + s))) in mret
    ]
    if len(vals) < MIN_YEARS:
        return math.nan, len(vals)
    return float(np.mean(vals)), len(vals)


def spread(sig: Mapping[str, float], ret: Mapping[str, float]) -> tuple[float, int]:
    """(y, n): top-k minus bottom-k mean holding return, k = max(1, round(n / 5)), over the
    assets with both a finite signal and a finite return; NaN if n < MIN_N. Ties in the signal
    are broken by symbol name."""
    ok = [x for x in sorted(sig) if math.isfinite(sig[x]) and math.isfinite(ret.get(x, math.nan))]
    n = len(ok)
    if n < MIN_N:
        return math.nan, n
    ranked = sorted(ok, key=lambda x: sig[x])  # stable: ties stay in name order
    k = max(1, round(n / 5))
    top = float(np.mean([ret[x] for x in ranked[-k:]]))
    bottom = float(np.mean([ret[x] for x in ranked[:k]]))
    return top - bottom, n


def mean_t(y: Sequence[float]) -> tuple[float, float, int]:
    """(mean, plain t, n) over the finite values."""
    a = np.asarray([v for v in y if math.isfinite(v)], dtype=float)
    if len(a) < 2:
        return math.nan, math.nan, len(a)
    sd = float(a.std(ddof=1))
    return (
        float(a.mean()),
        float(a.mean() / (sd / math.sqrt(len(a)))) if sd > 0 else math.nan,
        len(a),
    )


def rank_highest(true: float, others: Sequence[float]) -> int:
    """1 + the number of others strictly above `true` (1 = the highest)."""
    return 1 + sum(o > true for o in others)


def null_summary(ts: Sequence[float]) -> dict[str, float]:
    """Gate-null step 5: sd, share with |t| >= 2, 5/50/95% quantiles, min, max."""
    a = np.asarray(ts, dtype=float)
    q5, q50, q95 = (float(v) for v in np.quantile(a, [0.05, 0.5, 0.95]))
    return {
        "sd": float(a.std(ddof=1)),
        "share2": float(np.mean(np.abs(a) >= 2)),
        "q5": q5,
        "q50": q50,
        "q95": q95,
        "min": float(a.min()),
        "max": float(a.max()),
    }
