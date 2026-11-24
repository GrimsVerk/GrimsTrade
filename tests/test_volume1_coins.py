"""The cross-sectional IC of volume-1's card 2 finds a planted rank signal and nothing in noise."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def coins() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("volume1_coins")
    finally:
        sys.path.remove(str(LIB))


def test_xs_ic_planted_noise_and_masks(coins: Any) -> None:
    rng = np.random.default_rng(0)
    z = rng.standard_normal((200, 60))
    elig = np.ones(z.shape, dtype=bool)
    assert np.allclose(coins.xs_ic(np.exp(z), z, elig), 1.0)  # same ranks
    assert np.allclose(coins.xs_ic(-z, z, elig), -1.0)
    noise = coins.xs_ic(rng.standard_normal(z.shape), z, elig)
    assert abs(noise.mean()) < 0.03
    # Missing and ineligible cells are left out; too few coins gives NaN.
    sig = z.copy()
    sig[:, :10] = np.nan
    elig[:, 10:20] = False
    wrong = z.copy()
    wrong[:, 10:20] = -100 * z[:, 10:20]  # only in ineligible columns
    assert np.allclose(coins.xs_ic(sig, wrong, elig), 1.0)
    elig[0, 25:] = False
    assert np.isnan(coins.xs_ic(sig, z, elig)[0])
