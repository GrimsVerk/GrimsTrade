from datetime import UTC, date, datetime, timedelta

import pytest

from grimstrade import gym
from grimstrade.data import Bar, History
from grimstrade.gym import Decision

NO_COSTS = {"crypto": gym.Costs(0, 0), "etf": gym.Costs(0, 0)}


def bars(start: str, opens_closes: list[tuple[float, float]], step: int = 1) -> list[Bar]:
    d0 = date.fromisoformat(start)
    return [
        Bar(d0 + timedelta(days=i * step), o, max(o, c), min(o, c), c, 1.0)
        for i, (o, c) in enumerate(opens_closes)
    ]


def at(d: str, hh: int = 22, mm: int = 30) -> datetime:
    return datetime.fromisoformat(d).replace(hour=hh, minute=mm, tzinfo=UTC)


def test_fills_at_next_open_with_fee_and_slippage() -> None:
    hist: History = {"BTC": bars("2026-11-01", [(100, 110), (120, 130), (140, 150)])}
    res = gym.simulate([Decision(at("2026-11-01"), {"BTC": 1.0})], hist)
    (fill,) = res.fills
    assert fill.time == datetime(2026, 11, 2, tzinfo=UTC)
    assert fill.price == pytest.approx(120 * 1.0005)
    assert fill.qty == pytest.approx(10_000 / (120 * 1.0005 * 1.0025))
    assert fill.fee == pytest.approx(fill.qty * fill.price * 0.0025)
    assert res.cash == pytest.approx(0, abs=1e-6)
    # Marked at the last close.
    last_day, last_eq = res.equity[-1]
    assert last_day == date(2026, 11, 3)
    assert last_eq == pytest.approx(fill.qty * 150)


def test_etf_order_on_friday_fills_monday_open() -> None:
    # 2026-11-06 is a Friday; the next ETF bar is Monday 11-09.
    hist: History = {
        "SPY": [*bars("2026-11-05", [(10, 10), (11, 11)]), *bars("2026-11-09", [(12, 13)])]
    }
    res = gym.simulate([Decision(at("2026-11-06"), {"SPY": 1.0})], hist, costs=NO_COSTS)
    (fill,) = res.fills
    assert fill.time.date() == date(2026, 11, 9) and fill.price == 12


def test_decision_never_fills_at_an_open_before_it() -> None:
    # Decided at 14:00 UTC, after that day's ETF open (13:30): must wait for the next bar.
    hist: History = {"SPY": bars("2026-11-09", [(10, 10), (20, 20)])}
    res = gym.simulate([Decision(at("2026-11-09", 14, 0), {"SPY": 1.0})], hist, costs=NO_COSTS)
    assert res.fills[0].price == 20


def test_switch_sells_first_and_keeps_full_value_without_costs() -> None:
    hist: History = {
        "BTC": bars("2026-11-01", [(100, 100), (100, 100), (200, 200)]),
        "ETH": bars("2026-11-01", [(10, 10), (10, 10), (10, 10)]),
    }
    decisions = [Decision(at("2026-11-01"), {"BTC": 1.0}), Decision(at("2026-11-02"), {"ETH": 1.0})]
    res = gym.simulate(decisions, hist, costs=NO_COSTS)
    assert res.positions["BTC"] == 0
    # BTC bought at 100 on 11-02, sold at 200 on 11-03 open, all proceeds into ETH at 10.
    assert res.positions["ETH"] == pytest.approx(2000)
    assert res.equity[-1][1] == pytest.approx(20_000)


def test_round_trip_costs_are_charged_both_ways() -> None:
    hist: History = {"BTC": bars("2026-11-01", [(100, 100)] * 3)}
    decisions = [Decision(at("2026-11-01"), {"BTC": 1.0}), Decision(at("2026-11-02"), {})]
    res = gym.simulate(decisions, hist)
    qty = 10_000 / (100 * 1.0005 * 1.0025)
    expected = qty * 100 * 0.9995 * (1 - 0.0025)
    assert res.cash == pytest.approx(expected)
    assert res.cash < 10_000


def test_partial_weights_keep_cash_and_small_drift_is_not_traded() -> None:
    hist: History = {"BTC": bars("2026-11-01", [(100, 100), (100, 100), (101, 101), (101, 101)])}
    decisions = [Decision(at(f"2026-11-0{d}"), {"BTC": 0.5}) for d in (1, 2, 3)]
    res = gym.simulate(decisions, hist, costs=NO_COSTS)
    assert len(res.fills) == 1  # later drift is under the 1% band
    assert res.cash == pytest.approx(5_000)


@pytest.mark.parametrize("w", [{"BTC": -0.1}, {"BTC": 0.7, "SPY": 0.4}, {"DOGE": 0.1}])
def test_rejects_shorts_leverage_and_unknown_symbols(w: dict[str, float]) -> None:
    with pytest.raises(ValueError):
        gym.simulate([Decision(at("2026-11-01"), w)], {"BTC": []})


def test_backtest_strategy_sees_only_closed_bars() -> None:
    hist: History = {
        "BTC": bars("2026-11-01", [(1, 1)] * 10),
        "SPY": bars("2026-11-02", [(1, 1)] * 5),
    }
    seen: list[tuple[date, date | None, date | None]] = []

    def spy(h: History) -> tuple[dict[str, float], str]:
        last = {s: (b[-1].date if b else None) for s, b in h.items()}
        seen.append((date.min, last["BTC"], last["SPY"]))
        return {}, ""

    decisions = gym.backtest(spy, hist, date(2026, 11, 3), date(2026, 11, 5))
    for dec, (_, btc, spy_last) in zip(decisions, seen, strict=True):
        d = dec.time.date()
        assert btc == d - timedelta(days=1)  # today's crypto bar is still open at 22:30
        assert spy_last == d  # today's ETF bar closed at 21:00
