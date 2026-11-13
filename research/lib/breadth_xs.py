"""Cross-sectional engine of research run breadth-1 (card in research/breadth-1.md).

Everything is a calendar-day matrix `[days, assets]`: `px` (close, NaN where unknown; forward
filled where a market is shut), `elig` (bool, the point-in-time universe on that day) and a
signal (NaN where unknown). A signal on day `t` uses only data the card's as-of rule allows at
`t`; the position decided on `t` is set at the close of day `t + skip` and held to the next
decision's `t' + skip`. Weights drift with prices in between; costs are charged on the weight
change at each reset (drift included).

    ic_stats(px, elig, sig, dec, skip) -> mean IC, t, share positive, halves
    tilt(px, elig, sig, up, dec, skip, cost) -> daily returns of EW, TOP, TS, TOP-TS
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _rank(x: np.ndarray) -> np.ndarray:
    """Average ranks of a 1-d array (ties averaged)."""
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    r[order] = np.arange(len(x), dtype=float)
    xs = x[order]
    _, start, counts = np.unique(xs, return_index=True, return_counts=True)
    for s, c in zip(start, counts, strict=True):
        if c > 1:
            r[order[s : s + c]] = s + (c - 1) / 2
    return r


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = _rank(a), _rank(b)
    sa, sb = ra.std(), rb.std()
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def fwd_logret(px: np.ndarray, base: np.ndarray, end: np.ndarray) -> np.ndarray:
    """log(px[end] / px[base]) per decision row; NaN where the base price is missing. A price
    missing at `end` falls back to the last earlier finite price (exit at the last price)."""
    filled = ffill(px)
    out = np.log(filled[end] / px[base])
    return out


def ffill(a: np.ndarray) -> np.ndarray:
    """Forward fill NaN down the rows (days)."""
    idx = np.where(np.isfinite(a), np.arange(a.shape[0])[:, None], 0)
    np.maximum.accumulate(idx, axis=0, out=idx)
    out = a[idx, np.arange(a.shape[1])[None, :]]
    return out


def schedule(n_days: int, dec: np.ndarray, skip: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Decision rows that have a full holding period: (decision, base, end) indices."""
    dec = dec[dec + skip < n_days]
    base = dec + skip
    end = np.r_[base[1:], n_days]
    keep = end < n_days
    return dec[keep], base[keep], end[keep]


@dataclass
class IC:
    mean: float
    t: float
    pos: float
    first: float
    second: float
    dates: int
    breadth: float  # mean number of assets per date


def ic_stats(
    px: np.ndarray,
    elig: np.ndarray,
    sig: np.ndarray,
    dec: np.ndarray,
    skip: int,
    min_assets: int = 10,
) -> IC:
    d, b, e = schedule(px.shape[0], dec, skip)
    fr = fwd_logret(px, b, e)
    ics, ns = [], []
    for k in range(len(d)):
        m = elig[d[k]] & np.isfinite(sig[d[k]]) & np.isfinite(fr[k])
        if m.sum() >= min_assets:
            v = spearman(sig[d[k], m], fr[k, m])
            if np.isfinite(v):
                ics.append(v)
                ns.append(m.sum())
    x = np.array(ics)
    if len(x) < 10:
        return IC(np.nan, np.nan, np.nan, np.nan, np.nan, len(x), np.nan)
    h = len(x) // 2
    t = float(x.mean() / x.std(ddof=1) * np.sqrt(len(x)))
    return IC(
        float(x.mean()),
        t,
        float((x > 0).mean()),
        float(x[:h].mean()),
        float(x[h:].mean()),
        len(x),
        float(np.mean(ns)),
    )


def _weights(mask: np.ndarray, slot: float) -> np.ndarray:
    return np.where(mask, slot, 0.0)


def top_mask(sig: np.ndarray, m: np.ndarray, frac: float = 1 / 3) -> np.ndarray:
    """Top `frac` of the assets in `m` by signal (at least one)."""
    out = np.zeros_like(m)
    idx = np.flatnonzero(m)
    k = max(1, int(round(len(idx) * frac)))
    if len(idx):
        out[idx[np.argsort(-sig[idx], kind="mergesort")[:k]]] = True
    return out


def simulate(
    px: np.ndarray, targets: np.ndarray, base: np.ndarray, cost: np.ndarray, first_day: int
) -> np.ndarray:
    """Daily returns from `first_day + 1` on, given target weights reset at the close of each
    `base` day. `cost` is the cost per side per asset (fraction). Missing prices: no return."""
    n_days = px.shape[0]
    filled = ffill(px)
    r = np.zeros_like(filled)
    with np.errstate(invalid="ignore", divide="ignore"):
        r[1:] = filled[1:] / filled[:-1] - 1
    r[~np.isfinite(r)] = 0.0
    out = np.zeros(n_days)
    w = np.zeros(px.shape[1])
    reset = {int(b): k for k, b in enumerate(base)}
    for t in range(first_day, n_days):
        if t > first_day:
            g = w * (1 + r[t])
            port = w.sum()
            out[t] = g.sum() - port  # return on the account (cash earns 0)
            tot = 1 + out[t]
            w = g / tot if tot > 0 else g * 0
        k = reset.get(t)
        if k is not None:
            new = targets[k]
            c = float((np.abs(new - w) * cost).sum())
            out[t] = (1 + out[t]) * (1 - c) - 1
            w = new.copy()
    return out[first_day + 1 :]


@dataclass
class Tilt:
    first: int  # index of the first day with a return (first base day + 1)
    ew: np.ndarray
    top: np.ndarray
    ts: np.ndarray
    top_ts: np.ndarray
    turnover: dict[str, float]


def tilt(
    px: np.ndarray,
    elig: np.ndarray,
    sig: np.ndarray,
    up: np.ndarray,
    dec: np.ndarray,
    skip: int,
    cost: np.ndarray,
    frac: float = 1 / 3,
    min_assets: int = 10,
) -> Tilt:
    """The four long-only books of the card. `up` = the 365-day return is positive (bool)."""
    d, b, _ = schedule(px.shape[0], dec, skip)
    n = px.shape[1]
    tg = {k: np.zeros((len(d), n)) for k in ("ew", "top", "ts", "top_ts")}
    ok = np.zeros(len(d), bool)
    for k in range(len(d)):
        m = elig[d[k]] & np.isfinite(sig[d[k]]) & np.isfinite(px[b[k]])
        if m.sum() < min_assets:
            continue
        ok[k] = True
        top = top_mask(sig[d[k]], m, frac)
        tg["ew"][k] = _weights(m, 1 / m.sum())
        tg["ts"][k] = _weights(m & up[d[k]], 1 / m.sum())
        tg["top"][k] = _weights(top, 1 / top.sum())
        tg["top_ts"][k] = _weights(top & up[d[k]], 1 / top.sum())
    first_k = int(np.argmax(ok))
    d, b = d[first_k:], b[first_k:]
    out = {}
    turn = {}
    years = (px.shape[0] - b[0]) / 365
    for name, t in tg.items():
        t = t[first_k:]
        out[name] = simulate(px, t, b, cost, int(b[0]))
        turn[name] = float(np.abs(np.diff(t, axis=0)).sum() / years) if len(t) > 1 else 0.0
    return Tilt(int(b[0]) + 1, out["ew"], out["top"], out["ts"], out["top_ts"], turn)


# rolling helpers (NaN-aware), used by breadth_books


def roll_mean(a: np.ndarray, w: int, min_frac: float = 0.8) -> np.ndarray:
    """Mean of the last `w` rows including the current one; NaN if fewer than min_frac*w known."""
    ok = np.isfinite(a)
    x = np.where(ok, a, 0.0)
    cs = np.cumsum(np.vstack([np.zeros((1, a.shape[1])), x]), axis=0)
    cn = np.cumsum(np.vstack([np.zeros((1, a.shape[1])), ok]), axis=0)
    s = cs[w:] - cs[:-w]
    n = cn[w:] - cn[:-w]
    out = np.full(a.shape, np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        out[w - 1 :] = np.where(n >= min_frac * w, s / n, np.nan)
    return out


def roll_std(a: np.ndarray, w: int) -> np.ndarray:
    m = roll_mean(a, w)
    m2 = roll_mean(a * a, w)
    return np.sqrt(np.maximum(m2 - m * m, 0.0))


def roll_corr(a: np.ndarray, b: np.ndarray, w: int) -> np.ndarray:
    """Rolling correlation of each column of `a` with the vector `b` (same rows)."""
    bb = np.broadcast_to(b[:, None], a.shape)
    both = np.isfinite(a) & np.isfinite(bb)
    a2, b2 = np.where(both, a, np.nan), np.where(both, bb, np.nan)
    ma, mb = roll_mean(a2, w), roll_mean(b2, w)
    cov = roll_mean(a2 * b2, w) - ma * mb
    va, vb = roll_mean(a2 * a2, w) - ma * ma, roll_mean(b2 * b2, w) - mb * mb
    with np.errstate(invalid="ignore", divide="ignore"):
        return cov / np.sqrt(np.maximum(va, 1e-30) * np.maximum(vb, 1e-30))


def roll_median(a: np.ndarray, w: int, chunk: int = 64) -> np.ndarray:
    out = np.full(a.shape, np.nan, dtype=np.float32)
    for j in range(0, a.shape[1], chunk):
        v = np.lib.stride_tricks.sliding_window_view(a[:, j : j + chunk].astype(np.float32), w, 0)
        n = np.isfinite(v).sum(-1)
        with np.errstate(all="ignore"):
            import warnings

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                med = np.nanmedian(v, axis=-1)
        out[w - 1 :, j : j + chunk] = np.where(n >= 0.8 * w, med, np.nan)
    return out.astype(float)


def lag(a: np.ndarray, k: int) -> np.ndarray:
    out = np.full(a.shape, np.nan)
    if k < a.shape[0]:
        out[k:] = a[:-k] if k else a
    return out


def logret(px: np.ndarray, a: int, b: int) -> np.ndarray:
    """log(px[t - b] / px[t - a]) for every row t."""
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.log(lag(px, b) / lag(px, a))
