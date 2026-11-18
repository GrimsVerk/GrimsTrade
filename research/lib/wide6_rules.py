"""Pure functions for the wide-6 event-study gates (research/wide-6.md): rolling early-warning
indicators, their Kendall trend, the forward maximum drawdown, OLS with Driscoll-Kraay errors,
and lunar phase dates. No I/O here, so the tests can check each piece on made-up data."""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import UTC, date, datetime, timedelta

import numpy as np
from scipy import stats as sps


def _roll_sum(x: np.ndarray, w: int) -> np.ndarray:
    """Sum of x[i-w+1 .. i] at each i (NaN before a full window)."""
    out = np.full(len(x), np.nan)
    if len(x) < w:
        return out
    c = np.concatenate([[0.0], np.cumsum(x)])
    out[w - 1 :] = c[w:] - c[: len(x) - w + 1]
    return out


def rolling_ac1(x: np.ndarray, w: int) -> np.ndarray:
    """Lag-1 autocorrelation of x over the window x[i-w+1 .. i], at each i: the Pearson
    correlation of the w-1 pairs (x[j-1], x[j]) inside the window. NaN before a full window."""
    out = np.full(len(x), np.nan)
    if len(x) < w or w < 3:
        return out
    a, b = x[:-1], x[1:]  # pair j (ending at index j+1)
    m = w - 1
    sa, sb = _roll_sum(a, m), _roll_sum(b, m)
    saa, sbb, sab = _roll_sum(a * a, m), _roll_sum(b * b, m), _roll_sum(a * b, m)
    cov = sab - sa * sb / m
    va = saa - sa * sa / m
    vb = sbb - sb * sb / m
    with np.errstate(invalid="ignore", divide="ignore"):
        r = cov / np.sqrt(va * vb)
    out[1:] = r  # pair index j ends at bar j+1
    return out


def rolling_var(x: np.ndarray, w: int) -> np.ndarray:
    """Sample variance (ddof 1) of x[i-w+1 .. i] at each i."""
    s, ss = _roll_sum(x, w), _roll_sum(x * x, w)
    return (ss - s * s / w) / (w - 1)


def trailing_mean(x: np.ndarray, w: int) -> np.ndarray:
    return _roll_sum(x, w) / w


def kendall_trend(series: np.ndarray, i: int, w: int) -> float:
    """Kendall's tau between time and series[i-w+1 .. i]; NaN if any value is missing."""
    if i - w + 1 < 0:
        return math.nan
    v = series[i - w + 1 : i + 1]
    if np.isnan(v).any():
        return math.nan
    return float(sps.kendalltau(np.arange(w), v).statistic)


def forward_max_drawdown(logc: np.ndarray, i: int, h: int) -> float:
    """Largest fall from a running peak over bars i .. i+h (the peak may be bar i itself), in
    log units. NaN if the window runs past the data."""
    if i + h >= len(logc):
        return math.nan
    seg = logc[i : i + h + 1]
    return float((np.maximum.accumulate(seg) - seg).max())


def ols_dk(
    y: np.ndarray, x: np.ndarray, groups: Sequence[object], lags: int
) -> tuple[np.ndarray, np.ndarray]:
    """OLS of y on x (x carries its own intercept or dummies) with Driscoll-Kraay standard
    errors: scores x_i e_i summed within each time group, then Newey-West (Bartlett weights,
    `lags` lags) over the groups in sorted order. With one series this is plain Newey-West.
    Returns (coefficients, t-statistics)."""
    xtx_inv = np.linalg.pinv(x.T @ x)
    beta = xtx_inv @ (x.T @ y)
    e = y - x @ beta
    keys = sorted(set(groups))  # type: ignore[type-var]
    pos = {k: n for n, k in enumerate(keys)}
    s = np.zeros((len(keys), x.shape[1]))
    np.add.at(s, [pos[g] for g in groups], x * e[:, None])
    omega = s.T @ s
    for lag in range(1, lags + 1):
        wgt = 1 - lag / (lags + 1)
        g = s[lag:].T @ s[:-lag]
        omega += wgt * (g + g.T)
    v = xtx_inv @ omega @ xtx_inv
    se = np.sqrt(np.clip(np.diag(v), 0, None))
    with np.errstate(divide="ignore", invalid="ignore"):
        t = beta / se
    return beta, t


# --- lunar phase (mean lunation; error against the true phase is at most about a day) ---

SYNODIC = 29.530588853  # mean synodic month, days
NEW_MOON_EPOCH = datetime(2000, 1, 6, 18, 14, tzinfo=UTC)  # a new moon (Meeus)


def moon_dates(start: date, end: date, phase: float) -> list[date]:
    """UTC calendar dates of the mean new moons (phase 0) or full moons (phase 0.5) between
    start and end (inclusive)."""
    t0 = datetime(start.year, start.month, start.day, tzinfo=UTC) - timedelta(days=SYNODIC)
    k = math.floor((t0 - NEW_MOON_EPOCH).total_seconds() / 86400 / SYNODIC)
    out = []
    while True:
        t = NEW_MOON_EPOCH + timedelta(days=(k + phase) * SYNODIC)
        d = t.date()
        if d > end:
            return out
        if d >= start:
            out.append(d)
        k += 1


def moon_period(days: Sequence[date], half: int, shift: int = 0) -> np.ndarray:
    """For each day: +1 if within `half` calendar days of a new moon (shifted by `shift` days)
    and nearer to it than to any full moon, -1 likewise for a full moon, 0 otherwise."""
    if not days:
        return np.zeros(0)
    lo, hi = min(days) - timedelta(days=40), max(days) + timedelta(days=40)
    new = np.array([(d + timedelta(days=shift)).toordinal() for d in moon_dates(lo, hi, 0.0)])
    full = np.array([(d + timedelta(days=shift)).toordinal() for d in moon_dates(lo, hi, 0.5)])
    out = np.zeros(len(days))
    for n, d in enumerate(days):
        o = d.toordinal()
        dn = int(np.abs(new - o).min())
        df = int(np.abs(full - o).min())
        if dn <= half and dn < df:
            out[n] = 1
        elif df <= half and df < dn:
            out[n] = -1
    return out


def welch_t(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """Mean of a minus mean of b, and Welch's t."""
    if len(a) < 2 or len(b) < 2:
        return math.nan, math.nan
    d = float(a.mean() - b.mean())
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return d, d / se if se > 0 else math.nan
