"""The daily run when a source misbehaves (lane runner-faults-1, 2026-11-24).

The record is append-only: whatever a bad answer gets in stays in, and a row a crash cut short
stays too. These tests feed the run bad answers (no network: a fake `get`, as in
tests/test_run_daily.py) and check that nothing wrong is stored, nothing stored is rewritten, the
rest of the run still happens, and the failure is said in words (a problem line, exit 1; or a
refusal, exit 2).
"""

import json
import re
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest
from test_run_daily import DAY0, fake_market

from grimstrade import data, ledger, run_daily, sources
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

    def run(root: Path, now: datetime, repo: Path) -> list[str]:
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
