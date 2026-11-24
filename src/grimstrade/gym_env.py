"""A Gymnasium environment around the gym, for RL agents (docs/gym-env.md; DESIGN ladder rung 4).

The agent's action is a set of target weights; the environment replays them through the gym's own
rules: fills at each asset's next open with slippage and fees (Kraken tiers for crypto), the 1%
rebalance band, sells before buys, buys limited by cash, distributions, cash interest. `Replay`
is `gym.simulate`'s event loop cut open at each decision, and calls the gym's own trade step, so
an agent and a classic strategy are scored by the same code (a test drives the environment with
`ts_momentum`'s weights and gets `gym.simulate`'s result to the last fill).

The observation at a decision at time T uses only bars that closed by T (`data.visible`) and the
account as it stands then (its fills so far, valued at those closes). Train data only by
default: a bar after TRAIN_LAST_BAR (the held-out year) is refused unless `allow_held_out=True`.

Needs the optional `rl` dependency group (gymnasium, numpy). The daily runner never imports this
module.
"""

from __future__ import annotations

import bisect
import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, SupportsFloat

import gymnasium
import numpy as np
from gymnasium import spaces
from numpy.typing import NDArray

from grimstrade import data, gym, rates
from grimstrade.data import ETF, UNIVERSE, Bar, Dividends, History, close_time, open_time
from grimstrade.gym import _CLOSE, _DECIDE, _DIVIDEND, _OPEN, DAYS_PER_YEAR, DECIDE_AT

# The last bar of the train period. Later bars are the held-out year, looked at once per card
# (research/protocol.md), never by a training run.
TRAIN_LAST_BAR = date(2025, 11, 10)
# A held-out session's cash rate is known from that session's close at the earliest.
HELD_OUT_RATE_FROM = close_time(ETF, TRAIN_LAST_BAR + timedelta(days=1))

Obs = NDArray[np.float32]
Action = NDArray[np.float64]
# Market features from the visible bars at a decision time (one fixed-length vector).
Features = Callable[[Mapping[str, Sequence[Bar]], datetime], NDArray[np.float64]]


class HeldOutError(ValueError):
    """Data from the held-out year reached a train-only environment or loader."""


@dataclass(frozen=True)
class TrainData:
    history: dict[str, list[Bar]]
    dividends: dict[str, list[data.Dividend]]
    rates: gym.Rates


def load_train(
    root: Path, symbols: Sequence[str] = tuple(UNIVERSE), allow_held_out: bool = False
) -> TrainData:
    """Bars, distributions and cash rates from a data root (`data/bars/`, `data/dividends.csv`,
    `data/rates.csv`), cut after TRAIN_LAST_BAR unless `allow_held_out`. Rates are known from
    their session's close (backtest rule, `rates.steps(live=False)`)."""
    history = data.load_all(root, symbols)
    dividends = {s: list(d) for s, d in data.load_dividends(root).items() if s in symbols}
    rows = rates.load(root)
    if not allow_held_out:
        history = {s: [b for b in bars if b.date <= TRAIN_LAST_BAR] for s, bars in history.items()}
        dividends = {
            s: [d for d in ds if d.ex_date <= TRAIN_LAST_BAR] for s, ds in dividends.items()
        }
        rows = [r for r in rows if r.date <= TRAIN_LAST_BAR]
    return TrainData(history, dividends, rates.steps(rows, live=False))


def check_train_only(
    history: History, dividends: Dividends | None = None, cash_rates: gym.Rates = ()
) -> None:
    """Raise HeldOutError if any input holds data from after TRAIN_LAST_BAR."""
    for sym, bars in history.items():
        if bars and max(b.date for b in bars) > TRAIN_LAST_BAR:
            raise HeldOutError(f"{sym}: bars after {TRAIN_LAST_BAR} (held-out year)")
    for sym, ds in (dividends or {}).items():
        if any(d.ex_date > TRAIN_LAST_BAR for d in ds):
            raise HeldOutError(f"{sym}: distributions after {TRAIN_LAST_BAR} (held-out year)")
    if any(t >= HELD_OUT_RATE_FROM for t, _ in cash_rates):
        raise HeldOutError(f"cash rates known from {HELD_OUT_RATE_FROM} on (held-out year)")


def decide_time(d: date) -> datetime:
    return datetime.combine(d, DECIDE_AT, tzinfo=UTC)


class Replay:
    """`gym.simulate`, one decision at a time.

    The same events in the same order, the same day bookkeeping (interest, end-of-day equity)
    and the gym's own `_execute` for the fills, so feeding it the decisions `simulate` gets gives
    the same `Result`. Call `decide` with rising times, then `finish`.
    """

    def __init__(
        self,
        history: History,
        start_cash: float = gym.START_CASH,
        costs: Mapping[str, gym.Costs] = gym.COSTS,
        band: float = gym.BAND,
        dividends: Dividends | None = None,
        cash_rates: gym.Rates = (),
    ) -> None:
        events: list[tuple[datetime, int, str, float]] = []
        for sym, bars in history.items():
            cls = UNIVERSE[sym]
            for b in bars:
                events.append((open_time(cls, b.date), _OPEN, sym, b.open))
                events.append((close_time(cls, b.date), _CLOSE, sym, b.close))
            for dv in (dividends or {}).get(sym, []):
                events.append((open_time(cls, dv.ex_date), _DIVIDEND, sym, dv.amount))
        events.sort(key=lambda e: (e[0], e[1]))
        self.events = events
        self.symbols = list(history)
        self.costs, self.band = costs, band
        self.res = gym.Result(
            cash=start_cash, positions={s: 0.0 for s in history}, start_cash=start_cash
        )
        self.price: dict[str, float] = {}
        self.pending: dict[str, float] = {}
        self.unpaid: set[str] = set()
        self.started = False
        self.day: date | None = None
        self.growth = 1.0  # of one dollar of cash since the last equity point (as simulate)
        self.step_growth = 1.0  # of one dollar of cash since `take_step_growth` was last called
        self.rates = sorted(cash_rates, key=lambda r: r[0])
        self.known = [t for t, _ in self.rates]
        self.i = 0

    def equity(self) -> float:
        return self.res.cash + sum(
            q * self.price.get(s, 0.0) for s, q in self.res.positions.items()
        )

    def skip_to(self, t: datetime) -> None:
        """Jump over every event before a decision at `t`, before the first decision. Nothing
        but prices changes then (no positions, no orders), so only those are set."""
        assert not self.started and self.i == 0
        j = bisect.bisect_left(self.events, (t, _DECIDE), key=lambda e: (e[0], e[1]))
        for _, kind, sym, px in self.events[:j]:
            if kind != _DIVIDEND:
                self.price[sym] = px
        self.i = j

    def _accrue(self, d: date) -> None:
        r = gym.cash_rate(self.rates, d, self.known)
        self.res.cash += gym.interest(self.res.cash, r)
        self.growth *= 1 + r / DAYS_PER_YEAR
        self.step_growth *= 1 + r / DAYS_PER_YEAR

    def _new_day(self, t: datetime, kind: int) -> None:
        ev_day = (t - timedelta(microseconds=1)).date() if kind == _CLOSE else t.date()
        if self.started and self.day is not None and ev_day > self.day:
            self._accrue(self.day)
            self.res.equity.append((self.day, self.equity()))
            self.res.cash_growth.append(self.growth - 1)
            self.growth = 1.0
            for k in range(1, (ev_day - self.day).days):
                self._accrue(self.day + timedelta(days=k))
        self.day = ev_day

    def _run_until(self, t: datetime | None) -> None:
        """Process every event that comes before a decision at `t` (all of them if None)."""
        ev = self.events
        while self.i < len(ev) and (t is None or ev[self.i][0] <= t):
            et, kind = ev[self.i][0], ev[self.i][1]
            group = []
            while self.i < len(ev) and ev[self.i][0] == et and ev[self.i][1] == kind:
                group.append(ev[self.i])
                self.i += 1
            self._new_day(et, kind)
            if kind == _DIVIDEND:
                for _, _, sym, amount in group:
                    if (paid := self.res.positions[sym] * amount) > 0:
                        self.res.cash += paid
                        self.res.income.append((et, sym, paid))
                continue
            for _, _, sym, px in group:
                self.price[sym] = px
            if kind == _OPEN:
                syms = [g[2] for g in group if g[2] in self.pending]
                gym._execute(
                    et, syms, self.pending, self.unpaid, self.res, self.price, self.costs, self.band
                )

    def advance(self, t: datetime) -> None:
        """Bring the account up to a decision at `t`, without deciding."""
        self._run_until(t)
        self._new_day(t, _DECIDE)

    def decide(self, t: datetime, weights: Mapping[str, float]) -> None:
        gym.validate(weights)
        self.advance(t)
        self.started = True
        self.pending = {s: weights.get(s, 0.0) for s in self.symbols}
        self.unpaid.clear()

    def finish(self, stop: datetime | None = None) -> gym.Result:
        """Run the events before a decision at `stop` (all of them if None) and close the last
        day, as `simulate` does after its last event: that day's interest is not credited."""
        self._run_until(stop)
        if self.started and self.day is not None:
            self.res.equity.append((self.day, self.equity()))
            self.res.cash_growth.append(self.growth - 1)
        return self.res

    def take_step_growth(self) -> float:
        g, self.step_growth = self.step_growth, 1.0
        return g


@dataclass(frozen=True)
class StepInfo:
    """What a reward function sees about one step (decision to next decision)."""

    equity_before: float
    equity_after: float
    cash_growth: float  # what one dollar of cash grew to over the step (1.0 without rates)
    turnover: float  # sum of |new target - weight held| over assets, as shares of equity
    fees: float  # fees paid during the step, USD (slippage is in the fill prices)


def _log_growth(s: StepInfo) -> float:
    return math.log(max(s.equity_after, 1e-12) / s.equity_before)


REWARDS: dict[str, Callable[[StepInfo], float]] = {
    # log growth of the account after costs: sums to log(final / start equity) over an episode
    "log": _log_growth,
    "simple": lambda s: s.equity_after / s.equity_before - 1,
    # log growth above the cash rate (what Sharpe is measured against)
    "excess_log": lambda s: _log_growth(s) - math.log(s.cash_growth),
}


class TradingEnv(gymnasium.Env[Obs, Action]):
    """One step = one decision at DECIDE_AT UTC (daily, or weekly on `weekday`).

    Action: a target weight per symbol in `symbols` order, a Box in [0, 1]. Long-only, no
    leverage, as the paper broker: values are clipped to [0, 1], assets with fewer than `min_bars`
    visible bars get 0, and the rest is scaled down to sum to 1 if it sums to more. What is left
    over is cash.
    Between weekly decisions the same weights are re-submitted every day, as `common.weekly`
    strategies are replayed (the band rebalances drift daily).

    Observation (float32): `features(visible bars, T)` (default: the last `lookback` daily log
    close-to-close returns per symbol, zero-padded, and a 0/1 "has `min_bars` bars" flag), then
    each symbol's current weight and the cash weight, valued at the visible closes.

    Reward: `reward` names one of REWARDS or is a function of StepInfo; minus
    `turnover_penalty` x turnover. The step's account change is measured from the equity at this
    decision to the equity at the next one (last known prices).

    Episodes: decisions on the days `start`..`end` (default: the first and last bar dates). With
    `episode_steps`, each reset picks a random window of that many decisions (`np_random`, seeded
    by `reset(seed=...)`); otherwise an episode runs over the whole range. The last step runs to
    the decision time one period after the last decision. `truncated` is True at the episode's
    end; `terminated` only if equity reaches 0.
    """

    metadata: dict[str, Any] = {"render_modes": []}

    def __init__(
        self,
        history: History,
        *,
        symbols: Sequence[str] | None = None,
        start: date | None = None,
        end: date | None = None,
        weekday: int | None = None,
        episode_steps: int | None = None,
        lookback: int = 20,
        min_bars: int = 1,
        features: Features | None = None,
        reward: str | Callable[[StepInfo], float] = "log",
        turnover_penalty: float = 0.0,
        start_cash: float = gym.START_CASH,
        costs: Mapping[str, gym.Costs] = gym.COSTS,
        band: float = gym.BAND,
        dividends: Dividends | None = None,
        cash_rates: gym.Rates = (),
        allow_held_out: bool = False,
    ) -> None:
        super().__init__()
        if not allow_held_out:
            check_train_only(history, dividends, cash_rates)
        self.symbols = list(symbols) if symbols is not None else sorted(history)
        unknown = set(self.symbols) - set(UNIVERSE)
        if unknown:
            raise ValueError(f"unknown symbols: {sorted(unknown)}")
        self.history = {s: list(history.get(s, [])) for s in self.symbols}
        dates = [b.date for bars in self.history.values() for b in bars]
        if not dates:
            raise ValueError("no bars")
        start = start or min(dates)
        end = end or max(dates)
        if not allow_held_out and end > TRAIN_LAST_BAR:
            raise HeldOutError(f"episode end {end} is in the held-out year")
        self.period = 1 if weekday is None else 7
        first = start
        if weekday is not None:
            first += timedelta(days=(weekday - start.weekday()) % 7)
        n_days = (end - first).days // self.period + 1 if first <= end else 0
        self.days = [first + timedelta(days=k * self.period) for k in range(n_days)]
        if not self.days:
            raise ValueError(f"no decision day in {start}..{end}")
        if episode_steps is not None and not 1 <= episode_steps <= len(self.days):
            raise ValueError(f"episode_steps must be 1..{len(self.days)}")
        self.episode_steps = episode_steps
        self.lookback, self.min_bars = lookback, min_bars
        self.features = features
        self.reward_fn = REWARDS[reward] if isinstance(reward, str) else reward
        self.turnover_penalty = turnover_penalty
        self.sim_args: dict[str, Any] = {
            "start_cash": start_cash,
            "costs": costs,
            "band": band,
            "dividends": {s: list((dividends or {}).get(s, [])) for s in self.symbols},
            "cash_rates": cash_rates,
        }
        self._close_times = {
            s: [close_time(UNIVERSE[s], b.date) for b in bars] for s, bars in self.history.items()
        }
        self._closes = {
            s: np.array([b.close for b in bars], dtype=np.float64)
            for s, bars in self.history.items()
        }
        n = len(self.symbols)
        dim = len(self._market(decide_time(self.days[0]))) + n + 1
        self.observation_space = spaces.Box(-np.inf, np.inf, shape=(dim,), dtype=np.float32)
        self.action_space = spaces.Box(0.0, 1.0, shape=(n,), dtype=np.float64)
        self.replay: Replay | None = None
        self._k = 0  # index into self.days of the current decision
        self._stop_k = 0  # the episode ends at this index (exclusive)
        self._steps = 0

    # --- observation ---

    def _n_visible(self, sym: str, t: datetime) -> int:
        return bisect.bisect_right(self._close_times[sym], t)

    def _market(self, t: datetime) -> NDArray[np.float64]:
        if self.features is not None:
            vis = {s: bars[: self._n_visible(s, t)] for s, bars in self.history.items()}
            return np.asarray(self.features(vis, t), dtype=np.float64)
        out = np.zeros((len(self.symbols), self.lookback + 1))
        for j, s in enumerate(self.symbols):
            k = self._n_visible(s, t)
            c = self._closes[s][max(0, k - self.lookback - 1) : k]
            if len(c) > 1:
                r = np.log(c[1:] / c[:-1])
                out[j, self.lookback - len(r) : self.lookback] = r
            out[j, self.lookback] = 1.0 if k >= self.min_bars else 0.0
        return out.ravel()

    def _held_weights(self, t: datetime) -> tuple[NDArray[np.float64], float]:
        """Each symbol's share of equity and the cash share, at the closes visible at `t`."""
        assert self.replay is not None
        value = np.zeros(len(self.symbols))
        for j, s in enumerate(self.symbols):
            k = self._n_visible(s, t)
            if k:
                value[j] = self.replay.res.positions[s] * self._closes[s][k - 1]
        cash = self.replay.res.cash
        eq = cash + float(value.sum())
        if eq <= 0:
            return np.zeros(len(self.symbols)), 0.0
        return value / eq, cash / eq

    def _obs(self, t: datetime) -> Obs:
        w, cash = self._held_weights(t)
        return np.concatenate([self._market(t), w, [cash]]).astype(np.float32)

    # --- action ---

    def weights(self, action: Action, t: datetime) -> dict[str, float]:
        """The target weights an action means at decision time `t`."""
        a = np.clip(np.nan_to_num(np.asarray(action, dtype=np.float64), nan=0.0), 0.0, 1.0)
        if a.shape != (len(self.symbols),):
            raise ValueError(f"action shape {a.shape}, expected ({len(self.symbols)},)")
        for j, s in enumerate(self.symbols):
            if self._n_visible(s, t) < self.min_bars:
                a[j] = 0.0
        total = float(a.sum())
        if total > 1:
            a = a / total
        return {s: float(a[j]) for j, s in enumerate(self.symbols)}

    # --- episode ---

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[Obs, dict[str, Any]]:
        super().reset(seed=seed)
        if self.episode_steps is None:
            self._k, self._stop_k = 0, len(self.days)
        else:
            self._k = int(self.np_random.integers(0, len(self.days) - self.episode_steps + 1))
            self._stop_k = self._k + self.episode_steps
        self._steps = 0
        self.replay = Replay(self.history, **self.sim_args)
        t = decide_time(self.days[self._k])
        self.replay.skip_to(t)
        self.replay.advance(t)
        self.replay.take_step_growth()
        return self._obs(t), {"time": t, "equity": self.replay.equity()}

    def step(self, action: Action) -> tuple[Obs, SupportsFloat, bool, bool, dict[str, Any]]:
        if self.replay is None or self._k >= self._stop_k:
            raise RuntimeError("call reset() first")
        rp = self.replay
        day = self.days[self._k]
        t = decide_time(day)
        w = self.weights(action, t)
        held, _ = self._held_weights(t)
        turnover = float(sum(abs(w[s] - held[j]) for j, s in enumerate(self.symbols)))
        before = rp.equity()
        n_fills = len(rp.res.fills)
        nxt = day + timedelta(days=self.period)
        rp.decide(t, w)
        for k in range(1, self.period):  # weekly: the same weights again on the days between
            rp.decide(decide_time(day + timedelta(days=k)), w)
        self._k += 1
        self._steps += 1
        last = self._k >= self._stop_k
        t_next = decide_time(nxt)
        if last:
            rp.finish(t_next)
        else:
            rp.advance(t_next)
        after = rp.equity()
        fees = sum(f.fee for f in rp.res.fills[n_fills:])
        info_step = StepInfo(before, after, rp.take_step_growth(), turnover, fees)
        reward = self.reward_fn(info_step) - self.turnover_penalty * turnover
        terminated = after <= 0
        info: dict[str, Any] = {
            "time": t,
            "next_time": t_next,  # when the returned observation is from
            "weights": w,
            "equity": after,
            "fees": fees,
            "turnover": turnover,
            "cash_growth": info_step.cash_growth,
            "fills": rp.res.fills[n_fills:],
        }
        if last or terminated:
            info["result"] = rp.res
        return self._obs(t_next), reward, terminated, last, info
