"""The two fitted rules (hmm-regime, hawkes-clustering), walk-forward as fixed on their cards.

Both refit on the first Friday of each calendar year, on bars visible that day, and need 1,000
bars. Needs numba:  uv run --with numpy --with numba python research/lib/test_<idea>.py
"""

from __future__ import annotations

import math
from datetime import date, timedelta

import numpy as np
from common import FIT_MIN_BARS, View, Weights, bpy, live, vol_series
from numba import njit

# --- shared schedule ---


def first_friday(year: int) -> date:
    d = date(year, 1, 1)
    return d + timedelta(days=(4 - d.weekday()) % 7)


def fit_year(today: date) -> int:
    return today.year if today >= first_friday(today.year) else today.year - 1


# --- hmm-regime ---


@njit(cache=True)
def _emis(x: np.ndarray, mu: np.ndarray, var: np.ndarray) -> np.ndarray:
    b = np.empty((len(x), 2))
    for k in range(2):
        b[:, k] = np.exp(-0.5 * (x - mu[k]) ** 2 / var[k]) / np.sqrt(2 * np.pi * var[k])
    return b + 1e-300


@njit(cache=True)
def hmm_em(x: np.ndarray, par: np.ndarray, iters: int) -> np.ndarray:
    """Baum-Welch for a 2-state Gaussian HMM. par = [mu0, mu1, var0, var1, a00, a11]."""
    n = len(x)
    mu = par[0:2].copy()
    var = par[2:4].copy()
    a = np.array([[par[4], 1 - par[4]], [1 - par[5], par[5]]])
    prev = -np.inf
    alpha = np.empty((n, 2))
    beta = np.empty((n, 2))
    scale = np.empty(n)
    for _ in range(iters):
        b = _emis(x, mu, var)
        p0 = (1 - a[1, 1]) / (2 - a[0, 0] - a[1, 1])
        alpha[0, 0] = p0 * b[0, 0]
        alpha[0, 1] = (1 - p0) * b[0, 1]
        scale[0] = alpha[0, 0] + alpha[0, 1]
        alpha[0] /= scale[0]
        for t in range(1, n):
            for j in range(2):
                alpha[t, j] = (alpha[t - 1, 0] * a[0, j] + alpha[t - 1, 1] * a[1, j]) * b[t, j]
            scale[t] = alpha[t, 0] + alpha[t, 1]
            alpha[t] /= scale[t]
        ll = np.log(scale).sum()
        beta[n - 1] = 1.0
        for t in range(n - 2, -1, -1):
            for i in range(2):
                beta[t, i] = (
                    a[i, 0] * b[t + 1, 0] * beta[t + 1, 0] + a[i, 1] * b[t + 1, 1] * beta[t + 1, 1]
                ) / scale[t + 1]
        gamma = alpha * beta
        xi = np.zeros((2, 2))
        for t in range(n - 1):
            for i in range(2):
                for j in range(2):
                    xi[i, j] += alpha[t, i] * a[i, j] * b[t + 1, j] * beta[t + 1, j] / scale[t + 1]
        for i in range(2):
            a[i] = xi[i] / xi[i].sum()
            w = gamma[:, i]
            mu[i] = (w * x).sum() / w.sum()
            var[i] = max((w * (x - mu[i]) ** 2).sum() / w.sum(), 1e-10)
        if ll - prev < 1e-6 * abs(ll):
            break
        prev = ll
    return np.array([mu[0], mu[1], var[0], var[1], a[0, 0], a[1, 1]])


@njit(cache=True)
def hmm_filter(x: np.ndarray, par: np.ndarray) -> np.ndarray:
    """P(state 0 | x[0..t]) for each t (forward filter only: causal)."""
    n = len(x)
    mu, var = par[0:2], par[2:4]
    a = np.array([[par[4], 1 - par[4]], [1 - par[5], par[5]]])
    b = _emis(x, mu, var)
    out = np.empty(n)
    p0 = (1 - a[1, 1]) / (2 - a[0, 0] - a[1, 1])
    f0, f1 = p0 * b[0, 0], (1 - p0) * b[0, 1]
    s = f0 + f1
    f0, f1 = f0 / s, f1 / s
    out[0] = f0
    for t in range(1, n):
        g0 = (f0 * a[0, 0] + f1 * a[1, 0]) * b[t, 0]
        g1 = (f0 * a[0, 1] + f1 * a[1, 1]) * b[t, 1]
        s = g0 + g1
        f0, f1 = g0 / s, g1 / s
        out[t] = f0
    return out


def _cold_start(x: np.ndarray) -> np.ndarray:
    calm = np.abs(x) <= np.median(np.abs(x))
    lo, hi = x[calm], x[~calm]
    return np.array([lo.mean(), hi.mean(), lo.var(), hi.var(), 0.98, 0.98])


def hmm_params(view: View, s: str, year: int) -> np.ndarray | None:
    """Parameters fitted on the first Friday of `year` (warm-started from the year before)."""
    key = ("hmm", s, year)
    cache = view.panel.cache
    if key not in cache:
        x = view.at(first_friday(year)).logret(s) if s in view.n else np.array([])
        if len(x) + 1 < FIT_MIN_BARS:
            cache[key] = None
        else:
            prev = hmm_params(view, s, year - 1)
            cache[key] = hmm_em(x, prev if prev is not None else _cold_start(x), 30)
    return cache[key]  # type: ignore[return-value]


def hmm_calm(view: View, s: str) -> float | None:
    """P(calm state | returns so far), or None before the first fit."""
    year = fit_year(view.today)
    par = hmm_params(view, s, year)
    if par is None:
        return None
    key = ("hmm-filter", s, year)
    cache = view.panel.cache
    if key not in cache:
        p0 = hmm_filter(view.panel.lr[s], par)  # entry i depends on returns 0..i only
        cache[key] = p0 if par[2] <= par[3] else 1 - p0
    series: np.ndarray = cache[key]  # type: ignore[assignment]
    return float(series[view.n[s] - 2])


def hmm_hard(view: View, s: str) -> bool:
    p = hmm_calm(view, s)
    return p is None or p > 0.5


def hmm_soft(view: View) -> Weights:
    held = live(view)
    out = {}
    for s in held:
        p = hmm_calm(view, s)
        out[s] = (1.0 if p is None else p) / len(held)
    return out


# --- hawkes-clustering ---


@njit(cache=True)
def _hawkes_ll(e: np.ndarray, mu: float, alpha: float, decay: float) -> float:
    s = 0.0
    ll = 0.0
    for t in range(len(e)):
        lam = mu + alpha * s
        ll += e[t] * np.log(lam) - lam
        s = decay * (s + e[t])
    return ll


@njit(cache=True)
def hawkes_fit(e: np.ndarray) -> np.ndarray:
    """(mu, alpha, beta) by likelihood on a grid of memory lengths and branching ratios.
    mu is tied to the observed event rate: mu = rate x (1 - branching ratio)."""
    rate = e.mean()
    best = (-np.inf, rate, 0.0, 1.0)
    for beta in np.exp(np.linspace(np.log(0.01), np.log(2.0), 30)):
        decay = np.exp(-beta)
        for ratio in np.linspace(0.0, 0.95, 20):
            alpha = ratio * (1 / decay - 1)  # so that alpha x sum_k decay^k = ratio
            mu = rate * (1 - ratio)
            ll = _hawkes_ll(e, mu, alpha, decay)
            if ll > best[0] + 1e-9:
                best = (ll, mu, alpha, beta)
    return np.array([best[1], best[2], best[3], rate])


def hawkes_events(view: View, s: str) -> np.ndarray:
    """1.0 where a log return is below -2 x the EWMA volatility through the day before."""
    key = ("hawkes-events", s)
    cache = view.panel.cache
    if key not in cache:
        lr = view.panel.lr[s]
        key_view = view.panel.view(view.panel.close_times[s][-1])
        vol = vol_series(key_view, s, 60) / math.sqrt(bpy(s))
        e = np.zeros(len(lr))
        e[21:] = (lr[21:] < -2 * vol[20:-1]).astype(np.float64)
        cache[key] = e
    full: np.ndarray = cache[key]  # type: ignore[assignment]
    return full[: view.n[s] - 1]


def hawkes_params(view: View, s: str, year: int) -> np.ndarray | None:
    key = ("hawkes", s, year)
    cache = view.panel.cache
    if key not in cache:
        v = view.at(first_friday(year))
        if v.n.get(s, 0) < FIT_MIN_BARS:
            cache[key] = None
        else:
            cache[key] = hawkes_fit(hawkes_events(v, s))
    return cache[key]  # type: ignore[return-value]


def hawkes_quiet(view: View, s: str) -> bool:
    """True if tomorrow's crash intensity is at or below its long-run average."""
    par = hawkes_params(view, s, fit_year(view.today))
    if par is None:
        return True
    mu, alpha, beta, rate = par
    e = hawkes_events(view, s)
    decay = math.exp(-beta)
    k = min(len(e), int(40 / beta) + 5)  # older events have decayed to nothing
    w = decay ** np.arange(k, 0, -1)
    lam = mu + alpha * float(w @ e[-k:])
    return lam <= rate * (1 + 1e-9)
