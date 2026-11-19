"""The planted input of the rl-3 control is what its card says (research/rl-3.md).

- `week_z` is the return of the week a Friday decision holds: from the first open after the
  Friday to the first open after the next Friday, divided by the vol input x sqrt(7/365).
- `peek` correlates with it exactly `rho` inside every calendar year, has unit variance there,
  is 0 where the asset is not eligible, and uses the same noise for every `rho`.
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
    mods = {n: importlib.import_module(n) for n in ("rl_env", "rl2_env", "rl3_plant")}
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


def test_week_z_is_the_held_week(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    env, pl = lib["rl_env"], lib["rl3_plant"]
    hist = history(1)
    t = env.build_table(hist, lambda d: [math.nan] * len(env.MACRO_FEATS), START,
                        START + timedelta(days=1280))  # fmt: skip
    z = pl.week_z(t)
    checked = 0
    for i in range(0, len(t.fridays) - 2, 3):
        fr = t.fridays[i]
        for j, s in enumerate(t.book.syms):
            if not t.elig[i, j]:
                assert np.isnan(z[i, j])
                continue
            a = next(b for b in hist[s] if b.date > fr)
            b = next(b for b in hist[s] if b.date > fr + timedelta(days=7))
            vol = math.exp(t.X[i, j, 7])  # log_vol
            want = max(-5.0, min(5.0, math.log(b.open / a.open) / (vol * math.sqrt(7 / 365))))
            assert z[i, j] == pytest.approx(want, abs=1e-12)
            checked += 1
    assert checked > 50


def test_peek_has_exact_ic_every_year(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    env, pl = lib["rl_env"], lib["rl3_plant"]
    t = env.build_table(history(2), lambda d: [math.nan] * len(env.MACRO_FEATS), START,
                        START + timedelta(days=1280))  # fmt: skip
    z = pl.week_z(t)
    years = np.array([d.year for d in t.fridays])
    noise = pl.peek(t, 0.0, 7)
    for rho in (0.0, 0.05, 0.2):
        p = pl.peek(t, rho, 7)
        assert (p[~t.elig] == 0).all()
        for y in np.unique(years):
            cell = (years == y)[:, None] & np.isfinite(z)
            if cell.sum() < 3:
                continue
            assert np.corrcoef(p[cell], z[cell])[0, 1] == pytest.approx(rho, abs=1e-9)
            assert p[cell].std() == pytest.approx(1.0, abs=1e-9)
            # the same noise for every strength: p = rho z' + sqrt(1 - rho^2) e'
            zy = (z[cell] - z[cell].mean()) / z[cell].std()
            assert np.allclose(p[cell], rho * zy + math.sqrt(1 - rho**2) * noise[cell])
