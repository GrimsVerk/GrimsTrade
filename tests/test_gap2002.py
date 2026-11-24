"""gap-2002-1 (research/lib/gap2002.py): the window's gap and its split into fall, rebound, calm.

- By date, fall + rebound + calm add up to the gap exactly, and only window sessions count.
- A rule that matches holding has no gap and no parts.
- A rule in cash through a 30% fall gains the fall in the fall part; the rebound it misses
  lands in the rebound part; the by-peak reading drops an episode that peaked before the window.
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType

import pytest

from grimstrade import data

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def gap() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    saved_mods = {n: sys.modules.get(n) for n in ("stats", "harness", "gap2002")}
    sys.path.insert(0, str(LIB))
    mod = None
    for name in ("stats", "harness", "gap2002"):
        spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    assert mod is not None
    yield mod
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path
    for n, m in saved_mods.items():
        if m is None:
            sys.modules.pop(n, None)
        else:
            sys.modules[n] = m


def _days(n: int, first: date = date(2001, 1, 1)) -> list[date]:
    return [first + timedelta(days=i) for i in range(n)]


def test_parts_add_up_and_window_only(gap: ModuleType) -> None:
    import numpy as np

    rng = np.random.default_rng(0)
    days = _days(4000)
    hold = rng.normal(0.0003, 0.02, len(days))
    rule = np.where(rng.random(len(days)) < 0.7, hold, 0.0)
    g = gap.split(days, hold, rule, date(2002, 1, 1), date(2010, 12, 31))
    assert g.i + g.b + g.c == pytest.approx(g.g, abs=1e-9)
    win = np.array([date(2002, 1, 1) <= d <= date(2010, 12, 31) for d in days])
    want = 100 * (np.log1p(rule[win]) - np.log1p(hold[win])).sum() / gap.YEARS
    assert g.g == pytest.approx(want, abs=1e-9)
    same = gap.split(days, hold, hold.copy(), date(2002, 1, 1), date(2010, 12, 31))
    assert (same.g, same.i, same.b, same.c) == (0.0, 0.0, 0.0, 0.0)


def test_fall_and_rebound_land_in_their_parts(gap: ModuleType) -> None:
    import numpy as np

    days = _days(2000)
    hold = np.zeros(len(days))
    hold[400:430] = -0.012  # about a 30% fall: peak at 399, trough at 429
    hold[430:470] = 0.012  # rebound of more than 25%
    rule = hold.copy()
    rule[400:470] = 0.0  # out for the fall and the rebound
    g = gap.split(days, hold, rule, date(2001, 1, 1), date(2006, 6, 1))
    ln = 100 * np.log1p(0.012)
    assert g.i == pytest.approx(30 * -np.log1p(-0.012) * 100 / gap.YEARS)
    assert g.b == pytest.approx(-40 * ln / gap.YEARS)
    assert g.c == pytest.approx(0.0, abs=1e-12)
    late = gap.split(days, hold, rule, days[410], date(2006, 6, 1))  # peak before the window
    assert late.i_peak == late.b_peak == 0.0
    assert late.i > 0 and late.b < 0
