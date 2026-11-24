"""The turbulence-1 overlay measures what its card says (research/cards/turbulence.md).

- No look-ahead: every signal and trigger value at row k is the same when later rows are cut,
  and a shock planted at row k changes nothing before it.
- Mahalanobis algebra: with one asset turbulence equals magnitude surprise; two correlated
  assets moving against their correlation give turbulence above magnitude.
- The overlay's fast path equals the gym's own visible-history path.
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

from grimstrade import data
from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
START = date(2016, 1, 4)


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mods: dict[str, ModuleType] = {}
    for name in ("harness", "common", "turbulence1"):
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


def grid(seed: int, rows: int = 700) -> Any:
    np: Any = pytest.importorskip("numpy")
    rng = np.random.default_rng(seed)
    common = rng.normal(0, 0.01, rows)
    r = np.column_stack(
        [common + rng.normal(0, 0.005, rows), -0.5 * common + rng.normal(0, 0.006, rows),
         rng.normal(0, 0.02, rows)]
    )  # fmt: skip
    g = 100 * np.exp(np.cumsum(r, axis=0))
    g[:150, 2] = np.nan  # the third asset joins late
    return g


def test_signals_and_triggers_are_causal(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    t = lib["turbulence1"]
    g = grid(1)
    full = t.signals(g, 60, 5)
    for k in (200, 333, 500):
        part = t.signals(g[:k], 60, 5)
        for name in ("d", "m", "T", "M", "C", "n"):
            assert np.allclose(full[name][:k], part[name], equal_nan=True), (name, k)
        for sig in ("T", "M", "C"):
            a = t.trigger(full[sig], 90, 200, 50)[:k]
            b = t.trigger(part[sig], 90, 200, 50)
            assert (a == b).all()
    assert t.trigger(full["T"], 90, 200, 50).any()  # not vacuous


def test_planted_shock_changes_nothing_before_it(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    t = lib["turbulence1"]
    g = grid(2)
    k = 450
    shocked = g.copy()
    shocked[k:, 0] *= 0.8  # a 20% fall on row k
    a, b = t.signals(g, 60, 5), t.signals(shocked, 60, 5)
    for name in ("T", "M", "C"):
        assert np.allclose(a[name][:k], b[name][:k], equal_nan=True)
    assert b["T"][k] > 10 * a["T"][k]  # and it does register on the day


def test_mahalanobis_algebra(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    t = lib["turbulence1"]
    rng = np.random.default_rng(3)
    one = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, (300, 1)), axis=0))
    s = t.signals(one, 60, 5)
    ok = ~np.isnan(s["d"])
    assert ok.sum() > 200 and np.allclose(s["d"][ok], s["m"][ok])  # one asset: d = m
    z = rng.normal(0, 0.01, 300)
    r = np.column_stack([z + rng.normal(0, 0.001, 300), z + rng.normal(0, 0.001, 300)])
    r[-1] = [0.02, -0.02]  # two strongly correlated assets moving apart, two sigma each
    pair = 100 * np.exp(np.cumsum(r, axis=0))
    s2 = t.signals(pair, 60, 1)
    assert s2["d"][-1] > 5 * s2["m"][-1]
    assert s2["C"][-1] > 5


def walk(rng: random.Random, days: list[date], p0: float, vol: float) -> list[Bar]:
    out, p = [], p0
    for k, d in enumerate(days):
        drift = 0.5 * vol * math.sin(2 * math.pi * k / 300)
        shock = -0.06 if k % 170 == 0 and k else 0.0  # crashes now and then
        o = p * math.exp(rng.gauss(0, vol / 3))
        c = o * math.exp(rng.gauss(drift, vol) + shock)
        out.append(Bar(d, o, max(o, c) * 1.01, min(o, c) * 0.99, c, 1000.0))
        p = c
    return out


def test_overlay_matches_gym_and_cuts_only_risk(lib: dict[str, ModuleType]) -> None:
    h, c, t = lib["harness"], lib["common"], lib["turbulence1"]
    rng = random.Random(4)
    cal = [START + timedelta(days=i) for i in range(1100)]
    biz = [d for d in cal if d.weekday() < 5]
    hist = {"SPY": walk(rng, biz, 300, 0.012), "TLT": walk(rng, biz, 120, 0.008)}
    spec = t.Spec("T", 80, window=40, smooth=3, hist=120, min_hist=40)
    strat = t.overlay(t.tsmom12(), spec, ["SPY"])
    panel = h.Panel(hist)
    on = t.on_array(panel, spec)
    assert on.any() and not on.all()
    days = [panel.grid_dates[i] for i in range(400, len(panel.grid_dates), 37)]
    h.check_against_gym(strat, hist, days)
    base = c.weekly(c.slots(c.tsmom_signal))
    for d in days:
        w, b = strat(panel.view(h.decide_time(d))), base(panel.view(h.decide_time(d)))
        assert w.get("TLT") == b.get("TLT")
        if on[panel.grid_dates.index(d)]:
            assert "SPY" not in w
        else:
            assert w == b
