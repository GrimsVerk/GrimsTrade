"""The wide-11 functions compute what research/wide-11.md step 2 says they do."""

from __future__ import annotations

import importlib
import math
import sys
import zipfile
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide11_events")
    finally:
        sys.path.remove(str(LIB))


def _row(code: str, yymmdd: str, cl: str, cs: str) -> dict[str, str]:
    return {
        "CFTC Contract Market Code ": code,
        "As of Date in Form YYMMDD": yymmdd,
        "Commercial Positions-Long (All)": cl,
        "Commercial Positions-Short (All)": cs,
    }


def test_shifts_are_forty_odd_and_never_a_year() -> None:
    ev = _ev()
    s = ev.SHIFTS_W22
    assert len(s) == 40 and len(set(s)) == 40
    assert all(27 <= abs(k) <= 103 and k % 2 != 0 and k % 52 != 0 for k in s)
    assert 27 in s and -103 in s and 29 not in s


def test_hedging_pressure_sign() -> None:
    ev = _ev()
    assert ev.hedging_pressure(100.0, 300.0) == 0.5  # hedgers net short -> positive
    assert ev.hedging_pressure(300.0, 100.0) == -0.5
    assert math.isnan(ev.hedging_pressure(0.0, 0.0))


def test_parse_rows_drops_shutdowns_late_reports_and_other_codes() -> None:
    ev = _ev()
    codes = {"GLD": "088691"}
    rows = [
        _row("088691", "180605", "100", "300"),
        _row("088691", "190108", "100", "300"),  # 2018-19 shutdown window
        _row("088691", "251007", "100", "300"),  # 2025 shutdown
        _row("088691", "251111", "100", "300"),  # after the train cut
        _row("999999", "180605", "100", "300"),
        _row("088691", "180605", "300", "100"),  # a later row for the same date wins
    ]
    out = ev.parse_rows(rows, codes, date(2025, 11, 10))
    assert out == {"GLD": {date(2018, 6, 5): -0.5}}
    assert ev.report_date("991228") == date(1999, 12, 28)


def test_read_zips_later_file_wins(tmp_path: Path) -> None:
    ev = _ev()
    hdr = (
        "CFTC Contract Market Code,As of Date in Form YYMMDD,"
        "Commercial Positions-Long (All),Commercial Positions-Short (All)\n"
    )
    paths = []
    for i, body in enumerate(["088691,180605,100,300\n", "088691,180605,300,100\n"]):
        p = tmp_path / f"f{i}.zip"
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("annual.txt", hdr + body)
        paths.append(p)
    out = ev.read_zips(paths, {"GLD": "088691"}, date(2025, 11, 10))
    assert out["GLD"] == {date(2018, 6, 5): -0.5}


def test_zscores_are_past_only_and_need_104_reports() -> None:
    ev = _ev()
    t0 = date(2010, 1, 5)
    hp = {t0 + timedelta(days=7 * i): float(i % 3) for i in range(200)}
    z = ev.zscores(hp)
    assert min(z) == t0 + timedelta(days=7 * 104)  # first date with 104 earlier reports
    d = t0 + timedelta(days=7 * 180)
    prev = [hp[t0 + timedelta(days=7 * i)] for i in range(180 - 156, 180)]
    assert abs(z[d] - (hp[d] - np.mean(prev)) / np.std(prev, ddof=1)) < 1e-12
    hp2 = dict(hp)
    hp2[d] = 99.0  # changing T's own value leaves earlier z untouched
    z2 = ev.zscores(hp2)
    assert all(z2[k] == z[k] for k in z if k < d)
    assert ev.shifted_z(z, d, 3) == z[d - timedelta(days=21)]
    assert math.isnan(ev.shifted_z(z, t0, 1))


def test_outcome_waits_a_week_after_the_position_date() -> None:
    ev = _ev()
    t = date(2020, 1, 7)  # Tuesday position date
    bars = {t + timedelta(days=i): 100.0 + i for i in range(0, 50) if (t.weekday() + i) % 7 < 5}
    px = ev.Closes(bars)
    y = ev.outcome(px, t, 35, date(2025, 11, 10))
    assert abs(y - math.log((100 + 35) / (100 + 7))) < 1e-12
    y1 = ev.outcome(px, t, 14, date(2025, 11, 10))
    assert abs(y1 - math.log((100 + 14) / (100 + 7))) < 1e-12
    assert math.isnan(ev.outcome(px, t, 35, date(2020, 2, 1)))  # exit after the cut
    gap = {d: v for d, v in bars.items() if not t + timedelta(days=30) < d < t + timedelta(days=45)}
    assert math.isnan(ev.outcome(ev.Closes(gap), t, 35, date(2025, 11, 10)))  # exit too late
    r4 = ev.past_return(px, t + timedelta(days=28), 28)
    assert abs(r4 - math.log((100 + 28) / 100)) < 1e-12


def test_ols_dk_matches_ols_and_widens_with_common_week_shocks() -> None:
    ev = _ev()
    rng = np.random.default_rng(0)
    nw, na = 400, 4
    week = np.repeat(np.arange(nw), na)
    common = np.repeat(rng.normal(size=nw), na)
    xc = np.repeat(rng.normal(size=nw), na)  # a dose common to all markets in a week
    y = 0.5 * xc + common + 0.3 * rng.normal(size=nw * na)
    ones = np.ones(nw * na)
    beta, t, n = ev.ols_dk([ones, xc], y, week, 0)
    ref = np.linalg.lstsq(np.column_stack([ones, xc]), y, rcond=None)[0]
    assert n == nw * na and np.allclose(beta, ref)
    # Naive HC t treats the 4 rows of a week as independent: about 2x too large.
    e = y - np.column_stack([ones, xc]) @ ref
    xm = xc - xc.mean()
    t_naive = ref[1] / math.sqrt(float((xm**2) @ (e**2)) / float(xm @ xm) ** 2)
    assert 1.6 < t_naive / t[1] < 2.4
    # An all-zero dummy column is dropped, NaN rows are dropped.
    y2 = y.copy()
    y2[0] = np.nan
    b2, t2, n2 = ev.ols_dk([ones, np.zeros_like(ones), xc], y2, week, 4)
    assert n2 == nw * na - 1 and math.isnan(b2[1]) and abs(b2[2] - 0.5) < 0.2


def test_rank_and_null_spread() -> None:
    ev = _ev()
    assert ev.rank_highest(2.0, [1.0, 3.0, 2.0]) == 2
    sd, share = ev.null_spread([-2.0, 0.0, 2.0, 1.0])
    assert share == 0.5 and sd > 0
