import json
from datetime import UTC, datetime
from pathlib import Path

from grimstrade.intraday import BAR_FIELDS, append_new, collect, kraken_funding, yahoo_1h

NOW = datetime(2026, 11, 12, 15, 0, tzinfo=UTC)
H = 3600
T0 = int(datetime(2026, 11, 12, 12, 0, tzinfo=UTC).timestamp())


def yahoo_body(n: int) -> bytes:
    ts = [T0 + i * H for i in range(n)]
    q = {k: [1.0] * n for k in ("open", "high", "low", "close", "volume")}
    q["close"][1] = None  # type: ignore[call-overload]
    return json.dumps(
        {"chart": {"result": [{"timestamp": ts, "indicators": {"quote": [q]}}]}}
    ).encode()


def funding_body() -> bytes:
    rates = [
        {"timestamp": "2026-11-12T13:00:00.000Z", "fundingRate": 1.5, "relativeFundingRate": 2e-5},
        {"timestamp": "2026-11-12T14:50:00.000Z", "fundingRate": 9.0, "relativeFundingRate": 1e-4},
    ]
    return json.dumps({"rates": rates}).encode()


def test_yahoo_skips_empty_hours_and_stamps_available_at() -> None:
    rows = yahoo_1h("SPY", lambda url: yahoo_body(3))
    assert [r["open_time"] for r in rows] == ["2026-11-12T12:00:00Z", "2026-11-12T14:00:00Z"]
    assert rows[0]["available_at"] == "2026-11-12T13:15:00Z"


def test_append_new_stores_only_available_rows_and_never_rewrites(tmp_path: Path) -> None:
    path = tmp_path / "SPY.csv"
    rows = yahoo_1h("SPY", lambda url: yahoo_body(3))
    # the 14:00 bar is available at 15:15, after NOW: not stored yet
    assert append_new(path, BAR_FIELDS, rows, "open_time", NOW) == 1
    before = path.read_text()
    later = datetime(2026, 11, 12, 16, 0, tzinfo=UTC)
    changed = [dict(r, close="99.0") for r in rows]  # a source changing a stored bar
    assert append_new(path, BAR_FIELDS, changed, "open_time", later) == 1
    text = path.read_text()
    assert text.startswith(before)  # the stored line is untouched
    assert text.count("\n") == 3


def test_kraken_funding_known_at_settlement_plus_15_min() -> None:
    rows = kraken_funding("PF_XBTUSD", lambda url: funding_body())
    assert rows[0]["time"] == "2026-11-12T13:00:00Z"
    assert rows[0]["available_at"] == "2026-11-12T13:15:00Z"


def test_collect_isolates_failures(tmp_path: Path) -> None:
    def get(url: str) -> bytes:
        if "kraken" in url:
            return funding_body()
        raise OSError("offline")

    report = collect(tmp_path, NOW, get)
    assert report["funding/PF_XBTUSD"] == "+1"  # 14:50 settles 15:05, after NOW
    assert report["etf-1h/SPY"].startswith("error")
    assert report["crypto-1h/BTC-USD"].startswith("error")
    assert (tmp_path / "funding" / "PF_ETHUSD.csv").exists()


def test_a_changed_stored_row_is_logged_once_and_kept_as_stored(tmp_path: Path) -> None:
    path, log = tmp_path / "SPY.csv", tmp_path / "revisions.jsonl"
    later = datetime(2026, 11, 12, 16, 0, tzinfo=UTC)
    rows = yahoo_1h("SPY", lambda url: yahoo_body(3))
    assert append_new(path, BAR_FIELDS, rows, "open_time", later, log, "etf-1h/SPY") == 2
    stored = path.read_text()
    assert not log.exists()  # same values again: nothing to log

    changed = [dict(r, close="99.0") if r["open_time"].endswith("12:00:00Z") else r for r in rows]
    for _ in range(2):  # the same difference seen twice is logged once
        assert append_new(path, BAR_FIELDS, changed, "open_time", later, log, "etf-1h/SPY") == 0
    assert path.read_text() == stored
    [line] = log.read_text().splitlines()
    entry = json.loads(line)
    assert entry["series"] == "etf-1h/SPY" and entry["key"] == "2026-11-12T12:00:00Z"
    assert entry["stored"] == {"close": "1.0"} and entry["source_now"] == {"close": "99.0"}
    assert entry["seen_at"] == "2026-11-12T16:00:00Z"


def test_collect_rechecks_the_last_coinbase_day(tmp_path: Path) -> None:
    urls: list[str] = []

    def get(url: str) -> bytes:
        urls.append(url)
        if "coinbase" in url:
            return json.dumps([[T0, 1.0, 2.0, 1.5, 1.5, 1.0]]).encode()
        raise OSError("offline")

    collect(tmp_path, NOW, get)
    urls.clear()
    collect(tmp_path, NOW, get)
    first = next(u for u in urls if "BTC-USD" in u)
    assert "start=2026-11-11T13:00:00Z" in first  # last stored 12:00, +1 h, -24 h


def test_open_interest_pages_forward_past_empty_windows() -> None:
    from urllib.parse import parse_qs, urlparse

    from grimstrade.intraday import OI_START, kraken_open_interest

    first = int(OI_START.timestamp()) + 3000 * H  # the series starts 3,000 hours in
    last = first + 2500 * H
    calls: list[int] = []

    def get(url: str) -> bytes:
        since = int(parse_qs(urlparse(url).query)["since"][0])
        calls.append(since)
        end = since + 2000 * H  # one page: 2,000 hours from `since`
        ts = [t for t in range(first, last + 1, H) if since <= t < end]
        data = [[str(t), str(t + 1), str(t - 1), str(t)] for t in ts]
        return json.dumps({"result": {"timestamp": ts, "data": data, "more": end <= last}}).encode()

    rows = kraken_open_interest("PF_XBTUSD", OI_START, NOW, get)
    assert len(rows) == 2501 and len(calls) == 3
    assert calls[1] == calls[0] + 2000 * H  # an empty page moves on by a full page
    assert rows[0]["time"] == "2022-05-06T00:00:00Z"
    assert rows[0]["oi_close"] == repr(float(first))
    assert rows[0]["available_at"] == "2022-05-06T01:15:00Z"
