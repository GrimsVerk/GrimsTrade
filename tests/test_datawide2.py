"""The data-wide-2 loaders read what the sources publish, and the episode counts are right."""
# ruff: noqa: E501  (literal sample rows from the sources, kept verbatim)

from __future__ import annotations

import importlib
import json
import math
import sys
import zipfile
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _dw() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("datawide2")
    finally:
        sys.path.remove(str(LIB))


IMM = """NewID,Name,Year,Month,OldID,ISO,SIC,Industry,Type,Currency,CapitalNumShare/AmntOutstanding,CapitalAmntShare,CapitalPar,CapitalPaid,PriceMonthOpen,PriceMonthHigh,PriceMonthLow,PriceMonthLate,YieldInvt,DvdValue,Redeemable,AmntLoanUnredeemed
10001,Venezuela 1.50% Bond,1869,1,10001,VEN,,1,Government Bond,GBP,1382350,Stock,100,,,7,5.5,6.25,,,,
10001,Venezuela 1.50% Bond,1869,2,10001,VEN,,1,Government Bond,GBP,1382350,Stock,100,,,,,6,,,,
10001,Venezuela 1.50% Bond,1869,4,10001,VEN,,1,Government Bond,GBP,1382350,Stock,100,,,6.5,5.5,7,,,,
10002,Venezuela 3% Bond,1869,1,10002,VEN,,1,Government Bond,GBP,1,Stock,100,,,,,50,,,,
10002,Venezuela 3% Bond,1869,2,10002,VEN,,1,Government Bond,GBP,1,Stock,100,,,,,40,,,,
10003,Venezuela local,1869,1,10003,VEN,,1,Government Bond,VEB,1,Stock,100,,,,,10,,,,
10003,Venezuela local,1869,2,10003,VEN,,1,Government Bond,VEB,1,Stock,100,,,,,1,,,,
20001,Some Mine,1869,1,20001,ZAF,,1,Common Stock,GBP,1,5,5,5,,,,2,,,,
"""


def test_imm_country_index_chains_the_median_of_sterling_moves() -> None:
    import csv
    import io

    dw = _dw()
    rows = list(csv.DictReader(io.StringIO(IMM)))
    (ven,) = dw.parse_imm_rows(rows, "Government Bond")
    # Feb 1869: moves ln(6/6.25) and ln(40/50); median of two = their mean. April has no
    # March price, so no pair: no point. The local-currency bond is left out.
    assert ven.market == "VEN" and ven.asset == "bond"
    assert ven.months == [dw.ym(1869, 2)]
    want = 100 * math.exp((math.log(6 / 6.25) + math.log(40 / 50)) / 2)
    assert math.isclose(ven.level[0], want)
    assert ven.extra == {"securities": 2, "pairs": 2}
    assert dw.parse_imm_rows(rows, "Government Bond", min_pairs=3)[0].months == []
    assert len(dw.parse_imm_rows(rows, "Government Bond", currency=None)[0].level) == 1


def test_falls_counts_one_episode_per_peak_and_open_falls() -> None:
    dw = _dw()
    lv = [100, 80, 70, 90, 101, 120, 60, 65]
    out = dw.falls(list(range(len(lv))), lv)
    assert [(p, t) for p, t, _ in out] == [(0, 2), (5, 6)]
    assert math.isclose(out[0][2], 0.30) and math.isclose(out[1][2], 0.50)
    assert dw.falls([0, 1, 2], [100, 80, 100]) == []  # 20% is below the threshold


def test_dbnomics_parser_inverts_and_maps_codes() -> None:
    dw = _dw()
    text = json.dumps(
        {
            "series": [
                {
                    "series_code": "M.IN.ENDA_XDC_USD_RATE",
                    "provider": "IMF",
                    "dataset": "IFS",
                    "period": ["1966-05", "1966-06", "2025-11"],
                    "value": [4.76, 7.5, "NA"],
                }
            ]
        }
    )
    (s,) = dw.parse_dbnomics(text, "fx", invert=True, iso2=True)
    assert s.market == "IND" and s.months == [dw.ym(1966, 5), dw.ym(1966, 6)]
    assert math.isclose(s.level[1], 1 / 7.5)
    # the 1966 rupee devaluation is a fall of 36.5% for a holder in USD
    assert len(dw.falls(s.months, s.level)) == 1


def test_labelled_columns_yields_and_the_cut() -> None:
    dw = _dw()
    rows = [
        ["Year", "GOV"],
        ["1820:05", 7.5],
        ["1820:06", "."],
        ["1924 01", "4.0"],
        ["2025-11-30", 3.0],
        [None, 1],
    ]
    pts = dw.parse_labelled_columns(rows, 1)
    assert pts == [(dw.ym(1820, 5), 7.5), (dw.ym(1924, 1), 4.0), (dw.ym(2025, 11), 3.0)]
    s = dw.from_points("x", "bond", "NOR", dw.yields_to_price(pts))
    assert s.months[-1] == dw.ym(1924, 1)  # 2025-11 is held out
    assert math.isclose(s.level[0], 100 / 7.5)
    assert dw.find_col(rows, "GOV") == 1


def test_yale_files() -> None:
    dw = _dw()
    nyse = dw.parse_yale_nyse(
        '"","2015 Index Returns","2020 Index Returns"\n"Feb-1815",-0.02,-0.1\n"Mar-1815",0.0,0.5\n'
    )
    assert nyse.months == [dw.ym(1815, 2), dw.ym(1815, 3)] and math.isclose(nyse.level[1], 135.0)
    _, spse = dw.parse_spse_nyse(
        [["month", "NYSE", "SPSE"], [23743.0, 100.0, 100.0], [23774.0, 100.4, 99.5]]
    )
    assert spse.market == "RUS" and spse.months == [dw.ym(1865, 1), dw.ym(1865, 2)]


def test_read_xlsx_rows_without_openpyxl(tmp_path: Path) -> None:
    dw = _dw()
    p = tmp_path / "t.xlsx"
    m = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    r = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    with zipfile.ZipFile(p, "w") as z:
        z.writestr(
            "xl/workbook.xml",
            f'<workbook {m} {r}><sheets><sheet name="Front" sheetId="1" r:id="rId1"/><sheet name="Data" sheetId="2" r:id="rId2"/></sheets></workbook>',
        )
        z.writestr(
            "xl/_rels/workbook.xml.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Target="worksheets/sheet2.xml"/></Relationships>',
        )
        z.writestr(
            "xl/sharedStrings.xml", f"<sst {m}><si><t>Month</t></si><si><t>1914:01</t></si></sst>"
        )
        z.writestr("xl/worksheets/sheet1.xml", f"<worksheet {m}><sheetData/></worksheet>")
        z.writestr(
            "xl/worksheets/sheet2.xml",
            f'<worksheet {m}><sheetData><row r="1"><c r="A1" t="s"><v>0</v></c></row>'
            f'<row r="2"><c r="A2" t="s"><v>1</v></c><c r="C2"><v>131.5</v></c></row></sheetData></worksheet>',
        )
    rows = dw.read_xlsx_rows(p, "Data")
    assert rows == [["Month"], ["1914:01", None, 131.5]]
    assert dw.parse_labelled_columns(rows, 2) == [(dw.ym(1914, 1), 131.5)]


def test_new_years_respect_the_scored_coverage() -> None:
    dw = _dw()
    months = [dw.ym(y, mo) for y in (1865, 1866, 1867) for mo in range(1, 13)]
    lv = [100.0] * 12 + [60.0] * 12 + [100.0] * 12
    c = dw.count_new(dw.Monthly("uk", "stock", "GBR", months, lv))
    # 1867 is scored (NBER GB shares); 1865-66 are new and no scored stock series covers them
    assert (c.new_years, c.new_calendar_years, c.falls_new, c.falls_all) == (2, 2, 1, 1)
    assert dw.seen("fx", "JPN", 1971) and not dw.seen("fx", "IND", 1990)
