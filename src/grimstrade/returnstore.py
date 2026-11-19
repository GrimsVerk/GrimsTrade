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

Only strategy returns: never prices or other market data. Stdlib only.
"""

from __future__ import annotations

import csv
import gzip
import io
import math
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
