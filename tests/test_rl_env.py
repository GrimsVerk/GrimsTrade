"""The RL environment (research run rl-1) follows the gym exactly and never looks ahead.

- `rl_sim.BatchSim` gives the same daily equity as `grimstrade.gym.simulate` for the same
  weights: synthetic bars with weekends, holidays, assets that start late, full exits, small
  trades inside the band, and cash-limited buys.
- `rl_env.build_table`: the inputs of a Friday decision do not change when every bar that closes
  after that decision is scrambled, and the macro function is only ever asked about the
  decision day itself (its as-of rule is proven in test_macro_asof.py).
"""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from collections.abc import Iterator
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from grimstrade import data, gym
from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mods: dict[str, ModuleType] = {}
    for name in ("rl_sim", "rl_env"):
        spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        mods[name] = mod
    yield mods
    # harness registers research-only symbols in UNIVERSE; undo that for the other tests
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path


START = date(2020, 1, 1)
HOLIDAYS = {date(2020, 1, 20), date(2020, 2, 17), date(2020, 4, 10), date(2020, 7, 3)}


def walk(rng: random.Random, days: list[date], p0: float, vol: float) -> list[Bar]:
    out, p = [], p0
    for d in days:
        o = p * math.exp(rng.gauss(0, vol / 3))
        c = o * math.exp(rng.gauss(0, vol))
        out.append(Bar(d, o, max(o, c) * 1.01, min(o, c) * 0.99, c, 1000.0))
        p = c
    return out


def history(seed: int, n_days: int = 760) -> dict[str, list[Bar]]:
    rng = random.Random(seed)
    cal = [START + timedelta(days=i) for i in range(n_days)]
    biz = [d for d in cal if d.weekday() < 5 and d not in HOLIDAYS]
    return {
        "SPY": walk(rng, biz, 300, 0.012),
        "QQQ": walk(rng, [d for d in biz if d >= date(2020, 6, 1)], 200, 0.018),
        "TLT": walk(rng, biz, 120, 0.008),
        "BTC": walk(rng, cal[20:], 9000, 0.04),
        "ETH": walk(rng, cal[300:], 400, 0.05),
    }


def scramble(b: Bar, f: float) -> Bar:
    p = b.open * f
    return Bar(b.date, p, p, p, p, 1.0)


def random_weights(rng: random.Random, syms: list[str], live: set[str]) -> dict[str, float]:
    if rng.random() < 0.1:
        return {}
    raw = {s: rng.random() ** 2 if rng.random() < 0.8 else 0.0 for s in syms if s in live}
    tot = sum(raw.values()) + rng.random() * 0.5
    return {s: x / tot for s, x in raw.items() if tot > 0 and x > 0}


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_batch_sim_equals_gym(lib: dict[str, ModuleType], seed: int) -> None:
    np: Any = pytest.importorskip("numpy")
    sim = lib["rl_sim"]
    hist = history(seed)
    book = sim.make_book(hist)
    rng = random.Random(seed + 100)
    start = START + timedelta(days=5)
    days = (date(2021, 12, 31) - start).days + 1
    weights: list[dict[str, float]] = []
    w: dict[str, float] = {}
    for i in range(days):
        d = start + timedelta(days=i)
        live = {s for s, bars in hist.items() if bars[0].date < d}
        if i % 7 == 0 or rng.random() < 0.05:  # mostly weekly, sometimes mid-week
            w = random_weights(rng, book.syms, live)
        weights.append(w)
    decs = [
        gym.Decision(datetime.combine(start + timedelta(days=i), gym.DECIDE_AT, tzinfo=UTC), w)
        for i, w in enumerate(weights)
    ]
    res = gym.simulate(decs, hist)
    assert len(res.fills) > 100
    known = dict(res.equity)
    ref, cur = [], known[start]
    for i in range(days):
        cur = known.get(start + timedelta(days=i), cur)
        ref.append(cur)
    arr = [np.array([w.get(s, 0.0) for s in book.syms]) for w in weights]
    got = sim.replay_daily(book, start, arr)
    assert np.allclose(got, np.array(ref), rtol=1e-10, atol=0)


def test_week_steps_equal_daily_replay(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    sim, env = lib["rl_sim"], lib["rl_env"]
    book = sim.make_book(history(7))
    rng = np.random.default_rng(0)
    k0 = book.day(date(2021, 1, 1))  # a Friday
    weeks = 30
    w = rng.dirichlet(np.ones(len(book.syms) + 1), size=(weeks, 3))[:, :, :-1]
    batch = sim.BatchSim(book, 3)
    batch.reset()
    for i in range(weeks):
        env.step_week(batch, np.full(3, k0 + 7 * i), w[i])
    # finish the last Friday like a daily replay does: its decision, then the crypto close
    last = np.full(3, k0 + 7 * weeks)
    batch.decide(w[-1])
    batch.evening(last)
    for e in range(3):
        daily = [w[min(i // 7, weeks - 1), e] for i in range(7 * weeks + 1)]
        ref = sim.replay_daily(book, book.date(k0), daily)
        assert batch.equity()[e] == pytest.approx(ref[-1], rel=1e-12)


def test_inputs_ignore_the_future(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    env = lib["rl_env"]
    hist = history(11)
    asked: list[date] = []

    def macro_fn(d: date) -> list[float]:
        asked.append(d)
        return [float(d.toordinal() % 97)] * len(env.MACRO_FEATS)

    first, last = date(2021, 1, 1), date(2022, 1, 28)
    base = env.build_table(hist, macro_fn, first, last)
    assert asked == base.fridays
    assert base.elig.any(axis=0).all()  # every asset becomes eligible at some point
    rng = random.Random(5)
    for cut in (date(2021, 3, 5), date(2021, 7, 2), date(2021, 11, 26)):
        at = datetime.combine(cut, gym.DECIDE_AT, tzinfo=UTC)
        scrambled = {
            s: [
                b
                if data.close_time(data.UNIVERSE[s], b.date) <= at
                else scramble(b, rng.uniform(0.5, 2))
                for b in bars
            ]
            for s, bars in hist.items()
        }
        other = env.build_table(scrambled, macro_fn, first, last)
        i = base.fridays.index(cut)
        assert np.array_equal(base.X[: i + 1], other.X[: i + 1])
        assert np.array_equal(base.elig[: i + 1], other.elig[: i + 1])
        assert not np.array_equal(base.X[i + 1 :], other.X[i + 1 :])  # the scramble bites


def test_friday_uses_friday_etf_close_not_crypto(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    env = lib["rl_env"]
    hist = history(13)
    first, last = date(2021, 6, 4), date(2021, 6, 4)
    base = env.build_table(hist, lambda d: [0.0] * len(env.MACRO_FEATS), first, last)
    friday = date(2021, 6, 4)

    def bump(sym: str) -> Any:
        h = {s: list(b) for s, b in hist.items()}
        h[sym] = [Bar(b.date, b.open, b.high, b.low, b.close * 1.5, b.volume)
                  if b.date == friday else b for b in h[sym]]  # fmt: skip
        return env.build_table(h, lambda d: [0.0] * len(env.MACRO_FEATS), first, last)

    j = {s: i for i, s in enumerate(base.book.syms)}
    # SPY's Friday bar closes at 21:00, before the 22:30 decision: it is used.
    assert not np.array_equal(bump("SPY").X[0, j["SPY"]], base.X[0, j["SPY"]])
    # BTC's Friday bar closes at midnight, after the decision: it is not.
    assert np.array_equal(bump("BTC").X[0, j["BTC"]], base.X[0, j["BTC"]])
