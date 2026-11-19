"""trend-where-long's monthly rule: all-yes is tsmom12 exactly, answers and weights never see
later returns, and the gap month is respected (research/cards/trend-where-long.md)."""

from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
import pytest

PATH = Path(__file__).resolve().parents[1] / "research" / "lib" / "trend_where_long.py"


@pytest.fixture(scope="module")
def tw() -> ModuleType:
    spec = importlib.util.spec_from_file_location("trend_where_long_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def grid(tw: ModuleType, seed: int = 1, months: int = 240) -> Any:
    rng = np.random.default_rng(seed)
    series = {}
    for j, name in enumerate(("a", "b")):
        start = 1960 * 12 + 3 * j
        r = rng.normal(0.004, 0.03 + 0.02 * j, months)
        series[name] = [(tw.mdate(start + i), 1 + float(x)) for i, x in enumerate(r)]
    return tw.Grid.build(series)


def test_all_yes_is_tsmom12_and_all_no_is_hold(tw: ModuleType) -> None:
    g = grid(tw)
    yes: Any = np.full(g.r.shape, True)
    w_where, _ = tw.weights(g, "where", 1, yes)
    w_ts, _ = tw.weights(g, "tsmom12", 1)
    assert np.array_equal(w_where, w_ts)
    w_no, _ = tw.weights(g, "where", 1, ~yes)
    w_hold, _ = tw.weights(g, "hold", 1)
    assert np.array_equal(w_no, w_hold)


def test_refit_and_weights_ignore_later_returns(tw: ModuleType) -> None:
    g = grid(tw)
    cut = 150
    later = tw.Grid(g.first, g.names, g.r.copy())
    later.r[cut + 1 :] = np.random.default_rng(9).normal(0, 0.2, later.r[cut + 1 :].shape)
    keeps = []
    for gg in (g, later):
        valid, on = tw.signals(gg.r)
        keeps.append(tw.keep_table(gg, tw.labels(valid, on, 1), 1.0, 5))
    assert np.array_equal(keeps[0][: cut + 1], keeps[1][: cut + 1])
    assert not keeps[0].all()  # the test exercises a real "no"
    # the weight on the return dated m depends on returns dated <= m - 2 only (gap month)
    w1, _ = tw.weights(g, "where", 1, keeps[0])
    w2, _ = tw.weights(later, "where", 1, keeps[1])
    assert np.array_equal(w1[: cut + 3], w2[: cut + 3])


def test_signal_and_drawdown(tw: ModuleType) -> None:
    r = np.full((14, 1), 0.01)
    r[12, 0] = -0.5
    valid, on = tw.signals(r)
    assert not valid[10, 0] and valid[11, 0] and on[11, 0] and not on[12, 0]
    assert tw.max_dd(np.array([0.1, -0.5, 0.2])) == pytest.approx(0.5)
    assert tw.decision_of(5, 1) == 3
    assert tw.mdate(tw.mnum(date(1971, 1, 1))) == date(1971, 1, 1)
