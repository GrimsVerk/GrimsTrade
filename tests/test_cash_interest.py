"""Idle cash earns the T-bill rate (DECISIONS, 2026-11-18, cash interest). Offline tests."""

import json
import math
import subprocess
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path

import pytest

from grimstrade import data, gym, ledger, rates, report, run_daily, sources
from grimstrade.data import Bar, History
from grimstrade.gym import Decision
from grimstrade.rates import Rate

NO_COSTS = {"crypto": gym.Costs(0, 0), "etf": gym.Costs(0, 0)}
MON = date(2026, 11, 2)  # a Monday


def at(d: date, hh: int = 22, mm: int = 30) -> datetime:
    return datetime.combine(d, time(hh, mm), tzinfo=UTC)


def flat(start: date, n: int, px: float = 100.0, weekdays_only: bool = False) -> list[Bar]:
    days = [start + timedelta(days=i) for i in range(n)]
    return [Bar(d, px, px, px, px, 1.0) for d in days if not weekdays_only or d.weekday() < 5]


def const(rate: float, since: date = date(2000, 1, 3)) -> gym.Rates:
    return [(at(since, 21, 0), rate)]


# --- the rate for a day: known at its start, carried forward, never below zero ---


def test_the_rate_for_a_day_is_the_newest_known_at_its_start() -> None:
    steps = [(at(MON, 21, 0), 0.04), (at(MON + timedelta(days=1), 21, 0), 0.05)]
    assert gym.cash_rate(steps, MON) == 0  # Monday's close is not known at Monday 00:00
    assert gym.cash_rate(steps, MON + timedelta(days=1)) == 0.04
    assert gym.cash_rate(steps, MON + timedelta(days=2)) == 0.05
    assert gym.cash_rate(steps, MON + timedelta(days=30)) == 0.05  # carried forward
    exactly = [(at(MON, 0, 0), 0.04)]
    assert gym.cash_rate(exactly, MON) == 0.04  # known at 00:00 counts for that day
    late = [(at(MON, 0, 0) + timedelta(microseconds=1), 0.04)]
    assert gym.cash_rate(late, MON) == 0  # a microsecond later does not


def test_a_negative_rate_pays_nothing_and_negative_cash_is_charged() -> None:
    assert gym.cash_rate([(at(MON, 0, 0), -0.002)], MON) == 0
    assert gym.interest(1_000.0, 0.0365) == pytest.approx(0.1)
    assert gym.interest(0.0, 0.05) == 0
    assert gym.interest(-1_000.0, 0.0365) == pytest.approx(-0.1)  # charged, never credited


def test_no_rates_means_no_interest_as_before() -> None:
    hist: History = {"BTC": flat(MON, 10)}
    res = gym.simulate([Decision(at(MON), {})], hist, costs=NO_COSTS)
    assert [e for _, e in res.equity] == [gym.START_CASH] * len(res.equity)
    assert res.cash_growth == [0.0] * len(res.equity)


# --- accrual in the gym ---


def test_cash_compounds_daily_and_the_open_last_day_waits() -> None:
    hist: History = {"BTC": flat(MON, 10)}
    res = gym.simulate([Decision(at(MON), {})], hist, costs=NO_COSTS, rates=const(0.0365))
    days = [d for d, _ in res.equity]
    assert days[0] == MON
    for k, (_, e) in enumerate(res.equity[:-1]):
        assert e == pytest.approx(gym.START_CASH * 1.0001 ** (k + 1))
    # The replay's last day may still be open: its interest is credited by the next run.
    assert res.equity[-1][1] == pytest.approx(res.equity[-2][1])


def test_weekends_earn_too() -> None:
    """An ETF-only history has no event at weekends; Friday's equity point carries Friday's
    interest and Monday's carries Saturday's, Sunday's and Monday's."""
    hist: History = {"SPY": flat(MON, 14, weekdays_only=True)}
    res = gym.simulate([Decision(at(MON), {})], hist, costs=NO_COSTS, rates=const(0.0365))
    eq = dict(res.equity)
    fri, next_mon = MON + timedelta(days=4), MON + timedelta(days=7)
    assert eq[next_mon] / eq[fri] == pytest.approx(1.0001**3)
    assert res.cash_growth[list(eq).index(next_mon)] == pytest.approx(1.0001**3 - 1)


def test_a_rate_change_counts_from_the_day_after_its_session_closed() -> None:
    hist: History = {"BTC": flat(MON, 6)}
    rows = [
        Rate(MON - timedelta(days=3), 3.65, at(MON)),
        Rate(MON + timedelta(days=1), 7.3, at(MON)),
    ]
    res = gym.simulate(
        [Decision(at(MON), {})], hist, costs=NO_COSTS, rates=rates.steps(rows, live=False)
    )
    g = dict(zip([d for d, _ in res.equity], res.cash_growth, strict=True))
    assert g[MON + timedelta(days=1)] == pytest.approx(0.0001)  # Tuesday: still Friday's rate
    assert g[MON + timedelta(days=2)] == pytest.approx(0.0002)  # Wednesday: Tuesday's close


def test_a_fully_invested_book_earns_nothing() -> None:
    hist: History = {"BTC": flat(MON, 10)}
    res = gym.simulate([Decision(at(MON), {"BTC": 1.0})], hist, costs=NO_COSTS, rates=const(0.05))
    assert res.cash == pytest.approx(0, abs=1e-9)
    assert res.equity[-1][1] == pytest.approx(gym.START_CASH * (1 + 0.05 / 365))  # day 1 only


def test_interest_is_only_paid_on_the_cash_share() -> None:
    hist: History = {"BTC": flat(MON, 10)}
    decision = [Decision(at(MON), {"BTC": 0.5})]
    res = gym.simulate(decision, hist, costs=NO_COSTS, rates=const(0.0365))
    # Day 1 all cash (fills at the next open), then half the equity in cash, at 1 bp a day.
    cash_after_day1 = gym.START_CASH * 1.0001 / 2
    assert res.cash == pytest.approx(cash_after_day1 * 1.0001 ** (len(res.equity) - 2))


def test_interest_never_changes_a_fill() -> None:
    hist: History = {"BTC": flat(MON, 10), "SPY": flat(MON, 10, weekdays_only=True)}
    decisions = [Decision(at(MON + timedelta(days=i)), {"BTC": 0.3, "SPY": 0.3}) for i in range(5)]
    without = gym.simulate(decisions, hist)
    with_rate = gym.simulate(decisions, hist, rates=const(0.05))
    assert [(f.time, f.symbol) for f in with_rate.fills] == [
        (f.time, f.symbol) for f in without.fills
    ]


# --- scoring: Sharpe above the cash rate ---


def test_a_cash_only_book_shows_no_sharpe_from_interest() -> None:
    hist: History = {"BTC": flat(MON, 60)}
    steps = [(at(MON + timedelta(days=i), 0, 0), 0.04 + 0.001 * (i % 3)) for i in range(60)]
    res = gym.simulate([Decision(at(MON), {})], hist, costs=NO_COSTS, rates=steps)
    s = report.score("cash", res)
    assert s.total_return > 0.005  # it earned about 0.7% in 60 days...
    assert abs(s.sharpe) < 1e-6  # ...which is no skill: Sharpe is measured above the rate
    # Against zero it would have looked like a miracle.
    eq = [res.start_cash] + [e for _, e in res.equity]
    raw = [b / a - 1 for a, b in zip(eq, eq[1:], strict=False)]
    mean = sum(raw) / len(raw)
    sd = math.sqrt(sum((r - mean) ** 2 for r in raw) / len(raw))
    assert mean / sd * math.sqrt(365) > 10


# --- the rate store: append-only, refuses rows no run writes ---


def row(d: date, rate: float = 4.0, seen: datetime | None = None) -> Rate:
    return Rate(d, rate, seen or at(d, 22, 30))


def test_rates_are_appended_never_rewritten(tmp_path: Path) -> None:
    week = [row(MON + timedelta(days=i)) for i in range(5)]
    assert rates.append(tmp_path, week[:3]) == (3, [])
    first = (tmp_path / rates.RATES).read_text()
    assert first.startswith("date,rate,seen\n2026-11-02,4.0,2026-11-02T22:30:00+00:00\n")
    # A later answer that disagrees about a stored day changes nothing stored.
    again = [row(MON, 9.0), *week[1:]]
    assert rates.append(tmp_path, again) == (2, [])
    text = (tmp_path / rates.RATES).read_text()
    assert text.startswith(first) and len(text.splitlines()) == 6
    assert rates.load(tmp_path)[0].rate == 4.0


@pytest.mark.parametrize(
    "bad",
    [
        row(MON + timedelta(days=5)),  # a Saturday
        row(MON + timedelta(days=1), 45.0),  # no T-bill rate
        row(MON + timedelta(days=1), float("nan")),
        row(MON + timedelta(days=1), seen=at(MON + timedelta(days=1), 20, 0)),  # before the close
    ],
)
def test_a_bad_rate_is_refused_and_what_came_before_is_kept(tmp_path: Path, bad: Rate) -> None:
    added, problems = rates.append(tmp_path, [row(MON), bad, row(MON + timedelta(days=7))])
    assert added == 1 and len(problems) == 1
    assert [r.date for r in rates.load(tmp_path)] == [MON]


@pytest.mark.parametrize(
    "line",
    [
        "2026-11-07,4.0,2026-11-07T22:30:00+00:00\n",  # a weekend
        "2026-11-02,4.1,2026-11-03T22:30:00+00:00\n",  # a second row for a stored day
        "2026-11-04,4.0,2026-11-04T12:00:00+00:00\n",  # stored before its session closed
        "2026-11-04,4.0,2026-11-04T22:30:00\n",  # no time zone
        "2026-11-04,4.0,2026-11-20T22:30:00+00:00\n",  # stored in the future
    ],
)
def test_the_daily_run_refuses_a_rate_row_no_run_writes(tmp_path: Path, line: str) -> None:
    now = at(MON + timedelta(days=4))
    rates.append(tmp_path, [row(MON), row(MON + timedelta(days=1))])
    run_daily.check_record(tmp_path, now)  # as written: accepted
    with (tmp_path / rates.RATES).open("a") as f:
        f.write(line)
    with pytest.raises(ledger.LedgerTampered):
        run_daily.check_record(tmp_path, now)


def git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def test_a_rewritten_rate_is_caught(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q")
    rates.append(tmp_path, [row(MON), row(MON + timedelta(days=1))])
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "rates")
    path = tmp_path / rates.RATES
    path.write_text(path.read_text().replace("2026-11-02,4.0,", "2026-11-02,9.0,"))
    git(tmp_path, "commit", "-qam", "rewrite")
    with pytest.raises(ledger.LedgerTampered, match="data/rates.csv"):
        ledger.check_append_only(path)


# --- live record vs backtests: the same gym, different knowledge times ---


def test_the_live_record_counts_a_rate_from_when_it_was_stored() -> None:
    backfilled = [
        row(MON - timedelta(days=7 - i), seen=at(MON + timedelta(days=3))) for i in (0, 1)
    ]
    live = rates.steps(backfilled, live=True)
    hindsight = rates.steps(backfilled, live=False)
    assert [t for t, _ in live] == [at(MON + timedelta(days=3))] * 2
    assert [t for t, _ in hindsight] == [at(MON - timedelta(days=7), 21, 0),
                                         at(MON - timedelta(days=6), 21, 0)]  # fmt: skip
    assert gym.cash_rate(live, MON + timedelta(days=3)) == 0
    assert gym.cash_rate(live, MON + timedelta(days=4)) == 0.04
    assert gym.cash_rate(hindsight, MON) == 0.04


def irx_market(rate: float, ok: bool = True) -> sources.Get:
    """Kraken for crypto, everything on Yahoo down except ^IRX at `rate` (if ok)."""

    def get(url: str) -> bytes:
        days = [date(2026, 10, 1) + timedelta(days=i) for i in range(60)]
        if "kraken" in url:
            ts = [int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp()) for d in days]
            rows = [[t, "100", "100", "100", "100", "0", "10", 1] for t in ts]
            return json.dumps({"error": [], "result": {"PAIR": rows, "last": ts[-1]}}).encode()
        if ok and "yahoo" in url and "%5EIRX" in url:
            sessions = [d for d in days if d.weekday() < 5]
            ts = [int(at(d, 14, 30).timestamp()) for d in sessions]
            q = {k: [rate] * len(ts) for k in ("open", "high", "low", "close")}
            res = {"timestamp": ts, "indicators": {"quote": [q | {"volume": [0] * len(ts)}]}}
            return json.dumps({"chart": {"result": [res], "error": None}}).encode()
        raise OSError("blocked")

    return get


def test_the_daily_run_stores_rates_and_pays_only_from_its_first_run(tmp_path: Path) -> None:
    first = at(date(2026, 11, 10))
    problems = run_daily.run(tmp_path, first, irx_market(3.65), tmp_path)
    assert all("rate" not in p for p in problems)
    stored = rates.load(tmp_path)
    btc = data.load(tmp_path, "BTC")
    assert stored[0].date >= btc[0].date and stored[-1].date == date(2026, 11, 10)
    assert {r.seen for r in stored} == {first}
    for k in range(1, 6):
        run_daily.run(tmp_path, first + timedelta(days=k), irx_market(3.65), tmp_path)
    stored_after = (tmp_path / rates.RATES).read_text()
    assert len(rates.load(tmp_path)) == len(stored) + 3  # Wed, Thu, Fri; appended
    # Every strategy that sat in cash since the first run earned 1 bp a day from the day after.
    res = report.live_results(tmp_path, data.load_all(tmp_path))["ts_momentum"]
    assert not any(res.positions.values())
    days = [d for d, _ in res.equity]
    paid = res.equity[-2][1] / gym.START_CASH - 1  # the last day is still open
    assert paid == pytest.approx(1.0001 ** (len(days) - 2) - 1)
    # A failed fetch is a problem line, stores nothing, and the last rate carries forward.
    later = run_daily.run(tmp_path, first + timedelta(days=6), irx_market(3.65, ok=False), tmp_path)
    assert any(p.startswith("rates not fetched") for p in later)
    assert (tmp_path / rates.RATES).read_text() == stored_after


def test_interest_never_changes_a_decision_or_a_bar(tmp_path: Path) -> None:
    now = at(date(2026, 11, 10))
    with_rates, without = tmp_path / "a", tmp_path / "b"
    run_daily.run(with_rates, now, irx_market(5.0), with_rates)
    run_daily.run(without, now, irx_market(5.0, ok=False), without)
    for rel in (ledger.DECISIONS, Path("data/bars/BTC.csv")):
        assert (with_rates / rel).read_text() == (without / rel).read_text()
