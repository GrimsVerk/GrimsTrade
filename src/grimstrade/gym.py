"""The gym: a simulated broker that replays decisions over real bars.

An order decided at time T fills at the open of each asset's first bar that opens after T, at
open * (1 +/- slippage), plus a fee on the traded value. Long-only, no leverage, fractional units.
A buy the cash cannot fully pay for keeps waiting and buys the rest at that asset's next open,
until a newer decision replaces it; while a decision's buys need more cash than there is, assets
above their target are sold down to it even inside the rebalance band (DECISIONS, audit G2).
Cash earns the rate passed in `rates`, accrued daily (DECISIONS, 2026-11-18, cash interest).
The same replay (`Replay`, one event loop) serves the live ledger, backtests and the RL
environment (`gym_env`), so they can't disagree on the rules.
Distributions are paid as cash at the open of the ex-date, on the units held before that open
(DECISIONS, audit G4); paid out, they are cash and earn the cash rate like any other.
"""

from __future__ import annotations

import bisect
import math
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time, timedelta

from grimstrade.data import (
    CRYPTO,
    ETF,
    UNIVERSE,
    Dividends,
    History,
    close_time,
    open_time,
    visible_history,
)

Weights = dict[str, float]
Strategy = Callable[[History], tuple[Weights, str]]
# (known from, annual rate as a fraction), oldest first: the cash rate as it became known.
Rates = Sequence[tuple[datetime, float]]

START_CASH = 10_000.0
# Skip a trade smaller than this share of equity (rebalance band), except a full exit.
BAND = 0.01
# Backtests decide once a day at this UTC time, like the daily runner.
DECIDE_AT = time(22, 30)


@dataclass(frozen=True)
class Costs:
    fee: float  # share of traded value (with `tiers`: the fee at no volume)
    slip: float  # half-spread + slippage, share of price
    # (30-day volume in USD from which it applies, fee) by rising volume; empty = flat `fee`
    tiers: tuple[tuple[float, float], ...] = ()

    def fee_at(self, volume: float) -> float:
        """The fee for an account that traded `volume` USD in this asset class in the last
        30 days."""
        return max((t for t in self.tiers if t[0] <= volume), default=(0.0, self.fee))[1]


# Kraken Pro spot taker fee by 30-day spot volume in USD (kraken.com/pro/fees, read 2026-11-12
# and again 2026-11-18; DECISIONS, crypto fee tiers). A fill at the open is a market order, so
# the taker fee applies. Each strategy is its own account; only its crypto fills count.
KRAKEN_TAKER: tuple[tuple[float, float], ...] = (
    (0, 0.0080), (2_500, 0.0060), (10_000, 0.0038), (25_000, 0.0035), (50_000, 0.0030),
    (100_000, 0.0025), (250_000, 0.0022), (500_000, 0.0020), (1_000_000, 0.0018),
    (2_500_000, 0.0015), (5_000_000, 0.0012), (10_000_000, 0.0010), (50_000_000, 0.0009),
    (100_000_000, 0.0008), (250_000_000, 0.0007), (400_000_000, 0.0006), (500_000_000, 0.0005),
)  # fmt: skip
VOLUME_WINDOW = timedelta(days=30)
COSTS: dict[str, Costs] = {
    CRYPTO: Costs(fee=0.0080, slip=0.0005, tiers=KRAKEN_TAKER),
    ETF: Costs(fee=0.0, slip=0.0002),
}


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
    income: list[tuple[datetime, str, float]] = field(default_factory=list)  # dividends paid
    # What one dollar of cash earned over each step of `equity` (the risk-free return): 0 when no
    # rates are passed. Sharpe is measured above it.
    cash_growth: list[float] = field(default_factory=list)


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


# Order of events that share a timestamp. A dividend is paid at its ex-date's open before that
# open's fills: a unit sold at that open still gets it, a unit bought there does not.
_CLOSE, _DIVIDEND, _OPEN, _DECIDE = 0, 1, 2, 3

DAYS_PER_YEAR = 365  # interest accrues rate / 365 per calendar day


def cash_rate(rates: Rates, day: date, known: Sequence[datetime] | None = None) -> float:
    """The annual rate cash earns on UTC day `day`: the newest rate known at the day's start
    (carried forward over holidays and gaps), 0 before any is known, never below 0. `known` is
    `[t for t, _ in rates]`, precomputed for speed."""
    start = datetime.combine(day, time(0, 0), tzinfo=UTC)
    i = bisect.bisect_right(known if known is not None else [t for t, _ in rates], start)
    return max(rates[i - 1][1], 0.0) if i else 0.0


def interest(cash: float, rate: float) -> float:
    """One day's interest on a cash balance. Negative cash (float dust; the gym never borrows) is
    charged at the same rate."""
    return cash * rate / DAYS_PER_YEAR


class Replay:
    """The gym's event loop, one decision at a time: the one copy of the replay rules.

    `simulate` is a loop of `decide` calls over it, and the RL environment
    (`gym_env.TradingEnv`) steps it, so both score by the same code. Events in time order (at
    one timestamp: closes, distributions, opens, then the decision); each UTC day that ends
    credits its interest on the closing cash and marks the account; days with no event at all
    (weekends, holidays) earn their interest too; the trades at each open go through
    `_execute`. Call `decide` with non-decreasing times, then `finish` once.

    No held-out guard: it replays whatever bars, distributions and rates it is given (the daily
    runner replays the record up to today). A train-only caller checks its inputs itself
    (`gym_env.check_train_only`).
    """

    def __init__(
        self,
        history: History,
        start_cash: float = START_CASH,
        costs: Mapping[str, Costs] = COSTS,
        band: float = BAND,
        dividends: Dividends | None = None,
        rates: Rates = (),
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
        self.res = Result(
            cash=start_cash, positions={s: 0.0 for s in history}, start_cash=start_cash
        )
        self.price: dict[str, float] = {}
        self.pending: dict[str, float] = {}  # symbol -> target weight not yet executed
        self.unpaid: set[str] = set()  # pending buys left over from an open whose cash ran out
        self.started = False  # a decision has been made (before it, no day is marked)
        self.day: date | None = None  # the UTC day of the last event or decision
        self.growth = 1.0  # of one dollar of cash since the last equity point
        self.step_growth = 1.0  # of one dollar of cash since `take_step_growth` was last called
        self.rates = sorted(rates, key=lambda r: r[0])
        self.known = [t for t, _ in self.rates]
        self.i = 0  # the next event to process

    def equity(self) -> float:
        """Cash plus positions at the latest known prices."""
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

    def _accrue(self, d: date) -> None:  # day d is over: credit its interest on the closing cash
        r = cash_rate(self.rates, d, self.known)
        self.res.cash += interest(self.res.cash, r)
        self.growth *= 1 + r / DAYS_PER_YEAR
        self.step_growth *= 1 + r / DAYS_PER_YEAR

    def _new_day(self, t: datetime, kind: int) -> None:
        # A close at midnight ends the previous day; everything else belongs to its own date.
        ev_day = (t - timedelta(microseconds=1)).date() if kind == _CLOSE else t.date()
        if self.started and self.day is not None and ev_day > self.day:
            self._accrue(self.day)
            self.res.equity.append((self.day, self.equity()))
            self.res.cash_growth.append(self.growth - 1)
            self.growth = 1.0
            for k in range(1, (ev_day - self.day).days):  # days with no event (weekends) earn too
                self._accrue(self.day + timedelta(days=k))
        self.day = ev_day

    def _run_until(self, t: datetime | None) -> None:
        """Process every event that comes before a decision at `t` (all of them if None)."""
        ev, res, price = self.events, self.res, self.price
        while self.i < len(ev) and (t is None or ev[self.i][0] <= t):
            et, kind = ev[self.i][0], ev[self.i][1]
            group = []
            while self.i < len(ev) and ev[self.i][0] == et and ev[self.i][1] == kind:
                group.append(ev[self.i])
                self.i += 1
            self._new_day(et, kind)
            if kind == _DIVIDEND:
                for _, _, sym, amount in group:
                    if (paid := res.positions[sym] * amount) > 0:
                        res.cash += paid
                        res.income.append((et, sym, paid))
                continue
            for _, _, sym, px in group:
                price[sym] = px
            if kind == _OPEN:
                syms = [g[2] for g in group if g[2] in self.pending]
                _execute(et, syms, self.pending, self.unpaid, res, price, self.costs, self.band)

    def advance(self, t: datetime) -> None:
        """Bring the account up to a decision at `t`, without deciding."""
        self._run_until(t)
        self._new_day(t, _DECIDE)

    def decide(self, t: datetime, weights: Mapping[str, float]) -> None:
        """A decision at `t`: from now on these target weights replace any order still open. A
        second decision at the same `t` replaces the first."""
        validate(weights)
        self.advance(t)
        self.started = True
        self.pending = {s: weights.get(s, 0.0) for s in self.symbols}
        self.unpaid.clear()

    def finish(self, stop: datetime | None = None) -> Result:
        """Run the events before a decision at `stop` (all of them if None) and mark the last
        day. Its interest is not credited: the day is not over."""
        self._run_until(stop)
        if self.started and self.day is not None:
            self.res.equity.append((self.day, self.equity()))
            self.res.cash_growth.append(self.growth - 1)
        return self.res

    def take_step_growth(self) -> float:
        """What one dollar of cash grew to since the last call (RL rewards above cash)."""
        g, self.step_growth = self.step_growth, 1.0
        return g


def simulate(
    decisions: Iterable[Decision],
    history: History,
    start_cash: float = START_CASH,
    costs: Mapping[str, Costs] = COSTS,
    band: float = BAND,
    dividends: Dividends | None = None,
    rates: Rates = (),
) -> Result:
    """Replay `decisions` over `history` (module docstring for the rules). Every decision is
    checked before anything runs; decisions at one time count in the order given, the last one
    in force."""
    decs = sorted(decisions, key=lambda d: d.time)
    for d in decs:
        validate(d.weights)
    replay = Replay(history, start_cash, costs, band, dividends, rates)
    for d in decs:
        replay.decide(d.time, d.weights)
    return replay.finish()


def _execute(
    t: datetime,
    syms: list[str],
    pending: dict[str, float],
    unpaid: set[str],
    res: Result,
    price: Mapping[str, float],
    costs: Mapping[str, Costs],
    band: float,
) -> None:
    eq = res.cash + sum(q * price.get(s, 0.0) for s, q in res.positions.items())
    # Cash the decision's buys still need (outside the band; assets opening now or later, at the
    # latest known prices). When the cash on hand does not cover it, assets above their target
    # are sold down to it even inside the band, so the buys can be paid (audit G2).
    need = sum(
        d
        for s, w in pending.items()
        if s in price and (d := w * eq - res.positions[s] * price[s]) >= band * eq
    )
    short = need > res.cash
    trades = []
    for sym in syms:
        target = pending.pop(sym)
        held = res.positions[sym]
        delta = target * eq - held * price[sym]
        full_exit = target == 0 and held > 0
        funding = short and delta < -1e-9 * eq
        if sym in unpaid:  # a leftover buy only ever buys
            unpaid.discard(sym)
            if delta < 0:
                continue
        if full_exit or funding or abs(delta) >= band * eq:
            trades.append((delta, sym, full_exit, target))
    # Each asset class's fee for fills at this open: by the volume of its fills in the 30 days
    # before (not those at this same open).
    since = t - VOLUME_WINDOW
    rate: dict[str, float] = {}
    for cls in {UNIVERSE[s] for _, s, _, _ in trades}:
        volume = sum(abs(f.qty) * f.price for f in res.fills
                     if since < f.time < t and UNIVERSE[f.symbol] == cls)  # fmt: skip
        rate[cls] = costs[cls].fee_at(volume)
    for delta, sym, full_exit, target in sorted(trades):  # sells (negative) first, to free cash
        c = costs[UNIVERSE[sym]]
        fee_rate = rate[UNIVERSE[sym]]
        if delta < 0:
            px = price[sym] * (1 - c.slip)
            qty = res.positions[sym] if full_exit else min(-delta / price[sym], res.positions[sym])
            fee = qty * px * fee_rate
            res.cash += qty * px - fee
            res.positions[sym] -= qty
            res.fills.append(Fill(t, sym, -qty, px, fee))
        else:
            px = price[sym] * (1 + c.slip)
            wanted = delta / price[sym] * px * (1 + fee_rate)
            spend = min(wanted, res.cash)
            if spend < wanted:  # not fully paid: try the rest again at this asset's next open
                pending[sym] = target
                unpaid.add(sym)
            if spend <= 0:
                continue
            qty = spend / (px * (1 + fee_rate))
            fee = qty * px * fee_rate
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
