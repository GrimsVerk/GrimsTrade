"""The wide-2 rule (research/lib/idea_wide2_trend_age.py) does what cards/trend-age.md says:
entry three weeks after the twin, exit with the twin, and no bar after the decision is read."""

from __future__ import annotations

import importlib
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _lib() -> tuple[Any, Any, Any]:
    sys.path.insert(0, str(LIB))
    try:
        return (
            importlib.import_module("idea_wide2_trend_age"),
            importlib.import_module("common"),
            importlib.import_module("harness"),
        )
    finally:
        sys.path.remove(str(LIB))


def _bars(closes: list[float], start: date = date(2018, 1, 1)) -> list[Bar]:
    out, d = [], start
    for x in closes:
        while d.weekday() >= 5:
            d += timedelta(days=1)
        out.append(Bar(d, x, x, x, x, 1.0))
        d += timedelta(days=1)
    return out


def _path() -> list[float]:
    # 300 sessions falling, then rising for good: the 365-day return turns positive once
    down = [100.0 - 0.1 * k for k in range(300)]
    up = [down[-1] + 0.3 * k for k in range(1, 400)]
    return down + up


def _weekly_flags(rule: Any, c: Any, h: Any, hist: dict[str, list[Bar]]) -> dict[date, bool]:
    panel = h.Panel(hist)
    first, last = hist["SPY"][260].date, hist["SPY"][-1].date
    ds = h.decisions(c.weekly(c.slots(rule)), panel, first, last)
    return {d.time.date(): "SPY" in d.weights for d in ds if d.time.date().weekday() == 4}


def test_entry_three_weeks_after_the_twin_and_exit_with_it() -> None:
    idea, c, h = _lib()
    closes = [*_path(), *[1.0] * 30]  # a crash at the end: both leave
    hist = {"SPY": _bars(closes)}
    twin = _weekly_flags(c.tsmom_signal, c, h, hist)
    aged = _weekly_flags(idea.aged_signal, c, h, hist)
    days = sorted(twin)
    on_t = [d for d in days if twin[d]]
    on_a = [d for d in days if aged[d]]
    assert on_t and on_a
    assert on_a[0] == on_t[0] + timedelta(days=21)  # entry: three Fridays later
    assert on_a[-1] == on_t[-1]  # exit: the same Friday
    assert all(twin[d] for d in on_a)  # never holds what the twin does not


def test_uses_no_later_data() -> None:
    idea, c, h = _lib()
    closes = _path()
    cut = 500
    other = closes[:cut] + [5.0 + (k % 7) for k in range(len(closes) - cut)]  # scrambled future
    a = _weekly_flags(idea.aged_signal, c, h, {"SPY": _bars(closes)})
    b = _weekly_flags(idea.aged_signal, c, h, {"SPY": _bars(other)})
    last_seen = _bars(closes)[cut - 1].date
    same = [d for d in a if d <= last_seen]
    assert len(same) > 20 and any(a[d] for d in same)
    assert all(a[d] == b[d] for d in same)
