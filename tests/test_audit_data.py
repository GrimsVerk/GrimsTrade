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


@pytest.mark.xfail(
    strict=True,
    reason="audit D1: a bar taken soon after the close is frozen for ever; when the source later "
    "shows different numbers for that day nobody is told (the day is never even asked for again)",
)
def test_a_revised_bar_is_reported(tmp_path: Path) -> None:
    # The first real run, 2026-11-11 22:00 UTC, one hour after the close: Yahoo's row for the day
    # was still provisional (its volume, 37,707,134, is the only one of 481 not rounded to 100).
    early = yahoo_body([(D11, 756.8, 762.51, 754.91, 759.81, 37_707_134)])
    run_daily.run(tmp_path, datetime(2026, 11, 11, 22, 0, tzinfo=UTC), only("yahoo", early))
    assert data.load(tmp_path, "SPY")[-1].close == 759.81

    # Next evening the source has the final row for the 11th (another close), plus the 12th.
    final = yahoo_body(
        [(D11, 756.8, 762.51, 754.91, 760.25, 61_254_300), (D12, 761.0, 764.0, 758.0, 763.0, 5e7)]
    )
    problems = run_daily.run(
        tmp_path, datetime(2026, 11, 12, 22, 30, tzinfo=UTC), only("yahoo", final)
    )
    # Keeping the stored row is right (append-only). Staying silent about the difference is not.
    assert data.load(tmp_path, "SPY")[-2].close == 759.81
    assert any("SPY" in p and "2026-11-11" in p for p in problems)


@pytest.mark.xfail(
    strict=True,
    reason="audit D2: after a split the source's new rows are in post-split prices while stored "
    "rows and held units are pre-split, so the gym books a crash that never happened",
)
def test_a_split_is_not_stored_as_a_crash(tmp_path: Path) -> None:
    data.append(tmp_path, "SPY", flat("2026-11-02", 5, 100.0))  # Mon-Fri at 100
    after_split = flat("2026-11-09", 2, 50.0)  # 2-for-1 over the weekend: same value, half price
    history: History = {"SPY": [*data.load(tmp_path, "SPY"), *after_split]}
    decision = Decision(datetime(2026, 11, 2, 22, 30, tzinfo=UTC), {"SPY": 1.0})
    res = gym.simulate([decision], history, costs=NO_COSTS)
    assert res.equity[-1][1] == pytest.approx(5_000)  # the holder "lost" half, in the record

    # What should happen: ingest refuses a bar that opens absurdly far from the last close, so a
    # human looks at it before it becomes permanent.
    with pytest.raises(ValueError):
        data.append(tmp_path, "SPY", after_split)


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


@pytest.mark.xfail(
    strict=True,
    reason="audit D5: the record does not say which source a bar came from, so a switch "
    "(Kraken -> Coinbase, Yahoo -> Stooq) in the middle of the history cannot be seen afterwards",
)
def test_the_record_says_which_source_each_bar_came_from(tmp_path: Path) -> None:
    def coinbase_only(url: str) -> bytes:
        if "coinbase" in url:
            ts = int(datetime(2026, 11, 10, tzinfo=UTC).timestamp())
            return json.dumps([[ts, 99.0, 101.0, 100.0, 100.5, 10.0]]).encode()
        raise OSError("blocked")

    run_daily.run(tmp_path, datetime(2026, 11, 12, 22, 30, tzinfo=UTC), coinbase_only)
    assert data.load(tmp_path, "BTC")  # the bar is in, from the second-choice exchange
    written = "".join(p.read_text() for p in tmp_path.rglob("*") if p.is_file())
    assert "coinbase" in written


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
