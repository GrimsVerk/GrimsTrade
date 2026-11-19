"""The stop-reentry core (research/lib/stop_reentry_core.py) behaves as the card says.

- The hold at a decision does not change when later prices are scrambled (no look-ahead).
- It is never on where the twin is off, and equals the weekly stop before a coin's first
  stop-out.
- A stop-out keeps the coin out for 13 decisions, and afterwards the band is read against the
  highest close since the stop-out, not the old one-year high.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
sr: Any = importlib.import_module("stop_reentry_core")


def _weekly(
    pl: np.ndarray, vl: np.ndarray, d: np.ndarray, twin: np.ndarray, k: float
) -> np.ndarray:
    out = np.zeros(twin.shape, dtype=bool)
    for i, t in enumerate(d):
        for j in range(pl.shape[1]):
            win = pl[max(t - 364, 0) : t + 1, j]
            win = win[np.isfinite(win)]
            hi = win.max() if len(win) else np.nan
            _, ok = sr.stop_state(pl[t, j], vl[t, j], hi, k)
            out[i, j] = twin[i, j] and ok
    return out


def _book(
    seed: int = 3, n: int = 1500, c: int = 4
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    px = np.exp(np.cumsum(rng.normal(0, 0.05, (n, c)), axis=0))
    vl = np.full((n, c), 0.8)
    d = np.arange(400, n, 7)
    twin = rng.random((len(d), c)) < 0.8
    return px, vl, d, twin


def test_no_look_ahead_and_twin() -> None:
    px, vl, d, twin = _book()
    a, _ = sr.cool_hold(px, vl, d, twin, 0.25)
    i = 120
    t = int(d[i])
    px2 = px.copy()
    px2[t + 1 :] = np.random.default_rng(9).random(px2[t + 1 :].shape) * 50
    b, _ = sr.cool_hold(px2, vl, d, twin, 0.25)
    assert (a[: i + 1] == b[: i + 1]).all()
    assert not (a & ~twin).any()


def test_weekly_until_first_stop_out() -> None:
    px, vl, d, twin = _book()
    hold, outs = sr.cool_hold(px, vl, d, twin, 0.25)
    assert outs.any()
    w = _weekly(px, vl, d, twin, 0.25)
    before = np.cumsum(outs, axis=0) == 0
    assert (hold[before] == w[before]).all()
    huge, none = sr.cool_hold(px, vl, d, twin, 1e9)
    assert not none.any() and (huge == twin).all()


def test_cool_off_and_reset_high() -> None:
    # one coin, daily rows, decisions every 7 rows: a high of 100, a drop to 60 (stop-out),
    # then a flat 70 well below the old high
    n = 400
    px = np.full((n, 1), 100.0)
    px[100:, 0] = 60.0
    px[120:, 0] = 70.0
    vl = np.full((n, 1), 0.5)  # band: log(p / H) >= -0.125
    d = np.arange(0, n, 7)
    twin = np.ones((len(d), 1), dtype=bool)
    hold, outs = sr.cool_hold(px, vl, d, twin, 0.25)
    i_out = int(np.argmax(outs[:, 0]))
    assert d[i_out] == 105 and outs[:, 0].sum() == 1
    assert not hold[i_out : i_out + 13, 0].any()  # 13 decisions out, the stop-out's included
    # back in at the first decision 91 days on: 70 is within the band of the high since the
    # stop-out (70), though far below the old high (100)
    assert d[i_out + 13] == 105 + 91 and hold[i_out + 13 :, 0].all()
    w = _weekly(px, vl, d, twin, 0.25)
    assert not w[i_out + 13, 0]  # the weekly stop is still out there


def test_reentries_and_after_low() -> None:
    pos = np.array([0, 1, 1, 0, 0, 1, 0, 1, 1])
    assert sr.reentries(pos, 0, 8) == 2
    assert sr.reentries(np.ones(6), 0, 5) == 0
    r = np.arange(10, dtype=float)
    assert sr.after_low(r, 2, 3) == 3 + 4 + 5
    assert sr.after_low(r, 8, 5) == 9
