"""jst-autocorr-2: source pieces, pairing, flags, the card's readings and usability rule."""

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
PATH = ROOT / "research" / "lib" / "jstautocorr2.py"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    spec = importlib.util.spec_from_file_location("jstautocorr2_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def seg(m: ModuleType, iso: str, first: int, r: np.ndarray) -> Any:
    n = len(r)
    years = list(range(first, first + n + 1))
    z = np.zeros(n)
    return m.ins.Seg(iso, years, r, z, z, np.ones(n))


def test_source_and_labels(m: ModuleType) -> None:
    assert m.source("DEU", 1889) == "Ronge top-30"
    assert m.source("DEU", 1890) == "Eube all-share"
    assert m.timing("USA", 1900) == m.DAVG
    assert m.timing("ESP", 1938) == m.INTP
    assert m.timing("NOR", 1930) == m.YE
    assert m.disrupted("SWE", 1916, frozenset())
    assert not m.disrupted("SWE", 1925, frozenset())
    assert m.disrupted("SWE", 1925, frozenset({1925}))


def test_pieces_split_at_source_change_and_demean(m: ModuleType) -> None:
    # Germany 1880-1899 scored: source changes at 1890
    s = seg(m, "DEU", 1879, np.linspace(0.01, 0.2, 20))
    ps = m.pieces([s])
    assert [p.src for p in ps] == ["Ronge top-30", "Eube all-share"]
    assert ps[0].years[0] == 1880 and ps[1].years[0] == 1890
    assert all(abs(p.x.mean()) < 1e-12 for p in ps)
    pr = m.pairs(ps)
    assert len(pr.u) == 9 + 9  # no pair crosses the source change


def test_acf_alternating_and_lag2(m: ModuleType) -> None:
    alt = np.array([0.1, -0.1] * 6)
    s = seg(m, "PRT", 1880, np.expm1(alt))
    ps = m.pieces([s])
    a, n = m.acf(m.pairs(ps))
    assert n == 11 and a == pytest.approx(-1.0)
    a2, n2 = m.acf(m.pairs(ps, 2))
    assert n2 == 10 and a2 == pytest.approx(1.0)


def test_flag_on_marks_pairs_touching_flagged_years(m: ModuleType) -> None:
    s = seg(m, "SWE", 1909, np.full(12, 0.05) + np.arange(12) * 0.001)  # scored 1910-1921
    ps = m.pieces([s])
    pr = m.pairs(ps)
    f = m.make_flag("d", [s], ps, lambda p: False, lambda iso, y: m.disrupted(iso, y, frozenset()))
    on = f.on(pr)
    # pairs (1910,1911) ... (1920,1921); flagged if either year in 1914-1918
    flagged = {(int(a), int(b)) for a, b, o in zip(pr.y0, pr.y1, on, strict=True) if o}
    assert (1913, 1914) in flagged and (1918, 1919) in flagged
    assert (1912, 1913) not in flagged and (1919, 1920) not in flagged


def test_reading_rule(m: ModuleType) -> None:
    # rest within noise and p small: explains
    assert m.reading(0.4, 300, 0.02, 900, 0.01, 0.17) == "explains it"
    # rest still high but p small: partly
    assert m.reading(0.4, 300, 0.15, 900, 0.01, 0.17) == "partly explains it"
    # rest halved, p large: partly
    assert m.reading(0.2, 300, 0.08, 900, 0.30, 0.17) == "partly explains it"
    assert m.reading(0.2, 300, 0.16, 900, 0.30, 0.17) == "not explained by this flag"
    assert m.reading(0.9, 20, 0.0, 900, 0.0, 0.17).startswith("not decidable")


def test_usability_rule(m: ModuleType) -> None:
    assert m.usability(m.INTP, m.BROAD, 0.0, 50).startswith("not usable")
    assert m.usability(m.YE, m.BROAD, 0.0, 50) == "usable"
    assert m.usability(m.YE, m.BROAD, 0.5, 50).startswith("AR-preserving null only (acf")
    assert m.usability(m.YE, m.THIN, 0.0, 50) == "AR-preserving null only (thin)"
    assert m.usability(m.UNK, m.BROAD, 0.0, 50) == "AR-preserving null only (labels unknown)"
    assert m.usability(m.YE, m.BROAD, math.nan, 2).startswith("too short")


def test_flag_test_finds_planted_autocorrelation(m: ModuleType) -> None:
    rng = np.random.default_rng(1)
    segs = []
    isos = ["SWE", "BEL", "FRA", "PRT", "AUS", "GBR", "USA", "NLD", "ITA", "FIN", "DNK", "JPN"]
    for k, iso in enumerate(isos):  # 12 units: the shuffle can reach p < 0.05
        e = rng.standard_normal(40) * 0.1
        if k < 3:  # strong AR(1) in the first three countries
            for t in range(1, 40):
                e[t] += 0.8 * e[t - 1]
        segs.append(seg(m, iso, 1919, np.expm1(e)))  # scored 1920-1959 (WW2 inside)
    ps = m.pieces(segs)
    pr = m.pairs(ps)
    a0, _ = m.acf(pr)
    f = m.Flag("planted", np.array([p.iso in ("SWE", "BEL", "FRA") for p in ps]),
               [np.zeros(len(s.r), dtype=bool) for s in segs])  # fmt: skip
    t = m.flag_test(f, pr, a0, perms=200)
    assert t.a_flag > 0.5 and t.p < 0.05
