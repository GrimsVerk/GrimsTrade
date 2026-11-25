"""Pure functions for the wide-21 gate W35 `solar-max-recession` (research/cards/wide-21.md).
No function here reads a file, a price or the network. Months are indexed as in
`wide17_events.month_index` (January 2000 -> 24000)."""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping, Sequence
from datetime import date

from wide17_events import month_index

# Months, both ways (the sun does not answer prices): +-19, 23, ..., 95; every |k| at least 19
# months from 0 and at least 37 from the 132-month solar cycle (the card's "37 from both" is a
# slip, see research/wide-21.md).
SHIFTS: list[int] = [s * k for k in range(19, 96, 4) for s in (1, -1)]
CYCLE = 132
# R35 (only if W35 passes): years, multiples of the cycle (10-12, 21-23) left out.
SHIFTS_YEARS: list[int] = [
    s * k for k in [*range(2, 10), *range(13, 21), *range(24, 28)] for s in (1, -1)
]


def parse_silso(text: str, last: date) -> dict[int, float]:
    """Monthly mean total sunspot number by month index from SILSO's `SN_m_tot_V2.0` CSV
    (semicolon-separated: year; month; decimal year; mean; sd; observations; provisional flag).
    Negative means (missing) and months after the month of `last` are left out."""
    out: dict[int, float] = {}
    cut = month_index(last)
    for row in text.splitlines():
        parts = [p.strip() for p in row.split(";")]
        if len(parts) < 4:
            continue
        try:
            y, mo, v = int(parts[0]), int(parts[1]), float(parts[3])
        except ValueError:
            continue
        m = y * 12 + mo - 1
        if not 1 <= mo <= 12 or m > cut or v < 0:
            continue
        out[m] = v
    return out


def trailing_dose(sn: Mapping[int, float], months: int = 12) -> dict[int, float]:
    """x(m) = mean of SN(m - j), j = 0..months-1, divided by 100; only where all months exist."""
    out: dict[int, float] = {}
    for m in sn:
        vals = [sn.get(m - j) for j in range(months)]
        if all(v is not None for v in vals):
            out[m] = sum(v for v in vals if v is not None) / months / 100.0
    return out


def phase_dose(x: Mapping[int, float]) -> dict[int, float]:
    """x(m) - x(m - 12): rising (> 0) or falling activity."""
    return {m: v - x[m - 12] for m, v in x.items() if m - 12 in x}


def shifted(d: Mapping[int, float], m: int, k: int) -> float:
    """d_k(m) = d(m - k); NaN if missing."""
    return d.get(m - k, math.nan)


def parse_shiller(rows: Iterable[Sequence[object]], last: date) -> dict[int, tuple[float, float]]:
    """{month index: (P, D)} from the rows of Shiller's `ie_data.xls` sheet `Data` (column 0 the
    date as year.month, e.g. 1871.01 or 1871.1 for October; column 1 P; column 2 D). Rows without
    a numeric date and P are skipped; a D that is not a positive number takes the last reported
    D. Months after the month of `last` are left out."""
    cut = month_index(last)
    raw: dict[int, tuple[float, object]] = {}
    for r in rows:
        if len(r) < 3 or not isinstance(r[0], float) or not isinstance(r[1], float):
            continue
        y = int(r[0])
        mo = round((r[0] - y) * 100)
        if not 1 <= mo <= 12 or r[1] <= 0:
            continue
        m = y * 12 + mo - 1
        if m <= cut:
            raw[m] = (r[1], r[2])
    out: dict[int, tuple[float, float]] = {}
    d_last = math.nan
    for m in sorted(raw):
        p, d = raw[m]
        if isinstance(d, float) and d > 0:
            d_last = d
        out[m] = (p, d_last)
    return out


def shiller_return(sh: Mapping[int, tuple[float, float]], m: int, h: int = 1) -> float:
    """y(m) = ln(P(m+1+h) / P(m+1) + sum_{i=2..h+1} D(m+i) / 12 / P(m+1)): total return from the
    average price of month m+1 to that of month m+1+h (h = 1: the gate's outcome
    ln((P(m+2) + D(m+2) / 12) / P(m+1))). NaN if a month or a dividend is missing."""
    need = [sh.get(m + i) for i in range(1, h + 2)]
    if any(v is None for v in need):
        return math.nan
    vals = [v for v in need if v is not None]
    p0 = vals[0][0]
    divs = sum(v[1] for v in vals[1:]) / 12.0
    if math.isnan(divs):
        return math.nan
    return math.log((vals[-1][0] + divs) / p0)


def fall_within(
    sh: Mapping[int, tuple[float, float]], m: int, h: int = 12, cut: float = 0.8
) -> float:
    """1.0 if min P over months m+1..m+h is at most `cut` x P(m+1), else 0.0; NaN if any month
    is missing."""
    ps = [sh.get(m + i) for i in range(1, h + 1)]
    if any(v is None for v in ps):
        return math.nan
    vals = [v[0] for v in ps if v is not None]
    return 1.0 if min(vals) <= cut * vals[0] else 0.0


def smoothed13(sn: Mapping[int, float]) -> dict[int, float]:
    """SILSO's 13-month tapered running mean (half weights at both ends); uses six months after
    m (look-ahead: shown cells only)."""
    out: dict[int, float] = {}
    for m in sn:
        vals = [sn.get(m + j) for j in range(-6, 7)]
        if all(v is not None for v in vals):
            v = [x for x in vals if x is not None]
            out[m] = (0.5 * v[0] + sum(v[1:12]) + 0.5 * v[12]) / 12.0
    return out


def maxima(sm: Mapping[int, float], half_width: int = 48) -> list[int]:
    """Months where the smoothed series is the strict maximum of the window m +- half_width
    (one per solar cycle when half_width is about 4 years)."""
    out = []
    for m, v in sm.items():
        window = [sm[j] for j in range(m - half_width, m + half_width + 1) if j in sm and j != m]
        if len(window) >= half_width and all(v > w for w in window):
            out.append(m)
    return sorted(out)


def window_indicator(
    months: Iterable[int], peaks: Sequence[int], before: int = 12, after: int = 24
) -> dict[int, float]:
    """1.0 for months in [peak - before, peak + after] of any peak, else 0.0."""
    return {m: 1.0 if any(p - before <= m <= p + after for p in peaks) else 0.0 for m in months}


def annual_mean(sn: Mapping[int, float]) -> dict[int, float]:
    """Calendar-year mean of SN / 100, only years with 12 months."""
    by: dict[int, list[float]] = {}
    for m, v in sn.items():
        by.setdefault(m // 12, []).append(v)
    return {y: sum(v) / 1200.0 for y, v in by.items() if len(v) == 12}
