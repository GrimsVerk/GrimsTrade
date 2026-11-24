"""Interactions between gym rules that landed in separate PRs (integration preview
`docs/integrate-1.md`): each rule has its own tests; these check that they compose."""

from datetime import UTC, date, datetime, time, timedelta

import pytest

from grimstrade import gym
from grimstrade.data import Bar, Dividend, History
from grimstrade.gym import Decision

NO_COSTS = {"crypto": gym.Costs(0, 0), "etf": gym.Costs(0, 0)}
DAY1 = date(2026, 11, 2)  # a Monday


def at(day: int, hh: int = 22, mm: int = 30) -> datetime:
    return datetime.combine(DAY1 + timedelta(days=day), time(hh, mm), tzinfo=UTC)


def flat(n: int, px: float, weekdays_only: bool = False) -> list[Bar]:
    days = [DAY1 + timedelta(days=i) for i in range(n)]
    return [Bar(d, px, px, px, px, 1.0) for d in days if not weekdays_only or d.weekday() < 5]


def test_a_dividend_on_units_sold_to_fund_a_waiting_buy_is_spent_by_that_buy() -> None:
    """G2 x G4. All in SPY; Wednesday 22:30 switch to BTC. BTC opens Thursday 00:00 with no
    cash, so the buy waits (G2). Thursday is SPY's ex-date: the units sold at that open are paid
    first (G4), then sold. The waiting buy at Friday's BTC open spends both."""
    hist: History = {"SPY": flat(12, 100.0, weekdays_only=True), "BTC": flat(12, 100.0)}
    divs = {"SPY": [Dividend(DAY1 + timedelta(days=3), 1.0)]}
    decisions = [Decision(at(0), {"SPY": 1.0}), Decision(at(2), {"BTC": 1.0})]
    res = gym.simulate(decisions, hist, costs=NO_COSTS, dividends=divs)
    ((paid_at, sym, paid),) = res.income
    assert (paid_at, sym) == (at(3, 13, 30), "SPY")
    assert paid == pytest.approx(100.0)
    btc = [f for f in res.fills if f.symbol == "BTC"]
    assert [f.time for f in btc] == [at(4, 0, 0)]
    assert res.positions["BTC"] == pytest.approx(101.0)  # 10,000 from the sale + 100 paid
    assert res.cash == pytest.approx(0.0, abs=1e-6)


def test_a_buy_waiting_for_cash_pays_the_fee_tier_of_the_open_it_fills_at() -> None:
    """G2 x crypto fee tiers (#32). In and out of BTC (about 19,800 USD of crypto volume), then
    SPY, then back to BTC: that buy finds no cash at Thursday 00:00 and waits for the SPY sale.
    At Friday's open it pays the 0.38% tier of the volume before that open, and the fee is in its
    sizing, so cash never goes below zero."""
    hist: History = {"SPY": flat(12, 100.0, weekdays_only=True), "BTC": flat(12, 100.0)}
    decisions = [
        Decision(at(0), {"BTC": 1.0}),
        Decision(at(1), {"SPY": 1.0}),
        Decision(at(2), {"BTC": 1.0}),
    ]
    res = gym.simulate(decisions, hist)
    btc = [f for f in res.fills if f.symbol == "BTC"]
    assert [f.time for f in btc] == [at(1, 0, 0), at(2, 0, 0), at(4, 0, 0)]
    rates = [round(f.fee / abs(f.qty * f.price), 4) for f in btc]
    assert rates == [0.0080, 0.0060, 0.0038]
    assert res.cash >= -1e-9
    assert res.positions["SPY"] == 0


RATE = 0.0365  # 0.01% a day
RATES = [(datetime(2026, 10, 1, tzinfo=UTC), RATE)]  # known long before the replays below
DAILY = 1 + RATE / gym.DAYS_PER_YEAR


def test_a_dividend_paid_as_cash_earns_the_cash_rate() -> None:
    """G4 x cash interest (#61). All in SPY from Tuesday; Wednesday is an ex-date. The payout
    sits in cash (it is not reinvested by itself) and earns the T-bill rate every day after,
    weekends included, until the replay's last day (credited by the next run)."""
    hist: History = {"SPY": flat(12, 100.0, weekdays_only=True)}
    divs = {"SPY": [Dividend(DAY1 + timedelta(days=2), 1.0)]}
    decisions = [Decision(at(0), {"SPY": 1.0})]
    res = gym.simulate(decisions, hist, costs=NO_COSTS, dividends=divs, rates=RATES)
    ((_, _, paid),) = res.income
    assert paid == pytest.approx(res.positions["SPY"] * 1.0)
    # Wednesday 4 to Thursday 12 November credited (9 days); Friday 13 is the last day.
    assert res.cash == pytest.approx(paid * DAILY**9)
    no_rate = gym.simulate(decisions, hist, costs=NO_COSTS, dividends=divs)
    assert no_rate.cash == pytest.approx(100.0)


def test_cash_waiting_for_a_pending_buy_earns_interest_and_the_buy_spends_it() -> None:
    """G2 x cash interest (#61). SPY to BTC: the BTC buy waits from Thursday 00:00 for the SPY
    sale at 13:30. The proceeds sit in cash over Thursday night and earn one day's interest, which
    the waiting buy spends at Friday 00:00."""
    hist: History = {"SPY": flat(12, 100.0, weekdays_only=True), "BTC": flat(12, 100.0)}
    decisions = [Decision(at(0), {"SPY": 1.0}), Decision(at(2), {"BTC": 1.0})]
    res = gym.simulate(decisions, hist, costs=NO_COSTS, rates=RATES)
    spy_sold = next(f for f in res.fills if f.symbol == "SPY" and f.qty < 0)
    (btc,) = [f for f in res.fills if f.symbol == "BTC"]
    assert (spy_sold.time, btc.time) == (at(3, 13, 30), at(4, 0, 0))
    assert btc.qty == pytest.approx(-spy_sold.qty * DAILY)
    assert res.cash >= -1e-9
