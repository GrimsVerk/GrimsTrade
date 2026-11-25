"""tick-tier-1's window split (research/lib/ticktier1.py; card research/cards/tick-tier-1.md).

- Window Sharpes from month cells equal the Sharpe of the returns inside the window.
- A rule identical to holding gives a timing contrast of exactly 0 in every draw.
- A planted break (small-tick classes lose their drift after 2009, bonds keep it) gives C < 0.
- The bill is charged per session from the rate known at the previous session.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


sys.path.insert(0, str(LIB))
qc: Any = _load("pooled2_core")
tt: Any = _load("ticktier1")


def _fridays(first: date, last: date) -> np.ndarray:
    d = first + timedelta(days=(4 - first.weekday()) % 7)
    out = []
    while d <= last:
        out.append(d.toordinal())
        d += timedelta(days=7)
    return np.array(out, dtype=np.int64)


def _mkt(name: str, group: str, f: np.ndarray, rets: dict[str, np.ndarray]) -> Any:
    m = qc.Mkt(name, group, "w", f)
    m.rets = rets
    return m


def _weekly(seed: int, f: np.ndarray, mu_pre: float, mu_post: float) -> np.ndarray:
    rng = np.random.default_rng(seed)
    cut = date(2009, 1, 1).toordinal()
    mu = np.where(f < cut, mu_pre, mu_post)
    return mu + rng.normal(0.0, 0.02, len(f))


def test_window_sharpe_matches_direct() -> None:
    f = _fridays(date(1994, 6, 3), date(2025, 10, 31))
    x = _weekly(1, f, 0.002, 0.0)
    m = _mkt("A", "EQ-US10", f, {r: x for r in tt.RULES})
    c = qc.cells([m], tt.RULES)
    sp, ok = tt.split(c, draws=3)
    assert ok.all()
    for win, got in ((tt.PRE, sp.pre), (tt.POST, sp.post)):
        sel = np.array(
            [win[0] <= date.fromordinal(int(o)) <= win[1] for o in f]  # month = Friday's month
        )
        w = x[sel]
        assert math.isclose(float(got[0, 0]), w.mean() / w.std() * math.sqrt(52), rel_tol=1e-9)


def test_rule_equal_to_hold_has_zero_timing_part() -> None:
    f = _fridays(date(1990, 1, 5), date(2025, 10, 31))
    ms = []
    for i, (n, g) in enumerate((("A", "EQ-US10"), ("B", "FX9"), ("C", "USB3"), ("D", "COM8"))):
        x = _weekly(10 + i, f, 0.001, 0.001)
        ms.append(_mkt(n, g, f, {r: x for r in tt.RULES}))
    res = tt.analyse(ms, draws=50)
    s = res["sum"]["tsmom12-timing"]["C"]
    assert s["est"] == 0.0
    assert s["se"] == 0.0


def test_planted_break_gives_negative_contrast() -> None:
    f = _fridays(date(1990, 1, 5), date(2025, 10, 31))
    ms = []
    k = 0
    for g, mu_post in (("EQ-US10", 0.0), ("FX9", 0.0), ("USB3", 0.004)):
        for _ in range(3):
            k += 1
            x = _weekly(100 + k, f, 0.004, mu_post)
            ms.append(_mkt(f"{g}-{k}", g, f, {"tsmom12": x, "e4": x, "hold": x * 0}))
    s = tt.analyse(ms, draws=200)["sum"]["tsmom12"]
    assert s["EQ"]["est"] < 0 and s["FX"]["est"] < 0
    assert s["C"]["est"] < -0.5
    assert tt.reading(s) == "consistent with the paper (class level)"


def test_bill_charged_from_previous_session() -> None:
    d = np.array([date(2000, 1, 3).toordinal(), date(2000, 1, 4).toordinal(),
                  date(2000, 1, 7).toordinal()], dtype=np.int64)  # fmt: skip
    bill = [(date(2000, 1, 3), 3.65), (date(2000, 1, 4), 7.30)]
    b = tt._bill_steps(d, bill)
    assert b[0] == 0.0
    assert math.isclose(b[1], 0.0365 * 1 / 365)
    assert math.isclose(b[2], 0.0730 * 3 / 365)


def test_asset_classes() -> None:
    assert tt.asset_class("IEF", "EQ-ETF8") == "BD"
    assert tt.asset_class("SLV", "EQ-ETF8") == "CM"
    assert tt.asset_class("IEF", "EQ-ETF8", as_is=True) == "EQ"
    assert tt.asset_class("FX-EUR", "FX9") == "FX"
    assert tt.asset_class("GOV10-JP", "GOV9") == "BD"
