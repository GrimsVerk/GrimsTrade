"""The micro-1 inputs (card in research/micro-1.md, "Data and as-of rule").

- The daily table measures what the card says: session bars only, New York time, overnight
  from the previous session's close.
- A Friday sees only days before it: changing Friday's and later days leaves it unchanged.
"""

from __future__ import annotations

import importlib
import math
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _load(name: str) -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module(name)
    finally:
        sys.path.remove(str(LIB))


@pytest.fixture(scope="module")
def days_mod() -> Any:
    return _load("micro1_days")


@pytest.fixture(scope="module")
def ic_mod() -> Any:
    return _load("micro1_ic")


def _minute(day: date, hour_utc: int, minute: int) -> int:
    return int(datetime(day.year, day.month, day.day, hour_utc, minute, tzinfo=UTC).timestamp())


def test_day_stats_session_and_overnight(days_mod: Any) -> None:
    # January: New York = UTC - 5, so the session is 14:30-21:00 UTC.
    d1, d2 = date(2020, 1, 2), date(2020, 1, 3)
    ts, o, c = [], [], []
    for day, base in ((d1, 100.0), (d2, 110.0)):
        ts.append(_minute(day, 9, 0))  # pre-market bar at a wild price: must be ignored
        o.append(1.0)
        c.append(1.0)
        for k in range(390):  # one bar a minute through the session
            ts.append(_minute(day, 14, 30) + 60 * k)
            o.append(base)
            # the close doubles in the last minute of the first five-minute bin, then stays
            c.append(base if k < 4 else 2 * base)
    stats = days_mod.day_stats(np.array(ts), np.array(o), np.array(c), True, days_mod.SESSION)
    k1 = (d1 - date(1970, 1, 1)).days
    rv, bv, rsp, rsn, first_open, last_close = stats[k1]
    assert rv == pytest.approx(math.log(2) ** 2)  # one five-minute return of log 2
    assert bv == pytest.approx(0.0)  # a lone jump: no bipower variation
    assert (rsp, rsn) == (pytest.approx(rv), 0.0)
    assert (first_open, last_close) == (100.0, 200.0)
    table = dict(days_mod.rows(stats, stats))
    assert math.isnan(table[d1][4])  # no session before the first
    assert table[d2][4] == pytest.approx(math.log(110.0 / 200.0))  # overnight
    assert table[d2][5] == pytest.approx(math.log(2))  # intraday


def test_thin_day_is_missing(days_mod: Any) -> None:
    day = date(2020, 1, 2)
    ts = np.array([_minute(day, 15, 0) + 300 * k for k in range(10)])
    px = np.linspace(100.0, 101.0, 10)
    assert days_mod.day_stats(ts, px, px, True, days_mod.SESSION) == {}


def test_friday_sees_only_earlier_days(ic_mod: Any) -> None:
    rng = np.random.default_rng(1)
    start = date(2018, 1, 1)
    days = [start + timedelta(days=i) for i in range(700)]

    def table(vals: np.ndarray) -> dict[str, Any]:
        d = {k: vals[:, i] for i, k in enumerate(ic_mod.FIELDS)}
        d["rv"] = np.abs(d["rv"]) + 1.0
        d["bv"] = np.abs(d["bv"])
        d["rsp"] = np.abs(d["rsp"])
        d["rsn"] = np.abs(d["rsn"])
        return {"BTC": (days, d)}

    vals = rng.normal(size=(700, len(ic_mod.FIELDS)))
    fridays = [d for d in days if d.weekday() == 4]
    cut = fridays[80]
    changed = vals.copy()
    changed[days.index(cut) :] += 5.0  # Friday itself and everything after
    a = ic_mod.features(table(vals), ["BTC"], fridays)
    b = ic_mod.features(table(changed), ["BTC"], fridays)
    for name in ic_mod.CANDIDATES:
        assert np.isfinite(a[name][80, 0]), name
        np.testing.assert_array_equal(a[name][:81], b[name][:81])
        assert not np.array_equal(a[name][81:], b[name][81:], equal_nan=True), name
