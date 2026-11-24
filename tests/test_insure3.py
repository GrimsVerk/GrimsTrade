"""insure-3 (research/lib/insure3.py): data alignment, the trend rule without look-ahead, the mix.

- CBOE and Yahoo parsers keep nothing after the cut-off, whatever the file holds.
- `align` carries the last level over a missing session and refuses a missing first day.
- `splice` joins two total-return series on the joining day's own return.
- Bills accrue the yield seen before the session, per calendar day.
- The trend series (the record's `trend_tune.paper`) holds exactly the positions an independent
  restatement of the rule gives, and changing prices after a day never changes a position
  up to and including that day's next decision.
- The 50/50 mix is back to 50/50 after each month's last session.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from collections.abc import Iterator
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from grimstrade import data

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def ins() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mod = None
    for name in ("stats", "harness", "insure3"):
        spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    assert mod is not None
    yield mod
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path


def _sessions(start: date, n: int) -> list[date]:
    out: list[date] = []
    d = start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def _level(n: int) -> list[float]:
    """A deterministic path that rises, falls hard and recovers, so the rule flips."""
    out, x = [], 100.0
    for k in range(n):
        drift = 0.0008 if (k // 260) % 2 == 0 else -0.0012
        x *= 1 + drift + 0.006 * math.sin(k * 0.7)
        out.append(x)
    return out


def test_parsers_cut_at_last(ins: ModuleType) -> None:
    text = "DATE,PPUT\n10/30/2025,10.0\n10/31/2025,11.0\n11/03/2025,12.0\nbad,line\n"
    got = ins.parse_cboe(text)
    assert got == {date(2025, 10, 30): 10.0, date(2025, 10, 31): 11.0}
    ts = [int(datetime(2025, 10, d, 14, 30, tzinfo=UTC).timestamp()) for d in (30, 31)]
    ts.append(int(datetime(2025, 11, 3, 14, 30, tzinfo=UTC).timestamp()))
    obj: dict[str, Any] = {"chart": {"result": [{
        "timestamp": ts, "indicators": {"quote": [{"close": [1.0, None, 3.0]}]},
    }]}}  # fmt: skip
    assert ins.parse_yahoo(obj) == {date(2025, 10, 30): 1.0}


def test_align_carries_and_refuses_missing_first(ins: ModuleType) -> None:
    days = [date(2020, 1, 2), date(2020, 1, 3), date(2020, 1, 6)]
    lv, miss = ins.align(days, {days[0]: 1.0, days[2]: 3.0})
    assert list(lv) == [1.0, 1.0, 3.0] and miss == 1
    with pytest.raises(ValueError):
        ins.align(days, {days[1]: 1.0})


def test_splice_keeps_late_returns(ins: ModuleType) -> None:
    d = _sessions(date(2020, 1, 1), 5)
    early = {x: 10.0 + i for i, x in enumerate(d)}
    late = {x: 100.0 * 1.1**i for i, x in enumerate(d[2:])}
    out = ins.splice(early, late, d[2])
    assert out[d[1]] == early[d[1]]
    assert out[d[2]] / out[d[1]] == pytest.approx(early[d[2]] / early[d[1]])
    assert out[d[4]] / out[d[3]] == pytest.approx(1.1)


def test_bills_use_yield_before_session(ins: ModuleType) -> None:
    days = [date(2020, 1, 3), date(2020, 1, 6), date(2020, 1, 7)]  # Fri, Mon, Tue
    yld = {date(2020, 1, 3): 3.65, date(2020, 1, 6): 7.30}
    rf = ins.bill_returns(days, yld)
    assert rf[0] == 0.0
    assert rf[1] == pytest.approx(0.0365 * 3 / 365)  # Friday's yield, three calendar days
    assert rf[2] == pytest.approx(0.0730 / 365)


def test_trend_matches_rule_and_has_no_lookahead(ins: ModuleType) -> None:
    np = pytest.importorskip("numpy")
    days = _sessions(date(2010, 1, 4), 1400)
    lv = np.array(_level(len(days)))
    ret, pos = ins.trend(days, lv)
    own = ins.own_positions(days, lv)
    assert np.array_equal(pos, own)
    assert 0 < pos.sum() < len(pos) - 252  # the path makes it flip
    bar = np.zeros(len(lv))
    bar[1:] = lv[1:] / lv[:-1] - 1
    flips = np.abs(np.diff(pos, prepend=0.0))
    assert np.allclose(ret, pos * bar - ins.COST * flips)
    # change every price after a Friday: positions through the next Friday must not move
    for cut in (400, 777, 1100):
        while days[cut].weekday() != 4:
            cut += 1
        lv2 = lv.copy()
        lv2[cut + 1 :] *= np.linspace(0.3, 3.0, len(lv) - cut - 1)
        _, p2 = ins.trend(days, lv2)
        nxt = cut + 1
        while nxt < len(days) and days[nxt].weekday() != 4:
            nxt += 1
        assert np.array_equal(p2[: nxt + 1], pos[: nxt + 1])


def test_mix_rebalances_each_month(ins: ModuleType) -> None:
    np = pytest.importorskip("numpy")
    days = _sessions(date(2021, 1, 4), 60)
    a = np.full(len(days), 0.01)
    b = np.zeros(len(days))
    a[0] = b[0] = 0.0
    m = ins.mix(days, a, b)
    first_feb = next(i for i, d in enumerate(days) if d.month == 2)
    assert m[first_feb] == pytest.approx(0.005)  # back to 50/50 after January's last session
    assert m[first_feb - 1] > 0.005  # drifted towards a within January


def test_falls_and_cost(ins: ModuleType) -> None:
    np = pytest.importorskip("numpy")
    days = _sessions(date(2020, 1, 1), 8)
    hold = np.array([0.0, 0.1, -0.1, -0.1, 0.0, 0.2, 0.2, 0.0])
    half = hold / 2
    ff = ins.falls(days, {"hold": hold, "half": half}, "hold")
    assert len(ff) == 1 and ff[0].peak == days[1] and ff[0].trough == days[3]
    assert ff[0].hold == pytest.approx(0.81 - 1)
    assert ff[0].ins["half"] == pytest.approx(100 * (2 * math.log(0.95) - 2 * math.log(0.9)))
    assert ins.cost_ratio(2.0, ff, "half") == pytest.approx(2.0 / ff[0].ins["half"])
