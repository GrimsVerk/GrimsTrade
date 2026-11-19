"""deep-1, Part B: the three combination rules as pure functions of past sleeve returns.

Nothing here reads prices or runs a backtest; `deep1_combo.py` does that. Card: research/deep-1.md.

Conventions. `R` is days x sleeves: `R[j, m]` is sleeve m's return on calendar day j + 1 of the
run (NaN before the sleeve's first day). A decision on day k may use `R[: k - 1]` only: the
return of day k itself includes the crypto close at midnight, after the 22:30 decision. Weekly
returns are 7-day blocks from one Friday decision to the next; at a refit on Friday k the newest
block is `R[k - 14 : k - 7]` (the week still running is left out). Column `t` is `tsmom12`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

import numpy as np

MIN_WEEKS = 104  # weekly returns a sleeve needs before it can be chosen
MIN_LOSING = 26  # losing weeks of tsmom12 needed to measure a correlation in losses
VAR_WEEKS = 156  # window of the inverse-variance shares
LAMBDAS = (0.1, 1.0, 10.0)
FOLDS = 5
OFF, MIXED, ON = 0, 1, 2


def first_friday(year: int) -> date:
    d = date(year, 1, 1)
    return d + timedelta(days=(4 - d.weekday()) % 7)


def refit_days(days: np.ndarray) -> list[int]:
    """Decision indices that fall on the first Friday of a calendar year."""
    out = []
    for k, o in enumerate(days[:-1]):
        d = date.fromordinal(int(o))
        if d == first_friday(d.year):
            out.append(k)
    return out


def blocks(r: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    """Weekly returns usable at a refit on decision index k, oldest first, and the decision
    index each week starts on. `r` is days (x sleeves)."""
    n = k // 7 - 1
    if n <= 0:
        return np.empty((0, *r.shape[1:])), np.empty(0, dtype=np.int64)
    starts = k - 7 * np.arange(n + 1, 1, -1)
    out = np.stack([np.prod(1 + r[s : s + 7], axis=0) - 1 for s in starts])
    return out, starts


def trend_state(breadth: np.ndarray) -> np.ndarray:
    """0 off, 1 mixed, 2 on from the share of the book `tsmom12` holds."""
    return np.where(breadth <= 1 / 3 + 1e-9, OFF, np.where(breadth >= 2 / 3 - 1e-9, ON, MIXED))


def eligible(b: np.ndarray) -> np.ndarray:
    """Sleeves with at least MIN_WEEKS weekly returns and non-zero variance."""
    ok = ~np.isnan(b)
    out = np.zeros(b.shape[1], dtype=bool)
    for m in range(b.shape[1]):
        x = b[ok[:, m], m]
        out[m] = len(x) >= MIN_WEEKS and x.std() > 0
    return out


def sharpe(x: np.ndarray) -> float:
    """Mean over standard deviation of weekly returns; 0 when there is no variance."""
    return float(x.mean() / x.std()) if len(x) > 1 and x.std() > 0 else 0.0


def stack(b: np.ndarray, t: int, pool: list[int]) -> tuple[int | None, float]:
    """B1: the complement least correlated with `tsmom12` in its losing weeks, and `tsmom12`'s
    share of the two-sleeve book (inverse variance over the last VAR_WEEKS weeks)."""
    el = eligible(b)
    if not el[t]:
        return None, 1.0
    best: tuple[float, int] | None = None
    for m in pool:
        if not el[m]:
            continue
        have = ~np.isnan(b[:, m]) & ~np.isnan(b[:, t])
        if sharpe(b[~np.isnan(b[:, m]), m]) <= 0:
            continue
        lose = have & (b[:, t] < 0)
        x, y = b[lose, m], b[lose, t]
        if lose.sum() < MIN_LOSING or x.std() == 0 or y.std() == 0:
            continue
        c = float(np.corrcoef(x, y)[0, 1])
        if best is None or c < best[0]:
            best = (c, m)
    if best is None:
        return None, 1.0
    m = best[1]
    vt = b[~np.isnan(b[:, t]), t][-VAR_WEEKS:].var()
    vm = b[~np.isnan(b[:, m]), m][-VAR_WEEKS:].var()
    return m, float((1 / vt) / (1 / vt + 1 / vm))


def switch(b: np.ndarray, state: np.ndarray, t: int, pool: list[int]) -> list[int]:
    """B2: for each trend state, the sleeve with the best Sharpe over the past weeks that began
    in that state (`state` holds each week's state). Ties and no data go to `tsmom12`."""
    el = eligible(b)
    out = []
    for s in (OFF, MIXED, ON):
        rows = state == s
        ok_t = rows & ~np.isnan(b[:, t])
        best, pick = sharpe(b[ok_t, t]), t
        for m in pool:
            ok_m = rows & ~np.isnan(b[:, m])
            if el[t] and el[m] and ok_m.sum() >= MIN_WEEKS:
                sc = sharpe(b[ok_m, m])
                if sc > best + 1e-12:
                    best, pick = sc, m
        out.append(pick)
    return out


def _ridge(x: np.ndarray, lam: float) -> np.ndarray:
    pen = lam * len(x) * float((x * x).mean())
    coef: np.ndarray = np.linalg.solve(x.T @ x + pen * np.eye(x.shape[1]), x.sum(axis=0))
    return coef


def meta(b: np.ndarray, t: int, pool: list[int]) -> tuple[np.ndarray, float]:
    """B3: ridge regression of 1 on the weekly returns of `tsmom12` and the eligible
    complements (no intercept), lambda by 5-fold cross-validation in time order; coefficients
    below zero dropped, the rest scaled to sum to 1. Returns shares over all sleeves and lambda.
    A sleeve's weeks before its first day take the average of the other sleeves that week."""
    el = eligible(b)
    shares = np.zeros(b.shape[1])
    shares[t] = 1.0
    cols = [t] + [m for m in pool if el[m]]
    if not el[t] or len(cols) < 2:
        return shares, float("nan")
    x = b[~np.isnan(b[:, t])][:, cols]
    fill = np.nanmean(x, axis=1, keepdims=True)
    x = np.where(np.isnan(x), fill, x)
    folds = np.array_split(np.arange(len(x)), FOLDS)
    best: tuple[float, float] | None = None
    for lam in LAMBDAS:
        err = 0.0
        for f in folds:
            train = np.ones(len(x), dtype=bool)
            train[f] = False
            err += float(((1 - x[f] @ _ridge(x[train], lam)) ** 2).sum())
        if best is None or err < best[0]:
            best = (err, lam)
    assert best is not None
    coef = np.clip(_ridge(x, best[1]), 0, None)
    if coef.sum() <= 0:
        return shares, best[1]
    shares[:] = 0.0
    shares[cols] = coef / coef.sum()
    return shares, best[1]


@dataclass
class Plan:
    """Sleeve shares for every decision day, and what each refit chose."""

    stack: np.ndarray  # days x sleeves
    meta: np.ndarray  # days x sleeves
    switch: np.ndarray  # days: index of the sleeve held
    log: list[dict[str, object]] = field(default_factory=list)


def plan(days: np.ndarray, r: np.ndarray, breadth: np.ndarray, t: int, pool: list[int]) -> Plan:
    """Walk forward: refit on the first Friday of each year from returns before it, hold the
    shares until the next refit. Before the first refit every book is `tsmom12`."""
    n, m = r.shape
    st_day = trend_state(breadth)
    a_stack, a_meta = np.zeros((n, m)), np.zeros((n, m))
    a_stack[:, t] = a_meta[:, t] = 1.0
    assign = np.full((n, 3), t, dtype=np.int64)
    log: list[dict[str, object]] = []
    ks = refit_days(days)
    for i, k in enumerate(ks):
        b, starts = blocks(r, k)
        if len(b) == 0:
            continue
        hi = ks[i + 1] if i + 1 < len(ks) else n
        comp, share = stack(b, t, pool)
        a_stack[k:hi] = 0.0
        a_stack[k:hi, t] = share
        if comp is not None:
            a_stack[k:hi, comp] = 1 - share
        sw = switch(b, st_day[starts], t, pool)
        assign[k:hi] = sw
        sh, lam = meta(b, t, pool)
        a_meta[k:hi] = sh
        log.append({"k": k, "stack": comp, "share": share, "switch": sw, "meta": sh, "lam": lam})
    pick = assign[np.arange(n), st_day]
    return Plan(a_stack, a_meta, pick, log)
