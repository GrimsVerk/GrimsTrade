"""ownvol-indep-1 assembly (research/lib/ownvolindep1.py; card research/cards/ownvol-indep-1.md).

- A market's scored returns are its counted segments run by pooled-2's frozen monthly code,
  concatenated unchanged, for `tsmom12` and own-vol (`vt-own-70-x`).
- The "sized months only" cell drops exactly the first 60 + gap scored months of each segment.
- Own-vol holds the fixed 0.70 share through the warm-up; the share summary is recomputed with
  the same frozen calls (it reproduces `run_monthly`'s own-vol returns).
- The card's reading: confirmed at z >= 1.645; contradicted when D + 1.645 SE < +0.022.
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
def mods() -> tuple[Any, Any, Any, Any]:
    pytest.importorskip("numpy")
    sys.path.insert(0, str(LIB))
    _load("pooled1_core")
    qc = _load("pooled2_core")
    ed = _load("e4indep1_data")
    ei = _load("e4indep1")
    ov = _load("ownvolindep1")
    return ed, ei, qc, ov


def _segs(ed: Any, n1: int, n2: int, gap: int) -> list[Any]:
    np = pytest.importorskip("numpy")
    rng = np.random.default_rng(3)
    out = []
    for y0, n in ((1870, n1), (1900, n2)):
        months = [date(y0 + i // 12, i % 12 + 1, 1) for i in range(n)]
        out.append(ed.Seg("X", months, list(rng.normal(0.005, 0.04, n)), gap))
    return out


def test_build_concatenates_frozen_runs(
    mods: tuple[Any, Any, Any, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    ed, ei, qc, ov = mods
    np = pytest.importorskip("numpy")
    segs = _segs(ed, 200, 70, 1)
    monkeypatch.setattr(ei, "load_segs", lambda root, s, gap_all=None: segs)
    spec = ei.Spec("X", "P4", "nber:x", 1)
    ms, shares = ov.build(Path("."), [spec])
    assert len(ms) == 1
    runs = [qc.run_monthly("X", "P4", s.months, np.array(s.r), 1, ei.COST) for s in segs]
    for r in ov.RULES2:
        assert np.array_equal(ms[0].rets[r], np.concatenate([x.rets[r] for x in runs]))
    # sized months only: the first 60 + gap scored months of each segment go
    mw, _ = ov.build(Path("."), [spec], skip_warm=True)
    k = ov.WARM + 1
    want = np.concatenate([x.rets[ov.OV][k:] for x in runs])
    assert np.array_equal(mw[0].rets[ov.OV], want)
    assert len(mw[0].periods) == len(want)
    assert 0 < shares["X"]["share"] <= 1


def test_warmup_is_fixed_share_and_share_matches_returns(
    mods: tuple[Any, Any, Any, Any],
) -> None:
    ed, ei, qc, ov = mods
    np = pytest.importorskip("numpy")
    seg = _segs(ed, 240, 0, 0)[0]
    r = np.array(seg.r)
    m = qc.run_monthly("X", "P4", seg.months, r, 0, ei.COST)
    pos, start = qc.decide_monthly(r, 0)
    p = pos["tsmom12"]
    net = p * r - ei.COST * np.abs(np.diff(p, prepend=0.0))
    out, plan = qc.own_vol_monthly(net, p, start, 0, qc.TARGET, qc.pc.RESET_COST)
    assert np.array_equal(out[start:], m.rets[ov.OV])
    # through the warm-up (first 59 resets) the planned share is the target
    assert all(plan[t] == qc.TARGET for t in range(start + 1, start + ov.WARM - 1))
    a, _ = ov.mean_share(r, 0, ei.COST)
    vals = [plan.get(t, qc.TARGET) for t in range(start, len(r))]
    assert a == pytest.approx(float(np.mean(vals)))


def test_reading_thresholds(mods: tuple[Any, Any, Any, Any]) -> None:
    _, _, _, ov = mods
    assert ov.reading({"D": 0.04, "se": 0.02, "z": 2.0}).startswith("confirmed")
    assert ov.reading({"D": -0.02, "se": 0.02, "z": -1.0}).startswith("contradicted")
    got = ov.reading({"D": 0.0, "se": 0.02, "z": 0.0})
    assert got.startswith("not confirmed") and "below #110" in got
    assert "not excluded" in ov.reading({"D": 0.02, "se": 0.03, "z": 0.67})
