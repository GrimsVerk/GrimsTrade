"""eu-2 data: EUR-hedged UCITS lines from Yahoo's public chart API. Stdlib only.

    uv run python -I research/lib/eu2_data.py fetch   # raw JSON into <cache root>/eu-2/raw-<date>/
    uv run python -I research/lib/eu2_data.py build   # research/data/{bars,adj}/<SYM>.csv
    uv run python -I research/lib/eu2_data.py check   # sanity table (no strategy numbers)

Same parsing as `eu1_data.py` (json.loads only, never executed); cache root from the git-ignored
`research/macro.local.json`. Nothing downloaded is committed.
"""

from __future__ import annotations

import json
import math
import sys
import time
from datetime import UTC, date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # our own lib folder (isolated mode)

import eu1_data as e1  # noqa: E402

# Our symbol -> Yahoo ticker. Candidates; `check` shows which are usable (research/eu-2.md).
HEDGED = {
    "IBCF": "IBCF.DE",  # iShares S&P 500 EUR Hedged (Acc), Xetra
    "IUSE": "IUSE.AS",  # same fund, Euronext Amsterdam
    "IUSEL": "IUSE.L",  # same fund, London (EUR line)
    "NQSE": "NQSE.DE",  # iShares Nasdaq 100 EUR Hedged (Acc), Xetra
    "XAD1": "XAD1.DE",  # Xtrackers Physical Gold EUR Hedged ETC, Xetra
}
TRAIN_LAST_BAR = date(2025, 11, 10)


def fetch() -> None:
    now = datetime.now(UTC)
    out = e1.cache_root() / "eu-2" / f"raw-{now:%Y-%m-%d}" / "yahoo"
    out.mkdir(parents=True, exist_ok=True)
    p2 = int(now.timestamp()) + 86400
    for ticker in HEDGED.values():
        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            f"?period1={e1.YAHOO_FROM}&period2={p2}&interval=1d&events=history"
        )
        try:
            (out / f"{ticker}.json").write_bytes(e1.get(url))
            print("ok", ticker, flush=True)
        except Exception as e:  # noqa: BLE001 - a missing ticker is reported, not fatal
            print("FAILED", ticker, type(e).__name__, e, flush=True)
        time.sleep(0.5)
    (out.parent / "fetched.txt").write_text(now.strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")


def newest_raw() -> Path:
    folders = sorted((e1.cache_root() / "eu-2").glob("raw-*"))
    if not folders:
        raise FileNotFoundError("run `fetch` first")
    return folders[-1]


def build() -> None:
    raw = newest_raw()
    print("raw folder", raw.name)
    for sym, ticker in HEDGED.items():
        path = raw / "yahoo" / f"{ticker}.json"
        if not path.exists():
            print("missing", sym)
            continue
        try:
            cur, rows, adj = e1.parse_yahoo(json.loads(path.read_bytes()))
        except (KeyError, IndexError, TypeError) as e:
            print("unparsable", sym, type(e).__name__)
            continue
        if cur != "EUR" or not rows:
            print("skip", sym, cur, len(rows))
            continue
        e1.write_rows(e1.DATA / "bars" / f"{sym}.csv", rows)
        e1.write_rows(e1.DATA / "adj" / f"{sym}.csv", adj)
        print(sym, cur, len(rows), rows[0][0], flush=True)


def _weekly(rows: list[e1.Row]) -> dict[tuple[int, int], float]:
    out = {}
    for d, *_, cl, _v in rows:
        if d <= TRAIN_LAST_BAR:
            out[tuple(d.isocalendar())[:2]] = cl
    return out  # type: ignore[return-value]


def check() -> None:
    """Coverage, gaps, largest move, and per-year return against the S&P 500 in USD (SPY) and
    in EUR unhedged (SXR8): the hedge's carry. Up to the train cut; no strategy numbers."""
    spy = e1.read_rows(e1.DATA / "adj" / "SPY.csv")
    sxr8 = e1.read_rows(e1.DATA / "adj" / "SXR8.csv")
    print("| Sym | First | Bars | Gaps >5d | Zero-vol bars | Biggest day | Weekly corr SPY (USD) |")
    print("|---|---|---:|---:|---:|---|---:|")
    for sym in HEDGED:
        p = e1.DATA / "adj" / f"{sym}.csv"
        if not p.exists():
            continue
        rows = [r for r in e1.read_rows(p) if r[0] <= TRAIN_LAST_BAR]
        gaps = sum(1 for a, b in zip(rows, rows[1:]) if (b[0] - a[0]).days > 5)  # noqa: B905
        zero = sum(1 for r in rows if r[5] == 0)
        moves = [(b[4] / a[4] - 1, b[0]) for a, b in zip(rows, rows[1:])]  # noqa: B905
        big = max(moves, key=lambda m: abs(m[0]))
        wa, wb = _weekly(rows), _weekly(spy)
        ks = sorted(set(wa) & set(wb))
        ra = [math.log(wa[k2] / wa[k1]) for k1, k2 in zip(ks, ks[1:])]  # noqa: B905
        rb = [math.log(wb[k2] / wb[k1]) for k1, k2 in zip(ks, ks[1:])]  # noqa: B905
        corr = _corr(ra, rb)
        print(
            f"| {sym} | {rows[0][0]} | {len(rows)} | {gaps} | {zero} | {big[0]:+.1%} on {big[1]} | "
            f"{corr:.2f} |"
        )
    print()
    print("Calendar-year total return: hedged line, SPY in USD, SXR8 (unhedged, EUR)")
    print("| Year | IBCF | SPY (USD) | SXR8 (EUR) | IBCF - SPY | IBCF - SXR8 |")
    print("|---|---:|---:|---:|---:|---:|")
    ibcf = e1.read_rows(e1.DATA / "adj" / "IBCF.csv")
    for y in range(2011, 2026):
        a, b, s = _year(ibcf, y), _year(spy, y), _year(sxr8, y)
        print(f"| {y} | {a:+.1%} | {b:+.1%} | {s:+.1%} | {a - b:+.1%} | {a - s:+.1%} |")


def _year(rows: list[e1.Row], y: int) -> float:
    """Total return from the last close of y-1 to the last close of y (2025: to the train cut)."""
    before = [r for r in rows if r[0].year < y]
    inside = [r for r in rows if r[0].year == y and r[0] <= TRAIN_LAST_BAR]
    if not before or not inside:
        return math.nan
    return inside[-1][4] / before[-1][4] - 1


def _corr(a: list[float], b: list[float]) -> float:
    n = len(a)
    if n < 3:
        return math.nan
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))  # noqa: B905
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    return cov / math.sqrt(va * vb)


if __name__ == "__main__":
    {"fetch": fetch, "build": build, "check": check}[sys.argv[1]]()
