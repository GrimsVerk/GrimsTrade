"""The e4-anatomy-1 engine (research/lib/e4anatomy_core.py; card research/cards/e4-anatomy-1.md).

- The rules re-run with legs give exactly pooled-1's / pooled-2's `e4` and `tsmom12` returns.
- The decomposition adds up: return part + risk part = d; regimes and legs sum to the return
  part; the legs before costs are e4 minus `tsmom12`.
- Regime labels: insure-1's zigzag on a constructed path, fast against slow, rebound span,
  whipsaw only outside falls and rebounds, one label per period.
- The mix split is exact in both orders.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
READ = {"A": (0.25, 13), "W": (0.25, 26), "C": (0.15, 13)}


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def ec() -> ModuleType:
    pytest.importorskip("numpy")
    sys.path.insert(0, str(LIB))
    _load("pooled1_core")
    _load("pooled2_core")
    return _load("e4anatomy_core")


def market(seed: int, years: float = 8.0, vol: float = 0.2) -> tuple[Any, Any]:
    import numpy as np

    rng = np.random.default_rng(seed)
    days: list[int] = []
    d = date(1981, 1, 2)
    while len(days) < int(252 * years):
        if d.weekday() < 5:
            days.append(d.toordinal())
        d += timedelta(days=1)
    drift = np.repeat(rng.choice([-0.4, 0.4], len(days) // 80 + 1), 80)[: len(days)] / 252
    lr = drift + rng.normal(0, vol / math.sqrt(252), len(days))
    lr[0] = 0.0
    return np.array(days, dtype=np.int64), 100 * np.exp(np.cumsum(lr))


@pytest.mark.parametrize("seed", [1, 2])
def test_weekly_is_pooled1(ec: ModuleType, seed: int) -> None:
    import numpy as np

    pc = sys.modules["pooled1_core"]
    d, px = market(seed)
    s = ec.run_weekly("x", "g", d, px, d.copy(), pc.COST, READ)
    m = pc.run_market("x", "g", d, px)
    f, w_e4 = pc.weekly(d, m.daily["e4"], m.start)
    _, w_ts = pc.weekly(d, m.daily["tsmom12"], m.start)
    assert np.array_equal(s.periods, f)
    assert np.array_equal(s.r_e4, w_e4) and np.array_equal(s.r_ts, w_ts)


def test_monthly_is_pooled2(ec: ModuleType) -> None:
    import numpy as np

    qc = sys.modules["pooled2_core"]
    rng = np.random.default_rng(3)
    n = 240
    r = rng.normal(0.003, 0.04, n)
    months = [date(1980 + i // 12, i % 12 + 1, 1) for i in range(n)]
    s = ec.run_monthly("x", "g", months, r, 1, 0.0003, READ)
    m = qc.run_monthly("x", "g", months, r, 1, 0.0003)
    assert np.array_equal(s.r_e4, m.rets["e4"]) and np.array_equal(s.r_ts, m.rets["tsmom12"])
    assert np.allclose(s.legs["resid"], 0.0, atol=1e-15)


@pytest.mark.parametrize("seed", [4, 5])
def test_parts_add_up(ec: ModuleType, seed: int) -> None:
    import numpy as np

    pc = sys.modules["pooled1_core"]
    d, px = market(seed)
    s = ec.run_weekly("x", "g", d, px, d.copy(), pc.COST, READ)
    for rd in READ:
        p = ec.parts(s, rd)  # raises if the identities fail
        assert math.isclose(p.ret + p.risk, p.d, abs_tol=1e-12)
        assert math.isclose(sum(p.by_regime.values()), p.ret, abs_tol=1e-12)
        assert math.isclose(sum(p.by_leg.values()), p.ret, abs_tol=1e-12)
        assert math.isclose(sum(p.share.values()), 1.0)
        lab = s.labels[rd]
        assert lab.min() >= 0 and lab.max() <= 5 and len(lab) == len(s.r_e4)
    assert abs(ec.parts(s, "A").by_leg["resid"]) < 0.02  # weekly compounding only
    # the cells and pool sums give the same parts as the series itself
    p = ec.parts(s, "A")
    cal = ec.month_cells([s], "A", [p])
    st = ec.pool_stats(ec.totals(cal), np.array([True]), np.array([52.0]))
    assert math.isclose(sum(st["C"].values()), p.ret, abs_tol=1e-12)
    assert math.isclose(st["risk"], p.risk, abs_tol=1e-12)


def test_legs_before_costs(ec: ModuleType) -> None:
    import numpy as np

    d, px = market(6)
    s = ec.run_weekly("x", "g", d, px, d.copy(), 0.0, READ)
    legs = s.legs["1m"] + s.legs["3m"] + s.legs["6m"]
    assert np.allclose(s.legs["cost"], 0.0)
    assert np.allclose(legs + s.legs["resid"], s.r_e4 - s.r_ts, atol=1e-15)


def test_zigzag_labels(ec: ModuleType) -> None:
    import numpy as np

    # flat 50 days, -40% over 30 days (fast), +60% over 100 days, flat, -30% over 200 (slow),
    # +50% over 60, flat
    seg = [
        np.full(50, 100.0),
        np.linspace(100, 60, 31)[1:],
        np.linspace(60, 96, 101)[1:],
        np.full(100, 96.0),
        np.linspace(96, 67.2, 201)[1:],
        np.linspace(67.2, 100.8, 61)[1:],
        np.full(500, 100.8),
    ]
    px = np.concatenate(seg)
    ords = np.arange(len(px), dtype=np.int64) + 700000  # one point a calendar day
    pairs, open_pk = ec.zigzag(px, 0.25, 0.25)
    assert open_pk is None and len(pairs) == 2
    lab = ec.fall_labels(ords, px, 0.25, 0.25)
    (a1, b1), (a2, b2) = pairs
    assert a1 == 0 and b1 == 79 and a2 == 179 and b2 == 479
    assert (lab[a1 + 1 : b1 + 1] == ec.FASTC).all()
    assert (lab[a2 + 1 : b2 + 1] == ec.MEDC).all()
    # first rebound ends at the next peak (before trough + 365), second after 365 days
    assert (lab[b1 + 1 : a2 + 1] == ec.REBC).all()
    assert (lab[b2 + 1 : b2 + 366] == ec.REBC).all() and lab[b2 + 366] == ec.CALMC
    assert (lab[: a1 + 1] == ec.CALMC).all()


def test_whipsaw(ec: ModuleType) -> None:
    import numpy as np

    sig = np.array([1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
    w = ec.whipsaw(sig, 2)
    # changes at 4 and 5 (two flips close together), one at 12 (alone)
    assert w[3] and w[4] and w[5]
    assert not w[2] and not w[6]
    assert not w[1] and not w[9] and not w[12]


def test_mix_split_exact(ec: ModuleType) -> None:
    S_a = {"x": 0.2, "y": 0.8}
    C_a = {"x": 0.05, "y": 0.01}
    S_b = {"x": 0.05, "y": 0.95}
    C_b = {"x": 0.002, "y": 0.0}
    m = ec.mix_split(S_a, C_a, S_b, C_b, 0.03, 0.01)
    assert math.isclose(m["mix_at_b_rates"] + m["rates_at_a_mix"] + m["risk"], m["gap"])
    assert math.isclose(m["mix_at_a_rates"] + m["rates_at_b_mix"] + m["risk"], m["gap"])
