"""The coin-cap-3 core (research/lib/coin_cap3_core.py) reads the stop daily as the card says.

- On a Friday both daily variants equal the weekly stop.
- `d` exits and re-enters on any day; `dx` exits on any day and re-enters only on a Friday.
- A variant's hold at decision t does not change when prices after t - 1 are scrambled.
- Round trips and the deepest-fall span follow their definitions.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
k3: Any = importlib.import_module("coin_cap3_core")


def test_fridays_equal_weekly_stop() -> None:
    rng = np.random.default_rng(0)
    week_d = np.arange(10, 200, 7)
    day_d = np.arange(10, 205)
    week_hold = rng.random((len(week_d), 3)) < 0.6
    ok = rng.random((300, 3)) < 0.7
    for mode in k3.MODES:
        h = k3.daily_hold(week_d, week_hold, day_d, ok, mode)
        fri = np.searchsorted(day_d, week_d)
        assert (h[fri] == (week_hold & ok[week_d])).all()


def test_d_and_dx_between_fridays() -> None:
    week_d = np.array([0, 7])
    day_d = np.arange(0, 10)
    week_hold = np.array([[True], [True]])
    ok = np.ones((10, 1), dtype=bool)
    ok[3] = False  # the stop fails on day 3 only
    d = k3.daily_hold(week_d, week_hold, day_d, ok, "d")[:, 0]
    dx = k3.daily_hold(week_d, week_hold, day_d, ok, "dx")[:, 0]
    assert d.tolist() == [1, 1, 1, 0, 1, 1, 1, 1, 1, 1]  # back in on day 4
    assert dx.tolist() == [1, 1, 1, 0, 0, 0, 0, 1, 1, 1]  # back in on the next Friday
    out = k3.daily_hold(week_d, np.array([[False], [True]]), day_d, ok, "d")[:, 0]
    assert out[:7].sum() == 0  # never in while the twin is out
    with pytest.raises(ValueError):
        k3.daily_hold(week_d, week_hold, day_d, ok, "weekly")


def test_no_look_ahead() -> None:
    rng = np.random.default_rng(1)
    px = np.exp(np.cumsum(rng.normal(0, 0.05, (900, 4)), axis=0))
    t = 700
    scr = px.copy()
    scr[t:] = px[t:] * np.exp(rng.normal(0, 0.5, px[t:].shape))  # prices stamped t and later
    a, b = k3.stop_ok(px, 1, 0.25), k3.stop_ok(scr, 1, 0.25)
    assert (a[: t + 1] == b[: t + 1]).all()  # usable at decision t: stamped t - 1 or earlier
    assert not (a[t + 1 :] == b[t + 1 :]).all()
    week_d = np.arange(400, 890, 7)
    week_hold = np.ones((len(week_d), 4), dtype=bool)
    day_d = np.arange(400, 890)
    for mode in k3.MODES:
        ha = k3.daily_hold(week_d, week_hold, day_d, a, mode)
        hb = k3.daily_hold(week_d, week_hold, day_d, b, mode)
        upto = int(np.searchsorted(day_d, t, side="right"))
        assert (ha[:upto] == hb[:upto]).all()


def test_round_trips_and_span() -> None:
    pos = np.array([0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    px = np.arange(1.0, 17.0)
    # exit earns its last return on row 2 (price px[2] = 3); back in from row 5 (bought at px[4])
    assert k3.short_round_trips(pos, px) == [pytest.approx(5 / 3 - 1)]  # second trip: 8 days
    assert len(k3.switches(pos[:, None])) == len(pos)
    assert int(k3.switches(pos[:, None]).sum()) == 5
    depth, peak, trough = k3.deepest_fall_span(np.array([0.1, 0.1, -0.3, 0.05, -0.1, 0.4]))
    assert depth == pytest.approx(0.35) and (peak, trough) == (2, 5)
