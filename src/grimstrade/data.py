"""Bars, the universe, bar timing, and the append-only CSV store.

Timing rules (see docs/DESIGN.md): a bar is visible to a decision at time T only if it closed at
or before T; an order decided at T fills at the open of the first bar that opens after T.
"""

from __future__ import annotations

import csv
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path

CRYPTO = "crypto"
ETF = "etf"

# symbol -> asset class. Source tickers live in sources.py.
UNIVERSE: dict[str, str] = {
    "BTC": CRYPTO,
    "ETH": CRYPTO,
    "SPY": ETF,
    "QQQ": ETF,
    "GLD": ETF,
    "TLT": ETF,
}

# ETF session times in UTC, chosen conservatively across daylight saving:
# the real open is 13:30 or 14:30 UTC, the real close 20:00 or 21:00 UTC.
ETF_OPEN_UTC = time(13, 30)
ETF_CLOSE_UTC = time(21, 0)
# Don't store a bar until this long after its close (late prints, provider lag).
SETTLE = timedelta(minutes=15)

FIELDS = ["date", "open", "high", "low", "close", "volume"]


@dataclass(frozen=True)
class Bar:
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float


History = Mapping[str, Sequence[Bar]]


def _at(d: date, t: time) -> datetime:
    return datetime.combine(d, t, tzinfo=UTC)


def open_time(asset_class: str, d: date) -> datetime:
    if asset_class == CRYPTO:
        return _at(d, time(0, 0))
    return _at(d, ETF_OPEN_UTC)


def close_time(asset_class: str, d: date) -> datetime:
    if asset_class == CRYPTO:
        return _at(d + timedelta(days=1), time(0, 0))
    return _at(d, ETF_CLOSE_UTC)


def visible(bars: Sequence[Bar], asset_class: str, at: datetime) -> list[Bar]:
    """Bars closed at or before `at`: all a decision at `at` may see."""
    return [b for b in bars if close_time(asset_class, b.date) <= at]


def visible_history(history: History, at: datetime) -> dict[str, list[Bar]]:
    return {s: visible(bars, UNIVERSE[s], at) for s, bars in history.items()}


def settled(bars: Iterable[Bar], asset_class: str, now: datetime) -> list[Bar]:
    """Bars that are final: closed at least SETTLE ago. In-progress bars are dropped."""
    return [b for b in bars if close_time(asset_class, b.date) + SETTLE <= now]


# --- CSV store: data/bars/<SYMBOL>.csv, one row per day, append-only ---


def bars_path(root: Path, symbol: str) -> Path:
    return root / "data" / "bars" / f"{symbol}.csv"


def load(root: Path, symbol: str) -> list[Bar]:
    path = bars_path(root, symbol)
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return [
            Bar(
                date=date.fromisoformat(r["date"]),
                open=float(r["open"]),
                high=float(r["high"]),
                low=float(r["low"]),
                close=float(r["close"]),
                volume=float(r["volume"]),
            )
            for r in csv.DictReader(f)
        ]


def load_all(root: Path, symbols: Iterable[str] = UNIVERSE) -> dict[str, list[Bar]]:
    return {s: load(root, s) for s in symbols}


def append(root: Path, symbol: str, new_bars: Iterable[Bar]) -> int:
    """Append bars newer than the last stored one. Never touches stored rows. Returns rows added."""
    path = bars_path(root, symbol)
    existing = load(root, symbol)
    last = existing[-1].date if existing else None
    fresh: dict[date, Bar] = {}
    for b in new_bars:
        if last is None or b.date > last:
            fresh[b.date] = b
    rows = [fresh[d] for d in sorted(fresh)]
    if not rows:
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        if write_header:
            w.writerow(FIELDS)
        for b in rows:
            w.writerow([b.date.isoformat(), _num(b.open), _num(b.high), _num(b.low),
                        _num(b.close), _num(b.volume)])  # fmt: skip
    return len(rows)


def _num(x: float) -> str:
    return repr(float(x))
