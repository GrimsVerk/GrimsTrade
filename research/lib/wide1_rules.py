"""Pure rule logic of research run wide-1, exactly as fixed on the cards in research/cards/
(auction-concession, rebalance-pressure, contagion-catchup, vol-echo). numpy and the standard
library only, free of `harness`, so the tests can import it."""

from __future__ import annotations

import bisect
from collections.abc import Mapping, Sequence
from datetime import date

import numpy as np

# --- vol-echo ---


def echo_in(lr: np.ndarray, n: int, theta: float, hold: int = 3) -> np.ndarray:
    """`out[m]` is True if the decision that sees the first `m` returns holds the asset.

    Trigger at `m`: the return that leaves the `n`-return window at the next close, `lr[m - n]`,
    holds at least `theta` of the window's sum of squares. The asset is held for `hold` sessions
    from the roll-off day, so the decision is "in" if a trigger occurred at m, m-1 .. m-hold+1.
    Entry `m` uses `lr[:m]` only."""
    sq = lr * lr
    cs = np.concatenate([[0.0], np.cumsum(sq)])
    trig = np.zeros(len(lr) + 1, dtype=bool)
    m = np.arange(n, len(lr) + 1)
    if len(m):
        tot = cs[m] - cs[m - n]
        leave = sq[m - n]
        trig[n:] = (tot > 0) & (leave >= theta * tot)
    out = trig.copy()
    for k in range(1, hold):
        out[k:] |= trig[:-k]
    return out


# --- auction-concession ---


def term_years(term: str) -> float:
    """'29-Year 9-Month' -> 29.75."""
    years = 0.0
    for part in term.split():
        num, _, unit = part.partition("-")
        if unit.startswith("Year"):
            years += float(num)
        elif unit.startswith("Month"):
            years += float(num) / 12
    return years


def auction_group(security_type: str, original_term: str, tips: str, frn: str) -> str | None:
    """`long` (bonds of 19 years or more: TLT), `mid` (notes of 6y11m to 10y: IEF), else None.
    Nominal fixed-rate securities only."""
    if tips != "No" or frn != "No":
        return None
    y = term_years(original_term)
    if security_type == "Bond" and y >= 19:
        return "long"
    if security_type == "Note" and 6.9 <= y <= 10.01:
        return "mid"
    return None


def out_days(
    cal: Sequence[date], auctions: Sequence[tuple[date, date]], before: int = 5
) -> set[date]:
    """Sessions after whose close the slot is empty: A-`before` .. A-1 for each auction day A
    (the next session if A is not one), as far as they fall on or after the announcement.
    `auctions` = (announcement date, auction date). The slot is then out for sessions A-4 .. A."""
    out: set[date] = set()
    for announced, auction in auctions:
        j = bisect.bisect_left(cal, auction)
        if j >= len(cal):
            continue
        for k in range(max(j - before, 0), j):
            if cal[k] >= announced:
                out.add(cal[k])
    return out


# --- rebalance-pressure ---


def _same_month(a: date, b: date) -> bool:
    return (a.year, a.month) == (b.year, b.month)


def month_phase(cal: Sequence[date], i: int) -> tuple[str, int] | None:
    """For the decision after the close of session `cal[i]`: ('pressure', index of T) on the
    sessions T-5 .. T-1 (T = the month's last session), ('rebound', index of T) on T and on the
    first two sessions of the next month, else None. None too if the calendar ends before the
    month does (T unknown)."""
    d = cal[i]
    j = i
    while j + 1 < len(cal) and _same_month(cal[j + 1], d):
        j += 1
    if j + 1 >= len(cal):
        return None
    left = j - i
    if 1 <= left <= 5:
        return ("pressure", j)
    if left == 0:
        return ("rebound", i)
    k = i
    while k - 1 >= 0 and _same_month(cal[k - 1], d):
        k -= 1
    if i - k + 1 <= 2 and k >= 1:
        return ("rebound", k - 1)
    return None


def month_refs(cal: Sequence[date], t: int) -> tuple[int, int] | None:
    """(index of M = T-5, index of the previous month's last session) for month end `cal[t]`."""
    k = t
    while k - 1 >= 0 and _same_month(cal[k - 1], cal[t]):
        k -= 1
    if k < 1 or t - 5 < k:
        return None
    return t - 5, k - 1


def tilt(
    base: Mapping[str, float], halve: Sequence[str], receive: Sequence[str]
) -> dict[str, float]:
    """Halve every held weight in `halve`; split the freed weight equally among the assets of
    `receive` that the base holds (cash if it holds none)."""
    w = dict(base)
    freed = 0.0
    for s in halve:
        if w.get(s, 0.0) > 0:
            freed += w[s] / 2
            w[s] = w[s] / 2
    got = [s for s in receive if w.get(s, 0.0) > 0]
    for s in got:
        w[s] += freed / len(got)
    return w


# --- contagion-catchup ---


def catchup(z: np.ndarray, daily: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(lambda, catchup) per asset. `z`: standardised one-week move (NaN = unknown). `daily`:
    rows x assets of daily log returns (NaN where missing). lambda_i = sum_j w_ij z_j / sum_j
    w_ij with w_ij = max(corr_ij, 0), w_ii = 0, over assets with a full window; 0 otherwise."""
    lam = np.zeros(len(z))
    full = np.isfinite(z) & ~np.isnan(daily).any(axis=0)
    full &= np.nan_to_num(daily, nan=0.0).std(axis=0) > 0
    if full.sum() >= 2:
        w = np.clip(np.corrcoef(daily[:, full].T), 0.0, None)
        np.fill_diagonal(w, 0.0)
        den = w.sum(axis=1)
        num = w @ z[full]
        lam[full] = np.where(den > 0, num / np.where(den > 0, den, 1.0), 0.0)
    return lam, lam - z


def top_slots(
    names: Sequence[str], signal: np.ndarray, up: Sequence[bool], k: int
) -> dict[str, float]:
    """The `k` assets with the highest finite signal get slot 1/k each, held only while `up`."""
    order = [int(i) for i in np.argsort(-signal, kind="mergesort") if np.isfinite(signal[i])]
    return {names[i]: 1.0 / k for i in order[:k] if up[i]}


def rank_ic(x: np.ndarray, y: np.ndarray) -> float:
    """Spearman rank correlation of the finite pairs (NaN if fewer than 5)."""
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 5:
        return float("nan")
    rx = np.argsort(np.argsort(x[ok], kind="mergesort"), kind="mergesort").astype(float)
    ry = np.argsort(np.argsort(y[ok], kind="mergesort"), kind="mergesort").astype(float)
    if rx.std() == 0 or ry.std() == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])
