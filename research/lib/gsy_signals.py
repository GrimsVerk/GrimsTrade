"""GSY run-up signals and crash bookkeeping (card: research/cards/gsy-runup.md). Pure numpy, no
harness import, so tests can load it. Every per-bar array is causal: entry `i` uses bars `<= i`.

Bars are given as day ordinals `ords` (strictly increasing) and closes `close` of a
total-return index; windows are in calendar days.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

YEARS2 = 730  # the paper's two years, in calendar days
SMA_DAYS = 290  # ~200 sessions / 10 months
VOL_DAYS = 182  # half a year; compared with the half year before
CRASH = 0.40


def value_at(ords: np.ndarray, close: np.ndarray, when: np.ndarray) -> np.ndarray:
    """Close of the last bar on or before each day in `when` (NaN if none)."""
    j = np.searchsorted(ords, when, side="right") - 1
    out = np.where(j >= 0, close[np.clip(j, 0, None)], np.nan)
    return np.asarray(out, dtype=float)


def ret2(ords: np.ndarray, close: np.ndarray, at: np.ndarray, days: int = YEARS2) -> np.ndarray:
    """Return from the close on or before `at - days` to the close on or before `at`."""
    return value_at(ords, close, at) / value_at(ords, close, at - days) - 1


def runup(
    ords: np.ndarray,
    close: np.ndarray,
    m_ords: np.ndarray,
    m_close: np.ndarray,
    threshold: float,
    days: int = YEARS2,
) -> np.ndarray:
    """True on bar i if the two-year return is >= threshold raw and net of the market."""
    r = ret2(ords, close, ords, days)
    m = ret2(m_ords, m_close, ords, days)
    with np.errstate(invalid="ignore"):
        out = (r >= threshold) & (r - m >= threshold)
    return np.asarray(out & ~np.isnan(r) & ~np.isnan(m), dtype=bool)


def flag_active(ords: np.ndarray, ru: np.ndarray, days: int = YEARS2) -> np.ndarray:
    """True on bar i if a run-up held on any bar within the last `days` calendar days."""
    last = np.maximum.accumulate(np.where(ru, ords, np.iinfo(np.int64).min // 2))
    return np.asarray(last >= ords - days, dtype=bool)


def below_sma(ords: np.ndarray, close: np.ndarray, days: int = SMA_DAYS) -> np.ndarray:
    """True on bar i if its close is below the mean close of bars in (t - days, t]. False until
    a full window exists."""
    cs = np.concatenate([[0.0], np.cumsum(close)])
    j0 = np.searchsorted(ords, ords - days, side="right")
    i1 = np.arange(len(ords)) + 1
    mean = (cs[i1] - cs[j0]) / (i1 - j0)
    full = ords - days >= ords[0]
    return np.asarray(full & (close < mean), dtype=bool)


def vol_rising(
    ords: np.ndarray, close: np.ndarray, days: int = VOL_DAYS, min_obs: int = 20
) -> np.ndarray:
    """True on bar i if the stdev of daily log returns over (t - days, t] is above that over
    (t - 2 days, t - days]. A return belongs to the bar it ends on."""
    lr = np.zeros(len(close))
    lr[1:] = np.log(close[1:] / close[:-1])
    s1 = np.concatenate([[0.0], np.cumsum(lr)])
    s2 = np.concatenate([[0.0], np.cumsum(lr * lr)])

    def std(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        a = np.maximum(a, 1)  # bar 0 has no return
        n = b - a
        safe = np.maximum(n, 1)
        mu = (s1[b] - s1[a]) / safe
        var = (s2[b] - s2[a]) / safe - mu * mu
        return np.sqrt(np.maximum(var, 0.0)), n

    i1 = np.arange(len(ords)) + 1
    mid = np.searchsorted(ords, ords - days, side="right")
    lo = np.searchsorted(ords, ords - 2 * days, side="right")
    recent, n_r = std(mid, i1)
    prior, n_p = std(lo, mid)
    full = (ords - 2 * days >= ords[0]) & (n_r >= min_obs) & (n_p >= min_obs)
    return np.asarray(full & (recent > prior), dtype=bool)


@dataclass(frozen=True)
class Crash:
    peak: int  # ordinal of the peak close
    x: int  # ordinal of the first close at least 40% below it


def crashes(ords: np.ndarray, close: np.ndarray, drop: float = CRASH) -> list[Crash]:
    """Falls of `drop` or more from a running peak. After a crash the peak restarts at the
    crash day's close, so each peak gives at most one crash."""
    out: list[Crash] = []
    peak, pk = -math.inf, -1
    for o, x in zip(ords, close, strict=True):
        if x > peak:
            peak, pk = float(x), int(o)
        elif x <= (1 - drop) * peak:
            out.append(Crash(pk, int(o)))
            peak, pk = float(x), int(o)
    return out


# --- the monthly replication ---


@dataclass(frozen=True)
class Episode:
    month: int  # row index of the first run-up month
    industry: int
    crash: bool  # peak-to-trough fall of 40% within the next 24 months (peak counted from t)
    strict: bool  # a close 40% below month t's level within the next 24 months
    r6: float  # return over the next 6 months
    r24: float


def index_of(rets: np.ndarray) -> np.ndarray:
    """Total-return index from simple returns (months x series); NaN from a missing value on
    until the series is complete again."""
    out = np.full(rets.shape, np.nan)
    for j in range(rets.shape[1]):
        level = math.nan
        for t in range(rets.shape[0]):
            x = rets[t, j]
            prev = 1.0 if math.isnan(level) else level
            level = math.nan if math.isnan(x) else prev * (1 + x)
            out[t, j] = level
    return out


def window_crash(path: np.ndarray, drop: float = CRASH) -> tuple[bool, bool]:
    """(peak-to-trough fall >= drop, fall >= drop below path[0]) along path[0..]."""
    peak = np.maximum.accumulate(path)
    return bool((1 - path / peak).max() >= drop - 1e-12), bool(
        path[1:].min() <= (1 - drop) * path[0]
    )


def episodes(
    idx: np.ndarray, mkt: np.ndarray, threshold: float, first: int, last: int, horizon: int = 24
) -> tuple[list[Episode], int, int, int]:
    """Run-up episodes starting in rows first..last whose next `horizon` months exist.

    Returns (episodes, industry-months considered, of which crash, of which strict crash): the
    last three are the unconditional base rate over the same rows."""
    n_t, n_j = idx.shape
    r = np.full(idx.shape, np.nan)
    r[horizon:] = idx[horizon:] / idx[:-horizon] - 1
    m = np.full(n_t, np.nan)
    m[horizon:] = mkt[horizon:] / mkt[:-horizon] - 1
    with np.errstate(invalid="ignore"):
        ru = (r >= threshold) & ((r - m[:, None]) >= threshold)
    eps: list[Episode] = []
    base = hit = hit_s = 0
    for t in range(first, min(last, n_t - 1 - horizon) + 1):
        for j in range(n_j):
            path = idx[t : t + horizon + 1, j]
            if np.isnan(path).any() or math.isnan(r[t, j]):
                continue
            pp, st = window_crash(path)
            base += 1
            hit += pp
            hit_s += st
            if ru[t, j] and not ru[max(t - horizon, 0) : t, j].any():
                eps.append(Episode(t, j, pp, st, path[6] / path[0] - 1, path[-1] / path[0] - 1))
    return eps, base, hit, hit_s


def share(xs: Sequence[bool]) -> float:
    return sum(xs) / len(xs) if xs else math.nan
