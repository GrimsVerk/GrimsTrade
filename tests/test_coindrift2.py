"""coin-drift-2 (research/lib/coindrift2.py) picks and builds its data as the card
(research/cards/coin-drift-2.md) says.

- The pick ranks by cap among eligible coins only and skips the excluded names.
- The bars are breadth-book-1's CM bars and stop at the last day (no later price can enter).
"""

from __future__ import annotations

import importlib
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
sys.path.insert(0, str(LIB))
cd2: Any = importlib.import_module("coindrift2")


def test_pick_ranks_eligible_by_cap_and_skips_excluded() -> None:
    names = ["btc", "a", "b", "c", "usdt", "d", "e"]
    elig = np.array([True, True, False, True, True, True, True])
    cap = np.array([100.0, 5.0, 50.0, 7.0, 9.0, np.nan, 1.0])
    got = cd2.pick_coins(names, elig, cap, ("btc", "usdt"), k=3)
    assert got == ["c", "a", "e"]  # b not eligible, d has no cap, btc/usdt excluded


def test_card_exclusions_cover_wide16_and_bases() -> None:
    for s in ("btc", "eth", "usdt", "ltc", "xrp", "bch", "etc", "xlm", "dash"):
        assert s in cd2.EXCLUDE
    assert not set(cd2.CARD_COINS) & set(cd2.EXCLUDE)


def test_bars_cut_at_last_day_and_open_at_previous_price() -> None:
    d0 = date(2018, 1, 1)
    series = [(d0 + timedelta(days=i), 10.0 + i) for i in range(10)]
    series.append((d0 + timedelta(days=4), -1.0))  # a bad price is dropped
    bars = cd2.cm_bars(series, d0 + timedelta(days=5))
    assert [b.date for b in bars] == [d0 + timedelta(days=i) for i in range(1, 6)]
    assert all(b.open == b.close - 1 for b in bars)
    assert all(b.low <= min(b.open, b.close) and b.high >= max(b.open, b.close) for b in bars)
    # prices after the last day do not change any bar
    later = series + [(d0 + timedelta(days=20), 999.0)]
    assert cd2.cm_bars(later, d0 + timedelta(days=5)) == bars
