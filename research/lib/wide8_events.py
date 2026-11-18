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
