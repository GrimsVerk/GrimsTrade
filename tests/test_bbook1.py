"""breadth-book-1's universe rules have no look-ahead (research/lib/bbook1_core.py).

- The ETF pool and its order read nothing after 2006-12-31.
- The coin list reads nothing after 2019-12-31.
- The effective number of bets at a row reads no later row, and counts planted structure.
- Nested sets keep their base and the fixed order.
"""

from __future__ import annotations

import importlib
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
core: Any = importlib.import_module("bbook1_core")  # no harness import: it changes global state


def _raw(first: date, last: date, close: float, vol: float) -> list[tuple[date, float, float]]:
    n = (last - first).days + 1
    return [(first + timedelta(i), close, vol) for i in range(n)]


def _pool(later: float) -> dict[str, list[tuple[date, float, float]]]:
    end = date(2025, 11, 10)
    out = {}
    for k, s in enumerate(core.POOL):
        early = _raw(date(2005, 1, 3), date(2006, 12, 31), 10.0, 1e5 * (k + 1))
        out[s] = early + _raw(date(2007, 1, 1), end, 10.0 * later, 1e3 * later)
    out["IEI"] = _raw(date(2007, 1, 5), end, 50.0, 1e7)  # starts too late
    out["FXA"] = _raw(date(2006, 1, 2), date(2006, 12, 31), 1.0, 1e3) + out["FXA"][-10:]
    return out


def test_pool_reads_nothing_after_2006() -> None:
    a, b = core.eligible_pool(_pool(1.0)), core.eligible_pool(_pool(777.0))
    assert a == b
    assert "IEI" not in a and "FXA" not in a  # too late; too thin
    assert core.round_robin(a) == core.round_robin(b)


def test_round_robin_cycles_classes_by_volume() -> None:
    dv = {"SPY": 3.0, "QQQ": 5.0, "TLT": 1.0, "GLD": 2.0, "SLV": 9.0, "FXE": 1.0}
    assert core.round_robin(dv) == ["QQQ", "TLT", "SLV", "FXE", "SPY", "GLD"]
    assert core.by_volume(dv)[:2] == ["SLV", "QQQ"]


def test_nested_keeps_base_then_order() -> None:
    order = ["SPY", "TLT", "GLD", "EEM", "FXE", "QQQ", "SHY"]
    assert core.nested(order, 3) == ["SPY", "TLT", "GLD"]
    six = core.SIX
    assert core.nested(order, 8, six) == [*six, "EEM", "FXE"]
    assert core.nested(order, 99, six) == [*six, "EEM", "FXE", "SHY"]


def _coins(seed: int, later: float) -> tuple[dict[str, dict[date, float]], dict[str, Any]]:
    rng = np.random.default_rng(seed)
    days = [date(2018, 6, 1) + timedelta(i) for i in range(900)]
    px: dict[str, dict[date, float]] = {}
    cap: dict[str, dict[date, float]] = {}
    base = np.cumsum(rng.normal(0, 0.04, len(days)))
    for a in ["btc", "eth", "aaa", "bbb", "usdx", "wbtc"]:
        if a == "usdx":
            lp = rng.normal(0, 0.0005, len(days))
        elif a == "wbtc":
            lp = base + rng.normal(0, 0.001, len(days))
        elif a == "btc":
            lp = base
        else:
            lp = np.cumsum(rng.normal(0, 0.04, len(days)))
        px[a] = {d: float(np.exp(x)) * (later if d > core.COIN_ASOF else 1) for d, x in
                 zip(days, lp, strict=True)}  # fmt: skip
        size = {"btc": 9e9, "eth": 5e9, "aaa": 1e9, "bbb": 2e9, "usdx": 8e9, "wbtc": 7e9}[a]
        cap[a] = {d: size * (1 / later if d > core.COIN_ASOF else 1) for d in days}
    return px, cap


def test_coin_list_reads_nothing_after_2019() -> None:
    a = core.coin_list(*_coins(0, 1.0), 10)
    b = core.coin_list(*_coins(0, 1e6), 10)
    assert a == b == ["btc", "eth", "bbb", "aaa"]  # stablecoin and wrapper dropped


def test_neff_reads_no_later_row_and_counts_structure() -> None:
    rng = np.random.default_rng(1)
    common = rng.normal(size=(200, 1))
    x = np.hstack([common, common, common, rng.normal(size=(200, 2))])
    e, rho = core.neff_at(x, 150, range(5))
    assert 2.0 < e < 2.6  # eigenvalues 3, 1, 1, 0, 0: 25 / 11 = 2.27
    y = x.copy()
    y[151:] = rng.normal(size=(49, 5)) * 100
    assert core.neff_at(y, 150, range(5)) == (e, rho)
    assert np.isnan(core.neff_at(x, 50, range(5))[0])  # not enough history yet


def test_paired_difference_of_identical_books_is_zero() -> None:
    r = np.random.default_rng(2).normal(0.0005, 0.01, 3000)
    d, se, _, p = core.paired(r, r, draws=200)
    assert d == 0 and se == 0 and p == 1.0
    d2, se2, z2, _ = core.paired(r + 0.0005, r, draws=200)
    assert d2 > 0 and se2 > 0 and z2 > 0
