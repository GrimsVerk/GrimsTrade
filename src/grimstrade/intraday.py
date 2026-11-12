"""Daily collection of finer data (docs/data-sources.md section 9, items 1 and 2). Not yet wired
into `run_daily`.

Three append-only CSV series, each row stamped with `available_at` (UTC time it could first have
been known); a row is stored only once `available_at <= now`:
- crypto 1-hour bars from Coinbase (`BTC-USD`, `ETH-USD`): available at open + 1 h + 15 min;
- ETF 1-hour bars from Yahoo (SPY, QQQ, GLD, TLT): available at open + 1 h + 15 min (the last
  bar of a session is shorter; using a full hour is the conservative side);
- Kraken Futures funding rates (`PF_XBTUSD`, `PF_ETHUSD`): the timestamp is the settlement, so
  available at timestamp + 15 min. Live/estimated rates are never stored.

Files: `<dir>/<kind>/<symbol>.csv`. A run appends only rows newer than the last stored one and
never rewrites a line. Each series fails on its own: one broken source never stops the others.
"""

from __future__ import annotations

import csv
import json
from collections.abc import Callable, Iterable
from datetime import UTC, datetime, timedelta
from functools import partial
from pathlib import Path

Get = Callable[[str], bytes]
Row = dict[str, str]

SETTLE = timedelta(minutes=15)
HOUR = timedelta(hours=1)
BAR_FIELDS = ["open_time", "open", "high", "low", "close", "volume", "available_at"]
FUNDING_FIELDS = ["time", "funding_rate", "relative_funding_rate", "available_at"]
CRYPTO = ["BTC-USD", "ETH-USD"]
ETFS = ["SPY", "QQQ", "GLD", "TLT"]
PERPS = ["PF_XBTUSD", "PF_ETHUSD"]


def iso(t: datetime) -> str:
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(UTC)


def _bar(t: datetime, o: float, h: float, lo: float, c: float, v: float) -> Row:
    vals = [o, h, lo, c, v]
    return {
        "open_time": iso(t),
        **{k: repr(float(x)) for k, x in zip(BAR_FIELDS[1:6], vals, strict=True)},
        "available_at": iso(t + HOUR + SETTLE),
    }


def coinbase_1h(product: str, since: datetime, now: datetime, get: Get) -> list[Row]:
    """Hourly candles opening at or after `since`, up to 300 per call (12.5 days)."""
    out: dict[str, Row] = {}
    start = since
    while start < now:
        end = min(start + 300 * HOUR, now)
        url = (
            f"https://api.exchange.coinbase.com/products/{product}/candles"
            f"?granularity=3600&start={iso(start)}&end={iso(end)}"
        )
        for ts, lo, hi, op, cl, vol in json.loads(get(url)):  # [time, low, high, open, close, v]
            row = _bar(datetime.fromtimestamp(ts, UTC), op, hi, lo, cl, vol)
            out[row["open_time"]] = row
        start = end
    return [out[k] for k in sorted(out)]


def yahoo_1h(ticker: str, get: Get) -> list[Row]:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=30d&interval=1h"
    res = json.loads(get(url))["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    rows = []
    for i, ts in enumerate(res.get("timestamp") or []):
        vals = [q[k][i] for k in ("open", "high", "low", "close", "volume")]
        if any(v is None for v in vals):
            continue  # an empty hour stays missing, never filled
        rows.append(_bar(datetime.fromtimestamp(ts, UTC), *vals))
    return rows


def kraken_funding(symbol: str, get: Get) -> list[Row]:
    url = f"https://futures.kraken.com/derivatives/api/v4/historicalfundingrates?symbol={symbol}"
    rows = []
    for r in json.loads(get(url))["rates"]:
        t = parse(r["timestamp"])
        rows.append(
            {
                "time": iso(t),
                "funding_rate": repr(float(r["fundingRate"])),
                "relative_funding_rate": repr(float(r["relativeFundingRate"])),
                "available_at": iso(t + SETTLE),
            }
        )
    return rows


def last_key(path: Path, key: str) -> str | None:
    if not path.exists():
        return None
    last = None
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            last = row[key]
    return last


def append_new(path: Path, fields: list[str], rows: Iterable[Row], key: str, now: datetime) -> int:
    """Append rows newer than the last stored one and already available. Never rewrites."""
    last = last_key(path, key)
    new = sorted(
        (r for r in rows if (last is None or r[key] > last) and parse(r["available_at"]) <= now),
        key=lambda r: r[key],
    )
    if not new:
        return 0
    fresh = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        if fresh:
            w.writeheader()
        w.writerows(new)
    return len(new)


def _crypto(product: str, path: Path, now: datetime, get: Get) -> list[Row]:
    last = last_key(path, "open_time")
    since = parse(last) + HOUR if last else now - timedelta(days=30)
    return coinbase_1h(product, since, now, get)


def collect(base: Path, now: datetime, get: Get) -> dict[str, str]:
    """Run every series once; returns {series: "+N" or "error: ..."} and never raises."""
    jobs: list[tuple[str, list[str], str, Callable[[], list[Row]]]] = []
    for p in CRYPTO:
        path = base / "crypto-1h" / f"{p}.csv"
        fetch_cb: Callable[[], list[Row]] = partial(_crypto, p, path, now, get)
        jobs.append((f"crypto-1h/{p}", BAR_FIELDS, "open_time", fetch_cb))
    for t in ETFS:
        jobs.append((f"etf-1h/{t}", BAR_FIELDS, "open_time", partial(yahoo_1h, t, get)))
    for s in PERPS:
        jobs.append((f"funding/{s}", FUNDING_FIELDS, "time", partial(kraken_funding, s, get)))
    report: dict[str, str] = {}
    for name, fields, key, fetch in jobs:
        try:
            report[name] = f"+{append_new(base / f'{name}.csv', fields, fetch(), key, now)}"
        except Exception as e:  # noqa: BLE001 - one source failing must not stop the rest
            report[name] = f"error: {e!r}"
    return report
