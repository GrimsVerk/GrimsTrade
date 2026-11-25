"""Keyless public data sources for daily bars. Each symbol tries its sources in order.

Formats are from the providers' public docs; live fetching is proven on GitHub Actions
(the dev container can't reach these hosts). Tests use small fixture files.
"""

from __future__ import annotations

import csv
import http.client
import io
import json
import math
import sys
import time
import urllib.request
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from typing import Any

from grimstrade.data import CRYPTO, DAY, UNIVERSE, Bar, Dividend, settled

Get = Callable[[str], bytes]

USER_AGENT = "grimstrade/0.1 (paper trading research)"
# `urlopen`'s timeout limits each socket operation, not a request: a server that sends a few
# bytes every so often would hold a request open for ever. The daily runner's requests
# (`runner_get`) get this long (seconds) for the body; its answers are small and normally take a
# second or two. Scripts with large downloads call `http_get` without a cap.
REQUEST_CAP = 90.0
SOCKET_TIMEOUT = 30.0


def http_get(
    url: str, cap: float | None = None, clock: Callable[[], float] = time.monotonic
) -> bytes:
    """The whole body at `url`. Raises `http.client.IncompleteRead` for a body that ends
    before its Content-Length (a connection dropped mid-answer: a CSV cut inside its newest row
    could otherwise pass as data and be stored for good); a chunked body cut short raises too.
    With a `cap` (seconds), also raises TimeoutError once the request has taken longer than
    that: the time is checked after each `read1`, which returns as soon as some bytes arrive
    (`read(n)` would wait for all n of them), so a body trickled byte by byte stops at the cap,
    plus at most one socket timeout if the server then goes silent. Not covered: a server
    trickling the status line or headers; `urlopen` reads those before this can check, under
    the per-operation socket timeout only."""
    deadline = None if cap is None else clock() + cap
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=SOCKET_TIMEOUT) as resp:
        chunks = []
        while chunk := resp.read1(1 << 16):
            chunks.append(chunk)
            if deadline is not None and clock() > deadline:
                raise TimeoutError(f"no whole answer within {cap:g} s")
        body = b"".join(chunks)
        # `read1` ends on the closed connection without a word; `read()` used to raise here.
        # Bytes still owed: > 0 after an early end, 0 after a whole one, None if chunked.
        if missing := getattr(resp, "length", None):
            raise http.client.IncompleteRead(body, missing)
        return body


def runner_get(url: str) -> bytes:
    """`http_get` with the daily runner's per-request cap, REQUEST_CAP."""
    return http_get(url, cap=REQUEST_CAP)


class Budget:
    """`get` with an overall time cap for one run: once `seconds` have passed since it was made,
    every further call raises TimeoutError without asking anyone. The run then goes on with what
    it has (the failed fetches are problem lines; the next run catches up), instead of being
    killed by the job's own timeout halfway through. A call already under way is limited by
    `http_get`'s own cap (`runner_get`)."""

    def __init__(self, get: Get, seconds: float, clock: Callable[[], float] = time.monotonic):
        self.get, self.seconds, self.clock = get, seconds, clock
        self.deadline = clock() + seconds

    def __call__(self, url: str) -> bytes:
        if self.clock() >= self.deadline:
            raise TimeoutError(f"the run's fetch time cap of {self.seconds:g} s is used up")
        return self.get(url)


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


def yahoo_dividends(ticker: str, since: date, get: Get) -> list[Dividend]:
    """Distributions from Yahoo's chart API (`events=div`): per unit, keyed by the ex-date (the
    event's time is that day's open). Split-adjusted like Yahoo's prices."""
    period2 = int(datetime.now(UTC).timestamp()) + 86400
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?period1={_ts(since)}&period2={period2}&interval=1d&events=div"
    )
    payload: dict[str, Any] = json.loads(get(url))
    chart = payload["chart"]
    if chart.get("error"):
        raise ValueError(f"yahoo error: {chart['error']}")
    events: dict[str, Any] = (chart["result"][0].get("events") or {}).get("dividends") or {}
    out = []
    for e in events.values():
        amount = float(e["amount"])
        if not (math.isfinite(amount) and amount > 0):
            raise ValueError(f"yahoo: dividend amount {e['amount']!r} is not a positive number")
        if (d := _day(e["date"])) >= since:
            out.append(Dividend(d, amount))
    return sorted(out, key=lambda d: d.ex_date)


# symbol -> Yahoo ticker, for the symbols that pay distributions (the ETFs).
DIVIDEND_TICKERS: dict[str, str] = {"SPY": "SPY", "QQQ": "QQQ", "GLD": "GLD", "TLT": "TLT"}


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
    """Raise ValueError on a bar no market can print, and on an answer that lists one day twice
    with different numbers (it contradicts itself: which one is right is unknown, and the store
    would keep whichever came last). Stored rows are never rewritten, so a nonsense bar (zero
    price, columns mixed up) must be stopped before it gets in. The same bar listed twice is
    harmless and passes (it is stored once)."""
    seen: dict[date, Bar] = {}
    for b in bars:
        if seen.setdefault(b.date, b) != b:
            raise ValueError(f"two different bars for {b.date} in one answer")
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


def skipped_day(symbol: str, since: date, bars: list[Bar], continues: bool) -> str | None:
    """Why a crypto answer leaves out a day, or None: it starts after `since` (when `continues`:
    `since` is the day after the newest stored bar) or skips a day inside. Crypto trades every
    day, and the store only appends newer bars, so such an answer could store nothing past the
    missing day (`data.append` refuses it). ETFs have holidays: no check."""
    if UNIVERSE[symbol] != CRYPTO or not bars:
        return None
    days = sorted({b.date for b in bars})
    if continues and days[0] != since:
        return f"the answer starts at {days[0]}, not at {since}"
    for a, b in zip(days, days[1:], strict=False):
        if b - a != DAY:
            return f"the answer skips from {a} to {b}"
    return None


def fetch_from(
    symbol: str, since: date, now: datetime, get: Get = http_get, *, continues: bool = True
) -> tuple[str, list[Bar]]:
    """Settled, sane bars from `since` on, and the name of the source that gave them: the first
    one that has any. A source that answers with nothing new is not trusted on that alone: the
    next one is asked too (an empty or cut-short answer looks exactly like "no news"). A crypto
    answer that leaves out a day (`skipped_day`; `continues`: `since` is the day after the newest
    stored bar) is not taken either while another source may have the day; if none has, the
    first such answer is returned (the store keeps what comes before the missing day and the run
    says why the rest was refused). Raises if every source fails."""
    errors = []
    nothing_new_from = None
    gapped: tuple[str, list[Bar]] | None = None
    for source, ticker in SOURCES[symbol]:
        try:
            bars = settled(source(ticker, since, get), UNIVERSE[symbol], now)
            check_sane(bars)
        except Exception as e:  # noqa: BLE001 - any failure means: try the next source
            errors.append(f"{source.__name__}: {e}")
            print(f"{symbol}: {source.__name__} failed: {e}", file=sys.stderr)
            continue
        if skip := skipped_day(symbol, since, bars, continues):
            print(f"{symbol}: {source.__name__} set aside: {skip}", file=sys.stderr)
            gapped = gapped or (source.__name__, bars)
            continue
        if bars:
            return source.__name__, bars
        nothing_new_from = nothing_new_from or source.__name__
    if gapped is not None:
        return gapped
    if nothing_new_from is not None:
        return nothing_new_from, []
    raise RuntimeError(f"{symbol}: all sources failed: {'; '.join(errors)}")


def fetch(symbol: str, since: date, now: datetime, get: Get = http_get) -> list[Bar]:
    return fetch_from(symbol, since, now, get)[1]
