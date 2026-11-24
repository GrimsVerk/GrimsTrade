"""reconcile-1 (research/lib/reconcile1.py) tells live from gym and names the cause.

On a small synthetic record (bars, a ledger written with `ledger.write_decision`):
- a live book that decided at the backtest's own times matches the backtest every day;
- one that decided a few hours late (the delayed schedule) differs, and every gap is (a);
- one whose ledger weights are not what its strategy gives is (c), also day by day;
- the fill check finds a fill at a wrong price, off an open, or cash that does not add up;
- snapshots: cents tolerance, (c) when the code that ran disagrees with what it wrote, (d) when
  only today's gym does; bars a run could not have had are found.
"""

from __future__ import annotations

import dataclasses
import importlib
import sys
from collections.abc import Iterator
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from grimstrade import gym, ledger, report
from grimstrade.data import Bar, History, visible_history

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def rc() -> Iterator[ModuleType]:
    sys.path.insert(0, str(LIB))
    try:
        yield importlib.import_module("reconcile1")
    finally:
        sys.path.remove(str(LIB))


START = date(2026, 11, 2)  # a Monday
DAYS = 12


def bars(prices: list[float], weekdays_only: bool) -> list[Bar]:
    out = []
    for i, px in enumerate(prices):
        d = START + timedelta(days=i)
        if weekdays_only and d.weekday() >= 5:
            continue
        out.append(Bar(d, px, px * 1.01, px * 0.99, px * 1.002, 1.0))
    return out


def history() -> History:
    btc = [100.0 * (1 + 0.03 * ((-1) ** i) + 0.01 * i) for i in range(DAYS)]
    spy = [50.0 + 0.5 * i for i in range(DAYS)]
    return {"BTC": bars(btc, False), "SPY": bars(spy, True)}


def trend(h: History) -> tuple[dict[str, float], str]:
    """Depends on the newest BTC close, so seeing one bar more can change it."""
    b = h["BTC"]
    if len(b) < 2:
        return {}, "warm-up"
    w = 0.6 if b[-1].close > b[-2].close else 0.3
    return {"BTC": w, "SPY": 0.3}, "test"


def at(d: date, hh: int, mm: int = 0) -> datetime:
    return datetime.combine(d, time(hh, mm), tzinfo=UTC)


def write_ledger(root: Path, h: History, times: list[datetime], tamper: int | None = None) -> None:
    for i, t in enumerate(times):
        w, why = trend(visible_history(h, t))
        if i == tamper:
            w = {"BTC": 0.1, "SPY": 0.1}
        ledger.write_decision(root, t, "trend", w, visible_history(h, t), why)


def books(
    rc: ModuleType, root: Path, h: History, times: list[datetime]
) -> tuple[gym.Result, gym.Result, gym.Result, dict[datetime, str]]:
    live = report.live_results(root, h)["trend"]
    rows = ledger.decisions(root, "trend")
    first, last = rc.due_day(times[0]), rc.due_day(times[-1])
    bt = gym.simulate(gym.backtest(trend, h, first, last), h)
    recomputed = [gym.Decision(t, trend(visible_history(h, t))[0]) for t in times]
    same_t = gym.simulate(recomputed, h)
    classes = {}
    for t, r in zip(times, rows, strict=True):
        if c := rc.classify_weights(
            r["weights"],
            recomputed[times.index(t)].weights,
            recomputed[times.index(t)].weights,
            None,
        ):
            classes[t] = c
    return live, same_t, bt, classes


def test_live_at_backtest_times_matches_every_day(rc: Any, tmp_path: Path) -> None:
    h = history()
    times = [at(START + timedelta(days=i), 22, 30) for i in range(1, DAYS - 2)]
    write_ledger(tmp_path, h, times)
    live, same_t, bt, classes = books(rc, tmp_path, h, times)
    out = rc.compare_days("trend", live, same_t, bt, classes)
    assert out.days >= 8
    assert out.matched == out.days and not out.findings
    assert rc.check_fills("trend", live, [gym.Decision(t, {}) for t in times], h) == []


def test_delayed_runs_differ_only_by_schedule(rc: Any, tmp_path: Path) -> None:
    h = history()
    # Due day D, run at 03:00 on D+1 (DECISIONS 2026-11-24): sees crypto bar D, fills it at D+2.
    times = [at(START + timedelta(days=i + 1), 3) for i in range(1, DAYS - 2)]
    write_ledger(tmp_path, h, times)
    live, same_t, bt, classes = books(rc, tmp_path, h, times)
    assert classes == {}
    out = rc.compare_days("trend", live, same_t, bt, classes)
    assert out.days - out.matched >= 1
    assert set(out.by_class) == {"a"}
    assert out.max_equity_gap > 0
    # And the weights: the 03:00 run sees one crypto bar more than 22:30 on its due day.
    d = START + timedelta(days=4)
    late, on_time = (
        trend(visible_history(h, at(d + timedelta(days=1), 3))),
        trend(visible_history(h, at(d, 22, 30))),
    )
    assert late[0] != on_time[0]  # BTC alternates up and down: the extra bar flips the weight
    assert rc.classify_weights(late[0], late[0], late[0], on_time[0]) == "a"
    assert rc.classify_weights(late[0], late[0], late[0], late[0]) is None


def test_wrong_ledger_weights_are_a_bug(rc: Any, tmp_path: Path) -> None:
    h = history()
    times = [at(START + timedelta(days=i), 22, 30) for i in range(1, DAYS - 2)]
    write_ledger(tmp_path, h, times, tamper=3)
    live, same_t, bt, classes = books(rc, tmp_path, h, times)
    assert classes == {times[3]: "c"}
    out = rc.compare_days("trend", live, same_t, bt, classes)
    assert out.by_class.get("c", 0) >= 1
    assert all(f.cls == "c" for f in out.findings)


def test_weight_classes(rc: Any) -> None:
    w, v = {"BTC": 0.5}, {"BTC": 0.5 + 1e-12}
    assert rc.classify_weights(w, v, v, v) is None
    assert rc.classify_weights(w, {"BTC": 0.4}, w, w) == "c"
    assert rc.classify_weights(w, w, {"BTC": 0.4}, w) == "b"
    assert rc.classify_weights(w, w, w, {"BTC": 0.4}) == "a"
    assert rc.classify_weights({"BTC": 0.5, "SPY": 0.0}, w, w, None) is None


def test_fill_check_catches_broken_fills(rc: Any, tmp_path: Path) -> None:
    h = history()
    times = [at(START + timedelta(days=i), 22, 30) for i in range(1, DAYS - 2)]
    decs = [gym.Decision(t, trend(visible_history(h, t))[0]) for t in times]
    res = gym.simulate(decs, h)
    assert res.fills and rc.check_fills("trend", res, decs, h) == []

    f = res.fills[0]
    bad_price = dataclasses.replace(res, fills=[dataclasses.replace(f, price=f.price * 1.001)])
    assert any("price" in x.what for x in rc.check_fills("t", bad_price, decs, h))
    off_open = dataclasses.replace(
        res, fills=[dataclasses.replace(f, time=f.time + timedelta(hours=1))]
    )
    assert any("not the open" in x.what for x in rc.check_fills("t", off_open, decs, h))
    early = rc.check_fills("t", res, [gym.Decision(f.time + timedelta(hours=1), {})], h)
    assert any("no decision" in x.what for x in early)
    bad_fee = dataclasses.replace(
        res, fills=[dataclasses.replace(f, fee=f.fee * 2 + 1)] + res.fills[1:]
    )
    assert any("fee" in x.what for x in rc.check_fills("t", bad_fee, decs, h))
    bad_cash = dataclasses.replace(res, cash=res.cash + 1)
    assert [x.day for x in rc.check_fills("t", bad_cash, decs, h)] == ["end"]


def test_snapshot_tolerance_and_classes(rc: Any) -> None:
    row = {
        "cash": 10.0,
        "equity": 100.0,
        "positions": {"BTC": 0.5},
        "fills": 2,
        "marked_on": "2026-11-10",
    }
    assert rc.snapshot_gaps(row, {**row, "equity": 100.004}) == []
    assert rc.snapshot_gaps(row, {**row, "equity": 100.006}) != []
    assert rc.snapshot_gaps(row, {**row, "positions": {"BTC": 0.5 + 1e-6}}) != []
    assert rc.snapshot_gaps(row, {**row, "fills": 3}) != []
    other = {**row, "cash": 12.0}
    assert rc.classify_snapshot(row, row, row) == (None, [])
    assert rc.classify_snapshot(row, row, other)[0] == "d"
    assert rc.classify_snapshot(row, other, row)[0] == "c"


def test_late_bars(rc: Any) -> None:
    h = history()
    run_at = at(START + timedelta(days=5), 3)  # Saturday: bars of Mon-Fri have closed (5 each)
    assert rc.late_bars(h, [(run_at, {"BTC": 5, "SPY": 5})]) == []
    late = rc.late_bars(h, [(run_at, {"BTC": 4, "SPY": 5})])
    assert late == [(run_at.isoformat(), "BTC", (START + timedelta(days=4)).isoformat())]


def test_due_day(rc: Any) -> None:
    d = date(2026, 11, 23)
    assert rc.due_day(at(d, 22, 0)) == d
    assert rc.due_day(at(d + timedelta(days=1), 6, 13)) == d
    assert rc.due_day(at(d + timedelta(days=1), 13)) == d + timedelta(days=1)
