"""The Gymnasium environment scores an agent by the gym's own rules (docs/gym-env.md).

- Driven with a classic strategy's weights (`ts_momentum`, `equal_weight`), it reproduces
  `gym.simulate`'s result for that strategy: the same equity curve, fills, cash and positions,
  with distributions, cash interest, ETF holidays and an asset that starts late. The same holds
  for a window that starts mid-history and for weekly decisions repeated daily.
- No look-ahead: scrambling every bar that has not closed by T (keeping the opens that already
  happened) changes no observation or reward up to T.
- Costs: a first all-in buy at flat prices loses exactly slippage and fee; the step's fees match
  the fills; the turnover penalty and the excess-of-cash reward do what they say.
- Episodes end where they should; seeded windows repeat.
- The held-out year (bars after 2025-11-10) is refused unless explicitly allowed, and the loader
  drops it.
- The daily runner does not import the environment or gymnasium.
"""

from __future__ import annotations

import csv
import math
import random
import subprocess
import sys
from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np
import pytest
from numpy.typing import NDArray

from grimstrade import gym
from grimstrade.data import UNIVERSE, Bar, Dividend, close_time, open_time, visible_history
from grimstrade.gym import Decision
from grimstrade.gym_env import (
    TRAIN_LAST_BAR,
    HeldOutError,
    TradingEnv,
    check_train_only,
    decide_time,
    load_train,
)
from grimstrade.strategies import equal_weight, ts_momentum

START = date(2022, 1, 3)
END = date(2023, 9, 29)
HOLIDAYS = {date(2022, 7, 4), date(2022, 12, 26), date(2023, 1, 16)}


def walk(sym: str, first: date, last: date, seed: int, etf: bool) -> list[Bar]:
    rng = random.Random(seed)
    out, px, d = [], 100.0, first
    while d <= last:
        if not etf or (d.weekday() < 5 and d not in HOLIDAYS):
            o = px * math.exp(rng.gauss(0, 0.005)) if etf else px  # ETFs gap overnight
            c = o * math.exp(rng.gauss(0.0004, 0.02))
            out.append(Bar(d, o, max(o, c) * 1.01, min(o, c) * 0.99, c, 1.0))
            px = c
        d += timedelta(days=1)
    return out


def make_history(last: date = END) -> dict[str, list[Bar]]:
    return {
        "BTC": walk("BTC", START, last, 1, etf=False),
        "ETH": walk("ETH", date(2022, 6, 1), last, 2, etf=False),  # starts late
        "SPY": walk("SPY", START, last, 3, etf=True),
        "TLT": walk("TLT", START, last, 4, etf=True),
    }


DIVIDENDS = {
    "SPY": [Dividend(date(2022, 3, 18), 0.4), Dividend(date(2023, 3, 17), 0.5)],
    "TLT": [Dividend(date(2022, 9, 1), 0.3)]
    + [
        Dividend(date(2023, m, 1) + timedelta(days=(7 - date(2023, m, 1).weekday()) % 7), 0.2)
        for m in range(2, 10)
    ],  # first Monday of each month
}
RATES: gym.Rates = [
    (datetime(2021, 12, 31, 21, tzinfo=UTC), 0.001),
    (datetime(2022, 6, 15, 21, tzinfo=UTC), 0.02),
    (datetime(2023, 3, 1, 21, tzinfo=UTC), 0.045),
]


Policy = Callable[[datetime], NDArray[np.float64]]


def drive(env: TradingEnv, policy: Policy) -> tuple[list[float], gym.Result, list[gym.Weights]]:
    """Run one episode; `policy(t)` gives the action at decision time t."""
    _, info = env.reset(seed=0)
    t = info["time"]
    rewards, chosen = [], []
    done = False
    while not done:
        _, r, term, trunc, info = env.step(policy(t))
        t = info["next_time"]
        rewards.append(float(r))
        chosen.append(info["weights"])
        done = term or trunc
    return rewards, info["result"], chosen


def strategy_policy(env: TradingEnv, strategy: gym.Strategy, hist: dict[str, list[Bar]]) -> Policy:
    def policy(t: datetime) -> NDArray[np.float64]:
        w, _ = strategy(visible_history(hist, t))
        return np.array([w.get(s, 0.0) for s in env.symbols])

    return policy


def assert_same(a: gym.Result, b: gym.Result) -> None:
    assert [d for d, _ in a.equity] == [d for d, _ in b.equity]
    np.testing.assert_allclose([e for _, e in a.equity], [e for _, e in b.equity], rtol=1e-12)
    np.testing.assert_allclose(a.cash_growth, b.cash_growth, rtol=1e-12, atol=1e-15)
    assert len(a.fills) == len(b.fills)
    for f, g in zip(a.fills, b.fills, strict=True):
        assert (f.time, f.symbol) == (g.time, g.symbol)
        assert f.qty == pytest.approx(g.qty, rel=1e-12)
        assert f.price == pytest.approx(g.price, rel=1e-12)
        assert f.fee == pytest.approx(g.fee, rel=1e-12, abs=1e-12)
    assert a.cash == pytest.approx(b.cash, rel=1e-12, abs=1e-9)
    assert a.positions == pytest.approx(b.positions, rel=1e-12)
    assert a.income == b.income


@pytest.mark.parametrize("strategy", [ts_momentum.decide, equal_weight.decide])
def test_classic_strategy_through_the_env_matches_simulate(strategy: gym.Strategy) -> None:
    hist = make_history()
    env = TradingEnv(hist, dividends=DIVIDENDS, cash_rates=RATES)
    rewards, got, _ = drive(env, strategy_policy(env, strategy, hist))
    want = gym.simulate(
        gym.backtest(strategy, hist, START, END), hist, dividends=DIVIDENDS, rates=RATES
    )
    assert len(want.fills) > 20 and want.income  # it really trades and is paid distributions
    assert_same(got, want)
    # The log rewards add up to the account's growth from the first decision to the last mark.
    assert sum(rewards) == pytest.approx(math.log(got.equity[-1][1] / gym.START_CASH), rel=1e-9)


def test_window_starting_mid_history_matches_simulate() -> None:
    hist = make_history()
    start = date(2023, 2, 1)
    env = TradingEnv(hist, start=start, dividends=DIVIDENDS, cash_rates=RATES)
    _, got, _ = drive(env, strategy_policy(env, ts_momentum.decide, hist))
    want = gym.simulate(
        gym.backtest(ts_momentum.decide, hist, start, END), hist, dividends=DIVIDENDS, rates=RATES
    )
    assert_same(got, want)


def test_weekly_decisions_repeat_daily_like_simulate() -> None:
    hist = make_history()
    env = TradingEnv(hist, weekday=4, dividends=DIVIDENDS, cash_rates=RATES)
    rng = np.random.default_rng(7)
    _, got, chosen = drive(env, lambda t: rng.uniform(0, 0.6, size=len(env.symbols)))
    assert all(d.weekday() == 4 for d in env.days)
    decisions = [
        Decision(decide_time(d + timedelta(days=k)), w)
        for d, w in zip(env.days, chosen, strict=True)
        for k in range(7)
    ]
    want = gym.simulate(decisions, hist, dividends=DIVIDENDS, rates=RATES)
    assert_same(got, want)


def test_action_is_long_only_unlevered_and_masked() -> None:
    env = TradingEnv(make_history(), start=date(2022, 3, 1))
    t = decide_time(date(2022, 3, 1))
    i = {s: j for j, s in enumerate(env.symbols)}
    a = np.zeros(4)
    a[i["BTC"]], a[i["SPY"]], a[i["TLT"]], a[i["ETH"]] = 2.0, 0.5, -1.0, 0.7
    w = env.weights(a, t)
    assert w["ETH"] == 0.0  # no ETH bar yet
    assert w["TLT"] == 0.0
    assert w["BTC"] == pytest.approx(1 / 1.5) and w["SPY"] == pytest.approx(0.5 / 1.5)
    assert sum(w.values()) == pytest.approx(1.0)
    small = env.weights(np.array([0.1, 0.0, 0.2, 0.3]), t)
    assert sum(small.values()) == pytest.approx(0.6)  # under 1: the rest stays cash


def scramble_after(hist: dict[str, list[Bar]], t: datetime, seed: int) -> dict[str, list[Bar]]:
    """Every bar not closed by `t` gets other prices; a bar already open at `t` keeps its open."""
    rng = random.Random(seed)
    out = {}
    for s, bars in hist.items():
        cls = UNIVERSE[s]
        new = []
        for b in bars:
            if close_time(cls, b.date) <= t:
                new.append(b)
                continue
            o = b.open if open_time(cls, b.date) <= t else b.open * rng.uniform(0.5, 2)
            c = b.close * rng.uniform(0.5, 2)
            new.append(replace(b, open=o, close=c, high=max(o, c) * 2, low=min(o, c) / 2))
        out[s] = new
    return out


def test_no_look_ahead_future_bars_change_nothing_up_to_t() -> None:
    hist = make_history()
    t = decide_time(date(2023, 3, 15))
    other = scramble_after(hist, t, seed=11)
    runs = []
    for h in (hist, other):
        env = TradingEnv(h, start=date(2023, 1, 2), dividends=DIVIDENDS, cash_rates=RATES)
        rng = np.random.default_rng(3)
        obs, info = env.reset(seed=0)
        seen = [(info["time"], obs, 0.0)]
        while seen[-1][0] < t:
            obs, r, _, _, info = env.step(rng.uniform(0, 0.5, size=4))
            seen.append((info["next_time"], obs, float(r)))
        runs.append(seen)
    assert runs[0][-1][0] == t
    for (ta, oa, ra), (tb, ob, rb) in zip(*runs, strict=True):
        assert ta == tb and ra == rb
        np.testing.assert_array_equal(oa, ob)
    # ... and the very next step does see the scrambled bars.
    assert not np.array_equal(
        TradingEnv(hist, start=date(2023, 3, 16))._market(decide_time(date(2023, 3, 16))),
        TradingEnv(other, start=date(2023, 3, 16))._market(decide_time(date(2023, 3, 16))),
    )


def flat(sym: str, n: int = 10) -> dict[str, list[Bar]]:
    first = date(2024, 3, 4)  # a Monday
    days = [first + timedelta(days=k) for k in range(n)]
    if UNIVERSE[sym] == "etf":
        days = [d for d in days if d.weekday() < 5]
    return {sym: [Bar(d, 100.0, 100.0, 100.0, 100.0, 1.0) for d in days]}


@pytest.mark.parametrize("sym,cost", [("BTC", (1.0005) * (1.008)), ("SPY", 1.0002)])
def test_first_buy_at_flat_prices_loses_exactly_slippage_and_fee(sym: str, cost: float) -> None:
    env = TradingEnv(flat(sym), start=date(2024, 3, 5))
    env.reset(seed=0)
    # Decided Tuesday night, filled at the next open, marked a day later at the same price.
    _, r, _, _, info = env.step(np.array([1.0]))
    assert r == pytest.approx(-math.log(cost), rel=1e-9)
    (fill,) = info["fills"]
    assert info["fees"] == pytest.approx(fill.fee) and info["turnover"] == pytest.approx(1.0)
    _, r2, _, _, info2 = env.step(np.array([1.0]))  # holding: nothing to trade, nothing lost
    assert r2 == pytest.approx(0.0, abs=1e-12) and info2["fills"] == []


def test_turnover_penalty_and_excess_reward() -> None:
    plain = TradingEnv(flat("SPY"))
    penal = TradingEnv(flat("SPY"), turnover_penalty=0.01)
    plain.reset(seed=0)
    penal.reset(seed=0)
    _, r0, *_ = plain.step(np.array([0.5]))
    _, r1, *_ = penal.step(np.array([0.5]))
    assert float(r0) - float(r1) == pytest.approx(0.005)
    rate = [(datetime(2024, 1, 1, tzinfo=UTC), 0.0365)]
    for name, want in (("log", math.log(1.0001)), ("excess_log", 0.0)):
        env = TradingEnv(flat("SPY"), cash_rates=rate, reward=name)
        env.reset(seed=0)
        _, r, _, _, info = env.step(np.array([0.0]))  # all cash for one day
        assert info["cash_growth"] == pytest.approx(1.0001)
        assert r == pytest.approx(want, abs=1e-12)


def test_episode_ends_on_the_last_decision_and_windows_are_seeded() -> None:
    hist = make_history()
    env = TradingEnv(hist, start=date(2023, 9, 20))
    env.reset(seed=0)
    flags = [env.step(np.zeros(4))[2:4] for _ in range(len(env.days))]
    assert flags[:-1] == [(False, False)] * (len(env.days) - 1) and flags[-1] == (False, True)
    with pytest.raises(RuntimeError):
        env.step(np.zeros(4))

    win = TradingEnv(hist, episode_steps=30)
    starts = [win.reset(seed=s)[1]["time"] for s in (1, 1, 2)]
    assert starts[0] == starts[1] != starts[2]
    for k in range(30):
        *_, trunc, info = win.step(np.full(4, 0.25))
        assert trunc == (k == 29)
    assert info["result"].equity


def test_held_out_year_is_refused_unless_allowed() -> None:
    hist = make_history()
    late = {**hist, "BTC": [*hist["BTC"], Bar(TRAIN_LAST_BAR + timedelta(1), 1, 1, 1, 1, 1)]}
    ok = {**hist, "BTC": [*hist["BTC"], Bar(TRAIN_LAST_BAR, 1, 1, 1, 1, 1)]}
    with pytest.raises(HeldOutError):
        TradingEnv(late)
    TradingEnv(ok)
    TradingEnv(late, allow_held_out=True)
    with pytest.raises(HeldOutError):
        TradingEnv(hist, end=TRAIN_LAST_BAR + timedelta(days=1))
    with pytest.raises(HeldOutError):
        check_train_only(hist, {"SPY": [Dividend(date(2025, 12, 1), 1.0)]})
    with pytest.raises(HeldOutError):
        check_train_only(hist, cash_rates=[(datetime(2025, 11, 11, 21, tzinfo=UTC), 0.04)])
    check_train_only(hist, cash_rates=[(datetime(2025, 11, 11, 3, tzinfo=UTC), 0.04)])


def test_load_train_drops_the_held_out_year(tmp_path: Path) -> None:
    (tmp_path / "data" / "bars").mkdir(parents=True)
    days = [date(2025, 11, 7), date(2025, 11, 10), date(2025, 11, 11)]
    with (tmp_path / "data" / "bars" / "SPY.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close", "volume"])
        for d in days:
            w.writerow([d.isoformat(), 1, 1, 1, 1, 1])
    with (tmp_path / "data" / "dividends.csv").open("w", newline="") as f:
        f.write("symbol,ex_date,amount\nSPY,2025-11-07,0.1\nSPY,2025-11-11,0.1\n")
    with (tmp_path / "data" / "rates.csv").open("w", newline="") as f:
        f.write(
            "date,rate,seen\n2025-11-10,4.0,2025-11-11T03:00:00+00:00\n"
            "2025-11-11,4.1,2025-11-12T03:00:00+00:00\n"
        )
    train = load_train(tmp_path, ["SPY"])
    assert [b.date for b in train.history["SPY"]] == days[:2]
    assert [d.ex_date for d in train.dividends["SPY"]] == [date(2025, 11, 7)]
    assert [r for _, r in train.rates] == [0.04]
    check_train_only(train.history, train.dividends, train.rates)
    full = load_train(tmp_path, ["SPY"], allow_held_out=True)
    assert len(full.history["SPY"]) == 3 and len(full.rates) == 2


def test_daily_runner_does_not_import_the_env() -> None:
    code = (
        "import sys, grimstrade.run_daily; "
        "bad = [m for m in ('grimstrade.gym_env', 'gymnasium') if m in sys.modules]; "
        "assert not bad, bad"
    )
    subprocess.run([sys.executable, "-c", code], check=True)


def test_passes_the_gymnasium_env_checker() -> None:
    from gymnasium.utils.env_checker import check_env

    with pytest.warns(UserWarning):  # only the unbounded observation Box is warned about
        check_env(TradingEnv(make_history(), start=date(2023, 6, 1)), skip_render_check=True)
