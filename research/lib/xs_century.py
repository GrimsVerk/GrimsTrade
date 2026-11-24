"""xs-century-1: pure parts of the century style book (card: research/cards/xs-century-1.md).

No I/O. Months are `date`s on the first of the month; a monthly series is a dict month -> value.
Tests: tests/test_xs_century.py (synthetic data only).
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from datetime import date

import numpy as np

PER_YEAR = 12
TARGET_VOL = 0.10
VOL_WINDOW = 36
VOL_MIN = 24
SCALE_CAP = 4.0
MIN_ASSETS = 4
BLOCK = 12
DRAWS = 2000
SEED = 20261124
GRID = np.linspace(0.0, 1.0, 101)

Monthly = Mapping[date, float]


def add_months(d: date, k: int) -> date:
    i = d.year * 12 + d.month - 1 + k
    return date(i // 12, i % 12 + 1, 1)


def months(first: date, last: date) -> list[date]:
    out, d = [], first
    while d <= last:
        out.append(d)
        d = add_months(d, 1)
    return out


# --- signals (AMP 2013, KMPV 2018) ---


def momentum(ret: Monthly, t: date, end_lag: int) -> float | None:
    """Compound return over the 11 months ending at month t - end_lag (AMP's 12-1 when
    end_lag = 2); None if any month is missing."""
    acc = 1.0
    for k in range(end_lag, end_lag + 11):
        v = ret.get(add_months(t, -k))
        if v is None:
            return None
        acc *= 1.0 + v
    return acc - 1.0


def yield_change_value(y: Monthly, t: date, lag: int) -> float | None:
    """AMP bond value: 5-year change in the 10y yield, y(L) - y(L-60), L = t - lag."""
    a, b = y.get(add_months(t, -lag)), y.get(add_months(t, -lag - 60))
    return None if a is None or b is None else a - b


def reversal_value(px: Monthly, t: date, lag: int) -> float | None:
    """AMP commodity value (used for FX spot and commodities): log of the mean price over months
    L-65..L-54 minus log of the price at L, L = t - lag."""
    last = px.get(add_months(t, -lag))
    old = [px.get(add_months(t, -lag - k)) for k in range(54, 66)]
    if last is None or last <= 0 or any(v is None or v <= 0 for v in old):
        return None
    return math.log(sum(v for v in old if v is not None) / len(old)) - math.log(last)


def spread_value(a: Monthly, b: Monthly, t: date, lag: int) -> float | None:
    """Carry as a rate spread a(L) - b(L), L = t - lag."""
    m = add_months(t, -lag)
    x, y = a.get(m), b.get(m)
    return None if x is None or y is None else x - y


# --- weights and scaling ---


def rank_weights(signal: Mapping[str, float]) -> dict[str, float]:
    """AMP eq. 1: w_i = c (rank_i - mean rank), long side sums to +1, short side to -1.
    Ties get the mean rank. Empty if fewer than MIN_ASSETS or all ranks equal."""
    if len(signal) < MIN_ASSETS:
        return {}
    names = sorted(signal)
    vals = np.array([signal[n] for n in names], dtype=float)
    order = vals.argsort(kind="mergesort")
    ranks = np.empty(len(vals))
    ranks[order] = np.arange(1, len(vals) + 1, dtype=float)
    for v in np.unique(vals):  # mean rank for ties
        m = vals == v
        ranks[m] = ranks[m].mean()
    dev = ranks - ranks.mean()
    pos = dev[dev > 0].sum()
    if pos <= 0:
        return {}
    return {n: float(x / pos) for n, x in zip(names, dev, strict=True)}


def vol_scale(history: Sequence[float]) -> float | None:
    """10% a year over the SD of the last up-to-36 raw monthly returns (>= 24 needed), cap 4."""
    h = list(history)[-VOL_WINDOW:]
    if len(h) < VOL_MIN:
        return None
    sd = float(np.std(h, ddof=1)) * math.sqrt(PER_YEAR)
    if sd <= 0:
        return SCALE_CAP
    return min(SCALE_CAP, TARGET_VOL / sd)


def constructed_sleeve(
    signals: Mapping[date, Mapping[str, float]],
    returns: Mapping[str, Monthly],
    cost: float,
) -> dict[date, tuple[float, float, float]]:
    """A rank-weighted, vol-scaled sleeve. signals[t]: the signal per asset known at the start
    of t (only assets with a month-t return are ranked). Returns t -> (net, gross scaled,
    raw gross unscaled) for every month the sleeve is live and scaled. Cost: per unit of
    one-way turnover of the scaled weights (entering counts as turnover)."""
    out: dict[date, tuple[float, float, float]] = {}
    raw_hist: list[float] = []
    prev_w: dict[str, float] = {}
    for t in sorted(signals):
        sig = {a: v for a, v in signals[t].items() if t in returns.get(a, {})}
        w = rank_weights(sig)
        if not w:
            prev_w = {}
            continue
        raw = sum(w[a] * returns[a][t] for a in w)
        s = vol_scale(raw_hist)
        raw_hist.append(raw)
        if s is None:
            continue
        sw = {a: s * x for a, x in w.items()}
        turn = sum(abs(sw.get(a, 0.0) - prev_w.get(a, 0.0)) for a in set(sw) | set(prev_w))
        prev_w = sw
        out[t] = (s * raw - cost * turn, s * raw, raw)
    return out


def factor_sleeve(
    raw: Monthly, cost_month: float, borrow_year: float
) -> dict[date, tuple[float, float, float]]:
    """A published long-short factor (HML, UMD), vol-scaled on its own past gross returns;
    cost and borrow per $ of scaled notional (one $ short per $ of scale)."""
    out: dict[date, tuple[float, float, float]] = {}
    hist: list[float] = []
    for t in sorted(raw):
        s = vol_scale(hist)
        hist.append(raw[t])
        if s is None:
            continue
        net = s * (raw[t] - cost_month - borrow_year / PER_YEAR)
        out[t] = (net, s * raw[t], raw[t])
    return out


def book(classes: Mapping[str, Sequence[Mapping[date, float]]]) -> dict[date, float]:
    """Equal weight across live classes; inside a class equal weight across live sleeves."""
    allm = sorted({t for sl in classes.values() for s in sl for t in s})
    out: dict[date, float] = {}
    for t in allm:
        means = []
        for sl in classes.values():
            live = [s[t] for s in sl if t in s]
            if live:
                means.append(sum(live) / len(live))
        if means:
            out[t] = sum(means) / len(means)
    return out


# --- statistics (monthly; as alpha-form-1, with 12-month blocks) ---


def nw_lag(n: int) -> int:
    return int(math.floor(4 * (n / 100) ** (2 / 9)))


def alpha(r: np.ndarray, t: np.ndarray) -> dict[str, float]:
    """OLS r = a + b t + e: monthly alpha, beta, annual residual IR, Newey-West SE and z."""
    n = len(r)
    x = np.column_stack([np.ones(n), t])
    xtx_inv = np.linalg.inv(x.T @ x)
    coef = xtx_inv @ (x.T @ r)
    e = r - x @ coef
    sd_e = float(e.std(ddof=2))
    lag = nw_lag(n)
    u = x * e[:, None]
    s = u.T @ u
    for j in range(1, lag + 1):
        g = u[j:].T @ u[:-j]
        s += (1 - j / (lag + 1)) * (g + g.T)
    cov = xtx_inv @ s @ xtx_inv
    se = math.sqrt(max(float(cov[0, 0]), 0.0))
    a = float(coef[0])
    return {
        "a": a,
        "b": float(coef[1]),
        "ir": a / sd_e * math.sqrt(PER_YEAR) if sd_e > 0 else 0.0,
        "se_nw": se,
        "z_nw": a / se if se > 0 else 0.0,
        "lag": lag,
        "n": n,
    }


def _mix_sharpe(mr, mt, vr, vt, c, w):  # type: ignore[no-untyped-def]
    m = w * mr + (1 - w) * mt
    v = w**2 * vr + (1 - w) ** 2 * vt + 2 * w * (1 - w) * c
    return np.where(v > 0, m / np.sqrt(np.maximum(v, 1e-300)), -np.inf)


def best_mix(r: np.ndarray, t: np.ndarray) -> dict[str, float]:
    """Long-only, fully invested mix w r + (1 - w) t with the largest in-sample Sharpe (grid)."""
    mr, mt = float(r.mean()), float(t.mean())
    vr, vt = float(r.var(ddof=1)), float(t.var(ddof=1))
    c = float(np.cov(r, t)[0, 1])
    sr = _mix_sharpe(mr, mt, vr, vt, c, GRID)
    i = int(np.argmax(sr))
    sr_t = mt / math.sqrt(vt) if vt > 0 else 0.0
    k = math.sqrt(PER_YEAR)
    return {"w": float(GRID[i]), "sr_mix": float(sr[i]) * k, "sr_t": sr_t * k,
            "gain": (float(sr[i]) - sr_t) * k}  # fmt: skip


def boot_se(r: np.ndarray, t: np.ndarray, draws: int = DRAWS, seed: int = SEED) -> float:
    """Circular block bootstrap (12-month blocks) SE of the monthly alpha."""
    rng = np.random.default_rng(seed)
    n = len(r)
    nb = -(-n // BLOCK)
    out = []
    for chunk in range(0, draws, 250):
        k = min(250, draws - chunk)
        starts = rng.integers(0, n, size=(k, nb))
        idx = (starts[:, :, None] + np.arange(BLOCK)[None, None, :]).reshape(k, -1)[:, :n] % n
        rs_, ts_ = r[idx], t[idx]
        mr, mt = rs_.mean(1), ts_.mean(1)
        vt = ts_.var(1, ddof=1)
        c = ((rs_ - mr[:, None]) * (ts_ - mt[:, None])).sum(1) / (n - 1)
        out.append(mr - c / vt * mt)
    return float(np.concatenate(out).std(ddof=1))


def score(r: np.ndarray, t: np.ndarray, draws: int = DRAWS) -> dict[str, float]:
    """The card's statistic: alpha, NW and bootstrap SE, z with the larger SE (decides)."""
    a = alpha(r, t)
    se_b = boot_se(r, t, draws)
    se = max(a["se_nw"], se_b)
    k = math.sqrt(PER_YEAR)
    out = dict(a)
    out.update(
        se_boot=se_b,
        z_boot=a["a"] / se_b if se_b > 0 else 0.0,
        z=a["a"] / se if se > 0 else 0.0,
        rho=float(np.corrcoef(r, t)[0, 1]),
        sr_r=float(r.mean() / r.std(ddof=1)) * k,
        vol_r=float(r.std(ddof=1)) * k,
        years=len(r) / PER_YEAR,
    )
    out.update({f"mix_{k_}": v for k_, v in best_mix(r, t).items()})
    return out
