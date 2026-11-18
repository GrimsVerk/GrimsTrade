"""The wide-8 functions compute what research/wide-8.md says they do."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _rules() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide8_rules")
    finally:
        sys.path.remove(str(LIB))


def _daily(start: date, end: date) -> list[date]:
    out, d = [], start
    while d <= end:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def test_month_helpers() -> None:
    r = _rules()
    assert r.month_end(2024, 2) == date(2024, 2, 29)
    assert r.shift_month(2026, 1, -1) == (2025, 12)
    assert r.shift_month(2026, 12, 1) == (2027, 1)


def test_window_point_december_is_ytd_and_turn_of_year() -> None:
    r = _rules()
    days = _daily(date(2019, 12, 1), date(2021, 1, 31))
    logc = np.array([0.001 * i for i in range(len(days))])
    got = r.window_point(days, logc, 2020, 12, date(2021, 1, 31))
    assert got is not None
    lo, ret = got
    i0 = days.index(date(2019, 12, 31))
    i1 = days.index(date(2020, 11, 30))
    j0 = days.index(date(2020, 12, 31))
    j1 = days.index(date(2021, 1, 8))  # 10 Jan 2021 is a Sunday
    assert lo == 0.0  # a rising fund is no loser
    assert abs(ret - (logc[j1] - logc[j0])) < 1e-12
    falling = -logc
    lo2, _ = r.window_point(days, falling, 2020, 12, date(2021, 1, 31))
    assert abs(lo2 - (logc[i1] - logc[i0])) < 1e-12


def test_window_point_placebo_dose_ends_a_month_before() -> None:
    r = _rules()
    days = _daily(date(2019, 1, 1), date(2020, 12, 31))
    logc = -np.array([0.001 * i for i in range(len(days))])
    lo, _ = r.window_point(days, logc, 2020, 3, date(2020, 12, 31))
    i0 = r.last_on_or_before(days, date(2019, 3, 31))
    i1 = r.last_on_or_before(days, date(2020, 2, 29))
    assert abs(lo - (logc[i0] - logc[i1])) < 1e-12


def test_window_point_refuses_unread_or_missing_bars() -> None:
    r = _rules()
    days = _daily(date(2019, 12, 1), date(2021, 1, 31))
    logc = np.zeros(len(days))
    assert r.window_point(days, logc, 2020, 12, date(2021, 1, 9)) is None  # window not done
    assert r.window_point(days, logc, 2019, 12, date(2021, 1, 31)) is None  # no dose start
    gap = [d for d in days if d.month != 11 or d.year != 2020]  # no November bar
    assert r.window_point(gap, np.zeros(len(gap)), 2020, 12, date(2021, 1, 31)) is None


def test_cross_t_matches_textbook_ols() -> None:
    r = _rules()
    x = [0.0, 0.0, 0.1, 0.2, 0.3]
    y = [0.01, -0.01, 0.02, 0.05, 0.04]
    b, t = r.cross_t(x, y)
    xa, ya = np.array(x), np.array(y)
    bb = np.polyfit(xa, ya, 1)[0]
    e = ya - np.polyval(np.polyfit(xa, ya, 1), xa)
    se = math.sqrt((e @ e) / 3 / ((xa - xa.mean()) @ (xa - xa.mean())))
    assert abs(b - bb) < 1e-12 and abs(t - bb / se) < 1e-9
    assert math.isnan(r.cross_t([0.0, 0.0, 0.0], [1.0, 2.0, 3.0])[0])


def test_empirical_p_and_verdict() -> None:
    r = _rules()
    null = [-1.0, 0.0, 1.0, 2.0]
    assert r.empirical_p(3.0, null) == 1 / 5
    assert r.empirical_p(1.0, null) == 3 / 5
    few = [(0.1, 0.0)] * 2 + [(0.0, 0.0)] * 20
    assert r.verdict(few, null, 0.2)["verdict"].startswith("no verdict")
    rng = np.random.default_rng(0)
    pts = [
        (lo, 0.5 * lo + 0.001 * e)
        for lo, e in zip(
            np.r_[np.zeros(15), np.linspace(0.05, 0.3, 6)], rng.standard_normal(21), strict=True
        )
    ]
    v = r.verdict(pts, null, 0.2)
    assert v["verdict"] == "pass" and v["losers"] == 6 and v["funds"] == 21
    v2 = r.verdict([(lo, -ret) for lo, ret in pts], null, 0.2)
    assert v2["verdict"] == "fail"


def test_power_rises_with_effect() -> None:
    r = _rules()
    rng = np.random.default_rng(1)
    wins = []
    for _ in range(40):
        lo = np.r_[np.zeros(15), rng.uniform(0.05, 0.3, 6)]
        wins.append(list(zip(lo, 0.02 * rng.standard_normal(21), strict=True)))
    null = [r.cross_t([p[0] for p in w], [p[1] for p in w])[1] for w in wins]
    assert r.power(wins, null, 0.0, 0.05) <= 0.1
    assert r.power(wins, null, 1.0, 0.05) > 0.9


def test_rule_hash_is_canonical() -> None:
    r = _rules()
    a = r.rule_hash({"f": "1"}, {"x": 1, "y": 2}, {"s": "z"})
    b = r.rule_hash({"f": "1"}, {"y": 2, "x": 1}, {"s": "z"})
    assert a == b and len(a) == 64


def _events() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide8_events")
    finally:
        sys.path.remove(str(LIB))


def test_parse_ap_reads_the_24th_field_and_skips_missing() -> None:
    ev = _events()
    text = (
        "# header\n"
        "1932 01 01     0     0.5 1352 10  3.333  2.667  2.333  2.667  3.333  2.667  3.333  "
        "3.333   18   12    9   12   18   12   18   18    15  22     -1.0     -1.0 2\n"
        "1932 01 02     1     1.5 1352 11  3.667  3.667  3.333  3.667  3.333  4.667  3.000  "
        "5.000   22   22   18   22   18   39   15   48    -1  43     -1.0     -1.0 2\n"
    )
    assert ev.parse_ap(text) == {date(1932, 1, 1): 15}


def test_storm_max_covers_first_six_sessions_after_the_day() -> None:
    ev = _events()
    days = _daily(date(2024, 5, 1), date(2024, 5, 31))
    storm = date(2024, 5, 10)  # a Friday
    m = ev.storm_max(days, {storm: 200})
    after = [d for d in days if d > storm][:6]
    for d, v in zip(days, m, strict=True):
        if d < days[6]:
            assert math.isnan(v)
        else:
            assert v == (200 if d in after else 0), d
    shifted = ev.storm_max(days, {storm: 200}, shift=3)  # storm now on Monday 13 May
    assert [d for d, v in zip(days, shifted, strict=True) if v == 200][0] == date(2024, 5, 14)


def test_storm_design_and_rank() -> None:
    ev = _events()
    x = ev.storm_design(np.array([0.0, 30.0, 99.0, 100.0, 250.0]))
    assert x[:, 1].tolist() == [0, 0, 0, 1, 1]
    assert x[:, 2].tolist() == [0, 1, 1, 0, 0]
    assert ev.rank_most_negative(-3.0, [-1.0, -4.0, 2.0]) == 2
