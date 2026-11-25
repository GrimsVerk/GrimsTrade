"""The daily run when a source misbehaves (lane runner-faults-1, 2026-11-24).

The record is append-only: whatever a bad answer gets in stays in, and a row a crash cut short
stays too. These tests feed the run bad answers (no network: a fake `get`, as in
tests/test_run_daily.py) and check that nothing wrong is stored, nothing stored is rewritten, the
rest of the run still happens, and the failure is said in words (a problem line, exit 1; or a
refusal, exit 2).
"""

import http.client
import inspect
import json
import re
import urllib.request
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest
from test_run_daily import DAY0, fake_market

from grimstrade import data, ledger, rates, run_daily, sources
from grimstrade.strategies import LIVE

FIRST = datetime(2026, 11, 2, 22, 30, tzinfo=UTC)  # a Monday evening, after the US close
DAYS = [DAY0 + timedelta(days=i) for i in range(60)]


def coinbase_body(url: str) -> bytes:
    """Coinbase candles for the days in `fake_market`, same prices as its Kraken answer."""
    rows = [
        [int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp()), 99.0 + i, 101.0 + i,
         100.0 + i, 100.5 + i, 10.0]
        for i, d in enumerate(DAYS)
    ]  # fmt: skip
    return json.dumps(rows[::-1]).encode()


def market(**override: Callable[[str], bytes]) -> sources.Get:
    """`fake_market` plus Coinbase, where a URL containing a key of `override` is answered by
    that function instead."""

    def get(url: str) -> bytes:
        for needle, answer in override.items():
            if needle in url:
                return answer(url)
        if "coinbase" in url:
            return coinbase_body(url)
        return fake_market(url)

    return get


def body(b: bytes) -> Callable[[str], bytes]:
    return lambda url: b


def raise_(e: BaseException) -> Callable[[str], bytes]:
    def get(url: str) -> bytes:
        raise e

    return get


def snapshot(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def kraken_rows(days: list[date], shift: float = 0.0) -> bytes:
    rows = []
    for d in days:
        i = (d - DAY0).days
        t = int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp())
        px = 100 + i + shift
        rows.append([t, str(px), str(px + 1), str(px - 1), str(px + 0.5), "0", "10", 1])
    return json.dumps({"error": [], "result": {"XXBTZUSD": rows, "last": 0}}).encode()


# --- one source down for one symbol ---


def test_one_symbol_timing_out_leaves_the_others_stored_and_says_so(tmp_path: Path) -> None:
    flaky = market(XBTUSD=raise_(TimeoutError("timed out")), **{"BTC-USD": raise_(TimeoutError())})
    problems = run_daily.run(tmp_path, FIRST, flaky, tmp_path)
    assert len(problems) == 1 and problems[0].startswith("BTC: all sources failed: kraken: timed")
    assert data.load(tmp_path, "BTC") == []
    assert all(data.load(tmp_path, s) for s in data.UNIVERSE if s != "BTC")
    # The problem is in the record, every strategy still decided, and the reports were written.
    assert ledger.problem_runs(tmp_path) == [{"time": "2026-11-02T22:30:00Z", "problems": problems}]
    assert {r["strategy"] for r in ledger.decisions(tmp_path)} == set(LIVE)
    assert (tmp_path / "reports" / "scoreboard.md").exists()
    # The next run, the source back, catches up with every day it missed.
    assert run_daily.run(tmp_path, FIRST + timedelta(days=1), market(), tmp_path) == []
    assert data.load(tmp_path, "BTC")[-1].date == date(2026, 11, 2)


def test_main_exits_1_on_a_problem_and_2_on_a_record_it_cannot_believe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    real = run_daily.run
    get = market(XBTUSD=raise_(OSError("503")), **{"BTC-USD": raise_(OSError("503"))})

    def run(root: Path, now: datetime, repo: Path, fetch_cap: float) -> list[str]:
        assert fetch_cap == run_daily.FETCH_CAP
        return real(root, FIRST, get, repo)

    monkeypatch.setattr(run_daily, "run", run)
    with pytest.raises(SystemExit) as exit_:
        run_daily.main(["--root", str(tmp_path), "--repo", str(tmp_path)])
    assert exit_.value.code == 1
    assert "BTC: FAILED BTC: all sources failed" in capsys.readouterr().err
    assert data.load(tmp_path, "ETH")  # what could be stored was stored

    # A record that fails its checks: exit 2, said in words, and nothing written.
    path = data.bars_path(tmp_path, "SPY")
    path.write_text(path.read_text() + "2026-11-07,1.0,1.0,1.0,1.0,1.0\n")  # a Saturday
    before = snapshot(tmp_path)
    with pytest.raises(SystemExit) as exit_:
        run_daily.main(["--root", str(tmp_path), "--repo", str(tmp_path)])
    assert exit_.value.code == 2
    assert "REFUSING TO RUN: SPY: a stored bar on a weekend" in capsys.readouterr().err
    assert snapshot(tmp_path) == before


# --- answers that are not data ---

KRAKEN_JUNK = {
    "empty body": b"",
    "html": b"<html><body>502 Bad Gateway</body></html>",
    "cut-off json": b'{"error":[],"result":{"XXBTZUSD":[[1793577600,"100"',
    "200 with an error": b'{"error":["EService:Unavailable"]}',
    "no pair in result": b'{"error":[],"result":{"last":0}}',
    "null": b"null",
    "a row too short": b'{"error":[],"result":{"XXBTZUSD":[[1793577600,"100"]],"last":0}}',
    "a price that is no number": (
        b'{"error":[],"result":{"XXBTZUSD":[[1793577600,"x","1","1","1","0","1",1]],"last":0}}'
    ),
    "a NaN price": (
        b'{"error":[],"result":{"XXBTZUSD":[[1793577600,"nan","1","1","1","0","1",1]],"last":0}}'
    ),
}
COINBASE_JUNK = {
    "empty body": b"",
    "200 with an error": b'{"message":"NotFound"}',
    "html": b"<html>rate limited</html>",
}
YAHOO_JUNK = {
    "empty body": b"",
    "200 with an error": (
        b'{"chart":{"result":null,"error":{"code":"Not Found","description":"No data found"}}}'
    ),
    "another error shape": b'{"finance":{"result":null,"error":{"code":"Unauthorized"}}}',
    "no result": b'{"chart":{"result":[],"error":null}}',
    "plain text": b"Too Many Requests\r\n",
}
STOOQ_JUNK = {
    "empty body": b"",
    "no data": b"No data",
    "a row too short": b"Date,Open,High,Low,Close,Volume\n2026-11-03,1,2\n",
    "a price that is no number": b"Date,Open,High,Low,Close,Volume\n2026-11-03,1,2,x,1,1\n",
}


@pytest.mark.parametrize("junk", KRAKEN_JUNK.values(), ids=KRAKEN_JUNK)
def test_a_crypto_answer_that_is_not_data_falls_back_to_the_second_source(junk: bytes) -> None:
    since = date(2026, 10, 30)
    got = sources.fetch_from("BTC", since, FIRST, market(kraken=body(junk)))
    assert got[0] == "coinbase" and [b.date for b in got[1]][0] == since


@pytest.mark.parametrize("junk", YAHOO_JUNK.values(), ids=YAHOO_JUNK)
def test_an_etf_answer_that_is_not_data_falls_back_to_the_second_source(junk: bytes) -> None:
    got = sources.fetch_from("SPY", date(2026, 10, 30), FIRST, market(yahoo=body(junk)))
    assert got[0] == "stooq" and got[1][0].date == date(2026, 10, 30)


@pytest.mark.parametrize(
    ("symbol", "first", "second"),
    [("BTC", k, c) for k in KRAKEN_JUNK.values() for c in COINBASE_JUNK.values()][::7]
    + [("SPY", y, s) for y in YAHOO_JUNK.values() for s in STOOQ_JUNK.values()][::3],
)
def test_two_answers_that_are_not_data_store_nothing_and_are_one_problem_line(
    tmp_path: Path, symbol: str, first: bytes, second: bytes
) -> None:
    run_daily.run(tmp_path, FIRST, market(), tmp_path)
    before = data.bars_path(tmp_path, symbol).read_bytes()
    junk = {"kraken": body(first), "coinbase": body(second)}
    if symbol == "SPY":
        junk = {"query1.finance.yahoo.com/v8/finance/chart/SPY?": body(first),
                "stooq": body(second)}  # fmt: skip
    problems = run_daily.run(tmp_path, FIRST + timedelta(days=1), market(**junk), tmp_path)
    mine = [p for p in problems if p.startswith(f"{symbol}: all sources failed")]
    assert len(mine) == 1
    assert data.bars_path(tmp_path, symbol).read_bytes() == before
    assert ledger.problem_runs(tmp_path)[-1]["problems"] == problems


# --- answers that are data, but odd ---


def test_duplicated_and_out_of_order_bars_are_stored_once_in_order(tmp_path: Path) -> None:
    days = DAYS[:10]
    shuffled = [days[3], days[0], days[7], days[1], days[1], *days[2:3], *days[4:7], *days[8:]]
    shuffled += [days[5]]
    run_daily.run(tmp_path, FIRST, market(kraken=body(kraken_rows(shuffled))), tmp_path)
    assert [b.date for b in data.load(tmp_path, "BTC")] == days


def test_a_bar_from_the_future_is_not_stored(tmp_path: Path) -> None:
    """A bar dated after now (a source's clock, a time-zone slip) and the bar still in progress
    are dropped; the run goes on with the closed ones and later stores the rest normally."""
    days = [d for d in DAYS if d <= FIRST.date()]  # through today, whose bar is in progress
    answer = kraken_rows([*days, date(2027, 1, 1), date(2099, 12, 31)])
    assert run_daily.run(tmp_path, FIRST, market(kraken=body(answer)), tmp_path) == []
    assert data.load(tmp_path, "BTC")[-1].date == FIRST.date() - timedelta(days=1)
    assert run_daily.run(tmp_path, FIRST + timedelta(days=1), market(), tmp_path) == []
    assert data.load(tmp_path, "BTC")[-1].date == FIRST.date()


def test_a_source_revising_stored_bars_goes_to_revisions_never_into_the_stored_rows(
    tmp_path: Path,
) -> None:
    run_daily.run(tmp_path, FIRST, market(), tmp_path)
    before = data.bars_path(tmp_path, "BTC").read_bytes()
    # The next day Kraken shows every day 2% higher, the stored ones included.
    revised = body(kraken_rows(DAYS, shift=2.0))
    problems = run_daily.run(tmp_path, FIRST + timedelta(days=1), market(kraken=revised), tmp_path)
    after = data.bars_path(tmp_path, "BTC").read_bytes()
    assert after.startswith(before) and after.count(b"\n") == before.count(b"\n") + 1
    logged = [r for r in data.revisions(tmp_path) if r["symbol"] == "BTC"]
    assert len(logged) == data.REVISION_DAYS  # the days it looks back at, less the one just stored
    assert all(r["source"] == "kraken" for r in logged)
    assert sum("BTC" in p and "kept as stored" in p for p in problems) == len(logged)
    # Asked again, the same revision is not logged twice.
    run_daily.run(tmp_path, FIRST + timedelta(days=1, hours=1), market(kraken=revised), tmp_path)
    assert len([r for r in data.revisions(tmp_path) if r["symbol"] == "BTC"]) == len(logged)


def test_a_kraken_answer_cut_short_at_the_end_is_said_and_caught_up_next_run(
    tmp_path: Path,
) -> None:
    run_daily.run(tmp_path, FIRST, market(), tmp_path)
    stored = data.load(tmp_path, "BTC")[-1].date
    later = FIRST + timedelta(days=5)
    short = body(kraken_rows([stored + timedelta(days=1), stored + timedelta(days=2)]))
    problems = run_daily.run(tmp_path, later, market(kraken=short), tmp_path)
    # What came is stored; that the newest bar is too old is said (no source failed).
    assert data.load(tmp_path, "BTC")[-1].date == stored + timedelta(days=2)
    assert [p for p in problems if p.startswith("BTC")] == [
        "BTC: no new bar for 3 days (newest stored: 2026-11-03)"
    ]
    assert run_daily.run(tmp_path, later + timedelta(hours=1), market(), tmp_path) == []
    got = [b.date for b in data.load(tmp_path, "BTC")]
    assert got[-1] == later.date() - timedelta(days=1)
    assert all(b - a == timedelta(days=1) for a, b in zip(got, got[1:], strict=False))


# --- a write cut short ---

CUT = {
    "a bar row": ("data/bars/SPY.csv", b"2026-11-03,100.0,10", "SPY.csv line"),
    "a bar row, whole fields": ("data/bars/BTC.csv", b"2026-11-02,100.0,101.0", "BTC.csv line"),
    "a cash rate row": ("data/rates.csv", b"2026-11-03,4.0", "rates.csv line"),
    "a dividend row": (
        "data/dividends.csv",
        b"symbol,ex_date,amount\nSPY,2026-10-0",
        "dividends.csv line 2",
    ),  # fmt: skip
    "a decision": (
        "ledger/decisions.jsonl",
        b'{"strategy":"buy_hold_btc","wei',
        "ledger/decisions.jsonl line 13",
    ),  # fmt: skip
    "a try": ("ledger/tries.jsonl", b'{"na', "ledger/tries.jsonl line 13"),
    "a problem line": (
        "ledger/problems.jsonl",
        b'{"problems":["BTC',
        "ledger/problems.jsonl line 1",
    ),
    "a revision": ("data/revisions.jsonl", b'{"symbol":"BTC"', "data/revisions.jsonl line 1"),
    "a header": ("data/bars/QQQ.csv", None, "QQQ.csv: the header is ['date', 'op']"),
}


@pytest.mark.parametrize(("rel", "tail", "said"), CUT.values(), ids=CUT)
def test_a_row_cut_short_is_refused_in_words_before_anything_is_written(
    tmp_path: Path, rel: str, tail: bytes | None, said: str
) -> None:
    """A job killed in mid-write (or a full disk) can leave a last row cut short, and the commit
    step (`if: always()`) commits it. The row then stays for good: removing it is a rewrite. Each
    later run crashed on it with a bare TypeError or JSONDecodeError (for the ledger files after
    storing that day's bars and before any decision), every day. Now the record check refuses it
    by name, before anything is written (exit 2: a person has to look)."""
    assert run_daily.run(tmp_path, FIRST, market(), tmp_path) == []
    path = tmp_path / rel
    if tail is None:
        path.write_bytes(b"date,op")
    elif tail.startswith(b"symbol,") or not path.exists():
        path.write_bytes(tail)
    else:
        path.write_bytes(path.read_bytes() + tail)
    before = snapshot(tmp_path)
    with pytest.raises(ledger.LedgerTampered, match="^" + re.escape(said)):
        run_daily.run(tmp_path, FIRST + timedelta(days=1), market(), tmp_path)
    assert snapshot(tmp_path) == before


def test_a_lost_newline_alone_is_no_cut_row(tmp_path: Path) -> None:
    """A last row that is whole but lost its newline (a hand edit) is completed by the next
    write, as before: refused is only a row with fields missing."""
    assert run_daily.run(tmp_path, FIRST, market(), tmp_path) == []
    for rel in ("data/bars/BTC.csv", "data/rates.csv", "ledger/decisions.jsonl"):
        path = tmp_path / rel
        path.write_bytes(path.read_bytes().rstrip(b"\n"))
    assert run_daily.run(tmp_path, FIRST + timedelta(days=1), market(), tmp_path) == []
    assert len(data.load(tmp_path, "BTC")) == 33


# --- findings of PR #161, fixed by lane runner-faults-2 ---


def test_a_kraken_answer_missing_the_first_day_asked_is_filled_from_coinbase(
    tmp_path: Path,
) -> None:
    """Kraken answers, but from a day later than asked (it lacks 2026-11-02). `fetch_from` took
    any non-empty answer from the first source, and `data.append` then refused the whole answer
    (a crypto day skipped could never be added later). Coinbase, which has the day, was never
    asked, so BTC stored nothing for as long as Kraken lacked the day. Now an answer that does
    not continue the stored series counts as a failed source, and the next one is asked."""
    run_daily.run(tmp_path, FIRST, market(), tmp_path)
    assert data.load(tmp_path, "BTC")[-1].date == date(2026, 11, 1)
    gap = body(kraken_rows([d for d in DAYS if d >= date(2026, 11, 3)]))
    later = FIRST + timedelta(days=3)
    problems = run_daily.run(tmp_path, later, market(kraken=gap), tmp_path)
    assert not any(p.startswith("BTC") for p in problems), problems
    assert data.load(tmp_path, "BTC")[-1].date == date(2026, 11, 4)


def test_an_answer_with_two_different_bars_for_one_day_is_not_stored_silently(
    tmp_path: Path,
) -> None:
    """One answer lists 2026-10-05 twice with different prices. `data.append` kept whichever
    came last and said nothing; the other version was lost. Now such an answer counts as a failed
    source (the next one is asked), like a nonsense bar (docs/DECISIONS.md, 2026-11-25)."""
    days = DAYS[:10]
    rows = json.loads(kraken_rows(days))
    twin = list(rows["result"]["XXBTZUSD"][4])
    twin[1:5] = [str(float(x) * 1.05) for x in twin[1:5]]
    rows["result"]["XXBTZUSD"].append(twin)
    problems = run_daily.run(tmp_path, FIRST, market(kraken=body(json.dumps(rows).encode())),
                             tmp_path)  # fmt: skip
    stored = data.load(tmp_path, "BTC")
    assert stored and stored[4].close == 100.5 + 4  # the first source's other bars or Coinbase's
    assert not any(p.startswith("BTC") for p in problems)


def test_a_kraken_answer_skipping_a_day_inside_is_filled_from_coinbase(tmp_path: Path) -> None:
    run_daily.run(tmp_path, FIRST, market(), tmp_path)
    holed = body(kraken_rows([d for d in DAYS if d != date(2026, 11, 3)]))
    problems = run_daily.run(tmp_path, FIRST + timedelta(days=3), market(kraken=holed), tmp_path)
    # Stored from Coinbase; that Kraken lacks a stored day is still said (the revision check).
    assert [p for p in problems if p.startswith("BTC")] == [
        "BTC 2026-11-03: a bar is stored, but kraken lists no such day"
    ]
    got = [b.date for b in data.load(tmp_path, "BTC")]
    assert got[-1] == date(2026, 11, 4) and date(2026, 11, 3) in got
    assert data.load(tmp_path, "ETH")[-1].date == date(2026, 11, 4)  # same Kraken answer: "PAIR"


def test_when_no_source_has_the_missing_day_what_comes_before_it_is_stored_and_said(
    tmp_path: Path,
) -> None:
    """Both sources lack 2026-11-03: as before the fix, the days before the hole are stored, the
    rest is refused with a problem line (the store can never hold a crypto gap)."""
    run_daily.run(tmp_path, FIRST, market(), tmp_path)
    days = [d for d in DAYS if d != date(2026, 11, 3)]
    stamp = [int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp()) for d in days]
    coin = json.dumps([[t, 1.0, 1.0, 1.0, 1.0, 1.0] for t in stamp]).encode()  # not chosen
    get = market(kraken=body(kraken_rows(days)), coinbase=body(coin))
    problems = run_daily.run(tmp_path, FIRST + timedelta(days=3), get, tmp_path)
    assert data.load(tmp_path, "BTC")[-1].date == date(2026, 11, 2)
    assert data.load(tmp_path, "BTC")[-1].close == 100.5 + (date(2026, 11, 2) - DAY0).days
    assert [p for p in problems if p.startswith("BTC")] == [
        "BTC: the source skips from 2026-11-02 to 2026-11-04; a day left out now could never be "
        "added later. Not stored.",
        "BTC: no new bar for 2 days (newest stored: 2026-11-02)",
    ]


def test_a_contradicting_answer_from_every_source_stores_nothing_and_is_one_problem_line(
    tmp_path: Path,
) -> None:
    run_daily.run(tmp_path, FIRST, market(), tmp_path)
    before = data.bars_path(tmp_path, "BTC").read_bytes()
    day = date(2026, 11, 2)
    rows = json.loads(kraken_rows([day, day], shift=0.0))
    rows["result"]["XXBTZUSD"][1][4] = "200.0"  # the same day, another close
    t = int(datetime(day.year, day.month, day.day, tzinfo=UTC).timestamp())
    coin = json.dumps([[t, 99.0, 101.0, 100.0, 100.5, 10.0], [t, 99.0, 101.0, 100.0, 100.7, 10.0]])
    get = market(kraken=body(json.dumps(rows).encode()), coinbase=body(coin.encode()))
    problems = run_daily.run(tmp_path, FIRST + timedelta(days=1), get, tmp_path)
    assert data.bars_path(tmp_path, "BTC").read_bytes() == before
    assert [p for p in problems if p.startswith("BTC")] == [
        "BTC: all sources failed: kraken: two different bars for 2026-11-02 in one answer; "
        "coinbase: two different bars for 2026-11-02 in one answer",
        "BTC: no new bar for 1 days (newest stored: 2026-11-01)",
    ]


# --- the cash rate: a session Yahoo lacks while the Treasury is down ---


def irx_without(missing: date) -> bytes:
    sessions = [d for d in DAYS if d.weekday() < 5 and d != missing]
    ts = [int(datetime(d.year, d.month, d.day, 14, 30, tzinfo=UTC).timestamp()) for d in sessions]
    quote = {k: [4.0] * len(ts) for k in ("open", "high", "low", "close")}
    result = {"timestamp": ts, "indicators": {"quote": [quote | {"volume": [0] * len(ts)}]}}
    return json.dumps({"chart": {"result": [result], "error": None}}).encode()


def test_a_rate_gap_yahoo_leaves_with_the_treasury_down_is_a_problem_line(tmp_path: Path) -> None:
    """Yahoo `^IRX` lacks a session inside its answer and the Treasury request fails: the rows
    are stored (the gym carries the previous rate over that day), and the gap, which stays for
    good, is said. Before, only stderr had the Treasury failure."""
    run_daily.run(tmp_path, FIRST, market(), tmp_path)
    later = FIRST + timedelta(days=3)  # Thursday evening: Tue, Wed, Thu are new
    get = market(**{"%5EIRX": body(irx_without(date(2026, 11, 4)))})  # Treasury: blocked
    problems = run_daily.run(tmp_path, later, get, tmp_path)
    assert [p for p in problems if p.startswith("rates")] == [
        "rates: no rate stored for 2026-11-04 (a holiday, or a gap that stays: Yahoo lacks it "
        "and treasury: blocked)"
    ]
    stored = [r.date for r in rates.load(tmp_path)]
    assert stored[-2:] == [date(2026, 11, 3), date(2026, 11, 5)]


def test_a_rate_day_both_sources_lack_is_a_holiday_and_no_problem(tmp_path: Path) -> None:
    run_daily.run(tmp_path, FIRST, market(), tmp_path)
    csv = b"Date,13 WEEKS BANK DISCOUNT\n11/05/2026,4.0\n11/03/2026,4.0\n"
    get = market(**{"%5EIRX": body(irx_without(date(2026, 11, 4))), "treasury": body(csv)})
    problems = run_daily.run(tmp_path, FIRST + timedelta(days=3), get, tmp_path)
    assert not any(p.startswith("rates") for p in problems), problems


# --- an overall time cap on fetching ---


class FakeClock:
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t


def test_fetching_stops_at_the_time_cap_and_the_run_still_decides(tmp_path: Path) -> None:
    """Every call takes 100 s of a fake clock; the cap is 450 s. Five calls are made (the fifth
    starts at 400 s), every later one fails at once without being sent, those fetches are problem
    lines, and the rest of the run happens: decisions, reports. The next run catches up."""
    clock, asked = FakeClock(), []

    def slow(url: str) -> bytes:
        asked.append(url)
        clock.t += 100
        return market()(url)

    problems = run_daily.run(tmp_path, FIRST, slow, tmp_path, fetch_cap=450, clock=clock)
    assert len(asked) == 5
    assert any("fetch time cap of 450 s is used up" in p for p in problems)
    assert data.load(tmp_path, "BTC") and data.load(tmp_path, "ETH")
    assert {r["strategy"] for r in ledger.decisions(tmp_path)} == set(LIVE)
    assert (tmp_path / "reports" / "scoreboard.md").exists()
    assert ledger.problem_runs(tmp_path)[-1]["problems"] == problems
    later = FIRST + timedelta(days=1)
    assert run_daily.run(tmp_path, later, market(), tmp_path, clock=clock) == []
    assert all(data.load(tmp_path, s)[-1].date >= FIRST.date() for s in data.UNIVERSE)


def test_no_cap_means_every_call_is_made(tmp_path: Path) -> None:
    clock, asked = FakeClock(), []

    def slow(url: str) -> bytes:
        asked.append(url)
        clock.t += 10_000
        return market()(url)

    assert run_daily.run(tmp_path, FIRST, slow, tmp_path, fetch_cap=None, clock=clock) == []
    assert len(asked) > 10


def test_the_fetch_cap_is_a_command_line_option(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    caps = []

    def run(root: Path, now: datetime, repo: Path, fetch_cap: float) -> list[str]:
        caps.append(fetch_cap)
        return []

    monkeypatch.setattr(run_daily, "run", run)
    run_daily.main(["--root", str(tmp_path), "--fetch-cap", "120"])
    assert caps == [120.0]
    with pytest.raises(SystemExit) as exit_:
        run_daily.main(["--root", str(tmp_path), "--fetch-cap", "0"])
    assert exit_.value.code == 2 and "--fetch-cap must be a positive" in capsys.readouterr().err


class Trickle:
    """A response trickling two bytes every 20 s of a fake clock. Like `http.client`'s, its
    `read1` returns what has arrived; its `read(n)` waits for all n bytes (or the end), so a
    cap checked between `read` calls would only see the time after the whole body came."""

    def __init__(self, clock: FakeClock, reads: int) -> None:
        self.clock, self.left = clock, reads

    def __enter__(self) -> "Trickle":
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def read1(self, n: int) -> bytes:
        self.clock.t += 20
        if self.left == 0:
            return b""
        self.left -= 1
        return b"ab"

    def read(self, n: int) -> bytes:
        out = b""
        while len(out) < n and (chunk := self.read1(n)):
            out += chunk
        return out


@pytest.mark.parametrize(("reads", "ok"), [(3, True), (100_000, False)])
def test_a_trickling_answer_is_cut_off_at_the_request_cap(
    monkeypatch: pytest.MonkeyPatch, reads: int, ok: bool
) -> None:
    """`urlopen`'s timeout is per socket operation: a server sending two bytes every 20 s never
    trips it. `http_get` gives the whole request at most its cap."""
    clock = FakeClock()
    monkeypatch.setattr(urllib.request, "urlopen", lambda req, timeout: Trickle(clock, reads))
    if ok:
        assert sources.http_get("https://example.invalid/", cap=90, clock=clock) == b"ab" * reads
    else:
        with pytest.raises(TimeoutError, match="no whole answer within 90 s"):
            sources.http_get("https://example.invalid/", cap=90, clock=clock)
        assert clock.t <= 90 + 20  # stopped at the cap, not after the whole (long) body
    # Without a cap (scripts with large downloads) the whole body is read, however slow.
    monkeypatch.setattr(urllib.request, "urlopen", lambda req, timeout: Trickle(clock, reads))
    assert sources.http_get("https://example.invalid/", clock=clock) == b"ab" * reads


class Sized:
    """A response with a Content-Length of 100 whose connection closes after `sent` bytes, as
    `http.client` reports it: `read1` gives what came, then b"", and `length` keeps the bytes
    still owed (0 after a whole body)."""

    def __init__(self, sent: int) -> None:
        self.length, self.left = 100, sent

    def __enter__(self) -> "Sized":
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def read1(self, n: int) -> bytes:
        out, self.left = b"x" * min(n, self.left, 30), self.left - min(n, self.left, 30)
        self.length -= len(out)
        return out


@pytest.mark.parametrize("cap", [None, 90.0])
def test_a_body_cut_short_is_an_error_not_a_shorter_answer(
    monkeypatch: pytest.MonkeyPatch, cap: float | None
) -> None:
    """A CSV cut inside its newest row (a close 601.23 read as 601.2, a volume missing) would
    pass every check and be stored for good."""
    monkeypatch.setattr(urllib.request, "urlopen", lambda req, timeout: Sized(50))
    with pytest.raises(http.client.IncompleteRead):
        sources.http_get("https://example.invalid/", cap=cap)
    monkeypatch.setattr(urllib.request, "urlopen", lambda req, timeout: Sized(100))
    assert sources.http_get("https://example.invalid/", cap=cap) == b"x" * 100


def test_the_runner_caps_each_request_by_default() -> None:
    assert inspect.signature(run_daily.run).parameters["get"].default is sources.runner_get
