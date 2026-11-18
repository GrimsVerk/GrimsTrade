"""The rule of card `month-end-bonds` as plain functions of a trading calendar and opens, so
they can be tested without the harness (tests/test_monthend.py)."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date


def last_four(cal: Sequence[date], i: int) -> bool:
    """True if session `i` is one of the last four of its month. False when the calendar ends
    before the month does (its end is then unknown)."""
    for j in range(i + 1, min(i + 5, len(cal))):
        if (cal[j].year, cal[j].month) != (cal[i].year, cal[i].month):
            return True
    return False


def holds_after(cal: Sequence[date], i: int) -> bool:
    """The decision after the close of session `i`: hold if the next session (the one the fill
    opens) is one of the last four of its month. True after the closes of T-4 .. T-1."""
    return i + 1 < len(cal) and last_four(cal, i + 1)


def window_returns(days: Sequence[date], opens: Sequence[float]) -> list[tuple[date, float]]:
    """(T, return from the open of T-3 to the open of T+1) for every month end T that has both
    opens: what the rule earns in a month before costs."""
    out = []
    for t in range(3, len(days) - 1):
        if (days[t + 1].year, days[t + 1].month) != (days[t].year, days[t].month):
            out.append((days[t], opens[t + 1] / opens[t - 3] - 1))
    return out
