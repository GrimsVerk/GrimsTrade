from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from grimstrade import data, sources
from grimstrade.data import CRYPTO, ETF, Bar

FIX = Path(__file__).parent / "fixtures"
# Monday 2026-11-10, after the US close: crypto bar 11-10 is still in progress.
NOW = datetime(2026, 11, 10, 22, 30, tzinfo=UTC)


def fixture_get(name: str) -> sources.Get:
    def get(url: str) -> bytes:
        return (FIX / name).read_bytes()

    return get


def failing_get(url: str) -> bytes:
    raise OSError("blocked")


def bar(d: str, px: float) -> Bar:
    return Bar(date.fromisoformat(d), px, px, px, px, 1.0)


def test_kraken_drops_in_progress_bar() -> None:
    bars = sources.fetch("BTC", date(2026, 11, 1), NOW, fixture_get("kraken_ohlc.json"))
    assert [b.date for b in bars] == [date(2026, 11, 8), date(2026, 11, 9)]
    assert bars[0] == Bar(date(2026, 11, 8), 100000.0, 101000.0, 99000.0, 100500.0, 1234.5)


def test_coinbase_columns_and_order() -> None:
    bars = sources.coinbase("BTC-USD", date(2026, 11, 1), fixture_get("coinbase_candles.json"))
    assert [b.date for b in bars] == [date(2026, 11, 8), date(2026, 11, 9), date(2026, 11, 10)]
    assert bars[0] == Bar(date(2026, 11, 8), 100000.0, 101000.0, 99000.0, 100500.0, 1234.5)


def test_yahoo_skips_null_bar_and_keeps_closed_ones() -> None:
    bars = sources.fetch("SPY", date(2026, 11, 1), NOW, fixture_get("yahoo_chart.json"))
    assert [b.date for b in bars] == [date(2026, 11, 6), date(2026, 11, 9)]
    assert bars[1].open == 602.0 and bars[1].close == 604.0


def test_falls_back_to_stooq_when_yahoo_fails() -> None:
    def get(url: str) -> bytes:
        if "yahoo" in url:
            raise OSError("429")
        return (FIX / "stooq.csv").read_bytes()

    bars = sources.fetch("SPY", date(2026, 11, 1), NOW, get)
    assert [b.close for b in bars] == [603.0, 604.0]


def test_all_sources_failing_raises() -> None:
    with pytest.raises(RuntimeError, match="all sources failed"):
        sources.fetch("ETH", date(2026, 11, 1), NOW, failing_get)


def test_etf_bar_only_settles_after_close() -> None:
    today = [bar("2026-11-10", 1.0)]
    assert data.settled(today, ETF, datetime(2026, 11, 10, 20, 0, tzinfo=UTC)) == []
    assert data.settled(today, ETF, NOW) == today
    assert data.settled(today, CRYPTO, NOW) == []


def test_append_is_idempotent_and_never_rewrites(tmp_path: Path) -> None:
    assert data.append(tmp_path, "BTC", [bar("2026-11-01", 1), bar("2026-11-02", 2)]) == 2
    before = data.bars_path(tmp_path, "BTC").read_text()
    # Same bars again, plus a revised old bar and a new one: only the new one is added.
    added = data.append(
        tmp_path, "BTC", [bar("2026-11-01", 9), bar("2026-11-02", 2), bar("2026-11-03", 3)]
    )
    assert added == 1
    after = data.bars_path(tmp_path, "BTC").read_text()
    assert after.startswith(before)
    assert [b.close for b in data.load(tmp_path, "BTC")] == [1, 2, 3]


def test_visibility_hides_bars_not_yet_closed() -> None:
    bars = [bar("2026-11-09", 1), bar("2026-11-10", 2)]
    assert [b.close for b in data.visible(bars, CRYPTO, NOW)] == [1]
    assert [b.close for b in data.visible(bars, ETF, NOW)] == [1, 2]
