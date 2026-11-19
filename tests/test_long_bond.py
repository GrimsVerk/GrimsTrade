"""Shiller long-bond loader finds the split header and reads monthly returns (research/lib)."""

from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path
from types import ModuleType

import pytest

PATH = Path(__file__).resolve().parents[1] / "research" / "lib" / "long_bond.py"


@pytest.fixture(scope="module")
def lb() -> ModuleType:
    spec = importlib.util.spec_from_file_location("long_bond_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


# Tiny copy of the ie_data "Data" sheet layout: labels split over rows, then "Date".
SHEET: list[list[object]] = [
    ["", "", "", "", ""],
    ["", "Long", "Monthly", "Real", ""],
    ["", "Interest", "Total", "Total", ""],
    ["", "Rate", "Bond", "Bond", ""],
    ["Date", "Rate GS10", "Returns", "Returns", ""],
    [1871.01, 5.32, 1.004, 100.0, ""],
    [1871.1, 5.33, 0.99, 99.0, ""],
    [1871.11, 5.34, "", "", "note"],
    ["", "Sept GS10 is Sept 1st value", "", "", ""],
]


def test_parse_reads_monthly_returns(lb: ModuleType) -> None:
    out = lb.parse(SHEET)
    assert out == [(date(1871, 1, 1), 1.004), (date(1871, 10, 1), 0.99)]
    assert lb.total_return_index(out) == pytest.approx([1.004, 1.004 * 0.99])


def test_parse_rejects_missing_column(lb: ModuleType) -> None:
    bad = [row[:2] for row in SHEET]
    with pytest.raises(ValueError):
        lb.parse(bad)
