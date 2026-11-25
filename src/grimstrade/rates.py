"""The rate idle cash earns: the 13-week T-bill rate, stored append-only in `data/rates.csv`.

Rules and why: docs/DECISIONS.md (2026-11-18, cash interest; 2026-11-24, second bill-rate
source). A row is one session's 13-week bill discount rate (percent) and the time it was stored
(`seen`): Yahoo's `^IRX` close, or for a session Yahoo lacks the US Treasury's published "13
WEEKS BANK DISCOUNT" (`fetch`). Which source gave a row goes in `data/sources.jsonl`. `steps`
turns rows into the `gym.Rates` the gym accrues with: in backtests a rate is known from its
session's close, in the live record from the later of that and `seen`, so the live record never
earns interest it could not have known about when it happened.
"""

from __future__ import annotations

import csv
import io
import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from grimstrade import gym, sources
from grimstrade.data import ETF, SETTLE, append_rows, close_time, read_rows, settled

RATES = Path("data/rates.csv")
FIELDS = ["date", "rate", "seen"]
TICKER = "%5EIRX"  # ^IRX, URL-encoded: the 13-week T-bill discount rate, in percent
# The US Treasury's Daily Treasury Bill Rates, one CSV per calendar year (keyless, public domain).
TREASURY_URL = (
    "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
    "daily-treasury-rates.csv/{year}/all?type=daily_treasury_bill_rates"
)
# The bank discount rate, the convention ^IRX quotes (not the coupon-equivalent yield beside it).
TREASURY_COLUMN = "13 WEEKS BANK DISCOUNT"
YAHOO, TREASURY = "yahoo", "treasury"  # source names in data/sources.jsonl
SYMBOL = "rates"  # the "symbol" of the cash rate's lines in data/sources.jsonl
# A stored rate outside this range (percent) is bad data: ^IRX has been 0.0 to 17.1 since 1960.
LOW, HIGH = -5.0, 30.0


@dataclass(frozen=True)
class Rate:
    date: date  # the session it closed on
    rate: float  # percent, as quoted
    seen: datetime  # when it was stored


def problem(r: Rate, before: date | None = None) -> str | None:
    """Why `r` is not a row a run writes, or None: a weekend, a rate outside LOW..HIGH, stored
    before its session closed, a date not after the row `before` it."""
    if r.date.weekday() >= 5:
        return f"rate for {r.date}: a weekend, when no bills trade"
    if not (math.isfinite(r.rate) and LOW <= r.rate <= HIGH):
        return f"rate for {r.date}: {r.rate}% is not a T-bill rate"
    if r.seen < close_time(ETF, r.date):
        return f"rate for {r.date}: stored at {r.seen}, before its session closed"
    if before is not None and r.date <= before:
        return f"rate for {r.date}: not after the stored rate for {before}"
    return None


def load(root: Path) -> list[Rate]:
    """The stored rates, oldest first. Raises ValueError on a row no run writes (`problem`)."""
    path = root / RATES
    if not path.exists():
        return []
    out: list[Rate] = []
    for row in read_rows(path, FIELDS):
        r = Rate(
            date.fromisoformat(row["date"]),
            float(row["rate"]),
            datetime.fromisoformat(row["seen"]),
        )
        if r.seen.tzinfo is None:
            raise ValueError(f"rate for {r.date}: stored time {row['seen']} has no time zone")
        if p := problem(r, out[-1].date if out else None):
            raise ValueError(p)
        out.append(r)
    return out


def append(root: Path, fetched: Iterable[Rate]) -> tuple[int, list[str]]:
    """Append the rates newer than the newest stored one. Never touches stored rows. Returns
    (rows added, problems): a bad row stops the append there, like a bad bar."""
    stored = load(root)
    last = stored[-1].date if stored else None
    rows: list[Rate] = []
    for r in sorted({r.date: r for r in fetched}.values(), key=lambda r: r.date):
        if last is not None and r.date <= last:
            continue
        if p := problem(r, rows[-1].date if rows else last):
            return _write(root, rows), [p]
        rows.append(r)
    return _write(root, rows), []


def _write(root: Path, rows: Sequence[Rate]) -> int:
    if not rows:
        return 0
    lines = [[r.date.isoformat(), repr(float(r.rate)), r.seen.isoformat()] for r in rows]
    append_rows(root / RATES, FIELDS, lines)
    return len(rows)


def yahoo(since: date, now: datetime, get: sources.Get) -> list[Rate]:
    """`^IRX` closes from `since` on, for sessions settled by `now` (Yahoo chart API, keyless)."""
    bars = settled(sources.yahoo(TICKER, since, get), ETF, now)
    return [Rate(b.date, b.close, now) for b in bars]


def parse_treasury(body: bytes) -> dict[date, float]:
    """The 13-week bank discount rate (percent) per day from one Daily Treasury Bill Rates CSV.
    Columns are found by name (the set of maturities changes over the years); a blank cell is
    no rate. Raises ValueError if the column is missing."""
    if not body.strip():  # a year with no published rates yet answers 200 with an empty body
        return {}
    reader = csv.reader(io.StringIO(body.decode("utf-8-sig")))
    header = [h.strip().upper() for h in next(reader, [])]
    if "DATE" not in header or TREASURY_COLUMN not in header:
        raise ValueError(f"treasury bill rates: no {TREASURY_COLUMN!r} column in {header[:3]}...")
    at, col = header.index("DATE"), header.index(TREASURY_COLUMN)
    out = {}
    for row in reader:
        if len(row) <= max(at, col) or not row[col].strip():
            continue
        out[datetime.strptime(row[at].strip(), "%m/%d/%Y").date()] = float(row[col])
    return out


def treasury(since: date, now: datetime, get: sources.Get) -> list[Rate]:
    """Treasury 13-week bank discount rates from `since` on, for sessions settled by `now` (one
    CSV per calendar year). The Treasury publishes a day's rates in its afternoon; a day not
    published yet is simply missing."""
    out = []
    for year in range(since.year, now.year + 1):
        days = parse_treasury(get(TREASURY_URL.format(year=year)))
        out += [
            Rate(d, r, now)
            for d, r in days.items()
            if d >= since and close_time(ETF, d) + SETTLE <= now
        ]
    return sorted(out, key=lambda r: r.date)


def lacking(since: date, now: datetime, have: set[date]) -> list[date]:
    """Weekdays from `since` on whose session has settled by `now` and that `have` lacks."""
    out, d = [], since
    while close_time(ETF, d) + SETTLE <= now:
        if d.weekday() < 5 and d not in have:
            out.append(d)
        d += timedelta(days=1)
    return out


def fetch(
    since: date, now: datetime, get: sources.Get
) -> tuple[list[tuple[str, Rate]], list[str], bool]:
    """The rates from `since` on, each with its source; what failed; whether any source answered.
    Yahoo `^IRX` first; the Treasury only for settled weekdays Yahoo lacks (Yahoo down or late,
    or a holiday). Yahoo's rate wins for a day both have."""
    found: dict[date, tuple[str, Rate]] = {}
    failed = []
    answered = False
    try:
        found = {r.date: (YAHOO, r) for r in yahoo(since, now, get)}
        answered = True
    except Exception as e:  # noqa: BLE001 - the Treasury is there for exactly this
        failed.append(f"yahoo ^IRX: {e}")
    if lacking(since, now, set(found)):
        try:
            for r in treasury(since, now, get):
                found.setdefault(r.date, (TREASURY, r))
            answered = True
        except Exception as e:  # noqa: BLE001 - one bad answer must not stop the run
            failed.append(f"treasury: {e}")
    return sorted(found.values(), key=lambda x: x[1].date), failed, answered


def steps(rows: Iterable[Rate], live: bool) -> gym.Rates:
    """The rates as the gym takes them: (known from, annual rate as a fraction). `live=True`
    (the record): known from the later of the session close and the time the row was stored.
    `live=False` (backtests, hindsight anyway): known from the session close."""
    out = []
    for r in rows:
        known = close_time(ETF, r.date)
        out.append((max(known, r.seen) if live else known, r.rate / 100))
    return sorted(out, key=lambda x: x[0])
