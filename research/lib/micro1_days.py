"""Daily table from the raw minute bars (card: research/micro-1.md, "Data and as-of rule").

    .venv/bin/python -I research/lib/micro1_days.py <cache root>

Reads `<cache root>/alpaca/1m-sip/<SYM>/<YYYY-MM>.json` and `<cache root>/coinbase/1m/<pair>/
<year>/*.json` (downloaded files: untrusted, so this script runs isolated and uses only the
standard library and numpy) and writes `<cache root>/derived/micro-1/days.csv`, one row per
asset and day, train period only. Nothing here is committed.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

NY = ZoneInfo("America/New_York")
TRAIN_LAST = date(2025, 11, 9)  # harness.TRAIN_LAST_BAR
SESSION = (570, 960)  # 09:30-16:00 in minutes of the local day
FULL_DAY = (0, 1440)
MIN_RETURNS = 30
ETFS = ("SPY", "QQQ", "GLD", "TLT")
COINS = {"BTC": "BTC-USD", "ETH": "ETH-USD"}
EPOCH = date(1970, 1, 1)
FIELDS = ("rv", "bv", "rsp", "rsn", "overnight", "intraday")

Stats = dict[int, tuple[float, float, float, float, float, float]]


def ny_offset(utc_day: int) -> int:
    """Seconds New York is ahead of UTC (negative) at 12:00 UTC on that day (days since 1970)."""
    off = (datetime(1970, 1, 1, 12, tzinfo=UTC) + timedelta(days=utc_day)).astimezone(NY)
    delta = off.utcoffset()
    assert delta is not None
    return int(delta.total_seconds())


def local_seconds(ts: np.ndarray, ny: bool) -> np.ndarray:
    if not ny:
        return ts
    days = ts // 86400
    uniq = np.unique(days)
    off = np.array([ny_offset(int(d)) for d in uniq], dtype=np.int64)
    return ts + off[np.searchsorted(uniq, days)]


def day_stats(
    ts: np.ndarray, o: np.ndarray, c: np.ndarray, ny: bool, window: tuple[int, int]
) -> Stats:
    """{local day (days since 1970): (rv, bv, rs+, rs-, first open, last close)} from minute
    bars sorted by time (`ts` = bar start, epoch seconds). Only bars inside `window` (minutes of
    the local day) count; a day with under MIN_RETURNS five-minute returns is left out."""
    loc = local_seconds(ts, ny)
    m = (loc % 86400) // 60
    inw = (m >= window[0]) & (m < window[1])
    day, m, o, c = (loc // 86400)[inw], m[inw], o[inw], c[inw]
    out: Stats = {}
    if len(day) == 0:
        return out
    key = day * 1000 + (m - window[0]) // 5
    is_last = np.r_[key[1:] != key[:-1], True]
    starts = np.flatnonzero(np.r_[True, day[1:] != day[:-1]])
    ends = np.r_[starts[1:], len(day)]
    for a, b in zip(starts, ends, strict=True):
        closes = c[a:b][is_last[a:b]]
        r = np.diff(np.log(np.r_[o[a], closes]))
        n = len(r)
        if n < MIN_RETURNS or not np.isfinite(r).all():
            continue
        r2 = r * r
        bv = math.pi / 2 * float((np.abs(r[1:]) * np.abs(r[:-1])).sum()) * n / (n - 1)
        out[int(day[a])] = (
            float(r2.sum()), bv, float(r2[r > 0].sum()), float(r2[r < 0].sum()),
            float(o[a]), float(c[b - 1]),
        )  # fmt: skip
    return out


def rows(vol: Stats, sess: Stats) -> list[tuple[date, list[float]]]:
    """Rows (date, FIELDS): rv/bv/rs+/rs- from `vol`, overnight/intraday from `sess` (overnight
    = from the previous day in `sess`'s last close to this day's first open)."""
    out = []
    prev_close = math.nan
    last = {}
    for d in sorted(sess):
        op, cl = sess[d][4], sess[d][5]
        last[d] = (math.log(op / prev_close), math.log(cl / op))
        prev_close = cl
    for d in sorted(set(vol) | set(sess)):
        v = list(vol[d][:4]) if d in vol else [math.nan] * 4
        out.append((EPOCH + timedelta(days=d), v + list(last.get(d, (math.nan, math.nan)))))
    return out


def tidy(ts: list[int], o: list[float], c: list[float]) -> tuple[np.ndarray, ...]:
    t = np.array(ts, dtype=np.int64)
    t, idx = np.unique(t, return_index=True)  # sorted, first of duplicates
    return t, np.array(o, float)[idx], np.array(c, float)[idx]


def load_alpaca(root: Path, sym: str) -> tuple[np.ndarray, ...]:
    ts: list[int] = []
    o: list[float] = []
    c: list[float] = []
    for f in sorted((root / "alpaca" / "1m-sip" / sym).glob("*.json")):
        if f.stem > TRAIN_LAST.strftime("%Y-%m"):
            continue
        pages = json.loads(f.read_text())
        for page in pages if isinstance(pages, list) else [pages]:
            bars = (page.get("bars") or {}).get(sym) or []
            stamps = np.array([b["t"][:19] for b in bars], dtype="datetime64[s]")
            ts.extend(stamps.astype(np.int64).tolist())
            o.extend(float(b["o"]) for b in bars)
            c.extend(float(b["c"]) for b in bars)
    return tidy(ts, o, c)


def load_coinbase(root: Path, pair: str) -> tuple[np.ndarray, ...]:
    ts: list[int] = []
    o: list[float] = []
    c: list[float] = []
    for ydir in sorted((root / "coinbase" / "1m" / pair).iterdir()):
        if not ydir.name.isdigit() or int(ydir.name) > TRAIN_LAST.year:
            continue
        for f in sorted(ydir.glob("*.json")):
            candles = json.loads(f.read_text())  # [time, low, high, open, close, volume]
            if not isinstance(candles, list):
                continue
            for k in candles:
                ts.append(int(k[0]))
                o.append(float(k[3]))
                c.append(float(k[4]))
    return tidy(ts, o, c)


def main(root: Path) -> None:
    out = root / "derived" / "micro-1"
    out.mkdir(parents=True, exist_ok=True)
    tmp = out / "days.csv.tmp"
    with tmp.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["asset", "date", *FIELDS])
        for sym in (*ETFS, *COINS):
            if sym in COINS:
                ts, o, c = load_coinbase(root, COINS[sym])
                table = rows(
                    day_stats(ts, o, c, False, FULL_DAY), day_stats(ts, o, c, True, SESSION)
                )
            else:
                ts, o, c = load_alpaca(root, sym)
                sess = day_stats(ts, o, c, True, SESSION)
                table = rows(sess, sess)
            kept = [(d, v) for d, v in table if d <= TRAIN_LAST]
            for d, v in kept:
                w.writerow([sym, d.isoformat(), *(repr(x) for x in v)])
            print(f"{sym}: {len(ts)} minute bars, {len(kept)} days", file=sys.stderr)
    tmp.replace(out / "days.csv")


if __name__ == "__main__":
    main(Path(sys.argv[1]).expanduser())
