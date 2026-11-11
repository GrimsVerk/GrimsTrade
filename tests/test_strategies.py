"""Behaviour of the M1 classic strategies and their shared signal helpers, on synthetic bars."""

import math
from datetime import date, timedelta

import pytest

from grimstrade import gym, signals
from grimstrade.data import UNIVERSE, Bar, History
from grimstrade.strategies import LIVE, NOTES, ts_momentum

END = date(2026, 11, 10)


def series(days: int, trend: float, wiggle: float = 0.01, etf: bool = False) -> list[Bar]:
    """`days` calendar days ending at END; price drifts by `trend` per day with a small zigzag.
    ETFs skip weekends."""
    out = []
    for i in range(days):
        d = END - timedelta(days=days - 1 - i)
        if etf and d.weekday() >= 5:
            continue
        px = 100 * math.exp(trend * i + wiggle * (-1) ** i)
        out.append(Bar(d, px, px, px, px, 1.0))
    return out


def universe(days: int, trends: dict[str, float]) -> History:
    return {s: series(days, t, etf=UNIVERSE[s] == "etf") for s, t in trends.items()}


# --- signals ---


def test_trailing_return_needs_the_full_lookback() -> None:
    bars = series(100, 0.0, wiggle=0.0)
    assert signals.trailing_return(bars, 100) is None
    assert signals.trailing_return(bars, 99) == pytest.approx(0.0)


def test_trailing_return_uses_the_last_close_on_or_before_the_start() -> None:
    bars = [Bar(date(2026, 1, d), 0, 0, 0, c, 0) for d, c in ((1, 100.0), (5, 110.0), (9, 121.0))]
    # 6 days before 01-09 is 01-03: the close on or before it is 01-01's.
    assert signals.trailing_return(bars, 6) == pytest.approx(0.21)
    assert signals.trailing_return(bars, 4) == pytest.approx(0.10)


def test_vol_of_a_steady_zigzag() -> None:
    rets = [0.01, -0.01] * 50
    assert signals.realized_vol(rets, 252) == pytest.approx(0.01 * math.sqrt(252), rel=0.02)
    assert signals.ewma_vol(rets, 60, 252) == pytest.approx(0.01 * math.sqrt(252), rel=0.02)
    assert signals.realized_vol([0.01], 252) is None


def test_ewma_vol_weights_recent_returns_more() -> None:
    calm_then_wild = [0.001, -0.001] * 100 + [0.05, -0.05] * 10
    wild_then_calm = [0.05, -0.05] * 10 + [0.001, -0.001] * 100
    a = signals.ewma_vol(calm_then_wild, 60, 365)
    b = signals.ewma_vol(wild_then_calm, 60, 365)
    assert a is not None and b is not None and a > 2 * b


# --- every live strategy ---


@pytest.mark.parametrize("name", sorted(LIVE))
@pytest.mark.parametrize("days", [0, 30, 400, 800])
def test_every_strategy_gives_valid_weights_and_a_reason(name: str, days: int) -> None:
    trends = {"BTC": 0.002, "ETH": -0.002, "SPY": 0.0005, "QQQ": 0.001, "GLD": -0.0003, "TLT": 0.0}
    weights, reason = LIVE[name](universe(days, trends) if days else {})
    gym.validate(weights)
    assert reason


def test_every_live_strategy_has_a_try_note() -> None:
    assert set(NOTES) == set(LIVE)


# --- time-series momentum ---


def test_ts_momentum_holds_risers_and_drops_fallers() -> None:
    hist = universe(400, {"BTC": 0.002, "ETH": -0.002, "SPY": 0.0005, "TLT": -0.0005})
    weights, reason = ts_momentum.decide(hist)
    assert set(weights) == {"BTC", "SPY"}
    assert "ETH" in reason


def test_ts_momentum_sizes_by_volatility_and_never_levers() -> None:
    calm = series(400, 0.001, wiggle=0.001)  # ~3% vol: 40% target would mean 13x, capped at 1
    wild = series(400, 0.001, wiggle=0.03)  # ~57% vol
    weights, _ = ts_momentum.decide({"BTC": wild, "ETH": calm})
    assert weights["ETH"] == pytest.approx(0.5)  # capped at 1 / N
    vol = signals.ewma_vol(signals.daily_returns(wild), 60, 365)
    assert vol is not None
    assert weights["BTC"] == pytest.approx(0.40 / vol / 2)


def test_ts_momentum_waits_for_twelve_months() -> None:
    assert ts_momentum.decide(universe(300, {"BTC": 0.01})) == (
        {},
        "ts momentum: no asset has 12 months of history yet, stay in cash",
    )
