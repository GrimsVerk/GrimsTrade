"""Pure functions for the wide-8 event gates (research/wide-8.md, steps 2 and 3). Kept apart
from `wide8_rules.py`, whose hash is part of the proposed forward entry of step 1."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from datetime import date, timedelta

import numpy as np

# --- Step 2: W16 geomagnetic storms ---

SEVERE = 100
MINOR = 30
STORM_SESSIONS = 6


def parse_ap(text: str) -> dict[date, int]:
    """Daily Ap from GFZ's Kp_ap_Ap_SN_F107 file (blank-separated: YYYY MM DD days days_m Bsr
    dB Kp1..Kp8 ap1..ap8 Ap ...; Ap is field 24, index 23). Missing values (-1) are left out."""
    out: dict[date, int] = {}
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split()
        ap = int(f[23])
        if ap >= 0:
            out[date(int(f[0]), int(f[1]), int(f[2]))] = ap
    return out


def storm_max(days: Sequence[date], ap: Mapping[date, int], shift: int = 0) -> np.ndarray:
    """M(t): the largest Ap(d) over UT days d with date(t-6) <= d < date(t), i.e. the storms
    whose six-session window (the first six sessions dated after d) holds session t. The Ap
    calendar is moved later by `shift` days (Ap of day d - shift); days outside it count as 0.
    NaN for the first six sessions."""
    out = np.full(len(days), math.nan)
    for t in range(STORM_SESSIONS, len(days)):
        d, best = days[t - STORM_SESSIONS], 0
        while d < days[t]:
            best = max(best, ap.get(d - timedelta(days=shift), 0))
            d += timedelta(days=1)
        out[t] = best
    return out


def storm_design(m: np.ndarray, severe: int = SEVERE, minor: int = MINOR) -> np.ndarray:
    """Columns: constant, Sev = M >= severe, Min = minor <= M < severe."""
    sev = (m >= severe).astype(float)
    mnr = ((m >= minor) & (m < severe)).astype(float)
    return np.column_stack([np.ones(len(m)), sev, mnr])


def rank_most_negative(true: float, others: Sequence[float]) -> int:
    """1 + the number of others strictly below `true` (1 = most negative)."""
    return 1 + sum(o < true for o in others)


# --- Step 3: W15 hurricane landfalls ---

Fix = tuple[date, str, float, float, int]  # day, record id, lat (N), lon (E; west < 0), wind kt


def _coord(s: str) -> float:
    v = float(s[:-1])
    return -v if s[-1] in "SW" else v


def parse_hurdat(text: str) -> dict[str, tuple[str, list[Fix]]]:
    """HURDAT2: a header line `AL011851, UNNAMED, 14,` then that many data lines
    `YYYYMMDD, HHMM, RI, ST, LAT, LON, WIND, ...`. Returns {storm id: (name, fixes)}."""
    out: dict[str, tuple[str, list[Fix]]] = {}
    cur: list[Fix] = []
    for line in text.splitlines():
        f = [x.strip() for x in line.split(",")]
        if len(f) < 4:
            continue
        if f[0][:2].isalpha():
            cur = []
            out[f[0]] = (f[1], cur)
            continue
        d = date(int(f[0][:4]), int(f[0][4:6]), int(f[0][6:8]))
        cur.append((d, f[2], _coord(f[4]), _coord(f[5]), int(f[6])))
    return out


def us_mainland(lat: float, lon: float) -> bool:
    """The box of research/wide-8.md step 3 (lon in degrees east; west is negative)."""
    if lat < 24.4 or lon < -98.0 or lon > -66.9:
        return False
    if lat < 30.0 and lon > -80.0:  # Bahamas
        return False
    return not (lat < 25.85 and lon < -97.0)  # Mexico


def category(wind: int) -> int:
    for k, lo in ((5, 137), (4, 113), (3, 96), (2, 83), (1, 64)):
        if wind >= lo:
            return k
    return 0


def landfall_events(storms: Mapping[str, tuple[str, list[Fix]]]) -> list[tuple[str, date, int]]:
    """(storm id, event day, category) for each storm with a US mainland landfall record:
    event day = date of the first such record, category from the largest wind over them."""
    out = []
    for sid, (_, fixes) in storms.items():
        us = [x for x in fixes if x[1] == "L" and us_mainland(x[2], x[3])]
        if us:
            out.append((sid, us[0][0], category(max(x[4] for x in us))))
    return sorted(out, key=lambda e: e[1])


def after_return(days: Sequence[date], logc: np.ndarray, d: date, n: int) -> float:
    """Log return from the last close on or before d to the close of the n-th session dated
    after d; NaN if either bar is missing."""
    import bisect

    i = bisect.bisect_right(days, d) - 1
    if i < 0 or i + n >= len(days):
        return math.nan
    return float(logc[i + n] - logc[i])


def shift_years(d: date, k: int) -> date:
    y = d.year + k
    return date(y, d.month, 28) if (d.month, d.day) == (2, 29) else date(y, d.month, d.day)
