"""Pure rules of the wide-5 cards (no data access): the dealer-share surprise of
`dealer-backlog` (research/cards/dealer-backlog.md) and the index extension of
`extension-dose` (research/cards/extension-dose.md)."""

from __future__ import annotations

import bisect
import calendar as _cal
import math
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

import numpy as np


@dataclass(frozen=True)
class Auction:
    cusip: str
    years: int  # leading years of the original term
    announced: date
    auction: date
    issue: date
    maturity: date
    accepted: float  # $ billion
    comp: float | None  # competitive awards, $ billion
    dealer: float | None  # primary dealers' awards, $ billion


def group_of(years: int) -> str | None:
    """`long` (20 years or more, TLT), `ten` (10 years, IEF), else None."""
    if years >= 20:
        return "long"
    return "ten" if years == 10 else None


# --- dealer-backlog ---


def dealer_surprises(
    auctions: Sequence[Auction], group: str, window: int = 12, min_prev: int = 6
) -> list[tuple[date, float]]:
    """(auction date, u) for each auction of `group` with dealer data: u = dealer share of the
    competitive awards in percentage points minus the median share of the previous `window`
    auctions of the group (at least `min_prev` needed)."""
    sel = sorted(
        (a for a in auctions if group_of(a.years) == group and a.comp and a.dealer is not None),
        key=lambda a: (a.auction, a.cusip),
    )
    out: list[tuple[date, float]] = []
    hist: list[float] = []
    for a in sel:
        assert a.comp is not None and a.dealer is not None
        s = 100.0 * a.dealer / a.comp
        if len(hist) >= min_prev:
            out.append((a.auction, s - float(np.median(hist[-window:]))))
        hist.append(s)
    return out


def backlog_sessions(
    cal: Sequence[date], events: Sequence[tuple[date, float]], positive: bool, hold: int = 5
) -> set[date]:
    """Sessions A .. A+`hold`-1 after whose close idle cash goes to the bond, for the auctions
    whose surprise is positive (`positive`) or zero or negative (the placebo). An auction date
    that is not a session of `cal` is dropped."""
    out: set[date] = set()
    for d, u in events:
        if (u > 0) != positive:
            continue
        j = bisect.bisect_left(cal, d)
        if j < len(cal) and cal[j] == d:
            out.update(cal[j : min(j + hold, len(cal))])
    return out


# --- extension-dose ---


def month_end(y: int, m: int) -> date:
    return date(y, m, _cal.monthrange(y, m)[1])


def _holdings(auctions: Sequence[Auction], d: date, asof: date) -> dict[str, tuple[date, float]]:
    """cusip -> (maturity, amount issued on or before `d`), counting auctions held by `asof`."""
    out: dict[str, tuple[date, float]] = {}
    for a in auctions:
        if a.issue <= d and a.auction <= asof and a.maturity > d:
            mat, amt = out.get(a.cusip, (a.maturity, 0.0))
            out[a.cusip] = (mat, amt + a.accepted)
    return out


def _years(mat: date, d: date) -> float:
    return (mat - d).days / 365.25


def _in_bucket(
    held: dict[str, tuple[date, float]], d: date, lo: float, hi: float
) -> dict[str, tuple[date, float]]:
    return {k: v for k, v in held.items() if lo <= _years(v[0], d) <= hi and v[1] > 0}


def _avg_maturity(items: dict[str, tuple[date, float]], d: date) -> float:
    tot = sum(a for _, a in items.values())
    if tot <= 0:
        return math.nan
    return sum(a * _years(m, d) for m, a in items.values()) / tot


def extension(
    auctions: Sequence[Auction], r_prev: date, r: date, asof: date, lo: float, hi: float
) -> float:
    """Par-weighted average remaining maturity at `r` of the bucket rebuilt at `r` (amounts at
    `r`, auctions held by `asof`) minus that of the bucket chosen at `r_prev` (amounts at
    `r_prev`), in years."""
    old = _in_bucket(_holdings(auctions, r_prev, asof), r_prev, lo, hi)
    new = _in_bucket(_holdings(auctions, r, asof), r, lo, hi)
    return _avg_maturity(new, r) - _avg_maturity(old, r)


def month_end_doses(
    cal: Sequence[date], auctions: Sequence[Auction], lo: float, hi: float, first: date, last: date
) -> dict[int, float]:
    """For each month whose last session T in `cal` lies in [first, last]: index of T ->
    E(m), with only auctions held by the close of T-4 counted."""
    out: dict[int, float] = {}
    y, m = first.year, first.month
    while date(y, m, 1) <= last:
        r = month_end(y, m)
        j = bisect.bisect_right(cal, r) - 1
        if j >= 4 and cal[j].month == m and cal[j].year == y and first <= cal[j] <= last:
            py, pm = (y - 1, 12) if m == 1 else (y, m - 1)
            e = extension(auctions, month_end(py, pm), r, cal[j - 4], lo, hi)
            if not math.isnan(e):
                out[j] = e
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def classify(doses: dict[int, float], window: int = 24) -> dict[int, bool]:
    """Index of T -> True if E(m) is above the median of the previous `window` months' E, False
    if at or below; months without `window` predecessors are left out."""
    keys = sorted(doses)
    out: dict[int, bool] = {}
    for n, j in enumerate(keys):
        if n >= window:
            prev = [doses[k] for k in keys[n - window : n]]
            out[j] = doses[j] > float(np.median(prev))
    return out


def ext_sessions(cal: Sequence[date], cls: dict[int, bool], high: bool) -> set[date]:
    """Sessions T-4 .. T-1 after whose close idle cash goes to the bond, in the months classed
    `high` (or not)."""
    out: set[date] = set()
    for j, h in cls.items():
        if h == high:
            out.update(cal[k] for k in range(max(j - 4, 0), j))
    return out


# --- event study ---


def open_excess(opens: np.ndarray, starts: Sequence[int], n: int, base_lo: int) -> np.ndarray:
    """For each start index i: log(open[i+n] / open[i]) minus the average n-session open-to-open
    log return over all windows starting at `base_lo` or later. NaN where i+n is past the end."""
    lo = np.log(opens)
    base = lo[base_lo + n :] - lo[base_lo : len(lo) - n]
    mean = float(base.mean())
    return np.array([lo[i + n] - lo[i] - mean if i + n < len(lo) else math.nan for i in starts])
