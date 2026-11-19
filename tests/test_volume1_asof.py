"""The volume-1 inputs are look-ahead safe and match the card (research/volume-1.md).

- Scrambling future bars leaves every feature's past unchanged.
- A Friday decision uses bars through Thursday only (a bar dated x from x + 1).
- BTC volume before the venue switch is not used; a volume doubling reads as log 2.
"""

from __future__ import annotations

import importlib
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def vol() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("volume1_ic")
    finally:
        sys.path.remove(str(LIB))


def _series(seed: int, n: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    close = 100 * np.exp(np.cumsum(0.01 * rng.standard_normal(n)))
    return close, np.exp(rng.standard_normal(n)) * 1e6


def test_daily_features_ignore_the_future(vol: Any) -> None:
    close, volume = _series(1, 900)
    c2, v2 = close.copy(), volume.copy()
    rng = np.random.default_rng(2)
    c2[600:] = close[600:] * np.exp(rng.standard_normal(300))
    v2[600:] = volume[600:] * 50
    a, b = vol.daily_features(close, volume, 5), vol.daily_features(c2, v2, 5)
    assert set(a) == set(vol.CANDIDATES)
    for name in vol.CANDIDATES:
        x, y = a[name][:600], b[name][:600]
        assert np.isfinite(x).any(), name
        assert np.array_equal(np.isnan(x), np.isnan(y)), name
        assert np.allclose(x[~np.isnan(x)], y[~np.isnan(y)]), name


def test_volume_doubling_and_sign(vol: Any) -> None:
    n = 400
    close = 100 * np.exp(0.001 * np.arange(n) + 0.01 * np.sin(np.arange(n)))  # rising
    volume = np.where(np.arange(n) >= n - 20, 2e6, 1e6)  # doubled over the last 4 weeks
    f = vol.daily_features(close, volume, 5)
    assert f["vol_chg4"][-1] == pytest.approx(np.log(2))
    assert f["vol_z52"][-1] > 2
    assert f["vw_trend13"][-1] > 0
    assert f["pv_div13"][-1] == pytest.approx(f["vol_chg13"][-1])  # up move, rising volume
    f_down = vol.daily_features(close[::-1].copy(), volume, 5)
    assert f_down["pv_div13"][-1] == pytest.approx(-f_down["vol_chg13"][-1])


def test_zero_volume_is_missing(vol: Any) -> None:
    close, volume = _series(3, 300)
    volume[:] = 0.0
    f = vol.daily_features(close, volume, 5)
    assert all(np.isnan(f[name]).all() for name in vol.CANDIDATES)


def test_friday_sees_bars_through_thursday_and_btc_cut(vol: Any) -> None:
    first = date(2014, 1, 1)
    n = 1100  # daily bars to 2017-01-04
    close, volume = _series(4, n)
    days = [first + timedelta(days=i) for i in range(n)]

    def bars(v: np.ndarray) -> list[Bar]:
        return [Bar(d, c, c, c, c, x) for d, c, x in zip(days, close, v, strict=True)]

    friday = date(2016, 12, 30)
    k = days.index(friday)
    bumped = volume.copy()
    bumped[k:] *= 100  # Friday's own bar and everything after
    early = volume.copy()
    early[: days.index(vol.BTC_FROM)] *= 100  # Bitstamp-era volume
    base = vol.features({"BTC": bars(volume)}, ["BTC"], [friday])
    for other in (bumped, early):
        got = vol.features({"BTC": bars(other)}, ["BTC"], [friday])
        for name in vol.CANDIDATES:
            assert np.isfinite(base[name][0, 0]), name
            assert got[name][0, 0] == pytest.approx(base[name][0, 0]), name
    # Thursday's bar is used: changing it changes the 4-week volume change.
    thursday = volume.copy()
    thursday[k - 1] *= 100
    got = vol.features({"BTC": bars(thursday)}, ["BTC"], [friday])
    assert got["vol_chg4"][0, 0] != pytest.approx(base["vol_chg4"][0, 0])
