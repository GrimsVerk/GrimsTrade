"""Pure functions for the wide-15 gates W27 `congress-workload` and W28 `refund-runoff`
(research/wide-15.md steps 3 and 4). No function here reads a file, a price or the network."""

from __future__ import annotations

import csv
import io
import json
import math
import statistics
from collections.abc import Iterable, Mapping, Sequence
from datetime import date, timedelta

# W27: earlier doses only (the dose can answer prices), every odd week 27..105 (40).
SHIFTS_EARLY: list[int] = list(range(27, 106, 2))
CLOSE_MARGIN = 0.10  # a close vote: |yea - nay| / (yea + nay) below this


def friday_of(day: date) -> date:
    """The Friday ending the Saturday..Friday week that holds `day`."""
    return day + timedelta(days=(4 - day.weekday()) % 7)


# ---------------------------------------------------------------- W27 roll calls


def parse_rollcalls(text: str, last: date) -> list[tuple[date, str, int, int]]:
    """(date, chamber, yea, nay) of every roll call in Voteview's HSall_rollcalls.csv dated on
    or before `last`. Rows with an unreadable date are skipped; missing counts read as 0."""
    out = []
    for r in csv.DictReader(io.StringIO(text)):
        try:
            d = date.fromisoformat((r.get("date") or "").strip())
        except ValueError:
            continue
        if d > last:
            continue

        def num(k: str, row: Mapping[str, str | None] = r) -> int:
            try:
                return int(float(row.get(k) or 0))
            except ValueError:
                return 0

        out.append((d, (r.get("chamber") or "").strip(), num("yea_count"), num("nay_count")))
    return out


def weekly_counts(
    rolls: Iterable[tuple[date, str, int, int]],
    weeks: Sequence[date],
    chamber: str | None = None,
    close_only: bool = False,
) -> dict[date, int]:
    """n(F): roll calls dated F - 6 .. F for each Friday F in `weeks` (0 if none), optionally one
    chamber or close votes only."""
    n = {f: 0 for f in weeks}
    for d, ch, yea, nay in rolls:
        if chamber is not None and ch != chamber:
            continue
        if close_only and not (yea + nay > 0 and abs(yea - nay) / (yea + nay) < CLOSE_MARGIN):
            continue
        f = friday_of(d)
        if f in n:
            n[f] += 1
    return n


def anscombe(n: int) -> float:
    """Variance-stabilised count: 2 sqrt(n + 3/8)."""
    return 2.0 * math.sqrt(n + 0.375)


def workload_dose(counts: Mapping[date, int]) -> dict[date, tuple[float, float]]:
    """(x, s) per Friday: x = anscombe(n), s = 1 if in session (n > 0)."""
    return {f: (anscombe(n), 1.0 if n > 0 else 0.0) for f, n in counts.items()}


def shifted_pair(dose: Mapping[date, tuple[float, float]], t: date, k: int) -> tuple[float, float]:
    """(x, s)(t - 7k days), or (NaN, NaN) if missing."""
    return dose.get(t - timedelta(days=7 * k), (math.nan, math.nan))


# ---------------------------------------------------------------- W28 refunds


def is_individual(kind: str) -> bool:
    """A refund row that pays individuals (checks or EFT), in either DTS format."""
    k = kind.lower()
    return "individual" in k and "business" not in k


def parse_refund_pages(pages: Iterable[str], last: date) -> dict[date, float]:
    """D(day): individual refunds (millions of USD) per day, summed over the matching rows of
    the fiscaldata `income_tax_refunds_issued` JSON pages; days after `last` never read."""
    out: dict[date, float] = {}
    for page in pages:
        for r in json.loads(page).get("data", []):
            try:
                d = date.fromisoformat(str(r.get("record_date", "")))
                amt = float(r.get("tax_refund_today_amt"))
            except (TypeError, ValueError):
                continue
            if d > last or not is_individual(str(r.get("tax_refund_type", ""))):
                continue
            out[d] = out.get(d, 0.0) + amt
    return out


def weekly_sums(daily: Mapping[date, float], weeks: Sequence[date]) -> dict[date, float]:
    """R(F) = sum of D over F - 6 .. F, for Fridays with at least one reported day."""
    acc: dict[date, float] = {}
    for d, v in daily.items():
        f = friday_of(d)
        acc[f] = acc.get(f, 0.0) + v
    return {f: acc[f] for f in weeks if f in acc}


def year_totals(daily: Mapping[date, float]) -> dict[int, float]:
    """T(y) = sum of D over calendar year y, only for years the data cover from their first
    week (first reported day on or before 7 January) through their last week."""
    if not daily:
        return {}
    first, final = min(daily), max(daily)
    out: dict[int, float] = {}
    for y in range(first.year, final.year + 1):
        if date(y, 1, 1) < first - timedelta(days=6) or date(y, 12, 31) > final + timedelta(days=6):
            continue
        out[y] = sum(v for d, v in daily.items() if d.year == y)
    return out


def refund_surprise(weekly: Mapping[date, float], totals: Mapping[int, float]) -> dict[date, float]:
    """d(F) = 100 (R(F) - B(F)) / T(year(F) - 1); B(F) = median of R at the same ISO week of
    the three previous ISO years (at least two present). ISO week 53 has no baseline."""
    by_iso = {f.isocalendar()[:2]: v for f, v in weekly.items()}
    out: dict[date, float] = {}
    for f, v in weekly.items():
        y, w = f.isocalendar()[:2]
        if w == 53 or (f.year - 1) not in totals or totals[f.year - 1] <= 0:
            continue
        base = [by_iso[(y - j, w)] for j in (1, 2, 3) if (y - j, w) in by_iso]
        if len(base) < 2:
            continue
        out[f] = 100.0 * (v - statistics.median(base)) / totals[f.year - 1]
    return out


def _gamma2_cdf(tau: float) -> float:
    """CDF of the Nash-cascade kernel h(tau) = tau exp(-tau): 1 - (1 + tau) exp(-tau)."""
    return 1.0 - (1.0 + tau) * math.exp(-tau)


def kernel_weights(lags: int = 8, entry: int = 5, exit_: int = 33) -> list[float]:
    """w_i, i = 0..lags-1: the share of week F - i's refunds that h delivers inside the outcome
    window (days F + entry .. F + exit_, i.e. weeks i + entry/7 .. i + exit_/7 after it)."""
    return [_gamma2_cdf(i + exit_ / 7) - _gamma2_cdf(i + entry / 7) for i in range(lags)]


def runoff(surprise: Mapping[date, float], weeks: Sequence[date]) -> dict[date, float]:
    """u(F) = sum_i w_i d(F - 7i); only Fridays with every term present."""
    w = kernel_weights()
    out: dict[date, float] = {}
    for f in weeks:
        terms = [surprise.get(f - timedelta(days=7 * i)) for i in range(len(w))]
        if any(t is None for t in terms):
            continue
        out[f] = sum(wi * float(t) for wi, t in zip(w, terms, strict=True))  # type: ignore[arg-type]
    return out
