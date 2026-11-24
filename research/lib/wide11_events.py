"""Pure functions for the wide-11 gate W22 `hedging-pressure` (research/wide-11.md step 2)."""

from __future__ import annotations

import bisect
import csv
import io
import math
import zipfile
from collections.abc import Iterable, Mapping, Sequence
from datetime import date, timedelta
from pathlib import Path

import numpy as np

# Placebo shifts in weeks: odd 27..103 in steps of 4, both signs (40).
SHIFTS_W22: list[int] = [s * k for k in range(27, 104, 4) for s in (1, -1)]

# Report dates whose release a government shutdown delayed (info-1's windows).
COT_DROP: tuple[tuple[date, date], ...] = (
    (date(2013, 10, 1), date(2013, 10, 29)),
    (date(2018, 12, 21), date(2019, 3, 5)),
    (date(2025, 9, 30), date(9999, 1, 1)),
)
GATE_CODES = {"GLD": "088691", "TLT": "020601", "SPY": "13874A", "QQQ": "209742"}
SHOWN_CODES = {"IEF": "043602", "SLV": "084691", "BTC": "133741"}
Z_WINDOW_DAYS = 1092  # 156 weeks
Z_MIN = 104


def report_date(s: str) -> date:
    """`As of Date in Form YYMMDD` -> date (yy < 50 means 20yy)."""
    s = s.strip()
    yy = int(s[:2])
    return date(2000 + yy if yy < 50 else 1900 + yy, int(s[2:4]), int(s[4:6]))


def dropped(d: date) -> bool:
    return any(lo <= d <= hi for lo, hi in COT_DROP)


def hedging_pressure(long_: float, short: float) -> float:
    """HP = (short - long) / (short + long); NaN if no commercial positions."""
    tot = long_ + short
    return (short - long_) / tot if tot > 0 else math.nan


def parse_rows(
    rows: Iterable[Mapping[str, str]], codes: Mapping[str, str], last: date
) -> dict[str, dict[date, float]]:
    """Legacy COT rows -> {asset: {report date: HP}}; later rows win; shutdown and late
    report dates (> `last`) skipped."""
    code_to = {c: a for a, c in codes.items()}
    out: dict[str, dict[date, float]] = {a: {} for a in codes}
    for raw in rows:
        row = {k.strip(): v for k, v in raw.items() if k}
        a = code_to.get(row.get("CFTC Contract Market Code", "").strip())
        if a is None:
            continue
        d = report_date(row["As of Date in Form YYMMDD"])
        if d > last or dropped(d):
            continue
        cl = float(row["Commercial Positions-Long (All)"].replace(",", "") or 0)
        cs = float(row["Commercial Positions-Short (All)"].replace(",", "") or 0)
        out[a][d] = hedging_pressure(cl, cs)
    return out


def read_zips(
    paths: Sequence[Path], codes: Mapping[str, str], last: date
) -> dict[str, dict[date, float]]:
    """Read the yearly legacy zip files in order (later files win on duplicate dates)."""
    out: dict[str, dict[date, float]] = {a: {} for a in codes}
    for zp in paths:
        with zipfile.ZipFile(zp) as z:
            for name in z.namelist():
                rd = csv.DictReader(io.TextIOWrapper(z.open(name), "latin-1"))
                for a, m in parse_rows(rd, codes, last).items():
                    out[a].update(m)
    return out


def zscores(hp: Mapping[date, float]) -> dict[date, float]:
    """z(T) = (HP(T) - mean) / sd over reports dated T-1092 .. T-1 days, >= 104 of them."""
    ds = sorted(d for d, v in hp.items() if not math.isnan(v))
    vals = np.array([hp[d] for d in ds])
    out: dict[date, float] = {}
    for i, d in enumerate(ds):
        lo = bisect.bisect_left(ds, d - timedelta(days=Z_WINDOW_DAYS))
        w = vals[lo:i]
        if len(w) < Z_MIN:
            continue
        sd = float(w.std(ddof=1))
        if sd > 0:
            out[d] = (vals[i] - float(w.mean())) / sd
    return out


def shifted_z(z: Mapping[date, float], t: date, k: int) -> float:
    """z_k(T) = z(T - 7k days); NaN if missing."""
    return z.get(t - timedelta(days=7 * k), math.nan)


class Closes:
    """Daily closes of one asset with first-on-or-after / last-on-or-before lookups."""

    def __init__(self, bars: Mapping[date, float]):
        self.days = sorted(bars)
        self.c = bars

    def first_on_or_after(self, d: date) -> date | None:
        i = bisect.bisect_left(self.days, d)
        return self.days[i] if i < len(self.days) else None

    def last_on_or_before(self, d: date) -> date | None:
        i = bisect.bisect_right(self.days, d)
        return self.days[i - 1] if i > 0 else None


def outcome(px: Closes, t: date, hold_days: int, last: date) -> float:
    """ln(exit / entry): entry = close of the first bar dated >= T + 7 (a day after the latest
    regular release), exit = close of the first bar dated >= T + hold_days (35 for the 4-week
    gate, 14 for the 1-week cell). NaN if a bar is missing, the exit bar is dated after
    T + hold_days + 7 days or after `last`."""
    a = px.first_on_or_after(t + timedelta(days=7))
    b = px.first_on_or_after(t + timedelta(days=hold_days))
    if a is None or b is None or b > last or b > t + timedelta(days=hold_days + 7) or b <= a:
        return math.nan
    return math.log(px.c[b] / px.c[a])


def past_return(px: Closes, t: date, back_days: int) -> float:
    """ln(close of last bar <= T / close of last bar <= T - back_days)."""
    a = px.last_on_or_before(t - timedelta(days=back_days))
    b = px.last_on_or_before(t)
    if a is None or b is None or a == b:
        return math.nan
    return math.log(px.c[b] / px.c[a])


def ols_dk(
    cols: Sequence[np.ndarray], y: np.ndarray, week: np.ndarray, lags: int
) -> tuple[np.ndarray, np.ndarray, int]:
    """(coefficients, Driscoll-Kraay t, rows) of y on cols (no constant added; pass the
    intercept dummies yourself). Scores are summed within each `week` (integer index), then
    Newey-West with Bartlett weights over week distance up to `lags`. NaN rows dropped."""
    x = np.column_stack(cols)
    ok = ~(np.isnan(x).any(axis=1) | np.isnan(y))
    x, ya, wk = x[ok], y[ok], week[ok]
    keep = x.any(axis=0)  # drop all-zero dummy columns (a market without rows)
    n = len(ya)
    xk = x[:, keep]
    inv = np.linalg.inv(xk.T @ xk)
    beta_k = inv @ xk.T @ ya
    e = ya - xk @ beta_k
    weeks = np.unique(wk)
    idx = {w: i for i, w in enumerate(weeks)}
    s = np.zeros((len(weeks), xk.shape[1]))
    for r in range(n):
        s[idx[wk[r]]] += xk[r] * e[r]
    meat = s.T @ s
    for lag in range(1, lags + 1):
        wgt = 1 - lag / (lags + 1)
        pos = {w: i for i, w in enumerate(weeks)}
        g = np.zeros_like(meat)
        for i, w in enumerate(weeks):
            j = pos.get(w - lag)
            if j is not None:
                g += np.outer(s[i], s[j])
        meat += wgt * (g + g.T)
    cov = inv @ meat @ inv
    beta = np.full(x.shape[1], np.nan)
    t = np.full(x.shape[1], np.nan)
    beta[keep] = beta_k
    t[keep] = beta_k / np.sqrt(np.diag(cov))
    return beta, t, n


def rank_highest(true: float, others: Sequence[float]) -> int:
    """1 + the number of others strictly above `true` (1 = the highest)."""
    return 1 + sum(o > true for o in others)


def null_spread(ts: Sequence[float]) -> tuple[float, float]:
    """(standard deviation, share with |t| >= 2) of placebo t values."""
    a = np.asarray(ts, dtype=float)
    return float(a.std(ddof=1)), float(np.mean(np.abs(a) >= 2))
