"""Daily collection of finer data (docs/data-sources.md section 9, items 1 and 2). The daily job
runs it after the record is pushed (`run_daily --intraday DIR`); DIR is kept in an Actions cache,
never published (docs/DECISIONS.md, 2026-11-13).

Four kinds of append-only CSV series, each row stamped with `available_at` (UTC time it could
first have been known); a row is stored only once `available_at <= now`:
- crypto 1-hour bars from Coinbase (`BTC-USD`, `ETH-USD`): available at open + 1 h + 15 min;
- ETF 1-hour bars from Yahoo (SPY, QQQ, GLD, TLT): available at open + 1 h + 15 min (the last
  bar of a session is shorter; using a full hour is the conservative side);
- Kraken Futures funding rates (`PF_XBTUSD`, `PF_ETHUSD`): the timestamp is the settlement, so
  available at timestamp + 15 min. Live/estimated rates are never stored.
- Kraken Futures open interest (same perpetuals): open/high/low/close of each hour as served,
  available at the hour's start + 1 h + 15 min. Back to `OI_START` on the first run.

Files: `<dir>/<kind>/<symbol>.csv`. A run appends only rows newer than the last stored one and
never rewrites a line. Each series fails on its own: one broken source never stops the others.

Revisions: every fetch overlaps what is stored (Yahoo's 30 days, Kraken's 12 months, the last
`RECHECK` of Coinbase hours). When the source now shows other values for a stored row, the row
stays as stored and a line goes to `<dir>/revisions.jsonl` (series, key, stored and new values,
`seen_at`); the same difference is logged once.
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
OI_FIELDS = ["time", "oi_open", "oi_high", "oi_low", "oi_close", "available_at"]
OI_START = datetime(2022, 1, 1, tzinfo=UTC)  # before the PF_ perpetuals' first served hour
OI_PAGE = 2000 * HOUR  # the analytics API serves at most this much from `since` per call
RECHECK = timedelta(hours=24)  # stored Coinbase hours fetched again to look for revisions
REVISIONS = "revisions.jsonl"


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


def stored_rows(path: Path, key: str) -> dict[str, Row]:
    if not path.exists():
        return {}
    with path.open(newline="") as f:
        return {row[key]: row for row in csv.DictReader(f)}


def kraken_open_interest(symbol: str, since: datetime, now: datetime, get: Get) -> list[Row]:
    """Hourly open interest from `since`, paging forward. Each call returns up to 2,000 hours
    starting at `since` and `more` while later data exists; an empty page (before the series
    starts) moves on by a full page."""
    out: dict[str, Row] = {}
    start = since
    while start < now:
        url = (
            f"https://futures.kraken.com/api/charts/v1/analytics/{symbol}/open-interest"
            f"?since={int(start.timestamp())}&interval=3600"
        )
        res = json.loads(get(url))["result"]
        stamps = res["timestamp"]
        for ts, vals in zip(stamps, res["data"], strict=True):
            t = datetime.fromtimestamp(ts, UTC)
            o, h, lo, c = (repr(float(v)) for v in vals)
            out[iso(t)] = {"time": iso(t), "oi_open": o, "oi_high": h, "oi_low": lo,
                           "oi_close": c, "available_at": iso(t + HOUR + SETTLE)}  # fmt: skip
        if not res.get("more"):
            break
        start = datetime.fromtimestamp(stamps[-1], UTC) + HOUR if stamps else start + OI_PAGE
    return [out[k] for k in sorted(out)]


def last_key(path: Path, key: str) -> str | None:
    return max(stored_rows(path, key), default=None)


def log_revisions(
    log: Path, series: str, stored: dict[str, Row], rows: Iterable[Row], key: str, now: datetime
) -> int:
    """Append a line per stored row the source now shows differently; each difference once."""
    seen = set()
    if log.exists():
        for line in log.read_text().splitlines():
            e = json.loads(line)
            seen.add((e["series"], e["key"], json.dumps(e["source_now"], sort_keys=True)))
    new = []
    for r in sorted(rows, key=lambda r: r[key]):
        old = stored.get(r[key])
        if old is None:
            continue
        diff = {f: r[f] for f in r if f not in (key, "available_at") and r[f] != old.get(f)}
        mark = (series, r[key], json.dumps(diff, sort_keys=True))
        if diff and mark not in seen:
            seen.add(mark)
            entry = {"series": series, "key": r[key], "stored": {f: old.get(f) for f in diff},
                     "source_now": diff, "seen_at": iso(now)}  # fmt: skip
            new.append(json.dumps(entry, sort_keys=True))
    if new:
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("a") as f:
            f.write("".join(line + "\n" for line in new))
    return len(new)


def append_new(
    path: Path,
    fields: list[str],
    rows: Iterable[Row],
    key: str,
    now: datetime,
    revisions: Path | None = None,
    series: str = "",
) -> int:
    """Append rows newer than the last stored one and already available. Never rewrites. With
    `revisions`, log stored rows the source now shows differently (see `log_revisions`)."""
    rows = list(rows)
    stored = stored_rows(path, key)
    last = max(stored, default=None)
    if revisions is not None:
        log_revisions(revisions, series or path.stem, stored, rows, key, now)
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
    since = parse(last) + HOUR - RECHECK if last else now - timedelta(days=30)
    return coinbase_1h(product, since, now, get)


def _open_interest(symbol: str, path: Path, now: datetime, get: Get) -> list[Row]:
    last = last_key(path, "time")
    since = parse(last) + HOUR - RECHECK if last else OI_START
    return kraken_open_interest(symbol, since, now, get)


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
        oi_path = base / "open-interest" / f"{s}.csv"
        fetch_oi: Callable[[], list[Row]] = partial(_open_interest, s, oi_path, now, get)
        jobs.append((f"open-interest/{s}", OI_FIELDS, "time", fetch_oi))
    report: dict[str, str] = {}
    for name, fields, key, fetch in jobs:
        try:
            path = base / f"{name}.csv"
            report[name] = f"+{append_new(path, fields, fetch(), key, now, base / REVISIONS, name)}"
        except Exception as e:  # noqa: BLE001 - one source failing must not stop the rest
            report[name] = f"error: {e!r}"
    return report
