"""Pure parts of halving-2 (card `research/halving-2.md`): calendars, the frozen window, placebo
calendars, bars from Coin Metrics rows, and the BTC-relative statistic C2.

No harness import (it changes global state), so the tests can load this module directly.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

from grimstrade.data import Bar

TRAIN_LAST_BAR = date(2025, 11, 10)  # the train cut (harness.TRAIN_LAST_BAR)
WIN_LO, WIN_HI = 548, 913  # `macro.halving_bear`: 548 <= days since the last halving < 913
SEED = 20261124
N_PLACEBO = 40
MIN_SHIFT = 365  # a placebo window never shares a day with a true one

# UTC day of each reward cut, from on-chain issuance per block (card table). Train dates only.
CALENDARS: dict[str, tuple[date, ...]] = {
    "BTC": (date(2012, 11, 28), date(2016, 7, 9), date(2020, 5, 11), date(2024, 4, 19)),
    "LTC": (date(2015, 8, 25), date(2019, 8, 5), date(2023, 8, 2)),
    "ZEC": (date(2020, 11, 18), date(2024, 11, 23)),
    "BCH": (date(2020, 4, 8), date(2024, 4, 3)),
    "BSV": (date(2020, 4, 9), date(2024, 4, 13)),
    "ETC": (date(2017, 12, 11), date(2020, 3, 17), date(2022, 4, 25), date(2024, 5, 31)),
}
CM_ASSET = {s: s.lower() for s in CALENDARS}


def days_since(cal: Sequence[date], d: date) -> float:
    """Days since the last cut strictly before d (NaN before the first): `macro.days_since_halving`
    with any calendar."""
    past = [h for h in cal if h < d]
    return float((d - past[-1]).days) if past else math.nan


def in_window(cal: Sequence[date], d: date) -> bool:
    """The frozen window of `halving-alone` (NaN compares false: held before a first cut)."""
    return WIN_LO <= days_since(cal, d) < WIN_HI


def spacings(cal: Sequence[date]) -> list[int]:
    return [(b - a).days for a, b in zip(cal, cal[1:], strict=False)]


def shift_bounds(cal: Sequence[date]) -> tuple[int, int]:
    """Shifts |s| in [365, P_min - 365]: the placebo window [548 + s, 913 + s) then misses every
    true window, the coin's own and the neighbouring cycles'."""
    return MIN_SHIFT, min(spacings(cal)) - MIN_SHIFT


def placebo_calendar(cal: Sequence[date], s: int) -> tuple[date, ...]:
    """The whole calendar moved by s days, extended by one implied cut before the first and one
    after the last at the mean spacing (so every placebo has windows across the sample)."""
    p = round(float(np.mean(spacings(cal))))
    ext = [cal[0] - timedelta(days=p), *cal, cal[-1] + timedelta(days=p)]
    return tuple(d + timedelta(days=s) for d in ext)


def draw_shifts(coins: Sequence[str], n: int = N_PLACEBO, seed: int = SEED) -> list[dict[str, int]]:
    """n placebos; in each, every coin gets its own shift (uniform integer in its bounds, random
    sign). Deterministic: one generator, coins drawn in the order given."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        row = {}
        for c in coins:
            lo, hi = shift_bounds(CALENDARS[c])
            mag = int(rng.integers(lo, hi + 1))
            row[c] = mag if rng.random() < 0.5 else -mag
        out.append(row)
    return out


# --- data ---


def prices_from_rows(
    rows: Sequence[Mapping[str, Any]], last: date = TRAIN_LAST_BAR
) -> dict[date, float]:
    """Daily PriceUSD by date, rows dated after `last` dropped (the train cut)."""
    out: dict[date, float] = {}
    for r in rows:
        d = date.fromisoformat(str(r["time"])[:10])
        v = r.get("PriceUSD")
        if d > last or v in (None, ""):
            continue
        out[d] = float(v)
    if out and max(out) > last:
        raise AssertionError("a bar after the train cut")
    return out


def volumes_from_rows(
    rows: Sequence[Mapping[str, Any]], last: date = TRAIN_LAST_BAR
) -> dict[date, float]:
    out: dict[date, float] = {}
    for r in rows:
        d = date.fromisoformat(str(r["time"])[:10])
        v = r.get("volume_reported_spot_usd_1d")
        if d <= last and v not in (None, ""):
            out[d] = float(v)
    return out


def bars(px: Mapping[date, float], vol: Mapping[date, float] | None = None) -> list[Bar]:
    """Daily bars: close = the day's price, open = the previous day's close (coins trade around
    the clock), high/low = max/min of the two. Requires consecutive days."""
    ds = sorted(px)
    if any((b - a).days != 1 for a, b in zip(ds, ds[1:], strict=False)):
        raise ValueError("price series has gaps")
    out = []
    prev = px[ds[0]]
    for d in ds:
        c = px[d]
        v = (vol or {}).get(d, 0.0)
        out.append(Bar(d, prev, max(prev, c), min(prev, c), c, v))
        prev = c
    return out


def load_rows(root: Path, coin: str) -> list[dict[str, Any]]:
    """Coin Metrics community rows from the shared cache (snapshot 2026-11-13)."""
    path = (
        root / "coinmetrics" / "full" / "2026-11-13" / "assets" / CM_ASSET[coin] / "page-000.json"
    )
    rows: list[dict[str, Any]] = json.loads(path.read_text())["data"]
    return rows


# --- C2: own timing net of BTC ---


def relative_gap(
    alts: Mapping[str, Mapping[date, float]],
    btc: Mapping[date, float],
    cals: Mapping[str, Sequence[date]],
    starts: Mapping[str, date],
    end: date,
) -> tuple[float, int, int]:
    """Mean daily log return of each coin priced in BTC on days inside its window minus days
    outside, pooled over coins. Day d's return is from close d-1 to close d, classified by
    `in_window(cal, d)`. Returns (gap, days inside, days outside)."""
    inside: list[float] = []
    outside: list[float] = []
    for c, px in alts.items():
        d = starts[c]
        while d <= end:
            p = d - timedelta(days=1)
            if all(x in px and x in btc for x in (d, p)):
                r = math.log(px[d] / btc[d]) - math.log(px[p] / btc[p])
                (inside if in_window(cals[c], d) else outside).append(r)
            d += timedelta(days=1)
    if not inside or not outside:
        return math.nan, len(inside), len(outside)
    return float(np.mean(inside) - np.mean(outside)), len(inside), len(outside)


def rank_high(true: float, placebos: Sequence[float]) -> int:
    """1 + the number of placebos at least as high as the true value (1 = best)."""
    return 1 + sum(p >= true for p in placebos)


def rank_low(true: float, placebos: Sequence[float]) -> int:
    return 1 + sum(p <= true for p in placebos)


def null_summary(xs: Sequence[float]) -> str:
    a = np.asarray(xs, dtype=float)
    q5, q50, q95 = np.quantile(a, [0.05, 0.5, 0.95])
    return (
        f"SD {a.std(ddof=1):.3f}; 5/50/95% {q5:+.3f} / {q50:+.3f} / {q95:+.3f}; "
        f"min {a.min():+.3f}, max {a.max():+.3f}"
    )
