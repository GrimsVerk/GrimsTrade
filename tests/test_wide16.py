"""wide-16 `cost-band` measures what its card says (research/cards/cost-band.md).

- The rule's decisions are `tsmom12`'s and use no bar after the decision: cutting or changing
  the bars after day k changes no decision up to k.
- The band works as the card says: a held slot that drifts 3 points of equity is topped up at
  b = 0.01 and left alone at b = 0.05; a full exit trades at any band.
- The harness passes the band through, and its default is the gym's own.
- The train loader never returns a bar after 2025-11-10.
"""

from __future__ import annotations

import importlib.util
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
START = date(2019, 1, 1)


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mods: dict[str, ModuleType] = {}
    for name in ("harness", "common", "wide16"):
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


def history(days: int = 900) -> dict[str, list[Bar]]:
    return {
        "SPY": bars(1, days, False, 0.0004, 0.01),
        "TLT": bars(2, days, False, -0.0003, 0.008),
        "BTC": bars(3, days, True, 0.001, 0.04),
    }


def test_decisions_use_no_later_bar(lib: dict[str, ModuleType]) -> None:
    h, c, w = lib["harness"], lib["common"], lib["wide16"]
    full = history()
    cut = START + timedelta(days=600)
    short = {s: [b for b in v if b.date <= cut] for s, v in full.items()}
    changed = {s: [b if b.date <= cut else Bar(b.date, 1, 1, 1, 1, 1) for b in v]
                for s, v in full.items()}  # fmt: skip
    a, z = START + timedelta(days=380), cut - timedelta(days=1)
    ref = h.decisions(w.rule(), h.Panel(full), a, z)
    assert ref == h.decisions(w.rule(), h.Panel(short), a, z)
    assert ref == h.decisions(w.rule(), h.Panel(changed), a, z)
    # and the weights are exactly the baseline's (`tsmom12`)
    assert ref == h.decisions(c.weekly(c.slots(c.tsmom_signal)), h.Panel(full), a, z)
    assert any(d.weights for d in ref)


def _two_day(price2: float, w2: float, band: float) -> gym.Result:
    """Hold half the book in SPY, then let it drift: day 2's open is `price2`."""
    days = [date(2024, 1, 2), date(2024, 1, 3), date(2024, 1, 4)]
    hist = {"SPY": [Bar(days[0], 100, 100, 100, 100, 1), Bar(days[1], 100, 100, 100, 100, 1),
                    Bar(days[2], price2, price2, price2, price2, 1)]}  # fmt: skip
    t = [datetime.combine(d, gym.DECIDE_AT, tzinfo=UTC) for d in days]
    decs = [gym.Decision(t[0], {"SPY": 0.5}), gym.Decision(t[1], {"SPY": w2})]
    return gym.simulate(decs, hist, costs={"etf": gym.Costs(0, 0), "crypto": gym.Costs(0, 0)},
                        band=band)  # fmt: skip


def test_band_keeps_a_drifted_slot_but_never_blocks_an_exit() -> None:
    # SPY up 12.8% from a half slot: weight 0.53, three points over the target 0.5
    assert len(_two_day(112.8, 0.5, 0.01).fills) == 2  # topped back (trimmed) at 1%
    assert len(_two_day(112.8, 0.5, 0.05).fills) == 1  # left alone at 5%
    assert len(_two_day(112.8, 0.0, 0.05).fills) == 2  # a full exit always trades
    # entries trade whenever they exceed the band: every slot is at least 1/6 > 0.05
    assert len(_two_day(112.8, 0.5, 0.05).fills) == 1  # the entry itself


def test_harness_passes_the_band(lib: dict[str, ModuleType]) -> None:
    h, w = lib["harness"], lib["wide16"]
    hist = history()
    pan = h.Panel(hist)
    a, z = START + timedelta(days=380), START + timedelta(days=880)
    kw: dict[str, Any] = {"panel": pan, "history": hist, "start": a, "end": z, "log": False}
    default = h.run("t", "d", w.rule(), **kw)
    same = h.run("t", "d", w.rule(), band=gym.BAND, **kw)
    wide = h.run("t", "w", w.rule(), band=0.05, **kw)
    assert list(default.equity) == list(same.equity)
    assert default.decisions == wide.decisions  # same weights, only the trades differ
    assert list(default.equity) != list(wide.equity)
    assert wide.score.turnover < default.score.turnover


def test_train_loader_stops_at_the_cut(lib: dict[str, ModuleType], monkeypatch: Any) -> None:
    h = lib["harness"]
    late = {"SPY": [Bar(date(2025, 11, 10), 1, 1, 1, 1, 1), Bar(date(2025, 11, 11), 1, 1, 1, 1, 1)]}
    monkeypatch.setattr(h.data, "load_all", lambda root, syms: {s: list(late[s]) for s in syms})
    got = h.load_history("train", adjusted=False, syms=["SPY"])
    assert [b.date for b in got["SPY"]] == [date(2025, 11, 10)]
