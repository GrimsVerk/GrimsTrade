"""insure-1's `infer_pos` (research/lib/insure1.py): the paper series' position from its returns.

The paper series is ret = pos * bar - cost * |pos - prev| (trend_tune.paper). A flip on a day the
holding does not move (bar 0) earns exactly -cost; the old reading took that as "no flip" and
dated the flip one session late (calm-drag-1's note, #203).
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from grimstrade import data

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
NAMES = ("harness", "insure1")
COST = 0.0002


@pytest.fixture(scope="module")
def i1() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    saved_mods = {n: sys.modules.get(n) for n in NAMES}
    sys.path.insert(0, str(LIB))
    mod = None
    for name in NAMES:
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
    for n, m in saved_mods.items():
        if m is None:
            sys.modules.pop(n, None)
        else:
            sys.modules[n] = m


def paper(pos: Any, bar: Any, cost: float = COST) -> Any:
    import numpy as np

    return pos * bar - cost * np.abs(np.diff(pos, prepend=0.0))


@pytest.mark.parametrize(
    "pos",
    [
        [0, 0, 1, 1, 1, 0, 0, 1, 1],  # into the market on a flat day (session 2), out on 5
        [0, 0, 0, 0, 0, 1, 1, 1, 0],  # into the market on a flat day (5), out on another (8)
        [0, 1, 0, 1, 0, 1, 0, 0, 0],  # a flip on every flat day
    ],
)
def test_a_flip_on_a_flat_day_is_dated_on_that_day(i1: ModuleType, pos: list[int]) -> None:
    import numpy as np

    p = np.array(pos, dtype=float)
    bar = np.array([0.0, 0.01, 0.0, 0.02, -0.01, 0.0, 0.03, -0.02, 0.0])
    got = i1.infer_pos(paper(p, bar), bar, COST)
    assert got.tolist() == p.tolist()
    # The cost then falls on the day of the flip, as the paper series has it.
    assert np.allclose(paper(got, bar), paper(p, bar), atol=1e-15)


def test_a_flip_whose_return_equals_the_cost_is_read_from_the_next_day(i1: ModuleType) -> None:
    """bar = cost: going in earns cost - cost = 0, staying out earns 0; both fit. The next day
    (in: bar - 0; out: 0) settles it."""
    import numpy as np

    bar = np.array([0.0, 0.01, COST, 0.01, 0.0])
    for pos in ([0, 0, 1, 1, 1], [0, 0, 0, 0, 0]):
        p = np.array(pos, dtype=float)
        assert i1.infer_pos(paper(p, bar), bar, COST).tolist() == p.tolist()


def test_random_paths_are_read_back_exactly(i1: ModuleType) -> None:
    import numpy as np

    rng = np.random.default_rng(0)
    for _ in range(200):
        n = 60
        bar = rng.normal(0, 0.01, n) * (rng.random(n) > 0.3)  # many flat days
        bar[0] = 0.0
        p = (rng.random(n) > 0.5).astype(float)
        p[0] = 0.0
        got = i1.infer_pos(paper(p, bar), bar, COST)
        assert np.allclose(paper(got, bar), paper(p, bar), atol=1e-15)
        assert got.tolist() == p.tolist()


# --- ties: a rule that stays in through a fall (insure-bonds-1, #219) ---


def held_series(i1: ModuleType) -> Any:
    """A rule that holds every session of a path with two falls of 25% or more. As in
    `insure1.build`, the rule's returns come from the closes and the holding from the closes
    rescaled, so the two differ at rounding size (about 1e-14 log points per fall)."""
    import numpy as np

    legs = [(120, 1.004), (90, 0.9955), (150, 1.0037), (80, 0.9951), (200, 1.0021)]
    steps = np.concatenate([np.full(n, g) * (1 + 1e-4 * np.sin(np.arange(n))) for n, g in legs])
    close = 37.3 * np.concatenate([[1.0], np.cumprod(steps)])
    px = close / close[0]
    days = [i1.date(1990, 1, 1) + i1.timedelta(days=i) for i in range(len(px))]
    rule = np.zeros(len(px))
    rule[1:] = close[1:] / close[:-1] - 1
    ones = np.ones(len(px))
    return i1.Series("held", days, px, rule, rule.copy(), ones, np.zeros(len(px)))


def test_a_rule_in_through_a_fall_has_no_insurance_and_no_rebound(i1: ModuleType) -> None:
    sc = i1.score(held_series(i1), 0.25, 0.25)
    assert len(sc.eps) == 2
    for e in sc.eps:
        assert (e.ins, e.rebound, e.ins_tb, e.net_tb, e.net) == (0.0, 0.0, 0.0, 0.0, 0.0)
    assert i1.sign_test([e.ins for e in sc.eps]) == (0, 0, 1.0)


def test_a_rounding_sized_value_is_a_tie_in_the_sign_test(i1: ModuleType) -> None:
    """A value within TIE of 0 is left out like an exact 0, not counted as a win or a loss."""
    assert i1.sign_test([1e-14, -3e-13, 2.0, -1.0, 0.5]) == (2, 3, 0.5)
    assert i1.sign_test([i1.TIE * 2, -i1.TIE * 2]) == (1, 2, 0.75)
