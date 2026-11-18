"""Pure functions for lane wide-8 (research/wide-8.md). No I/O, so the tests can check each
piece on made-up data.

Step 1: the turn-of-year loser rebound as a forward test. One "window" = an anchor month m of
year Y: dose = the loss over the eleven months ending at the end of month m-1 (start: the end of
month m of Y-1), outcome = the return from the end of month m to ten calendar days later. For
m = 12 that is the YTD loss to the end of November and the 31 Dec .. 10 Jan return (wide-7's
turn-of-year cell); m = 1..11 are the placebo windows whose t values make the null.
"""

from __future__ import annotations

import bisect
import calendar
import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from datetime import date, timedelta
from typing import Any

import numpy as np

OUTCOME_DAYS = 10
MIN_FUNDS = 15
MIN_LOSERS = 3


def month_end(y: int, m: int) -> date:
    return date(y, m, calendar.monthrange(y, m)[1])


def shift_month(y: int, m: int, k: int) -> tuple[int, int]:
    n = y * 12 + (m - 1) + k
    return n // 12, n % 12 + 1


def last_on_or_before(days: Sequence[date], d: date) -> int:
    return bisect.bisect_right(days, d) - 1


def window_point(
    days: Sequence[date], logc: np.ndarray, y: int, m: int, last: date
) -> tuple[float, float] | None:
    """(L, R) for one fund at anchor (y, m), or None if its bars do not cover the window.
    `last` = the last date whose bars may be read and are complete."""
    e = month_end(y, m)
    if e + timedelta(days=OUTCOME_DAYS) > last:
        return None
    py, pm = shift_month(y, m, -1)
    i0 = last_on_or_before(days, month_end(y - 1, m))
    i1 = last_on_or_before(days, month_end(py, pm))
    if i0 < 0 or i1 <= i0 or (days[i1].year, days[i1].month) != (py, pm):
        return None
    j0 = last_on_or_before(days, e)
    j1 = last_on_or_before(days, e + timedelta(days=OUTCOME_DAYS))
    if j0 < i1 or j1 <= j0:
        return None
    dose = float(logc[i1] - logc[i0])
    return max(0.0, -dose), float(logc[j1] - logc[j0])


def cross_t(loss: Sequence[float], ret: Sequence[float]) -> tuple[float, float]:
    """OLS slope of ret on loss with an intercept, and its plain t (residual variance on n - 2
    degrees of freedom). NaN if fewer than 3 points or no spread in loss."""
    x, y = np.asarray(loss, float), np.asarray(ret, float)
    n = len(x)
    if n < 3:
        return math.nan, math.nan
    xc = x - x.mean()
    sxx = float(xc @ xc)
    if sxx <= 0:
        return math.nan, math.nan
    b = float(xc @ (y - y.mean())) / sxx
    e = y - y.mean() - b * xc
    s2 = float(e @ e) / (n - 2)
    if s2 <= 0:
        return b, math.copysign(math.inf, b)
    return b, b / math.sqrt(s2 / sxx)


def eligible(points: Sequence[tuple[float, float]]) -> bool:
    return len(points) >= MIN_FUNDS and sum(lo > 0 for lo, _ in points) >= MIN_LOSERS


def empirical_p(t: float, null: Sequence[float]) -> float:
    """One-sided p of t against the null list: (1 + #null >= t) / (1 + len(null))."""
    return (1 + sum(v >= t for v in null)) / (1 + len(null))


def power(
    windows: Sequence[Sequence[tuple[float, float]]],
    null: Sequence[float],
    bstar: float,
    alpha: float,
) -> float:
    """Share of placebo windows that pass (b > 0 and p <= alpha) once b* L is added to R."""
    hits = 0
    for pts in windows:
        lo = [p[0] for p in pts]
        b, t = cross_t(lo, [r + bstar * x for x, r in pts])
        hits += b > 0 and empirical_p(t, null) <= alpha
    return hits / len(windows) if windows else math.nan


def verdict(
    points: Sequence[tuple[float, float]], null: Sequence[float], alpha: float
) -> dict[str, Any]:
    """The forward scoring rule of research/wide-8.md, step 1, on one turn's (L, R) points."""
    n_los = sum(lo > 0 for lo, _ in points)
    out: dict[str, Any] = {"funds": len(points), "losers": n_los}
    if not eligible(points):
        out["verdict"] = "no verdict (too few funds or losers): score the next turn"
        return out
    b, t = cross_t([p[0] for p in points], [p[1] for p in points])
    p = empirical_p(t, null)
    out.update(b=b, t=t, p=p, verdict="pass" if b > 0 and p <= alpha else "fail")
    return out


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def rule_hash(code: Mapping[str, str], params: Mapping[str, Any], data: Mapping[str, Any]) -> str:
    """As `grimstrade.forward.rule_hash` on branch forward-1."""
    obj = {"code": dict(code), "params": dict(params), "data": dict(data)}
    return hashlib.sha256(canonical(obj)).hexdigest()
