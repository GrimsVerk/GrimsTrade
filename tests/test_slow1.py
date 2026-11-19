"""The slow-1 screen measures what its card says (research/slow-1.md).

- `horizon_z(t, h)` is the return from the first open after the Friday to the first open after
  the Friday `h` weeks later, over vol x sqrt(7h/365); `h` = 1 is rl-3's `week_z`.
- A rotation only reorders rows inside the span, by at least 52 weeks from either end.
- `fit_predict` is ordinary least squares with an intercept, predicting with the slopes only.
- The planted control has exactly the in-sample IC it claims.
"""

from __future__ import annotations

import importlib
import math
import random
import sys
from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from grimstrade import data
from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
START = date(2020, 1, 1)


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mods = {n: importlib.import_module(n) for n in ("rl_env", "rl3_plant", "slow1_ic")}
    yield mods
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path


def history(seed: int) -> dict[str, list[Bar]]:
    rng = random.Random(seed)
    cal = [START + timedelta(days=i) for i in range(1300)]
    biz = [d for d in cal if d.weekday() < 5 and d not in {date(2021, 7, 2), date(2022, 4, 15)}]

    def walk(days: list[date], p: float, vol: float) -> list[Bar]:
        out = []
        for d in days:
            o = p * math.exp(rng.gauss(0, vol / 3))
            c = o * math.exp(rng.gauss(0.0003, vol))
            out.append(Bar(d, o, max(o, c) * 1.01, min(o, c) * 0.99, c, 1000.0))
            p = c
        return out

    return {
        "SPY": walk(biz, 300, 0.012),
        "TLT": walk([d for d in biz if d >= date(2020, 9, 1)], 120, 0.008),
        "BTC": walk(cal[30:], 9000, 0.04),
    }


def table(lib: dict[str, ModuleType], seed: int) -> tuple[Any, dict[str, list[Bar]]]:
    env = lib["rl_env"]
    hist = history(seed)
    t = env.build_table(
        hist, lambda d: [math.nan] * len(env.MACRO_FEATS), START, START + timedelta(days=1280)
    )
    return t, hist


def test_horizon_z_is_the_held_window(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    s1, pl = lib["slow1_ic"], lib["rl3_plant"]
    t, hist = table(lib, 1)
    z1, zw = s1.horizon_z(t, 1), pl.week_z(t)
    assert np.array_equal(np.isnan(z1), np.isnan(zw))
    assert np.allclose(z1[np.isfinite(z1)], zw[np.isfinite(zw)], atol=1e-12)
    for h in (4, 13):
        z = s1.horizon_z(t, h)
        checked = 0
        for i in range(0, len(t.fridays), 3):
            fr = t.fridays[i]
            for j, s in enumerate(t.book.syms):
                a = next((b for b in hist[s] if b.date > fr), None)
                b = next((b for b in hist[s] if b.date > fr + timedelta(days=7 * h)), None)
                if not t.elig[i, j] or a is None or b is None:
                    assert np.isnan(z[i, j])
                    continue
                vol = math.exp(t.X[i, j, 7])  # log_vol
                want = math.log(b.open / a.open) / (vol * math.sqrt(7 * h / 365))
                assert z[i, j] == pytest.approx(max(-5.0, min(5.0, want)), abs=1e-12)
                checked += 1
        assert checked > 50
        # the last Friday's h-week window does not close inside the bars
        assert np.isnan(z[-1]).all()


def test_rotation_stays_inside_the_span(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    s1 = lib["slow1_ic"]
    x = np.arange(400.0)[:, None] * np.ones((1, 3))
    x[:50] = np.nan
    base = np.ones(x.shape, dtype=bool)
    r0, r1 = s1.span(x, base)
    assert (r0, r1) == (50, 400)
    for u in (0.0, 0.5, 0.999999):
        s = s1.shift_of(u, r1 - r0)
        assert s1.MIN_SHIFT <= s <= (r1 - r0) - s1.MIN_SHIFT
        y = s1.rotate(x, r0, r1, s)
        assert np.isnan(y[:50]).all()
        assert sorted(y[50:, 0]) == sorted(x[50:, 0])
        assert (y[:, 0] == y[:, 1]).all() or np.isnan(y[:, 0]).any()  # assets move together
        assert y[50 + s, 0] == x[50, 0]


def test_fit_predict_is_ols_with_slopes_only(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    s1 = lib["slow1_ic"]
    rng = np.random.default_rng(3)
    xtr, xte = rng.standard_normal((300, 4)) + 2.0, rng.standard_normal((50, 4)) + 2.0
    xtr[:, 3] = 1.0  # a dead column is dropped
    xte[:, 3] = 1.0
    ztr = xtr[:, :3] @ np.array([0.5, -1.0, 0.2]) + 3.0 + 0.1 * rng.standard_normal(300)
    mu, sd = xtr[:, :3].mean(0), xtr[:, :3].std(0)
    a = np.column_stack([np.ones(300), (xtr[:, :3] - mu) / sd])
    b = np.linalg.lstsq(a, ztr, rcond=None)[0]
    want = ((xte[:, :3] - mu) / sd) @ b[1:]
    assert np.allclose(s1.fit_predict(xtr, ztr, xte), want, atol=1e-9)


def test_planted_control_has_its_ic(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    s1 = lib["slow1_ic"]
    t, _ = table(lib, 2)
    z = s1.horizon_z(t, 4)
    i0 = 10
    keep = np.isfinite(z)
    keep[:i0] = False
    for kind in ("fast", "slow"):
        x = s1.planted(z, i0, kind, 4, 5)
        assert np.array_equal(np.isfinite(x), keep)
        assert np.corrcoef(x[keep], z[keep])[0, 1] == pytest.approx(s1.PLANT_RHO, abs=1e-9)
