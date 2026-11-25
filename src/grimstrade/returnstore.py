"""The committed store of weekly strategy returns behind the bar (card `research/register-4.md`).

`research/register2.py` measures the trials' record length, shape and correlation from their
weekly returns. Those used to exist only as gitignored caches on one machine (re-simulated
baselines, live strategies, the harness's saved equity curves); this store commits the weekly
returns themselves, so `trials.json`, `moments.jsonl` and BAR.md regenerate on any checkout.

Layout: `research/register/returns/<family>.csv.gz`, one gzip file per family (the register's
`Idea` column; the live strategies are `live`), written with a zero timestamp and no file name
so the same series give the same bytes everywhere. One CSV row per series:

    source,idea,variant,start,sharpe,first_friday,micro_returns

- `source`: `harness@<sha>` (a re-simulated baseline), `live@<sha>` or `curve` (a saved curve).
- `start`: first day of the record; `sharpe`: the harness's daily Sharpe at full precision
  (used to match the series to its register row; see `register2.match`).
- `micro_returns`: the weekly simple returns, Friday to Friday, on consecutive Fridays from
  `first_friday` (the first return ends there), as integers in millionths (rounded to 1e-6),
  space separated; `nan`, `inf` and `-inf` as such.

Only weekly strategy returns, never raw bars. Buy-and-hold baselines are strategies too, so their
series are a coarse weekly index of one asset: weekly returns, rounded to 1e-6, derived from
Yahoo ETF and index prices (SPY, QQQ, GLD, TLT, euro UCITS funds, FTSE/DAX/Nikkei/S&P 500
indices) and crypto exchange prices back to 1994, plus Ken French and Shiller series. Accepted
(2026-11-24, lead's call): a weekly return is a derived statistic, not the source's bars (no
open/high/low/close/volume, no daily data), and `paper-trail` already publishes the live six's
daily bars since 2024-12. Raw bars stay out of git (`research/data/` is ignored). Stdlib only.

register-5: the research harness (`research/lib/harness.py`, `_log`) adds a train try's series
here itself when it logs the row (`of_equity`, then `add`), so no saved curve is needed; the
row is the one `register2.py export` builds from that try's saved curve (same key).
"""

from __future__ import annotations

import csv
import fcntl
import gzip
import io
import math
import os
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

STORE = "research/register/returns"
SUFFIX = ".csv.gz"
HEADER = ("source", "idea", "variant", "start", "sharpe", "first_friday", "micro_returns")
SCALE = 1_000_000  # returns are kept in millionths
BUDGET = 5_000_000  # bytes for the whole store (card register-4)
# register-7: kinds whose curves are not stored by default (never selectable; the harness hook
# skips them and `register2.py export` needs `--robustness`). Rows already stored stay.
NOT_STORED_BY_DEFAULT = frozenset({"robustness"})
FRIDAY = 4


class StoreError(ValueError):
    pass


def quantize(rets: Iterable[float]) -> list[float]:
    """Returns as the store keeps them: rounded to 1e-6, non-finite values unchanged."""
    return [round(v * SCALE) / SCALE if math.isfinite(v) else v for v in rets]


def _token(v: float) -> str:
    if math.isnan(v):
        return "nan"
    if math.isinf(v):
        return "inf" if v > 0 else "-inf"
    return str(round(v * SCALE))


def _value(tok: str) -> float:
    return float(tok) if tok in ("nan", "inf", "-inf") else int(tok) / SCALE


@dataclass(frozen=True)
class Row:
    """One stored series. `rets` are already rounded to 1e-6 (`quantize`)."""

    source: str
    idea: str
    variant: str
    start: str
    sharpe: float
    first_friday: str
    rets: tuple[float, ...]

    @classmethod
    def of(
        cls,
        source: str,
        idea: str,
        variant: str,
        start: str,
        sharpe: float,
        weeks: Sequence[str],
        rets: Sequence[float],
    ) -> Row:
        """From a series keyed by the Fridays its returns end on (consecutive, checked)."""
        if len(weeks) != len(rets) or not weeks:
            raise StoreError(f"{idea}/{variant}: {len(weeks)} weeks, {len(rets)} returns")
        first = date.fromisoformat(weeks[0])
        if first.weekday() != FRIDAY or any(
            w != (first + timedelta(days=7 * k)).isoformat() for k, w in enumerate(weeks)
        ):
            raise StoreError(f"{idea}/{variant}: weeks are not consecutive Fridays")
        return cls(source, idea, variant, start, sharpe, weeks[0], tuple(quantize(rets)))

    def weeks(self) -> list[str]:
        first = date.fromisoformat(self.first_friday)
        return [(first + timedelta(days=7 * k)).isoformat() for k in range(len(self.rets))]

    def tokens(self) -> str:
        return " ".join(_token(v) for v in self.rets)

    def key(self) -> tuple[str, str, str, str, float, str, str]:
        """Identity and canonical order (identical rows are one series)."""
        return (
            self.source,
            self.idea,
            self.variant,
            self.start,
            self.sharpe,
            self.first_friday,
            self.tokens(),
        )


def family_file(idea: str) -> str:
    """File name of a family: the idea with anything but letters, digits, `.`, `_`, `-`
    replaced by `_` (two ideas sharing a name share the file; the idea is a column)."""
    return (re.sub(r"[^A-Za-z0-9._-]", "_", idea) or "_") + SUFFIX


def merge(*sets: Iterable[Row]) -> list[Row]:
    """Union of rows, identical rows once, in canonical order."""
    out: dict[tuple[str, str, str, str, float, str, str], Row] = {}
    for rows in sets:
        for r in rows:
            out.setdefault(r.key(), r)
    return [out[k] for k in sorted(out)]


def encode(rows: Iterable[Row]) -> bytes:
    """One family file's bytes: canonical order, deterministic gzip."""
    text = io.StringIO()
    w = csv.writer(text, lineterminator="\n")
    w.writerow(HEADER)
    for r in merge(rows):
        w.writerow([r.source, r.idea, r.variant, r.start, repr(r.sharpe), r.first_friday,
                    r.tokens()])  # fmt: skip
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0, compresslevel=9) as gz:
        gz.write(text.getvalue().encode())
    return buf.getvalue()


def decode(raw: bytes, where: str) -> list[Row]:
    rows = list(csv.reader(io.StringIO(gzip.decompress(raw).decode())))
    if not rows or tuple(rows[0]) != HEADER:
        raise StoreError(f"{where}: header is not {','.join(HEADER)}")
    out = []
    for n, f in enumerate(rows[1:], 2):
        if len(f) != len(HEADER):
            raise StoreError(f"{where}:{n}: {len(f)} fields")
        rets = tuple(_value(t) for t in f[6].split())
        out.append(Row(f[0], f[1], f[2], f[3], float(f[4]), f[5], rets))
    return out


def read(directory: Path) -> list[Row]:
    """Every stored row, in canonical order; empty when there is no store."""
    if not directory.is_dir():
        return []
    return merge(*(decode(p.read_bytes(), str(p)) for p in sorted(directory.glob(f"*{SUFFIX}"))))


def write(directory: Path, rows: Iterable[Row]) -> dict[str, int]:
    """Rewrite the store with exactly `rows` (one file per family; files of families no longer
    present are removed). Returns bytes per file."""
    by_file: dict[str, list[Row]] = {}
    for r in rows:
        by_file.setdefault(family_file(r.idea), []).append(r)
    directory.mkdir(parents=True, exist_ok=True)
    sizes = {}
    for name in sorted(by_file):
        raw = encode(by_file[name])
        path = directory / name
        if not path.exists() or path.read_bytes() != raw:
            path.write_bytes(raw)
        sizes[name] = len(raw)
    for old in directory.glob(f"*{SUFFIX}"):
        if old.name not in by_file:
            old.unlink()
    return sizes


def _ratio(b: float, a: float) -> float:
    """b / a - 1 as numpy computes it (register2), also when a is zero."""
    if a == 0:
        return (
            math.nan
            if b == 0 or math.isnan(b)
            else math.copysign(math.inf, b) * (math.copysign(1.0, a))
        )
    return b / a - 1


def of_equity(
    source: str,
    idea: str,
    variant: str,
    days: Sequence[date],
    equity: Sequence[float],
    sharpe: float,
) -> Row | None:
    """A series from an equity curve as `research/register2.py` builds it from a saved curve:
    equity on every calendar day (carried over days without a bar), simple returns Friday to
    Friday keyed by the Friday they end on; `start` is the first day. `sharpe` is the harness's
    daily Sharpe of the same curve. None when the curve holds no full week."""
    if len(days) != len(equity):
        raise StoreError(f"{idea}/{variant}: {len(days)} days but {len(equity)} equity values")
    if not days:
        return None
    known = {d: float(e) for d, e in zip(days, equity, strict=True)}
    first, last = days[0], days[-1]
    fridays: list[tuple[date, float]] = []
    cur = float(equity[0])
    d = first
    while d <= last:
        cur = known.get(d, cur)
        if d.weekday() == FRIDAY:
            fridays.append((d, cur))
        d += timedelta(days=1)
    if len(fridays) < 2:
        return None
    weeks = [f.isoformat() for f, _ in fridays[1:]]
    rets = [_ratio(b, a) for (_, a), (_, b) in zip(fridays, fridays[1:], strict=False)]
    return Row.of(source, idea, variant, first.isoformat(), sharpe, weeks, rets)


def add(directory: Path, rows: Iterable[Row]) -> dict[str, int]:
    """Merge `rows` into their family files; other files are not touched. Holds an exclusive
    lock on the directory, so parallel runs of one lane keep each other's rows, and replaces
    each changed file in one rename. Returns the bytes of each family file touched."""
    by_file: dict[str, list[Row]] = {}
    for r in rows:
        by_file.setdefault(family_file(r.idea), []).append(r)
    if not by_file:
        return {}
    directory.mkdir(parents=True, exist_ok=True)
    fd = os.open(directory, os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        sizes = {}
        for name in sorted(by_file):
            path = directory / name
            old = path.read_bytes() if path.exists() else None
            stored = decode(old, str(path)) if old is not None else []
            raw = encode(stored + by_file[name])
            if raw != old:
                tmp = directory / f".{name}.tmp"
                tmp.write_bytes(raw)
                os.replace(tmp, path)
            sizes[name] = len(raw)
        return sizes
    finally:
        os.close(fd)  # releases the lock


def size(directory: Path) -> int:
    """Bytes of the whole store (the budget is checked against this)."""
    if not directory.is_dir():
        return 0
    return sum(p.stat().st_size for p in directory.glob(f"*{SUFFIX}"))
