"""The parked-gates-1 functions compute what research/cards/parked-gates-1.md says they do."""

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
        return importlib.import_module("parkedgates1_events")
    finally:
        sys.path.remove(str(LIB))


def test_w33_shifts_are_forty_earlier_doses_only() -> None:
    s = _ev().SHIFTS_W33
    assert len(s) == 40 and len(set(s)) == 40
    assert min(s) == 25 and max(s) == 103 and all(k > 0 for k in s)


def test_parse_pdsi_reads_only_the_national_row_and_cuts_after_last() -> None:
    vals = " ".join(f"{v:6.2f}" for v in [1.0, -2.0, 3.0, 0, 0, 0, 0, 0, 0, 0, -99.99, 5.0])
    text = "\n".join(
        [
            "0010052025 " + vals,  # a state row: ignored
            "1100022025 " + vals,  # another element: ignored
            "1100052025 " + vals,
        ]
    )
    out = _ev().parse_pdsi(text, date(2025, 10, 31))
    assert out[2025 * 12] == 1.0 and out[2025 * 12 + 1] == -2.0
    assert 2025 * 12 + 10 not in out  # November: after the cut (and missing anyway)
    assert 2025 * 12 + 11 not in out  # December: after the cut
    assert len(out) == 10


def test_drought_dose_is_minus_pdsi_and_change_is_drying() -> None:
    ev = _ev()
    p = {10: 1.0, 11: 0.0, 12: -1.0, 13: -3.0}
    assert ev.drought_dose(p) == {10: -1.0, 11: -0.0, 12: 1.0, 13: 3.0}
    assert ev.drought_change(p) == {13: 4.0}


def test_parse_fred_keys_by_quarter_end_month_and_drops_late_quarters() -> None:
    text = "observation_date,X\n2025-01-01,10\n2025-04-01,.\n2025-07-01,30\n2025-10-01,40\n"
    out = _ev().parse_fred(text, date(2025, 10, 31))
    assert out == {2025 * 12 + 2: 10.0, 2025 * 12 + 8: 30.0}  # Q4 ends in December: cut


def test_susceptible_dose_needs_forty_earlier_quarters() -> None:
    ev = _ev()
    qs = [2 + 3 * i for i in range(42)]
    recv = {q: 1.0 for q in qs}
    mv = {q: 100.0 for q in qs}
    recv[qs[-1]] = math.e  # last ratio e times the baseline
    s = ev.susceptible_dose(recv, mv)
    assert set(s) == {qs[40], qs[41]}
    assert abs(s[qs[40]]) < 1e-12
    assert abs(s[qs[41]] - 1.0) < 1e-12


def test_monthly_known_uses_only_quarters_ended_lag_months_before() -> None:
    q = {2: 1.0, 5: 2.0}  # quarters ending in month 2 and month 5
    m = _ev().monthly_known(q, 3)
    assert min(m) == 5 and m[5] == 1.0 and m[7] == 1.0
    assert m[8] == 2.0 and max(m) == 10


def test_fall_is_min_of_return_and_zero() -> None:
    ev = _ev()
    assert ev.fall(0.03) == 0.0 and ev.fall(-0.04) == -0.04
    assert math.isnan(ev.fall(math.nan))
