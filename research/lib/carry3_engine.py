"""Simulator and shapes of research run carry-3 (card in research/carry-3.md). A copy of
short-1's signed-weight simulator (`short_engine.py`, not edited) in which the decision sees
the drifted weights (for the no-trade band), costs depend on each trade's size, and orders
below the smallest order are not made. Kept free of `harness` so tests can import it.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import numpy as np

Decide = Callable[[int, int, np.ndarray], np.ndarray]  # (k, day, drifted weights) -> wanted
Charge = Callable[[int, np.ndarray], np.ndarray]  # (day, weight changes) -> [fee, spread, impact]


@dataclass
class Run:
    r: np.ndarray  # daily account returns, from first_day + 1
    funding: np.ndarray  # funding part of each day's return (positive = received)
    gross: np.ndarray  # gross exposure at each day's close
    net: np.ndarray  # net exposure at each day's close
    traded: np.ndarray  # sum of |weight change| traded at each day's close
    cost: np.ndarray  # [days, 3]: fee, spread, impact charged at each day's close


def ffill(a: np.ndarray) -> np.ndarray:
    """Forward fill NaN down the rows (days)."""
    idx = np.where(np.isfinite(a), np.arange(a.shape[0])[:, None], 0)
    np.maximum.accumulate(idx, axis=0, out=idx)
    out: np.ndarray = a[idx, np.arange(a.shape[1])[None, :]]
    return out


def simulate(
    px: np.ndarray,
    fund: np.ndarray | None,
    base: np.ndarray,
    decide: Decide,
    charge: Charge,
    first_day: int,
    min_dw: np.ndarray | None = None,
) -> Run:
    """At the close of each `base` day the book asks `decide` for weights and trades to them;
    weights drift with prices in between. `charge` prices the trades. A trade smaller than
    `min_dw[day]` is not made, except closing a position. Missing price: no return. If equity
    reaches 0 the account stays dead."""
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
    net = np.zeros(n_days)
    traded = np.zeros(n_days)
    cost = np.zeros((n_days, 3))
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
            new = decide(k, t, w.copy())
            dw = new - w
            if min_dw is not None:
                skip = (np.abs(dw) < min_dw[t]) & (new != 0)
                dw = np.where(skip, 0.0, dw)
            parts = charge(t, dw)
            out[t] = (1 + out[t]) * (1 - float(parts.sum())) - 1
            cost[t] = parts
            traded[t] = float(np.abs(dw).sum())
            w = w + dw
        gross[t] = float(np.abs(w).sum())
        net[t] = float(w.sum())
    # the first entry's cost is booked on first_day, which is not returned: carry it forward
    if first_day + 1 < n_days:
        out[first_day + 1] = (1 + out[first_day]) * (1 + out[first_day + 1]) - 1
        cost[first_day + 1] += cost[first_day]
        traded[first_day + 1] += traded[first_day]
    s = slice(first_day + 1, n_days)
    return Run(out[s], fout[s], gross[s], net[s], traded[s], cost[s])


def long_short(sig: np.ndarray, m: np.ndarray, frac: float = 1 / 3) -> np.ndarray:
    """+0.5 spread over the top `frac` of `m` by signal, -0.5 over the bottom `frac`
    (short-1's rule, copied)."""
    w = np.zeros(len(m))
    idx = np.flatnonzero(m)
    k = max(1, int(round(len(idx) * frac)))
    if len(idx) < 2 * k:
        return w
    order = idx[np.argsort(-sig[idx], kind="mergesort")]
    w[order[:k]] = 0.5 / k
    w[order[-k:]] = -0.5 / k
    return w


def band_weights(
    sig: np.ndarray,
    m: np.ndarray,
    w: np.ndarray,
    enter: float = 1 / 3,
    tol: float = 0.25,
) -> np.ndarray:
    """The card's `band` shape. A coin enters a leg when it is in that leg's `enter` share of
    the ranked coins and stays until it leaves that leg's half. Each leg's target is 0.5 split
    equally over its members. A member already held on the right side is left alone while its
    weight is within `tol` (relative) of the target; entries and exits trade in full. Coins
    outside `m` are closed."""
    out = np.zeros(len(m))
    idx = np.flatnonzero(m)
    n = len(idx)
    k = max(1, int(round(n * enter)))
    if n < 2 * k:
        return out
    order = idx[np.argsort(-sig[idx], kind="mergesort")]
    h = n // 2
    long = np.zeros(len(m), bool)
    short = np.zeros(len(m), bool)
    long[order[:k]] = True
    short[order[-k:]] = True
    stay_long = np.zeros(len(m), bool)
    stay_short = np.zeros(len(m), bool)
    stay_long[order[:h]] = True
    stay_short[order[n - h :]] = True
    long |= stay_long & (w > 0)
    short |= stay_short & (w < 0)
    out[long] = 0.5 / long.sum()
    out[short] = -0.5 / short.sum()
    keep = (w * out > 0) & (np.abs(w - out) <= tol * np.abs(out))
    return np.where(keep, w, out)


def top_n(adv: np.ndarray, m: np.ndarray, n: int) -> np.ndarray:
    """The `n` coins of `m` with the highest ADV (the liquidity-floor robustness row)."""
    out = np.zeros(len(m), bool)
    idx = np.flatnonzero(m & np.isfinite(adv))
    out[idx[np.argsort(-adv[idx], kind="mergesort")[:n]]] = True
    return out


# ---------------------------------------------------------------- held-out guard

CLAIM = "claim: the one held-out run of carry-3 starts"


def heldout_rows(tries: Path, idea: str = "carry-3") -> tuple[int, int]:
    """(claim rows, result rows) of the idea's held-out period in tries.md."""
    claims = results = 0
    for line in tries.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[1].startswith(idea) and cells[4] == "heldout":
            if cells[2] == CLAIM:
                claims += 1
            else:
                results += 1
    return claims, results


def heldout_used(tries: Path, idea: str = "carry-3") -> bool:
    return sum(heldout_rows(tries, idea)) > 0


def claim_heldout(tries: Path, stamp: str, idea: str = "carry-3") -> None:
    """Write the claim row before any held-out bar is loaded. Refuse once result rows exist (the
    year was looked at). A run that crashed before it wrote or showed any result has left only
    its claim: it may be restarted, and the claim is not written twice."""
    claims, results = heldout_rows(tries, idea)
    if results:
        raise RuntimeError(f"{idea}: the held-out year was already spent; no second look")
    if claims:
        print("restarting a held-out run that never produced a result (claim row found)")
        return
    row = (
        f"| {stamp} | {idea} | {CLAIM} | variant | heldout | 2025-11-11 | 2026-11-09 |"
        " - | - | - | - |\n"
    )
    with tries.open("a") as f:
        f.write(row)
