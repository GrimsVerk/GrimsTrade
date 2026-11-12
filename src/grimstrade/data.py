"""Bars, the universe, bar timing, and the append-only CSV store.

Timing rules (see docs/DESIGN.md): a bar is visible to a decision at time T only if it closed at
or before T; an order decided at T fills at the open of the first bar that opens after T.
"""

from __future__ import annotations

import csv
import json
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

# A bar opening further than this from the previous close is not stored (see `append`). No
# asset in the universe has gapped half as much: the largest in two stored years is 6% (GLD);
# for crypto the open and the previous close are the same instant.
MAX_GAP = 0.4

DAY = timedelta(days=1)

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


def ends_mid_line(path: Path) -> bool:
    """True if `path` has content that does not end with a newline."""
    if not path.exists() or path.stat().st_size == 0:
        return False
    with path.open("rb") as f:
        f.seek(-1, 2)
        return f.read(1) != b"\n"


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
    """Append bars newer than the last stored one. Never touches stored rows. Returns rows added.
    Raises ValueError, after storing the bars before it, at a bar that opens more than MAX_GAP
    away from the previous close."""
    path = bars_path(root, symbol)
    existing = load(root, symbol)
    last = existing[-1].date if existing else None
    fresh: dict[date, Bar] = {}
    for b in new_bars:
        if last is None or b.date > last:
            fresh[b.date] = b
    rows = [fresh[d] for d in sorted(fresh)]
    # A split (sources adjust their whole history backwards; stored rows and held units stay as
    # they were) or bad data would be booked as a real crash or jump, for ever. Keep what comes
    # before it, refuse the rest, and let a person decide.
    jump = None
    prev = existing[-1] if existing else None
    for i, b in enumerate(rows):
        if prev is not None and abs(b.open / prev.close - 1) > MAX_GAP:
            jump = (
                f"{symbol} {b.date}: open {b.open} is {b.open / prev.close - 1:+.0%} from the "
                f"previous close {prev.close} ({prev.date}): split or bad data? Not stored."
            )
        # Crypto trades every day, so a skipped day is the source's mistake, and once a later
        # day is stored the missing one could never be added.
        elif prev is not None and UNIVERSE.get(symbol) == CRYPTO and b.date - prev.date != DAY:
            jump = (
                f"{symbol}: the source skips from {prev.date} to {b.date}; a day left out now "
                "could never be added later. Not stored."
            )
        if jump:
            rows = rows[:i]
            break
        prev = b
    if not rows:
        if jump:
            raise ValueError(jump)
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="") as f:
        if ends_mid_line(path):  # never glue a new row onto a last row that lost its newline
            f.write("\n")
        w = csv.writer(f, lineterminator="\n")
        if write_header:
            w.writerow(FIELDS)
        for b in rows:
            w.writerow([b.date.isoformat(), _num(b.open), _num(b.high), _num(b.low),
                        _num(b.close), _num(b.volume)])  # fmt: skip
    if jump:
        raise ValueError(jump)
    return len(rows)


def _num(x: float) -> str:
    return repr(float(x))


# --- provenance: which source each stored bar came from ---

SOURCES_LOG = Path("data/sources.jsonl")


def log_source(root: Path, symbol: str, source: str, bars: Sequence[Bar], seen: str) -> None:
    """One line per run and symbol that stored bars: the source and the days it supplied. The
    sources are different exchanges and vendors (Kraken/Coinbase, Yahoo/Stooq) with slightly
    different prices; without this a mixed series cannot be recognised afterwards."""
    if not bars:
        return
    entry = {
        "symbol": symbol,
        "source": source,
        "first": bars[0].date.isoformat(),
        "last": bars[-1].date.isoformat(),
        "rows": len(bars),
        "seen": seen,
    }
    path = root / SOURCES_LOG
    path.parent.mkdir(parents=True, exist_ok=True)
    start = "\n" if ends_mid_line(path) else ""
    with path.open("a") as f:
        f.write(start + json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")


# --- revisions: what the source says now about bars we already hold ---

REVISIONS = Path("data/revisions.jsonl")
# Look this many days back for changed bars on each run.
REVISION_DAYS = 5


def _prices(b: Bar) -> dict[str, float]:
    return {"open": b.open, "high": b.high, "low": b.low, "close": b.close}


def log_revisions(
    root: Path, symbol: str, source: str, fetched: Iterable[Bar], seen: str, tolerance: float = 1e-7
) -> list[tuple[date, float]]:
    """Compare freshly fetched bars with the stored ones for the same days. Stored rows are never
    changed; each difference in a price (not volume, which sources revise all the time) is
    appended once to `data/revisions.jsonl`. Returns (day, largest relative difference) for the
    newly logged ones. `tolerance` absorbs float noise (Yahoo serves 32-bit floats)."""
    stored = {b.date: b for b in load(root, symbol)}
    path = root / REVISIONS
    logged = set()
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                logged.add((r["symbol"], r["date"], json.dumps(r["source_now"], sort_keys=True)))
    new = []
    for b in fetched:
        old = stored.get(b.date)
        if old is None:
            continue
        pairs = zip(_prices(old).values(), _prices(b).values(), strict=True)
        diff = max(abs(now / was - 1) for was, now in pairs)
        key = (symbol, b.date.isoformat(), json.dumps(_prices(b), sort_keys=True))
        if diff <= tolerance or key in logged:
            continue
        entry = {
            "symbol": symbol,
            "date": b.date.isoformat(),
            "seen": seen,
            "source": source,
            "stored": _prices(old),
            "source_now": _prices(b),
            "largest_diff": diff,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        start = "\n" if ends_mid_line(path) else ""
        with path.open("a") as f:
            f.write(start + json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")
        new.append((b.date, diff))
    return new


def revisions(root: Path) -> list[dict[str, object]]:
    path = root / REVISIONS
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
