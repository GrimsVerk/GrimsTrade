"""fx-peg-1: peg filter (trailing only), signals, loaders, chronology labels, books, joint nulls."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "fxpeg1.py"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    spec = importlib.util.spec_from_file_location("fxpeg1_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_classify_peg_float_unknown(m: ModuleType) -> None:
    rng = np.random.default_rng(0)
    peg = rng.normal(0, 0.002, 40)
    flt = rng.normal(0, 0.04, 40)
    st = m.classify(np.concatenate([peg, flt]))
    assert all(s == m.UNKNOWN for s in st[:23])
    assert all(s == m.PEG for s in st[23:40])
    assert all(s == m.FLOAT for s in st[60:])


def test_classify_band_and_share_edges(m: ModuleType) -> None:
    # 19 small and 5 large moves in 24: 79% small -> float; 20 small and 4 large -> peg
    x = np.array([0.001] * 19 + [0.05] * 5)
    assert m.classify(x)[-1] == m.FLOAT
    x = np.array([0.001] * 20 + [0.05] * 4)
    assert m.classify(x)[-1] == m.PEG
    # a missing change inside the window makes the state unknown
    x = np.array([0.001] * 30)
    x[20] = np.nan
    st = m.classify(x)
    assert st[20] == m.UNKNOWN and st[29] == m.UNKNOWN


def test_classify_uses_no_future_data(m: ModuleType) -> None:
    rng = np.random.default_rng(1)
    x = rng.normal(0, 0.01, 120)
    base = m.classify(x)
    y = x.copy()
    y[70:] = rng.normal(0, 0.2, 50)  # rewrite the future
    assert list(m.classify(y)[:70]) == list(base[:70])


def test_signals_match_trend_where_long(m: ModuleType) -> None:
    sys.path.insert(0, str(ROOT / "research" / "lib"))
    import trend_where_long as twl  # type: ignore[import-not-found]

    rng = np.random.default_rng(2)
    x = rng.normal(0.001, 0.03, 200)
    x[50] = np.nan
    valid, on = m.signals(x)
    v2, o2 = twl.signals(np.expm1(x).reshape(-1, 1))
    assert (valid == v2[:, 0]).all()
    assert (on == o2[:, 0]).all()


def test_label_month_reads_small_excel_serials(m: ModuleType) -> None:
    assert m.label_month(5145.0) == m.ym(1914, 1)  # 1914-01-31, dropped by datawide2's parser
    assert m.label_month(10000.0) == m.ym(1927, 5)
    assert m.label_month("1819 04") == m.ym(1819, 4)


def test_make_market_breaks_on_redenomination_and_column_switch(m: ModuleType) -> None:
    a = {m.ym(1876, 10): 1.0, m.ym(1876, 11): 1.01, m.ym(1876, 12): 1.02}
    b = {m.ym(1877, 1): 50.0, m.ym(1877, 2): 50.5}
    c = {m.ym(1877, 3): 5050.0, m.ym(1877, 4): 5000.0}  # x100 jump -> break
    b.update(c)
    mk = m.make_market("t", "DEM", "NOK", [(m.changes(a), "end"), (m.changes(b), "end")])
    xs = dict(zip(mk.months.tolist(), mk.x.tolist(), strict=True))
    assert m.ym(1877, 1) not in xs or math.isnan(xs[m.ym(1877, 1)])  # no change across columns
    assert math.isnan(xs[m.ym(1877, 3)]) and mk.breaks == 1
    assert xs[m.ym(1877, 2)] == pytest.approx(math.log(1.01))


def test_changes_respect_bounds_and_cut(m: ModuleType) -> None:
    lv = {m.ym(1914, 11): 1.0, m.ym(1914, 12): 2.0, m.ym(1915, 1): 4.0}
    assert list(m.changes(lv, hi=m.JOIN - 1)) == [m.ym(1914, 12)]
    assert list(m.changes(lv, lo=m.JOIN)) == [m.ym(1915, 1)]
    late = {m.ym(1970, 12): 1.0, m.ym(1971, 1): 2.0}
    assert m.changes(late) == {}


def test_chronology_pairs(m: ModuleType) -> None:
    ym = m.ym
    assert m.chrono_pair("GBP", "USD", ym(1880, 6)) == m.PEG  # both gold
    assert m.chrono_pair("GBP", "USD", ym(1870, 6)) == m.FLOAT  # greenbacks
    assert m.chrono_pair("GBP", "USD", ym(1810, 6)) == m.FLOAT  # Bank Restriction
    assert m.chrono_pair("GBP", "USD", ym(1925, 6)) == m.AMBIG  # within 3 months of a switch
    assert m.chrono_pair("GBP", "USD", ym(1917, 1)) == m.PEG  # pegged at 4.765
    assert m.chrono_pair("GBP", "NOK", ym(1936, 6)) == m.PEG  # krone pegged to sterling
    assert m.chrono_pair("USD", "NOK", ym(1936, 6)) == m.FLOAT  # sterling floats vs the dollar
    assert m.chrono_pair("GBP", "NOK", ym(1855, 6)) == m.AMBIG  # silver vs gold
    assert m.chrono_pair("DEM", "NOK", ym(1855, 6)) == m.PEG  # both silver
    assert m.chrono_pair("FRF", "NOK", ym(1925, 6)) == m.FLOAT


def test_irr_pair_resolves_anchor_chains(m: ModuleType) -> None:
    t = m.ym(1960, 1)
    fine = {"NOK": {t: 4}, "GBP": {t: 3}, "CAD": {t: 13}, "SEK": {t: 7}}
    anch = {"NOK": {t: "USD"}, "GBP": {t: "USD"}, "CAD": {t: "USD"}, "SEK": {t: "USD"}}
    assert m.irr_pair("GBP", "NOK", t, fine, anch) == m.PEG
    assert m.irr_pair("USD", "NOK", t, fine, anch) == m.PEG
    assert m.irr_pair("CAD", "NOK", t, fine, anch) == m.FLOAT
    assert m.irr_pair("SEK", "NOK", t, fine, anch) == m.AMBIG  # crawling code 7
    fine2 = {"DKK": {t: 4}, "NOK": {t: 4}}
    anch2 = {"DKK": {t: "DEM"}, "NOK": {t: "USD"}}
    assert (
        m.irr_pair("DKK", "NOK", t, {**fine2, "DEM": {t: 4}}, {**anch2, "DEM": {t: "USD"}}) == m.PEG
    )


def test_irr_parsers(m: ModuleType) -> None:
    fine_rows = [
        {1: "Independence"},
        {0: " ", 1: "Country", 3: "United"},
        {2: " Norway", 3: "Kingdom"},
        {},
        {1: "1960M1", 2: "4", 3: "3"},
        {1: "1971M1", 2: "12", 3: "13"},
    ]
    fine = m.parse_irr_fine(fine_rows)
    assert fine["NOK"] == {m.ym(1960, 1): 4}  # 1971 is after the cut
    assert fine["GBP"] == {m.ym(1960, 1): 3}
    anchor_rows = [{0: "ISO3 Code", 1: "NOR", 2: "GBR"}, {0: "1960M1", 1: "USD", 2: "n.a."}]
    anch = m.parse_irr_anchor(anchor_rows)
    assert anch["NOK"] == {m.ym(1960, 1): "USD"} and anch["GBP"] == {}


def test_agreement_kappa(m: ModuleType) -> None:
    pairs = [(m.PEG, m.PEG)] * 6 + [(m.FLOAT, m.FLOAT)] * 2 + [(m.PEG, m.FLOAT)] * 2
    pairs += [(m.UNKNOWN, m.PEG), (m.PEG, m.AMBIG)]
    ag = m.agreement(pairs)
    assert ag.n == 10 and ag.agree == pytest.approx(0.8)
    # pa = 0.8, pb = 0.6 -> pe = 0.56, kappa = 0.24 / 0.44
    assert ag.kappa == pytest.approx(0.24 / 0.44)


def _market(m: ModuleType, x: np.ndarray, name: str = "t") -> Any:
    return m.Market(name, "GBP", "USD", m.ym(1900, 1), x, ["end"] * len(x))


def test_filtered_book_skips_peg_months_and_uses_prior_state(m: ModuleType) -> None:
    rng = np.random.default_rng(3)
    x = np.concatenate([rng.normal(0, 0.002, 60), rng.normal(0, 0.05, 60)])
    mk = _market(m, x)
    st = m.classify(x)
    ok = m.scored_mask(mk, m.Spec())
    for k in range(1, len(x)):
        assert ok[k] == (st[k - 1] == m.FLOAT)
    assert not ok[:60].any()
    unf = m.scored_mask(mk, m.Spec(book="unfiltered"))
    peg = m.scored_mask(mk, m.Spec(book="pegonly"))
    assert ((ok | peg) == unf).all() and not (ok & peg).any()


def test_make_seg_positions_from_prior_signal(m: ModuleType) -> None:
    x = np.array([0.01] * 12 + [-0.02] * 12 + [0.01] * 20)
    mk = _market(m, x)
    ref = m.SegRef(0, 12, len(x))
    s = m.make_seg(mk, ref, x, 0)
    _, on = m.signals(x)
    assert s.pos[1] == float(on[11]) and s.pos[0] == s.pos[1]
    assert s.months[0] == mk.start + 11 and s.months[1] == mk.start + 12
    assert s.r[1] == pytest.approx(math.expm1(x[12]))


def test_ls_book_is_invariant_to_quoting_direction(m: ModuleType) -> None:
    rng = np.random.default_rng(4)
    x = rng.normal(0, 0.03, 80)
    a, b = _market(m, x), _market(m, -x)
    ref = m.SegRef(0, 12, 80)
    la = m.ls_mean([m.make_seg(a, ref, x, 0)])
    lb = m.ls_mean([m.make_seg(b, ref, -x, 0)])
    # signals flip except on exact zero sums; with continuous draws the books are equal
    assert la[0] == pytest.approx(lb[0]) and la[1] == lb[1]


def test_joint_worlds_draw_the_same_calendar_month(m: ModuleType) -> None:
    rng = np.random.default_rng(5)
    x = rng.normal(0, 0.03, 100)
    a, b = _market(m, x, "a"), _market(m, x.copy(), "b")
    refs = [m.SegRef(0, 30, 100), m.SegRef(1, 30, 100)]
    jw = m.JointWorlds([a, b], refs)
    assert len(jw.epochs) == 1
    for kind in ("bb", "iid", "ar1"):
        w = jw.draw(np.random.default_rng(6), kind, demean=False)
        assert np.allclose(w[0], w[1]) or kind == "ar1"
    w = jw.draw(np.random.default_rng(7), "bb", demean=True)
    assert set(np.round(w[0], 12)) <= set(np.round(x[30:] - x[30:].mean(), 12))
    segs = jw.world(w)
    assert [len(s.r) for s in segs] == [71, 71]
    assert np.allclose(np.log1p(segs[0].r[1:]), w[0])


def test_joint_ar1_keeps_contemporaneous_dependence(m: ModuleType) -> None:
    rng = np.random.default_rng(8)
    x = rng.normal(0, 0.03, 300)
    a, b = _market(m, x, "a"), _market(m, x.copy(), "b")
    jw = m.JointWorlds([a, b], [m.SegRef(0, 30, 300), m.SegRef(1, 30, 300)])
    w = jw.draw(np.random.default_rng(9), "ar1", demean=True)
    assert np.corrcoef(w[0], w[1])[0, 1] > 0.95


def test_evaluate_on_a_synthetic_float(m: ModuleType) -> None:
    rng = np.random.default_rng(10)
    calm = rng.normal(0, 0.002, 40)
    trend = np.concatenate([rng.normal(-0.03, 0.02, 30), rng.normal(0.03, 0.02, 30)])
    x = np.concatenate([calm, trend, trend, trend])
    ev = m.evaluate([_market(m, x)], m.Spec(), rotations=50)
    assert ev.segs and ev.eps and ev.tim is not None
    assert m.verdict(ev, 0.5) in (
        "Too few falls",
        "Does not hold",
        "Holds only as lower exposure",
        "In between",
        "Holds, timing not separable from autocorrelation",
    )
    assert m.premium_verdict(0.001, 0.01, 0.2) == "Premium not separable from autocorrelation"
    assert m.premium_verdict(0.001, 0.01, 0.01) == "Trend premium beyond autocorrelation"
    assert m.premium_verdict(-0.001, 0.01, 0.01) == "No trend premium shown"
