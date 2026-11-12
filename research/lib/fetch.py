"""Fetch long daily history into research/data/ (git-ignored). Keyless public sources only.

    uv run python research/lib/fetch.py

Writes `research/data/bars/<SYM>.csv` in the same format as the live store (raw prices), and
`research/data/adj/<SYM>.csv` for ETFs with dividend-adjusted OHLC (total return).

Sources:
- ETFs and indexes: Yahoo chart API, from each one's first day (SPY 1993, QQQ 1999, TLT 2002,
  GLD 2004).
- BTC: Bitstamp daily candles 2012-01-01 .. 2015-07-19, then Coinbase Exchange (the live runner's
  second source) from its first day, 2015-07-20. One seam, two venues; prices differ by a few bps.
- ETH and the other coins: Coinbase Exchange from each product's first day; XRP from Bitstamp
  (Coinbase delisted it 2021-2023).

`UNIVERSE_EXTRA` (in harness.py) names every symbol outside the six live assets.
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.request
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from grimstrade.data import CRYPTO, ETF, FIELDS, Bar, settled  # noqa: E402

DATA = ROOT / "research" / "data"
USER_AGENT = "Mozilla/5.0 (daily-bar research script)"

BTC_BITSTAMP_START = date(2012, 1, 1)
BTC_COINBASE_START = date(2015, 7, 20)
# symbol -> (coinbase product, first day to ask for)
COINBASE = {
    "ETH": ("ETH-USD", date(2016, 5, 18)),
    "LTC": ("LTC-USD", date(2016, 8, 17)),
    "BCH": ("BCH-USD", date(2017, 12, 20)),
    "ETC": ("ETC-USD", date(2018, 8, 7)),
    "XLM": ("XLM-USD", date(2019, 3, 13)),
    "DASH": ("DASH-USD", date(2019, 9, 16)),
}
BITSTAMP = {"XRP": ("xrpusd", date(2017, 1, 1))}
# symbol -> yahoo ticker. ETFs get raw + adjusted files; indexes (no dividends) raw only.
YAHOO_ETFS = {
    s: s
    for s in [
        "SPY", "QQQ", "GLD", "TLT",  # the live universe
        "IWM", "EFA", "EEM", "IEF", "LQD", "VNQ", "DBC", "SLV",  # out-of-universe ETFs
        "XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLB", "XLU",  # the 9 original sectors
    ]
}  # fmt: skip
YAHOO_INDEXES = {"GSPC": "%5EGSPC", "N225": "%5EN225", "FTSE": "%5EFTSE", "GDAXI": "%5EGDAXI"}
# 13-week Treasury bill yield in percent (the "close" is the yield): what cash would earn.
YAHOO_RATES = {"IRX": "%5EIRX"}
YAHOO_FROM = -631152000  # 1950-01-01


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body: bytes = resp.read()
                return body
        except Exception as e:  # noqa: BLE001 - retry any transient failure
            if attempt == 4:
                raise
            print(f"  retry after {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    raise AssertionError("unreachable")


def coinbase_all(product: str, start: date, now: datetime) -> list[Bar]:
    bars: dict[date, Bar] = {}
    d = start
    today = now.date()
    while d <= today:
        end = min(d + timedelta(days=299), today)
        url = (
            f"https://api.exchange.coinbase.com/products/{product}/candles"
            f"?granularity=86400&start={d.isoformat()}T00:00:00Z&end={end.isoformat()}T00:00:00Z"
        )
        rows: list[list[float]] = json.loads(get(url))
        for r in rows:  # [time, low, high, open, close, volume]
            day = datetime.fromtimestamp(r[0], tz=UTC).date()
            bars[day] = Bar(day, float(r[3]), float(r[2]), float(r[1]), float(r[4]), float(r[5]))
        d = end + timedelta(days=1)
        time.sleep(0.25)
    return settled([bars[k] for k in sorted(bars)], CRYPTO, now)


def bitstamp_all(pair: str, start: date, end: date, now: datetime) -> list[Bar]:
    bars: dict[date, Bar] = {}
    d = start
    while d <= end:
        ts = int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp())
        url = f"https://www.bitstamp.net/api/v2/ohlc/{pair}/?step=86400&limit=1000&start={ts}"
        rows: list[dict[str, str]] = json.loads(get(url))["data"]["ohlc"]
        if not rows:
            d += timedelta(days=1000)
            continue
        for r in rows:
            day = datetime.fromtimestamp(int(r["timestamp"]), tz=UTC).date()
            if start <= day <= end and float(r["volume"]) > 0:
                bars[day] = Bar(day, float(r["open"]), float(r["high"]), float(r["low"]),
                                float(r["close"]), float(r["volume"]))  # fmt: skip
        last = datetime.fromtimestamp(int(rows[-1]["timestamp"]), tz=UTC).date()
        d = max(last, d) + timedelta(days=1)
        time.sleep(0.25)
    return settled([bars[k] for k in sorted(bars)], CRYPTO, now)


def yahoo_all(ticker: str, now: datetime) -> tuple[list[Bar], list[Bar]]:
    """(raw bars, dividend-adjusted bars)."""
    p2 = int(now.timestamp()) + 86400
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?period1={YAHOO_FROM}&period2={p2}&interval=1d&events=history"
    )
    payload: dict[str, Any] = json.loads(get(url))
    res = payload["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    adj = res["indicators"]["adjclose"][0]["adjclose"]
    offset = int(res["meta"].get("gmtoffset", 0))  # so each bar gets its exchange-local date
    raw, adjusted = [], []
    for i, ts in enumerate(res["timestamp"]):
        vals = [q["open"][i], q["high"][i], q["low"][i], q["close"][i], adj[i]]
        if any(v is None or v <= 0 for v in vals):
            continue
        d = datetime.fromtimestamp(ts + offset, tz=UTC).date()
        o, h, lo, c, a = (float(v) for v in vals)
        vol = float(q["volume"][i] or 0)
        raw.append(Bar(d, o, h, lo, c, vol))
        k = a / c
        adjusted.append(Bar(d, o * k, h * k, lo * k, a, vol))
    return settled(_dedupe(raw), ETF, now), settled(_dedupe(adjusted), ETF, now)


def _dedupe(bars: list[Bar]) -> list[Bar]:
    by_day = {b.date: b for b in bars}
    return [by_day[d] for d in sorted(by_day)]


def write(path: Path, bars: list[Bar]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(FIELDS)
        for b in bars:
            w.writerow([b.date.isoformat(), b.open, b.high, b.low, b.close, b.volume])


def gaps(bars: list[Bar], max_gap: int) -> list[tuple[date, date]]:
    pairs = zip(bars, bars[1:], strict=False)
    return [(a.date, b.date) for a, b in pairs if (b.date - a.date).days > max_gap]


def report(sym: str, bars: list[Bar], max_gap: int) -> None:
    print(sym, len(bars), bars[0].date, bars[-1].date, "gaps:", gaps(bars, max_gap), flush=True)


def fetch_rates(now: datetime) -> None:
    for sym, ticker in YAHOO_RATES.items():
        raw, _ = yahoo_all(ticker, now)
        write(DATA / "bars" / f"{sym}.csv", raw)
        report(sym, raw, 7)


def main() -> None:
    now = datetime.now(UTC)
    early = bitstamp_all("btcusd", BTC_BITSTAMP_START, BTC_COINBASE_START - timedelta(1), now)
    btc = early + coinbase_all("BTC-USD", BTC_COINBASE_START, now)
    write(DATA / "bars" / "BTC.csv", btc)
    report("BTC", btc, 1)
    for sym, (product, start) in COINBASE.items():
        bars = coinbase_all(product, start, now)
        write(DATA / "bars" / f"{sym}.csv", bars)
        report(sym, bars, 1)
    for sym, (pair, start) in BITSTAMP.items():
        bars = bitstamp_all(pair, start, now.date(), now)
        write(DATA / "bars" / f"{sym}.csv", bars)
        report(sym, bars, 1)
    for sym, ticker in YAHOO_ETFS.items():
        raw, adjusted = yahoo_all(ticker, now)
        write(DATA / "bars" / f"{sym}.csv", raw)
        write(DATA / "adj" / f"{sym}.csv", adjusted)
        report(sym, raw, 5)
        time.sleep(0.5)
    for sym, ticker in YAHOO_INDEXES.items():
        raw, _ = yahoo_all(ticker, now)
        write(DATA / "bars" / f"{sym}.csv", raw)
        report(sym, raw, 7)
        time.sleep(0.5)
    fetch_rates(now)
    (DATA / "fetched.txt").write_text(now.strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")


if __name__ == "__main__":
    main()
