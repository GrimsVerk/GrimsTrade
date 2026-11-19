"""The wide-12 functions compute what research/wide-12.md step 2 says they do."""

from __future__ import annotations

import importlib
import io
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide12_events")
    finally:
        sys.path.remove(str(LIB))


def _closes(bars: dict[date, float]) -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide11_events").Closes(bars)
    finally:
        sys.path.remove(str(LIB))


XML = b"""<?xml version="1.0"?>
<m:DataSet xmlns:m="urn:x" xmlns:k="urn:k">
 <k:Series SERIES_NAME="OTHER.WW"><k:Obs TIME_PERIOD="2020-01-01" OBS_VALUE="9"/></k:Series>
 <k:Series SERIES_NAME="RESH4FG_N.WW">
  <k:Annotations/>
  <k:Obs TIME_PERIOD="2020-01-01" OBS_VALUE="100"/>
  <k:Obs TIME_PERIOD="2020-01-08" OBS_VALUE="ND"/>
  <k:Obs TIME_PERIOD="2020-01-29" OBS_VALUE="110"/>
  <k:Obs TIME_PERIOD="2020-02-05" OBS_VALUE="120"/>
 </k:Series>
</m:DataSet>"""


def test_read_series_picks_the_named_series_skips_bad_and_late_values() -> None:
    ev = _ev()
    got = ev.read_series(io.BytesIO(XML), "RESH4FG_N.WW", date(2020, 1, 31))
    assert got == {date(2020, 1, 1): 100.0, date(2020, 1, 29): 110.0}


def test_flow_is_the_log_change_over_exactly_28_days() -> None:
    ev = _ev()
    lv = {date(2020, 1, 1): 100.0, date(2020, 1, 29): 110.0, date(2020, 2, 5): 120.0}
    f = ev.flows(lv)
    assert f == {date(2020, 1, 29): math.log(1.1)}


def test_outcome_enters_monday_after_release_and_never_sees_later_bars() -> None:
    ev = _ev()
    w = date(2020, 1, 1)  # a Wednesday
    bars = {w + timedelta(days=i): 100.0 + i for i in range(0, 60)}
    px = _closes(bars)
    y = ev.outcome(px, w, 33, date(2030, 1, 1))
    assert math.isclose(y, math.log(133.0 / 105.0))
    # exit after the last train bar: dropped
    assert math.isnan(ev.outcome(px, w, 33, w + timedelta(days=30)))
    # exit bar too late (gap of more than a week): dropped
    gap = {
        d: v for d, v in bars.items() if not (w + timedelta(days=30) <= d <= w + timedelta(days=41))
    }
    assert math.isnan(ev.outcome(_closes(gap), w, 33, date(2030, 1, 1)))


def _xlsx(cells: list[list[str]]) -> io.BytesIO:
    import zipfile

    strings: list[str] = []
    rows = []
    for i, r in enumerate(cells, start=1):
        cs = []
        for j, v in enumerate(r):
            ref = f"{chr(65 + j)}{i}"
            if v == "":
                continue
            try:
                float(v)
                cs.append(f'<c r="{ref}"><v>{v}</v></c>')
            except ValueError:
                strings.append(v)
                cs.append(f'<c r="{ref}" t="s"><v>{len(strings) - 1}</v></c>')
        rows.append(f'<row r="{i}">{"".join(cs)}</row>')
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    rns = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(
            "xl/workbook.xml",
            f'<workbook {ns} {rns}><sheets><sheet name="A" sheetId="1" r:id="rId1"/>'
            f'<sheet name="CPI10" sheetId="2" r:id="rId2"/></sheets></workbook>',
        )
        rel = "http://schemas.openxmlformats.org/package/2006/relationships"
        z.writestr(
            "xl/_rels/workbook.xml.rels",
            f'<Relationships xmlns="{rel}"><Relationship Id="rId1" Target="worksheets/sheet1.xml"/>'
            f'<Relationship Id="rId2" Target="worksheets/sheet2.xml"/></Relationships>',
        )
        sst = "".join(f"<si><t>{s}</t></si>" for s in strings)
        z.writestr("xl/sharedStrings.xml", f"<sst {ns}>{sst}</sst>")
        z.writestr("xl/worksheets/sheet1.xml", f"<worksheet {ns}><sheetData/></worksheet>")
        z.writestr(
            "xl/worksheets/sheet2.xml",
            f"<worksheet {ns}><sheetData>{''.join(rows)}</sheetData></worksheet>",
        )
    buf.seek(0)
    return buf


def test_xlsx_reader_finds_the_sheet_and_the_column_by_label() -> None:
    ev = _ev()
    book = _xlsx(
        [
            ["Title"],
            ["Survey_Date(T)", "CPI10_P25_D1", "CPI10_D1"],
            ["1991Q4", "3.0", "0.5"],
            ["1992Q1", "#N/A", "#N/A"],
            ["1992Q2", "2.9", "0.75"],
        ]
    )
    rows = ev.read_xlsx_sheet(book, "CPI10")
    col = ev.quarter_column(rows, "CPI10_D1")
    assert col == {1991 * 4 + 3: 0.5, 1992 * 4 + 1: 0.75}


def test_quarterly_z_uses_only_earlier_surveys() -> None:
    ev = _ev()
    d = {q: float(q % 3) for q in range(100, 130)}
    z = ev.zscores_q(d)
    assert min(z) == 120  # needs 20 earlier surveys
    w = [d[p] for p in range(100, 125)]
    m = sum(w) / len(w)
    sd = math.sqrt(sum((x - m) ** 2 for x in w) / (len(w) - 1))
    assert math.isclose(z[125], (d[125] - m) / sd)
    d2 = dict(d)
    d2[129] = 99.0  # a later value must not change an earlier z
    assert ev.zscores_q(d2)[125] == z[125]


def test_quarterly_outcome_enters_after_release_and_holds_three_months() -> None:
    ev = _ev()
    q = 2020 * 4 + 3  # 2020Q4: entry 1 Dec 2020, exit 1 Mar 2021
    assert ev.entry_target(q) == date(2020, 12, 1)
    start = date(2020, 11, 1)
    bars = {start + timedelta(days=i): 100.0 + i for i in range(0, 200)}
    px = _closes(bars)
    y = ev.outcome_q(px, q, date(2030, 1, 1))
    a = (date(2020, 12, 1) - start).days
    b = (date(2021, 3, 1) - start).days
    assert math.isclose(y, math.log((100.0 + b) / (100.0 + a)))
    assert math.isnan(ev.outcome_q(px, q, date(2021, 2, 1)))
    assert len(ev.SHIFTS_W24) == 40 and all(k % 4 for k in ev.SHIFTS_W24)
