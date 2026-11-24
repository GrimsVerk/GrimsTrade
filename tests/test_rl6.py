"""The power-analysis helpers of run rl-6 do what research/rl-6.md says.

- A phase book trades only on its own weeks and holds its weights in between.
- A book rebalanced every 4 weeks turns over about a quarter as much as a weekly one.
- The noise summary ignores the mean: shifting a series changes none of its numbers.
- The detectable edge and the years needed follow the textbook formulas.
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Iterator
from math import sqrt
from pathlib import Path
from types import ModuleType

import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def pw() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    pytest.importorskip("sklearn")
    saved = list(sys.path)
    sys.path.insert(0, str(LIB))
    yield importlib.import_module("rl6_power")
    sys.path[:] = saved


def test_phase_book_holds_between_rebalances(pw: ModuleType) -> None:
    import numpy as np

    rng = np.random.default_rng(1)
    sig = rng.standard_normal((12, 30))
    m = np.ones((12, 30), bool)
    w = pw.phase_weights(sig, m, 4, 1)
    for i in range(12):
        if i % 4 == 1 or i == 0:
            assert np.array_equal(w[i], pw.third_book(sig[i], m[i]))
        else:
            assert np.array_equal(w[i], w[i - 1])
    assert abs(w[5].sum()) < 1e-12 and abs(np.abs(w[5]).sum() - 1) < 1e-12


def test_slow_book_trades_less(pw: ModuleType) -> None:
    import numpy as np

    rng = np.random.default_rng(2)
    sig = rng.standard_normal((400, 60))
    m = np.ones((400, 60), bool)
    weekly = pw.turnover_per_year(pw.phase_weights(sig, m, 1, 0))
    slow = pw.turnover_per_year(pw.phase_weights(sig, m, 4, 0))
    assert 0.2 < slow / weekly < 0.3


def test_noise_ignores_the_mean(pw: ModuleType) -> None:
    import numpy as np

    x = np.random.default_rng(3).standard_normal(240) * 0.02
    a, b = pw.noise(x), pw.noise(x + 0.5)
    for k in a:
        assert a[k] == pytest.approx(b[k])
    assert a["blocks"] == 60


def test_book_weeks_empty_book_is_nan(pw: ModuleType) -> None:
    import numpy as np

    w = np.array([[0.5, -0.5], [0.0, 0.0]])
    fwd = np.log1p(np.array([[0.02, 0.01], [0.1, 0.1]]))
    r = pw.book_weeks(w, fwd)
    assert r[0] == pytest.approx(0.005) and np.isnan(r[1])


def test_formulas(pw: ModuleType) -> None:
    assert pw.mde(0.02, 400, 1.0, 1.0) == pytest.approx(2 * 0.02 / 20)
    assert pw.years_needed(0.5, 1.0, 0.0) == pytest.approx(4.0)
    assert pw.years_needed(2.0 / sqrt(5), 1.0, 1.0) == pytest.approx(5.0)
