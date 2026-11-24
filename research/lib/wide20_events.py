"""Lane wide-20, gate W29 `air-disaster-mood` (research/cards/wide-20.md): pure functions.

Parse the Wikidata aviation-accident list, build the event dose on a bar calendar, move the
event calendar for the placebos, and fit OLS with HC1 standard errors. No function here reads a
price or the network; the tests feed small literal samples.
"""

from __future__ import annotations

import csv
import io
import math
from collections.abc import Sequence
from datetime import date, timedelta

import numpy as np

MIN_DEATHS = 50
STEP_DAYS = 23  # placebo step: not a multiple of a week
SHIFTS = [k for k in range(-20, 21) if k != 0]  # 40 placebos

QUERY = """SELECT ?item ?date ?precision ?deaths WHERE {
  ?item wdt:P31/wdt:P279* wd:Q744913 .
  ?item wdt:P1120 ?deaths .
  ?item p:P585/psv:P585 ?tv .
  ?tv wikibase:timeValue ?date .
  ?tv wikibase:timePrecision ?precision .
  FILTER(?deaths >= 50)
}"""

Event = tuple[date, float]  # (accident day, deaths)


def parse_events(text: str, min_deaths: float = MIN_DEATHS) -> list[Event]:
    """One event per item: earliest day-precision date, largest death count (card, Data)."""
    best: dict[str, tuple[date, float]] = {}
    for r in csv.DictReader(io.StringIO(text)):
        try:
            prec = int(float(r.get("precision") or "0"))
            deaths = float(r.get("deaths") or "nan")
            raw = (r.get("date") or "").lstrip("+")
            day = date.fromisoformat(raw[:10])
        except ValueError:
            continue
        if prec != 11 or not math.isfinite(deaths):
            continue
        item = r.get("item") or ""
        if item in best:
            d0, n0 = best[item]
            best[item] = (min(d0, day), max(n0, deaths))
        else:
            best[item] = (day, deaths)
    return sorted(v for v in best.values() if v[1] >= min_deaths)


def in_window(events: Sequence[Event], lo: date, hi: date) -> list[Event]:
    """Events with lo <= E <= hi - 2 days (day 1 then falls on or before hi for ETFs)."""
    return [e for e in events if lo <= e[0] <= hi - timedelta(days=2)]


def span(lo: date, hi: date) -> int:
    """L of the card: days from lo to hi - 1 day (the wrap length of a shifted calendar)."""
    return (hi - timedelta(days=1) - lo).days


def shift(events: Sequence[Event], k: int, lo: date, hi: date) -> list[Event]:
    """E_k = lo + ((E - lo + 23k) mod L): every event moved 23k days, wrapped in the window."""
    n = span(lo, hi)
    return sorted((lo + timedelta(days=((e - lo).days + STEP_DAYS * k) % n), d) for e, d in events)


def weight(deaths: float, binary: bool = False) -> float:
    return 1.0 if binary else math.log2(deaths / 25.0)


def dose(
    bars: Sequence[date],
    events: Sequence[Event],
    days: Sequence[int] = (0, 1),
    binary: bool = False,
) -> np.ndarray:
    """x on the bar calendar: each event adds its weight on the bars `days` after its day 0
    (day 0 = the first bar dated >= the accident day). Bars must be sorted."""
    x = np.zeros(len(bars))
    for e, d in events:
        lo, hi = 0, len(bars)
        while lo < hi:  # first index with bars[i] >= e
            mid = (lo + hi) // 2
            if bars[mid] < e:
                lo = mid + 1
            else:
                hi = mid
        for j in days:
            if lo + j < len(bars):
                x[lo + j] += weight(d, binary)
    return x


def ols_hc1(x: np.ndarray, y: np.ndarray) -> tuple[float, float, int]:
    """(b, t, n) of y = a + b x with HC1 standard errors."""
    n = len(y)
    X = np.column_stack([np.ones(n), x])
    xtx_inv = np.linalg.inv(X.T @ X)
    beta = xtx_inv @ X.T @ y
    u = y - X @ beta
    meat = (X * (u**2)[:, None]).T @ X
    cov = xtx_inv @ meat @ xtx_inv * n / (n - 2)
    return float(beta[1]), float(beta[1] / math.sqrt(cov[1, 1])), n


def rank_lowest(t: float, placebo: Sequence[float]) -> int:
    """1 + number of placebos with t at or below the true t (ties count against it)."""
    return 1 + sum(1 for p in placebo if p <= t)


def null_spread(placebo: Sequence[float]) -> tuple[float, float, float, float, float]:
    """(sd, share |t| >= 2, q5, median, q95)."""
    a = np.asarray(placebo, dtype=float)
    q5, q50, q95 = (float(v) for v in np.quantile(a, [0.05, 0.5, 0.95]))
    return float(a.std(ddof=1)), float(np.mean(np.abs(a) >= 2)), q5, q50, q95
