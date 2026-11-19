"""Rules of research run trend-tune, exactly as fixed on the card (research/trend-tune.md).

- `signal`: the L-month trend signal (`tsmom12` is L = 12, unchanged).
- `fixed`, `both`, `either`, `threshold`: the cells of Part A's sensitivity surface.
- `paper`: the gym-free paper series the tuner scores lookbacks on.
- `Tuner`: the three walk-forward procedures of Part B (`asset`, `pooled`, `shrunk`).

Everything is causal: a decision or a refit reads only bars visible at its own decision time.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, timedelta

import common as c
import numpy as np
from harness import Panel, ResearchStrategy, View, Weights, decide_time

from grimstrade import gym
from grimstrade.data import UNIVERSE

GRID = (3, 6, 9, 12, 15, 18, 24)  # months: the tuning grid of Part B
MIN_YEARS = 5.0  # wf-asset / wf-pooled: below this much paper series, stay at 12 months
PRIOR_YEARS = 20.0  # wf-shrunk: prior strength
HURDLE = 0.10  # wf-shrunk: smallest shrunk Sharpe advantage worth leaving 12 months for
FRIDAY = 4


def days_of(months: int) -> int:
    return round(365 * months / 12)


def lookback_logret(view: View, s: str, months: int) -> float:
    """Log return over the last L months. L = 12 is `tsmom12`'s own 365-day return. For L above
    12, an eligible asset with less history than that uses the return since its first bar."""
    if months == 12:
        return c.trailing_logret(view, s, 365)
    d, px = view.dates(s), view.close(s)
    if len(px) < 2:
        return math.nan
    target = d[-1] - days_of(months)
    if d[0] > target:
        return float(math.log(px[-1] / px[0])) if months > 12 else math.nan
    i = int(np.searchsorted(d, target, side="right")) - 1
    return float(math.log(px[-1] / px[i]))


def signal(view: View, s: str, months: int) -> bool:
    r = lookback_logret(view, s, months)
    return (not math.isnan(r)) and r > 0


def fixed(months: int) -> ResearchStrategy:
    """Equal slots, held while the L-month signal is on (not yet wrapped in a schedule)."""
    return c.slots(lambda view, s: signal(view, s, months))


def both(a: int, b: int) -> ResearchStrategy:
    """AND: held only if both lookbacks are positive (fast exit, slow re-entry)."""
    return c.slots(lambda view, s: signal(view, s, a) and signal(view, s, b))


def either(a: int, b: int) -> ResearchStrategy:
    """OR: held if either lookback is positive (slow exit, fast re-entry)."""
    return c.slots(lambda view, s: signal(view, s, a) or signal(view, s, b))


def per_asset(months: Mapping[str, int]) -> ResearchStrategy:
    """A fixed lookback per asset (12 where none is given)."""
    return c.slots(lambda view, s: signal(view, s, months.get(s, 12)))


def last_friday(today: date) -> date:
    return today - timedelta(days=(today.weekday() - FRIDAY) % 7)


def zscore(view: View, s: str, months: int) -> float:
    """L-month log return in units of the asset's volatility over that horizon (the ML
    protocol's `z(h)` without the clip): 60-bar-half-life EWMA volatility, annualised."""
    r = lookback_logret(view, s, months)
    v = c.vol_series(view, s, 60)
    if math.isnan(r) or len(v) == 0 or v[-1] <= 0:
        return math.nan
    return r / (float(v[-1]) * math.sqrt(days_of(months) / 365))


def threshold(months: int, centre: float, half: float) -> ResearchStrategy:
    """Weekly rule with an entry and an exit threshold on z: enter when z > centre + half, leave
    when z < centre - half, else keep last Friday's state (first state: in if z > centre).
    Handles its own Friday schedule, because the state walks from Friday to Friday."""
    token = object()

    def state(panel: Panel, s: str, day: date) -> bool:
        memo: dict[date, bool] = panel.cache.setdefault((token, s), {})  # type: ignore[assignment]
        todo = []
        d = day
        prev: bool | None = None
        while True:
            if d in memo:
                prev = memo[d]
                break
            v = panel.view(decide_time(d))
            if not c.eligible(v, s):
                break
            todo.append(d)
            d -= timedelta(days=7)
        for d in reversed(todo):
            z = zscore(panel.view(decide_time(d)), s, months)
            if math.isnan(z):
                cur = False
            elif prev is None:
                cur = z > centre
            elif z > centre + half:
                cur = True
            elif z < centre - half:
                cur = False
            else:
                cur = prev
            memo[d] = cur
            prev = cur
        return bool(prev)

    def f(view: View) -> Weights:
        day = last_friday(view.today)
        key = (token, day)
        memo = view.panel.cache
        if key not in memo:
            v = view if day == view.today else view.at(day)
            held = c.live(v)
            memo[key] = {x: 1 / len(held) for x in held if state(view.panel, x, day)}
        return memo[key]  # type: ignore[return-value]

    return f


# --- the paper series (card: "Shared definitions") ---


@dataclass
class Paper:
    """Gym-free paper series of one asset for every grid lookback. Entry i belongs to bar i:
    `ret[L][i]` is the L-month rule's return on that bar, `ok[i]` says the asset was eligible at
    the Friday whose signal the bar uses. Entry i depends only on bars 0..i."""

    ord: np.ndarray
    ok: np.ndarray
    ret: dict[int, np.ndarray]
    per_year: int


def paper(panel: Panel, s: str, grid: tuple[int, ...] = GRID) -> Paper:
    key = ("tt-paper", s, grid)
    if key in panel.cache:
        return panel.cache[key]  # type: ignore[return-value]
    dts, px = panel.ord[s], panel.c[s]
    n = len(px)
    cost = gym.COSTS[UNIVERSE[s]]
    one_way = cost.fee + cost.slip
    pos = {m: np.zeros(n) for m in grid}
    ok = np.zeros(n, dtype=bool)
    if n:
        first = date.fromordinal(int(dts[0]))
        fri = first + timedelta(days=(FRIDAY - first.weekday()) % 7)
        last = date.fromordinal(int(dts[-1]))
        while fri < last:
            view = panel.view(decide_time(fri))
            # bars this Friday's signal is applied to: dates after it, up to the next Friday
            lo = int(np.searchsorted(dts, fri.toordinal(), side="right"))
            hi = int(np.searchsorted(dts, fri.toordinal() + 7, side="right"))
            if c.eligible(view, s):
                ok[lo:hi] = True
                for m in grid:
                    pos[m][lo:hi] = 1.0 if signal(view, s, m) else 0.0
            fri += timedelta(days=7)
    bar = np.zeros(n)
    bar[1:] = px[1:] / px[:-1] - 1
    ret = {}
    for m in grid:
        flips = np.abs(np.diff(pos[m], prepend=0.0))
        ret[m] = pos[m] * bar - one_way * flips
    out = Paper(dts, ok, ret, c.bpy(s))
    panel.cache[key] = out
    return out


def sharpe_of(r: np.ndarray, per_year: int) -> float:
    if len(r) < 2:
        return 0.0
    sd = r.std()
    return float(r.mean() / sd * math.sqrt(per_year)) if sd > 0 else 0.0


@dataclass
class Warm:
    """History put in front of an asset's paper series (the S&P 500 index before SPY)."""

    ord: np.ndarray
    ok: np.ndarray
    ret: dict[int, np.ndarray]


def warm_from(panel: Panel, s: str, last: date, grid: tuple[int, ...] = GRID) -> Warm:
    p = paper(panel, s, grid)
    keep = p.ord <= last.toordinal()
    return Warm(p.ord[keep], p.ok[keep], {m: r[keep] for m, r in p.ret.items()})


def asset_series(
    panel: Panel, s: str, n_vis: int, months: int, warm: Mapping[str, Warm], grid: tuple[int, ...]
) -> tuple[np.ndarray, np.ndarray]:
    """(dates, returns) of the asset's paper series visible at a refit, warm-up in front."""
    p = paper(panel, s, grid)
    ok = p.ok[:n_vis]
    d, r = p.ord[:n_vis][ok], p.ret[months][:n_vis][ok]
    if s in warm:
        w = warm[s]
        d = np.concatenate([w.ord[w.ok], d])
        r = np.concatenate([w.ret[months][w.ok], r])
    return d, r


def pooled_series(
    panel: Panel, n_vis: Mapping[str, int], months: int, warm: Mapping[str, Warm],
    grid: tuple[int, ...],
) -> np.ndarray:  # fmt: skip
    """Calendar-day returns of the equal-slot book of the eligible assets' paper series."""
    return pooled_dated(panel, n_vis, months, warm, grid)[1]


def pooled_dated(
    panel: Panel, n_vis: Mapping[str, int], months: int, warm: Mapping[str, Warm],
    grid: tuple[int, ...],
) -> tuple[np.ndarray, np.ndarray]:  # fmt: skip
    """(day ordinals, returns) of the pooled paper series: days with an eligible asset."""
    parts = []
    for s in panel.syms:
        p = paper(panel, s, grid)
        k = n_vis[s]
        pieces = [(p.ord[:k], p.ok[:k], p.ret[months][:k])]
        if s in warm:
            pieces.append((warm[s].ord, warm[s].ok, warm[s].ret[months]))
        for d, ok, r in pieces:
            if ok.any():
                parts.append((d[ok], r[ok]))
    if not parts:
        return np.array([], dtype=np.int64), np.array([])
    lo = min(int(d[0]) for d, _ in parts)
    hi = max(int(d[-1]) for d, _ in parts)
    tot = np.zeros(hi - lo + 1)
    cnt = np.zeros(hi - lo + 1)
    for d, r in parts:
        cnt[int(d[0]) - lo : int(d[-1]) - lo + 1] += 1
        tot[d - lo] += r
    live = cnt > 0
    return np.arange(lo, hi + 1)[live], tot[live] / cnt[live]


def first_friday(year: int) -> date:
    d = date(year, 1, 1)
    return d + timedelta(days=(FRIDAY - d.weekday()) % 7)


def refit_of(day: date) -> date:
    """The refit in force on `day`: the latest first-Friday-of-a-year on or before it."""
    ff = first_friday(day.year)
    return ff if day >= ff else first_friday(day.year - 1)


def pick(scores: Mapping[int, float]) -> int:
    """Highest score; ties to the lookback nearest 12, then the shorter."""
    return min(scores, key=lambda m: (-scores[m], abs(m - 12), m))


class Tuner:
    """A walk-forward tuning procedure of the card: `asset`, `pooled` or `shrunk`."""

    def __init__(
        self, mode: str, warm: Mapping[str, Warm] | None = None, grid: tuple[int, ...] = GRID
    ):
        if mode not in ("asset", "pooled", "shrunk"):
            raise ValueError(mode)
        self.mode = mode
        self.warm = dict(warm or {})
        self.grid = grid
        self.token = object()

    def scores(self, panel: Panel, refit: date) -> dict[str, tuple[float, dict[int, float]]]:
        """Per asset (and under "*" for the pool): years of paper series and Sharpe by lookback,
        from bars visible at the refit's decision only."""
        view = panel.view(decide_time(refit))
        out: dict[str, tuple[float, dict[int, float]]] = {}
        for s in panel.syms:
            p = paper(panel, s, self.grid)
            sc = {}
            years = 0.0
            for m in self.grid:
                _, r = asset_series(panel, s, view.n[s], m, self.warm, self.grid)
                years = len(r) / p.per_year
                sc[m] = sharpe_of(r, p.per_year)
            out[s] = (years, sc)
        pool = {}
        years = 0.0
        for m in self.grid:
            r = pooled_series(panel, view.n, m, self.warm, self.grid)
            years = len(r) / 365
            pool[m] = sharpe_of(r, 365)
        out["*"] = (years, pool)
        return out

    def choices(self, panel: Panel, refit: date) -> dict[str, int]:
        key = (self.token, "choice", refit)
        if key in panel.cache:
            return panel.cache[key]  # type: ignore[return-value]
        sc = self.scores(panel, refit)
        out = {}
        for s in panel.syms:
            years, own = sc[s]
            if self.mode == "pooled":
                pool_years, pool = sc["*"]
                out[s] = pick(pool) if pool_years >= MIN_YEARS else 12
            elif self.mode == "asset":
                out[s] = pick(own) if years >= MIN_YEARS else 12
            else:
                k = years / (years + PRIOR_YEARS)
                adv = {m: (own[m] - own[12]) * k for m in self.grid}
                best = pick(adv)
                out[s] = best if adv[best] >= HURDLE else 12
        panel.cache[key] = out
        return out

    def strategy(self) -> ResearchStrategy:
        def f(view: View) -> Weights:
            day = last_friday(view.today)
            key = (self.token, day)
            memo = view.panel.cache
            if key not in memo:
                v = view if day == view.today else view.at(day)
                ch = self.choices(view.panel, refit_of(day))
                held = c.live(v)
                memo[key] = {s: 1 / len(held) for s in held if signal(v, s, ch[s])}
            return memo[key]  # type: ignore[return-value]

        return f
