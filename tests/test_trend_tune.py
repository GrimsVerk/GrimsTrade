"""The walk-forward tuners of research run trend-tune (research/lib/trend_tune.py).

- With every choice at 12 months a tuner IS `tsmom12`: same weights every day, same equity
  through `gym.simulate`. So are the plain cells of the sensitivity surface.
- No look-ahead: a tuner's choices at a refit, and its weights on any day, are the same when
  every later bar is removed (the gym's own slow path rebuilds history bar by bar).
- The paper series the tuner scores on charges costs and never uses a bar before it closed.
- The shrunk procedure leaves 12 months only for a large, well-supported advantage.
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
START = date(2012, 1, 2)
HOLIDAYS = {date(2014, 7, 4), date(2015, 12, 25), date(2016, 1, 1), date(2018, 3, 30)}


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mods: dict[str, ModuleType] = {}
    for name in ("harness", "common", "trend_tune"):
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


def walk(rng: random.Random, days: list[date], p0: float, vol: float, cycle: int) -> list[Bar]:
    """A random walk with a slow up-and-down drift, so trend signals flip now and then."""
    out, p = [], p0
    for k, d in enumerate(days):
        drift = 0.6 * vol * math.sin(2 * math.pi * k / cycle)
        o = p * math.exp(rng.gauss(0, vol / 3))
        c = o * math.exp(rng.gauss(drift, vol))
        out.append(Bar(d, o, max(o, c) * 1.01, min(o, c) * 0.99, c, 1000.0))
        p = c
    return out


def history(seed: int, n_days: int = 3300) -> dict[str, list[Bar]]:
    rng = random.Random(seed)
    cal = [START + timedelta(days=i) for i in range(n_days)]
    biz = [d for d in cal if d.weekday() < 5 and d not in HOLIDAYS]
    return {
        "SPY": walk(rng, biz, 300, 0.012, 400),
        "QQQ": walk(rng, [d for d in biz if d >= date(2012, 9, 3)], 200, 0.018, 250),
        "TLT": walk(rng, biz, 120, 0.008, 900),
        "BTC": walk(rng, cal[20:], 9000, 0.04, 600),
        "ETH": walk(rng, cal[900:], 400, 0.05, 330),
    }


def days_between(a: date, b: date) -> list[date]:
    return [a + timedelta(days=i) for i in range((b - a).days + 1)]


@pytest.mark.parametrize("mode", ["asset", "pooled", "shrunk"])
def test_all_twelve_is_tsmom12(lib: dict[str, ModuleType], mode: str) -> None:
    h, c, tt = lib["harness"], lib["common"], lib["trend_tune"]
    hist = history(1)
    panel = h.Panel(hist)
    a, b = date(2013, 6, 1), date(2020, 12, 31)
    ref = h.decisions(c.weekly(c.slots(c.tsmom_signal)), panel, a, b)
    got = h.decisions(tt.Tuner(mode, grid=(12,)).strategy(), panel, a, b)
    assert [d.weights for d in got] == [d.weights for d in ref]
    assert sum(len(d.weights) for d in ref) > 1000
    assert gym.simulate(got, hist).equity == gym.simulate(ref, hist).equity


def test_plain_surface_cells_are_tsmom12(lib: dict[str, ModuleType]) -> None:
    h, c, tt = lib["harness"], lib["common"], lib["trend_tune"]
    panel = h.Panel(history(2))
    a, b = date(2013, 6, 1), date(2018, 12, 31)
    ref = [d.weights for d in h.decisions(c.weekly(c.slots(c.tsmom_signal)), panel, a, b)]
    for strategy in (
        c.weekly(tt.fixed(12)),
        c.weekly(tt.both(12, 12)),
        c.weekly(tt.either(12, 12)),
        c.weekly(tt.per_asset({})),
        tt.threshold(12, 0.0, 0.0),
    ):
        assert [d.weights for d in h.decisions(strategy, panel, a, b)] == ref


def test_threshold_band_trades_less_and_differs(lib: dict[str, ModuleType]) -> None:
    h, tt = lib["harness"], lib["trend_tune"]
    panel = h.Panel(history(2))
    a, b = date(2013, 6, 1), date(2020, 12, 31)

    def flips(strategy: Any) -> int:
        w = [d.weights for d in h.decisions(strategy, panel, a, b)]
        return sum(set(x) != set(y) for x, y in zip(w, w[1:], strict=False))

    plain, banded = flips(tt.threshold(12, 0.0, 0.0)), flips(tt.threshold(12, 0.0, 0.5))
    assert 0 < banded < plain


@pytest.mark.parametrize("mode", ["asset", "pooled", "shrunk"])
def test_tuner_has_no_lookahead(lib: dict[str, ModuleType], mode: str) -> None:
    h, tt = lib["harness"], lib["trend_tune"]
    hist = history(3)
    tuner = tt.Tuner(mode)
    full = h.Panel(hist)
    moved = 0
    for year in range(2018, 2022):
        refit = tt.first_friday(year)
        t = h.decide_time(refit)
        cut = {s: data.visible(bars, data.UNIVERSE[s], t) for s, bars in hist.items()}
        got = tuner.choices(full, refit)
        assert got == tt.Tuner(mode).choices(h.Panel(cut), refit)
        moved += sum(m != 12 for m in got.values())
    if mode != "shrunk":
        assert moved > 0  # the test is not vacuous: the tuner does leave 12 months
    # weights from the fast path equal the gym's slow path, which sees truncated history only
    days = [date(2019, 3, 8), date(2020, 1, 3), date(2020, 6, 17), date(2020, 12, 26)]
    h.check_against_gym(tuner.strategy(), hist, days)


def test_surface_rules_have_no_lookahead(lib: dict[str, ModuleType]) -> None:
    h, c, tt = lib["harness"], lib["common"], lib["trend_tune"]
    hist = history(4, n_days=1500)
    days = [date(2014, 5, 9), date(2015, 2, 4), date(2015, 12, 26)]
    for strategy in (
        c.weekly(tt.fixed(18)),
        c.monthly(tt.fixed(6)),
        tt.fixed(3),
        c.weekly(tt.both(3, 12)),
        c.weekly(tt.either(6, 18)),
        tt.threshold(6, 0.25, 0.25),
    ):
        h.check_against_gym(strategy, hist, days)


def test_paper_series_is_causal_and_charges_costs(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    h, tt = lib["harness"], lib["trend_tune"]
    hist = history(5, n_days=1500)
    full = tt.paper(h.Panel(hist), "BTC")
    cut = {s: bars[:1000] for s, bars in hist.items()}
    part = tt.paper(h.Panel(cut), "BTC")
    k = len(part.ord) - 8  # the last week of a shorter history may not have its Friday yet
    for m in tt.GRID:
        assert np.array_equal(full.ret[m][:k], part.ret[m][:k])
    # the position on a bar is the signal of the latest Friday strictly before the bar's date
    panel = h.Panel(hist)
    bars = hist["BTC"]
    i = 700
    fri = tt.last_friday(bars[i].date - timedelta(days=1))
    view = panel.view(h.decide_time(fri))
    assert all(b.date < fri for b in bars[: view.n["BTC"]])  # the Friday's own bar is not closed
    held = tt.signal(view, "BTC", 12)
    prev = tt.signal(panel.view(h.decide_time(fri - timedelta(days=7))), "BTC", 12)
    move = bars[i].close / bars[i - 1].close - 1
    flip = held != prev and bars[i - 1].date <= fri
    want = (move if held else 0.0) - (0.003 if flip else 0.0)
    assert full.ret[12][i] == pytest.approx(want)
    flips = np.abs(np.diff((full.ret[12] != 0).astype(float))).sum()
    assert flips > 2


def test_shrunk_leaves_twelve_only_for_strong_evidence(lib: dict[str, ModuleType]) -> None:
    h, tt = lib["harness"], lib["trend_tune"]
    panel = h.Panel(history(6, n_days=800))
    base = {m: 0.5 for m in tt.GRID}

    def tuned(years: float, edge: float, mode: str = "shrunk") -> int:
        t = tt.Tuner(mode)
        own = {**base, 9: 0.5 + edge}
        t.scores = lambda p, r: {s: (years, own) for s in [*p.syms, "*"]}
        return int(t.choices(panel, tt.first_friday(2014))["SPY"])

    assert tuned(20, 0.30) == 9  # 0.30 x 20/40 = 0.15 >= 0.10
    assert tuned(20, 0.15) == 12  # 0.075
    assert tuned(5, 0.30) == 12  # 0.30 x 5/25 = 0.06
    assert tuned(5, 0.30, "asset") == 9
    assert tuned(4.9, 0.30, "asset") == 12  # under five years of paper series
    assert tuned(4.9, 0.30, "pooled") == 12


def test_pick_and_refit_dates(lib: dict[str, ModuleType]) -> None:
    tt = lib["trend_tune"]
    assert tt.pick({3: 1.0, 9: 1.2, 12: 1.2, 15: 1.2}) == 12
    assert tt.pick({3: 1.0, 9: 1.2, 15: 1.2, 12: 1.1}) == 9
    assert tt.first_friday(2021) == date(2021, 1, 1)
    assert tt.first_friday(2022) == date(2022, 1, 7)
    assert tt.refit_of(date(2022, 1, 6)) == date(2021, 1, 1)
    assert tt.refit_of(date(2022, 1, 7)) == date(2022, 1, 7)
    assert tt.days_of(12) == 365
