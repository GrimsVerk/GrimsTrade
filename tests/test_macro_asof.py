"""The research macro layer never uses a number before it was public (research/lib/macro.py)."""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

PATH = Path(__file__).resolve().parents[1] / "research" / "lib" / "macro.py"


@pytest.fixture(scope="module")
def macro() -> ModuleType:
    spec = importlib.util.spec_from_file_location("macro_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def rec(obs: str, start: str, end: str, value: float | str) -> dict[str, str]:
    return {"date": obs, "realtime_start": start, "realtime_end": end, "value": str(value)}


def last(snap: dict[date, float], obs: list[date]) -> float:
    return snap[obs[-1]]


def test_vintage_value_is_used_only_from_the_day_after_publication(macro: Any) -> None:
    raw = [
        rec("2020-01-01", "2020-02-14", "2020-03-13", 100),
        rec("2020-01-01", "2020-03-14", "9999-12-31", 110),  # revised a month later
    ]
    step = macro.vintage_feature(macro.vintage_records("X", raw), last)
    assert math.isnan(step.at(date(2020, 2, 14)))  # published that day: not yet usable
    assert step.at(date(2020, 2, 15)) == 100
    assert step.at(date(2020, 3, 14)) == 100  # the revision is not seen on its own day
    assert step.at(date(2020, 3, 15)) == 110


def test_today_revised_numbers_are_not_used_for_the_past(macro: Any) -> None:
    raw = [
        rec("2020-01-01", "2020-02-14", "2020-03-13", 1),
        rec("2020-01-01", "2020-03-14", "9999-12-31", 2),
        rec("2020-02-01", "2020-03-14", "9999-12-31", 3),
    ]
    step = macro.vintage_feature(macro.vintage_records("X", raw), lambda s, o: s[o[0]])
    assert step.at(date(2020, 3, 1)) == 1  # the first print, not the revised 2


def test_market_value_is_used_from_the_next_day(macro: Any) -> None:
    raw = [
        rec("2020-01-06", "2026-11-11", "2026-11-11", 1.5),
        rec("2020-01-07", "2026-11-11", "2026-11-11", "."),
    ]
    step = macro.market_feature(macro.market_records("Y", raw), macro.last_value)
    assert math.isnan(step.at(date(2020, 1, 6)))
    assert step.at(date(2020, 1, 7)) == 1.5
    assert step.at(date(2020, 1, 9)) == 1.5  # the missing '.' day changes nothing


def test_observations_older_than_the_first_vintage_count_as_public_late(macro: Any) -> None:
    raw = [rec("2010-01-06", "2011-07-07", "9999-12-31", 5.0)]
    recs = macro.vintage_records("WALCL", raw)
    step = macro.vintage_feature(recs, last)
    assert math.isnan(step.at(date(2010, 1, 13)))  # 7-day lag, then the day after
    assert step.at(date(2010, 1, 14)) == 5.0


def _random_records(rng: random.Random) -> list[dict[str, str]]:
    raw = []
    base = date(2000, 1, 1)
    for m in range(24):
        obs = date(2000 + m // 12, m % 12 + 1, 1)
        start = obs + timedelta(days=30 + rng.randrange(20))
        while start < base + timedelta(days=900):
            end = start + timedelta(days=rng.randrange(1, 200))
            raw.append(rec(obs.isoformat(), start.isoformat(), end.isoformat(), rng.random()))
            if rng.random() < 0.1:  # sometimes the observation disappears for a while
                end += timedelta(days=rng.randrange(1, 30))
            start = end + timedelta(days=1)
        raw[-1]["realtime_end"] = "9999-12-31"
    return raw


def test_feature_equals_the_vintage_a_reader_saw_the_day_before(macro: Any) -> None:
    rng = random.Random(7)
    recs = macro.vintage_records("X", _random_records(rng))
    step = macro.vintage_feature(recs, lambda s, o: sum(s.values()) + 1000 * len(o))
    for k in range(0, 1000, 3):
        d = date(2000, 2, 1) + timedelta(days=k)
        snap = macro.snapshot(recs, d - timedelta(days=1))
        want = sum(snap.values()) + 1000 * len(snap) if snap else math.nan
        got = step.at(d)
        assert (math.isnan(want) and math.isnan(got)) or got == pytest.approx(want), d


def test_changing_the_future_does_not_change_the_past(macro: Any) -> None:
    rng = random.Random(11)
    raw = _random_records(rng)
    cut = date(2001, 3, 1)
    scrambled = [
        {**r, "value": str(rng.random())} if date.fromisoformat(r["realtime_start"]) >= cut else r
        for r in raw
    ]
    fn = macro.yoy
    a = macro.vintage_feature(macro.vintage_records("X", raw), fn)
    b = macro.vintage_feature(macro.vintage_records("X", scrambled), fn)
    for k in range(400):
        d = cut - timedelta(days=k)
        x, y = a.at(d), b.at(d)
        assert (math.isnan(x) and math.isnan(y)) or x == y, d


def test_halving_bear_window(macro: Any) -> None:
    assert not macro.Features.halving_bear(None, date(2021, 11, 9))  # day 547
    assert macro.Features.halving_bear(None, date(2021, 11, 10))  # day 548
    assert not macro.Features.halving_bear(None, date(2012, 1, 1))  # before any halving
