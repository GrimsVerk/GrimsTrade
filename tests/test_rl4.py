"""The forecasters and the gate of run rl-4 do what the card says (research/rl-4.md).

- The purged CV never trains within 14 days of the rows it validates on.
- The score has no intercept, is zero for a zero forecast, and is 10 x the forecast.
- Each fit puts its largest weight on a planted input among noise inputs.
- The gate's bars are the card's.
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


@pytest.fixture(scope="module")
def sup() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    pytest.importorskip("sklearn")
    saved = list(sys.path)
    sys.path.insert(0, str(LIB))
    yield importlib.import_module("rl4_sup")
    sys.path[:] = saved


def rows(np: Any, n: int = 3000, k: int = 20, ic: float = 0.2) -> tuple[Any, Any, Any]:
    rng = np.random.default_rng(5)
    x = rng.standard_normal((n, k))
    y = ic * x[:, 3] + np.sqrt(1 - ic**2) * rng.standard_normal(n)
    days = 730_000 + 7 * (np.arange(n) // 6)  # six rows per Friday
    return x, y, days


def test_cv_is_purged(sup: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    _, _, days = rows(np)
    folds = sup.cv_folds(days)
    assert len(folds) == sup.CV_FOLDS
    assert (sum(va.astype(int) for _, va in folds) == 1).all()  # each row validated once
    for tr, va in folds:
        assert not (tr & va).any()
        gap = np.abs(days[tr][:, None] - days[va][None, ::50]).min()
        assert gap > sup.CV_GAP
        assert tr.sum() > len(days) / 2


@pytest.mark.parametrize("kind", ["ols", "ridge", "lasso"])
def test_fit_finds_the_planted_input(sup: ModuleType, kind: str) -> None:
    np: Any = pytest.importorskip("numpy")
    x, y, days = rows(np)
    f = sup.fit(kind, x, y, days)
    assert int(np.argmax(np.abs(f.beta))) == 3
    assert 0.1 < f.beta[3] < 0.3
    assert (f.penalty is None) == (kind == "ols")
    # no intercept in the score: shifting the target changes nothing
    g = sup.fit(kind, x, y + 5.0, days)
    assert np.allclose(f.score(x[:50]), g.score(x[:50]), atol=1e-6)
    # score = C x forecast on standardised inputs, and a missing input counts as its mean
    xs = (x[:50] - f.mu) / f.sd
    assert np.allclose(f.score(x[:50]), sup.C * xs @ f.beta)
    hole = x[:1].copy()
    hole[0, 3] = np.nan
    mean = x[:1].copy()
    mean[0, 3] = f.mu[3]
    assert np.allclose(f.score(hole), f.score(mean))


def test_zero_forecast_is_zero_score(sup: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    x, _, _ = rows(np)
    f = sup.Fit(x.mean(0), x.std(0), np.zeros(x.shape[1]), None)
    assert (f.score(x) == 0).all()


def test_gate_bars(sup: ModuleType) -> None:
    good = {
        "0.00": {"diff": -0.01, "p": 0.7},
        "0.10": {"diff": 0.06, "p": 0.02, "seeds_ahead": 8},
        "0.20": {"diff": 0.30, "p": 0.00},
    }
    assert all(sup.gate(good, 0.155).values())
    assert all(sup.gate(good, 0.155, rl=True).values())
    assert len(sup.gate(good, 0.155, rl=True)) == 5

    def change(rho: str, **kw: float) -> dict[str, dict[str, float]]:
        return {**good, rho: {**good[rho], **kw}}

    assert not all(sup.gate(change("0.10", p=0.2), 0.155).values())  # not significant
    assert not all(sup.gate(change("0.10", diff=0.04), 0.155).values())  # under a third
    assert not all(sup.gate(change("0.20", diff=-0.1), 0.155).values())
    assert not all(sup.gate(change("0.00", diff=-0.03), 0.155).values())  # trades noise
    assert not all(sup.gate(change("0.00", diff=0.05, p=0.01), 0.155).values())  # false find
    assert not all(sup.gate(change("0.10", seeds_ahead=6), 0.155, rl=True).values())
