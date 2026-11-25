"""insure-jstbonds-1: overlap and drop rules, threshold choice, tie rule, shares, nulls, control."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "insurejstbonds1.py"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    spec = importlib.util.spec_from_file_location("insurejstbonds1_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _toy_jst() -> dict[str, dict[str, dict[int, float]]]:
    """Two countries, 1900-1990: a slow three-year bond fall 1950-52 in FRA, flat elsewhere."""
    years = range(1900, 1991)
    bond = {y: 0.05 for y in years}
    bond.update({1950: -0.06, 1951: -0.05, 1952: -0.04, 1953: 0.12})
    bill = {y: 0.03 for y in years}
    cpi = {y: 1.0 + 0.02 * (y - 1900) for y in years}
    return {
        "bond_tr": {"FRA": bond, "USA": dict(bond)},
        "bill_rate": {"FRA": bill, "USA": dict(bill)},
        "cpi": {"FRA": cpi, "USA": dict(cpi)},
    }


def test_overlap_register(m: ModuleType) -> None:
    assert m.overlap("USA", 1871) and m.overlap("USA", 2020)
    assert m.overlap("NOR", 1900) and m.overlap("NOR", 2000)  # insure-bonds-1, then SEEN
    assert m.overlap("GBR", 1900) and not m.overlap("GBR", 1940) and m.overlap("GBR", 1960)
    assert not m.overlap("FRA", 1950)
    assert not m.overlap("DEU", 1955) and m.overlap("DEU", 1956)


def test_dropped_years(m: ModuleType) -> None:
    cpi = {1919: 1.0, 1920: 2.0, 1921: 2.1}  # 1920: CPI +100%
    prim = m.dropped(m.CONFIGS[0], "FRA", cpi)
    assert {1914, 1918, 1939, 1945, 1920} <= prim and 1921 not in prim and 1950 not in prim
    keep = m.dropped(m.Config("x", "x", keep_disrupted=True), "FRA", cpi)
    assert 1914 not in keep and 1920 not in keep
    us = m.dropped(m.CONFIGS[0], "USA", cpi)
    assert 1950 in us  # US years all overlap
    post = m.dropped(m.Config("p", "p", era="post"), "FRA", cpi)
    assert 1964 in post and 1965 not in post  # 1965 is the signal year


def test_build_cuts_segments_at_drops(m: ModuleType) -> None:
    segs = m.build(m.CONFIGS[0], _toy_jst())
    assert {s.iso for s in segs} == {"FRA"}
    for s in segs:
        assert not any(1939 <= y <= 1945 for y in s.years)
    pre = m.build(m.Config("pre", "pre", era="pre"), _toy_jst())
    assert max(s.years[-1] for s in pre) == 1965


def test_choose_largest_rung_with_enough_clusters(m: ModuleType) -> None:
    C = m.Count
    cs = [C(d, 0, a, li, 0, 0, 0) for d, a, li in
          zip(m.LADDER, [2, 3, 4, 12, 21, 24], [2, 3, 4, 9, 19, 21], strict=True)]  # fmt: skip
    assert m.LADDER[m.choose(cs)] == 0.075  # 10% fails on linked (9)
    none = [C(d, 0, 1, 1, 0, 0, 0) for d in m.LADDER]
    assert m.choose(none) == len(m.LADDER) - 1


def test_fall_counts_use_holding_only(m: ModuleType) -> None:
    jst = _toy_jst()
    segs = m.build(m.CONFIGS[0], jst)
    for s in segs:
        s.pos[:] = np.nan  # counts must not touch positions
    cs = m.fall_counts(segs, m.anchor_segs(m.CONFIGS[0], jst), ladder=(0.25, 0.10))
    assert [c.episodes for c in cs] == [0, 1]
    assert cs[1].multi_year == 1 and cs[1].anchored == 1 and cs[1].linked == 1


def test_tie_rule_zeroes_rounding(m: ModuleType) -> None:
    jst = _toy_jst()
    seg = m.build(m.CONFIGS[0], jst)[-1]
    sc = m.ins.episodes(seg, 0.10, 0.10)
    rule = m.ins.strat(seg, np.ones(len(seg.pos))) + 1e-16  # fully in, float noise
    m.rescore(sc, rule)
    assert sc.eps and all(e.ins == 0.0 for e in sc.eps)


def test_ep_shares_matches_jstautocorr_and_real_denominator(m: ModuleType) -> None:
    r = np.array([0.05, -0.06, -0.05, -0.04, 0.12, 0.05])
    b = np.full(6, 0.03)
    pos = np.array([1.0, 1.0, 0.0, 0.0, 0.0, 1.0])
    pairs = [(1, 4)]
    assert np.allclose(m.ep_shares(r, b, pos, pairs), m.ja.shares(r, b, pos, pairs))
    pi = np.full(6, 0.10)
    real = m.ep_shares(r, b, pos, pairs, pi)[0]
    hold_real = 100 * np.sum(np.log1p(r[1:4]) - np.log1p(pi[1:4]))
    ins = m.ep_shares(r, b, pos, pairs)[0] * abs(100 * np.sum(np.log1p(r[1:4])))
    assert real == pytest.approx(ins / abs(hold_real))


def test_block_bootstrap_draws_own_values(m: ModuleType) -> None:
    jst = _toy_jst()
    seg = m.build(m.CONFIGS[0], jst)[-1]
    x = m.bb_x(np.random.default_rng(1), seg, 200)
    assert len(x) == 200 and set(np.round(x, 12)) <= set(np.round(m.logx(seg), 12))


def test_trimmed_lag2_uses_older_signal(m: ModuleType) -> None:
    seg = m.build(m.CONFIGS[0], _toy_jst())[-1]
    l1, l2 = m.trimmed([seg], 1)[0], m.trimmed([seg], 2)[0]
    assert l1.years == l2.years == seg.years[1:]
    assert np.array_equal(l1.pos, seg.pos[1:]) and np.array_equal(l2.pos, seg.pos[:-1])


def test_null_gaps_deterministic(m: ModuleType) -> None:
    segs = m.build(m.CONFIGS[0], _toy_jst())
    a = m.null_gaps(segs, 0.05, "ar", worlds=5, phis={"FRA": 0.0})
    b = m.null_gaps(segs, 0.05, "ar", worlds=5, phis={"FRA": 0.0})
    assert np.array_equal(a, b, equal_nan=True)
    assert m.p_ge(np.array([0.1, 0.2, np.nan, 0.3]), 0.2) == pytest.approx(2 / 3)


def test_reading_l2(m: ModuleType, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(m.ins, "ok", lambda vals: True)

    def r(p: float) -> SimpleNamespace:
        return SimpleNamespace(p_null=p, anch=[], linked=[])

    assert m.reading_l2(r(0.01), r(0.02)) == "timing does not rest on the last year alone"
    assert m.reading_l2(r(0.01), r(0.30)) == "timing rests on the last year's return"
    assert m.reading_l2(r(0.60), r(0.30)) == "in between / not read"


def test_run_toy_verdict_too_few(m: ModuleType) -> None:
    jst = _toy_jst()
    cfg = m.CONFIGS[0]
    res = m.run("toy", m.build(cfg, jst), m.anchor_segs(cfg, jst), 0.10, worlds=5)
    assert res.verdict == "Too few falls"
    assert res.head == (1, 1)  # the rule left after the first fall year
