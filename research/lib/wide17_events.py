"""Pure functions for the wide-17 gates W29 `temperature-premium` and W30 `outbreak-premium`
(research/cards/wide-17.md). No function here reads a file, a price or the network."""

from __future__ import annotations

import csv
import io
import json
import math
from collections.abc import Iterable, Mapping, Sequence
from datetime import date, timedelta

from wide13_events import Closes

# W29: months, both ways (temperature does not answer prices), step 4, never a multiple of 12.
SHIFTS_W29: list[int] = [s * k for k in range(13, 90, 4) for s in (1, -1)]
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def month_index(d: date) -> int:
    """Months since year 0: January 2000 -> 24000."""
    return d.year * 12 + d.month - 1


def month_last_day(m: int) -> date:
    y, mo = divmod(m + 1, 12)
    return date(y, mo + 1, 1) - timedelta(days=1)


# ---------------------------------------------------------------- W29 temperature


def parse_gistemp(text: str, last: date) -> dict[int, float]:
    """Monthly anomaly (deg C) by month index from GISTEMP's GLB.Ts+dSST.csv. Months after the
    month of `last` and missing cells ('***') are left out."""
    rows = text.splitlines()
    start = next(i for i, r in enumerate(rows) if r.startswith("Year,"))
    out: dict[int, float] = {}
    cut = month_index(last)
    for r in csv.DictReader(io.StringIO("\n".join(rows[start:]))):
        try:
            y = int((r.get("Year") or "").strip())
        except ValueError:
            continue
        for j, name in enumerate(MONTHS):
            m = y * 12 + j
            v = (r.get(name) or "").strip()
            if m > cut or not v or "*" in v:
                continue
            out[m] = float(v)
    return out


def _mean(a: Mapping[int, float], lo: int, hi: int) -> float:
    """Mean of a over months lo..hi inclusive; NaN if any is missing."""
    vals = [a.get(m) for m in range(lo, hi + 1)]
    if any(v is None for v in vals):
        return math.nan
    return sum(v for v in vals if v is not None) / len(vals)


def temp_dose(a: Mapping[int, float]) -> dict[int, float]:
    """d(m) = mean of A over m-11..m minus mean of A over m-131..m-12."""
    out = {}
    for m in a:
        v = _mean(a, m - 11, m) - _mean(a, m - 131, m - 12)
        if not math.isnan(v):
            out[m] = v
    return out


def temp_innovation(a: Mapping[int, float]) -> dict[int, float]:
    """A(m) minus the mean of A over m-120..m-1."""
    out = {}
    for m, v in a.items():
        base = _mean(a, m - 120, m - 1)
        if not math.isnan(base):
            out[m] = v - base
    return out


def shifted_month(d: Mapping[int, float], m: int, k: int) -> float:
    """d_k(m) = d(m - k); NaN if missing."""
    return d.get(m - k, math.nan)


def month_return(px: Closes, entry_month: int, exit_month: int, last: date) -> float:
    """ln(close of the last bar <= end of exit_month / close of the last bar <= end of
    entry_month). NaN if a bar is missing, not inside its month, or the exit bar is after
    `last`."""
    a = px.last_on_or_before(month_last_day(entry_month))
    b = px.last_on_or_before(month_last_day(exit_month))
    if a is None or b is None or b > last or exit_month <= entry_month:
        return math.nan
    if month_index(a) != entry_month or month_index(b) != exit_month:
        return math.nan
    return math.log(px.c[b] / px.c[a])


# ---------------------------------------------------------------- W30 outbreak reports


def parse_don_pages(pages: Iterable[str], last: date) -> list[date]:
    """Publication dates (UTC day) of every WHO Disease Outbreak News item dated on or before
    `last`, from the API's JSON pages. Items without a readable date are skipped."""
    out = []
    for text in pages:
        for item in json.loads(text).get("value", []):
            s = str(item.get("PublicationDate") or "")[:10]
            try:
                d = date.fromisoformat(s)
            except ValueError:
                continue
            if d <= last:
                out.append(d)
    return out


def weekly_counts(days: Iterable[date], fridays: Sequence[date]) -> dict[date, int]:
    """n(F): items dated F - 6 .. F (Saturday..Friday) for each Friday in `fridays`."""
    n = {f: 0 for f in fridays}
    for d in days:
        f = d + timedelta(days=(4 - d.weekday()) % 7)
        if f in n:
            n[f] += 1
    return n


def outbreak_dose(counts: Mapping[date, int]) -> dict[date, float]:
    """x(F) = 2 sqrt(n(F) + 3/8) minus its mean over the 52 weeks F - 7 .. F - 364 (all 52
    must be present in `counts`)."""
    z = {f: 2.0 * math.sqrt(n + 0.375) for f, n in counts.items()}
    out = {}
    for f, v in z.items():
        base = [z.get(f - timedelta(days=7 * i)) for i in range(1, 53)]
        if all(b is not None for b in base):
            out[f] = v - sum(b for b in base if b is not None) / 52
    return out
