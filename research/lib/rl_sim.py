"""Batched replay of the gym's rules for RL training (run rl-1). numpy only.

`grimstrade.gym.simulate` replays one account over an event list. Training needs thousands of
short episodes at once, so this module replays the same rules for N accounts in parallel, each
at its own day. The rules, copied from `gym.simulate` / `gym._execute`:

- Events inside a UTC day, in this order: crypto open (00:00), ETF open (13:30), ETF close
  (21:00), decision (22:30), crypto close (24:00, which ends the day: the gym's `_CLOSE` at
  midnight sorts before the next day's `_OPEN`).
- A decision sets a pending target weight for every asset. At an open, the assets that open
  (have a bar that day) and are pending execute against the equity at that moment; the rest
  wait. A trade is skipped if it is smaller than `band` x equity, unless it is a full exit.
  Sells go first (in order of size), then buys from the smallest, each limited by cash.
- Buy at open x (1 + slip) plus a fee on the traded value; sell at open x (1 - slip) minus fee.
- Equity is cash plus positions at the last price seen (0 before an asset's first bar).

`tests/test_rl_env.py` proves that daily equity equals `gym.simulate` for the same weights.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np

from grimstrade.data import CRYPTO, UNIVERSE, Bar
from grimstrade.gym import BAND, COSTS, START_CASH, Costs


@dataclass
class Book:
    """Bars of one asset set on a calendar-day grid; NaN on days without a bar."""

    syms: list[str]
    first: date  # grid day 0
    opens: np.ndarray  # [K, n]
    closes: np.ndarray  # [K, n]
    crypto: np.ndarray  # [n] bool
    fee: np.ndarray  # [n]
    slip: np.ndarray  # [n]

    def day(self, d: date) -> int:
        return (d - self.first).days

    def date(self, k: int) -> date:
        return self.first + timedelta(days=k)


def make_book(history: Mapping[str, Sequence[Bar]], costs: Mapping[str, Costs] = COSTS) -> Book:
    syms = [s for s in history if len(history[s])]
    first = min(history[s][0].date for s in syms)
    last = max(history[s][-1].date for s in syms)
    k = (last - first).days + 1
    o = np.full((k, len(syms)), np.nan)
    c = np.full((k, len(syms)), np.nan)
    for j, s in enumerate(syms):
        for b in history[s]:
            i = (b.date - first).days
            o[i, j], c[i, j] = b.open, b.close
    cls = [UNIVERSE[s] for s in syms]
    return Book(
        syms, first, o, c,
        np.array([x == CRYPTO for x in cls]),
        np.array([costs[x].fee for x in cls]),
        np.array([costs[x].slip for x in cls]),
    )  # fmt: skip


class BatchSim:
    """N accounts on one book. Each account sits at its own grid day `k[e]`.

    Call order for a day: `morning(k)` (opens and ETF closes of day k), then optionally
    `decide(w)` (22:30), then `evening(k)` (crypto closes; ends day k).
    """

    def __init__(self, book: Book, n_env: int, band: float = BAND):
        self.b = book
        self.n = n_env
        self.band = band
        m = len(book.syms)
        self.cash = np.full(n_env, START_CASH)
        self.pos = np.zeros((n_env, m))
        self.price = np.zeros((n_env, m))
        self.target = np.zeros((n_env, m))
        self.pending = np.zeros((n_env, m), dtype=bool)

    def reset(self) -> None:
        """All cash. Last prices are irrelevant while every position is 0: each asset's price
        is set by its next open before it can trade."""
        self.cash[:] = START_CASH
        self.pos[:] = 0.0
        self.target[:] = 0.0
        self.pending[:] = False
        self.price[:] = 0.0

    def reset_rows(self, rows: np.ndarray) -> None:
        self.cash[rows] = START_CASH
        self.pos[rows] = 0.0
        self.target[rows] = 0.0
        self.pending[rows] = False
        self.price[rows] = 0.0

    def equity(self) -> np.ndarray:
        return self.cash + (self.pos * self.price).sum(axis=1)

    def weights(self) -> np.ndarray:
        eq = self.equity()
        return self.pos * self.price / eq[:, None]

    def decide(self, w: np.ndarray, mask: np.ndarray | None = None) -> None:
        """Set targets (rows where mask is True; all rows if None)."""
        if mask is None:
            self.target[:] = w
            self.pending[:] = True
        else:
            self.target[mask] = w[mask]
            self.pending[mask] = True

    def morning(self, k: np.ndarray) -> None:
        o, c = self.b.opens[k], self.b.closes[k]
        has_o = ~np.isnan(o)
        for crypto in (True, False):  # crypto opens at 00:00, ETFs at 13:30
            grp = has_o & (self.b.crypto == crypto)[None, :]
            if not grp.any():
                continue
            self.price = np.where(grp, o, self.price)
            self._execute(grp & self.pending)
        etf_close = ~np.isnan(c) & ~self.b.crypto[None, :]
        self.price = np.where(etf_close, c, self.price)

    def evening(self, k: np.ndarray) -> None:
        c = self.b.closes[k]
        crypto_close = ~np.isnan(c) & self.b.crypto[None, :]
        self.price = np.where(crypto_close, c, self.price)

    def _execute(self, act: np.ndarray) -> None:
        if not act.any():
            return
        self.pending &= ~act
        px = np.where(act, self.price, 1.0)
        eq = self.equity()
        delta = self.target * eq[:, None] - self.pos * px
        full_exit = act & (self.target == 0) & (self.pos > 0)
        trade = act & (full_exit | (np.abs(delta) >= self.band * eq[:, None]))
        # Sells: each independent of the others.
        sell = trade & (delta < 0)
        if sell.any():
            sp = px * (1 - self.b.slip)
            qty = np.where(full_exit, self.pos, np.minimum(-delta / px, self.pos))
            qty = np.where(sell, qty, 0.0)
            fee = qty * sp * self.b.fee
            # add in the gym's order (ascending delta) so float sums match closely
            order = np.argsort(np.where(sell, delta, np.inf), axis=1, kind="stable")
            rows = np.arange(self.n)
            for r in range(order.shape[1]):
                j = order[:, r]
                on = sell[rows, j]
                if not on.any():
                    break
                proceeds = qty[rows, j] * sp[rows, j] - fee[rows, j]
                self.cash = np.where(on, self.cash + proceeds, self.cash)
                held = self.pos[rows, j]
                self.pos[rows, j] = np.where(on, held - qty[rows, j], held)
        buy = trade & (delta > 0)
        if buy.any():
            order = np.argsort(np.where(buy, delta, np.inf), axis=1, kind="stable")
            rows = np.arange(self.n)
            for r in range(order.shape[1]):
                j = order[:, r]
                on = buy[rows, j]
                if not on.any():
                    break
                p = px[rows, j]
                bp = p * (1 + self.b.slip[j])
                f = self.b.fee[j]
                spend = np.minimum(delta[rows, j] / p * bp * (1 + f), self.cash)
                on = on & (spend > 0)
                qty = np.where(on, spend / (bp * (1 + f)), 0.0)
                fee = qty * bp * f
                self.cash = np.where(on, self.cash - (qty * bp + fee), self.cash)
                self.pos[rows, j] = self.pos[rows, j] + qty


def replay_daily(book: Book, start: date, weights: Sequence[np.ndarray]) -> np.ndarray:
    """One account deciding `weights[i]` on day start + i. Equity at the end of each day."""
    sim = BatchSim(book, 1)
    k0 = book.day(start)
    sim.reset()
    out = np.empty(len(weights))
    for i, w in enumerate(weights):
        k = np.array([k0 + i])
        if i:
            sim.morning(k)
        sim.decide(np.asarray(w, dtype=float)[None, :])
        sim.evening(k)
        out[i] = sim.equity()[0]
    return out
