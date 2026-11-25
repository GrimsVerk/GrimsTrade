"""asset-ledger-1 (research/lib/assetledger1.py): the per-asset ledger and the book attribution.

- Fall gain, buy-back and calm drag add up to the whole gap to holding; a rule that always
  holds has a zero ledger; a rule out for a whole fall gains exactly that fall.
- The book attribution: each asset's P&L, summed, equals the gym's equity change, and the
  worst drawdown's contributions sum to minus the drawdown.
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

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
NAMES = ("stats", "harness", "gap2002", "calmdrag1", "assetledger1")


@pytest.fixture(scope="module")
def al() -> Iterator[ModuleType]:
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


def _ser(al: ModuleType, hold: Any, pos: Any, cost: float = 0.0) -> Any:
    import numpy as np

    days = [date(2001, 1, 1) + timedelta(days=i) for i in range(len(hold))]
    flip = np.abs(np.diff(pos, prepend=0.0))
    r0 = pos * hold - cost * flip
    n = len(hold)
    return al.cd.Ser("x", days, hold, pos, np.ones(n, dtype=bool), np.zeros(n), cost, r0, r0)


def _path() -> Any:
    """Calm, a 40% fall, a rebound, calm again (simple returns per session)."""
    import numpy as np

    r = [0.0] + [0.001] * 50 + [-0.02] * 25 + [0.015] * 60 + [0.001] * 400
    return np.array(r)


def test_parts_add_up_and_a_full_fall_out_gains_the_fall(al: ModuleType) -> None:
    import numpy as np

    hold = _path()
    pos = np.ones(len(hold))
    pos[51:76] = 0.0  # out for exactly the fall sessions
    s = _ser(al, hold, pos)
    part = al.cd.labels(s.days, s.hold)
    lg = al.ledger(s, s.days[0], s.days[-1], part, False)
    assert lg.falls == 1
    assert abs(lg.n - lg.i - lg.b - lg.c) < 1e-12
    fall = -100 * float(np.log1p(hold[51:76]).sum())
    assert lg.i == pytest.approx(fall / lg.yrs)
    assert lg.b == pytest.approx(0.0) and lg.c == pytest.approx(0.0)


def test_always_in_has_a_zero_ledger(al: ModuleType) -> None:
    import numpy as np

    hold = _path()
    s = _ser(al, hold, np.ones(len(hold)))
    lg = al.ledger(s, s.days[0], s.days[-1], al.cd.labels(s.days, s.hold), False)
    assert (lg.i, lg.b, lg.c, lg.n) == (0.0, 0.0, 0.0, 0.0)


def _hist(al: ModuleType) -> dict[str, list[data.Bar]]:
    data.UNIVERSE["AL1-A"] = data.ETF
    data.UNIVERSE["AL1-B"] = data.ETF
    out: dict[str, list[data.Bar]] = {"AL1-A": [], "AL1-B": []}
    pa = pb = 100.0
    d = date(2020, 1, 1)
    k = 0
    while len(out["AL1-A"]) < 80:
        if d.weekday() < 5:
            oa, ob = pa, pb
            pa *= 1 + (0.01 if k % 7 < 4 else -0.015) * (2 if 30 < k < 50 else 1)
            pb *= 1 + (-0.006 if k % 5 < 2 else 0.005)
            out["AL1-A"].append(data.Bar(d, oa, max(oa, pa), min(oa, pa), pa, 0.0))
            out["AL1-B"].append(data.Bar(d, ob, max(ob, pb), min(ob, pb), pb, 0.0))
            k += 1
        d += timedelta(days=1)
    return out


def test_book_attribution_sums_to_the_equity_change(al: ModuleType) -> None:
    hist = _hist(al)
    decs = []
    for i, b in enumerate(hist["AL1-A"][:-1]):
        if b.date.weekday() == 4:
            w = {"AL1-A": 0.5, "AL1-B": 0.5} if i % 2 else {"AL1-A": 0.7}
            decs.append(gym.Decision(datetime.combine(b.date, datetime.min.time(), UTC)
                                     + timedelta(hours=21), w))  # fmt: skip
    res = gym.simulate(decs, hist)
    days, eq, pnl, resid = al.attribute(res, hist)
    assert resid < 1e-12
    dr = al.worst(days, eq, pnl, days[0], days[-1])
    assert dr.dd > 0
    assert sum(dr.contrib.values()) == pytest.approx(-dr.dd, abs=1e-12)
