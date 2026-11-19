"""The data-snooping correction of evo-1 does what its card says (research/evo-1.md).

- Many rules with no edge: the best looks good, the Reality Check and SPA do not reject.
- One rule with a real edge among the noise: both reject.
- Clearly bad rules inflate the Reality Check's luck but not the SPA's (lower <= consistent <=
  upper p).
- Chunked input gives the same answer as one block.
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
DAYS, RULES = 1500, 200


@pytest.fixture(scope="module")
def es() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    yield importlib.import_module("evo_stats")
    sys.path[:] = saved_path


def _noise(seed: int) -> Any:
    import numpy as np

    return np.random.default_rng(seed).normal(0.0, 0.01, size=(DAYS, RULES))


def test_noise_is_not_rejected(es: ModuleType) -> None:
    import numpy as np

    r = _noise(1)
    test = es.SnoopTest(np.zeros(DAYS), draws=300, seed=7)
    d = test.add(r)
    out = test.result()
    assert out["rules"] == RULES
    assert d.max() > 1.0  # the best of 200 unskilled rules looks like a find
    assert out["rc_p"] > 0.10
    assert out["spa_consistent_p"] > 0.10


def test_planted_rule_is_found(es: ModuleType) -> None:
    import numpy as np

    r = _noise(1)
    r[:, 17] += 0.0015  # a real edge: Sharpe near 2.9 a year
    test = es.SnoopTest(np.zeros(DAYS), draws=300, seed=7)
    d = test.add(r)
    out = test.result()
    assert int(d.argmax()) == 17
    assert out["rc_p"] < 0.05
    assert out["spa_consistent_p"] < 0.05


def test_spa_ignores_clearly_bad_rules(es: ModuleType) -> None:
    import numpy as np

    rng = np.random.default_rng(3)
    good = rng.normal(0.0004, 0.01, size=(DAYS, 1))
    bad = rng.normal(-0.006, 0.05, size=(DAYS, 300))  # wild losers: big luck, no chance
    test = es.SnoopTest(np.zeros(DAYS), draws=300, seed=7)
    test.add(np.hstack([good, bad]))
    out = test.result()
    assert out["spa_lower_p"] <= out["spa_consistent_p"] <= out["spa_upper_p"]
    assert out["spa_consistent_p"] < out["rc_p"]


def test_chunks_give_the_same_answer(es: ModuleType) -> None:
    import numpy as np

    r = _noise(2)
    bench = np.random.default_rng(9).normal(0.0003, 0.01, size=DAYS)
    whole = es.SnoopTest(bench, draws=200, seed=5)
    whole.add(r)
    parts = es.SnoopTest(bench, draws=200, seed=5)
    for k in range(0, RULES, 64):
        parts.add(r[:, k : k + 64])
    assert whole.result() == pytest.approx(parts.result())


def test_benchmark_copy_and_flat_rule(es: ModuleType) -> None:
    import numpy as np

    bench = np.random.default_rng(9).normal(0.0003, 0.01, size=DAYS)
    test = es.SnoopTest(bench, draws=100, seed=5)
    d = test.add(np.column_stack([bench, np.zeros(DAYS)]))
    assert d[0] == pytest.approx(0.0)
    assert d[1] == pytest.approx(-test.bench_sharpe)
    out = test.result()
    assert out["rc_p"] == 1.0  # nothing beats the benchmark
    assert out["spa_consistent_p"] == 1.0


def test_effective_n(es: ModuleType) -> None:
    import numpy as np

    r = _noise(4)
    assert es.effective_n(r) > 0.8 * RULES
    copies = np.repeat(r[:, :1], 50, axis=1)
    assert es.effective_n(copies) == pytest.approx(1.0)
