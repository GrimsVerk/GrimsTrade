"""The daily run's own reconcile (`grimstrade.reconcile`).

A small synthetic record (BTC every day, SPY on weekdays, a distribution, a cash rate, fee tiers
in play) passes both checks; each planted fault (a wrong fill price, a fill before any decision,
the stored cash off by a cent, a ledger line whose weights are not its strategy's) gives exactly
one problem line. In the runner, a failed check is a problem in the record (so the job exits 1),
not a crash: every book and report is still written.
"""

from __future__ import annotations

import dataclasses
import json
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from typing import Any

import pytest
from test_run_daily import fake_market

from grimstrade import gym, ledger, reconcile, report, run_daily
from grimstrade.data import Bar, Dividend, History, visible_history

START = date(2026, 11, 2)  # a Monday
DAYS = 40


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
    """Depends on the newest BTC close: trades BTC up and down most days."""
    b = h["BTC"]
    if len(b) < 2:
        return {}, "warm-up"
    w = 0.6 if b[-1].close > b[-2].close else 0.3
    return {"BTC": w, "SPY": 0.3}, "test"


def at(d: date, hh: int, mm: int = 0) -> datetime:
    return datetime.combine(d, time(hh, mm), tzinfo=UTC)


TIMES = [at(START + timedelta(days=i), 3) for i in range(2, DAYS - 2)]  # late, like the live runs
DIVIDENDS = {"SPY": [Dividend(START + timedelta(days=17), 0.4)]}  # a Thursday
RATES = [(at(START, 21), 0.04), (at(START + timedelta(days=20), 21), 0.05)]


def book() -> tuple[History, list[gym.Decision], gym.Result, dict[str, Any]]:
    h = history()
    decs = [gym.Decision(t, trend(visible_history(h, t))[0]) for t in TIMES]
    res = gym.simulate(decs, h, dividends=DIVIDENDS, rates=RATES)
    return h, decs, res, run_daily.state_row(res)


def check(res: gym.Result, decs: list[gym.Decision], h: History, row: dict[str, Any]) -> list[str]:
    return reconcile.check_book("trend", row, res, decs, h, DIVIDENDS, RATES)


def test_the_synthetic_book_exercises_the_rules() -> None:
    _, _, res, _ = book()
    fees = {f.fee / (f.qty * f.price) for f in res.fills if f.symbol == "BTC" and f.qty > 0}
    assert len({round(x, 6) for x in fees}) >= 2  # more than one fee tier
    assert any(f.qty < 0 for f in res.fills) and res.income  # sells and a paid distribution
    assert any(g > 0 for g in res.cash_growth)  # cash interest


def test_a_clean_book_passes() -> None:
    h, decs, res, row = book()
    assert check(res, decs, h, row) == []


def test_a_wrong_fill_price_is_one_problem() -> None:
    h, decs, res, row = book()
    fills = list(res.fills)
    fills[3] = dataclasses.replace(fills[3], price=fills[3].price * 1.0001)
    out = check(dataclasses.replace(res, fills=fills), decs, h, row)
    assert len(out) == 1 and "price" in out[0], out


def test_a_fill_before_its_decision_is_one_problem() -> None:
    h, decs, res, row = book()
    first = res.fills[0]
    assert res.fills[1].time > first.time  # alone at its open
    assert decs[0].weights and decs[0].time.date() == first.time.date() < decs[1].time.date()
    # The first decision counts only from that open (on the same day: the interest is the same).
    moved = [gym.Decision(first.time, decs[0].weights), *decs[1:]]
    out = check(res, moved, h, row)
    assert len(out) == 1 and "no decision" in out[0], out


def test_the_stored_cash_off_by_a_cent_is_one_problem() -> None:
    h, decs, res, row = book()
    assert check(res, decs, h, {**row, "cash": res.cash}) == []  # unrounded passes too
    out = check(res, decs, h, {**row, "cash": round(row["cash"] + 0.01, 2)})
    assert len(out) == 1 and "cash" in out[0], out


def test_other_state_gaps() -> None:
    h, decs, res, row = book()
    pos = {s: q * (1 + 1e-6) for s, q in row["positions"].items()}
    assert len(check(res, decs, h, {**row, "positions": pos})) == len(pos)
    assert len(check(res, decs, h, {**row, "fills": row["fills"] + 1})) == 1
    assert len(check(res, decs, h, {**row, "equity": row["equity"] - 0.01})) == 1
    off_open = [dataclasses.replace(f, time=f.time + timedelta(hours=1)) for f in res.fills]
    out = check(dataclasses.replace(res, fills=off_open), decs, h, row)
    assert len(out) == reconcile.MAX_LINES + 1 and out[-1].endswith("more"), out


def write_ledger(root: Path, h: History, tamper: int | None = None) -> list[dict[str, Any]]:
    for i, t in enumerate(TIMES[:5]):
        w, why = trend(visible_history(h, t))
        if i == tamper:
            w = {**w, "BTC": w["BTC"] + 0.01}
        ledger.write_decision(root, t, "trend", w, visible_history(h, t), why)
    return ledger.decisions(root)


def test_ledger_lines_match_their_strategy(tmp_path: Path) -> None:
    h = history()
    assert reconcile.check_lines(write_ledger(tmp_path, h), h, {"trend": trend}) == []


def test_a_ledger_weight_mismatch_is_one_problem(tmp_path: Path) -> None:
    h = history()
    out = reconcile.check_lines(write_ledger(tmp_path, h, tamper=2), h, {"trend": trend})
    assert len(out) == 1 and TIMES[2].strftime("%Y-%m-%dT%H:%M") in out[0], out


def test_a_check_that_raises_is_a_problem_not_a_crash(tmp_path: Path) -> None:
    h = history()
    rows = write_ledger(tmp_path, h)

    def broken(_: History) -> tuple[dict[str, float], str]:
        raise RuntimeError("boom")

    assert len(reconcile.check_lines(rows, h, {"trend": broken})) == len(rows)
    assert len(reconcile.check_lines(rows, h, {})) == len(rows)  # an unknown strategy
    out = reconcile.check_state(tmp_path, {})  # no state file
    assert len(out) == 1 and "could not read" in out[0]


def test_the_runner_records_a_failed_check_and_still_writes_the_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first = datetime(2026, 11, 2, 22, 30, tzinfo=UTC)
    for k in range(3):
        assert run_daily.run(tmp_path, first + timedelta(days=k), fake_market, tmp_path) == []

    real = report.live_results

    def wrong_price(root: Path, h: History) -> dict[str, gym.Result]:
        out = real(root, h)
        r = out["buy_hold_btc"]
        f = dataclasses.replace(r.fills[0], price=r.fills[0].price * 1.01)
        out["buy_hold_btc"] = dataclasses.replace(r, fills=[f, *r.fills[1:]])
        return out

    monkeypatch.setattr(report, "live_results", wrong_price)
    problems = run_daily.run(tmp_path, first + timedelta(days=3), fake_market, tmp_path)
    assert len(problems) == 1 and problems[0].startswith("reconcile buy_hold_btc: fill"), problems
    assert ledger.problem_runs(tmp_path)[-1]["problems"] == problems
    state = json.loads((tmp_path / "state" / "portfolio.json").read_text())
    assert set(state) >= {"buy_hold_btc", "buy_hold_spy"}  # every book still written
    assert (tmp_path / "reports" / "scoreboard.md").exists()
