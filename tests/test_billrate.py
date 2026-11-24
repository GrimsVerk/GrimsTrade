"""The second source for the cash rate: the US Treasury's daily bill rates, used for sessions
Yahoo `^IRX` lacks (DECISIONS, 2026-11-24, second bill-rate source). Offline tests."""

import json
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path

import pytest

from grimstrade import data, rates, run_daily, sources

FIX = Path(__file__).parent / "fixtures"
TREASURY_CSV = (FIX / "treasury_bill_rates.csv").read_bytes()  # 2026-11-02 .. 2026-11-13, real
MON = date(2026, 11, 2)


def at(d: date, hh: int = 22, mm: int = 30) -> datetime:
    return datetime.combine(d, time(hh, mm), tzinfo=UTC)


def market(
    yahoo_ok: bool = True,
    treasury_ok: bool = True,
    yahoo_skips: frozenset[date] = frozenset(),
    asked: list[str] | None = None,
) -> sources.Get:
    """Kraken for crypto; Yahoo `^IRX` at 3.5% on every weekday but `yahoo_skips` (if up); the
    Treasury fixture (if up); everything else down. Records the URLs asked in `asked`."""

    def get(url: str) -> bytes:
        if asked is not None:
            asked.append(url)
        days = [date(2026, 10, 1) + timedelta(days=i) for i in range(60)]
        if "kraken" in url:
            ts = [int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp()) for d in days]
            rows = [[t, "100", "100", "100", "100", "0", "10", 1] for t in ts]
            return json.dumps({"error": [], "result": {"PAIR": rows, "last": ts[-1]}}).encode()
        if yahoo_ok and "yahoo" in url and "%5EIRX" in url:
            sessions = [d for d in days if d.weekday() < 5 and d not in yahoo_skips]
            ts = [int(at(d, 14, 30).timestamp()) for d in sessions]
            q = {k: [3.5] * len(ts) for k in ("open", "high", "low", "close")}
            res = {"timestamp": ts, "indicators": {"quote": [q | {"volume": [0] * len(ts)}]}}
            return json.dumps({"chart": {"result": [res], "error": None}}).encode()
        if treasury_ok and url.startswith("https://home.treasury.gov/") and "/2026/" in url:
            return TREASURY_CSV
        raise OSError("blocked")

    return get


# --- parsing the Treasury's CSV ---


def test_the_13_week_bank_discount_column_is_read_by_name() -> None:
    days = rates.parse_treasury(TREASURY_CSV)
    assert days[MON] == 4.03  # 13 WEEKS BANK DISCOUNT, not the 4.13 coupon equivalent beside it
    assert days[date(2026, 11, 13)] == 4.13
    assert date(2026, 11, 11) not in days  # Veterans Day: the bond market is closed
    assert len(days) == 9
    # Older years have other maturities (no 6-week bill before 2025); a blank cell is no rate.
    older = (
        b'Date,"4 WEEKS BANK DISCOUNT","4 WEEKS COUPON EQUIVALENT","13 WEEKS BANK DISCOUNT",'
        b'"13 WEEKS COUPON EQUIVALENT"\n01/03/2024,5.28,5.39,5.22,5.38\n01/02/2024,5.28,5.39,,'
    )
    assert rates.parse_treasury(older) == {date(2024, 1, 3): 5.22}


def test_a_csv_without_the_column_is_an_error() -> None:
    with pytest.raises(ValueError, match="13 WEEKS BANK DISCOUNT"):
        rates.parse_treasury(b"Date,1 Mo,3 Mo\n11/02/2026,4.1,4.2\n")
    with pytest.raises(ValueError):
        rates.parse_treasury(b"<html>maintenance</html>")


# --- which source gives which day ---


def test_yahoo_is_primary_and_the_treasury_is_not_asked_when_yahoo_has_every_session() -> None:
    asked: list[str] = []
    found, failed, answered = rates.fetch(MON, at(MON + timedelta(days=4)), market(asked=asked))
    assert answered and not failed
    assert {src for src, _ in found} == {rates.YAHOO} and len(found) == 5
    assert not any("treasury" in u for u in asked)


def test_the_treasury_fills_a_session_yahoo_lacks_and_yahoo_wins_where_both_have_one() -> None:
    gap = MON + timedelta(days=2)
    get = market(yahoo_skips=frozenset({gap}))
    found, failed, answered = rates.fetch(MON, at(MON + timedelta(days=4)), get)
    assert answered and not failed
    by_day = {r.date: (src, r.rate) for src, r in found}
    assert by_day[gap] == (rates.TREASURY, 4.03)
    assert all(v == (rates.YAHOO, 3.5) for d, v in by_day.items() if d != gap)


def test_yahoo_down_means_every_day_from_the_treasury_and_only_settled_sessions() -> None:
    fri = date(2026, 11, 13)
    now = at(fri, 21, 10)  # Friday's session closed 10 minutes ago: not settled yet
    found, failed, answered = rates.fetch(MON, now, market(yahoo_ok=False))
    assert answered and len(failed) == 1 and failed[0].startswith("yahoo ^IRX")
    assert {src for src, _ in found} == {rates.TREASURY}
    assert [r.date for _, r in found][-1] == fri - timedelta(days=1)
    assert all(r.seen == now for _, r in found)


def test_both_down_is_no_answer() -> None:
    found, failed, answered = rates.fetch(
        MON, at(MON + timedelta(days=4)), market(yahoo_ok=False, treasury_ok=False)
    )
    assert not found and not answered and len(failed) == 2


# --- the daily run ---


def sources_lines(root: Path) -> list[dict[str, object]]:
    lines = (root / data.SOURCES_LOG).read_text().splitlines()
    return [e for e in map(json.loads, lines) if e["symbol"] == rates.SYMBOL]


def test_the_daily_run_falls_back_to_the_treasury_and_logs_each_rows_source(
    tmp_path: Path,
) -> None:
    tue = date(2026, 11, 10)
    problems = run_daily.run(tmp_path, at(tue), market(yahoo_ok=False), tmp_path)
    assert all("rate" not in p for p in problems)  # a fallback that answered is no problem
    stored = rates.load(tmp_path)
    assert stored[0].date == MON and stored[-1].date == tue and stored[0].rate == 4.03
    assert sources_lines(tmp_path) == [
        {"first": "2026-11-02", "last": "2026-11-10", "rows": 7, "seen": "2026-11-10T22:30:00Z",
         "source": "treasury", "symbol": "rates"}
    ]  # fmt: skip
    # Yahoo back: its rows are appended after the Treasury's, which stay as stored.
    before = (tmp_path / rates.RATES).read_text()
    run_daily.run(tmp_path, at(tue + timedelta(days=2)), market(), tmp_path)
    text = (tmp_path / rates.RATES).read_text()
    assert text.startswith(before)
    assert [r.date for r in rates.load(tmp_path)][-2:] == [tue + timedelta(days=1),
                                                           tue + timedelta(days=2)]  # fmt: skip
    last = sources_lines(tmp_path)[-1]
    assert (last["source"], last["first"], last["rows"]) == ("yahoo", "2026-11-11", 2)


def test_both_sources_down_is_a_problem_and_the_last_rate_carries_forward(
    tmp_path: Path,
) -> None:
    tue = date(2026, 11, 10)
    run_daily.run(tmp_path, at(tue), market(), tmp_path)
    before = (tmp_path / rates.RATES).read_text()
    log_before = (tmp_path / data.SOURCES_LOG).read_text()
    down = market(yahoo_ok=False, treasury_ok=False)
    problems = run_daily.run(tmp_path, at(tue + timedelta(days=1)), down, tmp_path)
    [p] = [p for p in problems if p.startswith("rates not fetched")]
    assert "yahoo ^IRX" in p and "treasury" in p
    assert (tmp_path / rates.RATES).read_text() == before
    assert sources_lines(tmp_path) == [
        e for e in map(json.loads, log_before.splitlines()) if e["symbol"] == rates.SYMBOL
    ]
