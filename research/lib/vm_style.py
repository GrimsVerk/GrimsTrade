"""vm-style-1: pure parts of DeMiguel, Martin-Utrera and Uppal (JF 2024) on a sleeve book.

Card: research/cards/vm-style-1.md. No I/O. Months are `date`s on the first of the month; a
monthly series is a dict month -> value. Tests: tests/test_vm_style.py (synthetic data only).

The conditional mean-variance portfolio (DMU eq. 2-6): theta_k,t = a_k + b_k z_k,t, with z_k,t
the conditioner known before month t (1 / market volatility of month t-1 in the paper), and
eta = (a, b) >= 0 maximising (mu_ext - c)' eta - gamma / 2 eta' Sigma_ext eta on an expanding
window of the extended returns (r_k, r_k z_k). UMV is the same with b = 0.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from datetime import date

import numpy as np
from scipy.optimize import nnls

GAMMA = 5.0
MIN_HIST = 120
RIDGE = 1e-12
MIN_DAYS = 5

Monthly = Mapping[date, float]


def add_months(d: date, k: int) -> date:
    i = d.year * 12 + d.month - 1 + k
    return date(i // 12, i % 12 + 1, 1)


def realised_sd(daily: Iterable[tuple[date, float]]) -> dict[date, float]:
    """SD (ddof 1) of the daily returns inside each calendar month (DMU's sigma_t)."""
    by: dict[date, list[float]] = {}
    for d, r in daily:
        by.setdefault(d.replace(day=1), []).append(r)
    return {m: float(np.std(v, ddof=1)) for m, v in sorted(by.items()) if len(v) >= MIN_DAYS}


def trailing_sd(monthly: Monthly, window: int = 6) -> dict[date, float]:
    """SD (ddof 1) of the last `window` monthly values ending at month t (all must exist)."""
    out: dict[date, float] = {}
    for t in sorted(monthly):
        v = [monthly.get(add_months(t, -k)) for k in range(window)]
        if all(x is not None for x in v):
            out[t] = float(np.std([x for x in v if x is not None], ddof=1))
    return out


def conditioner(sd: Monthly, power: float = 1.0) -> dict[date, float]:
    """z for the return of month t: 1 / sd(t-1)^power (known at the end of t-1)."""
    return {add_months(m, 1): 1.0 / v**power for m, v in sd.items() if v > 0}


def fit_eta(m: np.ndarray, cov: np.ndarray, gamma: float = GAMMA) -> np.ndarray:
    """argmax m' eta - gamma / 2 eta' cov eta subject to eta >= 0, exactly (NNLS).

    With cov = L L', the objective is -gamma / 2 ||L' eta - v||^2 + const, v = L^-1 m / gamma."""
    k = len(m)
    chol = np.linalg.cholesky(cov + RIDGE * np.eye(k))
    v = np.linalg.solve(chol, m) / gamma
    eta, _ = nnls(chol.T, v)
    return np.asarray(eta, dtype=float)


def walk(
    sleeves: Mapping[str, Monthly],
    scale: Mapping[str, Monthly],
    kappa: Mapping[str, float],
    cond: Mapping[str, Monthly] | None,
    *,
    gamma: float = GAMMA,
    min_hist: int = MIN_HIST,
) -> tuple[dict[date, tuple[float, float, float]], dict[date, dict[str, float]]]:
    """DMU's out-of-sample walk. sleeves[k][t]: net return of sleeve k in month t; scale[k][t]:
    its vol scale s (gross notional per unit of theta is 2 s); kappa[k]: cost per unit traded;
    cond[k][t]: z_k,t known before month t (None = UMV, b = 0).

    A sleeve enters month t with >= min_hist returns before t (and z wherever needed); the window
    is every month before t in which all entered sleeves have a return (and z). Returns
    (t -> (net, gross, scaling cost), t -> theta per sleeve)."""
    allm = sorted({t for s in sleeves.values() for t in s})
    hist = dict.fromkeys(sleeves, 0)
    prev: dict[str, float] = {}
    last_s: dict[str, float] = {}
    out: dict[date, tuple[float, float, float]] = {}
    thetas: dict[date, dict[str, float]] = {}

    def ok(k: str, u: date) -> bool:
        return u in sleeves[k] and (cond is None or u in cond[k])

    for t in allm:
        ent = [k for k in sorted(sleeves) if hist[k] >= min_hist and ok(k, t)]
        theta: dict[str, float] = {}
        if ent:
            win = [u for u in allm if u < t and all(ok(k, u) for k in ent)]
            r = np.array([[sleeves[k][u] for k in ent] for u in win])
            if cond is None:
                x = r
                c = np.zeros(len(ent))
            else:
                z = np.array([[cond[k][u] for k in ent] for u in win])
                x = np.hstack([r, r * z])
                cb = np.zeros(len(ent))
                n = 0
                for i in range(1, len(win)):
                    if win[i - 1] != add_months(win[i], -1):
                        continue
                    g = np.array([2.0 * scale[k][win[i]] * kappa[k] for k in ent])
                    cb += g * np.abs(z[i] - z[i - 1])
                    n += 1
                c = np.concatenate([np.zeros(len(ent)), cb / max(n, 1)])
            mu = x.mean(0) - c
            cov = np.atleast_2d(np.cov(x, rowvar=False, ddof=1))
            eta = fit_eta(mu, cov, gamma)
            for i, k in enumerate(ent):
                th = float(eta[i])
                if cond is not None:
                    th += float(eta[len(ent) + i]) * cond[k][t]
                theta[k] = th
        gross = sum(theta[k] * sleeves[k][t] for k in theta)
        cost = 0.0
        for k in set(theta) | set(prev):
            s = scale[k][t] if k in theta else last_s.get(k, 0.0)
            cost += kappa[k] * 2.0 * s * abs(theta.get(k, 0.0) - prev.get(k, 0.0))
        if theta or prev:
            out[t] = (gross - cost, gross, cost)
            thetas[t] = theta
        for k in theta:
            last_s[k] = scale[k][t]
        prev = theta
        for k in sleeves:
            if t in sleeves[k]:
                hist[k] += 1
    return out, thetas


def sharpe(r: np.ndarray) -> float:
    sd = float(r.std(ddof=1))
    return float(r.mean()) / sd * math.sqrt(12) if sd > 0 else 0.0
