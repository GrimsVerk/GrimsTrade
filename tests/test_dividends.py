"""Audit G4: ETF distributions are paid into the gym as cash on the ex-date."""

import json
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path

import pytest

from grimstrade import data, gym, ledger, report, run_daily, sources
from grimstrade.data import Bar, Dividend, History
from grimstrade.gym import Decision

FIX = Path(__file__).parent / "fixtures"
NO_COSTS = {"crypto": gym.Costs(0, 0), "etf": gym.Costs(0, 0)}
MON = date(2026, 11, 2)


def weekdays(start: date, n: int, px: float) -> list[Bar]:
    days = [start + timedelta(days=i) for i in range(n)]
    return [Bar(d, px, px, px, px, 1.0) for d in days if d.weekday() < 5]


def fixture_get(url: str) -> bytes:
    if "query1.finance.yahoo.com" in url and "/TLT?" in url and "events=div" in url:
        return (FIX / "yahoo_dividends.json").read_bytes()
    raise OSError("blocked")


def test_yahoo_dividend_events_are_read_by_ex_date() -> None:
    got = sources.yahoo_dividends("TLT", date(2026, 9, 15), fixture_get)
    assert got == [Dividend(date(2026, 10, 1), 0.31), Dividend(date(2026, 11, 2), 0.32)]


def test_a_holder_is_paid_at_the_ex_date_open_and_stays_whole() -> None:
    """The raw price drops by the payout at the ex-date's open; the payout makes up for it."""
    ex = MON + timedelta(days=7)
    bars = [b if b.date < ex else Bar(b.date, 99.0, 99.0, 99.0, 99.0, 1.0)
            for b in weekdays(MON, 14, 100.0)]  # fmt: skip
    decision = Decision(datetime.combine(MON, time(22, 30), tzinfo=UTC), {"SPY": 1.0})
    divs = {"SPY": [Dividend(ex, 1.0)]}
    paid = gym.simulate([decision], {"SPY": bars}, costs=NO_COSTS, dividends=divs)
    unpaid = gym.simulate([decision], {"SPY": bars}, costs=NO_COSTS)
    assert paid.income == [(datetime.combine(ex, data.ETF_OPEN_UTC, tzinfo=UTC), "SPY", 100.0)]
    assert [e for _, e in paid.equity] == pytest.approx([gym.START_CASH] * len(paid.equity))
    assert unpaid.equity[-1][1] == pytest.approx(gym.START_CASH * 0.99)


def test_a_unit_sold_at_the_ex_date_open_is_paid_and_one_bought_there_is_not() -> None:
    ex = MON + timedelta(days=7)
    hist: History = {"SPY": weekdays(MON, 14, 100.0), "QQQ": weekdays(MON, 14, 100.0)}
    divs = {"SPY": [Dividend(ex, 1.0)], "QQQ": [Dividend(ex, 1.0)]}
    before_ex = datetime.combine(ex - timedelta(days=3), time(22, 30), tzinfo=UTC)  # Friday
    decisions = [
        Decision(datetime.combine(MON, time(22, 30), tzinfo=UTC), {"SPY": 1.0}),
        Decision(before_ex, {"QQQ": 1.0}),  # fills at the ex-date's open
    ]
    res = gym.simulate(decisions, hist, costs=NO_COSTS, dividends=divs)
    assert [(s, amount) for _, s, amount in res.income] == [("SPY", 100.0)]


def tlt_with_bars(root: Path) -> list[Bar]:
    bars = weekdays(date(2026, 8, 3), 89, 87.0)  # 2026-08-03 to 2026-10-30
    data.append(root, "TLT", bars)
    return bars


def test_ingest_appends_paid_dividends_once_and_waits_for_later_ones(tmp_path: Path) -> None:
    tlt_with_bars(tmp_path)
    problems = run_daily._dividends(tmp_path, fixture_get)
    # SPY, QQQ, GLD have no bars here and are skipped; TLT's 11-02 is after its newest bar.
    assert problems == []
    path = tmp_path / data.DIVIDENDS
    first = path.read_text()
    assert first == "symbol,ex_date,amount\nTLT,2026-09-01,0.3\nTLT,2026-10-01,0.31\n"
    assert run_daily._dividends(tmp_path, fixture_get) == []
    assert path.read_text() == first  # nothing twice
    data.append(tmp_path, "TLT", weekdays(date(2026, 11, 2), 1, 86.7))
    run_daily._dividends(tmp_path, fixture_get)
    assert path.read_text() == first + "TLT,2026-11-02,0.32\n"  # appended, nothing rewritten


def test_a_failed_or_absurd_dividend_answer_is_a_problem_and_stores_nothing(
    tmp_path: Path,
) -> None:
    tlt_with_bars(tmp_path)

    def down(url: str) -> bytes:
        raise OSError("blocked")

    assert run_daily._dividends(tmp_path, down) == ["TLT: dividends not fetched: blocked"]
    body = json.loads((FIX / "yahoo_dividends.json").read_text())
    body["chart"]["result"][0]["events"]["dividends"]["1790861400"]["amount"] = 31.0  # 36%

    def decimal_slip(url: str) -> bytes:
        return json.dumps(body).encode() if "/TLT?" in url else down(url)

    problems = run_daily._dividends(tmp_path, decimal_slip)
    assert len(problems) == 1 and problems[0].startswith("TLT 2026-10-01: dividend 31.0 is over")
    assert data.load_dividends(tmp_path) == {"TLT": [Dividend(date(2026, 9, 1), 0.3)]}


@pytest.mark.parametrize(
    "row",
    [
        "TLT,2026-09-05,0.3\n",  # a Saturday: no session
        "TLT,2026-09-01,0.3\n",  # paid twice
        "BTC,2026-09-01,0.3\n",  # crypto pays nothing
        "TLT,2026-09-02,-1\n",
    ],
)
def test_the_daily_run_refuses_a_dividend_row_no_run_writes(tmp_path: Path, row: str) -> None:
    tlt_with_bars(tmp_path)
    run_daily._dividends(tmp_path, fixture_get)
    run_daily.check_record(tmp_path, datetime(2026, 11, 1, tzinfo=UTC))  # as written: accepted
    with (tmp_path / data.DIVIDENDS).open("a") as f:
        f.write(row)
    with pytest.raises(ledger.LedgerTampered):
        run_daily.check_record(tmp_path, datetime(2026, 11, 1, tzinfo=UTC))


def test_the_record_credits_stored_dividends(tmp_path: Path) -> None:
    bars = tlt_with_bars(tmp_path)
    run_daily._dividends(tmp_path, fixture_get)
    when = datetime(2026, 8, 3, 22, 30, tzinfo=UTC)
    ledger.write_decision(tmp_path, when, "tlt", {"TLT": 1.0}, {"TLT": bars[:1]}, "t")
    res = report.live_results(tmp_path, data.load_all(tmp_path))["tlt"]
    units = res.positions["TLT"]
    assert [(t.date(), s) for t, s, _ in res.income] == [
        (date(2026, 9, 1), "TLT"),
        (date(2026, 10, 1), "TLT"),
    ]
    assert [x for _, _, x in res.income] == pytest.approx([units * 0.3, units * 0.31])
