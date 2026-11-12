"""Honesty audit 2026-11: ways the stored bars can be wrong without anyone being told.

Stored rows are never rewritten (by design), so whatever gets in stays in: these tests are about
what gets in. Findings D1-D6 in docs/audits/honesty-2026-11.md.
"""

import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from grimstrade import data, gym, run_daily, sources
from grimstrade.data import Bar, History
from grimstrade.gym import Decision

NO_COSTS = {"crypto": gym.Costs(0, 0), "etf": gym.Costs(0, 0)}
Row = tuple[date, float | None, float | None, float | None, float | None, float | None]


def yahoo_body(rows: list[Row]) -> bytes:
    """A Yahoo chart response: one row per day, stamped at the winter session open (14:30 UTC)."""
    ts = [int(datetime(d.year, d.month, d.day, 14, 30, tzinfo=UTC).timestamp()) for d, *_ in rows]
    cols = list(zip(*[r[1:] for r in rows], strict=True))
    quote = dict(zip(["open", "high", "low", "close", "volume"], map(list, cols), strict=True))
    result = [{"meta": {"symbol": "SPY"}, "timestamp": ts, "indicators": {"quote": [quote]}}]
    return json.dumps({"chart": {"result": result, "error": None}}).encode()


def kraken_body(rows: list[tuple[date, float, float, float, float]]) -> bytes:
    out = [
        [int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp()), str(o), str(h), str(lo),
         str(c), "0", "10", 1]
        for d, o, h, lo, c in rows
    ]  # fmt: skip
    return json.dumps({"error": [], "result": {"XXBTZUSD": out, "last": 0}}).encode()


def only(host: str, body: bytes) -> sources.Get:
    def get(url: str) -> bytes:
        if host in url and ("SPY" in url.upper() or "XBT" in url):
            return body
        raise OSError("blocked")

    return get


def flat(start: str, n: int, px: float) -> list[Bar]:
    d0 = date.fromisoformat(start)
    return [Bar(d0 + timedelta(days=i), px, px, px, px, 1.0) for i in range(n)]


D10, D11, D12 = date(2026, 11, 10), date(2026, 11, 11), date(2026, 11, 12)


def test_a_revised_bar_is_reported(tmp_path: Path) -> None:
    """Audit D1 (fixed): a bar taken soon after the close was frozen for ever, and when the
    source later showed different numbers for that day nobody was told (the day was never even
    asked for again)."""
    # The first real run, 2026-11-11 22:00 UTC, one hour after the close: Yahoo's row for the day
    # was still provisional (its volume, 37,707,134, is the only one of 481 not rounded to 100).
    early = yahoo_body([(D11, 756.8, 762.51, 754.91, 759.81, 37_707_134)])
    first = run_daily.run(tmp_path, datetime(2026, 11, 11, 22, 0, tzinfo=UTC), only("yahoo", early))
    assert data.load(tmp_path, "SPY")[-1].close == 759.81
    assert data.revisions(tmp_path) == [] and not any("SPY" in p for p in first)

    # Next evening the source has the final row for the 11th (another close), plus the 12th.
    final = yahoo_body(
        [(D11, 756.8, 762.51, 754.91, 760.25, 61_254_300), (D12, 761.0, 764.0, 758.0, 763.0, 5e7)]
    )
    evening = datetime(2026, 11, 12, 22, 30, tzinfo=UTC)
    problems = run_daily.run(tmp_path, evening, only("yahoo", final))
    # The stored row is kept (append-only)...
    assert data.load(tmp_path, "SPY")[-2].close == 759.81
    # ...and the difference is now on the record, in the run's problems and on the scoreboard.
    (entry,) = data.revisions(tmp_path)
    assert (entry["symbol"], entry["date"], entry["source"]) == ("SPY", "2026-11-11", "yahoo")
    assert entry["stored"] == {"open": 756.8, "high": 762.51, "low": 754.91, "close": 759.81}
    assert entry["source_now"] == {"open": 756.8, "high": 762.51, "low": 754.91, "close": 760.25}
    assert any(p.startswith("SPY 2026-11-11: yahoo now shows prices 0.06%") for p in problems)
    board = (tmp_path / "reports" / "scoreboard.md").read_text()
    assert "Stored bars whose source later showed other prices: 1 (largest difference 0.06%)" in (
        board
    )
    # Seeing the same revision again logs nothing new; a volume-only change is not a revision.
    volume_only = yahoo_body(
        [(D11, 756.8, 762.51, 754.91, 760.25, 61_999_999), (D12, 761.0, 764.0, 758.0, 763.0, 6e7)]
    )
    later = run_daily.run(tmp_path, evening + timedelta(hours=1), only("yahoo", volume_only))
    assert len(data.revisions(tmp_path)) == 1 and not any("SPY" in p for p in later)


def test_a_split_is_not_stored_as_a_crash(tmp_path: Path) -> None:
    """Audit D2 (guarded): after a split the source's new rows are in post-split prices while
    stored rows and held units are pre-split, so the gym would book a crash that never happened."""
    data.append(tmp_path, "SPY", flat("2026-11-02", 4, 100.0))  # Mon-Thu at 100
    friday = flat("2026-11-06", 1, 100.0)
    after_split = flat("2026-11-09", 2, 50.0)  # 2-for-1 over the weekend: same value, half price
    # What the record would say if those rows got in: the holder "lost" half.
    history: History = {"SPY": [*data.load(tmp_path, "SPY"), *friday, *after_split]}
    decision = Decision(datetime(2026, 11, 2, 22, 30, tzinfo=UTC), {"SPY": 1.0})
    assert gym.simulate([decision], history, costs=NO_COSTS).equity[-1][1] == pytest.approx(5_000)

    # Ingest keeps the good day before the jump and refuses the rest, loudly, every day until
    # a person has looked at it.
    for _ in range(2):
        with pytest.raises(ValueError, match="SPY 2026-11-09: open 50.0 is -50% from"):
            data.append(tmp_path, "SPY", [*friday, *after_split])
        assert [b.date for b in data.load(tmp_path, "SPY")][-1] == date(2026, 11, 6)
    # Ordinary big days are not affected.
    assert data.append(tmp_path, "SPY", flat("2026-11-09", 1, 80.0)) == 1


def test_a_nonsense_bar_is_not_stored() -> None:
    """Audit D3 (fixed): nothing checked a bar before it was stored for ever. A zero open made
    the gym divide by zero on every later run, and the row could not be removed."""
    now = datetime(2026, 11, 12, 22, 30, tzinfo=UTC)
    zero_open = kraken_body([(D10, 100.0, 101.0, 99.0, 100.0), (D11, 0.0, 101.0, 0.0, 100.0)])
    with pytest.raises(RuntimeError, match="kraken: nonsense bar 2026-11-11"):
        sources.fetch("BTC", D10, now, only("kraken", zero_open))
    # The damage it would have done:
    bad = [Bar(D10, 100.0, 101.0, 99.0, 100.0, 1.0), Bar(D11, 0.0, 101.0, 0.0, 100.0, 1.0)]
    decision = Decision(datetime(2026, 11, 10, 22, 30, tzinfo=UTC), {"BTC": 1.0})
    with pytest.raises(ZeroDivisionError):
        gym.simulate([decision], {"BTC": bad})

    # Columns mixed up (low above the open) is caught the same way, and the next source is used.
    def get(url: str) -> bytes:
        if "kraken" in url:
            return kraken_body([(D10, 100.0, 99.0, 101.0, 100.0)])
        ts = int(datetime(2026, 11, 10, tzinfo=UTC).timestamp())
        return json.dumps([[ts, 99.0, 101.0, 100.0, 100.5, 10.0]]).encode()

    assert sources.fetch("BTC", D10, now, get) == [Bar(D10, 100.0, 101.0, 99.0, 100.5, 10.0)]


@pytest.mark.parametrize(
    "bar",
    [
        Bar(D10, -1.0, 1.0, -1.0, 1.0, 1.0),
        Bar(D10, 1.0, 1.0, 1.0, float("nan"), 1.0),
        Bar(D10, 1.0, float("inf"), 1.0, 1.0, 1.0),
        Bar(D10, 100.0, 100.0, 90.0, 110.0, 1.0),  # close above the high
        Bar(D10, 1.0, 1.0, 1.0, 1.0, -5.0),
    ],
)
def test_check_sane_refuses(bar: Bar) -> None:
    with pytest.raises(ValueError, match="nonsense bar"):
        sources.check_sane([bar])


def test_every_real_stored_bar_shape_is_sane() -> None:
    # Float noise as Yahoo delivers it, and a flat bar, must pass.
    sources.check_sane(
        [
            Bar(D10, 605.780029296875, 608.4299926757812, 605.5, 607.4600219726562, 28677700.0),
            Bar(D11, 1.0, 1.0, 1.0, 1.0, 0.0),
        ]
    )


def test_a_hole_in_the_sources_answer_is_not_skipped_silently() -> None:
    """Audit D4 (fixed): a day Yahoo lists without prices, followed by priced days, used to be
    skipped; the later days were stored and the hole could never be filled."""
    hole = [
        (D10, 100.0, 101.0, 99.0, 100.0, 1e6),
        (D11, None, None, None, None, None),
        (D12, 102.0, 103.0, 101.0, 102.0, 1e6),
    ]
    with pytest.raises(ValueError, match="no prices for 2026-11-11"):
        sources.yahoo("SPY", D10, only("yahoo", yahoo_body(hole)))
    # Still fine: the newest day not published yet (it is asked for again tomorrow)...
    bars = sources.yahoo("SPY", D10, only("yahoo", yahoo_body(hole[:2])))
    assert [b.date for b in bars] == [D10]
    # ...an empty row for a day we already hold (before `since`)...
    assert [b.date for b in sources.yahoo("SPY", D12, only("yahoo", yahoo_body(hole)))] == [D12]
    # ...and an empty row plus a priced row for the same day.
    twice = [hole[0], hole[1], (D11, 101.0, 102.0, 100.0, 101.0, 1e6), hole[2]]
    bars = sources.yahoo("SPY", D10, only("yahoo", yahoo_body(twice)))
    assert [b.date for b in bars] == [D10, D11, D12]


def test_the_record_says_which_source_each_bar_came_from(tmp_path: Path) -> None:
    """Audit D5 (fixed): the record did not say which source a bar came from, so a switch
    (Kraken -> Coinbase, Yahoo -> Stooq) in the middle of the history could not be seen later."""

    def coinbase_only(url: str) -> bytes:
        if "coinbase" in url:
            ts = int(datetime(2026, 11, 10, tzinfo=UTC).timestamp())
            return json.dumps([[ts, 99.0, 101.0, 100.0, 100.5, 10.0]]).encode()
        raise OSError("blocked")

    run_daily.run(tmp_path, datetime(2026, 11, 12, 22, 30, tzinfo=UTC), coinbase_only)
    assert data.load(tmp_path, "BTC")  # the bar is in, from the second-choice exchange
    lines = [json.loads(x) for x in (tmp_path / data.SOURCES_LOG).read_text().splitlines()]
    assert lines == [
        {"symbol": s, "source": "coinbase", "first": "2026-11-10", "last": "2026-11-10",
         "rows": 1, "seen": "2026-11-12T22:30:00Z"}
        for s in ("BTC", "ETH")
    ]  # fmt: skip
    # A run that stores nothing new writes no line.
    run_daily.run(tmp_path, datetime(2026, 11, 12, 22, 45, tzinfo=UTC), coinbase_only)
    assert len((tmp_path / data.SOURCES_LOG).read_text().splitlines()) == 2


def test_stooq_browser_check_page_is_an_error_not_data() -> None:
    """Audit D6: on 2026-11-12 stooq.com answered the download URL with HTTP 200 and a JavaScript
    "verify your browser" page. The code rightly treats that as a failed source (this test pins
    it), which means the ETFs currently have one working source, not two."""
    page = (
        b'<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><noscript>This site '
        b"requires JavaScript to verify your browser.</noscript></body></html>"
    )
    with pytest.raises(ValueError, match="unexpected response"):
        sources.stooq("spy.us", D10, lambda url: page)
    with pytest.raises(RuntimeError, match="all sources failed"):
        sources.fetch("SPY", D10, datetime(2026, 11, 12, 22, 30, tzinfo=UTC), lambda url: page)


def test_an_empty_answer_is_not_taken_as_no_news(tmp_path: Path) -> None:
    """Audit D7 (fixed; found by the independent reviewer): a source that answered with an empty
    list counted as success. The second source was never asked, no problem was reported, nothing
    changed, nothing was committed: frozen data behind green runs."""
    now = datetime(2026, 11, 12, 22, 30, tzinfo=UTC)

    def kraken_empty(url: str) -> bytes:
        if "kraken" in url:
            return json.dumps({"error": [], "result": {"XXBTZUSD": [], "last": 0}}).encode()
        if "coinbase" in url:
            ts = int(datetime(2026, 11, 11, tzinfo=UTC).timestamp())
            return json.dumps([[ts, 99.0, 101.0, 100.0, 100.5, 10.0]]).encode()
        raise OSError("blocked")

    # The second source is asked, and it has the day.
    assert sources.fetch_from("BTC", D11, now, kraken_empty) == (
        "coinbase", [Bar(D11, 100.0, 101.0, 99.0, 100.5, 10.0)],
    )  # fmt: skip

    # When every source keeps saying "nothing new", the run says so once a bar is overdue.
    def nothing_new(url: str) -> bytes:
        if "kraken" in url:
            return json.dumps({"error": [], "result": {"XXBTZUSD": [], "last": 0}}).encode()
        if "coinbase" in url:
            return b"[]"
        raise OSError("blocked")

    data.append(tmp_path, "BTC", flat("2026-11-08", 3, 100.0))  # through 2026-11-10
    on_time = run_daily.run(tmp_path, datetime(2026, 11, 11, 22, 30, tzinfo=UTC), nothing_new)
    assert not any(p.startswith("BTC") for p in on_time)  # the 10th closed 22.5 hours ago: fine
    late = run_daily.run(tmp_path, datetime(2026, 11, 14, 22, 30, tzinfo=UTC), nothing_new)
    assert "BTC: no new bar for 3 days (newest stored: 2026-11-10)" in late


def test_a_day_the_source_leaves_out_is_not_skipped(tmp_path: Path) -> None:
    """Audit D8 (fixed for crypto, reported for ETFs; found by the independent reviewer): a day
    simply absent from a source's answer became a silent, permanent hole, because only bars newer
    than the last stored one are ever appended."""
    data.append(tmp_path, "BTC", flat("2026-11-01", 2, 100.0))  # 1st and 2nd
    skipping = [*flat("2026-11-04", 2, 100.0)]  # the answer has the 4th and 5th, not the 3rd
    with pytest.raises(ValueError, match="BTC: the source skips from 2026-11-02 to 2026-11-04"):
        data.append(tmp_path, "BTC", skipping)
    assert [b.date.day for b in data.load(tmp_path, "BTC")] == [1, 2]
    # Once a source has the 3rd, everything goes in.
    assert data.append(tmp_path, "BTC", [*flat("2026-11-03", 1, 100.0), *skipping]) == 3

    # ETFs have holidays, so a skipped day alone proves nothing; the four share one calendar,
    # though, and a session one lacks while the others have it is reported.
    week = flat("2026-11-02", 5, 100.0)  # Monday to Friday
    data.append(tmp_path, "SPY", week)
    data.append(tmp_path, "QQQ", [b for b in week if b.date.day != 4])  # no Wednesday
    assert run_daily._etf_holes(tmp_path) == [
        "QQQ: no bar for 2026-11-04, a session the other ETFs have"
    ]
    # A symbol that is merely behind (its newest day is older) has no hole.
    data.append(tmp_path, "TLT", week[:3])
    assert len(run_daily._etf_holes(tmp_path)) == 1
