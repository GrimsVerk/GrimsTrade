"""insure-1870-1: annual trend rule, segments, insurance decomposition and anchoring."""

from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "insure1870.py"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    spec = importlib.util.spec_from_file_location("insure1870_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _toy() -> tuple[dict[int, float], dict[int, float], dict[int, float]]:
    eq = {y: 0.10 for y in range(1900, 1930)}
    eq.update({1910: -0.20, 1911: -0.30, 1912: -0.10, 1913: 0.40, 1914: 0.30})
    bill = {y: 0.03 for y in range(1900, 1930)}
    cpi = {y: 1.02 ** (y - 1900) for y in range(1900, 1930)}
    return eq, bill, cpi


def test_signal_uses_only_the_year_before(m: ModuleType) -> None:
    eq, bill, cpi = _toy()
    (seg,) = m.segments("USA", eq, bill, cpi, last=1929)
    assert seg.years[0] == 1900 and seg.years[1] == 1901
    pos = dict(zip(seg.years[1:], seg.pos, strict=True))
    assert pos[1910] == 1.0  # 1909 beat bills: fully in for the first bad year
    assert pos[1911] == 0.0 and pos[1912] == 0.0 and pos[1913] == 0.0
    assert pos[1914] == 1.0  # 1913 beat bills
    # changing the year itself never changes its own position
    eq2 = {**eq, 1911: 5.0}
    (seg2,) = m.segments("USA", eq2, bill, cpi, last=1929)
    assert seg2.pos[seg2.years.index(1911) - 1] == 0.0


def test_gaps_split_segments_and_short_runs_drop(m: ModuleType) -> None:
    eq, bill, cpi = _toy()
    del bill[1915]
    segs = m.segments("FRA", eq, bill, cpi, last=1929)
    assert [(s.years[0], s.years[-1]) for s in segs] == [(1900, 1914), (1916, 1929)]
    assert len(m.segments("FRA", eq, bill, cpi, last=1910)) == 1
    assert m.segments("FRA", eq, bill, cpi, last=1909) == []  # 9 scored years only
    assert len(m.segments("FRA", eq, bill, cpi, last=1929, drop=frozenset({1922}))) == 1


def test_rule_return_cash_and_cost(m: ModuleType) -> None:
    eq, bill, cpi = _toy()
    (seg,) = m.segments("USA", eq, bill, cpi, last=1929)
    r = m.strat(seg, seg.pos)
    i = seg.years.index(1911) - 1
    assert r[i] == pytest.approx(0.03 - m.COST)  # switched to bills, one side paid
    assert r[i + 1] == pytest.approx(0.03)
    assert m.strat(seg, seg.pos, cash0=True)[i + 1] == 0.0


def test_episode_insurance_and_identity(m: ModuleType) -> None:
    eq, bill, cpi = _toy()
    (seg,) = m.segments("USA", eq, bill, cpi, last=1929)
    sc = m.episodes(seg, 0.25, 0.25)
    (e,) = sc.eps
    assert (e.peak, e.trough) == (date(1909, 12, 31), date(1912, 12, 31))
    want = 100 * (np.log(1.03 - m.COST) + np.log(1.03) - np.log(0.7) - np.log(0.9))
    assert e.ins == pytest.approx(want)
    assert e.rebound == pytest.approx(100 * (np.log(1.03) - np.log(1.4)))  # out in 1913
    total = sum(x.ins + x.rebound for x in sc.eps) + sc.calm
    assert total == pytest.approx(m.diff_cum(seg, m.strat(seg, seg.pos))[-1])


def test_anchors_are_labels_only(m: ModuleType) -> None:
    ep = m.i1.Episode
    anchor = ep("USA-1872", date(1928, 12, 31), date(1932, 12, 31), 0.5, -70, 0, 0, 0)
    a = ep("GBR-1871", date(1929, 12, 31), date(1931, 12, 31), 0.3, -40, 0, 10, 0)
    b = ep("SWE-1871", date(1927, 12, 31), date(1930, 12, 31), 0.3, -40, 0, 20, 0)
    c = ep("JPN-1886", date(1950, 12, 31), date(1952, 12, 31), 0.3, -40, 0, 5, 0)
    groups = m.anchored([anchor], [a, b, c])
    assert len(groups) == 2
    assert all(anchor not in g for g in groups)
    assert {x.series for x in groups[0]} == {"GBR-1871", "SWE-1871"}
