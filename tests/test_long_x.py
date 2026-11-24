"""data-long-3 loader: parsing cuts at the held-out year, bond, FX and commodity derivations."""

from __future__ import annotations

import importlib.util
import sys
import zipfile
from datetime import date
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "long_x.py"


@pytest.fixture(scope="module")
def lx() -> ModuleType:
    spec = importlib.util.spec_from_file_location("long_x_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


ALFRED = """observation_date,DGS10_20251110
1962-01-02,4.06
1962-01-03,.
1962-01-04,4.03
2025-10-31,4.11
2025-11-03,4.17
2025-11-07,4.10
"""


def test_alfred_drops_missing_and_cuts_before_heldout(lx: ModuleType) -> None:
    s = lx.parse_alfred(ALFRED)
    assert s == [(date(1962, 1, 2), 4.06), (date(1962, 1, 4), 4.03), (date(2025, 10, 31), 4.11)]
    assert max(d for d, _ in s) <= lx.LAST < date(2025, 11, 11)


def test_alfred_rejects_bad_header_and_disorder(lx: ModuleType) -> None:
    with pytest.raises(ValueError):
        lx.parse_alfred("date,value\n2000-01-01,1\n")
    with pytest.raises(ValueError):
        lx.parse_alfred("observation_date,X\n2000-01-02,1\n2000-01-01,2\n")


def test_month_end_and_consecutive(lx: ModuleType) -> None:
    daily = [(date(2000, 1, 3), 1.0), (date(2000, 1, 31), 2.0), (date(2000, 2, 28), 3.0)]
    assert lx.month_end(daily) == [(date(2000, 1, 1), 2.0), (date(2000, 2, 1), 3.0)]
    s = [(date(2000, 1, 1), 1.0), (date(2000, 3, 1), 2.0), (date(2000, 4, 1), 3.0)]
    assert lx.consecutive(s) == s[1:]


def test_par_price_textbook(lx: ModuleType) -> None:
    # 10y 5% semiannual bond at a 6% yield: 92.56 per 100 (integer periods, textbook value)
    v = 1.03**-20
    assert lx.par_price(0.05, 0.06, 10.0) == pytest.approx(0.025 / 0.03 * (1 - v) + v)
    assert lx.par_price(0.05, 0.06, 10.0) == pytest.approx(0.92561, abs=1e-5)
    # a par bond stays at par at its own yield, whatever maturity is left
    assert lx.par_price(0.05, 0.05, 7.3) == pytest.approx(1.0)


def test_bond_step_carry_rise_and_duration_check(lx: ModuleType) -> None:
    assert lx.bond_step(5.0, 5.0, 10.0, 1 / 12) == pytest.approx(0.05 / 12)
    up = lx.bond_step(5.0, 5.25, 10.0, 1 / 12)
    assert up < 0
    # a 25 bp rise on a 10y par bond loses about duration (7.8) x 0.25% = 1.95%, plus carry
    assert up == pytest.approx(0.05 / 12 - 0.0195, abs=0.001)
    assert lx.bond_step_duration(5.0, 5.25, 10.0, 1 / 12) == pytest.approx(up, abs=2e-4)


def test_bond_returns_daily_dt_and_monthly_gap(lx: ModuleType) -> None:
    ys = [(date(2000, 1, 3), 6.0), (date(2000, 1, 4), 6.0), (date(2000, 1, 7), 6.0)]
    r = lx.bond_returns(ys, 10.0)
    assert [d for d, _ in r] == [date(2000, 1, 4), date(2000, 1, 7)]
    assert r[1][1] == pytest.approx(0.06 * 3 / 365)
    with pytest.raises(ValueError):
        lx.bond_returns([(date(2000, 1, 1), 6.0), (date(2000, 3, 1), 6.0)], 10.0, monthly=True)


def test_fx_quote_splice_and_excess(lx: ModuleType) -> None:
    jpy = lx.usd_per_unit([(date(2000, 1, 3), 100.0)], per_usd=True)
    assert jpy == [(date(2000, 1, 3), 0.01)]
    dem = [(date(1998, 12, 31), 0.6), (date(1999, 1, 4), 0.61)]
    eur = [(date(1999, 1, 4), 1.18)]
    line = lx.splice_eur(dem, eur)
    assert line == [(date(1998, 12, 31), pytest.approx(0.6 * 1.95583)), (date(1999, 1, 4), 1.18)]
    spot = [(date(2000, 1, 1), 1.00), (date(2000, 2, 1), 1.01), (date(2000, 4, 1), 1.02)]
    i_f = [(date(2000, 1, 1), 6.0), (date(2000, 2, 1), 6.0)]
    i_us = [(date(2000, 1, 1), 3.0), (date(2000, 2, 1), 3.0)]
    out = lx.fx_excess_monthly(spot, i_f, i_us)
    assert len(out) == 1  # the Feb -> Apr step skips a month and is dropped
    m, s, x = out[0]
    assert m == date(2000, 2, 1)
    assert s == pytest.approx(0.01)
    assert x == pytest.approx(1.01 * 1.005 / 1.0025 - 1)


def test_first_available_priority(lx: ModuleType) -> None:
    a = [(date(2000, 2, 1), 1.0)]
    b = [(date(2000, 1, 1), 9.0), (date(2000, 2, 1), 9.0)]
    assert lx.first_available(a, b) == [(date(2000, 1, 1), 9.0), (date(2000, 2, 1), 1.0)]


def test_available_dates(lx: ModuleType) -> None:
    assert lx.available("h15-daily", date(2025, 10, 31)) == date(2025, 11, 3)  # Fri -> Mon
    assert lx.available("h10-daily", date(2025, 10, 29)) == date(2025, 11, 3)  # next Monday
    assert lx.available("h10-daily", date(2025, 11, 3)) == date(2025, 11, 10)
    assert lx.available("h15-monthly", date(2025, 9, 1)) == date(2025, 10, 1)
    assert lx.available("pink-sheet", date(2025, 9, 1)) == date(2025, 10, 6)
    assert lx.available("oecd-monthly", date(2025, 7, 1)) == date(2025, 10, 1)
    with pytest.raises(ValueError):
        lx.available("nope", date(2025, 1, 1))


def _xlsx(path: Path, rows: list[list[str | float]]) -> None:
    strings: list[str] = []
    xml_rows = []
    for i, row in enumerate(rows, start=1):
        cells = []
        for j, v in enumerate(row):
            ref = f"{chr(65 + j)}{i}"
            if isinstance(v, str):
                if v not in strings:
                    strings.append(v)
                cells.append(f'<c r="{ref}" t="s"><v>{strings.index(v)}</v></c>')
            else:
                cells.append(f'<c r="{ref}"><v>{v}</v></c>')
        xml_rows.append(f'<row r="{i}">{"".join(cells)}</row>')
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    rns = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    sst = "".join(f"<si><t>{s}</t></si>" for s in strings)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(
            "xl/workbook.xml",
            f'<workbook {ns} {rns}><sheets><sheet name="Monthly Prices" sheetId="1" '
            'r:id="rId1"/></sheets></workbook>',
        )
        z.writestr(
            "xl/_rels/workbook.xml.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Target="worksheets/sheet1.xml" Type="x"/></Relationships>',
        )
        z.writestr("xl/sharedStrings.xml", f"<sst {ns}>{sst}</sst>")
        z.writestr("xl/worksheets/sheet1.xml", f"<worksheet {ns}><sheetData>{''.join(xml_rows)}"
                   "</sheetData></worksheet>")  # fmt: skip


def test_pink_sheet_from_xlsx(lx: ModuleType, tmp_path: Path) -> None:
    p = tmp_path / "cmo.xlsx"
    _xlsx(
        p,
        [
            ["World Bank Commodity Price Data (The Pink Sheet)"],
            ["", "Crude oil, average", "Wheat, US HRW", "Gold"],
            ["", "($/bbl)", "($/mt)", "($/troy oz)"],
            ["1960M01", 1.63, "…", 35.27],
            ["1960M02", 1.63, 60.0, 35.27],
            ["2025M10", 63.0, 220.0, 4000.0],
            ["2025M11", 60.0, 210.0, 4100.0],
        ],
    )
    rows = lx.xlsx_rows(p, "Monthly Prices")
    assert rows[1][1] == "Crude oil, average"
    px = lx.parse_pink(rows)
    assert set(px) == {"Crude oil, average", "Wheat, US HRW", "Gold"}
    assert px["Wheat, US HRW"][0] == (date(1960, 2, 1), 60.0)  # "…" is missing, not zero
    assert px["Gold"][-1] == (date(2025, 10, 1), 4000.0)  # 2025M11 is held-out: cut


def test_yahoo_adjclose_cuts(lx: ModuleType) -> None:
    obj = {
        "chart": {
            "result": [
                {
                    "meta": {"regularMarketPrice": 999.0},
                    "timestamp": [1761921000, 1762525800],  # 2025-10-31, 2025-11-07 (UTC)
                    "indicators": {"adjclose": [{"adjclose": [10.0, 11.0]}]},
                }
            ]
        }
    }
    assert lx.yahoo_adjclose(obj) == [(date(2025, 10, 31), 10.0)]


def test_stats_and_drawdown(lx: ModuleType) -> None:
    a = [0.01, -0.02, 0.03, 0.00]
    st = lx.stats_pair(a, a, 12)
    assert st["corr"] == pytest.approx(1.0)
    assert st["te"] == pytest.approx(0.0)
    assert st["gap"] == pytest.approx(0.0)
    assert lx.max_drawdown([0.10, -0.50, 0.20]) == pytest.approx(0.5)
