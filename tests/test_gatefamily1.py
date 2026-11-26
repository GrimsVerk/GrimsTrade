"""The gate-family-1 arithmetic computes what research/cards/gate-family-1.md says it does."""

from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _mod() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("gatefamily1")
    finally:
        sys.path.remove(str(LIB))


def test_poisson_binomial_matches_binomial() -> None:
    g = _mod()
    d = g.poisson_binomial([0.1] * 5)
    for j in range(6):
        assert math.isclose(d[j], math.comb(5, j) * 0.1**j * 0.9 ** (5 - j))
    assert math.isclose(sum(d), 1.0)


def test_tail_and_subset() -> None:
    g = _mod()
    assert math.isclose(g.tail([0.5, 0.5], 1), 0.75)
    assert math.isclose(g.all_in_subset(40, 10, 3), 120 / 9880)


def test_records_family() -> None:
    g = _mod()
    assert len(g.GATES) == 40
    assert [x.gid for x in g.GATES if x.passed] == ["W32", "W36", "W45"]
    assert not any(x.gid.startswith("R") for x in g.GATES)


def test_pass_probabilities() -> None:
    g = _mod()
    by = {x.gid: x for x in g.GATES}
    assert math.isclose(g.p_rank(by["W32"]), 2 / 41)
    assert math.isclose(g.p_own_t(by["W32"]), 0.5 / 41)  # zero share: half a draw
    assert math.isclose(g.p_own_t(by["W45"]), 2 / 41)  # wide null: rank binds
    assert all(g.p_own_t(x) <= g.p_rank(x) + 1e-12 for x in g.GATES)


def test_recorded_thresholds_and_bootstrap_cap() -> None:
    g = _mod()
    by = {x.gid: x for x in g.GATES}
    assert math.isclose(g.p_rank(by["W3"]), 3 / 29)
    assert math.isclose(g.p_rank(by["W13"]), 3 / 15)
    assert math.isclose(g.p_rank(by["W15"]), 2 / 23)
    assert math.isclose(g.p_rank(by["W41n"]), 2 / 21)
    assert math.isclose(g.p_rank(by["W41n"], use_cap=True), 0.05)
