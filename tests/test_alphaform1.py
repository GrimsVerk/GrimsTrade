"""The alpha-form statistics recover what is planted in synthetic series (card
research/alpha-form-1.md)."""

from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

RESEARCH = Path(__file__).resolve().parents[1] / "research"


def _af() -> Any:
    sys.path.insert(0, str(RESEARCH))
    try:
        return importlib.import_module("alphaform1")
    finally:
        sys.path.remove(str(RESEARCH))


N = 1600  # about 31 years of weeks
WPY = 52.18


def _tsmom(rng: np.random.Generator) -> np.ndarray:
    return 0.02 / math.sqrt(WPY) + rng.standard_normal(N) * 0.02  # annual Sharpe about 1.0


def test_known_alpha_is_recovered() -> None:
    af = _af()
    rng = np.random.default_rng(1)
    t = _tsmom(rng)
    sd_e = 0.02
    ir_true = 0.8
    a_true = ir_true * sd_e / math.sqrt(WPY)
    r = a_true + 0.1 * t + rng.standard_normal(N) * sd_e
    al = af.alpha(r, t)
    assert abs(al["b"] - 0.1) < 0.06
    assert abs(al["ir"] - ir_true) < 0.4  # SE of the IR over 31 years is about 0.18
    # z = IR sqrt(years), about 4.5 here
    assert abs(al["z_nw"] - al["ir"] * math.sqrt(N / WPY)) < 0.6
    mix = af.best_mix(r, t)
    assert 0 < mix["w"] < 1
    # gain matches sqrt(SR_t^2 + IR^2) - SR_t when the tangency weight is interior
    assert abs(mix["gain"] - (math.sqrt(mix["sr_t"] ** 2 + al["ir"] ** 2) - mix["sr_t"])) < 0.02


def test_leveraged_copy_has_no_alpha() -> None:
    af = _af()
    rng = np.random.default_rng(2)
    t = _tsmom(rng)
    r = 2.0 * t
    al = af.alpha(r, t)
    assert abs(al["b"] - 2.0) < 1e-9
    assert abs(al["a"]) < 1e-12
    mix = af.best_mix(r, t)
    assert abs(mix["gain"]) < 1e-9
    # a near-copy with a little noise: IR about 0, not significant
    r2 = 2.0 * t + rng.standard_normal(N) * 0.002
    assert abs(af.alpha(r2, t)["z_nw"]) < 3


def test_noise_is_not_significant_and_mix_is_clipped() -> None:
    af = _af()
    rng = np.random.default_rng(3)
    t = _tsmom(rng)
    r = rng.standard_normal(N) * 0.02 - 0.03 / math.sqrt(WPY)  # negative mean, uncorrelated
    al = af.alpha(r, t)
    assert al["z_nw"] < 1.0
    mix = af.best_mix(r, t)
    assert mix["w"] == 0.0  # long-only: no short of the losing rule
    assert mix["gain"] == 0.0


def test_bootstrap_se_is_close_to_iid_se() -> None:
    af = _af()
    rng = np.random.default_rng(4)
    t = _tsmom(rng)
    r = 0.4 * t + rng.standard_normal(N) * 0.015
    al = af.alpha(r, t)
    bs = af.boot(r, t, np.random.default_rng(5))
    assert 0.75 < bs["se_a"] / al["se_nw"] < 1.33
    assert bs["se_gain"] > 0


def test_nw_lag_rule() -> None:
    af = _af()
    assert af.nw_lag(100) == 4
    assert af.nw_lag(1657) == 7
