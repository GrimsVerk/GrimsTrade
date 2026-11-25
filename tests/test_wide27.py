"""Offline tests for research/lib/wide27.py (W44 `revision-noise`)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "lib"))

import wide27 as w  # noqa: E402


def test_vintage_month_two_digit_years() -> None:
    assert w.vintage_month("EMPLOY64M12") == w.mi(1964, 12)
    assert w.vintage_month("EMPLOY99M1") == w.mi(1999, 1)
    assert w.vintage_month("EMPLOY26M10") == w.mi(2026, 10)
    assert w.vintage_month("DATE") is None


def test_parse_vintages_cuts_train_and_missing() -> None:
    rows = [
        ["DATE", "EMPLOY25M10", "EMPLOY25M11"],
        ["2025:08", "100", "101"],
        ["2025:09", "#N/A", "102"],
        [],
    ]
    vs = w.parse_vintages(rows)
    assert list(vs) == [w.mi(2025, 10)]  # 2025-11 vintage is after the train cut
    assert vs[w.mi(2025, 10)] == {w.mi(2025, 8): 100.0}


def _vintages() -> w.Vintages:
    # level 100 * 1.01^j; vintage v knows months up to v-1, and v revises month v-2 by +x
    vs: w.Vintages = {}
    for v in range(w.mi(2000, 1), w.mi(2001, 1)):
        vs[v] = {j: 100.0 * 1.01 ** (j - w.mi(1999, 1)) for j in range(w.mi(1999, 1), v)}
    return vs


def test_revision_zero_without_changes_and_positive_with() -> None:
    vs = _vintages()
    v = w.mi(2000, 6)
    assert w.revision(vs, v) == 0.0
    vs[v][v - 2] *= 1.002  # revises month v-2's change up and month v-1's change down
    r = w.revision(vs, v)
    assert math.isclose(r, 100 * math.log(1.002), rel_tol=1e-9)
    assert math.isclose(w.revision(vs, v, first_only=True), r)


def test_revision_missing_previous_vintage_is_nan() -> None:
    vs = _vintages()
    assert math.isnan(w.revision(vs, w.mi(2000, 1)))


def test_dose_uses_only_past_months() -> None:
    rev = {v: 1.0 for v in range(0, 200)}
    lr = {v: math.log(w.rolling_mean(rev, v, 12)) for v in range(11, 200)}
    assert all(x == 0.0 for x in lr.values())


def test_controls_growth_and_volatility() -> None:
    vs = {w.mi(2000, 1): {j: 100.0 * 1.01**j for j in range(w.mi(1998, 1), w.mi(2000, 1))}}
    g12, s12 = w.controls(vs, w.mi(2000, 1))
    assert math.isclose(g12, 1200 * math.log(1.01), rel_tol=1e-9)
    assert math.isnan(s12) or s12 < -20  # constant changes: (near) zero deviation


def test_parse_factors_stops_at_annual_and_cut() -> None:
    text = (
        "junk\n,Mkt-RF,SMB,HML,RF\n202509,1.0,0,0,0.3\n202510,2.0,0,0,0.3\n"
        "202511,3.0,0,0,0.3\n Annual Factors\n2025,9,0,0,1\n"
    )
    m = w.parse_factors(text)
    assert m == {w.mi(2025, 9): 1.0, w.mi(2025, 10): 2.0}


def test_fit_recovers_slope_and_shift() -> None:
    rng = np.random.default_rng(0)
    months = range(1000, 1400)
    dose = {v: float(rng.normal()) for v in range(900, 1400)}
    rows = {v: (2.0 * dose[v] + float(rng.normal()) * 0.1, {}) for v in months}
    spec = w.Spec(ctrl=(), first=1000, last=1399)
    b, t, n = w.fit(rows, dose, spec)
    assert n == 400 and abs(b - 2.0) < 0.05 and t > 20
    b2, _, _ = w.fit(rows, dose, spec, shift=30)
    assert abs(b2) < 0.5


def test_rank_and_pass_rules() -> None:
    assert w.rank_high(2.5, [1.0, 3.0]) == 2
    assert w.passes(1.0, 2.1, 1, 2)
    assert not w.passes(1.0, 2.1, 1, 3)
    assert w.passes(1.0, 2.1, 2, None)
    assert not w.passes(-1.0, 2.1, 1, 1)
    assert not w.passes(1.0, 1.9, 1, 1)


def test_dose_ignores_vintages_after_v() -> None:
    # 12 years of vintages with noisy revisions; perturbing vintages after v leaves D(v) alone
    rng = np.random.default_rng(1)
    start, end = w.mi(1980, 1), w.mi(1993, 1)
    base = {j: 100.0 * 1.002 ** (j - start) for j in range(start - 24, end)}
    vs: w.Vintages = {}
    for v in range(start, end):
        vs[v] = {j: base[j] * (1 + 0.001 * float(rng.normal())) for j in range(start - 24, v)}
    d0 = w.dose_series(vs)
    v = max(d0) - 5
    later = {u: {j: x * (1 + 0.01 * float(rng.normal())) for j, x in vs[u].items()} for u in vs}
    vs2 = {u: (later[u] if u > v else vs[u]) for u in vs}
    d1 = w.dose_series(vs2)
    assert all(math.isclose(d0[u], d1[u]) for u in d0 if u <= v)
    assert any(not math.isclose(d0[u], d1[u]) for u in d0 if u > v)
    assert w.controls(vs, v) == w.controls(vs2, v)
