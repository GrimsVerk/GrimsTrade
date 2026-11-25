"""calm-drag-1 (research/lib/calmdrag1.py): the calm drag split into cost, out-time and spells.

- The parts add up to the calm drag exactly, by every split, at cash 0 and at bills.
- A rule that always holds has no calm drag and no parts.
- A calm-only dip that the rule sits out splits into the dip it avoided and the rise it missed;
  a re-entry above the exit is a whipsaw loss; a flip costs exactly its cost.
- Calm days still out after a fall's rebound year land in E-post, not in the calm-only parts.
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

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
NAMES = ("stats", "harness", "gap2002", "calmdrag1")


@pytest.fixture(scope="module")
def cd() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    saved_mods = {n: sys.modules.get(n) for n in NAMES}
    sys.path.insert(0, str(LIB))
    mod = None
    for name in NAMES:
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


def _ser(cd: ModuleType, hold: Any, pos: Any, rf: Any, cost: float) -> Any:
    import numpy as np

    days = [date(2001, 1, 1) + timedelta(days=i) for i in range(len(hold))]
    flip = np.abs(np.diff(pos, prepend=0.0))
    r0 = pos * hold - cost * flip
    ok = np.ones(len(hold), dtype=bool)
    return cd.Ser("x", days, hold, pos, ok, rf, cost, r0, r0 + (1 - pos) * rf)


def _sum_ok(p: Any) -> None:
    assert p.k + p.o == pytest.approx(p.c, abs=1e-9)
    assert p.p + p.t == pytest.approx(p.o, abs=1e-9)
    e = p.e_pre + p.e_mid + p.e_post
    assert e + p.g + p.lag == pytest.approx(p.o, abs=1e-9)
    assert e + p.w_minus + p.w_plus == pytest.approx(p.o, abs=1e-9)
    assert e + p.short + p.long == pytest.approx(p.o, abs=1e-9)


def test_parts_add_up(cd: ModuleType) -> None:
    import numpy as np

    rng = np.random.default_rng(0)
    n = 4000
    hold = rng.normal(0.0004, 0.004, n)
    hold[0] = 0.0
    pos = (rng.random(n) < 0.8).astype(float)
    pos = np.repeat(pos[::20], 20)[:n]
    rf = np.full(n, 0.0001)
    s = _ser(cd, hold, pos, rf, 0.0002)
    for bills in (False, True):
        p = cd.decompose(s, date(2002, 1, 1), date(2011, 12, 31), bills)
        _sum_ok(p)
        assert p.k < 0
    same = _ser(cd, hold, np.ones(n), rf, 0.0002)
    p = cd.decompose(same, date(2002, 1, 1), date(2011, 12, 31), False)
    # only the first session's entry cost, outside the window
    assert (p.c, p.o, p.p, p.t, p.g, p.lag) == (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)


def test_calm_dip_splits_into_dip_and_lag(cd: ModuleType) -> None:
    import numpy as np

    n = 1000
    hold = np.full(n, 0.001)
    hold[0] = 0.0
    hold[500:510] = -0.01  # a 10% dip: calm (no 25% fall)
    hold[510:530] = 0.01  # rise back above the exit level
    pos = np.ones(n)
    pos[500:530] = 0.0  # out through the dip and the rise
    s = _ser(cd, hold, pos, np.zeros(n), 0.0)
    p = cd.decompose(s, date(2001, 1, 1), date(2003, 12, 31), False)
    _sum_ok(p)
    yrs = (date(2003, 12, 31) - date(2001, 1, 2)).days / 365.25  # from the first eligible
    assert p.g * yrs == pytest.approx(-100 * 10 * np.log1p(-0.01), abs=1e-9)
    assert p.lag * yrs == pytest.approx(-100 * 20 * np.log1p(0.01), abs=1e-9)
    assert p.w_minus == pytest.approx(p.o) and p.w_plus == 0.0
    assert p.short == pytest.approx(p.o) and p.long == 0.0
    assert p.e_pre == p.e_mid == p.e_post == 0.0
    assert p.spells_yr * yrs == pytest.approx(1.0)
    # with a cost, the two flips cost exactly two one-way costs
    sc = _ser(cd, hold, pos, np.zeros(n), 0.001)
    pc = cd.decompose(sc, date(2001, 1, 1), date(2003, 12, 31), False)
    want = 100 * (np.log1p(-0.001) + np.log1p(0.001 - 0.001) - np.log1p(0.001))
    assert pc.k * yrs == pytest.approx(want, abs=1e-9)


def test_out_after_rebound_year_is_e_post(cd: ModuleType) -> None:
    import numpy as np

    n = 2000
    hold = np.zeros(n)
    hold[1:] = 0.0005
    hold[400:430] = -0.012  # about a 30% fall
    hold[430:470] = 0.012  # rebound of more than 25%: next peak region
    pos = np.ones(n)
    pos[410:900] = 0.0  # out from inside the fall to well past the 365-day rebound
    s = _ser(cd, hold, pos, np.zeros(n), 0.0)
    part = cd.labels(s.days, s.hold)
    p = cd.decompose(s, date(2001, 1, 1), date(2006, 6, 1), False, part)
    _sum_ok(p)
    calm_out = [i for i in range(410, 900) if part[i] == 0]
    assert calm_out and min(calm_out) > 430
    assert p.e_post < 0 and p.g == p.lag == 0.0 and p.e_pre == 0.0
