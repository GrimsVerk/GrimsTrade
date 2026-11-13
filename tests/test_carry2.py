"""Carry-2's venue panels (research/lib/carry2_panel.py) follow short-1's day rules (card in
research/carry-2.md):

- A funding event at 00:00 of day t+1 is paid on return day t, and is known to the signal
  only from day t+1.
- The daily funding signal is the mean rate of the day's events x 3.
- Nothing stamped after the train cut enters any panel.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _c2() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("carry2_panel")
    finally:
        sys.path.remove(str(LIB))


def test_funding_days_and_train_cut() -> None:
    c2 = _c2()
    d = 86400
    t5 = c2.T0 + 5 * d
    day_s = np.array([c2.T0 + i * d for i in range(10)] + [c2.CUT])
    close = np.arange(1.0, 12.0)
    ft = np.array([t5, t5 + 8 * 3600, t5 + 16 * 3600, c2.CUT])
    fr = np.array([0.001, 0.002, 0.003, 0.5])
    acc = c2.Acc()
    acc.add("X", day_s, close, close * 1e6, ft, fr, ft, fr)
    fsim = acc.cols["fsim"][0]
    fsig = acc.cols["fsig"][0]
    px = acc.cols["px"][0]
    assert fsim[4] == 0.001  # the 00:00 event of day 5 is paid on return day 4
    assert np.isclose(fsim[5], 0.005)
    assert np.isclose(fsig[5], 0.002 * 3)  # known on day 5: mean x 3
    assert np.isnan(fsig[4])
    assert fsim.sum() < 0.01 and np.isfinite(px).sum() == 10  # the cut drops the late rows
    assert np.nanmax(acc.cols["prem"][0]) < 0.5
