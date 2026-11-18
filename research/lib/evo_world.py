"""Synthetic worlds for evo-1 (research/evo-1.md, "Controls" and "Bar 3, replaced").

A world is built from the real train bars of the six assets and of the S&P 500 index (cut at
1993-01-28, from 1961, the fitness window's warm-up). Each asset's (overnight, open-to-close)
log-return pairs are redrawn, independently per asset with a fixed seed per world and asset:

- `shuffle` (the controls): a plain permutation in time;
- `block` (the replay worlds of bar 3): a stationary bootstrap, mean block 20 bars, wrap-around.

Then the pairs are shifted so the asset's total log return is zero (the shift is taken off the
open-to-close part), calendars and start dates stay, and prices are rebuilt from the first real
bar. Highs and lows are max/min of open and close (no input uses them), volumes stay.

`plant(world, k)` adds the card's planted rule `H` = `mom(91) > 0 and lvol(365) > lvol(30)`:
each Friday its state is read from the synthetic closes visible at the decision, and the
open-to-close log return of every bar that opens after that decision, up to the next one, gets
`+k s` when `H` holds and `-k s` when not (`s` = the asset's real daily log-return sd). A rule
deciding on that Friday fills at those opens, so the plant can be earned by trading `H`.
"""

from __future__ import annotations

import bisect
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date

import numpy as np
import stats
from evo_feat import bars as lookback_bars
from evo_score import fridays_between
from harness import SYMS, decide_time, load_history

from grimstrade.data import UNIVERSE, Bar, close_time, open_time

GSPC_FIRST_YEAR, GSPC_LAST = 1961, date(1993, 1, 28)
ASSETS = (*SYMS, "GSPC")  # the seed of an asset is its place here
MEAN_BLOCK = 20


@dataclass
class World:
    """Six-asset bars and index bars of one world, with the real daily sd per asset."""

    six: dict[str, list[Bar]]
    gspc: dict[str, list[Bar]]
    sd: dict[str, float]
    label: str


def load_real() -> World:
    """The real train bars the worlds are built from (never the held-out period)."""
    six = load_history("train", True, SYMS)
    idx = load_history("train", True, ["GSPC"])["GSPC"]
    gspc = {"GSPC": [b for b in idx if b.date.year >= GSPC_FIRST_YEAR and b.date <= GSPC_LAST]}
    sd = {s: _sd(bars) for s, bars in {**six, **gspc}.items()}
    return World(six, gspc, sd, "real")


def _sd(bars: Sequence[Bar]) -> float:
    cl = np.array([b.close for b in bars])
    return float(np.diff(np.log(cl)).std())


def _pairs(bars: Sequence[Bar]) -> tuple[np.ndarray, np.ndarray]:
    o = np.array([b.open for b in bars])
    cl = np.array([b.close for b in bars])
    return np.log(o[1:] / cl[:-1]), np.log(cl[1:] / o[1:])


def _rebuild(bars: Sequence[Bar], on: np.ndarray, oc: np.ndarray) -> list[Bar]:
    out = [bars[0]]
    px = bars[0].close
    for b, x, y in zip(bars[1:], on, oc, strict=True):
        o = px * math.exp(x)
        px = o * math.exp(y)
        out.append(Bar(b.date, o, max(o, px), min(o, px), px, b.volume))
    return out


def redraw(
    bars: Sequence[Bar], kind: str, rng: np.random.Generator, zero: str = "log"
) -> list[Bar]:
    """One asset's bars with its return pairs redrawn in time and the drift taken out:
    `zero="log"` makes the total log return 0 (the card's replay worlds), `zero="simple"` the
    mean simple close-to-close return 0 (the control worlds since the card note of
    2026-11-18: a zero log drift still pays a holder about half the variance a day)."""
    on, oc = _pairs(bars)
    n = len(on)
    if kind == "shuffle":
        idx = rng.permutation(n)
    elif kind == "block":
        idx = stats._stationary_indices(n, MEAN_BLOCK, rng)
    else:
        raise ValueError(kind)
    on, oc = on[idx], oc[idx]
    if zero == "log":
        oc = oc - (on.sum() + oc.sum()) / n
    elif zero == "simple":
        oc = oc - math.log(float(np.exp(on + oc).mean()))
    else:
        raise ValueError(zero)
    return _rebuild(bars, on, oc)


def world(real: World, kind: str, seed: int, zero: str = "log") -> World:
    """World `seed` of the given kind (`shuffle`: controls 1-3, `block`: replays 101-140)."""

    def one(s: str, bars: list[Bar]) -> list[Bar]:
        return redraw(bars, kind, np.random.default_rng([seed, ASSETS.index(s)]), zero)

    return World(
        {s: one(s, b) for s, b in real.six.items()},
        {s: one(s, b) for s, b in real.gspc.items()},
        dict(real.sd),
        f"{kind} {seed}" + (" zero-mean" if zero == "simple" else ""),
    )


def h_state(dates: np.ndarray, log_close: np.ndarray, s: str) -> bool:
    """`H` on the closes visible at a decision, as `evo_feat` computes its inputs: the 91-day
    log return is positive (the volatility scale is positive whenever it is defined) and the
    365-day realised volatility is above the 30-day one (both need their full window)."""
    if len(log_close) < 2:
        return False
    target = dates[-1] - 91
    if dates[0] > target:
        return False
    i = int(np.searchsorted(dates, target, side="right")) - 1
    if not log_close[-1] - log_close[i] > 0:
        return False
    lr = np.diff(log_close)
    b_long, b_short = lookback_bars(s, 365), lookback_bars(s, 30)
    if len(lr) < b_long:
        return False
    rv_long = float((lr[-b_long:] ** 2).mean())
    rv_short = float((lr[-b_short:] ** 2).mean())
    if not (rv_long > 0 and rv_short > 0):
        return False
    return rv_long > rv_short


def _plant_one(bars: list[Bar], s: str, k: float, sd: float, fridays: list[date]) -> list[Bar]:
    on, oc = _pairs(bars)
    oc = oc.copy()
    cls = UNIVERSE[s]
    dates = np.array([b.date.toordinal() for b in bars], dtype=np.int64)
    closes = [close_time(cls, b.date) for b in bars]
    opens = [open_time(cls, b.date) for b in bars]
    taus = [decide_time(f) for f in fridays]
    first = math.log(bars[0].close)
    for t, tau in enumerate(taus):
        n = bisect.bisect_right(closes, tau)
        lc = first + np.concatenate([[0.0], np.cumsum(on[: n - 1] + oc[: n - 1])])
        hold = n >= 1 and h_state(dates[:n], lc[:n], s)
        lo = bisect.bisect_right(opens, tau)  # first bar opening after the decision
        hi = bisect.bisect_right(opens, taus[t + 1]) if t + 1 < len(taus) else len(bars)
        # bar b's open-to-close part is oc[b - 1]
        a, z = max(lo, 1), max(hi, 1)
        if z > a:
            oc[a - 1 : z - 1] += (k if hold else -k) * sd
    return _rebuild(bars, on, oc)


def plant(w: World, k: float) -> World:
    """The world with `H`'s edge of strength `k` planted into every asset."""

    def one(s: str, bars: list[Bar]) -> list[Bar]:
        fr = fridays_between(bars[0].date, bars[-1].date)
        return _plant_one(bars, s, k, w.sd[s], fr)

    return World(
        {s: one(s, b) for s, b in w.six.items()},
        {s: one(s, b) for s, b in w.gspc.items()},
        dict(w.sd),
        f"{w.label} plant k={k:g}",
    )


H_RULE = (
    "slot",
    (
        "if",
        ("and", ("gtc", ("mom", 91), 0.0), ("gt", ("lvol", 365), ("lvol", 30))),
        ("const", 1.0),
        ("const", 0.0),
    ),
)


def total_logret(bars: Mapping[str, Sequence[Bar]]) -> dict[str, float]:
    return {s: math.log(b[-1].close / b[0].close) for s, b in bars.items()}
