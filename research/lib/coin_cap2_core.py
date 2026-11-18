"""coin-cap-2 core: coin falls grouped into independent episodes, and the per-fall measures
(card: research/cards/coin-cap.md, "Third reading"). Pure numpy, no harness import, so the
tests can load it alone. Rows are calendar days, as in `cointop1_core`."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

PRE_TOP = 91  # the window of a fall starts this many days before the top
MAX_AFTER_LOW = 365  # and ends at the settled day, at most this many days after the low
MARKET_LEAD = 60  # a coin top up to this many days before a market top belongs to that fall
OWN_GAP = 30  # coin-own tops further apart than this start a new episode


@dataclass(frozen=True)
class Fall:
    coin: int
    top: int
    low: int
    settled: int  # -1 if the low is not settled by the end of the data


def window(f: Fall, n_days: int) -> tuple[int, int]:
    """First and last row of a fall's window: the P&L path starts at 0 at the first row and
    takes the returns earned on the rows after it, up to and including the last."""
    end = f.settled if f.settled >= 0 else n_days - 1
    return max(f.top - PRE_TOP, 0), min(end, f.low + MAX_AFTER_LOW, n_days - 1)


def deepest_fall(r: np.ndarray) -> float:
    """Largest peak-to-trough drop of the running sum of `r`, starting from 0 (both ends inside)."""
    path = np.concatenate([[0.0], np.cumsum(r)])
    return float((np.maximum.accumulate(path) - path).max())


def market_index(ret: np.ndarray, member: np.ndarray) -> np.ndarray:
    """Equal-weight index: each day the mean simple return of the member coins (0 if none),
    compounded. `ret` and `member` are `[days, coins]`."""
    n = member.sum(1)
    s = np.where(member, ret, 0.0).sum(1)
    m = np.where(n > 0, s / np.maximum(n, 1), 0.0)
    return np.cumprod(1 + m)


def episodes(
    falls: Sequence[Fall], market: Sequence[tuple[int, int]]
) -> tuple[list[str], list[str]]:
    """Episode key per fall, and the keys in time order. `market` holds (top row, low row) of each
    market fall. A coin fall whose top is from `MARKET_LEAD` days before a market top up to that
    market fall's low is in that market fall's episode (the first such, if two qualify). The
    rest, sorted by top, start a new episode whenever the gap to the previous one exceeds
    `OWN_GAP` days."""
    keys = [""] * len(falls)
    own: list[int] = []
    for i, f in enumerate(falls):
        for k, (mt, ml) in enumerate(market):
            if mt - MARKET_LEAD <= f.top <= ml:
                keys[i] = f"market-{k}"
                break
        else:
            own.append(i)
    own.sort(key=lambda i: falls[i].top)
    run, prev = -1, -(10**9)
    for i in own:
        if falls[i].top - prev > OWN_GAP:
            run += 1
        prev = falls[i].top
        keys[i] = f"own-{run}"
    first: dict[str, int] = {}
    for k, f in zip(keys, falls, strict=True):
        first[k] = min(first.get(k, f.top), f.top)
    return keys, sorted(first, key=lambda k: first[k])


def effective_number(keys: Sequence[str]) -> float:
    """1 / sum of squared shares of the falls per key."""
    if not keys:
        return float("nan")
    _, counts = np.unique(np.asarray(keys), return_counts=True)
    s = counts / counts.sum()
    return float(1 / (s**2).sum())


def sign_p(k: int, n: int) -> float:
    """One-sided sign test: chance of at least `k` positives in `n` fair coin flips."""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2**n if n else float("nan")


def boot_mean(x: np.ndarray, draws: int = 2000, seed: int = 0) -> tuple[float, float, float]:
    """Plain bootstrap of the mean over the items of `x`: (one-sided p of mean <= 0, 5%, 95%)."""
    if len(x) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    m = x[rng.integers(0, len(x), (draws, len(x)))].mean(1)
    return float((m <= 0).mean()), float(np.quantile(m, 0.05)), float(np.quantile(m, 0.95))
