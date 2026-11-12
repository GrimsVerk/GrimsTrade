"""Honesty audit 2026-11: the gym (simulated broker). Findings G1-G4 in
docs/audits/honesty-2026-11.md, plus invariants that held up under random testing."""

import math
import random
from datetime import UTC, date, datetime, time, timedelta

import pytest

from grimstrade import gym
from grimstrade.data import Bar, History
from grimstrade.gym import Decision

NO_COSTS = {"crypto": gym.Costs(0, 0), "etf": gym.Costs(0, 0)}
DAY1 = date(2026, 11, 2)  # a Monday


def at(day: int, hh: int = 22, mm: int = 30) -> datetime:
    return datetime.combine(DAY1 + timedelta(days=day), time(hh, mm), tzinfo=UTC)


def flat(n: int, px: float, weekdays_only: bool = False) -> list[Bar]:
    days = [DAY1 + timedelta(days=i) for i in range(n)]
    return [Bar(d, px, px, px, px, 1.0) for d in days if not weekdays_only or d.weekday() < 5]


@pytest.mark.xfail(
    strict=True,
    reason="audit G1: NaN weights pass validation (NaN is neither < 0 nor > 1); the gym then "
    "quietly keeps the old position and the ledger records NaN",
)
def test_nan_weights_are_rejected() -> None:
    with pytest.raises(ValueError):
        gym.validate({"BTC": math.nan})


def test_nan_weights_today_mean_keep_whatever_you_hold() -> None:
    """What G1 does in practice: the strategy wanted out (or in), a division by zero produced
    NaN, and the portfolio just stays as it was, with no error anywhere."""
    hist: History = {"BTC": flat(5, 100.0)}
    decisions = [Decision(at(0), {"BTC": 1.0}), Decision(at(1), {"BTC": math.nan})]
    try:
        res = gym.simulate(decisions, hist, costs=NO_COSTS)
    except ValueError:
        return  # fixed: NaN is refused
    assert res.positions["BTC"] == pytest.approx(100.0) and len(res.fills) == 1


@pytest.mark.xfail(
    strict=True,
    reason="audit G2: an order that cannot be paid for when its market opens is dropped, not "
    "kept: moving from an ETF into crypto leaves the money in cash until a later decision",
)
def test_a_switch_from_etf_to_crypto_ends_up_in_crypto() -> None:
    hist: History = {"SPY": flat(12, 100.0, weekdays_only=True), "BTC": flat(12, 100.0)}
    # Monday: all in SPY. Wednesday 22:30: switch everything to BTC. No decision after that.
    decisions = [Decision(at(0), {"SPY": 1.0}), Decision(at(2), {"BTC": 1.0})]
    res = gym.simulate(decisions, hist, costs=NO_COSTS)
    # BTC opens Thursday 00:00, before SPY can be sold at 13:30: the buy finds no cash and is
    # forgotten. SPY is then sold, and the 10,000 sits in cash for good.
    assert res.positions["SPY"] == 0
    assert res.positions["BTC"] == pytest.approx(100.0)


def test_dividends_are_not_credited_which_costs_a_bond_fund_holder_about_4_percent_a_year() -> None:
    """Audit G4 (known gap, sized): prices are raw, so on each ex-dividend day the price drops by
    the payout and the holder gets nothing for it. A fund that only pays out its 0.36% a month
    (TLT's order of size) and otherwise goes nowhere shows about -4.2% a year here; a real holder
    would be flat. The benchmarks holding SPY/TLT are understated by this, crypto is not."""
    bars, px = [], 100.0
    for i in range(365):
        d = DAY1 + timedelta(days=i)
        if d.weekday() >= 5:
            continue
        if d.day == 1 or (d.day in (2, 3) and d.weekday() == 0):  # first session of the month
            px *= 1 - 0.0036
        bars.append(Bar(d, px, px, px, px, 1.0))
    res = gym.simulate([Decision(at(-1), {"TLT": 1.0})], {"TLT": bars}, costs=NO_COSTS)
    assert res.equity[-1][1] / gym.START_CASH - 1 == pytest.approx(-0.042, abs=0.004)


def test_random_trading_at_constant_prices_never_creates_money() -> None:
    """Invariant that held: with prices that never move, no sequence of decisions can make
    equity rise, cash go negative or a position go short; with costs it can only shrink."""
    rng = random.Random(11)
    hist: History = {
        "BTC": flat(60, 100.0),
        "ETH": flat(60, 10.0),
        "SPY": flat(60, 500.0, weekdays_only=True),
        "TLT": flat(60, 80.0, weekdays_only=True),
    }
    for costs in (NO_COSTS, gym.COSTS):
        decisions = []
        for day in range(55):
            raw = {s: rng.random() * rng.choice([0, 1]) for s in hist}
            total = sum(raw.values()) or 1.0
            scale = rng.random() / total  # weights sum to something in [0, 1)
            decisions.append(Decision(at(day, rng.randrange(24), rng.randrange(60)),
                                      {s: w * scale for s, w in raw.items()}))  # fmt: skip
        res = gym.simulate(decisions, hist, costs=costs)
        assert res.cash >= -1e-6 and all(q >= -1e-9 for q in res.positions.values())
        equity = [e for _, e in res.equity]
        assert len(res.fills) > 50
        if costs is NO_COSTS:
            assert all(e == pytest.approx(gym.START_CASH) for e in equity)
        else:
            assert all(b <= a + 1e-6 for a, b in zip(equity, equity[1:], strict=False))
            paid = sum(f.fee for f in res.fills)
            assert equity[-1] < gym.START_CASH - paid + 1e-6  # fees and slippage both hurt


def test_buy_and_hold_earns_exactly_first_fill_open_to_last_close() -> None:
    rng = random.Random(5)
    bars, px = [], 100.0
    for i in range(40):
        o = px * (1 + rng.uniform(-0.02, 0.02))
        c = o * (1 + rng.uniform(-0.05, 0.05))
        bars.append(Bar(DAY1 + timedelta(days=i), o, max(o, c), min(o, c), c, 1.0))
        px = c
    res = gym.simulate([Decision(at(3), {"BTC": 1.0})], {"BTC": bars}, costs=NO_COSTS)
    assert res.equity[-1][1] == pytest.approx(gym.START_CASH * bars[-1].close / bars[4].open)
