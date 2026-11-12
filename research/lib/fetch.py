"""Fetch long daily history into research/data/ (git-ignored). Keyless public sources only.

    uv run python research/lib/fetch.py

Writes `research/data/bars/<SYM>.csv` in the same format as the live store (raw prices), and
`research/data/adj/<SYM>.csv` for the ETFs with dividend-adjusted OHLC (robustness checks only;
the live paper system trades raw prices and does not credit dividends).

Crypto: Coinbase Exchange candles, paged 300 days at a time (the live runner's second source;
Kraken's public API only returns the last 720 days). ETFs: Yahoo chart API.
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

CRYPTO_START = {"BTC": date(2015, 7, 20), "ETH": date(2016, 5, 18)}
ETFS = ["SPY", "QQQ", "GLD", "TLT"]
ETF_START = date(2002, 7, 30)  # TLT's first day; GLD starts 2004-11-18


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


def yahoo_all(ticker: str, start: date, now: datetime) -> tuple[list[Bar], list[Bar]]:
    """(raw bars, dividend-adjusted bars)."""
    p1 = int(datetime(start.year, start.month, start.day, tzinfo=UTC).timestamp())
    p2 = int(now.timestamp()) + 86400
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?period1={p1}&period2={p2}&interval=1d&events=history"
    )
    payload: dict[str, Any] = json.loads(get(url))
    res = payload["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    adj = res["indicators"]["adjclose"][0]["adjclose"]
    raw, adjusted = [], []
    for i, ts in enumerate(res["timestamp"]):
        vals = [q["open"][i], q["high"][i], q["low"][i], q["close"][i], adj[i]]
        if any(v is None for v in vals):
            continue
        d = datetime.fromtimestamp(ts, tz=UTC).date()
        o, h, lo, c, a = (float(v) for v in vals)
        vol = float(q["volume"][i] or 0)
        raw.append(Bar(d, o, h, lo, c, vol))
        k = a / c
        adjusted.append(Bar(d, o * k, h * k, lo * k, a, vol))
    return settled(raw, ETF, now), settled(adjusted, ETF, now)


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


def main() -> None:
    now = datetime.now(UTC)
    for sym, start in CRYPTO_START.items():
        bars = coinbase_all(f"{sym}-USD", start, now)
        write(DATA / "bars" / f"{sym}.csv", bars)
        print(sym, len(bars), bars[0].date, bars[-1].date, "gaps:", gaps(bars, 1))
    for sym in ETFS:
        raw, adjusted = yahoo_all(sym, ETF_START, now)
        write(DATA / "bars" / f"{sym}.csv", raw)
        write(DATA / "adj" / f"{sym}.csv", adjusted)
        print(sym, len(raw), raw[0].date, raw[-1].date, "gaps:", gaps(raw, 5))
    (DATA / "fetched.txt").write_text(now.strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")


if __name__ == "__main__":
    main()
