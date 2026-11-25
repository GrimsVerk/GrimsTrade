"""The panic-words-1 functions compute what research/cards/panic-words-1.md says they do."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("panicwords1_events")
    finally:
        sys.path.remove(str(LIB))


def test_shifts_are_forty_earlier_doses_off_the_year() -> None:
    s = _ev().SHIFTS_W34
    assert len(s) == 40 and len(set(s)) == 40
    assert min(s) >= 25 and all(k % 12 for k in s)


def test_panic_matches_word_forms_not_substrings() -> None:
    ev = _ev()
    obj = {
        "full articles": [
            {"headline": "PANIC ON THE EXCHANGE", "article": "brokers fled"},
            {"headline": "", "article": "a panicky crowd"},
            {"headline": "", "article": "the pan-\nic spread"},  # line-end hyphen joined
            {"headline": "", "article": "hispanic and panicle"},
            {"headline": "Linen", "article": "fine crash towels"},
            {"headline": "x", "article": "   "},  # no text: not an article
        ]
    }
    n, p, c = ev.count_scan(obj)
    assert (n, p, c) == (5, 3, 1)


def test_scan_month_prefers_publication_date_then_file_name() -> None:
    ev = _ev()
    assert ev.scan_month({"edition": {"date": "1929-10-29"}}, "x/1930-01-01_p1.json") == (
        1929 * 12 + 9
    )
    assert ev.scan_month({}, "faro_1937/1937-03-02_p5_sn1.json") == 1937 * 12 + 2
    assert ev.scan_month({}, "faro/notadate.json") is None


def test_dose_is_surprise_against_the_past_twelve_valid_months() -> None:
    ev = _ev()
    arts = {m: 10_000 for m in range(13)}
    hits = {m: 9 for m in range(12)} | {12: 99}
    d = ev.dose(arts, hits)
    assert list(d) == [12]  # months 0..11 lack a full baseline
    assert math.isclose(d[12], math.log(99.5 / 10_000) - math.log(9.5 / 10_000))
    arts[5] = 100  # an invalid month breaks the baseline
    assert ev.dose(arts, hits) == {}


def test_monthly_market_compounds_and_past_return_needs_every_month() -> None:
    ev = _ev()
    daily = {date(1930, 1, 2): 0.10, date(1930, 1, 3): -0.10, date(1930, 2, 3): 0.05}
    mkt = ev.monthly_market(daily)
    jan, feb = 1930 * 12, 1930 * 12 + 1
    assert math.isclose(mkt[jan][0], math.log(1.1 * 0.9))
    assert math.isclose(mkt[jan][1], math.sqrt(0.02))
    assert math.isclose(ev.past_return(mkt, feb + 1, 2, 1), math.log(0.99) + math.log(1.05))
    assert math.isnan(ev.past_return(mkt, feb + 1, 3, 1))
