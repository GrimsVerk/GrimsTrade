"""The gym: a simulated broker that replays decisions over real bars.

An order decided at time T fills at the open of each asset's first bar that opens after T, at
open * (1 +/- slippage), plus a fee on the traded value. Long-only, no leverage, fractional units.
The same replay serves the live ledger and backtests, so they can't disagree on the rules.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time, timedelta

from grimstrade.data import CRYPTO, ETF, UNIVERSE, History, close_time, open_time, visible_history

Weights = dict[str, float]
Strategy = Callable[[History], tuple[Weights, str]]

START_CASH = 10_000.0
# Skip a trade smaller than this share of equity (rebalance band), except a full exit.
BAND = 0.01
# Backtests decide once a day at this UTC time, like the daily runner.
DECIDE_AT = time(22, 30)


@dataclass(frozen=True)
class Costs:
    fee: float  # share of traded value
    slip: float  # half-spread + slippage, share of price


COSTS: dict[str, Costs] = {CRYPTO: Costs(fee=0.0025, slip=0.0005), ETF: Costs(fee=0.0, slip=0.0002)}


@dataclass(frozen=True)
class Decision:
    time: datetime
    weights: Weights


@dataclass(frozen=True)
class Fill:
    time: datetime
    symbol: str
    qty: float  # + buy, - sell
    price: float  # execution price, after slippage
    fee: float


@dataclass
class Result:
    cash: float
    positions: dict[str, float]
    fills: list[Fill] = field(default_factory=list)
    equity: list[tuple[date, float]] = field(default_factory=list)  # end of each UTC day
    start_cash: float = START_CASH  # what the first day's return is measured from


def validate(weights: Mapping[str, float]) -> None:
    unknown = set(weights) - set(UNIVERSE)
    if unknown:
        raise ValueError(f"unknown symbols: {sorted(unknown)}")
    if not all(math.isfinite(w) for w in weights.values()):
        raise ValueError("weights must be finite numbers")
    if any(w < 0 for w in weights.values()):
        raise ValueError("long-only: weights must be >= 0")
    if sum(weights.values()) > 1 + 1e-9:
        raise ValueError("no leverage: weights must sum to <= 1")


_CLOSE, _OPEN, _DECIDE = 0, 1, 2  # order of events that share a timestamp


def simulate(
    decisions: Iterable[Decision],
    history: History,
    start_cash: float = START_CASH,
    costs: Mapping[str, Costs] = COSTS,
    band: float = BAND,
) -> Result:
    events: list[tuple[datetime, int, str, float, int]] = []
    for sym, bars in history.items():
        cls = UNIVERSE[sym]
        for b in bars:
            events.append((open_time(cls, b.date), _OPEN, sym, b.open, 0))
            events.append((close_time(cls, b.date), _CLOSE, sym, b.close, 0))
    decs = sorted(decisions, key=lambda d: d.time)
    for i, d in enumerate(decs):
        validate(d.weights)
        events.append((d.time, _DECIDE, "", 0.0, i))
    events.sort(key=lambda e: (e[0], e[1]))

    res = Result(cash=start_cash, positions={s: 0.0 for s in history}, start_cash=start_cash)
    price: dict[str, float] = {}
    pending: dict[str, float] = {}  # symbol -> target weight not yet executed
    started = False
    day: date | None = None

    def equity() -> float:
        return res.cash + sum(q * price.get(s, 0.0) for s, q in res.positions.items())

    i = 0
    while i < len(events):
        t, kind = events[i][0], events[i][1]
        group = []
        while i < len(events) and events[i][0] == t and events[i][1] == kind:
            group.append(events[i])
            i += 1
        # A close at midnight ends the previous day; everything else belongs to its own date.
        ev_day = (t - timedelta(microseconds=1)).date() if kind == _CLOSE else t.date()
        if started and day is not None and ev_day > day:
            res.equity.append((day, equity()))
        day = ev_day

        if kind == _DECIDE:
            started = True
            w = decs[group[-1][4]].weights
            pending = {s: w.get(s, 0.0) for s in history}
            continue
        for _, _, sym, px, _ in group:
            price[sym] = px
        if kind == _OPEN:
            _execute(t, [g[2] for g in group if g[2] in pending], pending, res, price, costs, band)
    if started and day is not None:
        res.equity.append((day, equity()))
    return res


def _execute(
    t: datetime,
    syms: list[str],
    pending: dict[str, float],
    res: Result,
    price: Mapping[str, float],
    costs: Mapping[str, Costs],
    band: float,
) -> None:
    eq = res.cash + sum(q * price.get(s, 0.0) for s, q in res.positions.items())
    trades = []
    for sym in syms:
        target = pending.pop(sym)
        held = res.positions[sym]
        delta = target * eq - held * price[sym]
        full_exit = target == 0 and held > 0
        if full_exit or abs(delta) >= band * eq:
            trades.append((delta, sym, full_exit))
    for delta, sym, full_exit in sorted(trades):  # sells (negative) first, to free cash
        c = costs[UNIVERSE[sym]]
        if delta < 0:
            px = price[sym] * (1 - c.slip)
            qty = res.positions[sym] if full_exit else min(-delta / price[sym], res.positions[sym])
            fee = qty * px * c.fee
            res.cash += qty * px - fee
            res.positions[sym] -= qty
            res.fills.append(Fill(t, sym, -qty, px, fee))
        else:
            px = price[sym] * (1 + c.slip)
            spend = min(delta / price[sym] * px * (1 + c.fee), res.cash)
            if spend <= 0:
                continue
            qty = spend / (px * (1 + c.fee))
            fee = qty * px * c.fee
            res.cash -= qty * px + fee
            res.positions[sym] += qty
            res.fills.append(Fill(t, sym, qty, px, fee))


def backtest(strategy: Strategy, history: History, start: date, end: date) -> list[Decision]:
    """One decision per day at DECIDE_AT UTC, each seeing only bars closed by then."""
    out = []
    d = start
    while d <= end:
        t = datetime.combine(d, DECIDE_AT, tzinfo=UTC)
        weights, _ = strategy(visible_history(history, t))
        out.append(Decision(t, weights))
        d += timedelta(days=1)
    return out
