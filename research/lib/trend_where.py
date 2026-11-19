"""Rule of research run trend-where, exactly as fixed on the card (research/trend-where.md).

Each January an asset keeps its `tsmom12` filter only if, on its own past, the bars the rule was
out were rougher than the bars it was in; otherwise its slot is simply held.

Everything is causal: a refit reads only bars visible at its own decision time.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import common as c
import numpy as np
import trend_tune as tt
from harness import Panel, ResearchStrategy, View, Weights, decide_time

MIN_YEARS = 5.0  # below this much eligible history the filter stays on
MIN_BARS = 60  # fewer out bars or in bars than this: the filter stays on
MODES = ("vol", "dd")


@dataclass
class InOut:
    """Per bar of one asset: `ok[i]` the asset was eligible at the Friday whose signal bar i
    uses, `on[i]` that `tsmom12` signal, `bar[i]` the close-to-close return. Entry i depends
    only on bars 0..i."""

    ord: np.ndarray
    ok: np.ndarray
    on: np.ndarray
    bar: np.ndarray
    per_year: int


def in_out(panel: Panel, s: str) -> InOut:
    key = ("tw-inout", s)
    if key in panel.cache:
        return panel.cache[key]  # type: ignore[return-value]
    dts, px = panel.ord[s], panel.c[s]
    n = len(px)
    ok = np.zeros(n, dtype=bool)
    on = np.zeros(n, dtype=bool)
    if n:
        first = date.fromordinal(int(dts[0]))
        fri = first + timedelta(days=(tt.FRIDAY - first.weekday()) % 7)
        last = date.fromordinal(int(dts[-1]))
        while fri < last:
            view = panel.view(decide_time(fri))
            # bars this Friday's signal is applied to: dates after it, up to the next Friday
            lo = int(np.searchsorted(dts, fri.toordinal(), side="right"))
            hi = int(np.searchsorted(dts, fri.toordinal() + 7, side="right"))
            if c.eligible(view, s):
                ok[lo:hi] = True
                on[lo:hi] = tt.signal(view, s, 12)
            fri += timedelta(days=7)
    bar = np.zeros(n)
    bar[1:] = px[1:] / px[:-1] - 1
    out = InOut(dts, ok, on, bar, c.bpy(s))
    panel.cache[key] = out
    return out


def worst_fall(r: np.ndarray) -> float:
    """Deepest peak-to-trough fall of the chained returns (0.3 = 30%)."""
    if len(r) == 0:
        return 0.0
    eq = np.concatenate([[1.0], np.cumprod(1 + r)])
    return float((1 - eq / np.maximum.accumulate(eq)).max())


def rough(r: np.ndarray, mode: str) -> float:
    return float(r.std()) if mode == "vol" else worst_fall(r)


@dataclass
class Evidence:
    years: float
    n_out: int
    n_in: int
    out: float
    inn: float
    keep: bool


class Where:
    """Walk-forward yes/no per asset: keep the `tsmom12` filter (yes) or hold the slot (no)."""

    def __init__(self, mode: str, min_years: float = MIN_YEARS, min_bars: int = MIN_BARS):
        if mode not in MODES:
            raise ValueError(mode)
        self.mode = mode
        self.min_years = min_years
        self.min_bars = min_bars
        self.token = object()

    def evidence(self, panel: Panel, s: str, refit: date) -> Evidence:
        """What the refit sees for one asset: only bars visible at the refit's decision."""
        k = panel.view(decide_time(refit)).n[s]
        io = in_out(panel, s)
        ok, on, bar = io.ok[:k], io.on[:k], io.bar[:k]
        r_out, r_in = bar[ok & ~on], bar[ok & on]
        years = float(ok.sum()) / io.per_year
        thin = years < self.min_years or min(len(r_out), len(r_in)) < self.min_bars
        a = rough(r_out, self.mode) if len(r_out) else 0.0
        b = rough(r_in, self.mode) if len(r_in) else 0.0
        return Evidence(years, len(r_out), len(r_in), a, b, thin or a > b)

    def answers(self, panel: Panel, refit: date) -> dict[str, bool]:
        key = (self.token, "answer", refit)
        if key not in panel.cache:
            panel.cache[key] = {s: self.evidence(panel, s, refit).keep for s in panel.syms}  # type: ignore[assignment]
        return panel.cache[key]  # type: ignore[return-value]

    def strategy(self) -> ResearchStrategy:
        def f(view: View) -> Weights:
            day = tt.last_friday(view.today)
            key = (self.token, day)
            memo = view.panel.cache
            if key not in memo:
                v = view if day == view.today else view.at(day)
                keep = self.answers(view.panel, tt.refit_of(day))
                held = c.live(v)
                memo[key] = {  # type: ignore[assignment]
                    s: 1 / len(held) for s in held if (not keep[s]) or tt.signal(v, s, 12)
                }
            return memo[key]  # type: ignore[return-value]

        return f
