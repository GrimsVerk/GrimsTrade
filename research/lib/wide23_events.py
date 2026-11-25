"""Lane wide-23, gate W37 `hack-drift` and replication R37 (research/cards/wide-23.md): pure
functions. Parse the hack list, build the daily dose, move it for the placebos, build the
outcome and controls from daily closes, and fit OLS with Newey-West standard errors. No
function here reads a file, a price or the network; the tests feed small literal samples.
Days are `date.toordinal()` integers."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime

import numpy as np

MIN_USD = 10_000_000.0
UNIT_USD = 5_000_000.0  # weight log2(A / 5 m): 1 at USD 10 m
STEP_DAYS = 23  # placebo step: not a multiple of a week
SHIFTS = [STEP_DAYS * k for k in range(1, 41)]  # earlier doses only: 23 .. 920 days
SEED = 23
LAGS = 7

Event = tuple[int, float, str]  # (UTC day ordinal, USD amount, targetType)


def parse_hacks(text: str, last: date, min_usd: float = MIN_USD) -> list[Event]:
    """Events of the DefiLlama hack list with an amount >= `min_usd`, dated on or before
    `last` (UTC day of the `date` timestamp). Rows without a usable date or amount dropped."""
    out: list[Event] = []
    for r in json.loads(text):
        if not isinstance(r, dict):
            continue
        ts, amt = r.get("date"), r.get("amount")
        if not isinstance(ts, int | float) or not isinstance(amt, int | float):
            continue
        if not math.isfinite(float(amt)) or float(amt) < min_usd:
            continue
        day = datetime.fromtimestamp(float(ts), UTC).date()
        if day > last:
            continue
        out.append((day.toordinal(), float(amt), str(r.get("targetType") or "")))
    return sorted(out)


def split(events: Sequence[Event]) -> tuple[list[Event], list[Event]]:
    """(G, X): G = every target type but `CEX` (the gate), X = `CEX` only (R37)."""
    g = [e for e in events if e[2] != "CEX"]
    x = [e for e in events if e[2] == "CEX"]
    return g, x


def weight(usd: float, binary: bool = False) -> float:
    return 1.0 if binary else math.log2(usd / UNIT_USD)


def dose(events: Sequence[Event], binary: bool = False, min_usd: float = 0.0) -> dict[int, float]:
    """D(d) = sum of weights of the events dated day d (absent days have dose 0)."""
    d: dict[int, float] = {}
    for day, usd, _ in events:
        if usd >= min_usd:
            d[day] = d.get(day, 0.0) + weight(usd, binary)
    return d


def at(d: Mapping[int, float], day: int, shift: int = 0) -> float:
    """D_k(day) = D(day - shift): shift > 0 is an earlier dose."""
    return d.get(day - shift, 0.0)


def logret(c: Mapping[int, float], a: int, b: int) -> float:
    """ln C(b) - ln C(a), NaN if either close is missing."""
    if a not in c or b not in c:
        return math.nan
    return math.log(c[b] / c[a])


def rows(c: Mapping[int, float], last: int, ahead: int = 8, back: int = 29) -> list[int]:
    """Days d with every close from C(d-back) to C(d+ahead) present and d + ahead <= last."""
    return sorted(
        d for d in c if d + ahead <= last and all(j in c for j in range(d - back, d + ahead + 1))
    )


def ols_nw(cols: Sequence[np.ndarray], y: np.ndarray, lags: int) -> tuple[np.ndarray, np.ndarray]:
    """(beta, t) of y on [1, cols...], Newey-West (Bartlett) standard errors with `lags`.
    Rows are consecutive days."""
    n = len(y)
    X = np.column_stack([np.ones(n), *cols])
    xtx_inv = np.linalg.inv(X.T @ X)
    beta = xtx_inv @ X.T @ y
    u = y - X @ beta
    g = X * u[:, None]
    s = g.T @ g
    for j in range(1, lags + 1):
        w = 1.0 - j / (lags + 1.0)
        gj = g[j:].T @ g[:-j]
        s += w * (gj + gj.T)
    cov = xtx_inv @ s @ xtx_inv
    return beta, beta / np.sqrt(np.diag(cov))


def phase_surrogates(x: np.ndarray, n: int = 40, seed: int = SEED) -> list[np.ndarray]:
    """n phase-randomised surrogates of x (same mean and amplitude spectrum, random Fourier
    phases; Theiler et al. 1992). Deterministic for a seed."""
    mu = float(x.mean())
    f = np.fft.rfft(x - mu)
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        ph = rng.uniform(0.0, 2.0 * math.pi, len(f))
        ph[0] = 0.0
        if len(x) % 2 == 0:
            ph[-1] = 0.0
        out.append(np.fft.irfft(np.abs(f) * np.exp(1j * ph), n=len(x)) + mu)
    return out


def day_surrogates(x: np.ndarray, n: int = 40, seed: int = SEED) -> list[np.ndarray]:
    """n surrogates that put the non-zero values of x on positions drawn uniformly without
    replacement (the weights kept, their days random). Deterministic for a seed."""
    rng = np.random.default_rng(seed + 1)
    vals = x[x != 0]
    out = []
    for _ in range(n):
        s = np.zeros_like(x)
        s[rng.choice(len(x), size=len(vals), replace=False)] = vals
        out.append(s)
    return out


def rank_lowest(t: float, others: Sequence[float]) -> int:
    """1 + number of others at or below t (ties count against the true t)."""
    return 1 + sum(1 for o in others if o <= t)


def null_spread(p: Sequence[float]) -> tuple[float, float, float, float, float, float, float]:
    """(sd, share |t| >= 2, q5, median, q95, min, max)."""
    a = np.asarray(p, dtype=float)
    q5, q50, q95 = (float(v) for v in np.quantile(a, [0.05, 0.5, 0.95]))
    return (
        float(a.std(ddof=1)),
        float(np.mean(np.abs(a) >= 2)),
        q5,
        q50,
        q95,
        float(a.min()),
        float(a.max()),
    )
