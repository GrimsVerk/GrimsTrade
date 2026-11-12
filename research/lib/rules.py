"""The idea rules, exactly as fixed on the cards in research/cards/."""

from __future__ import annotations

import math

import numpy as np
from common import (
    ResearchStrategy,
    View,
    Weights,
    bpy,
    eligible,
    live,
    trailing_logret,
    tsmom_signal,
    vol_series,
)

from grimstrade.data import CRYPTO, UNIVERSE

# --- kelly-shrunk ---


def kelly(k: float) -> ResearchStrategy:
    def f(view: View) -> Weights:
        g = view.grid(501)
        per_year = bpy(view.panel.grid_sym)
        held = []
        for s in live(view):
            col = g[:, view.syms.index(s)]
            if (~np.isnan(col)).sum() >= 251:
                held.append(s)
        if not held:
            return {}
        x = g[:, [view.syms.index(s) for s in held]]
        x = x[~np.isnan(x).any(axis=1)]
        r = np.diff(np.log(x), axis=0)
        w = 0.5 ** (np.arange(len(r))[::-1] / 60)
        cov = (r * w[:, None]).T @ r / w.sum()
        sd = np.sqrt(np.diag(cov))
        corr = 0.5 * cov / np.outer(sd, sd) + 0.5 * np.eye(len(held))
        frac = k * np.linalg.solve(corr, np.ones(len(held))) / (sd * math.sqrt(per_year))
        frac = np.maximum(frac, 0.0)
        if frac.sum() > 1:
            frac = frac / frac.sum()
        return {s: float(x) for s, x in zip(held, frac, strict=True)}

    return f


# --- fracdiff-momentum ---


def frac_window(s: str) -> int:
    return 730 if UNIVERSE[s] == CRYPTO else 500


def frac_weights(d: float, k: int) -> np.ndarray:
    """Return weights c_j = w_0 + ... + w_j of the order-d fractional difference."""
    w = np.empty(k)
    w[0] = 1.0
    for j in range(1, k):
        w[j] = -w[j - 1] * (d - j + 1) / j
    return np.cumsum(w)


def fracdiff_signal(d: float):  # type: ignore[no-untyped-def]
    cache: dict[int, np.ndarray] = {}

    def signal(view: View, s: str) -> bool:
        k = frac_window(s)
        lr = view.logret(s)
        if len(lr) < k:
            return False
        if k not in cache:
            cache[k] = frac_weights(d, k)
        return bool(cache[k] @ lr[-k:][::-1] > 0)

    return signal


def warmed(signal):  # type: ignore[no-untyped-def]
    """A twin's signal, switched on only once the fracdiff rule also has its window."""
    return lambda view, s: len(view.logret(s)) >= frac_window(s) and signal(view, s)


# --- drawdown-control ---


def drawdown_control(mult: float) -> ResearchStrategy:
    def f(view: View) -> Weights:
        held = live(view)
        out = {}
        for s in held:
            c = view.close(s)
            dd = 1 - c[-1] / c[-bpy(s) :].max()
            tol = mult * vol_series(view, s, 250)[-1]
            out[s] = max(0.0, 1 - dd / tol) / len(held)
        return out

    return f


# --- universal-portfolio ---

UP_MIXES = 20_000


def universal_portfolio(view: View) -> Weights:
    syms = view.syms
    g = view.grid()
    n = len(g)
    if n < 2:
        return {}
    cache = view.panel.cache
    if "up_mixes" not in cache:
        cache["up_mixes"] = np.random.default_rng(0).dirichlet(np.ones(len(syms) + 1), UP_MIXES)
    mixes: np.ndarray = cache["up_mixes"]  # type: ignore[assignment]
    dates = view.panel.grid_dates[:n]
    weeks = [d.isocalendar()[:2] for d in dates]
    ends = [i for i in range(n) if i == n - 1 or weeks[i + 1] != weeks[i]]  # last row of each week
    state = cache.get("up_state")
    if state is None or state[0] > ends[-1]:  # type: ignore[index]
        state = (ends[0], np.zeros(UP_MIXES))
    last, logw = state  # type: ignore[misc]
    seen = np.cumsum(~np.isnan(g), axis=0)  # rows of history each asset has at each grid row
    for e in ends:
        if e <= last:
            continue
        rel = g[e] / g[last]
        rel[np.isnan(rel) | (seen[last] < 252)] = 1.0  # not yet eligible: counts as cash
        logw = logw + np.log(mixes[:, :-1] @ rel + mixes[:, -1])
        last = e
    cache["up_state"] = (last, logw)
    w = np.exp(logw - logw.max())
    port = (w[:, None] * mixes).sum(axis=0) / w.sum()
    return {
        s: float(port[j]) for j, s in enumerate(syms) if seen[-1, j] >= 252 and eligible(view, s)
    }


def uniform_with_cash(view: View) -> Weights:
    return {s: 1 / (len(view.syms) + 1) for s in live(view)}


# --- run 2: vol-target, ensemble-tsmom, trend-vol ---


def vol20(view: View, s: str) -> float:
    lr = view.logret(s)[-20:]
    return float(math.sqrt((lr * lr).mean() * bpy(s)))


def vol_cap(view: View, s: str, target: float) -> float:
    v = vol20(view, s)
    return min(1.0, target / v) if v > 0 else 1.0


def vol_target(target: float) -> ResearchStrategy:
    def f(view: View) -> Weights:
        held = live(view)
        return {s: vol_cap(view, s, target) / len(held) for s in held}

    return f


def ensemble_tsmom(view: View) -> Weights:
    held = live(view)
    out = {}
    for s in held:
        rets = [trailing_logret(view, s, d) for d in (30, 91, 182, 365)]
        out[s] = sum(1 for r in rets if not math.isnan(r) and r > 0) / 4 / len(held)
    return out


def trend_vol(target: float) -> ResearchStrategy:
    def f(view: View) -> Weights:
        held = live(view)
        return {s: vol_cap(view, s, target) / len(held) for s in held if tsmom_signal(view, s)}

    return f
