"""The residual environment of run rl-2: the agent tilts `tsmom12`'s weights (research/rl-2.md).

numpy only (tests import it). Built on rl-1's tables (`rl_env.Table`) and simulator (`rl_sim`).

- `base_weights`: `tsmom12`'s weights on every Friday of a table, computed by the logged
  baseline's own code (`common.slots(common.tsmom_signal)` on `harness.Panel.view`).
- `residual`: base + a tilt of at most half a slot, clipped at 0, coins capped at their base
  weight, scaled to sum to at most 1. Zero scores give the base weights exactly.
- `ResEnv`: batched training episodes with a `tsmom12` account beside each agent account; the
  reward is the active log return minus a turnover penalty on the active position.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, timedelta

import common as c
import harness
import numpy as np
from rl_env import Obs, Table, step_week
from rl_sim import BatchSim

from grimstrade.data import CRYPTO, UNIVERSE, Bar
from grimstrade.gym import Decision

MAX_TILT = 0.5  # of a slot
TURNOVER_PENALTY = 0.001  # per unit change in the active position, per week
_TSMOM = c.slots(c.tsmom_signal)


@dataclass
class RTable:
    t: Table
    B: np.ndarray  # [F, n] tsmom12 weights decided on each Friday
    L: np.ndarray  # [F, n] live (a year of bars): the slot count
    coin: np.ndarray  # [n] bool


def base_weights(history: Mapping[str, Sequence[Bar]], t: Table) -> RTable:
    panel = harness.Panel(history)
    syms = t.book.syms
    B = np.zeros((len(t.fridays), len(syms)))
    L = np.zeros((len(t.fridays), len(syms)), dtype=bool)
    for i, d in enumerate(t.fridays):
        view = panel.view(harness.decide_time(d))
        w = harness.clean(_TSMOM(view))
        live = set(c.live(view))
        for j, s in enumerate(syms):
            B[i, j] = w.get(s, 0.0)
            L[i, j] = s in live
    coin = np.array([UNIVERSE[s] == CRYPTO for s in syms])
    return RTable(t, B, L, coin)


def residual(
    b: np.ndarray, live: np.ndarray, elig: np.ndarray, coin: np.ndarray, s: np.ndarray
) -> np.ndarray:
    """Target weights [N, n] from base weights b and scores s (any real numbers)."""
    n = live.sum(1, keepdims=True).clip(min=1)
    tilt = np.where(live & elig, MAX_TILT / n * np.tanh(s), 0.0)
    cap = np.where(coin, b, 1.0)
    w = np.clip(b + tilt, 0.0, cap)
    tot = w.sum(1, keepdims=True)
    return np.where(tot > 1 + 1e-9, w / np.maximum(tot, 1e-12), w)


def active_share(w: np.ndarray, b: np.ndarray) -> float:
    """Half the sum of |w - b| over assets, averaged over Fridays."""
    return float(np.abs(w - b).sum(-1).mean() / 2)


@dataclass
class RObs:
    o: Obs
    b: np.ndarray  # [N, n] base weights
    live: np.ndarray  # [N, n]


class ResEnv:
    """Episodes of at most `horizon` weeks from random Fridays in [lo, hi]; rows N..2N-1 of the
    simulator are the `tsmom12` accounts started on the same Fridays."""

    def __init__(
        self, rt: RTable, n_env: int, rng: np.random.Generator, lo: int, end: int,
        horizon: int = 52,
    ):  # fmt: skip
        self.rt, self.t = rt, rt.t
        self.n = n_env
        self.rng = rng
        self.lo, self.end, self.horizon = lo, end, horizon
        self.sim = BatchSim(self.t.book, 2 * n_env)
        self.f = np.zeros(n_env, dtype=np.int64)
        self.stop = np.zeros(n_env, dtype=np.int64)
        self.prev = np.zeros((n_env, len(self.t.book.syms)))
        self._reset(np.ones(n_env, dtype=bool))

    def _reset(self, rows: np.ndarray) -> None:
        hi = max(self.lo, self.end - self.horizon)
        self.f[rows] = self.rng.integers(self.lo, hi + 1, size=int(rows.sum()))
        self.stop[rows] = np.minimum(self.f[rows] + self.horizon, self.end)
        self.sim.reset_rows(np.concatenate([rows, rows]))
        self.prev[rows] = 0.0

    def obs(self) -> RObs:
        w = self.sim.weights()[: self.n]
        t, f = self.t, self.f
        o = Obs(t.X[f], t.elig[f], t.G[f], w, 1 - w.sum(axis=1))
        return RObs(o, self.rt.B[f], self.rt.L[f])

    def step(self, s: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Scores s [N, n] -> (reward, done). Done rows are reset."""
        b = self.rt.B[self.f]
        w = residual(b, self.rt.L[self.f], self.t.elig[self.f], self.rt.coin, s)
        eq0 = self.sim.equity()
        k = self.t.kf[self.f]
        step_week(self.sim, np.concatenate([k, k]), np.concatenate([w, b]))
        g = np.log(self.sim.equity() / eq0)
        act = w - b
        rew = g[: self.n] - g[self.n :] - TURNOVER_PENALTY * np.abs(act - self.prev).sum(1)
        self.prev = act
        self.f += 1
        done = self.f >= self.stop
        if done.any():
            self._reset(done)
        return rew, done


def base_daily(history: Mapping[str, Sequence[Bar]], syms: list[str], start: date,
               end: date) -> np.ndarray:  # fmt: skip
    """`tsmom12`'s decision on every day from `start` to `end` [D, n], exactly as the logged
    baseline decides it (`common.weekly`: on a holiday Friday it keeps the previous Friday's)."""
    decs = harness.decisions(c.weekly(_TSMOM), harness.Panel(history), start, end)
    return np.array([[d.weights.get(s, 0.0) for s in syms] for d in decs])


def res_decisions(rt: RTable, i0: int, S: np.ndarray, bd: np.ndarray, end: date) -> list[Decision]:
    """Gym decisions every day from Friday i0 to `end`. S [weeks, K, n]: the scores decided on
    each Friday by K policies (one seed, or the ten of an ensemble); each day's weights are the
    mean over the K policies of `residual` on that day's `tsmom12` weights (bd, from Friday i0)."""
    t = rt.t
    syms = t.book.syms
    out = []
    K = S.shape[1]

    def rep(a: np.ndarray) -> np.ndarray:
        return np.repeat(a[None], K, 0)

    for i in range(len(S)):
        for k in range(7):
            d = t.fridays[i0 + i] + timedelta(days=k)
            if d > end:
                break
            b = bd[(d - t.fridays[i0]).days]
            w = residual(rep(b), rep(rt.L[i0 + i]), rep(t.elig[i0 + i]), rt.coin, S[i])
            wd = w[0] if K == 1 else w.mean(0)
            out.append(Decision(
                harness.decide_time(d),
                harness.clean({s: float(wd[j]) for j, s in enumerate(syms) if wd[j] > 1e-9}),
            ))  # fmt: skip
    return out


def weekly_sharpe(eq: np.ndarray) -> float:
    r = np.diff(np.log(eq))
    return float(r.mean() / r.std() * math.sqrt(52)) if len(r) > 2 and r.std() > 0 else math.nan
