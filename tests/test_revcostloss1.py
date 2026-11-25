"""rev-costloss-1 (research/lib/revcostloss1.py): the exit scored as a binary crash warning.

- Relative economic value: 1 for a perfect warning, 0 or less for "always warn", and its
  maximum over the cost/loss ratio is the Peirce score H - F, reached at C/L = base rate.
- Events count a fall from the Friday close inside the window only, and only when the whole
  window lies inside the data; the warning is the position for the week after the Friday.
- The money bridges: a holder's cost/loss ratio and the money value have the right signs.
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
def rev() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    saved_mods = {n: sys.modules.get(n) for n in ("stats", "harness", "revcostloss1")}
    sys.path.insert(0, str(LIB))
    mod = None
    for name in ("stats", "harness", "revcostloss1"):
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


def test_value_curve_limits_and_peak(rev: ModuleType) -> None:
    import numpy as np

    rng = np.random.default_rng(1)
    e = rng.random(5000) < 0.2
    perfect = rev.table(e, e)
    for a in (0.05, 0.2, 0.5, 0.9):
        assert rev.v_of(perfect, a) == pytest.approx(1.0)
    always = rev.table(np.ones(5000, dtype=bool), e)
    assert all(rev.v_of(always, a) <= 1e-12 for a in (0.05, 0.2, 0.5, 0.9))
    w = np.where(rng.random(5000) < 0.6, e, rng.random(5000) < 0.3)
    t = rev.table(w, e)
    vs = [rev.v_of(t, float(a)) for a in rev.FINE]
    assert max(vs) == pytest.approx(t.pss, abs=0.02)
    assert rev.v_of(t, t.s) == pytest.approx(t.h - t.f)
    lo, hi = rev.v_range(t)
    assert lo < t.s < hi


def test_events_window_and_warning(rev: ModuleType) -> None:
    import numpy as np

    first = date(2001, 1, 1)  # a Monday
    days = [first + timedelta(days=i) for i in range(200)]
    px = np.full(len(days), 100.0)
    px[60:] = 88.0  # a 12% drop from day 60 on
    pos = np.ones(len(days))
    pos[33:40] = 0.0  # out in the week after the Friday of day 32 (2001-02-02)
    wk = rev.weekly("X", days, px, pos, np.ones(len(days), dtype=bool), last=days[-1])
    assert wk.fri[0] == date(2001, 1, 5)
    i = wk.fri.index(date(2001, 2, 2))
    assert wk.w[i] == 1.0 and wk.w.sum() == 1.0
    valid, ev = rev.events(wk, 0.10, 4, last=days[-1])
    hit = [f for f, v, x in zip(wk.fri, valid, ev, strict=True) if v and x]
    # Fridays whose 28-day window reaches day 60 (2001-03-02) and whose close is still 100
    assert hit == [date(2001, 2, 2), date(2001, 2, 9), date(2001, 2, 16), date(2001, 2, 23)]
    assert not valid[-1]  # the last Friday's window runs past the data


def test_money_bridges(rev: ModuleType) -> None:
    import numpy as np

    r = np.array([0.01, 0.01, -0.05, 0.01, -0.04, 0.01])
    e = np.array([0, 0, 1, 0, 1, 0], dtype=float)
    assert rev.alpha_hold(r, e) == pytest.approx(0.01 / (0.01 + 0.045))
    assert rev.v_money(r, e, e) == pytest.approx(1.0)
    assert rev.v_money(r, np.zeros(6), e) == pytest.approx(0.0)
    late = np.array([0, 0, 0, 1, 0, 1], dtype=float)  # out only after the falls
    assert rev.v_money(r, late, e) < 0
