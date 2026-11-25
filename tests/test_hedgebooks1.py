"""hedge-books-1 (research/lib/hedgebooks1.py): Hedge as carded, and no look-ahead.

- The weights after t rounds use rounds 1..t only: scrambling later outcomes leaves them as they
  were; a day's decision uses only rounds that ended by the end of the day before.
- The rate and bound are Cesa-Bianchi and Lugosi's Theorem 2.2; the realised loss regret stays
  under the bound; losses lie in [0, 1].
- The combined book is the Hedge-weighted sum of the books' targets: long-only, no leverage.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from collections.abc import Iterator
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from types import ModuleType

import pytest

from grimstrade import data, gym

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def hb() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mod = None
    for name in ("stats", "harness", "hedgebooks1"):
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


def _outcomes(n: int, k: int, seed: int):  # type: ignore[no-untyped-def]
    import numpy as np

    rng = np.random.default_rng(seed)
    return 1 + rng.normal(0.002, 0.03, size=(n, k))


def test_rounds_and_rate(hb: ModuleType) -> None:
    ths = hb.thetas()
    assert ths[0] == date(1994, 2, 3) and ths[-1] == date(2025, 10, 30)
    assert all(t.weekday() == 3 for t in ths)
    assert len(ths) - 1 == 1656
    assert hb.eta(16, 1656) == pytest.approx(math.sqrt(8 * math.log(16) / 1656))


def test_weights_use_only_past_rounds(hb: ModuleType) -> None:
    x = _outcomes(300, 5, 1)
    w = hb.hedge_weights(x, 0.3)
    assert w.shape == (301, 5)
    assert w[0] == pytest.approx([0.2] * 5)
    y = x.copy()
    y[150:] = _outcomes(150, 5, 2)  # a different future
    w2 = hb.hedge_weights(y, 0.3)
    assert (w2[:151] == w[:151]).all()
    assert not (w2[151:] == w[151:]).all()


def test_losses_bounded_and_regret_under_bound(hb: ModuleType) -> None:
    x = _outcomes(1000, 8, 3)
    lo = hb.losses(x)
    assert lo.min() >= 0 and lo.max() <= 1
    w = hb.hedge_weights(x, hb.eta(8, 1000))
    g = hb.regret_game(x, w)
    assert g["bound"] == pytest.approx(math.sqrt(1000 * math.log(8) / 2))
    assert g["loss_regret"] <= g["bound"]


def test_weights_on_a_day(hb: ModuleType) -> None:
    import numpy as np

    ths = [date(2024, 1, 4) + timedelta(days=7 * k) for k in range(4)]  # Thursdays
    w = np.arange(4)[:, None] * np.ones((1, 2))  # W[t] marked by t
    # before round 1 ends (Thu 2024-01-11), and on that Thursday itself: W[0]
    assert hb.weights_on(date(2024, 1, 11), ths, w)[0] == 0
    # the Friday after: round 1 ended at the end of the day before -> W[1]
    assert hb.weights_on(date(2024, 1, 12), ths, w)[0] == 1
    assert hb.weights_on(date(2024, 1, 18), ths, w)[0] == 1
    assert hb.weights_on(date(2024, 1, 19), ths, w)[0] == 2
    assert hb.weights_on(date(2030, 1, 1), ths, w)[0] == 3


def test_combine_is_weighted_sum_and_unlevered(hb: ModuleType) -> None:
    import numpy as np

    ths = [date(2024, 1, 4), date(2024, 1, 11)]
    t = datetime.combine(date(2024, 1, 12), time(22, 30), tzinfo=UTC)
    a = [gym.Decision(t, {"SPY": 1.0})]
    b = [gym.Decision(t, {"SPY": 0.5, "BTC": 0.5})]
    w = np.array([[0.5, 0.5], [0.25, 0.75]])
    (d,) = hb.combine([a, b], ths, w)
    assert d.weights == pytest.approx({"SPY": 0.25 + 0.375, "BTC": 0.375})
    assert sum(d.weights.values()) <= 1 + 1e-12
    bad = [gym.Decision(t + timedelta(hours=1), {"SPY": 1.0})]
    with pytest.raises(ValueError):
        hb.combine([a, bad], ths, w)
