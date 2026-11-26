"""The gate-null-3 helpers compute what research/cards/gate-null-3.md says they do."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _mod() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("gatenull3")
    finally:
        sys.path.remove(str(LIB))


def test_acf1_ar1() -> None:
    m = _mod()
    rng = np.random.default_rng(0)
    x = np.zeros(20000)
    for i in range(1, len(x)):
        x[i] = 0.9 * x[i - 1] + rng.standard_normal()
    assert abs(m.acf1(x) - 0.9) < 0.01


def test_acf1_alternating() -> None:
    m = _mod()
    assert m.acf1([1.0, -1.0] * 50) < -0.98


def test_skew_and_end_gap() -> None:
    m = _mod()
    assert abs(m.skew([1.0, 2.0, 3.0])) < 1e-12
    assert m.skew([0.0, 0.0, 0.0, 10.0]) > 1.0
    assert abs(m.end_gap([0.0, 1.0, 0.0, 1.0]) - 2.0) < 1e-12
