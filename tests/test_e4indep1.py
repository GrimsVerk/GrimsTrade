"""e4-indep-1 data and assembly (research/lib/e4indep1*.py; card research/cards/e4-indep-1.md).

- NBER rectdata and French country files parse to the right months; "." and -99.99 are gaps.
- A gap in the months splits a series into segments; returns are labelled by their end month.
- A market's scored returns are its counted segments run by pooled-2's frozen monthly code,
  concatenated unchanged; segments too short to count are dropped.
"""

from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mods() -> tuple[Any, Any, Any]:
    pytest.importorskip("numpy")
    sys.path.insert(0, str(LIB))
    _load("pooled1_core")
    qc = _load("pooled2_core")
    ed = _load("e4indep1_data")
    ei = _load("e4indep1")
    return ed, ei, qc


def test_parse_nber_skips_missing(mods: tuple[Any, Any, Any]) -> None:
    ed, _, _ = mods
    text = "1914    6 8.1300\n1914    7 7.6800\n1914    8 .\n1914   12 7.3500\nc comment\n"
    lv = ed.parse_nber(text)
    assert lv == {ed.mi(1914, 6): 8.13, ed.mi(1914, 7): 7.68, ed.mi(1914, 12): 7.35}
    segs = ed.segments(lv)
    assert [len(s) for s in segs] == [2, 1]
    r = ed.seg_returns("X", segs[0], 0)
    assert r.months == [date(1914, 7, 1)]
    assert r.r == pytest.approx([7.68 / 8.13 - 1])


def test_segments_respect_bounds(mods: tuple[Any, Any, Any]) -> None:
    ed, _, _ = mods
    lv = {ed.mi(1900, m): float(m) for m in range(1, 13)}
    segs = ed.segments(lv, ed.mi(1900, 3), ed.mi(1900, 6))
    assert [k for k, _ in segs[0]] == [ed.mi(1900, m) for m in (3, 4, 5, 6)]


def test_parse_french_mkt_first_block_only(mods: tuple[Any, Any, Any]) -> None:
    ed, _, _ = mods
    text = (
        "\n  Value-Weight Dollar Returns\n          Mkt   High\n"
        "202509   1.50  2.0\n202510  -99.99  1.0\n202511   3.00  1.0\n\n"
        " Annual\n198701  9.99  1.0\n"
    )
    out = ed.parse_french_mkt(text, date(2025, 10, 1))
    assert out == {ed.mi(2025, 9): pytest.approx(0.015)}


def test_build_concatenates_frozen_runs(mods: tuple[Any, Any, Any], tmp_path: Path) -> None:
    ed, ei, qc = mods
    np = pytest.importorskip("numpy")
    rng = np.random.default_rng(1)
    d = tmp_path / "e4-indep-1" / "nber"
    d.mkdir(parents=True)
    lines = []
    lv = 100.0
    for y in range(1880, 1891):  # 132 months, one segment
        for m in range(1, 13):
            lv *= float(np.exp(rng.normal(0.004, 0.04)))
            lines.append(f"{y} {m:4d} {lv:.4f}")
    for y in range(1895, 1897):  # 24 months: too short, dropped
        for m in range(1, 13):
            lines.append(f"{y} {m:4d} {100 + m:.4f}")
    (d / "m99999.dat").write_text("\n".join(lines) + "\n")
    spec = ei.Spec("ZZ", "P4", "nber:m99999", 1, None, ed.CUT)
    ms, log = ei.build(tmp_path, [spec])
    assert [row["counted"] for row in log] == [True, False]
    seg = ed.seg_returns("ZZ", ed.segments(ed.nber(tmp_path, "m99999"))[0], 1)
    ref = qc.run_monthly("ZZ", "P4", seg.months, np.array(seg.r), 1, ei.COST)
    assert len(ms) == 1
    for r in ei.RULES2:
        assert np.array_equal(ms[0].rets[r], ref.rets[r])
    assert np.array_equal(ms[0].periods, ref.periods)
