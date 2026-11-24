"""lagcost-1 (research/lib/lagcost1.py): the lag harness delays fills and adds no look-ahead.

- (e0, c1) is exactly today's backtest (`gym.backtest` at 22:30): same weights, same equity.
- `scheduled(22:30, offset 0)` is `gym.backtest` too.
- A planted signal at bar j fills at the open of bar j+1+k, for coins and for ETFs (weekends
  skipped), and the other class's lag does not move it.
- No decision sees a bar that closes after the earliest fill it can cause.
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Iterator, Mapping, Sequence
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from types import ModuleType

import pytest

from grimstrade import data, gym
from grimstrade.data import CRYPTO, UNIVERSE, Bar, close_time, open_time
from grimstrade.strategies import equal_weight, presets, ts_momentum, xs_momentum

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
START = date(2024, 1, 1)
DAYS = 500
JUMP = date(2025, 3, 5)  # a Wednesday: the planted signal's bar


@pytest.fixture(scope="module")
def lag() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mod = None
    for name in ("stats", "harness", "lagcost1"):
        spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    assert mod is not None
    yield mod
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path


def _bars(sym: str, jump: bool = False) -> list[Bar]:
    out = []
    px = 100.0
    for k in range(DAYS):
        d = START + timedelta(days=k)
        if UNIVERSE[sym] != CRYPTO and d.weekday() >= 5:
            continue
        nxt = px * (1 + 0.01 * ((k * 7 + len(sym)) % 5 - 2))
        if jump:
            nxt = 200.0 if d >= JUMP else 50.0
        out.append(Bar(d, px, max(px, nxt), min(px, nxt), nxt, 1.0))
        px = nxt
    return out


def _history(planted: str | None = None) -> dict[str, list[Bar]]:
    return {s: _bars(s, jump=s == planted) for s in ("BTC", "ETH", "SPY", "QQQ", "GLD", "TLT")}


def _same_weights(a: Sequence[gym.Decision], b: Sequence[gym.Decision]) -> None:
    assert len(a) == len(b)
    for x, y in zip(a, b, strict=True):
        assert set(x.weights) == set(y.weights)
        assert all(abs(x.weights[s] - y.weights[s]) < 1e-12 for s in x.weights)


STRATEGIES = [equal_weight.decide, ts_momentum.decide, xs_momentum.decide, presets.careful]


@pytest.mark.parametrize("strategy", STRATEGIES)
def test_e0_c1_is_todays_backtest(lag: ModuleType, strategy: gym.Strategy) -> None:
    hist = _history()
    a, b = START + timedelta(days=380), START + timedelta(days=DAYS - 10)
    ours = lag.lagged(strategy, hist, a, b, 0, 1)
    ref = gym.backtest(strategy, hist, a, b)
    _same_weights(ours, ref)
    assert gym.simulate(ours, hist).equity == gym.simulate(ref, hist).equity
    _same_weights(lag.scheduled(strategy, hist, a, b, time(22, 30), 0), ref)


def _hold_if_jumped(sym: str) -> gym.Strategy:
    def decide(history: Mapping[str, Sequence[Bar]]) -> tuple[dict[str, float], str]:
        bars = history[sym]
        return ({sym: 1.0} if bars and bars[-1].close > 100 else {}), "planted"

    return decide


@pytest.mark.parametrize("sym", ["BTC", "SPY"])
@pytest.mark.parametrize("k", [0, 1, 2, 5])
@pytest.mark.parametrize("other", [0, 3])
def test_lag_k_delays_the_fill_by_k_bars(lag: ModuleType, sym: str, k: int, other: int) -> None:
    hist = _history(planted=sym)
    coin = UNIVERSE[sym] == CRYPTO
    k_etf, k_coin = (other, k) if coin else (k, other)
    decs = lag.lagged(_hold_if_jumped(sym), hist, JUMP - timedelta(days=30),
                      JUMP + timedelta(days=30), k_etf, k_coin)  # fmt: skip
    fills = [f for f in gym.simulate(decs, hist).fills if f.symbol == sym and f.qty > 0]
    dates = [b.date for b in hist[sym]]
    j = dates.index(JUMP)
    assert fills[0].time == open_time(UNIVERSE[sym], dates[j + 1 + k])


def test_coin_lag_zero_fills_at_the_signal_close(lag: ModuleType) -> None:
    hist = _history(planted="BTC")
    decs = lag.lagged(_hold_if_jumped("BTC"), hist, JUMP - timedelta(days=5), JUMP, 0, 0)
    fill = next(f for f in gym.simulate(decs, hist).fills if f.symbol == "BTC")
    assert fill.time == close_time(CRYPTO, JUMP)  # the first price after bar JUMP closed


def _earliest_fill(hist: Mapping[str, Sequence[Bar]], t: datetime) -> datetime:
    return min(
        next(open_time(UNIVERSE[s], b.date) for b in bars if open_time(UNIVERSE[s], b.date) > t)
        for s, bars in hist.items()
    )


@pytest.mark.parametrize(
    "cfg", [(0, 0), (1, 0), (0, 1), (2, 2), (5, 5), "live"], ids=lambda c: str(c)
)
def test_no_decision_sees_past_its_first_fill(lag: ModuleType, cfg: object) -> None:
    hist = _history()
    seen: list[datetime] = []

    def spy(history: Mapping[str, Sequence[Bar]]) -> tuple[dict[str, float], str]:
        last = [close_time(UNIVERSE[s], b[-1].date) for s, b in history.items() if b]
        seen.append(max(last, default=datetime.min.replace(tzinfo=UTC)))
        return equal_weight.decide(history)

    a, b = START + timedelta(days=10), START + timedelta(days=DAYS - 20)
    if cfg == "live":
        decs = lag.scheduled(spy, hist, a, b, time(3, 0), 1)
        assert all(s <= d.time for s, d in zip(seen, decs, strict=True))
    else:
        assert isinstance(cfg, tuple)
        decs = lag.lagged(spy, hist, a, b, *cfg)
    assert len(seen) == len(decs)
    for s, d in zip(seen, decs, strict=True):
        assert s <= _earliest_fill(hist, d.time)
