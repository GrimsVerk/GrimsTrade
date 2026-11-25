"""data-long-4 loader: BIS, French and JST parsers cut at the held-out year; dividend yield."""

from __future__ import annotations

import importlib.util
import math
import sys
import zipfile
from datetime import date
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "long_macro.py"


@pytest.fixture(scope="module")
def lm() -> ModuleType:
    spec = importlib.util.spec_from_file_location("long_macro_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


HEAD = "FREQ,REF_AREA,UNIT_MEASURE,TIME_PERIOD,OBS_VALUE,OBS_STATUS\n"
BIS_M = HEAD + (
    "M,SE,628,1918-03,4.7,A\n"
    "M,SE,628,1918-04,NaN,M\n"
    "M,SE,628,1918-05,,M\n"
    "M,SE,628,2025-10,150.0,A\n"
    "M,SE,628,2025-11,151.0,A\n"
    "M,US,628,1913-01,9.8,A\n"
)


def test_bis_monthly_drops_missing_and_cuts_after_october_2025(lm: ModuleType) -> None:
    out = lm.parse_bis(BIS_M)
    assert out["SE"] == [(date(1918, 3, 1), 4.7), (date(2025, 10, 1), 150.0)]
    assert out["US"] == [(date(1913, 1, 1), 9.8)]


def test_bis_annual_drops_the_unfinished_year(lm: ModuleType) -> None:
    text = HEAD + "A,GB,628,1661,0.5,A\nA,GB,628,2024,150,A\nA,GB,628,2025,155,A\n"
    assert lm.parse_bis(text)["GB"] == [(date(1661, 1, 1), 0.5), (date(2024, 1, 1), 150.0)]


def test_bis_quarter_kept_only_when_it_ends_in_the_train_window(lm: ModuleType) -> None:
    text = HEAD + "Q,AU,628,2025-Q3,149,A\nQ,AU,628,2025-Q4,150,A\n"
    assert lm.parse_bis(text)["AU"] == [(date(2025, 7, 1), 149.0)]


def test_bis_refuses_two_series_for_one_area(lm: ModuleType) -> None:
    text = HEAD + "M,US,628,2000-01,1,A\nM,US,771,2000-01,2,A\n"
    with pytest.raises(ValueError, match="duplicate"):
        lm.parse_bis(text)


def test_quarter_ends_and_yoy(lm: ModuleType) -> None:
    s = [(date(2000, m, 1), 100.0) for m in (1, 2, 3)] + [(date(2001, 1, 1), 103.0)]
    assert lm.quarter_ends(s) == [(date(2000, 1, 1), 100.0), (date(2001, 1, 1), 103.0)]
    ((d, v),) = lm.yoy(s)
    assert d == date(2001, 1, 1) and v == pytest.approx(3.0)


COLS = "          Mkt   High    Low   High    Low   High    Low   High    Low   Zero\n"
FRENCH = (
    "\n     Value-Weight Dollar Returns      All 4 Data Items Not Reqd\n"
    "                -- BE/ME --   --- E/P ---   --- CE/P --   ------  Yld  -----\n"
    + COLS
    + "202509   1.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00 -99.99\n"
    "\n     Value-Weight Local  Returns      All 4 Data Items Not Reqd\n"
    "                -- BE/ME --   --- E/P ---   --- CE/P --   ------  Yld  -----\n"
    + COLS
    + "202509   2.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00 -99.99\n"
    "202510   3.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00   4.00\n"
    "202511   9.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00   4.00\n"
    "\n     Value-Weight Local  Returns      All 4 Data Items Not Reqd\n"
    "              -- BE/ME --   --- E/P ---   --- CE/P --   ------  Yld  -----\n"
    "        Mkt   High    Low   High    Low   High    Low   High    Low   Zero\n"
    "2025  20.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00   1.00\n"
    "\nAverage of Annual Value-Weight Averages\n(Annual Sum of Num / Annual Sum of Den)\n"
    "All 4 Data Items Not Reqd\nRatios x 100   Firms is number in B/M\n\n"
    "     Firms    B/M    E/P   CE/P    Yld\n"
    "2024   100  60.00   6.00  12.00   2.50\n"
    "2025   101  61.00   6.10  12.10   2.40\n"
    "2026   102  62.00   6.20  12.20 -99.99\n"
    "\nAverage of Annual Value-Weight Averages\n(Annual Sum of Num / Annual Sum of Den)\n"
    "All 4 Data Items Required\nRatios x 100\n\n"
    "     Firms    B/M    E/P   CE/P    Yld\n"
    "2024    90  70.00   7.00  13.00   3.00\n"
    "\nCopyright 2026 Kenneth R. French\n"
)


def test_french_country_blocks_missing_values_and_cut(lm: ModuleType) -> None:
    out = lm.parse_french_country(FRENCH)
    m = out["monthly"]
    local = m[("Local", "Not Reqd")]
    assert local["Mkt"] == [(date(2025, 9, 1), 2.0), (date(2025, 10, 1), 3.0)]  # Nov cut
    assert local["Yld Zero"] == [(date(2025, 10, 1), 4.0)]  # -99.99 dropped
    assert m[("Dollar", "Not Reqd")]["Mkt"] == [(date(2025, 9, 1), 1.0)]
    assert len(m) == 2  # the annual return block is not read as monthly
    r = out["annual_ratios"]
    assert r["Not Reqd"]["Yld"] == [(date(2024, 1, 1), 2.5), (date(2025, 1, 1), 2.4)]
    assert r["Required"]["E/P"] == [(date(2024, 1, 1), 7.0)]


def test_read_french_zip_maps_file_names(lm: ModuleType, tmp_path: Path) -> None:
    p = tmp_path / "f.zip"
    with zipfile.ZipFile(p, "w") as z:
        z.writestr("Swtzrlnd.Dat", FRENCH)
        z.writestr("readme.txt", "x")
    out = lm.read_french_zip(p)
    assert list(out) == ["CH"]


def _months(n: int, start: date = date(2000, 1, 1)) -> list[date]:
    out, d = [], start
    for _ in range(n):
        out.append(d)
        d = date(d.year + d.month // 12, d.month % 12 + 1, 1)
    return out


def test_dividend_yield_flat_price_constant_dividend(lm: ModuleType) -> None:
    ds = _months(14)
    without = [(d, 0.0) for d in ds]
    with_div = [(d, 0.25) for d in ds]
    dy = lm.dividend_yield(with_div, without)
    assert [d for d, _ in dy] == ds[11:]
    assert all(v == pytest.approx(3.0) for _, v in dy)


def test_dividend_yield_uses_the_price_at_the_end(lm: ModuleType) -> None:
    ds = _months(12)
    without = [(d, 0.0) for d in ds[:-1]] + [(ds[-1], 100.0)]  # price doubles in month 12
    with_div = [(d, 0.25) for d in ds[:-1]] + [(ds[-1], 100.25)]
    ((_, v),) = lm.dividend_yield(with_div, without)
    assert v == pytest.approx(1.5)


def test_dividend_yield_restarts_after_a_gap(lm: ModuleType) -> None:
    ds = _months(30)
    keep = ds[:5] + ds[6:]
    without = [(d, 0.0) for d in keep]
    with_div = [(d, 0.25) for d in keep]
    dy = lm.dividend_yield(with_div, without)
    assert dy[0][0] == ds[17]


def test_parse_jst_drops_na_and_years_from_2025(lm: ModuleType) -> None:
    rows = [
        ["year", "country", "iso", "cpi", "eq_dp"],
        ["1870", "Sweden", "SWE", "1.5", "NA"],
        ["1871", "Sweden", "SWE", "1.6", "0.05"],
        ["2025", "Sweden", "SWE", "9", "0.03"],
    ]
    out = lm.parse_jst(rows, ["cpi", "eq_dp"])
    assert out["cpi"]["SWE"] == [(date(1870, 1, 1), 1.5), (date(1871, 1, 1), 1.6)]
    assert out["eq_dp"]["SWE"] == [(date(1871, 1, 1), 0.05)]


def test_real_fx(lm: ModuleType) -> None:
    d0, d1 = date(2000, 1, 1), date(2000, 2, 1)
    s = lm.real_fx([(d0, 2.0), (d1, 2.0)], [(d0, 100.0), (d1, 110.0)], [(d0, 100.0)])
    assert s == [(d0, pytest.approx(math.log(2.0)))]


def test_available(lm: ModuleType) -> None:
    assert lm.available("cpi-monthly", date(2025, 9, 1)) == date(2025, 11, 1)
    assert lm.available("cpi-quarterly", date(2025, 7, 1)) == date(2025, 12, 1)
    assert lm.available("policy-monthly", date(2025, 10, 1)) == date(2025, 11, 1)
    assert lm.available("french-annual", date(2025, 1, 1)) == date(2025, 7, 1)
    assert lm.available("jst-annual", date(2020, 1, 1)) == date(2021, 7, 1)
    with pytest.raises(ValueError):
        lm.available("nope", date(2025, 1, 1))


def test_no_network_in_parser_module() -> None:
    src = PATH.read_text()
    assert "urllib" not in src and "requests" not in src


def test_known_monthly_quarterly_cpi_waits_for_publication(lm: ModuleType) -> None:
    # BIS AU style: each quarter's value repeated over its three months
    vals = {date(2025, 4, 1): 147.5, date(2025, 7, 1): 149.5}
    s = [(date(2025, m, 1), vals[date(2025, 4 if m < 7 else 7, 1)]) for m in range(4, 10)]
    known = dict(lm.known_monthly(lm.quarter_ends(s), "cpi-quarterly"))
    # Q2 (from 2025-04) is public from 2025-09-01: known at the end of 2025-08
    assert date(2025, 7, 1) not in known
    assert known[date(2025, 8, 1)] == 147.5
    # Q3 2025 would be public 2025-12-01: never inside the train window
    assert known[date(2025, 10, 1)] == 147.5
    assert max(known) == date(2025, 10, 1)


def test_real_fx_known_does_not_use_the_repeated_quarter(lm: ModuleType) -> None:
    months = [date(2025, m, 1) for m in range(1, 11)]
    q = {1: 100.0, 4: 110.0, 7: 121.0}
    au = [(d, q[(d.month - 1) // 3 * 3 + 1]) for d in months if d.month < 10]
    us = [(d, 100.0) for d in months]
    spot = [(d, 1.0) for d in months]
    rx = dict(lm.real_fx_known(spot, au, us, quarterly_foreign=True))
    # month 2025-07 must carry Q1 (public 2025-06-01), not Q3 (in the repeated months)
    assert rx[date(2025, 7, 1)] == pytest.approx(math.log(1.0))
    assert rx[date(2025, 10, 1)] == pytest.approx(math.log(1.1))  # Q2, public 2025-09-01
    naive = dict(lm.real_fx(spot, au, us))
    assert naive[date(2025, 7, 1)] == pytest.approx(math.log(1.21))  # the look-ahead trap
