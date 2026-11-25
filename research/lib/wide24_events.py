"""Lane wide-24, gate W40 `quake-drift` and replication R40 (research/cards/wide-24.md): pure
functions. Exposure of a market's country to an earthquake, aftershock declustering, the event
session, the dose, the outcome against the other markets and the controls. No function here
reads a file, a price or the network; the tests feed small literal samples. Dates are
`date.toordinal()` integers; times are UTC POSIX seconds."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

MIN_MAG = 6.0
MAX_DEPTH_KM = 70.0
DECLUSTER_KM = 300.0
DECLUSTER_DAYS = 30
H = 20
STALE_DAYS = 7
STEP_DAYS = 23
SHIFTS = [STEP_DAYS * k for k in range(-20, 0)] + [STEP_DAYS * k for k in range(1, 21)]
LAGS = 30
SEED = 24
EARTH_KM = 6371.0


@dataclass(frozen=True)
class Event:
    time: float  # UTC POSIX seconds
    lat: float
    lon: float
    depth_km: float
    mag: float


def radius_km(mag: float) -> float:
    """Rough radius of strong shaking, fixed by the card: 40 km x 10^(0.45 (M - 6.5))."""
    return float(40.0 * 10.0 ** (0.45 * (mag - 6.5)))


def haversine_km(lat1: float, lon1: float, lat2: np.ndarray, lon2: np.ndarray) -> np.ndarray:
    p1, p2 = math.radians(lat1), np.radians(lat2)
    dp = p2 - p1
    dl = np.radians(lon2) - math.radians(lon1)
    a = np.sin(dp / 2) ** 2 + math.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    out: np.ndarray = 2 * EARTH_KM * np.arcsin(np.sqrt(np.clip(a, 0.0, 1.0)))
    return out


def select(events: Sequence[Event], t_lo: float, t_hi: float) -> list[Event]:
    """M >= 6.0, depth <= 70 km (a missing depth fails), origin time in [t_lo, t_hi]."""
    out = [
        e
        for e in events
        if e.mag >= MIN_MAG
        and math.isfinite(e.depth_km)
        and e.depth_km <= MAX_DEPTH_KM
        and t_lo <= e.time <= t_hi
    ]
    return sorted(out, key=lambda e: e.time)


def decluster(events: Sequence[Event]) -> list[Event]:
    """Drop an event if an event of equal or larger magnitude lies within 300 km in the 30 days
    before it (strictly earlier origin time). Input in time order."""
    ev = sorted(events, key=lambda e: e.time)
    win = DECLUSTER_DAYS * 86400.0
    out: list[Event] = []
    lo = 0
    for i, e in enumerate(ev):
        while ev[lo].time < e.time - win:
            lo += 1
        drop = False
        for j in range(lo, i):
            p = ev[j]
            if p.time < e.time and p.mag >= e.mag:
                d = haversine_km(e.lat, e.lon, np.array([p.lat]), np.array([p.lon]))[0]
                if d <= DECLUSTER_KM:
                    drop = True
                    break
        if not drop:
            out.append(e)
    return out


def exposure(
    e: Event, lat: np.ndarray, lon: np.ndarray, pop: np.ndarray, radius: float | None = None
) -> float:
    """S = 100 x population of the country's places within hypocentral distance R / all of the
    country's place population."""
    tot = float(pop.sum())
    if tot <= 0 or len(pop) == 0:
        return 0.0
    r = radius_km(e.mag) if radius is None else radius
    d = haversine_km(e.lat, e.lon, lat, lon)
    hypo = np.sqrt(d**2 + e.depth_km**2)
    return 100.0 * float(pop[hypo <= r].sum()) / tot


def weight(s: float, binary: bool = False) -> float:
    if binary:
        return 1.0 if s >= 1.0 else 0.0
    return math.log2(1.0 + s)


def first_session(dates: np.ndarray, local_day: int) -> int:
    """Index of the first session dated on or after `local_day` (len(dates) if none)."""
    return int(np.searchsorted(dates, local_day, side="left"))


def dose(
    n: int, dates: np.ndarray, pairs: Sequence[tuple[int, float]], shift: int = 0
) -> np.ndarray:
    """D over one market's sessions: each (local day, weight) pair moved by `shift` days lands
    on its first session on or after that day; pairs before the first or after the last session
    drop."""
    d = np.zeros(n)
    if n == 0:
        return d
    for day, w in pairs:
        if w == 0:
            continue
        sd = day + shift
        if sd < dates[0] or sd > dates[-1]:
            continue
        s = first_session(dates, sd)
        if s < n:
            d[s] += w
    return d


def last_close_index(dates: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Index of the last session dated on or before each t (-1 if none)."""
    return np.searchsorted(dates, t, side="right") - 1


def world_change(
    t1: np.ndarray, t2: np.ndarray, others: Sequence[tuple[np.ndarray, np.ndarray]]
) -> np.ndarray:
    """Mean over the other markets (dates, log closes) of ln C_j(t2) - ln C_j(t1), C_j(t) = the
    last close on or before t, a market counting only where both closes are within 7 days of
    their dates. NaN where no market counts."""
    tot = np.zeros(len(t1))
    cnt = np.zeros(len(t1))
    for dj, lj in others:
        if len(dj) == 0:
            continue
        i1 = last_close_index(dj, t1)
        i2 = last_close_index(dj, t2)
        ok = (i1 >= 0) & (i2 >= 0)
        i1c, i2c = np.clip(i1, 0, None), np.clip(i2, 0, None)
        ok &= (t1 - dj[i1c] <= STALE_DAYS) & (t2 - dj[i2c] <= STALE_DAYS)
        ch = lj[i2c] - lj[i1c]
        tot[ok] += ch[ok]
        cnt[ok] += 1
    out = np.full(len(t1), np.nan)
    m = cnt > 0
    out[m] = tot[m] / cnt[m]
    return out


@dataclass(frozen=True)
class Rows:
    s: np.ndarray  # session indices of the rows
    y: np.ndarray  # outcome
    raw: np.ndarray  # own return over the window (no world subtraction)
    r2: np.ndarray
    r20: np.ndarray
    period: np.ndarray  # calendar day of session s+1 (Driscoll-Kraay)


def rows(
    dates: np.ndarray,
    logc: np.ndarray,
    others: Sequence[tuple[np.ndarray, np.ndarray]],
    first_day: int,
    last_day: int,
    h: int = H,
) -> Rows:
    """Rows s with s - 21 >= 0, session s+1+h present and dated <= last_day, date of s in
    [first_day, last_day], and a world change available."""
    n = len(dates)
    s = np.arange(21, max(21, n - 1 - h))
    s = s[(dates[s] >= first_day) & (dates[s] <= last_day) & (dates[s + 1 + h] <= last_day)]
    t1, t2 = dates[s + 1], dates[s + 1 + h]
    w = world_change(t1, t2, others)
    raw = logc[s + 1 + h] - logc[s + 1]
    ok = np.isfinite(w)
    s, w, raw = s[ok], w[ok], raw[ok]
    return Rows(
        s=s,
        y=raw - w,
        raw=raw,
        r2=logc[s + 1] - logc[s - 1],
        r20=logc[s - 1] - logc[s - 21],
        period=dates[s + 1].astype(int),
    )


def rank_lowest(true: float, others: Sequence[float]) -> int:
    return 1 + sum(1 for v in others if v < true)


def null_spread(v: Sequence[float]) -> tuple[float, float, float, float, float, float, float]:
    a = np.asarray([x for x in v if math.isfinite(x)])
    q5, q50, q95 = np.quantile(a, [0.05, 0.5, 0.95])
    return (
        float(a.std(ddof=1)),
        float(np.mean(np.abs(a) >= 2)),
        float(q5),
        float(q50),
        float(q95),
        float(a.min()),
        float(a.max()),
    )


def acf1(series: Sequence[np.ndarray]) -> float:
    """Pooled lag-1 autocorrelation of within-series demeaned values."""
    num = den = 0.0
    for x in series:
        if len(x) < 2:
            continue
        z = x - x.mean()
        num += float(z[1:] @ z[:-1])
        den += float(z @ z)
    return num / den if den > 0 else math.nan
