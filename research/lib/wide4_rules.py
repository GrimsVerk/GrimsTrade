"""Pure rules of the wide-4 cards (no data access): tax dates and regimes for `tax-drain`
(research/cards/tax-drain.md)."""

from __future__ import annotations

import bisect
import math
from collections.abc import Callable, Sequence
from datetime import date

import numpy as np

TAX_MONTHS = (1, 4, 6, 9, 12)
TGA_START = date(2008, 12, 16)  # funds-rate target range 0-0.25%: cash kept in the TGA
TTL_END = date(2008, 9, 14)  # the day before Lehman; 2008-09-15 .. 2008-12-15 is a transition
# regime C: the Fed shrinking its balance sheet, reserves no longer abundant
TIGHT = ((date(2018, 1, 1), date(2019, 12, 31)), (date(2022, 6, 1), date(2099, 12, 31)))


def statutory_dates(first_year: int, last_year: int) -> list[date]:
    """The 15th of Jan, Apr, Jun, Sep and Dec; in 2020 April and June moved to 15 July."""
    out = []
    for y in range(first_year, last_year + 1):
        months = (1, 7, 9, 12) if y == 2020 else TAX_MONTHS
        out += [date(y, m, 15) for m in months]
    return out


def tax_sessions(cal: Sequence[date], dates: Sequence[date]) -> list[int]:
    """Index in `cal` of D, the first session on or after each statutory date."""
    out = []
    for d in dates:
        j = bisect.bisect_left(cal, d)
        if j < len(cal) and (cal[j] - d).days < 7:
            out.append(j)
    return out


def out_sessions(
    cal: Sequence[date],
    ds: Sequence[int],
    active: tuple[date, date],
    before: int = 2,
    after: int = 2,
) -> set[date]:
    """Sessions after whose close the gated slots are empty: D-`before` .. D+`after` for each tax
    session D whose date lies in `active` (inclusive). With next-open fills the slots then miss
    the returns of sessions D-1 .. D+3."""
    out: set[date] = set()
    for j in ds:
        if not active[0] <= cal[j] <= active[1]:
            continue
        for k in range(max(j - before, 0), min(j + after + 1, len(cal))):
            out.add(cal[k])
    return out


def regime(d: date) -> str | None:
    """'A' (TT&L era), 'B' (TGA era, abundant reserves), 'C' (TGA era, reserves shrinking)."""
    if d <= TTL_END:
        return "A"
    if d < TGA_START:
        return None
    return "C" if any(a <= d <= b for a, b in TIGHT) else "B"


def window_excess(
    cal: Sequence[date],
    level: np.ndarray,
    ds: Sequence[int],
    keep: Callable[[date], bool],
    lo: int = 2,
    hi: int = 3,
    log: bool = True,
) -> np.ndarray:
    """For each D in `ds` with `keep(D)`: the change from session D-`lo` to D+`hi` (log return
    of a price if `log`, plain difference of a balance otherwise), minus the average change of
    all windows of the same length whose centre session (the window's D) passes `keep`.
    NaN levels are skipped."""
    x = np.log(level) if log else np.asarray(level, dtype=float)
    n = len(x)

    def chg(j: int) -> float:
        return float(x[j + hi] - x[j - lo]) if j - lo >= 0 and j + hi < n else math.nan

    base = np.array([chg(j) for j in range(n) if keep(cal[j])])
    base = base[~np.isnan(base)]
    ev = np.array([chg(j) for j in ds if keep(cal[j])])
    ev = ev[~np.isnan(ev)]
    if not len(base) or not len(ev):
        return np.array([])
    return ev - base.mean()
