"""Pure rules of the survey-2 card `fomc-cycle` (research/cards/fomc-cycle.md): FOMC-cycle week
labels (Cieslak, Morse and Vissing-Jorgensen 2019). No data access."""

from __future__ import annotations

import bisect
from collections.abc import Sequence
from datetime import date

import numpy as np

EVEN_SINCE = ((0, 3), (9, 13), (19, 23), (29, 33))  # weekdays since day 0, inclusive


def weekdays_between(a: date, b: date) -> int:
    """Number of weekdays (Mon-Fri) from `a` to `b`: 0 if equal, positive if `b` is later.
    Holidays count, as in the paper. Both dates are taken as weekdays."""
    return int(np.busday_count(a, b)) if a <= b else -int(np.busday_count(b, a))


def label(t: date, day0s: Sequence[date]) -> bool | None:
    """True if `t` is in an even FOMC-cycle week, False if odd, None before the first meeting.
    `day0s` must be sorted."""
    j = bisect.bisect_left(day0s, t)  # first day 0 on or after t
    if j < len(day0s):
        ahead = weekdays_between(t, day0s[j])
        if 1 <= ahead <= 6:
            return ahead == 1  # day -1 is week 0; days -6 .. -2 are week -1
    i = bisect.bisect_right(day0s, t) - 1  # last day 0 on or before t
    if i < 0:
        return None
    k = weekdays_between(day0s[i], t)
    return any(lo <= k <= hi for lo, hi in EVEN_SINCE)


def next_session(cal: Sequence[date], d: date) -> date | None:
    """The first session in `cal` after `d` (the session a decision after `d`'s close fills on)."""
    j = bisect.bisect_right(cal, d)
    return cal[j] if j < len(cal) else None
