"""wide-18 measures what its card says (research/cards/wide-18.md).

- Neither rule's decisions use a bar after the decision: cutting or changing the bars after
  day k changes no decision up to k.
- `vclock12`'s window holds one median year of variance: about a year at constant volatility,
  a quarter (the floor) after volatility doubles, and at most two years.
- `huber52`'s drift is the plain mean when nothing is clipped, and one huge week cannot flip it.
- With too little history both fall back to `tsmom12`.
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
    for name in ("harness", "common", "wide16", "wide18"):
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


def history(days: int = 1100) -> dict[str, list[Bar]]:
    return {
        "SPY": bars(1, days, False, 0.0003, 0.01),
        "TLT": bars(2, days, False, -0.0002, 0.008),
        "BTC": bars(3, days, True, 0.0008, 0.04),
    }


@pytest.mark.parametrize("name", ["vclock12", "huber52"])
def test_decisions_use_no_later_bar(lib: dict[str, ModuleType], name: str) -> None:
    h, w = lib["harness"], lib["wide18"]
    full = history()
    cut = START + timedelta(days=800)
    short = {s: [b for b in v if b.date <= cut] for s, v in full.items()}
    changed = {s: [b if b.date <= cut else Bar(b.date, 1, 1, 1, 1, 1) for b in v]
               for s, v in full.items()}  # fmt: skip
    a, z = START + timedelta(days=380), cut - timedelta(days=1)
    ref = h.decisions(w.rule(name), h.Panel(full), a, z)
    assert ref == h.decisions(w.rule(name), h.Panel(short), a, z)
    assert ref == h.decisions(w.rule(name), h.Panel(changed), a, z)
    assert any(d.weights for d in ref)


def test_vclock_window_follows_variance(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    w = lib["wide18"]
    rng = np.random.default_rng(0)
    calm = rng.choice([-0.01, 0.01], size=2000)  # every squared return equal
    assert w.vclock_window(calm, 252) == 252
    loud = np.concatenate([calm, 2 * calm[:300]])  # variance x4 for the last 300 bars
    assert w.vclock_window(loud, 252) == 63  # a quarter of the year's variance: the floor
    quiet = np.concatenate([calm, 0.1 * calm[:1000]])
    assert w.vclock_window(quiet, 252) == 504  # the two-year cap
    assert w.vclock_window(calm[:200], 252) == 0  # too short: fall back


def test_huber_drift_resists_one_jump(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    w = lib["wide18"]
    x = np.array([-0.01, 0.0, 0.01] * 17 + [0.0])
    assert w.huber_drift(x) == pytest.approx(x.mean())  # nothing clipped
    down = np.linspace(-0.012, 0.008, 51)  # most weeks down: median -0.002
    down = np.append(down, 0.5)  # and one +50% week
    assert down.mean() > 0  # the plain sum says up
    assert w.huber_drift(down) < 0  # the robust drift says down
    assert np.isnan(w.huber_drift(np.zeros(52)))


@pytest.mark.parametrize("name", ["vclock12", "huber52"])
def test_short_history_is_tsmom12(lib: dict[str, ModuleType], name: str) -> None:
    h, c, w = lib["harness"], lib["common"], lib["wide18"]
    hist = history(days=420)  # a year of bars: eligible, but too short for either rule
    a, z = START + timedelta(days=380), START + timedelta(days=418)
    ref = h.decisions(c.weekly(c.slots(c.tsmom_signal)), h.Panel(hist), a, z)
    assert h.decisions(w.rule(name), h.Panel(hist), a, z) == ref
