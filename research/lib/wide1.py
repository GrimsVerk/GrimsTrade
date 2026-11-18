"""Glue between the wide-1 rules (`wide1_rules.py`, cards in research/cards/) and the harness:
calendars, the auction file, book universes, and the shared comparison helpers."""

from __future__ import annotations

import bisect
import csv
import math
from collections.abc import Sequence
from datetime import date, timedelta

import common as c
import harness
import macro
import numpy as np
import stats
import wide1_rules as rules
from harness import TRAIN_END, TRAIN_START, Panel, Run, load_history

from grimstrade import data

_calendar: dict[str, list[date]] = {}
_auctions: dict[str, list[tuple[date, date]]] = {}
_out_days: dict[tuple[str, str], set[date]] = {}


def calendar(sym: str) -> list[date]:
    """All trading dates of the symbol, future ones included: dates only, known in advance
    (the rule `month-end-liquidity` already uses)."""
    if sym not in _calendar:
        _calendar[sym] = [b.date for b in data.load(harness.RESEARCH, sym)]
    return _calendar[sym]


def last_session(view: c.View, sym: str) -> date | None:
    """The last closed trading day of `sym` at the decision."""
    d = view.dates(sym)
    return date.fromordinal(int(d[-1])) if len(d) else None


def auctions(group: str) -> list[tuple[date, date]]:
    """(announcement date, auction date) of the card's auctions: `long` for TLT, `mid` for IEF."""
    if not _auctions:
        path = macro.cache_root() / "derived" / "wide-1" / "auctions.csv"
        with path.open(newline="") as f:
            for r in csv.DictReader(f):
                _auctions.setdefault(r["group"], []).append(
                    (date.fromisoformat(r["announced"]), date.fromisoformat(r["auction"]))
                )
    return _auctions[group]


def auction_out(view: c.View, sym: str, group: str) -> bool:
    """True if the decision holds nothing in `sym`: an announced auction is 1-5 sessions ahead."""
    key = (sym, group)
    if key not in _out_days:
        _out_days[key] = rules.out_days(calendar(sym), auctions(group))
    d = last_session(view, sym)
    return d is not None and d in _out_days[key]


def close_on(view: c.View, sym: str, d: date) -> float:
    """The close of `sym` on session `d` (NaN if it has no bar that day or it is not visible)."""
    days = view.dates(sym)
    i = int(np.searchsorted(days, d.toordinal()))
    return float(view.close(sym)[i]) if i < len(days) and days[i] == d.toordinal() else math.nan


def book_ctx(name: str, syms: Sequence[str], min_assets: int) -> c.Ctx:
    """A custom universe through the gym: starts once `min_assets` symbols have a year of bars."""
    hist = load_history("train", True, syms)
    ready = sorted(hist[s][c.bpy(s) - 1].date for s in syms if len(hist[s]) >= c.bpy(s))
    start = max(TRAIN_START, ready[min_assets - 1] + timedelta(days=1))
    end = min(TRAIN_END, max(b[-1].date for b in hist.values()) - timedelta(days=1))
    if c.DRY:
        start = end - timedelta(days=120)
    return c.Ctx(name, "train", hist, Panel(hist), start, end)


def versus(p: Run, t: Run, first_era: str | None = None) -> dict[str, float]:
    """Sharpe difference of `p` to `t` (paired bootstrap p) and the eras ahead, counted from
    `first_era` on."""
    a, b = c.align(p, t)
    diff, pval, _, _ = stats.sharpe_diff_boot(a, b)
    ep, et = c.era_sharpes(p), c.era_sharpes(t)
    names = [n for n in ep if not (math.isnan(ep[n]) or math.isnan(et[n]))]
    if first_era in names:
        names = names[names.index(first_era) :]
    ahead = sum(ep[n] > et[n] for n in names)
    return {"diff": diff, "p": pval, "ahead": ahead, "eras": len(names)}


def since(p: Run, t: Run, d0: date) -> float:
    """Sharpe of `p` minus Sharpe of `t` from `d0` to the end."""
    hi = min(p.days[-1], t.days[-1])
    return stats.sharpe(p.rets_between(d0, hi)) - stats.sharpe(t.rets_between(d0, hi))


def open_to_open(bars: Sequence[data.Bar], a: date, b: date) -> float:
    """Return from the open of the first bar on or after `a` to the open of the first bar on or
    after `b` (NaN if either is missing)."""
    days = [x.date for x in bars]
    i, j = bisect.bisect_left(days, a), bisect.bisect_left(days, b)
    if i >= len(days) or j >= len(days) or j <= i:
        return math.nan
    return bars[j].open / bars[i].open - 1


def tstat(x: np.ndarray) -> float:
    return float(x.mean() / x.std(ddof=1) * math.sqrt(len(x))) if len(x) > 2 else math.nan


def bars_report(bars: Sequence[tuple[str, bool, str]]) -> list[str]:
    out = [f"- {'PASS' if ok else 'FAIL'}: {text} ({detail})" for text, ok, detail in bars]
    return [*out, "", f"**{'PASSES' if all(ok for _, ok, _ in bars) else 'FAILS'} train.**", ""]
