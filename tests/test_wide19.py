"""wide-19 measures what its card says (research/cards/wide-19.md).

- Neither rule's decisions use a bar after the decision: cutting or changing the bars after
  day k changes no decision up to k.
- x is a year's mean weekly log return over its sample sd, on a Friday grid of last closes.
- Z follows Buhlmann: 0 when every asset's drift is the same (`cred-xs`) or never moves from
  its long-run mean (`cred-lr`), near 1 when drifts differ far beyond sampling noise, and 1
  when there is too little to estimate it.
- With too little history both rules are `tsmom12`.
"""

from __future__ import annotations

import importlib.util
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
START = date(2019, 1, 1)


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mods: dict[str, ModuleType] = {}
    for name in ("harness", "common", "wide16", "wide19"):
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


def bars(seed: int, days: int, crypto: bool, drift: float, vol: float) -> list[Bar]:
    np: Any = pytest.importorskip("numpy")
    rng = np.random.default_rng(seed)
    out, px = [], 100.0
    for k in range(days):
        d = START + timedelta(days=k)
        if not crypto and d.weekday() >= 5:
            continue
        nxt = px * float(np.exp(drift + vol * rng.normal()))
        out.append(Bar(d, px, max(px, nxt), min(px, nxt), nxt, 1e6))
        px = nxt
    return out


def history(days: int = 1500) -> dict[str, list[Bar]]:
    return {
        "SPY": bars(1, days, False, 0.0003, 0.01),
        "TLT": bars(2, days, False, -0.0002, 0.008),
        "BTC": bars(3, days, True, 0.0008, 0.04),
    }


@pytest.mark.parametrize("name", ["cred-xs", "cred-lr"])
def test_decisions_use_no_later_bar(lib: dict[str, ModuleType], name: str) -> None:
    h, w = lib["harness"], lib["wide19"]
    full = history()
    cut = START + timedelta(days=1300)
    short = {s: [b for b in v if b.date <= cut] for s, v in full.items()}
    changed = {s: [b if b.date <= cut else Bar(b.date, 1, 1, 1, 1, 1) for b in v]
               for s, v in full.items()}  # fmt: skip
    a, z = START + timedelta(days=1100), cut - timedelta(days=1)
    ref = h.decisions(w.rule(name), h.Panel(full), a, z)
    assert ref == h.decisions(w.rule(name), h.Panel(short), a, z)
    assert ref == h.decisions(w.rule(name), h.Panel(changed), a, z)
    assert any(d.weights for d in ref)


def test_weekly_returns_and_x(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    w = lib["wide19"]
    dates = np.array([10, 11, 17, 24, 25])
    closes = np.array([1.0, 2.0, 4.0, 8.0, 16.0])
    grid = np.array([3, 10, 17, 24])
    r = w.weekly_returns(dates, closes, grid)
    assert np.isnan(r[0])  # no close on or before day 3
    assert r[1:] == pytest.approx([np.log(4), np.log(2)])  # closes 1 -> 4 -> 8 on days 10, 17, 24
    rng = np.random.default_rng(0)
    x = rng.normal(0.001, 0.02, 60)
    rx = w.rolling_x(x)
    assert np.isnan(rx[:51]).all()
    tail = x[-52:]
    assert rx[-1] == pytest.approx(tail.mean() / tail.std(ddof=1))
    assert np.isnan(w.rolling_x(np.full(60, 0.01))[-1])  # sd 0


def test_z_follows_buhlmann(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    w = lib["wide19"]
    same = np.tile(np.linspace(-0.3, 0.3, 100), (3, 1))  # every asset the same drift
    assert w.xs_z(same) == 0.0
    apart = np.array([np.full(100, -3.0), np.zeros(100), np.full(100, 3.0)])
    assert w.xs_z(apart) > 0.99
    assert w.xs_z(apart[:, :40]) == 1.0  # too few Fridays to estimate
    mu = np.array([0.1, 0.0, -0.1])
    flat = np.tile(mu[:, None], (1, 100))  # x never leaves its long-run mean
    n = np.array([200, 200, 200])
    assert w.lr_z(flat, mu, n) == 0.0
    swing = np.tile(np.where(np.arange(100) % 2, 2.0, -2.0), (3, 1))
    assert w.lr_z(swing, np.zeros(3), n) > 0.98
    assert w.lr_z(swing, np.zeros(3), np.array([100, 100, 100])) == 1.0  # nobody has 3 years


@pytest.mark.parametrize("name", ["cred-xs", "cred-lr"])
def test_short_history_is_tsmom12(lib: dict[str, ModuleType], name: str) -> None:
    h, c, w = lib["harness"], lib["common"], lib["wide19"]
    hist = history(days=420)  # a year of bars: eligible, too short for a year of weekly returns
    a, z = START + timedelta(days=380), START + timedelta(days=418)
    ref = h.decisions(c.weekly(c.slots(c.tsmom_signal)), h.Panel(hist), a, z)
    assert h.decisions(w.rule(name), h.Panel(hist), a, z) == ref
