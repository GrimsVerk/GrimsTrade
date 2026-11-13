"""Signed-weight simulator with perpetual funding (research run short-1, card in
research/short-1.md). Kept free of `harness` so tests can import it.

Weights are fractions of equity; negative = short. Return day `t` runs from the close of
`t - 1` to the close of `t`. `fund[t, j]` is the sum of the funding rates of the events in that
interval: a position with weight `w` earns `-w x fund[t, j]` (positive rate: longs pay shorts).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from breadth_xs import ffill


@dataclass
class Run:
    r: np.ndarray  # daily account returns, from first_day + 1
    funding: np.ndarray  # funding part of each day's return (positive = received)
    gross: np.ndarray  # gross exposure at each day's close


def simulate(
    px: np.ndarray,
    fund: np.ndarray | None,
    targets: np.ndarray,
    base: np.ndarray,
    cost: float,
    first_day: int,
) -> Run:
    """Targets are set at the close of each `base` day and drift with prices until the next.
    `cost` per side on every unit of weight change, long or short. Missing price: no return.
    If equity reaches 0 the account stays dead (return -100% on that day, 0 after)."""
    n_days, n = px.shape
    filled = ffill(px)
    r = np.zeros_like(filled)
    with np.errstate(invalid="ignore", divide="ignore"):
        r[1:] = filled[1:] / filled[:-1] - 1
    r[~np.isfinite(r)] = 0.0
    f = np.zeros_like(r) if fund is None else np.nan_to_num(fund)
    out = np.zeros(n_days)
    fout = np.zeros(n_days)
    gross = np.zeros(n_days)
    w = np.zeros(n)
    dead = False
    reset = {int(b): k for k, b in enumerate(base)}
    for t in range(first_day, n_days):
        if dead:
            continue
        if t > first_day:
            price_pnl = float((w * r[t]).sum())
            fund_pnl = float(-(w * f[t]).sum())
            out[t] = price_pnl + fund_pnl
            fout[t] = fund_pnl
            tot = 1 + out[t]
            if tot <= 0:
                out[t], dead, w = -1.0, True, w * 0
                continue
            w = w * (1 + r[t]) / tot
        k = reset.get(t)
        if k is not None:
            new = targets[k]
            c = float(np.abs(new - w).sum() * cost)
            out[t] = (1 + out[t]) * (1 - c) - 1
            w = new.copy()
        gross[t] = float(np.abs(w).sum())
    # the first entry's cost is booked on first_day, which is not returned: carry it forward
    if first_day + 1 < n_days:
        out[first_day + 1] = (1 + out[first_day]) * (1 + out[first_day + 1]) - 1
    s = slice(first_day + 1, n_days)
    return Run(out[s], fout[s], gross[s])


def long_short(sig: np.ndarray, m: np.ndarray, frac: float = 1 / 3) -> np.ndarray:
    """+0.5 spread over the top `frac` of `m` by signal, -0.5 over the bottom `frac`."""
    w = np.zeros(len(m))
    idx = np.flatnonzero(m)
    k = max(1, int(round(len(idx) * frac)))
    if len(idx) < 2 * k:
        return w
    order = idx[np.argsort(-sig[idx], kind="mergesort")]
    w[order[:k]] = 0.5 / k
    w[order[-k:]] = -0.5 / k
    return w


def rank01(x: np.ndarray, m: np.ndarray) -> np.ndarray:
    """Cross-sectional rank in [0, 1] among the finite values inside `m` (NaN elsewhere)."""
    out = np.full(len(x), np.nan)
    idx = np.flatnonzero(m & np.isfinite(x))
    if len(idx) == 1:
        out[idx] = 0.5
    elif len(idx) > 1:
        order = np.argsort(np.argsort(x[idx], kind="mergesort"), kind="mergesort")
        out[idx] = order / (len(idx) - 1)
    return out


def spells(neg: np.ndarray, gap: int = 30, min_len: int = 30) -> int:
    """Runs of True, gaps shorter than `gap` merged, runs shorter than `min_len` dropped."""
    runs: list[list[int]] = []
    for i in np.flatnonzero(neg):
        if runs and i - runs[-1][1] <= gap:
            runs[-1][1] = int(i)
        else:
            runs.append([int(i), int(i)])
    return sum(1 for a, b in runs if b - a + 1 >= min_len)


def dd_spells(r: np.ndarray, depth: float = 0.10) -> int:
    """Drawdown spells deeper than `depth` (each counted once, from a new high to the next)."""
    eq = np.cumprod(1 + r)
    peak = np.maximum.accumulate(eq)
    n, inside, worst = 0, False, 0.0
    for e, p in zip(eq, peak, strict=True):
        if e >= p:
            if inside and worst >= depth:
                n += 1
            inside, worst = False, 0.0
        else:
            inside, worst = True, max(worst, 1 - e / p)
    return n + int(inside and worst >= depth)
