"""Keyless public data sources for daily bars. Each symbol tries its sources in order.

Formats are from the providers' public docs; live fetching is proven on GitHub Actions
(the dev container can't reach these hosts). Tests use small fixture files.
"""

from __future__ import annotations

import csv
import io
import json
import math
import urllib.request
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from typing import Any

from grimstrade.data import UNIVERSE, Bar, settled

Get = Callable[[str], bytes]

USER_AGENT = "grimstrade/0.1 (paper trading research)"


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body: bytes = resp.read()
        return body


def _ts(d: date) -> int:
    return int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp())


def _day(ts: float) -> date:
    return datetime.fromtimestamp(ts, tz=UTC).date()


# --- crypto ---


def kraken(pair: str, since: date, get: Get) -> list[Bar]:
    """Kraken public OHLC, daily. Returns at most the last 720 bars; the last one is in progress."""
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval=1440&since={_ts(since) - 1}"
    payload: dict[str, Any] = json.loads(get(url))
    if payload.get("error"):
        raise ValueError(f"kraken error: {payload['error']}")
    result: dict[str, Any] = payload["result"]
    rows = next(v for k, v in result.items() if k != "last")
    # [time, open, high, low, close, vwap, volume, count]
    return [
        Bar(_day(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[6]))
        for r in rows
        if _day(r[0]) >= since
    ]


def coinbase(product: str, since: date, get: Get) -> list[Bar]:
    """Coinbase Exchange public candles, daily, newest first, at most 300 per call."""
    start = max(since, datetime.now(UTC).date() - timedelta(days=299))
    url = (
        f"https://api.exchange.coinbase.com/products/{product}/candles"
        f"?granularity=86400&start={start.isoformat()}T00:00:00Z"
    )
    rows: list[list[float]] = json.loads(get(url))
    # [time, low, high, open, close, volume]
    bars = [
        Bar(_day(r[0]), float(r[3]), float(r[2]), float(r[1]), float(r[4]), float(r[5]))
        for r in rows
        if _day(r[0]) >= since
    ]
    return sorted(bars, key=lambda b: b.date)


# --- ETFs ---


def yahoo(ticker: str, since: date, get: Get) -> list[Bar]:
    """Yahoo Finance chart API, daily. Raw (split-adjusted, not dividend-adjusted) OHLC."""
    period2 = int(datetime.now(UTC).timestamp()) + 86400
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?period1={_ts(since)}&period2={period2}&interval=1d&events=history"
    )
    payload: dict[str, Any] = json.loads(get(url))
    chart = payload["chart"]
    if chart.get("error"):
        raise ValueError(f"yahoo error: {chart['error']}")
    res = chart["result"][0]
    q = res["indicators"]["quote"][0]
    bars = []
    empty: set[date] = set()  # days Yahoo lists without prices
    for i, ts in enumerate(res.get("timestamp") or []):
        vals = [q["open"][i], q["high"][i], q["low"][i], q["close"][i]]
        d = _day(ts)
        if d < since:
            continue
        if any(v is None for v in vals):
            empty.add(d)
            continue
        o, h, lo, c = (float(v) for v in vals)
        bars.append(Bar(d, o, h, lo, c, float(q["volume"][i] or 0)))
    # An empty newest day is normal (not published yet; it is asked for again tomorrow). An empty
    # day with priced days after it would become a permanent hole, since only newer bars are
    # ever appended: refuse the whole answer instead.
    have = {b.date for b in bars}
    holes = sorted(d for d in empty - have if have and d < max(have))
    if holes:
        raise ValueError(f"yahoo: no prices for {holes[0]} but later days have them")
    return bars


def stooq(ticker: str, since: date, get: Get) -> list[Bar]:
    """Stooq daily CSV: Date,Open,High,Low,Close,Volume."""
    url = f"https://stooq.com/q/d/l/?s={ticker}&i=d&d1={since:%Y%m%d}"
    text = get(url).decode("utf-8-sig")
    if not text.startswith("Date"):
        raise ValueError(f"stooq: unexpected response {text[:80]!r}")
    bars = []
    for r in csv.DictReader(io.StringIO(text)):
        d = date.fromisoformat(r["Date"])
        if d >= since:
            bars.append(
                Bar(
                    d,
                    float(r["Open"]),
                    float(r["High"]),
                    float(r["Low"]),
                    float(r["Close"]),
                    float(r.get("Volume") or 0),
                )  # fmt: skip
            )
    return bars


Source = Callable[[str, date, Get], list[Bar]]

# symbol -> [(source, ticker at that source), ...] in order of preference
SOURCES: dict[str, list[tuple[Source, str]]] = {
    "BTC": [(kraken, "XBTUSD"), (coinbase, "BTC-USD")],
    "ETH": [(kraken, "ETHUSD"), (coinbase, "ETH-USD")],
    "SPY": [(yahoo, "SPY"), (stooq, "spy.us")],
    "QQQ": [(yahoo, "QQQ"), (stooq, "qqq.us")],
    "GLD": [(yahoo, "GLD"), (stooq, "gld.us")],
    "TLT": [(yahoo, "TLT"), (stooq, "tlt.us")],
}


def check_sane(bars: list[Bar]) -> None:
    """Raise ValueError on a bar no market can print. Stored rows are never rewritten, so a
    nonsense bar (zero price, columns mixed up) must be stopped before it gets in."""
    for b in bars:
        prices = (b.open, b.high, b.low, b.close)
        ok = (
            all(math.isfinite(x) and x > 0 for x in prices)
            and math.isfinite(b.volume)
            and b.volume >= 0
            # 0.1% slack: some sources round each column separately.
            and b.low <= min(b.open, b.close) * 1.001
            and b.high >= max(b.open, b.close) * 0.999
        )
        if not ok:
            raise ValueError(f"nonsense bar {b.date}: o={b.open} h={b.high} l={b.low} c={b.close}")


def fetch_from(
    symbol: str, since: date, now: datetime, get: Get = http_get
) -> tuple[str, list[Bar]]:
    """Settled, sane bars from `since` on, and the name of the source that gave them: the first
    one that answers properly. Raises if all fail."""
    errors = []
    for source, ticker in SOURCES[symbol]:
        try:
            bars = settled(source(ticker, since, get), UNIVERSE[symbol], now)
            check_sane(bars)
            return source.__name__, bars
        except Exception as e:  # noqa: BLE001 - any failure means: try the next source
            errors.append(f"{source.__name__}: {e}")
    raise RuntimeError(f"{symbol}: all sources failed: {'; '.join(errors)}")


def fetch(symbol: str, since: date, now: datetime, get: Get = http_get) -> list[Bar]:
    return fetch_from(symbol, since, now, get)[1]
