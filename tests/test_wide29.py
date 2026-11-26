"""Offline tests for research/lib/wide29.py (W46 `ipo-heat`)."""

from __future__ import annotations

import io
import math
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "lib"))

import wide29 as w  # noqa: E402

SHEET = (
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
    '<row r="1"><c r="A1"><v>1</v></c><c r="B1"><v>60</v></c><c r="D1"><v>16</v></c></row>'
    '<row r="2"><c r="A2"><v>2</v></c><c r="B2"><v>5</v></c><c r="D2"><v>7</v></c>'
    '<c r="G2" t="s"><v>0</v></c></row>'
    '<row r="3"><c r="A3" t="s"><v>0</v></c></row>'
    "</sheetData></worksheet>"
)
STRINGS = (
    '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
    "<si><t>a note</t></si></sst>"
)


def _xlsx() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("xl/worksheets/sheet1.xml", SHEET)
        z.writestr("xl/sharedStrings.xml", STRINGS)
    return buf.getvalue()


def test_read_sheet_and_parse_ipo_dates_two_digit_years() -> None:
    rows = w.read_sheet(_xlsx())
    assert rows[1]["G"] == "a note"
    n = w.parse_ipo(rows)
    assert n == {w.mi(1960, 1): 16.0, w.mi(2005, 2): 7.0}


def test_heat_is_log_twelve_month_count_minus_past_mean() -> None:
    base = w.mi(1970, 1)
    n = {base + i: 1.0 for i in range(72)}
    n[base + 71] = 13.0  # last 12-month sum 24 instead of 12
    h = w.heat(n)
    assert set(h) == {base + 71}
    assert math.isclose(h[base + 71], math.log(25.0) - math.log(13.0))


def test_heat_needs_every_month() -> None:
    base = w.mi(1970, 1)
    n = {base + i: 1.0 for i in range(80) if i != 75}
    h = w.heat(n)
    assert all(not (75 <= m - base <= 75 + 11 + 60) for m in h)


def test_negative_sign_rank_and_pass() -> None:
    assert w.neg_rank(-3.0, [-1.0, 0.0, -2.5]) == 1
    assert w.neg_rank(-1.0, [-2.0, -3.0]) == 3
    assert w.passes_neg(-1.0, -2.5, 1, 2)
    assert not w.passes_neg(-1.0, -2.5, 3, 1)
    assert not w.passes_neg(1.0, -2.5, 1, 1)
    assert not w.passes_neg(-1.0, -1.5, 1, None)
