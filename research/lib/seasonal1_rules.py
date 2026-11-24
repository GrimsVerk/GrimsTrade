"""seasonal-20y rules (card `research/cards/seasonal-20y.md`): pure logic, no data access.

A month is an integer key k = 12 * year + (month - 1). For a holding month M the season is on if
the mean of the same calendar month over the 20 years before (S) is not below the mean of all
240 months before (A); both from month-end closes of months before M only.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, timedelta

import common as c
from harness import ResearchStrategy, View, Weights

YEARS = 20
MIN_SAME = 19  # of 20 same-month returns
MIN_ALL = 228  # of 240 monthly returns
DURATION = 17.0  # TLT-like duration for the yield proxy


def key(d: date) -> int:
    return 12 * d.year + d.month - 1


def next_weekday(d: date) -> date:
    n = d + timedelta(days=1)
    while n.weekday() >= 5:
        n += timedelta(days=1)
    return n


@dataclass
class Season:
    """One asset's season by holding month, and the last close date of each month."""

    on: dict[int, bool]  # holding month -> season on; absent = no signal
    last_day: dict[int, date]  # month -> date of its last close in the series

    def state(self, today: date) -> bool | None:
        """Season for the holding month of a decision whose latest visible close is `today`.
        The holding month is the month of the next weekday; if the series still has a session
        in the month before (a Saturday session, say), the switch waits for that close."""
        m = key(next_weekday(today))
        if self.last_day.get(m - 1, date.min) > today:
            m -= 1
        return self.on.get(m)


def month_ends(
    days: Sequence[date], closes: Sequence[float]
) -> tuple[dict[int, float], dict[int, date]]:
    """Last close (and its date) of every calendar month present in the series."""
    px: dict[int, float] = {}
    when: dict[int, date] = {}
    for d, x in zip(days, closes, strict=True):
        if not math.isfinite(x) or x <= 0:
            continue
        k = key(d)
        if k not in when or d >= when[k]:
            px[k], when[k] = float(x), d
    return px, when


def monthly_logret(px: Mapping[int, float]) -> dict[int, float]:
    """r[k] = log(close at end of k / close at end of k - 1), only where both months exist."""
    return {k: math.log(v / px[k - 1]) for k, v in px.items() if k - 1 in px}


def season_on(r: Mapping[int, float], m: int, shift: int = 0) -> bool | None:
    """The card's rule for holding month m (shift = 0). `shift` s > 0 gives the placebo: the
    'same month' replaced by months 12 j + s before m. None when too few returns exist."""
    same = [r[m - 12 * j - shift] for j in range(1, YEARS + 1) if m - 12 * j - shift in r]
    every = [r[m - i] for i in range(1, 12 * YEARS + 1) if m - i in r]
    if len(same) < MIN_SAME or len(every) < MIN_ALL:
        return None
    return sum(same) / len(same) >= sum(every) / len(every)


def season_table(r: Mapping[int, float], shift: int = 0) -> dict[int, bool]:
    if not r:
        return {}
    out = {}
    for m in range(min(r) + 1, max(r) + 2):
        s = season_on(r, m, shift)
        if s is not None:
            out[m] = s
    return out


def season_of(days: Sequence[date], closes: Sequence[float]) -> Season:
    px, when = month_ends(days, closes)
    return Season(season_table(monthly_logret(px)), when)


def yield_to_bond(px: Mapping[int, float]) -> dict[int, float]:
    """Month-end yields in percent -> approximate long-bond log returns (carry minus duration
    times the change), the card's TLT proxy."""
    out = {}
    for k, y in px.items():
        if k - 1 in px:
            y0 = px[k - 1]
            out[k] = math.log1p(y0 / 1200 - DURATION * (y - y0) / 100)
    return out


# --- strategies ---

Live = Callable[[View], list[str]]


def signal_live(seasons: Mapping[str, Season]) -> Live:
    """Long data sets: a slot exists once the asset has a year of bars and a signal."""

    def f(view: View) -> list[str]:
        t = view.today
        return [
            s for s in view.syms
            if c.eligible(view, s) and s in seasons and seasons[s].state(t) is not None
        ]  # fmt: skip

    return f


def proto_live(view: View) -> list[str]:
    """Primary test: the protocol's slots (a year of bars)."""
    return c.live(view)


def _on(seasons: Mapping[str, Season], s: str, today: date) -> bool:
    """Season on, or no signal (the slot is then left as it is)."""
    st = seasons[s].state(today) if s in seasons else None
    return st is not False


def tsmom(live: Live) -> ResearchStrategy:
    def f(view: View) -> Weights:
        held = live(view)
        return {s: 1 / len(held) for s in held if c.tsmom_signal(view, s)}

    return c.weekly(f)


def hold(live: Live) -> ResearchStrategy:
    def f(view: View) -> Weights:
        held = live(view)
        return {s: 1 / len(held) for s in held}

    return c.weekly(f)


def overlay(seasons: Mapping[str, Season], live: Live) -> ResearchStrategy:
    base = tsmom(live)

    def f(view: View) -> Weights:
        t = view.today
        return {s: w for s, w in base(view).items() if _on(seasons, s, t)}

    return f


def alone(seasons: Mapping[str, Season], live: Live) -> ResearchStrategy:
    def f(view: View) -> Weights:
        held = live(view)
        t = view.today
        return {s: 1 / len(held) for s in held if _on(seasons, s, t)}

    return f
