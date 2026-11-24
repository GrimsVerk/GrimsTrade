"""ownvol-anatomy-1 engine: where own-vol's lead (or loss) over `tsmom12` comes from.
Card: research/cards/ownvol-anatomy-1.md. numpy only; no data access (see `ownvolanatomy.py`).

A descriptive re-score: the own-vol loops of pooled-1 / pooled-2 replayed step for step to record
the share, plus a fixed-share twin F on the same resets. Per series, exactly:

    d = SR_o - SR_s = E + M + R
    E = SR_f - SR_s                              exposure (a fixed share, same average exposure)
    M = (mu_o - mu_f) / sd_o * sqrt(P)           timing, mean channel
    R = mu_f * (1 / sd_o - 1 / sd_f) * sqrt(P)   timing, risk channel

and each term is a sum of one term per period, so any partition of the periods splits it exactly.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from typing import Any

import numpy as np
import pooled1_core as pc

Window = Callable[[int, int], bool]
TARGET = 0.70
FAST, MEDIUM, REBOUND = 92, 365, 365  # insure-1: calendar days
ENTRY_DAYS, ENTRY_MONTHS = 182, 6  # trend phase: first 26 weeks / 6 months after an entry
WHIP_HALF = {"w": 13, "m": 3, "d": 91}  # periods on either side (13 weeks, 3 months)
TERMS = ("E", "M", "R")
REGIMES = ("fast", "slow", "rebound", "whipsaw", "calm")
FASTC, SLOWC, REBC, WHIPC, CALMC = range(5)
VOLSTATE = ("out", "warm-up", "low share", "mid share", "high share")
PHASE = ("entry", "held", "out")
READINGS = ("A", "B", "C")
PARTS: dict[str, tuple[str, ...]] = {
    "A": REGIMES,
    "B": REGIMES,
    "C": REGIMES,
    "vol": VOLSTATE,
    "phase": PHASE,
}


# --------------------------------------------------------------------------- replays


def book_weekly(
    d: np.ndarray,
    x: np.ndarray,
    g: np.ndarray,
    start: int,
    target: float = TARGET,
    skip: int = 0,
    reset_cost: float = pc.RESET_COST,
    fixed: float | None = None,
) -> tuple[np.ndarray, np.ndarray, int, list[tuple[int, float]]]:
    """`pooled1_core.own_vol` (skip 0) / `pooled2_core.own_vol_weekly` step for step, also
    returning the share v[k] held over return k, the first sized reset index (n if none) and
    (reset index, sigma) pairs after the warm-up. With `fixed`, every reset sets that share."""
    n = len(x)
    out = np.zeros(n)
    share = np.full(n, np.nan)
    seen: list[float] = []
    sig_at: list[tuple[int, float]] = []
    sized = n
    v = target if fixed is None else fixed
    for k in range(start, n):
        cost = 0.0
        new_month = k > start and (
            date.fromordinal(int(d[k])).month != date.fromordinal(int(d[k - 1])).month
        )
        if new_month:
            if fixed is not None:
                a = fixed
            else:
                sg = _sigma_w(d, x, k, start, skip)
                if math.isfinite(sg) and sg > 0:
                    seen.append(sg)
                if len(seen) < pc.WARMUP or not math.isfinite(sg):
                    a = target
                elif sg == 0:
                    a = v
                else:
                    a = min(1.0, pc.solve_k(seen, target) / sg)
                    sized = min(sized, k)
                    sig_at.append((k, sg))
            cost = reset_cost * abs(a - v) * g[k]
            v = a
        share[k] = v
        out[k] = v * x[k] - cost
        n1 = v * (1 + x[k])
        v = n1 / (n1 + 1 - v)
    return out, share, sized, sig_at


def _sigma_w(d: np.ndarray, x: np.ndarray, k: int, start: int, skip: int) -> float:
    if skip == 0:
        return pc.sigma52(d, x, k, start)
    import pooled2_core as qc

    return qc.sigma52_skip(d, x, k, start, skip)


def book_monthly(
    x: np.ndarray,
    g: np.ndarray,
    start: int,
    gap: int,
    target: float = TARGET,
    reset_cost: float = pc.RESET_COST,
    window: int = 36,
    fixed: float | None = None,
) -> tuple[np.ndarray, np.ndarray, int, list[tuple[int, float]]]:
    """`pooled2_core.own_vol_monthly` step for step, with the share, first sized month and the
    (month, sigma) pairs after the warm-up; `fixed` as in `book_weekly`."""
    n = len(x)
    out = np.zeros(n)
    share = np.full(n, np.nan)
    seen: list[float] = []
    sig_at: list[tuple[int, float]] = []
    sized = n
    v = target if fixed is None else fixed
    for t in range(start, n):
        cost = 0.0
        if t > start:
            if fixed is not None:
                a = fixed
            else:
                lo, hi = t - gap - window, t - gap
                sg = float(x[lo:hi].std(ddof=1) * math.sqrt(12)) if lo >= start else math.nan
                if math.isfinite(sg) and sg > 0:
                    seen.append(sg)
                if len(seen) < pc.WARMUP or not math.isfinite(sg):
                    a = target
                elif sg == 0:
                    a = v
                else:
                    a = min(1.0, pc.solve_k(seen, target) / sg)
                    sized = min(sized, t)
                    sig_at.append((t, sg))
            cost = reset_cost * abs(a - v) * g[t]
            v = a
        share[t] = v
        out[t] = v * x[t] - cost
        n1 = v * (1 + x[t])
        v = n1 / (n1 + 1 - v)
    return out, share, sized, sig_at


def s_bar(share: np.ndarray, g: np.ndarray, lo: int) -> float:
    """Own-vol's average share while `tsmom12` is invested (gross-weighted), sessions lo.."""
    w = g[lo:]
    return float((share[lo:] * w).sum() / w.sum()) if w.sum() > 0 else TARGET


# --------------------------------------------------------------------------- regimes


def zigzag(px: np.ndarray, down: float, up: float) -> tuple[list[tuple[int, int]], int | None]:
    """insure-1's zigzag, step for step (confirmed (peak, trough) pairs, unfinished peak)."""
    out: list[tuple[int, int]] = []
    falling, pk, tr = False, 0, 0
    for i in range(1, len(px)):
        if not falling:
            if px[i] > px[pk]:
                pk = i
            elif px[i] <= px[pk] * (1 - down):
                falling, tr = True, i
        else:
            if px[i] < px[tr]:
                tr = i
            elif px[i] >= px[tr] * (1 + up):
                out.append((pk, tr))
                falling, pk = False, i
    return out, (pk if falling else None)


def fall_labels(
    ords: np.ndarray, px: np.ndarray, down: float, up: float, rebound_n: int | None = None
) -> np.ndarray:
    """Per point of a level series: fast / slow falls (peak, trough], rebounds (trough,
    min(trough + 365 days, next peak)], calm otherwise (whipsaw added later). `rebound_n`:
    rebound length in points (monthly series)."""
    lab = np.full(len(px), CALMC, dtype=np.int8)
    pairs, open_pk = zigzag(px, down, up)
    peaks = [a for a, _ in pairs[1:]] + ([open_pk] if open_pk is not None else [])
    for j, (a, b) in enumerate(pairs):
        lab[a + 1 : b + 1] = FASTC if int(ords[b] - ords[a]) <= FAST else SLOWC
        if rebound_n is None:
            e = int(np.searchsorted(ords, int(ords[b]) + REBOUND, side="right")) - 1
        else:
            e = min(len(px) - 1, b + rebound_n)
        if j < len(peaks):
            e = min(e, peaks[j])
        lab[b + 1 : e + 1] = REBC
    return lab


def changes(pos: np.ndarray, reversals: bool = False) -> np.ndarray:
    """1 at period i if the position changed from i-1 (or, with `reversals`, if the change has
    the opposite sign of the previous non-zero change: for a fractional gross exposure)."""
    dp = np.diff(pos, prepend=pos[:1])
    if not reversals:
        return (np.abs(dp) > 1e-12).astype(np.int64)
    out = np.zeros(len(pos), dtype=np.int64)
    last = 0.0
    for i, x in enumerate(dp):
        if abs(x) > 1e-12:
            if last != 0.0 and np.sign(x) != np.sign(last):
                out[i] = 1
            last = x
    return out


def whipsaw(ch: np.ndarray, half: int) -> np.ndarray:
    """True at period i if `ch` (0/1 events) sums to >= 2 over periods i-half+1 .. i+half (the
    changes between the decisions i-half .. i+half)."""
    cs = np.concatenate([[0], np.cumsum(ch)])
    n = len(ch)
    idx = np.arange(n)
    lo = np.maximum(0, idx - half)
    hi = np.minimum(n - 1, idx + half)
    return (cs[hi + 1] - cs[lo + 1]) >= 2


def regime_labels(
    fall: np.ndarray, pos_by_period: np.ndarray, freq: str, reversals: bool = False
) -> np.ndarray:
    """Period labels: fall / rebound from `fall` (already per period), whipsaw where the position
    flips, calm otherwise; priority fall > rebound > whipsaw > calm."""
    lab = fall.copy()
    w = whipsaw(changes(pos_by_period, reversals), WHIP_HALF[freq])
    lab[(lab == CALMC) & w] = WHIPC
    return lab


# --------------------------------------------------------------------------- one series


@dataclass
class Series:
    """Scored period returns and labels of one series (o own-vol, f fixed twin, s `tsmom12`)."""

    name: str
    group: str
    freq: str  # "w", "m" or "d" (the six, calendar days)
    o: np.ndarray
    f: np.ndarray
    s: np.ndarray
    month: np.ndarray  # month index (year * 12 + month - 1) of each period
    labels: dict[str, np.ndarray] = field(default_factory=dict)  # partition -> codes
    sbar: float = math.nan
    lev_corr: float = math.nan  # L: return vs change in realised vol of the traded level
    persist: float = math.nan  # corr(sigma at reset, next month's realised sleeve vol)
    x_tercile: dict[str, tuple[float, float]] = field(default_factory=dict)  # (mean, var) a year
    stats: dict[str, tuple[float, float, float]] = field(default_factory=dict)  # sh, cagr, mdd

    @property
    def P(self) -> int:
        return {"w": 52, "m": 12, "d": 365}[self.freq]


def sharpe(x: np.ndarray, P: int) -> float:
    sd = x.std()
    return float(x.mean() / sd * math.sqrt(P)) if sd > 0 else 0.0


def terms(sr: Series) -> dict[str, np.ndarray]:
    """Per-period terms e_t, m_t, r_t (each sums to E, M, R over the periods)."""
    o, f, s, P, T = sr.o, sr.f, sr.s, sr.P, len(sr.o)
    q = math.sqrt(P)
    so, sf, ss = o.std(), f.std(), s.std()
    SRf, SRs = f.mean() / sf * q, s.mean() / ss * q
    e = (f - s) / (T * sf) * q - SRs * ((f - f.mean()) ** 2 - (s - s.mean()) ** 2) / (
        T * sf * (sf + ss)
    )
    m = (o - f) / (T * so) * q
    r = -SRf * ((o - o.mean()) ** 2 - (f - f.mean()) ** 2) / (T * so * (so + sf))
    return {"E": e, "M": m, "R": r}


def split(sr: Series) -> dict[str, Any]:
    """d, E, M, R and each partition's split of them (label -> term -> value)."""
    t = terms(sr)
    out: dict[str, Any] = {
        "d": sharpe(sr.o, sr.P) - sharpe(sr.s, sr.P),
        **{k: float(v.sum()) for k, v in t.items()},
    }
    for part, lab in sr.labels.items():
        names = PARTS[part]
        out[part] = {
            nm: {
                **{k: float(v[lab == c].sum()) for k, v in t.items()},
                "share": float((lab == c).mean()),
            }
            for c, nm in enumerate(names)
        }
    return out


def first_last(keys: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Index of the first and the last session of each period (keys sorted ascending)."""
    _, first = np.unique(keys, return_index=True)
    last = np.concatenate([first[1:] - 1, [len(keys) - 1]])
    return first, last


def vol_state(share_first: np.ndarray, out: np.ndarray, warm: np.ndarray) -> np.ndarray:
    """0 out, 1 warm-up, 2/3/4 low / mid / high-share terciles of the in-market sized periods."""
    lab = np.full(len(share_first), 3, dtype=np.int8)
    lab[warm] = 1
    lab[out] = 0
    sel = ~out & ~warm
    if sel.sum() >= 3:
        q1, q2 = np.quantile(share_first[sel], [1 / 3, 2 / 3])
        lab[sel & (share_first <= q1)] = 2
        lab[sel & (share_first > q2)] = 4
    return lab


def phase_labels(
    end_ord: np.ndarray, out: np.ndarray, entries: np.ndarray, window: Window
) -> np.ndarray:
    """0 entry (in-market, within `window` of the latest entry), 1 held, 2 out. `window` is a
    callable (entry ordinal, period end ordinal) -> bool."""
    lab = np.ones(len(end_ord), dtype=np.int8)
    lab[out] = 2
    for i in range(len(end_ord)):
        if out[i]:
            continue
        j = int(np.searchsorted(entries, end_ord[i], side="right")) - 1
        if j >= 0 and window(int(entries[j]), int(end_ord[i])):
            lab[i] = 0
    return lab


def lev_corr(r: np.ndarray, h: int) -> float:
    """corr(r_t, RV(t+1..t+h) - RV(t-h+1..t)), RV = sqrt(mean of squared returns)."""
    n = len(r)
    if n < 4 * h:
        return math.nan
    c = np.concatenate([[0.0], np.cumsum(r * r)])
    t = np.arange(h - 1, n - h)
    after = np.sqrt((c[t + 1 + h] - c[t + 1]) / h)
    before = np.sqrt((c[t + 1] - c[t + 1 - h]) / h)
    a, b = r[t], after - before
    if a.std() == 0 or b.std() == 0:
        return math.nan
    return float(np.corrcoef(a, b)[0, 1])


def tercile_mv(x: np.ndarray, lab: np.ndarray, P: int) -> dict[str, tuple[float, float]]:
    """Sleeve mean and variance a year in the low- and high-share terciles."""
    out = {}
    for c, nm in ((2, "low share"), (4, "high share")):
        y = x[lab == c]
        out[nm] = (float(y.mean() * P), float(y.var() * P)) if len(y) > 1 else (math.nan,) * 2
    return out


def corr(a: Sequence[float], b: Sequence[float]) -> float:
    x, y = np.asarray(a, float), np.asarray(b, float)
    if len(x) < 6 or x.std() == 0 or y.std() == 0:
        return math.nan
    return float(np.corrcoef(x, y)[0, 1])


def perf(x: np.ndarray, P: int) -> tuple[float, float, float]:
    """(Sharpe, growth a year, worst loss) of period returns."""
    eq = np.cumprod(1 + x)
    g = float(np.exp(np.log1p(x).sum() * P / len(x)) - 1)
    return sharpe(x, P), g, float((1 - eq / np.maximum.accumulate(eq)).max())


# --------------------------------------------------------------------------- pools, bootstrap


def label_index() -> list[tuple[str, str]]:
    """Flattened (partition, label) list; index 0 is the total."""
    return [("total", "total")] + [(p, nm) for p, names in PARTS.items() for nm in names]


@dataclass
class Cal:
    months: np.ndarray  # month index calendar
    C: np.ndarray  # [series, term, label, month] sums of T x per-period term
    N: np.ndarray  # [series, month] period counts
    min_n: np.ndarray  # [series] minimum periods for a series to enter a draw


def month_cells(series: Sequence[Series]) -> Cal:
    li = label_index()
    lo = min(int(s.month.min()) for s in series)
    hi = max(int(s.month.max()) for s in series)
    nm = hi - lo + 1
    C = np.zeros((len(series), len(TERMS), len(li), nm))
    N = np.zeros((len(series), nm))
    for i, s in enumerate(series):
        t = terms(s)
        T = len(s.o)
        idx = s.month - lo
        np.add.at(N[i], idx, 1.0)
        for a, k in enumerate(TERMS):
            v = t[k] * T
            np.add.at(C[i, a, 0], idx, v)
            for j, (p, lab) in enumerate(li[1:], start=1):
                code = PARTS[p].index(lab)
                sel = s.labels[p] == code
                np.add.at(C[i, a, j], idx[sel], v[sel])
    min_n = np.array([{"w": 52, "m": 12, "d": 365}[s.freq] for s in series], dtype=float)
    return Cal(np.arange(lo, hi + 1), C, N, min_n)


def _blocks(a: np.ndarray, length: int) -> np.ndarray:
    nw = a.shape[-1]
    ext = np.concatenate([a, a[..., :length]], axis=-1)
    cs = np.concatenate([np.zeros(a.shape[:-1] + (1,)), np.cumsum(ext, axis=-1)], axis=-1)
    return cs[..., length : length + nw] - cs[..., :nw]  # type: ignore[no-any-return]


def boot(
    cal: Cal, masks: Mapping[str, np.ndarray], block: int = 12, draws: int = 2000, seed: int = 0
) -> dict[str, np.ndarray]:
    """Pool means per draw: {pool: [term, label, draw]}, linearised (means and sds fixed)."""
    nm = cal.N.shape[-1]
    nb = -(-nm // block)
    BC, BN = _blocks(cal.C, block), _blocks(cal.N, block)
    rng = np.random.default_rng(seed)
    out = {k: np.full(cal.C.shape[1:3] + (draws,), np.nan) for k in masks}
    for b in range(draws):
        st = rng.integers(0, nm, nb)
        c = BC[..., st].sum(-1)
        n = BN[..., st].sum(-1)
        ok = n >= cal.min_n
        with np.errstate(invalid="ignore", divide="ignore"):
            est = c / n[:, None, None]
        est[~ok] = np.nan
        for k, m in masks.items():
            sel = m & ok
            if sel.any():
                out[k][..., b] = est[sel].mean(0)
    return out


def pool_point(splits: Sequence[dict[str, Any]], mask: np.ndarray) -> dict[str, Any]:
    """Equal-weight pool mean of each series' split (d, E, M, R and the partitions)."""
    sel = [s for s, m in zip(splits, mask, strict=True) if m]
    out: dict[str, Any] = {k: float(np.mean([s[k] for s in sel])) for k in ("d", *TERMS)}
    for p, names in PARTS.items():
        out[p] = {
            nm: {k: float(np.mean([s[p][nm][k] for s in sel])) for k in (*TERMS, "share")}
            for nm in names
        }
    out["n"] = len(sel)
    return out


def ses(draws: np.ndarray) -> dict[tuple[str, str], dict[str, float]]:
    """SE per (partition, label) and term (plus the M + R timing sum)."""
    out = {}
    for j, key in enumerate(label_index()):
        x = draws[:, j, :]
        row = {k: float(np.nanstd(x[a], ddof=1)) for a, k in enumerate(TERMS)}
        row["timing"] = float(np.nanstd(x[1] + x[2], ddof=1))
        row["d"] = float(np.nanstd(x.sum(0), ddof=1))
        out[key] = row
    return out


# --------------------------------------------------------------------------- readings


def reading_b(D: float, E: float) -> str:
    return "holding less" if abs(E) >= 0.5 * abs(D) else "not holding less"


def carries(D: float, x: float, se: float) -> bool:
    return bool(np.sign(x) == np.sign(D) and abs(x) >= 0.5 * abs(D) and abs(x) > 2 * se)


def reading_a(D: float, M: float, R: float, se_m: float, se_r: float) -> str:
    cm, cr = carries(D, M, se_m), carries(D, R, se_r)
    if cm and cr:
        return "both channels carry"
    if cr:
        return "risk channel carries"
    if cm:
        return "mean channel carries"
    return "within noise"


def reading_d(gap: Mapping[str, float]) -> str:
    """gap = {"D": .., "E": .., "M": .., "R": ..} of equity minus the other pool."""
    g = gap["D"]
    if g == 0:
        return "no gap"
    if gap["M"] / g >= 0.5:
        return "through the mean channel"
    if gap["R"] / g >= 0.5:
        return "through the risk channel"
    return "mixed"
