"""The rate idle cash earns: the 13-week T-bill rate, stored append-only in `data/rates.csv`.

Rules and why: docs/DECISIONS.md (2026-11-18, cash interest). A row is one session's `^IRX`
close (percent) and the time it was stored (`seen`). `steps` turns rows into the `gym.Rates`
the gym accrues with: in backtests a rate is known from its session's close, in the live record
from the later of that and `seen`, so the live record never earns interest it could not have
known about when it happened.
"""

from __future__ import annotations

import csv
import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from grimstrade import gym, sources
from grimstrade.data import ETF, close_time, ends_mid_line, settled

RATES = Path("data/rates.csv")
FIELDS = ["date", "rate", "seen"]
TICKER = "%5EIRX"  # ^IRX, URL-encoded: the 13-week T-bill discount rate, in percent
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
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
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
    path = root / RATES
    path.parent.mkdir(parents=True, exist_ok=True)
    header = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="") as f:
        if ends_mid_line(path):
            f.write("\n")
        w = csv.writer(f, lineterminator="\n")
        if header:
            w.writerow(FIELDS)
        for r in rows:
            w.writerow([r.date.isoformat(), repr(float(r.rate)), r.seen.isoformat()])
    return len(rows)


def fetch(since: date, now: datetime, get: sources.Get) -> list[Rate]:
    """`^IRX` closes from `since` on, for sessions settled by `now` (Yahoo chart API, keyless)."""
    bars = settled(sources.yahoo(TICKER, since, get), ETF, now)
    return [Rate(b.date, b.close, now) for b in bars]


def steps(rows: Iterable[Rate], live: bool) -> gym.Rates:
    """The rates as the gym takes them: (known from, annual rate as a fraction). `live=True`
    (the record): known from the later of the session close and the time the row was stored.
    `live=False` (backtests, hindsight anyway): known from the session close."""
    out = []
    for r in rows:
        known = close_time(ETF, r.date)
        out.append((max(known, r.seen) if live else known, r.rate / 100))
    return sorted(out, key=lambda x: x[0])
