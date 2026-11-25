"""jst-autocorr-1: autocorrelation, per-episode share avoided, smoothing simulation, parsers."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "jstautocorr.py"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    spec = importlib.util.spec_from_file_location("jstautocorr_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_acf_pairs_stays_inside_series_and_mask(m: ModuleType) -> None:
    alt = np.array([1.0, -1.0] * 5)
    ac, n = m.acf_pairs([alt])
    assert n == 9 and ac == pytest.approx(-1.0)
    # pairs never cross from one series to the next
    ac2, n2 = m.acf_pairs([alt, alt])
    assert n2 == 18 and ac2 == pytest.approx(-1.0)
    keep = np.array([True] * 4 + [False] * 6)
    _, n3 = m.acf_pairs([alt], [keep])
    assert n3 == 3


def test_shares_by_hand(m: ModuleType) -> None:
    r = np.array([0.10, -0.20, -0.20, 0.50])  # the last year confirms the trough
    b = np.zeros(4)
    pos = np.array([1.0, 1.0, 0.0, 0.0])  # out after a year below bills
    pairs = m.episodes([_seg(m, r, b, pos)]).pairs[0]
    assert pairs == [(1, 3)]  # peak after year 1, trough after year 3
    s = m.shares(r, b, pos, pairs)[0, 0]
    ins = 100 * (math.log(1 - 0.0002) - math.log(0.8))
    assert s == pytest.approx(ins / abs(200 * math.log(0.8)))
    # always in: no insurance at all
    assert m.shares(r, b, np.ones(4), pairs)[0, 0] == pytest.approx(0.0)


def _seg(m: ModuleType, r: np.ndarray, b: np.ndarray, pos: np.ndarray) -> object:
    n = len(r)
    return m.ins.Seg("TST", list(range(1900, 1901 + n)), r, b, np.zeros(n), pos)


def test_time_averaging_gives_working_autocorrelation(m: ModuleType) -> None:
    rng = np.random.default_rng(1)
    xs, trues = [], []
    for _ in range(300):
        x, xt = m.averaged(rng, 60, 0.0, 0.2)
        xs.append(x)
        trues.append(xt)
    ac, _ = m.acf_pairs(xs)
    act, _ = m.acf_pairs(trues)
    assert 0.18 < ac < 0.30  # Working (1960): about 0.24 for 12-point averages
    assert abs(act) < 0.05  # December-to-December stays a random walk
    assert np.std(np.concatenate(xs)) == pytest.approx(0.2, rel=0.08)


def test_ar1_has_the_stated_persistence(m: ModuleType) -> None:
    rng = np.random.default_rng(2)
    x = m.ar1(rng, 20_000, 0.05, 0.2, 0.3)
    assert m.acf_pairs([x])[0] == pytest.approx(0.3, abs=0.03)
    assert x.std() == pytest.approx(0.2, rel=0.05)


def test_shiller_annual_conventions(m: ModuleType) -> None:
    # price grows 1% a month, no dividends
    mon = {(y, mo): (1.01 ** ((y - 1900) * 12 + mo), 0.0) for y in range(1900, 1904)
           for mo in range(1, 13)}  # fmt: skip
    out = m.shiller_annual(mon)
    g = 1.01**12 - 1
    assert out["Dec-Dec"][1901] == pytest.approx(g)
    assert out["Jan-Jan"][1901] == pytest.approx(g)
    assert out["annual average"][1902] == pytest.approx(g)


def test_norway_annual_average_and_dec(m: ModuleType) -> None:
    mon = {(1950, mo): 100.0 for mo in range(1, 13)}
    mon.update({(1951, mo): 100.0 + 10 * (mo == 12) for mo in range(1, 13)})
    out = m.norway_annual(mon)
    assert out["Dec-Dec"][1951] == pytest.approx(0.10)
    assert out["annual average"][1951] == pytest.approx(10 / 12 / 100)
