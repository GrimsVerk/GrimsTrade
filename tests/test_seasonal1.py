"""seasonal-20y (research/lib/seasonal1_rules.py, card research/cards/seasonal-20y.md): the
season for a month is the 20-year same-month mean against the 240-month mean, from month-end
closes before the month only; the month's own return and anything later never enter it."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _mod(name: str) -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module(name)
    finally:
        sys.path.remove(str(LIB))


def _weekdays(start: date, end: date) -> list[date]:
    out: list[date] = []
    d = start
    while d <= end:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def _series(start: date, end: date) -> tuple[list[date], list[float]]:
    """Deterministic closes: a slow drift with a month-dependent wiggle (strong Januaries)."""
    days = _weekdays(start, end)
    px: list[float] = []
    x = 100.0
    for i, d in enumerate(days):
        x *= 1 + 0.0002 + (0.002 if d.month == 1 else 0.0) + 0.001 * math.sin(i * 0.7)
        px.append(x)
    return days, px


def test_rule_compares_same_month_mean_with_all_month_mean() -> None:
    sr = _mod("seasonal1_rules")
    r = {k: 0.01 for k in range(12 * 1980, 12 * 2001)}
    m = 12 * 2001  # January 2001
    assert sr.season_on(r, m) is True  # equal means: on (S >= A)
    for j in range(1, 21):
        r[m - 12 * j] = 0.0  # every past January below the average month
    assert sr.season_on(r, m) is False
    r[m - 12 * 20 - 1] = 0.5  # 241 months back: outside both windows, no effect
    assert sr.season_on(r, m) is False
    del r[m - 12], r[m - 24]  # only 18 of 20 Januaries: no signal
    assert sr.season_on(r, m) is None


def test_signal_never_sees_the_holding_month_or_later() -> None:
    sr = _mod("seasonal1_rules")
    days, px = _series(date(1960, 1, 1), date(1990, 12, 31))
    base = sr.season_of(days, px)
    assert len(base.on) > 100
    for m in sorted(base.on)[::7]:
        first = date(m // 12, m % 12 + 1, 1)
        # change every close from the first day of the holding month on, by a lot
        bumped = [
            p if d < first else p * (3.0 if d.day % 2 else 0.2)
            for d, p in zip(days, px, strict=True)
        ]
        assert sr.season_of(days, bumped).on[m] == base.on[m], m


def test_holding_month_switches_at_the_last_session() -> None:
    sr = _mod("seasonal1_rules")
    oct_, nov = sr.key(date(2024, 10, 1)), sr.key(date(2024, 11, 1))
    s = sr.Season({oct_: False, nov: True}, {oct_: date(2024, 10, 31)})
    assert s.state(date(2024, 10, 30)) is False  # Wednesday: next weekday still October
    assert s.state(date(2024, 10, 31)) is True  # Thursday, last session: November's season
    # a series with a session on Saturday the 31st waits for it
    o26, n26 = sr.key(date(2026, 10, 1)), sr.key(date(2026, 11, 1))
    s2 = sr.Season({o26: False, n26: True}, {o26: date(2026, 10, 31)})
    assert s2.state(date(2026, 10, 30)) is False
    assert s2.state(date(2026, 10, 31)) is True


def test_strategies_see_no_later_bar_end_to_end() -> None:
    """Decisions from a panel with the full history equal those from a panel cut at the
    decision day, for the overlay and the standalone rule, around month ends."""
    harness = _mod("harness")
    sr = _mod("seasonal1_rules")
    from grimstrade.data import ETF, UNIVERSE, Bar

    days, px = _series(date(1960, 1, 1), date(1984, 3, 31))
    bars = [Bar(d, p, p, p, p, 0.0) for d, p in zip(days, px, strict=True)]
    UNIVERSE["T-SEAS"] = ETF
    for name in ("overlay", "alone"):
        for d in (date(1982, 1, 29), date(1982, 2, 1), date(1983, 6, 30), date(1983, 7, 1)):
            cut = [b for b in bars if b.date <= d]

            def make(h: list[Any], name: str = name) -> Any:
                seas = {"T-SEAS": sr.season_of([b.date for b in h], [b.close for b in h])}
                live = sr.signal_live(seas)
                return sr.overlay(seas, live) if name == "overlay" else sr.alone(seas, live)

            full = harness.decisions(make(bars), harness.Panel({"T-SEAS": bars}), d, d)
            part = harness.decisions(make(cut), harness.Panel({"T-SEAS": cut}), d, d)
            assert full[0].weights == part[0].weights, (name, d)
            harness.check_against_gym(make(bars), {"T-SEAS": bars}, [d])


def test_yield_proxy_is_carry_minus_duration() -> None:
    sr = _mod("seasonal1_rules")
    r = sr.yield_to_bond({100: 6.0, 101: 5.0})
    assert math.isclose(r[101], math.log1p(0.005 + 0.17))
