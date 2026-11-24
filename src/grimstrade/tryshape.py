"""Record length, skew and excess kurtosis of a logged try, written next to its tries.md row.

The research harness (`research/lib/harness.py`, `_log`) calls `log()` right after it appends a
row to `research/tries.md`: one JSON line in `research/tries-shape.jsonl` holding the exact row
text and the shape of the run's weekly returns. The register (`grimstrade.register`) and
`research/register2.py` join these lines to register tries by that text, so every try logged
through the harness carries its shape on every machine, without local equity caches
(card `research/register-3.md`).

Weekly returns follow `research/register2.py`: equity on every calendar day (carried over days
without a bar), simple returns from Friday to Friday; T is their number; skew and excess
kurtosis are population moments. Stdlib only, and nothing else from `grimstrade`, so the module
runs unchanged on every branch's `src/`.
"""

from __future__ import annotations

import fcntl
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

SHAPES = "research/tries-shape.jsonl"  # append-only, like research/tries.md
WEEKS_PER_YEAR = 365.25 / 7
FRIDAY = 4
DIGITS = 4


@dataclass(frozen=True)
class Shape:
    weeks: int  # number of weekly returns
    skew: float
    excess_kurtosis: float
    sharpe_weekly: float  # annualised: weekly mean / sd times sqrt(weeks a year)


def weekly_returns(days: Sequence[date], equity: Sequence[float]) -> list[float]:
    """Simple returns from each Friday's equity to the next (calendar days carried over)."""
    if len(days) != len(equity):
        raise ValueError(f"{len(days)} days but {len(equity)} equity values")
    if not days:
        return []
    known = {d: float(e) for d, e in zip(days, equity, strict=True)}
    first, last = min(known), max(known)
    fridays: list[float] = []
    cur = known[first]
    d = first
    while d <= last:
        cur = known.get(d, cur)
        if d.weekday() == FRIDAY:
            fridays.append(cur)
        d += timedelta(days=1)
    return [b / a - 1 for a, b in zip(fridays, fridays[1:], strict=False)]


def of_returns(rets: Sequence[float]) -> Shape | None:
    """None if fewer than two returns or no variation (nothing to log)."""
    t = len(rets)
    if t < 2:
        return None
    mean = math.fsum(rets) / t
    m2 = math.fsum((r - mean) ** 2 for r in rets) / t
    if m2 <= 0 or not math.isfinite(m2):
        return None
    sd = math.sqrt(m2)
    m3 = math.fsum((r - mean) ** 3 for r in rets) / t
    m4 = math.fsum((r - mean) ** 4 for r in rets) / t
    return Shape(
        t,
        round(m3 / sd**3, DIGITS),
        round(m4 / m2**2 - 3, DIGITS),
        round(mean / sd * math.sqrt(WEEKS_PER_YEAR), DIGITS),
    )


def of_equity(days: Sequence[date], equity: Sequence[float]) -> Shape | None:
    return of_returns(weekly_returns(days, equity))


def to_line(row: str, s: Shape) -> str:
    d = {
        "row": row.strip(),
        "weeks": s.weeks,
        "skew": s.skew,
        "excess_kurtosis": s.excess_kurtosis,
        "sharpe_weekly": s.sharpe_weekly,
    }
    return json.dumps(d, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def log(path: Path, row: str, days: Sequence[date], equity: Sequence[float]) -> Shape | None:
    """Append the shape of a logged row's run to `path` (never rewrites a line). Returns the
    shape, or None (and writes nothing) when the run has no weekly variation."""
    s = of_equity(days, equity)
    if s is None:
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(to_line(row, s) + "\n")
    return s


def read(text: str, where: str = SHAPES) -> dict[str, Shape]:
    """Row text -> its shape. A row logged twice (a re-run) keeps its first line. Raises
    ValueError on a line that is not a shape line."""
    out: dict[str, Shape] = {}
    for n, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        try:
            d = json.loads(raw)
            row = str(d["row"]).strip()
            s = Shape(
                int(d["weeks"]),
                float(d["skew"]),
                float(d["excess_kurtosis"]),
                float(d["sharpe_weekly"]),
            )
        except (ValueError, KeyError, TypeError) as e:
            raise ValueError(f"{where}:{n}: not a shape line ({e})") from e
        if not row.startswith("| 20") or s.weeks < 2:
            raise ValueError(f"{where}:{n}: not a shape line (row or weeks)")
        out.setdefault(row, s)
    return out
