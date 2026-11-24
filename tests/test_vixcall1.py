"""vix-call-1 (research/lib/vixcall1.py): a VIX-call overlay on `tsmom12`.

- The overlay adds exactly the leg (VXTH's return minus the index's); with a zero leg V1 is
  `tsmom12` at bills; V2 with VXTH replaced by the index is `tsmom12` at bills.
- No look-ahead: changing every index and VXTH level after a decision Friday leaves V1's and V2's
  returns through the next Friday unchanged.
- The matched-cost bisection hits its target; leaving a fall out drops its sessions alike from
  every series.
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
def vc() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mod = None
    for name in ("stats", "harness", "insure3", "insure4", "vixcall1"):
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


def _level(n: int, phase: float = 0.0) -> list[float]:
    out, x = [], 100.0
    for k in range(n):
        drift = 0.0008 if (k // 260) % 2 == 0 else -0.0012
        x *= 1 + drift + 0.006 * math.sin(k * 0.7 + phase)
        out.append(x)
    return out


def test_overlay_adds_the_leg(vc: ModuleType) -> None:
    np = pytest.importorskip("numpy")
    r_vx = np.array([0.0, 0.02, -0.01, 0.30])
    r_hold = np.array([0.0, 0.01, -0.02, -0.10])
    lg = vc.leg(r_vx, r_hold)
    assert np.allclose(lg, [0.0, 0.01, 0.01, 0.40])
    base = np.array([0.0, 0.001, 0.0, -0.05])
    assert np.allclose(vc.overlay(base, lg), base + lg)
    assert np.allclose(vc.overlay(base, lg, 2.0), base + 2 * lg)
    assert np.array_equal(vc.overlay(base, np.zeros(4)), base)


def test_rules_reduce_to_tsmom12_and_have_no_lookahead(vc: ModuleType) -> None:
    np = pytest.importorskip("numpy")
    days = _sessions(date(2010, 1, 4), 1400)
    lv = np.array(_level(len(days)))
    rf = np.full(len(lv), 0.0001)
    rf[0] = 0.0
    tb = vc.trend_bills(days, lv, rf)
    # VXTH equal to the index: the leg is zero, V1 and V2 are tsmom12 at bills
    assert np.allclose(vc.v1_from_level(days, lv, lv, rf)[1:], tb[1:])
    v2, pos = vc.v2_from_level(days, lv, lv, rf)
    assert np.allclose(v2[1:], tb[1:])
    assert 0 < pos.sum() < len(pos) - 252
    vx = np.array(_level(len(days), phase=1.1))
    b1 = vc.v1_from_level(days, lv, vx, rf)
    b2, _ = vc.v2_from_level(days, lv, vx, rf)
    for cut in (400, 777, 1100):
        while days[cut].weekday() != 4:
            cut += 1
        nxt = cut + 1
        while nxt < len(days) and days[nxt].weekday() != 4:
            nxt += 1
        lv2, vx2 = lv.copy(), vx.copy()
        lv2[cut + 1 :] *= np.linspace(0.3, 3.0, len(lv) - cut - 1)
        vx2[cut + 1 :] *= np.linspace(2.0, 0.5, len(lv) - cut - 1)
        # returns up to the cut are unchanged; the positions through the next Friday too, so
        # V2's returns there move only with VXTH's own (changed) returns
        r1 = vc.v1_from_level(days, lv2, vx2, rf)
        assert np.allclose(r1[: cut + 1], b1[: cut + 1])
        _, p2 = vc.v2_from_level(days, lv2, vx2, rf)
        assert np.array_equal(p2[: nxt + 1], pos[: nxt + 1])


def test_solve_hits_target_and_clips(vc: ModuleType) -> None:
    x, clipped = vc.solve(lambda e: 0.02 + 0.08 * e, 0.06)
    assert x == pytest.approx(0.5, abs=1e-9) and not clipped
    x, clipped = vc.solve(lambda e: 0.10 - 0.08 * e, 0.04)  # decreasing
    assert x == pytest.approx(0.75, abs=1e-9) and not clipped
    x, clipped = vc.solve(lambda e: 0.02 + 0.08 * e, 0.5)
    assert x == 1.0 and clipped


def test_delever_and_matched_cagr(vc: ModuleType) -> None:
    np = pytest.importorskip("numpy")
    days = _sessions(date(2010, 1, 4), 800)
    r = np.zeros(800)
    r[1:] = 0.0006 + 0.01 * np.sin(np.arange(1, 800) * 0.9)
    rf = np.full(800, 0.00005)
    rf[0] = 0.0
    assert np.allclose(vc.delever(r, rf, 1.0)[1:], r[1:])
    target = vc.i3.cagr(r, days) - 0.01
    e, clipped = vc.solve(lambda x: vc.i3.cagr(vc.delever(r, rf, x), days), target)
    assert not clipped
    assert vc.i3.cagr(vc.delever(r, rf, e), days) == pytest.approx(target, abs=1e-9)


def test_leave_fall_out_and_premium(vc: ModuleType) -> None:
    np = pytest.importorskip("numpy")
    m = vc.keep_mask(6, 1, 3)
    assert m.tolist() == [True, True, False, False, True, True]
    x = np.array([0.0, 0.01, 0.5, 0.5, 0.01, 0.01])
    y = np.array([0.0, 0.01, -0.2, -0.2, 0.01, 0.01])
    assert vc.log_gap(x, y, m) == pytest.approx(0.0)
    assert vc.log_gap(x, y) > 0
    assert vc.premium_vs(5.0, 10.0) == pytest.approx(0.5)
    assert vc.premium_vs(-5.0, 10.0) == pytest.approx(1.5)
    assert math.isinf(vc.premium_vs(1.0, 0.0))
