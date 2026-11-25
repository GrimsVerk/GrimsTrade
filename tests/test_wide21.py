"""The wide-21 functions compute what research/cards/wide-21.md says they do."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide21_events")
    finally:
        sys.path.remove(str(LIB))


def test_forty_shifts_both_ways_away_from_the_solar_cycle() -> None:
    ev = _ev()
    assert len(ev.SHIFTS) == 40 and len(set(ev.SHIFTS)) == 40
    assert sorted(abs(k) for k in ev.SHIFTS) == sorted([*range(19, 96, 4)] * 2)
    for k in ev.SHIFTS:
        assert abs(k) >= 19 and abs(abs(k) - ev.CYCLE) >= 37
    assert len(ev.SHIFTS_YEARS) == 40
    assert not {10, 11, 12, 21, 22, 23} & {abs(k) for k in ev.SHIFTS_YEARS}


def test_parse_silso_skips_missing_and_months_after_the_cut() -> None:
    ev = _ev()
    text = (
        "1749;01;1749.042;  96.7; -1.0;   -1;1\n"
        "1749;02;1749.123;  -1.0; -1.0;   -1;1\n"
        "2025;10;2025.790;  50.0; 10.0; 1000;0\n"
        "2025;11;2025.870;  60.0; 10.0; 1000;0\n"
        "junk\n"
    )
    out = ev.parse_silso(text, date(2025, 10, 31))
    assert out == {1749 * 12: 96.7, 2025 * 12 + 9: 50.0}


def test_trailing_dose_needs_twelve_months() -> None:
    ev = _ev()
    sn = {m: float(m) for m in range(100, 124)}
    x = ev.trailing_dose(sn)
    assert min(x) == 111 and max(x) == 123
    assert math.isclose(x[111], sum(range(100, 112)) / 12 / 100)
    ph = ev.phase_dose(x)
    assert list(ph) == [123] and math.isclose(ph[123], 0.12)
    assert math.isnan(ev.shifted(x, 111, 1)) and ev.shifted(x, 112, 1) == x[111]


def test_parse_shiller_months_and_dividend_carry() -> None:
    ev = _ev()
    rows: list[list[object]] = [
        ["Date", "P", "D"],
        [1871.01, 4.44, 0.26],
        [1871.1, 4.5, 0.27],
        [1871.11, 4.6, ""],
        [2025.11, 6000.0, 70.0],
    ]
    sh = ev.parse_shiller(rows, date(2025, 10, 31))
    assert sh == {1871 * 12: (4.44, 0.26), 1871 * 12 + 9: (4.5, 0.27), 1871 * 12 + 10: (4.6, 0.27)}


def test_shiller_return_is_total_return_between_monthly_averages() -> None:
    ev = _ev()
    sh = {0: (100.0, 12.0), 1: (100.0, 12.0), 2: (110.0, 24.0), 3: (90.0, 12.0)}
    assert math.isclose(ev.shiller_return(sh, 0), math.log((110 + 2) / 100))
    assert math.isclose(ev.shiller_return(sh, 0, 2), math.log((90 + 2 + 1) / 100))
    assert math.isnan(ev.shiller_return(sh, 2))
    assert ev.fall_within(sh, 0, 3) == 0.0
    sh[3] = (80.0, 12.0)
    assert ev.fall_within(sh, 0, 3) == 1.0
    assert math.isnan(ev.fall_within(sh, 1, 3))


def test_maxima_and_window() -> None:
    ev = _ev()
    sn = {m: 100 * (1 + math.sin(2 * math.pi * m / 132)) for m in range(0, 600)}
    peaks = ev.maxima(ev.smoothed13(sn))
    assert all(abs((p - 33) % 132) <= 1 or abs((p - 33) % 132 - 132) <= 1 for p in peaks)
    assert len(peaks) >= 3
    w = ev.window_indicator(range(0, 300), [100])
    assert w[88] == 1.0 and w[124] == 1.0 and w[87] == 0.0 and w[125] == 0.0
    a = ev.annual_mean({m: 120.0 for m in range(24, 48)} | {48: 1.0})
    assert a == {2: 1.2, 3: 1.2}
