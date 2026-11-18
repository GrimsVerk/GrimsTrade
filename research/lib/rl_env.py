"""The RL environment of run rl-1: weekly decisions on Fridays, the gym's rules (`rl_sim`).

Observations (research/rl-1.md, "Observation"), all public before the Friday 22:30 decision:
- per asset: run 2's 15 features (`ml.rows_at`, built through `harness.Panel.view`, which hands
  out only bars closed before the decision), a coin flag, days since the last halving / 1461
  (coins only), and at run time the asset's current weight;
- shared: macro features through `lib/macro.py` (`Step.at(d)`: public before `d`), and at run
  time the cash weight.

`build_table` precomputes the per-Friday inputs once per asset set; `WeekEnv` runs batched
episodes on them; `run_policy` replays a fixed policy over a stretch of Fridays.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, timedelta

import harness
import ml
import numpy as np
from rl_sim import BatchSim, Book, make_book

from grimstrade.data import CRYPTO, UNIVERSE, Bar
from grimstrade.gym import Decision

N_ML = len(ml.FEATURES)  # 15
ASSET_FEATS = [*ml.FEATURES, "coin", "halving"]
MACRO_FEATS = [
    "dff30", "dff_chg182", "real_ff", "curve", "baa20", "real_m2", "unrate_rise", "cpi_yoy",
    "dgs10", "vix",
]  # fmt: skip
HALVINGS = (date(2012, 11, 28), date(2016, 7, 9), date(2020, 5, 11), date(2024, 4, 19))

MacroFn = Callable[[date], Sequence[float]]


def macro_vector(d: date) -> list[float]:
    """The shared macro inputs as a decision on day d may see them (NaN before a series starts)."""
    import macro  # loaded lazily: needs the data cache

    f = macro.features()
    return [getattr(f, k).at(d) for k in MACRO_FEATS]


def days_since_halving(d: date) -> float:
    past = [h for h in HALVINGS if h < d]
    return float((d - past[-1]).days) if past else math.nan


def next_friday(d: date) -> date:
    return d + timedelta(days=(4 - d.weekday()) % 7)


@dataclass
class Table:
    book: Book
    fridays: list[date]
    kf: np.ndarray  # [F] grid day of each Friday
    X: np.ndarray  # [F, n, len(ASSET_FEATS)], 0 where not eligible
    elig: np.ndarray  # [F, n] bool
    G: np.ndarray  # [F, len(MACRO_FEATS)], NaN where unknown

    def index(self, d: date) -> int:
        """Index of the first Friday on or after d."""
        return int(np.searchsorted(np.array([x.toordinal() for x in self.fridays]), d.toordinal()))


def build_table(
    history: Mapping[str, Sequence[Bar]], macro_fn: MacroFn, first: date, last: date
) -> Table:
    """Inputs for every Friday from `first` to `last` (decision dates)."""
    panel = harness.Panel(history)
    book = make_book(history)
    syms = book.syms
    fr = []
    d = next_friday(max(first, book.first))
    while d <= last:
        fr.append(d)
        d += timedelta(days=7)
    x = np.zeros((len(fr), len(syms), len(ASSET_FEATS)))
    el = np.zeros((len(fr), len(syms)), dtype=bool)
    g = np.full((len(fr), len(MACRO_FEATS)), np.nan)
    coin = np.array([UNIVERSE[s] == CRYPTO for s in syms])
    for i, d in enumerate(fr):
        rows = ml.rows_at(panel.view(harness.decide_time(d)))
        h = days_since_halving(d)
        for j, s in enumerate(syms):
            if s in rows:
                el[i, j] = True
                x[i, j, :N_ML] = rows[s]
                x[i, j, N_ML] = float(coin[j])
                x[i, j, N_ML + 1] = h / 1461 if coin[j] and not math.isnan(h) else 0.0
        g[i] = macro_fn(d)
    kf = np.array([book.day(d) for d in fr], dtype=np.int64)
    return Table(book, fr, kf, x, el, g)


@dataclass
class Obs:
    X: np.ndarray  # [N, n, A] asset features
    elig: np.ndarray  # [N, n]
    G: np.ndarray  # [N, M] macro (NaN where unknown)
    w: np.ndarray  # [N, n] current weights
    cash: np.ndarray  # [N] current cash weight


def step_week(sim: BatchSim, k: np.ndarray, w: np.ndarray) -> None:
    """Decide w at day k 22:30, repeat it every day, stop at day k + 7 before its decision."""
    sim.decide(w)
    sim.evening(k)
    for d in range(1, 7):
        sim.morning(k + d)
        sim.decide(w)
        sim.evening(k + d)
    sim.morning(k + 7)


class WeekEnv:
    """Batched training episodes: random start Friday in [lo, hi_start], at most `horizon` weeks,
    never past Friday index `end` (the last decision whose week ends inside the window)."""

    def __init__(
        self,
        table: Table,
        n_env: int,
        rng: np.random.Generator,
        lo: int,
        end: int,
        horizon: int = 52,
        dd_penalty: float = 0.0,
    ):
        self.t = table
        self.n = n_env
        self.rng = rng
        self.lo, self.end = lo, end
        self.horizon = horizon
        self.dd = dd_penalty
        self.sim = BatchSim(table.book, n_env)
        self.f = np.zeros(n_env, dtype=np.int64)
        self.stop = np.zeros(n_env, dtype=np.int64)
        self.logeq = np.zeros(n_env)
        self.peak = np.zeros(n_env)
        self._reset(np.ones(n_env, dtype=bool))

    def _reset(self, rows: np.ndarray) -> None:
        hi = max(self.lo, self.end - self.horizon)
        m = int(rows.sum())
        self.f[rows] = self.rng.integers(self.lo, hi + 1, size=m)
        self.stop[rows] = np.minimum(self.f[rows] + self.horizon, self.end)
        self.sim.reset_rows(rows)
        self.logeq[rows] = 0.0
        self.peak[rows] = 0.0

    def obs(self) -> Obs:
        w = self.sim.weights()
        return Obs(self.t.X[self.f], self.t.elig[self.f], self.t.G[self.f], w, 1 - w.sum(axis=1))

    def step(self, w: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Returns (reward, done). Done rows are reset; their next obs is a new episode."""
        eq0 = self.sim.equity()
        step_week(self.sim, self.t.kf[self.f], w)
        r = np.log(self.sim.equity() / eq0)
        self.logeq += r
        dd0 = self.peak - (self.logeq - r)
        self.peak = np.maximum(self.peak, self.logeq)
        dd1 = self.peak - self.logeq
        rew = r - self.dd * np.maximum(dd1 - dd0, 0.0)
        self.f += 1
        done = self.f >= self.stop
        if done.any():
            self._reset(done)
        return rew, done


Policy = Callable[[Obs], np.ndarray]  # -> target weights [N, n]


def run_policy(table: Table, policy: Callable[[Obs, int], np.ndarray], i0: int, i1: int,
               n_env: int = 1) -> tuple[np.ndarray, np.ndarray]:  # fmt: skip
    """Decide on Fridays i0..i1-1 (policy gets the Friday index too). Returns the weights decided
    [i1-i0, N, n] and the equity at each decision and after the last week [i1-i0+1, N]."""
    sim = BatchSim(table.book, n_env)
    sim.reset()
    ws, eqs = [], [sim.equity().copy()]
    for i in range(i0, i1):
        w = sim.weights()
        o = Obs(
            np.repeat(table.X[i][None], n_env, 0), np.repeat(table.elig[i][None], n_env, 0),
            np.repeat(table.G[i][None], n_env, 0), w, 1 - w.sum(axis=1),
        )  # fmt: skip
        a = policy(o, i)
        ws.append(a)
        k = np.full(n_env, table.kf[i])
        if table.kf[i] + 7 < len(table.book.opens):
            step_week(sim, k, a)
        eqs.append(sim.equity().copy())
    return np.array(ws), np.array(eqs)


def daily_decisions(table: Table, i0: int, weights: np.ndarray, end: date) -> list[Decision]:
    """Gym decisions every day from Friday i0 to `end`, repeating each Friday's weights."""
    out = []
    syms = table.book.syms
    for i in range(len(weights)):
        d0 = table.fridays[i0 + i]
        for k in range(7):
            d = d0 + timedelta(days=k)
            if d > end:
                break
            w = {s: float(weights[i][j]) for j, s in enumerate(syms) if weights[i][j] > 1e-9}
            out.append(Decision(harness.decide_time(d), harness.clean(w)))
    return out
