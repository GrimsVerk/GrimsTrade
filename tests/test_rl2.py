"""The residual agent of research run rl-2 can only tilt `tsmom12`, and with no tilt it IS
`tsmom12`.

- `rl2_env.residual`: zero scores give the base weights exactly; any scores stay within half a
  slot of the base, never below 0, coins never above their base weight, total at most 1.
- Zero tilt replayed through `gym.simulate` gives the same daily equity as the `tsmom12`
  baseline's own decisions (synthetic bars with holidays and assets that start late).
- In training episodes, zero scores earn exactly zero reward (the agent equals the `tsmom12`
  account beside it).
"""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from grimstrade import data, gym
from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
START = date(2020, 1, 1)
HOLIDAYS = {date(2021, 7, 2), date(2021, 1, 18), date(2021, 4, 2), date(2021, 12, 24)}


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mods: dict[str, ModuleType] = {}
    for name in ("harness", "common", "rl_sim", "rl_env", "rl2_env"):
        spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        mods[name] = mod
    yield mods
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path


def walk(rng: random.Random, days: list[date], p0: float, vol: float, drift: float) -> list[Bar]:
    out, p = [], p0
    for d in days:
        o = p * math.exp(rng.gauss(0, vol / 3))
        c = o * math.exp(rng.gauss(drift, vol))
        out.append(Bar(d, o, max(o, c) * 1.01, min(o, c) * 0.99, c, 1000.0))
        p = c
    return out


def history(seed: int, n_days: int = 1000) -> dict[str, list[Bar]]:
    rng = random.Random(seed)
    cal = [START + timedelta(days=i) for i in range(n_days)]
    biz = [d for d in cal if d.weekday() < 5 and d not in HOLIDAYS]
    return {
        "SPY": walk(rng, biz, 300, 0.012, 0.0005),
        "QQQ": walk(rng, [d for d in biz if d >= date(2020, 6, 1)], 200, 0.018, -0.0005),
        "TLT": walk(rng, biz, 120, 0.008, 0.0),
        "BTC": walk(rng, cal[20:], 9000, 0.04, 0.001),
        "ETH": walk(rng, cal[200:], 400, 0.05, -0.001),
    }


def table(lib: dict[str, ModuleType], hist: dict[str, list[Bar]]) -> Any:
    env, r2 = lib["rl_env"], lib["rl2_env"]
    t = env.build_table(hist, lambda d: [math.nan] * len(env.MACRO_FEATS), START,
                        START + timedelta(days=980))  # fmt: skip
    return r2.base_weights(hist, t)


def test_residual_bounds(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    r2 = lib["rl2_env"]
    rng = np.random.default_rng(0)
    coin = np.array([True, True, False, False, False, False])
    for _ in range(200):
        live = rng.random((8, 6)) < 0.8
        n = live.sum(1, keepdims=True).clip(min=1)
        b = np.where(live & (rng.random((8, 6)) < 0.6), 1 / n, 0.0)
        elig = live & (rng.random((8, 6)) < 0.9)
        assert np.array_equal(r2.residual(b, live, elig, coin, np.zeros((8, 6))), b)
        w = r2.residual(b, live, elig, coin, rng.normal(0, 3, (8, 6)))
        assert (w >= 0).all()
        assert (w.sum(1) <= 1 + 1e-9).all()
        assert (w[:, coin] <= b[:, coin] + 1e-12).all()
        unscaled = w.sum(1) < 1 - 1e-9
        assert (np.abs(w - b)[unscaled] <= (0.5 / n + 1e-12).repeat(6, 1)[unscaled]).all()
        assert (w[~(live & elig)] <= b[~(live & elig)] + 1e-12).all()


@pytest.mark.parametrize("seed", [1, 2])
def test_zero_tilt_is_tsmom12(lib: dict[str, ModuleType], seed: int) -> None:
    np: Any = pytest.importorskip("numpy")
    h, c, r2 = lib["harness"], lib["common"], lib["rl2_env"]
    hist = history(seed)
    rt = table(lib, hist)
    t = rt.t
    i0 = t.index(date(2021, 1, 4))
    end = date(2022, 9, 1)
    i1 = t.index(end)
    bd = r2.base_daily(hist, t.book.syms, t.fridays[i0], end)
    assert bd.sum() > 0
    zero = np.zeros((i1 - i0, 1, len(t.book.syms)))
    got = gym.simulate(r2.res_decisions(rt, i0, zero, bd, end), hist)
    ref_decs = h.decisions(c.weekly(c.slots(c.tsmom_signal)), h.Panel(hist), t.fridays[i0], end)
    ref = gym.simulate(ref_decs, hist)
    assert len(ref.fills) > 5
    assert got.equity == ref.equity


def test_zero_scores_earn_zero_reward(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    r2 = lib["rl2_env"]
    rt = table(lib, history(3))
    lo = int(np.argmax(rt.B.sum(1) > 0))
    env = r2.ResEnv(rt, 8, np.random.default_rng(1), lo, len(rt.t.fridays) - 2, horizon=20)
    total = 0.0
    for _ in range(45):
        o = env.obs()
        assert np.array_equal(o.b, rt.B[env.f])
        r, _ = env.step(np.zeros_like(o.b))
        total += float(np.abs(r).sum())
    assert total == 0.0
    r, _ = env.step(np.full_like(env.obs().b, -3.0))  # cutting everything: a nonzero reward
    assert np.abs(r).sum() > 0
