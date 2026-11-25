"""The reentry-reconcile-1 engine (research/lib/reconcile_reentry_core.py; card
research/cards/reentry-reconcile-1.md).

- The buy-back and trim components add up to the position gap and, with the cost term and the
  compounding residual, to the weekly return gap; the anatomy split adds up for every rule.
- Sleeves at w = 1 are the rule, at w = 0 `tsmom12`; `e4-re` and `e4-trim` split `e4`'s gap.
- The 3-month rules never trim; `e4` both buys back and trims.
- Episode windows are those of `e4anatomy_core.fall_labels`; dN = dI + dB.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
READ = {"A": (0.25, 13), "B": (0.20, 13)}


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mods() -> tuple[ModuleType, ModuleType]:
    pytest.importorskip("numpy")
    sys.path.insert(0, str(LIB))
    _load("pooled1_core")
    _load("pooled2_core")
    ec = _load("e4anatomy_core")
    return ec, _load("reconcile_reentry_core")


def path(seed: int, years: float = 10.0, vol: float = 0.25) -> tuple[Any, Any]:
    import numpy as np

    rng = np.random.default_rng(seed)
    days: list[int] = []
    d = date(1981, 1, 2)
    while len(days) < int(252 * years):
        if d.weekday() < 5:
            days.append(d.toordinal())
        d += timedelta(days=1)
    drift = np.repeat(rng.choice([-0.6, 0.5], len(days) // 120 + 1), 120)[: len(days)] / 252
    lr = drift + rng.normal(0, vol / math.sqrt(252), len(days))
    lr[0] = 0.0
    return np.array(days, dtype=np.int64), 100 * np.exp(np.cumsum(lr))


@pytest.fixture(scope="module")
def mk(mods: tuple[ModuleType, ModuleType]) -> Any:
    _, rc = mods
    d, px = path(3)
    return rc.market("X", "EQ-T", d, px, READ)


def test_components_add_up(mods: tuple[ModuleType, ModuleType], mk: Any) -> None:
    import numpy as np

    _, rc = mods
    h12 = mk.h["tsmom12"]
    assert set(np.unique(h12)) <= {0.0, 1.0}
    for r in rc.LOGGED:
        c = rc.components(mk.h[r], h12)
        assert np.allclose(c["buyback"] + c["trim"], mk.h[r] - h12, atol=1e-15)
    # the 3-month rules hold at least tsmom12: no trims
    for r in ("or3-12", "arm3-12"):
        assert np.all(rc.components(mk.h[r], h12)["trim"] == 0.0)
    c = rc.components(mk.h["e4"], h12)
    assert c["trim"].min() < 0 and c["buyback"].max() > 0


def test_series_legs_and_parts(mods: tuple[ModuleType, ModuleType], mk: Any) -> None:
    import numpy as np

    ec, rc = mods
    for r in rc.LOGGED:
        s = rc.series(mk, r, mk.h[r])
        assert np.allclose(sum(s.legs.values()), s.r_e4 - s.r_ts, atol=1e-14)
        assert abs(s.legs["resid"]).max() < 5e-3  # weekly compounding only (cross terms)
        for rd in READ:
            for vm in (False, True):
                p = ec.parts(s, rd, vm)  # raises if the split does not add up
                assert math.isclose(p.ret + p.risk, p.d, abs_tol=1e-9)


def test_sleeves(mods: tuple[ModuleType, ModuleType], mk: Any) -> None:
    import numpy as np

    _, rc = mods
    h12 = mk.h["tsmom12"]
    h = mk.h["or3-12"]
    assert np.array_equal(rc.sleeve(h, h12, 1.0), h)
    assert np.array_equal(rc.sleeve(h, h12, 0.0), h12)
    half = rc.sleeve(h, h12, 0.5)
    assert np.allclose(half - h12, 0.5 * (h - h12))
    e = rc.e4_parts(mk.h["e4"], h12)
    # e4-re keeps e4's buy-back, e4-trim its trims; their gaps add up to e4's
    assert np.allclose((e["e4-re"] - h12) + (e["e4-trim"] - h12), mk.h["e4"] - h12)
    assert np.all(rc.components(e["e4-re"], h12)["trim"] == 0.0)
    assert np.all(rc.components(e["e4-trim"], h12)["buyback"] == 0.0)


def test_episode_windows_match_labels(mods: tuple[ModuleType, ModuleType]) -> None:
    import numpy as np

    ec, rc = mods
    # constructed path: up, a 40% fall over 50 sessions, a 60% rise, then flat-ish up
    days = np.array([date(2000, 1, 3).toordinal() + 7 * i // 5 for i in range(700)], dtype=np.int64)
    lv = np.concatenate(
        [
            np.linspace(100, 130, 200),
            np.linspace(130, 78, 50),
            np.linspace(78, 125, 150),
            np.linspace(125, 160, 300),
        ]  # fmt: skip
    )
    lab = ec.fall_labels(days, lv, 0.25, 0.25)
    w = rc.windows(days, lv, 0.25, 0.25)
    assert len(w) == 1
    a, b, e = w[0]
    assert a == 199 and b == 249
    assert np.all(lab[a + 1 : b + 1] == ec.FASTC)
    assert np.all(lab[b + 1 : e + 1] == ec.REBC)
    assert lab[e + 1] == ec.CALMC if e + 1 < len(lab) else True


def test_episodes_net(mods: tuple[ModuleType, ModuleType], mk: Any) -> None:
    _, rc = mods
    eps = rc.episodes(mk, mk.h["e4"])
    assert eps
    for e in eps:
        assert math.isclose(e.dN, e.dI + e.dB)
        assert e.peak + 1 >= mk.start and e.trough > e.peak and e.end >= e.trough
    zero = rc.episodes(mk, mk.h["tsmom12"])
    assert all(e.dI == 0 and e.dB == 0 for e in zero)
    pool = rc.episode_pool(eps)
    assert math.isclose(pool["dN"], pool["dI"] + pool["dB"])
    assert rc.episode_pool([]) == {"n": 0}


def test_efficiency(mods: tuple[ModuleType, ModuleType]) -> None:
    _, rc = mods
    assert rc.efficiency(0.1, -0.05) == pytest.approx(2.0)
    assert math.isnan(rc.efficiency(0.1, 0.01))
