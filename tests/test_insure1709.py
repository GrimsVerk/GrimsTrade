"""insure-1709-1: BoE loader, splice check, monthly rule timing, S bookkeeping and the nulls."""

from __future__ import annotations

import importlib.util
import math
import sys
import zipfile
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "insure1709.py"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    spec = importlib.util.spec_from_file_location("insure1709_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_csv_keeps_only_months_up_to_the_cut(m: ModuleType, tmp_path: Path) -> None:
    p = tmp_path / "monthly.csv"
    p.write_text(
        "period,year,month,variable_id,variable,section,unit,value\n"
        "1866-12,1866,12,a,A,s,u,2.5\n"
        "1867-01,1867,1,a,A,s,u,3.0\n"
        "1866-11,1866,11,a,A,s,u,\n"
        "1866-12,1866,12,b,B,s,u,9\n"
    )
    out = m.read_csv(p, ["a"])
    assert out == {"a": {m.ym(1866, 12): 2.5}}


def _xlsx(path: Path) -> None:
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    rel = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(
            "xl/workbook.xml",
            f'<workbook {ns} {rel}><sheets><sheet name="S 1" sheetId="1" r:id="rId1"/>'
            "</sheets></workbook>",
        )
        z.writestr(
            "xl/_rels/workbook.xml.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>',
        )
        z.writestr("xl/sharedStrings.xml", f"<sst {ns}><si><t>Jan</t></si><si><t>x</t></si></sst>")
        z.writestr(
            "xl/worksheets/sheet1.xml",
            f"<worksheet {ns}><sheetData>"
            '<row r="1"><c r="A1"><v>1709</v></c><c r="B1" t="s"><v>0</v></c>'
            '<c r="AA1"><v>1.5E-1</v></c><c r="C1" t="s"><v>1</v></c></row>'
            "</sheetData></worksheet>",
        )


def test_xlsx_reader_resolves_columns_and_shared_strings(m: ModuleType, tmp_path: Path) -> None:
    p = tmp_path / "w.xlsx"
    _xlsx(p)
    rows = m.xlsx_sheet(p, "S 1")
    assert rows == [{0: "1709", 1: "Jan", 26: "1.5E-1", 2: "x"}]
    assert m._col("AA7") == 26


def test_splice_month_finds_the_switch(m: ModuleType) -> None:
    ms = list(range(10))
    neal = {k: 1.0 + 0.1 * k for k in ms}
    ach = {k: 2.0 ** (k / 3) for k in ms}
    sp = {k: neal[k] for k in range(5)}
    for k in range(5, 10):
        sp[k] = sp[k - 1] * ach[k] / ach[k - 1]
    cols = {"spliced": sp, "Neal": neal, "Acheson cap-weighted": ach}
    first, last_neal, _ = m.splice_month(cols)
    assert (first, last_neal) == (5, 4)


def test_segments_split_at_missing_months(m: ModuleType) -> None:
    lev = {1: 1.0, 2: 1.0, 3: 1.0, 5: 1.0, 6: 1.0}
    assert m.segments(lev) == [[1, 2, 3], [5, 6]]


def test_acf_uses_pairs_exactly_lag_apart(m: ModuleType) -> None:
    ms = np.array([0, 1, 2, 3, 10, 11])
    x = np.array([1.0, -1.0, 1.0, -1.0, 1.0, -1.0])
    a, n = m.acf(ms, x, 1)
    assert n == 4  # (0,1), (1,2), (2,3), (10,11)
    assert a < -0.5


def test_signal_trades_the_next_month_and_lag_delays_it(m: ModuleType) -> None:
    n = 100
    r = np.full(n, 0.01)
    r[0] = np.nan
    r[50:] = -0.02  # falls from month 50 on
    months = list(range(n))
    s0 = m.build_seg("x", months, r, lag=0)
    s1 = m.build_seg("x", months, r, lag=1)
    assert s0 is not None and s1 is not None
    # first decision at month 12 (12 returns dated 1..12); position earns month 13
    assert s0.months[0] == 12 and s1.months[0] == 13
    # the first month-end whose 12-month log return is not above 0
    lr = np.log1p(r)
    off = [k for k in range(12, n) if lr[k - 11 : k + 1].sum() <= 0][0]
    i0 = s0.months.index(off + 1)
    assert s0.pos[i0] == 0.0 and s0.pos[i0 - 1] == 1.0
    i1 = s1.months.index(off + 2)
    assert s1.pos[i1] == 0.0 and s1.pos[i1 - 1] == 1.0


def test_book_matches_insure1_episode_shares(m: ModuleType) -> None:
    rng = np.random.default_rng(3)
    n = 400
    r = np.concatenate([[np.nan], np.expm1(rng.normal(0.0, 0.06, n - 1))])
    s = m.build_seg("x", list(range(n)), r)
    assert s is not None
    ev = m.evaluate("t", [s], n_rot=20)
    if ev.eps:
        assert abs(np.mean([e.share for e in ev.eps]) - ev.t.rule.s_mean[0]) < 1e-9
    # rotation by 0 reproduces the rule
    b = m.book([s], m.rotated([s], np.array([0])), [m.pairs_of(s.r)])
    assert np.allclose(b.s_eps, ev.t.rule.s_eps)


def test_stationary_bootstrap_draws_from_own_period(m: ModuleType) -> None:
    rng = np.random.default_rng(0)
    pools = [np.array([1.0, 2.0, 3.0]), np.array([10.0, 20.0])]
    per = np.array([0] * 50 + [1] * 50)
    x = m.bb_path(rng, per, pools, block=1e9)  # never restarts inside a period
    assert set(x[:50]) <= {1.0, 2.0, 3.0} and set(x[50:]) <= {10.0, 20.0}
    # with an endless block the path walks the pool in order (circularly)
    d = np.diff(x[:50])
    assert set(d) <= {1.0, -2.0}


def test_ar1_path_has_the_target_autocorrelation(m: ModuleType) -> None:
    rng = np.random.default_rng(0)
    per = np.zeros(20000, dtype=int)
    x = m.ar1_path(rng, per, np.array([0.01]), np.array([0.05]), np.array([0.3]))
    d = x - x.mean()
    assert math.isclose(float((d[1:] * d[:-1]).sum() / (d * d).sum()), 0.3, abs_tol=0.03)
    assert math.isclose(float(x.std()), 0.05, rel_tol=0.05)
