"""halving-2 (research/lib/halving2_core.py, halving2.py): the frozen rule and its placebos.

- The window with BTC's calendar is exactly `macro.halving_bear`, every day 2010-2026.
- Placebo shifts stay in their bounds, are reproducible, and no placebo window shares a day
  with a true window (the coin's own, any cycle).
- The loader drops every row after the train cut; bars open at the previous close.
- No look-ahead: the rule's weights on a day are the same when every later bar is removed, and
  the fast path equals the gym's own slow path.
- C2 (alt priced in BTC, inside minus outside the window) on a hand-made series.
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

import pytest

from grimstrade import data
from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mods: dict[str, ModuleType] = {}
    for name in ("harness", "common", "macro", "halving2_core", "halving2"):
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


def _days(a: date, b: date) -> list[date]:
    return [a + timedelta(days=k) for k in range((b - a).days + 1)]


def test_btc_window_is_the_frozen_rule(lib: dict[str, ModuleType]) -> None:
    h, macro = lib["halving2_core"], lib["macro"]
    assert tuple(macro.HALVINGS) == h.CALENDARS["BTC"]
    for d in _days(date(2010, 1, 1), date(2026, 12, 31)):
        assert h.in_window(h.CALENDARS["BTC"], d) == macro.Features.halving_bear(None, d)


def test_placebo_shifts_bounded_reproducible_disjoint(lib: dict[str, ModuleType]) -> None:
    h = lib["halving2_core"]
    a = h.draw_shifts(["LTC", "ZEC"])
    assert a == h.draw_shifts(["LTC", "ZEC"]) and len(a) == 40
    assert any(r["LTC"] > 0 for r in a) and any(r["LTC"] < 0 for r in a)
    days = _days(date(2011, 1, 1), date(2027, 12, 31))
    for coin, rows in (("LTC", a), ("ZEC", a), ("BTC", h.draw_shifts(["BTC"], seed=h.SEED + 1))):
        lo, hi = h.shift_bounds(h.CALENDARS[coin])
        true = {d for d in days if h.in_window(h.CALENDARS[coin], d)}
        for r in rows:
            assert lo <= abs(r[coin]) <= hi
            cal = h.placebo_calendar(h.CALENDARS[coin], r[coin])
            fake = {d for d in days if h.in_window(cal, d)}
            assert fake and not (fake & true)


def test_loader_cuts_train_and_bars_open_at_previous_close(lib: dict[str, ModuleType]) -> None:
    h = lib["halving2_core"]
    rows = [{"time": f"{d}T00:00:00.000000000Z", "PriceUSD": str(10 + k)}
            for k, d in enumerate(_days(date(2025, 11, 1), date(2025, 11, 20)))]  # fmt: skip
    px = h.prices_from_rows(rows)
    assert max(px) == date(2025, 11, 10) and len(px) == 10
    b = h.bars(px)
    assert b[0].open == b[0].close == 10.0
    assert all(b[i].open == b[i - 1].close for i in range(1, len(b)))
    del px[date(2025, 11, 5)]
    with pytest.raises(ValueError):
        h.bars(px)


def _walk(h: ModuleType, seed: int, a: date, n: int) -> list[Bar]:
    rng = random.Random(seed)
    p, px = 10.0, {}
    for k in range(n):
        p *= math.exp(rng.gauss(0.0005 * math.sin(k / 200), 0.04))
        px[a + timedelta(days=k)] = p
    out: list[Bar] = h.bars(px)
    return out


def test_no_look_ahead(lib: dict[str, ModuleType]) -> None:
    harness, h2, h = lib["harness"], lib["halving2"], lib["halving2_core"]
    hist = {
        "LTC": _walk(h, 1, date(2015, 1, 1), 3000),
        "ZEC": _walk(h, 2, date(2016, 10, 29), 2500),
    }
    own = {s: h.CALENDARS[s] for s in hist}
    for strat in (h2.alone(own), h2.alone(own, trend=True)):
        full = harness.Panel(hist)
        checks = [date(2017, 2, 24), date(2017, 3, 3), date(2018, 2, 23), date(2021, 2, 5),
                  date(2022, 5, 20), date(2022, 6, 3), date(2023, 5, 19)]  # fmt: skip
        for d in checks:
            cut = {s: [b for b in bars if b.date < d] for s, bars in hist.items()}
            a = harness.decisions(strat, full, d, d)[0].weights
            b = harness.decisions(strat, harness.Panel(cut), d, d)[0].weights
            assert a == b
        harness.check_against_gym(strat, hist, checks[:3])
    w = harness.decisions(h2.alone(own), harness.Panel(hist), date(2017, 11, 3), date(2017, 11, 3))
    assert set(w[0].weights) == {"ZEC"}  # LTC is in its window; ZEC (eligible) is held


def test_relative_gap_hand_made(lib: dict[str, ModuleType]) -> None:
    h = lib["halving2_core"]
    cal = (date(2020, 1, 1),)
    ds = _days(date(2021, 6, 1), date(2023, 1, 1))
    btc = {d: 100.0 for d in ds}
    alt, p = {}, 1.0
    for d in ds:
        p *= math.exp(-0.01 if h.in_window(cal, d) else 0.002)
        alt[d] = p
    gap, n_in, n_out = h.relative_gap({"X": alt}, btc, {"X": cal}, {"X": ds[1]}, ds[-1])
    assert n_in == 365 and n_in + n_out == len(ds) - 1
    assert gap == pytest.approx(-0.012)
    assert h.rank_high(1.0, [0.5, 1.0, 2.0]) == 3 and h.rank_low(-1.0, [0.0, -2.0]) == 2
