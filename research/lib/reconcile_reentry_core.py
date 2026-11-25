"""reentry-reconcile-1 engine: `e4` against the fast re-entry rules on the same series and
regimes. Card: research/cards/reentry-reconcile-1.md. numpy only; no data access (see
`reconcile_reentry.py`).

Every rule's position gap to `tsmom12` (h12 in {0, 1}) splits exactly:

    h - h12 = (1 - h12) h          buy-back component (held while `tsmom12` is out)
            + h12 (h - 1)          trim component (held less while `tsmom12` is in)

and so does the return gap before costs. Regimes, the zigzag and the split d = return part +
risk part are e4-anatomy-1's code (`e4anatomy_core`), unchanged.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field

import e4anatomy_core as ec
import numpy as np
import pooled1_core as pc

LOGGED = ("e4", "or3-12", "arm3-12")
WS = (0.25, 0.5, 0.75)
COMPS = ("buyback", "trim")


def components(h: np.ndarray, h12: np.ndarray) -> dict[str, np.ndarray]:
    """The exact split of h - h12 (h12 must be 0 or 1)."""
    return {"buyback": (1.0 - h12) * h, "trim": h12 * (h - 1.0)}


def sleeve(h: np.ndarray, h12: np.ndarray, w: float) -> np.ndarray:
    """h12 + w (h - h12): the rule's gap to `tsmom12` at part size w (w = 1 is the rule)."""
    return h12 + w * (h - h12)


def e4_parts(h_e4: np.ndarray, h12: np.ndarray) -> dict[str, np.ndarray]:
    """`e4-re` (buy-back only, full while `tsmom12` is in) and `e4-trim` (trims only)."""
    return {"e4-re": h12 + (1.0 - h12) * h_e4, "e4-trim": h12 * h_e4}


@dataclass
class Market:
    name: str
    group: str
    d: np.ndarray
    px: np.ndarray
    start: int
    h: dict[str, np.ndarray]  # daily held positions: tsmom12, e4, or3-12, arm3-12
    weeks: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=np.int64))
    inv: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=np.int64))
    last: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=np.int64))
    labels: dict[str, np.ndarray] = field(default_factory=dict)


def market(
    name: str, group: str, d: np.ndarray, px: np.ndarray, readings: Mapping[str, tuple[float, int]]
) -> Market:
    """pooled-1's decisions and held positions, and e4-anatomy-1's weekly regime labels."""
    dec = pc.decide(d, px)
    if dec.first_ok < 0:
        raise ValueError(f"{name}: never eligible")
    n = len(px)
    h = {r: pc.held(n, dec.at[r]) for r in ("tsmom12", *LOGGED)}
    start = dec.first_ok + 1 + pc.LAG
    m = Market(name, group, d, px, start, h)
    uniq, inv = ec.week_keys(d, start)
    m.weeks, m.inv = uniq, inv
    last = np.zeros(len(uniq), dtype=np.int64)
    np.maximum.at(last, inv, np.arange(start, n))
    m.last = last
    lg = ec.decide_legs(d, px, d)
    if lg.first_ok != dec.first_ok:
        raise AssertionError(f"{name}: e4-anatomy and pooled-1 disagree on the first decision")
    fri = np.array(lg.fri, dtype=np.int64)
    sig = np.array(lg.sig12)
    for rd, (thr, half) in readings.items():
        lab = ec.fall_labels(d, px, thr, thr)[last].copy()
        ws = ec.whipsaw(sig, half)
        k = np.searchsorted(fri, uniq, side="right") - 1
        wk = np.where(k >= 0, ws[np.clip(k, 0, None)], False)
        lab[(lab == ec.CALMC) & wk] = ec.WHIPC
        m.labels[rd] = lab
    return m


def bar_of(px: np.ndarray) -> np.ndarray:
    b = np.zeros(len(px))
    b[1:] = px[1:] / px[:-1] - 1
    return b


def wsum(m: Market, x: np.ndarray) -> np.ndarray:
    out = np.zeros(len(m.weeks))
    np.add.at(out, m.inv, x[m.start :])
    return out


def wmean(m: Market, x: np.ndarray) -> np.ndarray:
    cnt = np.zeros(len(m.weeks))
    np.add.at(cnt, m.inv, 1.0)
    return wsum(m, x) / cnt


def buyback_size(m: Market, h: np.ndarray) -> float:
    """Mean over scored weeks of the weekly mean buy-back position (1 - h12) h."""
    return float(wmean(m, (1.0 - m.h["tsmom12"]) * h).mean())


def series(m: Market, rule: str, h: np.ndarray, cost: float = pc.COST) -> ec.Series:
    """One rule as an e4-anatomy `Series` against `tsmom12`, legs = the two components, the
    cost term and the weekly compounding residual (sum = r_rule - r_ts exactly)."""
    h12 = m.h["tsmom12"]
    bar = bar_of(m.px)
    f, w_r = pc.weekly(m.d, pc.returns(m.px, h, cost), m.start)
    _, w_t = pc.weekly(m.d, pc.returns(m.px, h12, cost), m.start)
    assert np.array_equal(f, m.weeks)
    legs = {k: wsum(m, v * bar) for k, v in components(h, h12).items()}
    legs["cost"] = wsum(
        m, -cost * np.abs(np.diff(h, prepend=0.0)) + cost * np.abs(np.diff(h12, prepend=0.0))
    )
    legs["resid"] = (w_r - w_t) - sum(legs.values())
    s = ec.Series(f"{m.name}:{rule}", m.group, "w", f, w_r, w_t, legs, wmean(m, h - h12))
    s.labels = dict(m.labels)
    return s


def comp_size_by_regime(m: Market, h: np.ndarray, reading: str) -> dict[str, dict[str, float]]:
    """Mean component position by merged regime (time-weighted over weeks)."""
    lab = m.labels[reading]
    out: dict[str, dict[str, float]] = {}
    for k, v in components(h, m.h["tsmom12"]).items():
        wk = wmean(m, v)
        per = {}
        for c, nm in enumerate(ec.REGIMES):
            sel = lab == c
            per[nm] = (float(wk[sel].sum()), int(sel.sum()))
        merged = {
            "fast": per["fast"],
            "slow": (
                per["slow-medium"][0] + per["slow-long"][0],
                per["slow-medium"][1] + per["slow-long"][1],
            ),
            "rebound": per["rebound"],
            "whipsaw": per["whipsaw"],
            "calm": per["calm"],
        }
        out[k] = {r: (s / n if n else math.nan) for r, (s, n) in merged.items()}
    return out


# --------------------------------------------------------------------------- episodes


@dataclass
class Episode:
    market: str
    group: str
    peak: int  # index of the peak session
    trough: int
    end: int  # last rebound session
    days: int  # calendar days peak -> trough
    dI: float  # log points, rule minus `tsmom12`, net of costs, over (peak, trough]
    dB: float  # the same over (trough, end]
    comp_I: dict[str, float]  # simple points before costs, by component
    comp_B: dict[str, float]

    @property
    def dN(self) -> float:
        return self.dI + self.dB


def windows(d: np.ndarray, px: np.ndarray, down: float, up: float) -> list[tuple[int, int, int]]:
    """(peak, trough, rebound end) per confirmed zigzag fall, the windows of
    `e4anatomy_core.fall_labels`: fall (peak, trough], rebound (trough, min(trough + 365
    days, next peak)]."""
    pairs, open_pk = ec.zigzag(px, down, up)
    peaks = [a for a, _ in pairs[1:]] + ([open_pk] if open_pk is not None else [])
    out = []
    for j, (a, b) in enumerate(pairs):
        e = int(np.searchsorted(d, int(d[b]) + ec.REBOUND, side="right")) - 1
        if j < len(peaks):
            e = min(e, peaks[j])
        out.append((a, b, e))
    return out


def episodes(m: Market, h: np.ndarray, down: float = 0.25, cost: float = pc.COST) -> list[Episode]:
    """Every 25% fall whose whole fall lies in the scored span (peak index >= start - 1)."""
    h12 = m.h["tsmom12"]
    lr = np.log1p(pc.returns(m.px, h, cost)) - np.log1p(pc.returns(m.px, h12, cost))
    bar = bar_of(m.px)
    comp = {k: v * bar for k, v in components(h, h12).items()}
    out = []
    for a, b, e in windows(m.d, m.px, down, down):
        if a + 1 < m.start:
            continue
        fall, reb = slice(a + 1, b + 1), slice(b + 1, e + 1)
        out.append(
            Episode(
                m.name,
                m.group,
                a,
                b,
                e,
                int(m.d[b] - m.d[a]),
                100 * float(lr[fall].sum()),
                100 * float(lr[reb].sum()),
                {k: 100 * float(v[fall].sum()) for k, v in comp.items()},
                {k: 100 * float(v[reb].sum()) for k, v in comp.items()},
            )
        )
    return out


def episode_pool(eps: list[Episode]) -> dict[str, float]:
    if not eps:
        return {"n": 0}
    dI = float(np.mean([e.dI for e in eps]))
    dB = float(np.mean([e.dB for e in eps]))
    dN = dI + dB
    out = {
        "n": len(eps),
        "dI": dI,
        "dB": dB,
        "dN": dN,
        "K": dN / dB if dB != 0 else math.nan,
        "share_dN_pos": float(np.mean([e.dN > 0 for e in eps])),
        "share_dB_pos": float(np.mean([e.dB > 0 for e in eps])),
    }
    for k in COMPS:
        out[f"{k}_I"] = float(np.mean([e.comp_I[k] for e in eps]))
        out[f"{k}_B"] = float(np.mean([e.comp_B[k] for e in eps]))
    return out


def efficiency(rebound: float, slow: float) -> float:
    """Buy-back gain per unit of bear-rally cost; NaN ("no cost") if the slow term >= 0."""
    return rebound / -slow if slow < 0 else math.nan
