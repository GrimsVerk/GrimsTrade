"""Pure functions for panic-words-1 (W34 `panic-words`, card research/cards/panic-words-1.md)."""

from __future__ import annotations

import math
import re
from collections.abc import Mapping
from datetime import date
from typing import Any

PANIC_RE = re.compile(r"\bpanic(?:s|ky|ked|king)?\b")
CRASH_RE = re.compile(r"\bcrash(?:es|ed|ing)?\b")
MIN_ARTICLES = 2000  # a month is valid with at least this many articles
BASE = 12  # baseline months before the dose month
SHIFTS_W34: list[int] = list(range(25, 104, 2))  # = parkedgates1_events.SHIFTS_W33


def month_index(d: date) -> int:
    """Months since year 0: January 2000 -> 24000 (as wide17_events.month_index)."""
    return d.year * 12 + d.month - 1


def clean(headline: str, article: str) -> str:
    """Headline + article, lower case, line-end hyphens joined, other breaks to spaces."""
    t = f"{headline}\n{article}".lower().replace("-\n", "")
    return t.replace("\n", " ")


def scan_month(obj: Mapping[str, Any], name: str) -> int | None:
    """Publication month of one scan: `edition.date`, else the date that starts the file name."""
    for raw in ((obj.get("edition") or {}).get("date"), name.rsplit("/", 1)[-1][:10]):
        if isinstance(raw, str) and len(raw) >= 7:
            try:
                return int(raw[:4]) * 12 + int(raw[5:7]) - 1
            except ValueError:
                continue
    return None


def count_scan(obj: Mapping[str, Any]) -> tuple[int, int, int]:
    """(articles with text, articles matching panic, articles matching crash) of one scan."""
    n = p = c = 0
    for a in obj.get("full articles") or []:
        art = a.get("article") or ""
        if not art.strip():
            continue
        t = clean(a.get("headline") or "", art)
        n += 1
        p += PANIC_RE.search(t) is not None
        c += CRASH_RE.search(t) is not None
    return n, p, c


def dose(articles: Mapping[int, int], hits: Mapping[int, int]) -> dict[int, float]:
    """d(m) = x(m) - mean(x(m-12..m-1)), x = ln((hits + 0.5) / articles), valid months only."""
    x = {m: math.log((hits.get(m, 0) + 0.5) / n) for m, n in articles.items() if n >= MIN_ARTICLES}
    out: dict[int, float] = {}
    for m, v in x.items():
        past = [x.get(m - j) for j in range(1, BASE + 1)]
        if all(p is not None for p in past):
            out[m] = v - sum(p for p in past if p is not None) / BASE
    return out


def monthly_market(daily: Mapping[date, float]) -> dict[int, tuple[float, float]]:
    """month -> (ln compounded return, sqrt of the sum of squared daily simple returns)."""
    acc: dict[int, list[float]] = {}
    for d in sorted(daily):
        acc.setdefault(month_index(d), []).append(daily[d])
    return {
        m: (sum(math.log1p(r) for r in rs), math.sqrt(sum(r * r for r in rs)))
        for m, rs in acc.items()
    }


def past_return(mkt: Mapping[int, tuple[float, float]], m: int, a: int, b: int) -> float:
    """ln return over months m-a .. m-b (a >= b), NaN if any month is missing."""
    vals = [mkt.get(m - j) for j in range(b, a + 1)]
    if any(v is None for v in vals):
        return math.nan
    return sum(v[0] for v in vals if v is not None)
