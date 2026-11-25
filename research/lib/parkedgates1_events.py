"""Pure functions for the parked-gates-1 gates W32 `drought-inflation` and W33
`margin-susceptibles` (research/cards/parked-gates-1.md). No function here reads a file, a price
or the network."""

from __future__ import annotations

import csv
import io
import math
from collections.abc import Mapping
from datetime import date

from wide17_events import month_index

# W33: months, earlier doses only (margin credit answers prices), odd k from 25 to 103.
SHIFTS_W33: list[int] = list(range(25, 104, 2))
NATIONAL = "110"  # nClimDiv code of the contiguous US
PDSI = "05"  # nClimDiv element code of the Palmer drought severity index


def parse_pdsi(text: str, last: date, code: str = NATIONAL) -> dict[int, float]:
    """PDSI by month index for one nClimDiv state code from a `climdiv-pdsist` file. Each row:
    3-digit code, 1-digit division, 2-digit element, 4-digit year, then 12 values; -99.99 is
    missing. Months after the month of `last` are left out."""
    out: dict[int, float] = {}
    cut = month_index(last)
    for row in text.splitlines():
        parts = row.split()
        if len(parts) != 13 or len(parts[0]) != 10:
            continue
        head = parts[0]
        if head[:3] != code or head[4:6] != PDSI:
            continue
        y = int(head[6:10])
        for j, v in enumerate(parts[1:]):
            m = y * 12 + j
            x = float(v)
            if m > cut or x <= -99:
                continue
            out[m] = x
    return out


def drought_dose(pdsi: Mapping[int, float]) -> dict[int, float]:
    """D(m) = -PDSI(m) (positive = drier)."""
    return {m: -v for m, v in pdsi.items()}


def drought_change(pdsi: Mapping[int, float]) -> dict[int, float]:
    """PDSI(m-3) - PDSI(m): drying over the last three months (positive = drier)."""
    return {m: pdsi[m - 3] - v for m, v in pdsi.items() if m - 3 in pdsi}


def parse_fred(text: str, last: date) -> dict[int, float]:
    """Quarterly FRED graph CSV (observation_date = first day of the quarter) -> value by the
    month index of the quarter's END month. Quarters ending after `last` and '.' cells are
    left out."""
    out: dict[int, float] = {}
    cut = month_index(last)
    for r in csv.reader(io.StringIO(text)):
        if len(r) < 2:
            continue
        try:
            d = date.fromisoformat(r[0].strip())
            v = float(r[1])
        except ValueError:
            continue
        end = month_index(d) + 2
        if end <= cut:
            out[end] = v
    return out


def susceptible_dose(recv: Mapping[int, float], mv: Mapping[int, float]) -> dict[int, float]:
    """s(q) = ln(R/V)(q) minus the mean of ln(R/V) over the 40 quarters before (keyed by
    quarter-end month index; NaN, i.e. absent, without all 40)."""
    ls = {q: math.log(recv[q] / mv[q]) for q in recv if q in mv and recv[q] > 0 and mv[q] > 0}
    out = {}
    for q, v in ls.items():
        base = [ls.get(q - 3 * i) for i in range(1, 41)]
        if all(b is not None for b in base):
            out[q] = v - sum(b for b in base if b is not None) / 40
    return out


def monthly_known(quarterly: Mapping[int, float], lag: int) -> dict[int, float]:
    """For each decision month m: the value of the latest quarter whose end month is <= m - lag
    (only months up to the last quarter end + lag + 2, so no value is carried past the next
    quarter's release)."""
    if not quarterly:
        return {}
    ends = sorted(quarterly)
    out = {}
    for m in range(ends[0] + lag, ends[-1] + lag + 3):
        q = max(e for e in ends if e <= m - lag)
        out[m] = quarterly[q]
    return out


def fall(r: float) -> float:
    """Trigger F = min(r, 0) (NaN stays NaN)."""
    return r if math.isnan(r) else min(r, 0.0)


# ---------------------------------------------------------------- R32 replication


def parse_fred_daily(text: str, last: date) -> dict[date, float]:
    """Daily FRED graph CSV -> value by day; '.' cells and days after `last` left out."""
    out: dict[date, float] = {}
    for r in csv.reader(io.StringIO(text)):
        if len(r) < 2:
            continue
        try:
            d = date.fromisoformat(r[0].strip())
            v = float(r[1])
        except ValueError:
            continue
        if d <= last:
            out[d] = v
    return out


def parse_fred_monthly(text: str, last: date) -> dict[int, float]:
    """Monthly FRED graph CSV (first day of the month) -> value by month index; months after
    the month of `last` left out."""
    out: dict[int, float] = {}
    cut = month_index(last)
    for d, v in parse_fred_daily(text, date.max).items():
        m = month_index(d)
        if m <= cut:
            out[m] = v
    return out


def month_end_values(daily: Mapping[date, float]) -> dict[int, float]:
    """Value on the last day with a value in each month, by month index."""
    out: dict[int, tuple[date, float]] = {}
    for d, v in daily.items():
        m = month_index(d)
        if m not in out or d > out[m][0]:
            out[m] = (d, v)
    return {m: v for m, (_, v) in out.items()}
