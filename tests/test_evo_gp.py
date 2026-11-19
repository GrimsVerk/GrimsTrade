"""The evo-1 grammar and GP operators are what the card says (research/evo-1.md).

- 72 inputs; `tsmom12` is 4 nodes and holds an equal slot exactly where `mom(365) > 0`.
- A comparison with an undefined input is false; weights are long only and sum to at most 1.
- Random rules and every genetic operator stay inside the grammar and the size limits.
- A run is repeatable for a seed and scores at most population x (generations + 1) rules.
- On a toy world the search finds half of a strong planted rule; it holds up on unseen days.
"""

from __future__ import annotations

import importlib
import math
import sys
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    yield {n: importlib.import_module(n) for n in ("evo_gp", "evo_smoke")}
    sys.path[:] = saved_path


def _world(lib: dict[str, ModuleType], days: int = 50) -> tuple[Any, Any]:
    feats, ret = lib["evo_smoke"].toy_world(5, days, 0.0)
    return feats, ret


def test_grammar_size_and_tsmom12(lib: dict[str, ModuleType]) -> None:
    import numpy as np

    gp = lib["evo_gp"]
    assert len(gp.INPUTS) == 72
    tree = gp.TSMOM12[1]
    assert gp.size(tree) == 4 and gp.depth(tree) == 2 and gp.valid(tree)
    feats, _ = _world(lib)
    feats[("mom", 365)][0, 0] = math.nan  # undefined input: the comparison is false
    elig = np.ones((50, 6), dtype=bool)
    elig[:, 5] = False  # one asset not yet eligible: five equal slots
    w = gp.weights(gp.TSMOM12, feats, elig)
    want = np.where(elig & (np.nan_to_num(feats[("mom", 365)], nan=-1.0) > 0), 0.2, 0.0)
    assert np.array_equal(w, want)
    assert w[0, 0] == 0.0
    assert gp.show_rule(gp.TSMOM12) == "slot: if(mom(365) > 0, 1, 0)"


def test_weights_are_long_only_and_at_most_one(lib: dict[str, ModuleType]) -> None:
    import numpy as np

    gp = lib["evo_gp"]
    feats, _ = _world(lib)
    elig = np.ones((50, 6), dtype=bool)
    rng = np.random.default_rng(0)
    for i in range(200):
        rule = gp.random_rule(rng, 2 + i % 3, full=i % 2 == 1)
        w = gp.weights(rule, feats, elig)
        assert (w >= 0).all() and (w.sum(axis=1) <= 1 + 1e-12).all()
        if rule[0] == "full":
            tot = w.sum(axis=1)
            assert np.allclose(tot[tot > 0], 1.0)


def test_operators_stay_inside_the_grammar(lib: dict[str, ModuleType]) -> None:
    import numpy as np

    gp = lib["evo_gp"]
    rng = np.random.default_rng(1)
    pop = [gp.random_rule(rng, 2 + i % 3, full=i % 2 == 1) for i in range(60)]
    assert all(2 <= gp.depth(r[1]) <= 4 for r in pop)
    changed = 0
    for _ in range(40):
        nxt = []
        for i, a in enumerate(pop):
            b = pop[int(rng.integers(len(pop)))]
            child = (
                gp.crossover(a, b, rng),
                gp.subtree_mutation(a, rng),
                gp.point_mutation(a, rng),
            )[i % 3]
            assert child[0] in ("slot", "full")
            assert gp.valid(child[1]), gp.show_rule(child)
            assert gp.within_limits(child[1])
            changed += child != a
            nxt.append(child)
        pop = nxt
    assert changed > 1000


def test_point_mutation_always_changes_one_thing(lib: dict[str, ModuleType]) -> None:
    import numpy as np

    gp = lib["evo_gp"]
    rng = np.random.default_rng(2)
    for _ in range(300):
        child = gp.point_mutation(gp.TSMOM12, rng)
        assert child != gp.TSMOM12
        assert gp.size(child[1]) == 4


def test_run_is_repeatable_and_within_budget(lib: dict[str, ModuleType]) -> None:
    gp = lib["evo_gp"]
    calls = 0

    def fitness(rule: Any) -> float:
        nonlocal calls
        calls += 1
        return -float(gp.size(rule[1]))  # smaller is better: a fitness with no data

    a = gp.evolve(fitness, seed=3, population=40, generations=5)
    b = gp.evolve(fitness, seed=3, population=40, generations=5)
    assert a == b and list(a) == list(b)
    assert calls == 2 * len(a) and len(a) <= 40 * 6
    best = gp.order(a)[0]
    assert a[best] == max(a.values())


def test_search_finds_a_planted_rule(lib: dict[str, ModuleType]) -> None:
    """The strongest toy plant: the search gets the trend half of `H` and it holds up on days it
    never saw (the full conjunction is not found at this budget; see research/evo-1.md)."""
    res = lib["evo_smoke"].run(seed=1, k=0.2)
    assert res["evaluations"] <= 200 * 16
    assert "mom(91)" in str(res["best"])
    assert res["best_oos_sharpe"] > 1.0
    assert res["weight_corr_h"] > 0.5
    assert res["spa_consistent_p"] < 0.05
