"""The 72 inputs of the evo-1 grammar per Friday decision (research/evo-1.md, "The grammar"), as
the arrays `evo_gp.evaluate` takes. Every number is computed from `harness.Panel.view` at the
decision time, so it can only see bars closed before the decision. The fast scorer is not here
yet.

Choices the card left open (2026-11-18): realised volatility is the root mean square of the
last `b(h)` daily log returns (zero mean, like `common.ewma_vol`), annualised on the asset's own
clock; `volcap`'s 30-day volatility is that number for h = 30; ranks give ties the middle rank;
cross-asset inputs use the eligible assets for which the number is defined.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import date

import common as c
import evo_gp as gp
import numpy as np
from harness import Panel, View, decide_time

from grimstrade.data import CRYPTO, UNIVERSE

ETF_BARS = dict(zip(gp.LOOKBACKS, (5, 10, 21, 42, 63, 126, 200, 252), strict=True))


def bars(s: str, h: int) -> int:
    """`h` calendar days on the asset's own clock."""
    return h if UNIVERSE[s] == CRYPTO else ETF_BARS[h]


def _own(view: View, s: str) -> dict[tuple[str, int], float]:
    """The inputs that need only the asset's own bars: mom, gap, dd, lvol (NaN if undefined)."""
    out: dict[tuple[str, int], float] = {}
    close, lr = view.close(s), view.logret(s)
    vs = c.vol_series(view, s, 60)
    vref = float(vs[-1]) if len(vs) else math.nan
    ok = vref > 0
    for h in gp.LOOKBACKS:
        b = bars(s, h)
        scale = vref * math.sqrt(h / 365) if ok else math.nan
        out[("mom", h)] = c.trailing_logret(view, s, h) / scale
        if len(close) >= b:
            out[("gap", h)] = math.log(close[-1] / close[-b:].mean()) / scale
            out[("dd", h)] = math.log(close[-1] / close[-b:].max()) / scale
        else:
            out[("gap", h)] = out[("dd", h)] = math.nan
        rv = math.sqrt(float((lr[-b:] ** 2).mean()) * c.bpy(s)) if len(lr) >= b else 0.0
        out[("lvol", h)] = math.log(rv) if rv > 0 else math.nan
    out[("vref", 0)] = vref if ok else math.nan
    return out


def _rank(x: np.ndarray) -> np.ndarray:
    """Rank from 0 to 1 among the defined entries (ties: the middle; 0.5 when alone)."""
    out = np.full(len(x), np.nan)
    good = ~np.isnan(x)
    n = int(good.sum())
    for i in np.flatnonzero(good):
        if n == 1:
            out[i] = 0.5
        else:
            less = (x[good] < x[i]).sum()
            same = (x[good] == x[i]).sum() - 1
            out[i] = (less + 0.5 * same) / (n - 1)
    return out


def friday_feats(panel: Panel, fridays: Sequence[date]) -> tuple[gp.Feats, np.ndarray]:
    """Inputs and the eligibility mask, one row per decision date, one column per asset."""
    syms = panel.syms
    shape = (len(fridays), len(syms))
    feats: gp.Feats = {inp: np.full(shape, np.nan) for inp in gp.INPUTS}
    feats["vol30"] = np.full(shape, np.nan)
    feats["coin"] = np.array([UNIVERSE[s] == CRYPTO for s in syms])
    elig = np.zeros(shape, dtype=bool)
    for t, d in enumerate(fridays):
        view = panel.view(decide_time(d))
        live = [j for j, s in enumerate(syms) if c.eligible(view, s)]
        if not live:
            continue
        elig[t, live] = True
        own = [_own(view, syms[j]) for j in live]
        for h in gp.LOOKBACKS:
            mom = np.array([o[("mom", h)] for o in own])
            lvol = np.array([o[("lvol", h)] for o in own])
            vref = np.array([o[("vref", 0)] for o in own])
            for name in ("mom", "gap", "dd", "lvol"):
                feats[(name, h)][t, live] = [o[(name, h)] for o in own]
            known = ~np.isnan(mom)
            if known.any():
                feats[("univ", h)][t, live] = mom[known].mean()
                feats[("breadth", h)][t, live] = (mom[known] > 0).mean()
            feats[("rank", h)][t, live] = _rank(mom)
            feats[("vrank", h)][t, live] = _rank(lvol)
            both = ~np.isnan(lvol) & ~np.isnan(vref)
            if both.any():
                feats[("vbreadth", h)][t, live] = (np.exp(lvol[both]) > vref[both]).mean()
            if h == 30:
                feats["vol30"][t, live] = np.exp(lvol)
    return feats, elig
