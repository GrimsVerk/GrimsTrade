"""The planted input of run rl-3 (research/rl-3.md, "What is planted"). numpy only.

`peek` for asset j on Friday i is a noisy copy of the risk-adjusted return the asset earns over
the week the Friday decision holds (first open after Friday i to the first open after Friday
i + 1). In every calendar year of a book its correlation with that return is exactly `rho`.
This is a control: the input knows the future on purpose. It is never a strategy.
"""

from __future__ import annotations

import dataclasses
import math
from datetime import date

import ml
import numpy as np
from rl2_env import RTable
from rl_env import Table

SEEDS = {"six": 301, "gspc": 302}  # one fixed noise draw per book, the same for every rho


def _next_open(opens: np.ndarray) -> np.ndarray:
    """nxt[k, j] = the first grid day > k with an open for asset j (len(opens) if none)."""
    k_n = len(opens)
    nxt = np.full(opens.shape, k_n, dtype=np.int64)
    cur = np.full(opens.shape[1], k_n, dtype=np.int64)
    for k in range(k_n - 1, -1, -1):
        nxt[k] = cur
        cur = np.where(np.isfinite(opens[k]), k, cur)
    return nxt


def week_z(t: Table) -> np.ndarray:
    """[F, n] log return held by Friday i's decision / (EWMA vol x sqrt(7/365)), clipped to +-5;
    NaN where the asset is not eligible or the week has no closing open inside the book."""
    op = t.book.opens
    nxt = _next_open(op)
    k_n, n = op.shape
    z = np.full(t.elig.shape, np.nan)
    cols = np.arange(n)
    for i, k in enumerate(t.kf):
        if k + 7 >= k_n:
            continue
        a, b = nxt[k], nxt[k + 7]
        ok = t.elig[i] & (b < k_n) & (a < b)
        if not ok.any():
            continue
        r = np.log(op[np.minimum(b, k_n - 1), cols] / op[np.minimum(a, k_n - 1), cols])
        vol = np.exp(t.X[i, :, ml.LOG_VOL])
        z[i] = np.where(ok, np.clip(r / (vol * math.sqrt(7 / 365)), -5, 5), np.nan)
    return z


def peek(t: Table, rho: float, seed: int) -> np.ndarray:
    """[F, n] the planted input: corr(peek, z) = rho exactly within each calendar year's cells."""
    z = week_z(t)
    eps = np.random.default_rng(seed).standard_normal(z.shape)
    out = np.zeros(z.shape)
    years = np.array([d.year for d in t.fridays])
    for y in np.unique(years):
        cell = (years == y)[:, None] & np.isfinite(z)
        if cell.sum() < 3:
            continue
        zy = z[cell] - z[cell].mean()
        if zy.std() == 0:
            continue
        zy /= zy.std()
        e = eps[cell] - eps[cell].mean()
        e -= (e @ zy) / (zy @ zy) * zy
        e /= e.std()
        out[cell] = rho * zy + math.sqrt(1 - rho * rho) * e
    return out


def plant(rt: RTable, rho: float, seed: int) -> RTable:
    """The table with `peek` appended as the last asset input."""
    t = rt.t
    x = np.concatenate([t.X, peek(t, rho, seed)[..., None]], axis=2)
    return dataclasses.replace(rt, t=dataclasses.replace(t, X=x))


def realised_ic(t: Table, col: np.ndarray, start: date | None = None) -> float:
    """Pooled correlation of an input with the coming week's z over the eligible cells."""
    z = week_z(t)
    keep = np.isfinite(z)
    if start is not None:
        keep &= (np.array([d >= start for d in t.fridays]))[:, None]
    return float(np.corrcoef(col[keep], z[keep])[0, 1])
