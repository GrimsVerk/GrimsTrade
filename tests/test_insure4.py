"""insure-4 (research/lib/insure4.py): PPUT while `tsmom12` is in, bills while out.

- While in, the rule earns PPUT's level-to-level return; while out, bills; 2 bps a side per
  switch.
- With the plain total return in place of PPUT it is exactly `tsmom12` (insure-3's series).
- No look-ahead: changing every S&P 500 price after a decision Friday leaves the rule's
  positions and returns through the next Friday unchanged; PPUT's later levels never move a
  position.
- The paired bootstrap is deterministic and zero for identical series.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType

import pytest

from grimstrade import data

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def ins() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mod = None
    for name in ("stats", "harness", "insure3", "insure4"):
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


def _sessions(start: date, n: int) -> list[date]:
    out: list[date] = []
    d = start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def _level(n: int) -> list[float]:
    out, x = [], 100.0
    for k in range(n):
        drift = 0.0008 if (k // 260) % 2 == 0 else -0.0012
        x *= 1 + drift + 0.006 * math.sin(k * 0.7)
        out.append(x)
    return out


def test_protected_switches_between_pput_and_bills(ins: ModuleType) -> None:
    np = pytest.importorskip("numpy")
    pos = np.array([0.0, 1.0, 1.0, 0.0, 0.0])
    r_in = np.array([0.0, 0.01, -0.02, 0.03, 0.04])
    rf = np.array([0.0, 0.001, 0.001, 0.001, 0.001])
    got = ins.protected(pos, r_in, rf, 0.0002)
    assert got[0] == 0.0
    assert got[1] == pytest.approx(0.01 - 0.0002)  # switch in: PPUT's return, one side's cost
    assert got[2] == pytest.approx(-0.02)
    assert got[3] == pytest.approx(0.001 - 0.0002)  # switch out: bills, one side's cost
    assert got[4] == pytest.approx(0.001)


def test_equals_tsmom12_with_total_return_and_no_lookahead(ins: ModuleType) -> None:
    np = pytest.importorskip("numpy")
    days = _sessions(date(2010, 1, 4), 1400)
    lv = np.array(_level(len(days)))
    bar = np.zeros(len(lv))
    bar[1:] = lv[1:] / lv[:-1] - 1
    rf = np.full(len(lv), 0.0001)
    rf[0] = 0.0
    tr, pos = ins.i3.trend(days, lv)
    got, pos2 = ins.rule_from_level(days, lv, bar, rf)
    assert np.array_equal(pos, pos2)
    assert 0 < pos.sum() < len(pos) - 252
    assert np.allclose(got[1:], (tr + (1 - pos) * rf)[1:])  # = insure-3's tsmom12 at bills
    # a PPUT-like series that differs from the index
    r_pp = bar * 0.7 - 0.0001 * np.cos(np.arange(len(lv)))
    r_pp[0] = 0.0
    base, bpos = ins.rule_from_level(days, lv, r_pp, rf)
    for cut in (400, 777, 1100):
        while days[cut].weekday() != 4:
            cut += 1
        nxt = cut + 1
        while nxt < len(days) and days[nxt].weekday() != 4:
            nxt += 1
        lv2 = lv.copy()
        lv2[cut + 1 :] *= np.linspace(0.3, 3.0, len(lv) - cut - 1)
        r2, p2 = ins.rule_from_level(days, lv2, r_pp, rf)
        assert np.array_equal(p2[: nxt + 1], bpos[: nxt + 1])
        assert np.allclose(r2[: nxt + 1], base[: nxt + 1])
        # later PPUT levels never move a position
        r_pp2 = r_pp.copy()
        r_pp2[cut + 1 :] = -0.05
        _, p3 = ins.rule_from_level(days, lv, r_pp2, rf)
        assert np.array_equal(p3, bpos)


def test_paired_test_is_deterministic(ins: ModuleType) -> None:
    np = pytest.importorskip("numpy")
    x = 0.0004 + 0.01 * np.sin(np.arange(3000) * 1.3)
    y = 0.0002 + 0.01 * np.sin(np.arange(3000) * 1.3 + 0.2)
    rf = np.zeros(3000)
    a = ins.paired_test(x, y, rf, draws=200)
    assert a == ins.paired_test(x, y, rf, draws=200)
    d, se, _, _ = ins.paired_test(x, x, rf, draws=50)
    assert d == 0.0 and se == 0.0
    assert ins.verdict(4.70) == "passes the bar" and ins.verdict(-2.0) == "worse than tsmom12"


def test_third_friday(ins: ModuleType) -> None:
    assert ins.third_friday(date(2020, 3, 20))
    assert not ins.third_friday(date(2020, 3, 13))
