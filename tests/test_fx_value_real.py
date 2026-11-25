"""fx-value-real-1: the swapped signal's sign and timing (synthetic data only)."""

from __future__ import annotations

import importlib.util
import math
import sys
from datetime import date
from pathlib import Path
from types import ModuleType

import pytest

PATH = Path(__file__).resolve().parents[1] / "research" / "lib" / "fx_value_real_run.py"


@pytest.fixture(scope="module")
def fv() -> ModuleType:
    spec = importlib.util.spec_from_file_location("fx_value_real_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _months(n: int) -> list[date]:
    return [date(2000 + (i // 12), i % 12 + 1, 1) for i in range(n)]


def test_point_value_is_minus_five_year_change_at_lag(fv: ModuleType) -> None:
    ms = _months(80)
    lnq = {d: 0.01 * i for i, d in enumerate(ms)}  # real rate rises 1% a month
    t = ms[70]
    # L = t - 2 = ms[68]; L - 60 = ms[8]: value = 0.08 - 0.68
    assert fv.point_value(lnq, t, 2) == pytest.approx(-0.60)
    assert fv.point_value(lnq, ms[60], 2) is None  # L - 60 before the data


def test_real_value_ranks_inflation_adjusted_cheapness(fv: ModuleType) -> None:
    """Spot falls 5 years in a row for both, but only one also fell in real terms."""
    ms = _months(80)
    xc = fv.xc
    spot = {d: math.exp(-0.005 * i) for i, d in enumerate(ms)}
    infl = {d: math.exp(0.005 * i) for i, d in enumerate(ms)}  # P_f / P_us grows as spot falls
    q_flat = {d: spot[d] * infl[d] for d in ms}  # PPP holds: real rate constant
    t = ms[75]
    assert xc.reversal_value(spot, t, 2) > 0.2  # the proxy calls it cheap
    assert xc.reversal_value(q_flat, t, 2) == pytest.approx(0.0, abs=1e-12)  # real: not cheap
