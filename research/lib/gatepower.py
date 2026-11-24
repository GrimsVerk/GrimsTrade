"""Lane gate-power: pure functions for the planted-effect power study (research/gate-power.md).

No I/O, no network, no randomness of its own (draws come in from the runner). The runner is
`gatepower_run.py`.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

import numpy as np

# Effect sizes: f = planted return per unit-SD position, in units of the asset's per-period SD.
F_GRID: tuple[float, ...] = (0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.30, 0.40, 0.60, 0.80)
N_SIM = 200
EARLIER_SHIFTS: list[int] = list(range(27, 184, 4))  # 40 earlier-dose shifts, weeks
TSMOM12 = 1.05  # tsmom12's train Sharpe (research/tries.md baseline row)

Fit = Callable[[np.ndarray, np.ndarray, np.ndarray | None, np.ndarray | None], tuple[float, float]]


def dk_fit(
    x: np.ndarray, y: np.ndarray, period: np.ndarray, lags: int, j: int
) -> tuple[float, float]:
    """(coefficient, Driscoll-Kraay t) of column j: the statistic of `wide11_events.ols_dk`,
    vectorized. No constant added; NaN rows and all-zero columns dropped; scores summed within
    each integer `period`, then Newey-West with Bartlett weights over period distance."""
    ok = ~(np.isnan(x).any(axis=1) | np.isnan(y))
    xa, ya, pa = x[ok], y[ok], period[ok]
    keep = xa.any(axis=0)
    if not keep[j]:
        return math.nan, math.nan
    jj = int(keep[:j].sum())
    xk = xa[:, keep]
    inv = np.linalg.inv(xk.T @ xk)
    b = inv @ (xk.T @ ya)
    e = ya - xk @ b
    p0 = (pa - pa.min()).astype(int)
    s = np.zeros((int(p0.max()) + 1, xk.shape[1]))
    np.add.at(s, p0, xk * e[:, None])
    meat = s.T @ s
    for lag in range(1, lags + 1):
        g = s[lag:].T @ s[:-lag]
        meat += (1 - lag / (lags + 1)) * (g + g.T)
    var = float((inv @ meat @ inv)[jj, jj])
    return float(b[jj]), float(b[jj] / math.sqrt(var)) if var > 0 else math.nan


def position(z: np.ndarray, h: int, mask: np.ndarray) -> np.ndarray:
    """The position a trader acting on the gate's claim holds in each period: the mean of the
    standardized doses (NaN counts 0) of the last h periods, whose outcome windows cover this
    period, rescaled to unit SD over `mask` (the periods the gate's outcomes span)."""
    zz = np.nan_to_num(z, nan=0.0)
    c = np.concatenate([[0.0], np.cumsum(zz)])
    i = np.arange(len(zz))
    lo = np.maximum(i - h + 1, 0)
    x = (c[i + 1] - c[lo]) / h
    sd = float(x[mask].std())
    return x / sd if sd > 0 else x


def standardize(v: np.ndarray) -> np.ndarray:
    """(v - mean) / sd over the finite values; NaN stays NaN."""
    m = np.isfinite(v)
    return (v - v[m].mean()) / v[m].std()


def window_sum(r: np.ndarray, start: np.ndarray, h: int) -> np.ndarray:
    """sum of r[start + j], j = 0..h-1, per start; NaN when any index falls outside r."""
    idx = start[:, None] + np.arange(h)[None, :]
    bad = (idx < 0) | (idx >= len(r))
    out = r[np.clip(idx, 0, len(r) - 1)].sum(axis=1)
    out[bad.any(axis=1)] = np.nan
    return out


def rank_highest(true: float, others: Sequence[float]) -> int:
    """1 + the number of others strictly above `true` (1 = the highest)."""
    return 1 + sum(o > true for o in others)


def passes(b: float, t: float, placebo: Sequence[float]) -> bool:
    """The gates' rule: b > 0, t >= 2 and rank 1 or 2 of 1 + len(placebo)."""
    return b > 0 and t >= 2 and rank_highest(t, placebo) <= 2


def mde(fs: Sequence[float], rates: Sequence[float], target: float = 0.8) -> float:
    """Smallest f with detection rate >= target, linearly interpolated on the grid; NaN if the
    grid never reaches it. Rates are taken as they come (no monotone smoothing)."""
    for k in range(1, len(fs)):
        if rates[k] >= target:
            r0, r1 = rates[k - 1], rates[k]
            if r0 >= target:
                return float(fs[k - 1])
            return float(fs[k - 1] + (target - r0) / (r1 - r0) * (fs[k] - fs[k - 1]))
    return math.nan


def n_eff(v: np.ndarray) -> float:
    """N / (1 + 2 sum of autocorrelations up to the first non-positive lag), finite values of a
    series on a regular clock (NaN gaps dropped, which is close enough for a diagnostic)."""
    a = v[np.isfinite(v)]
    a = a - a.mean()
    n = len(a)
    den = float(a @ a)
    tau = 1.0
    for k in range(1, n // 2):
        rho = float(a[k:] @ a[:-k]) / den
        if rho <= 0:
            break
        tau += 2 * rho
    return n / tau


def ir(f: float, per_year: int) -> float:
    """Standalone information ratio of a unit-SD timing position earning f per-period SDs."""
    return f * math.sqrt(per_year)


def added_sharpe(info_ratio: float, base: float = TSMOM12) -> float:
    """Sharpe gained by mixing an uncorrelated overlay optimally into a book of Sharpe `base`."""
    return math.sqrt(base**2 + info_ratio**2) - base


@dataclass
class Design:
    """One gate rebuilt on a per-period return clock (`pool`).

    base(s) gives the noise returns of draw s per asset (rotated or permuted real returns);
    row_asset/row_i say which asset and pool period each gate row starts its outcome window at;
    the outcome is the sum of h periods; controls are past sums over the given windows; `fit`
    is the gate's statistic for (dose, y, controls, row subset mask)."""

    name: str
    assets: list[str]
    base: Callable[[int], dict[str, np.ndarray]]
    sigma: dict[str, float]
    pos: dict[str, np.ndarray]
    row_asset: np.ndarray
    row_i: np.ndarray
    h: int
    true: np.ndarray
    old: list[np.ndarray]
    new: list[np.ndarray] | None
    fit: Fit
    controls: tuple[int, ...] = ()
    subsets: list[np.ndarray] = field(default_factory=list)


@dataclass
class SimResult:
    fs: list[float]
    rate_old: list[float]
    rate_new: list[float]
    rate_t2: list[float]
    rate_old_plus: list[float]  # old rule plus the gate's own extra conditions (subsets)
    null_old: list[float]  # placebo t at f = 0, all draws pooled
    null_new: list[float]
    true_null: list[float]  # true-dose t at f = 0


def outcomes(d: Design, r: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray | None]:
    """(y, controls) per gate row from per-period returns r."""
    y = np.full(len(d.row_i), np.nan)
    ctrl = np.full((len(d.row_i), len(d.controls)), np.nan) if d.controls else None
    for k, a in enumerate(d.assets):
        m = d.row_asset == k
        y[m] = window_sum(r[a], d.row_i[m], d.h)
        if ctrl is not None:
            for c, w in enumerate(d.controls):
                ctrl[m, c] = window_sum(r[a], d.row_i[m] - w, w)
    return y, ctrl


def simulate(d: Design, fs: Sequence[float] = F_GRID, n_sim: int = N_SIM) -> SimResult:
    """Detection rates by f under the old and the corrected placebo rule (placebo t are only
    computed where the true cell already has b > 0 and t >= 2, except at f = 0)."""
    new = d.new if d.new is not None else d.old
    hit_old = np.zeros(len(fs))
    hit_new = np.zeros(len(fs))
    hit_t2 = np.zeros(len(fs))
    hit_plus = np.zeros(len(fs))
    null_old: list[float] = []
    null_new: list[float] = []
    true_null: list[float] = []
    for s in range(n_sim):
        base = d.base(s)
        for q, f in enumerate(fs):
            r = {a: base[a] + f * d.sigma[a] * d.pos[a] for a in d.assets}
            y, ctrl = outcomes(d, r)
            b, t = d.fit(d.true, y, ctrl, None)
            if f == 0:
                true_null.append(t)
                po = [d.fit(x, y, ctrl, None)[1] for x in d.old]
                pn = po if d.new is None else [d.fit(x, y, ctrl, None)[1] for x in new]
                null_old += po
                null_new += pn
            elif not (b > 0 and t >= 2):
                continue
            else:
                po = [d.fit(x, y, ctrl, None)[1] for x in d.old]
                pn = po if d.new is None else [d.fit(x, y, ctrl, None)[1] for x in new]
            ok_t2 = b > 0 and t >= 2
            ok_old = passes(b, t, po)
            ok_new = passes(b, t, pn)
            hit_t2[q] += ok_t2
            hit_old[q] += ok_old
            hit_new[q] += ok_new
            if ok_old and d.subsets:
                ok_old = all(d.fit(d.true, y, ctrl, m)[0] > 0 for m in d.subsets)
            hit_plus[q] += ok_old
    n = float(n_sim)
    return SimResult(
        list(fs),
        list(hit_old / n),
        list(hit_new / n),
        list(hit_t2 / n),
        list(hit_plus / n),
        null_old,
        null_new,
        true_null,
    )
