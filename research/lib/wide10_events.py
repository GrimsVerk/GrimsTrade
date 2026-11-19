"""Pure functions for the wide-10 gates (research/wide-10.md)."""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping, Sequence
from datetime import date

import numpy as np

# --- Step 2: W20 Fed purchase operations ---

# Placebo shifts on the trading-day index: 3..27, no multiples of 5, both signs (40).
SHIFTS_W20: list[int] = [s * k for k in range(3, 28) if k % 5 != 0 for s in (1, -1)]


def keep_operation(op: Mapping[str, object]) -> bool:
    """An outright nominal coupon purchase with results (research/wide-10.md step 2)."""
    return (
        op.get("operationDirection") == "P"
        and op.get("auctionStatus") == "Results"
        and "coupon purchase" in str(op.get("operationType", "")).lower()
    )


def maturity(desc: str) -> date | None:
    """The maturity in a NY Fed security description like `T 08.125 05/15/21`."""
    tok = desc.split()[-1] if desc.split() else ""
    parts = tok.split("/")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        return None
    m, d, y = (int(p) for p in parts)
    year = 2000 + y if y < 70 else 1900 + y
    try:
        return date(year, m, d)
    except ValueError:
        return None


def add_years(d: date, n: int) -> date:
    """d plus n calendar years; 29 February becomes 28 February."""
    try:
        return d.replace(year=d.year + n)
    except ValueError:
        return d.replace(year=d.year + n, day=28)


def in_bucket(op_day: date, mat: date, lo_years: float, hi_years: float | None) -> bool:
    """Maturity in [op + lo, op + hi] (hi None = no upper end). Whole years only."""
    if mat < add_years(op_day, int(lo_years)):
        return False
    return hi_years is None or mat <= add_years(op_day, int(hi_years))


def daily_par(
    ops: Iterable[Mapping[str, object]], lo_years: float, hi_years: float | None
) -> dict[date, float]:
    """{operation date: $bn par accepted in the bucket} over kept operations."""
    out: dict[date, float] = {}
    for op in ops:
        if not keep_operation(op):
            continue
        day = date.fromisoformat(str(op["operationDate"]))
        details = op.get("details", [])
        assert isinstance(details, list)
        for sec in details:
            mat = maturity(str(sec.get("securityDescription", "")))
            amt = str(sec.get("parAmountAccepted", "0"))
            if mat is None or not amt.replace(".", "").isdigit():
                continue
            if in_bucket(day, mat, lo_years, hi_years):
                out[day] = out.get(day, 0.0) + float(amt) / 1e9
    return out


def dose_series(days: Sequence[date], par: Mapping[date, float]) -> np.ndarray:
    """x(d) = ln(1 + L(d)) on each trading day (0 where nothing was bought)."""
    return np.array([math.log1p(par.get(d, 0.0)) for d in days])


def shifted(x: np.ndarray, k: int) -> np.ndarray:
    """x_k(i) = x(i - k); NaN where i - k falls outside the series."""
    out = np.full(len(x), np.nan)
    if k >= 0:
        out[k:] = x[: len(x) - k] if k else x
    else:
        out[:k] = x[-k:]
    return out


def ols_hc1(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """(slope, White HC1 t) of y = a + b x, NaN pairs dropped."""
    ok = ~(np.isnan(x) | np.isnan(y))
    xa, ya = x[ok], y[ok]
    n = len(xa)
    if n < 3:
        return math.nan, math.nan
    dx = xa - xa.mean()
    sxx = float(dx @ dx)
    if sxx == 0:
        return math.nan, math.nan
    b = float(dx @ (ya - ya.mean())) / sxx
    a = ya.mean() - b * xa.mean()
    e = ya - a - b * xa
    var = float((dx**2) @ (e**2)) / sxx**2 * n / (n - 2)
    return b, b / math.sqrt(var) if var > 0 else math.nan


def rank_highest(true: float, others: Sequence[float]) -> int:
    """1 + the number of others strictly above `true` (1 = the highest)."""
    return 1 + sum(o > true for o in others)


def null_spread(ts: Sequence[float]) -> tuple[float, float]:
    """(standard deviation, share with |t| >= 2) of placebo t values."""
    a = np.asarray(ts, dtype=float)
    return float(a.std(ddof=1)), float(np.mean(np.abs(a) >= 2))
