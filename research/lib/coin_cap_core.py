"""coin-cap core: the cap itself and the walk-forward pick (card: research/cards/coin-cap.md).
Pure functions, no harness import, so tests can load them without side effects."""

from __future__ import annotations

import math
from collections.abc import Collection, Mapping, Sequence
from datetime import date

import numpy as np


def cap_coins(
    w: Mapping[str, float], coins: Collection[str], cap: float, mode: str
) -> dict[str, float]:
    """Scale the coin weights so they sum to at most `cap`. The excess goes to cash (`cash`) or
    to the held non-coin weights pro rata (`rest`; cash if none is held). Uses `w` only."""
    if mode not in ("cash", "rest"):
        raise ValueError(mode)
    held = sum(x for s, x in w.items() if s in coins)
    if held <= cap:
        return dict(w)
    k = cap / held
    rest = sum(x for s, x in w.items() if s not in coins)
    g = 1 + (held - cap) / rest if mode == "rest" and rest > 0 else 1.0
    return {s: x * k if s in coins else x * g for s, x in w.items()}


def score(r: np.ndarray) -> float:
    """Annualised log growth over the worst loss (365-day year)."""
    if len(r) < 2:
        return -math.inf
    eq = np.concatenate([[1.0], np.cumprod(1 + r)])
    dd = float((1 - eq / np.maximum.accumulate(eq)).max())
    return float(np.log1p(r).mean() * 365) / dd if dd > 0 else -math.inf


def walk_forward(
    ords: np.ndarray,
    rets: Mapping[str, np.ndarray],
    order: Sequence[str],
    years: Sequence[int],
    default: str,
) -> tuple[dict[int, str], np.ndarray]:
    """For each year, the name with the best `score` on returns dated before that year (ties:
    earliest in `order`), and the stitched series. `ords[i]` is the day return i is earned on.
    Days outside `years` carry `default`."""
    out = rets[default].copy()
    picks: dict[int, str] = {}
    for y in years:
        cut = date(y, 1, 1).toordinal()
        before = ords < cut
        best = default
        if before.sum() >= 2:
            best = max(order, key=lambda n: (score(rets[n][before]), -order.index(n)))
        picks[y] = best
        m = (ords >= cut) & (ords < date(y + 1, 1, 1).toordinal())
        out[m] = rets[best][m]
    return picks, out
