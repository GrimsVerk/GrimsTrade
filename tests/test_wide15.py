"""The wide-15 functions compute what research/wide-15.md steps 3 and 4 say they do."""

from __future__ import annotations

import importlib
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide15_events")
    finally:
        sys.path.remove(str(LIB))


def test_early_shifts_are_forty_earlier_odd_weeks_never_a_year() -> None:
    s = _ev().SHIFTS_EARLY
    assert len(s) == 40 and len(set(s)) == 40
    assert all(27 <= k <= 105 and k % 2 == 1 for k in s)  # earlier doses only (k > 0)


def test_friday_of_uses_saturday_to_friday_weeks() -> None:
    ev = _ev()
    assert ev.friday_of(date(2026, 11, 20)) == date(2026, 11, 20)  # Friday itself
    assert ev.friday_of(date(2026, 11, 21)) == date(2026, 11, 27)  # Saturday: next week
    assert ev.friday_of(date(2026, 11, 16)) == date(2026, 11, 20)  # Monday


def test_parse_rollcalls_cuts_after_last_and_skips_bad_dates() -> None:
    ev = _ev()
    text = (
        "congress,chamber,rollnumber,date,yea_count,nay_count\n"
        "119,House,1,2025-11-07,200,210\n"
        "119,Senate,2,2025-11-12,50,50\n"  # after last: never read
        "119,House,3,,1,1\n"  # no date
        "119,Senate,4,2025-11-03,,\n"  # missing counts read as 0
    )
    rows = ev.parse_rollcalls(text, last=date(2025, 11, 10))
    assert rows == [(date(2025, 11, 7), "House", 200, 210), (date(2025, 11, 3), "Senate", 0, 0)]


def test_weekly_counts_chambers_and_close_votes() -> None:
    ev = _ev()
    f = date(2025, 11, 7)
    weeks = [f, f + timedelta(days=7)]
    rolls = [
        (f, "House", 200, 210),  # margin 10/410: close
        (f - timedelta(days=6), "Senate", 90, 10),  # Saturday before: same week, not close
        (f + timedelta(days=1), "House", 1, 0),  # Saturday after: next week
    ]
    assert ev.weekly_counts(rolls, weeks) == {f: 2, weeks[1]: 1}
    assert ev.weekly_counts(rolls, weeks, chamber="Senate") == {f: 1, weeks[1]: 0}
    assert ev.weekly_counts(rolls, weeks, close_only=True) == {f: 1, weeks[1]: 0}


def test_workload_dose_and_earlier_shift() -> None:
    ev = _ev()
    f = date(2025, 11, 7)
    dose = ev.workload_dose({f: 0, f - timedelta(days=7 * 27): 10})
    assert dose[f] == (2 * math.sqrt(0.375), 0.0)
    assert ev.shifted_pair(dose, f, 27) == (2 * math.sqrt(10.375), 1.0)
    x, s = ev.shifted_pair(dose, f, 29)
    assert math.isnan(x) and math.isnan(s)


def test_refund_pages_sum_individual_rows_only_and_cut_after_last() -> None:
    ev = _ev()
    page = json.dumps(
        {
            "data": [
                {"record_date": "2024-03-01", "tax_refund_type": "Taxes - Individual Tax "
                 "Refunds (EFT)", "tax_refund_today_amt": "1202"},
                {"record_date": "2024-03-01", "tax_refund_type": "Taxes - Individual Tax "
                 "Refunds (Checks)", "tax_refund_today_amt": "839"},
                {"record_date": "2024-03-01", "tax_refund_type": "Taxes - Business Tax "
                 "Refunds (EFT)", "tax_refund_today_amt": "21"},
                {"record_date": "2006-03-01", "tax_refund_type": "Individual",
                 "tax_refund_today_amt": "66"},
                {"record_date": "2025-11-12", "tax_refund_type": "Individual",
                 "tax_refund_today_amt": "999"},
                {"record_date": "2006-03-02", "tax_refund_type": "Individual",
                 "tax_refund_today_amt": "null"},
            ]
        }
    )  # fmt: skip
    d = ev.parse_refund_pages([page], last=date(2025, 11, 10))
    assert d == {date(2024, 3, 1): 2041.0, date(2006, 3, 1): 66.0}


def test_year_totals_need_full_years() -> None:
    ev = _ev()
    daily = {date(2005, 10, 3) + timedelta(days=i): 1.0 for i in range(365 * 3)}
    t = ev.year_totals(daily)  # data 2005-10-03 .. 2008-10-01
    assert sorted(t) == [2006, 2007]
    assert t[2006] == 365.0


def test_refund_surprise_against_median_of_same_iso_week() -> None:
    ev = _ev()
    # Fridays of ISO week 10 in 2021..2024, and one week-53 Friday (2020-12-31 is in ISO 2020-W53).
    wk = {
        date(2021, 3, 12): 10.0,
        date(2022, 3, 11): 30.0,
        date(2023, 3, 10): 20.0,
        date(2024, 3, 8): 50.0,
        date(2021, 1, 1): 5.0,
    }
    assert all(f.isocalendar()[1] == 10 for f in list(wk)[:4])
    totals = {2020: 1000.0, 2021: 1000.0, 2022: 1000.0, 2023: 2000.0}
    s = ev.refund_surprise(wk, totals)
    assert math.isclose(s[date(2024, 3, 8)], 100 * (50 - 20) / 2000)  # median of 10, 30, 20
    assert math.isclose(s[date(2023, 3, 10)], 100 * (20 - 20) / 1000)  # median of 10, 30
    assert date(2022, 3, 11) not in s  # only one earlier year
    assert date(2021, 1, 1) not in s  # ISO week 53


def test_kernel_weights_are_the_gamma2_mass_in_the_window() -> None:
    ev = _ev()
    w = ev.kernel_weights()
    assert len(w) == 8

    def cdf(x: float) -> float:
        return 1 - (1 + x) * math.exp(-x)

    assert math.isclose(w[0], cdf(33 / 7) - cdf(5 / 7))
    assert all(a > b > 0 for a, b in zip(w[1:], w[2:], strict=False))  # decays after the peak
    assert 0.5 < w[0] < 0.9 and sum(w) < 2.0


def test_runoff_needs_every_lag_and_weights_them() -> None:
    ev = _ev()
    f = date(2024, 3, 8)
    weeks = [f - timedelta(days=7 * i) for i in range(10)]
    d = {x: 0.0 for x in weeks}
    d[f - timedelta(days=14)] = 1.0  # a unit surprise two weeks earlier
    u = ev.runoff(d, [f, weeks[-1]])
    assert math.isclose(u[f], ev.kernel_weights()[2])
    assert weeks[-1] not in u  # its earlier lags are missing
