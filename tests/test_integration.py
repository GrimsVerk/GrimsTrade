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
