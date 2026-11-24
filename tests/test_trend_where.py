"""The walk-forward yes/no of research run trend-where (research/lib/trend_where.py).

- With every answer yes the rule IS `tsmom12`; with every answer no it IS equal weight.
- No look-ahead: the answers at a refit, and the weights on any day, are the same when every
  later bar is removed (the gym's own slow path rebuilds history bar by bar).
- "Rougher" means what the card says: larger volatility, or a deeper chained fall, on out bars.
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Iterator
from datetime import date
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
from test_trend_tune import history

from grimstrade import data, gym

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mods: dict[str, ModuleType] = {}
    for name in ("harness", "common", "trend_tune", "trend_where"):
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


@pytest.mark.parametrize("mode", ["vol", "dd"])
def test_all_yes_is_tsmom12_and_all_no_is_equal_weight(
    lib: dict[str, ModuleType], mode: str
) -> None:
    h, c, tw = lib["harness"], lib["common"], lib["trend_where"]
    hist = history(1)
    panel = h.Panel(hist)
    a, b = date(2013, 6, 1), date(2020, 12, 31)
    trend = h.decisions(c.weekly(c.slots(c.tsmom_signal)), panel, a, b)
    yes = h.decisions(tw.Where(mode, min_years=1e9).strategy(), panel, a, b)
    assert [d.weights for d in yes] == [d.weights for d in trend]
    assert gym.simulate(yes, hist).equity == gym.simulate(trend, hist).equity
    never: Any = tw.Where(mode)
    never.answers = lambda p, r: dict.fromkeys(p.syms, False)
    no = h.decisions(never.strategy(), panel, a, b)
    ew = h.decisions(c.weekly(c.equal_weight), panel, a, b)
    assert [d.weights for d in no] == [d.weights for d in ew]
    assert [d.weights for d in ew] != [d.weights for d in trend]


@pytest.mark.parametrize("mode", ["vol", "dd"])
def test_answers_have_no_lookahead(lib: dict[str, ModuleType], mode: str) -> None:
    h, tt, tw = lib["harness"], lib["trend_tune"], lib["trend_where"]
    hist = history(3)
    where = tw.Where(mode, min_years=2.0)
    full = h.Panel(hist)
    seen = set()
    for year in range(2015, 2022):
        refit = tt.first_friday(year)
        t = h.decide_time(refit)
        cut = {s: data.visible(bars, data.UNIVERSE[s], t) for s, bars in hist.items()}
        got = where.answers(full, refit)
        assert got == tw.Where(mode, min_years=2.0).answers(h.Panel(cut), refit)
        seen |= set(got.values())
    assert seen == {True, False}  # not vacuous: both answers occur
    # weights from the fast path equal the gym's slow path, which sees truncated history only
    days = [date(2019, 3, 8), date(2020, 1, 3), date(2020, 6, 17), date(2020, 12, 26)]
    h.check_against_gym(where.strategy(), hist, days)


def test_rougher_is_what_the_card_says(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    tw = lib["trend_where"]
    assert tw.worst_fall(np.array([0.1, -0.5, 0.2, -0.3])) == pytest.approx(1 - 0.5 * 1.2 * 0.7)
    assert tw.worst_fall(np.array([0.1, 0.2])) == 0.0
    calm, wild = np.array([0.01, -0.01] * 50), np.array([0.05, -0.05] * 50)
    assert tw.rough(wild, "vol") > tw.rough(calm, "vol")
    assert tw.rough(wild, "dd") > tw.rough(calm, "dd")


def test_thin_evidence_keeps_the_filter(lib: dict[str, ModuleType]) -> None:
    h, tt, tw = lib["harness"], lib["trend_tune"], lib["trend_where"]
    panel = h.Panel(history(6, n_days=1500))
    refit = tt.first_friday(2015)
    ev = tw.Where("vol").evidence(panel, "SPY", refit)
    assert ev.years < tw.MIN_YEARS and ev.keep
    loose = tw.Where("vol", min_years=0.5, min_bars=10).evidence(panel, "SPY", refit)
    assert loose.keep == (loose.out > loose.inn)
