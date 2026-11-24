"""ownvol-anatomy-1: the replays equal the frozen own-vol code, the split adds up exactly."""

from __future__ import annotations

import importlib
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "lib"))
oc: Any = importlib.import_module("ownvolanatomy_core")
pc: Any = importlib.import_module("pooled1_core")
qc: Any = importlib.import_module("pooled2_core")


def _market(n: int = 2600, seed: int = 3) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    days: list[int] = []
    d = date(1990, 1, 1)
    while len(days) < n:
        if d.weekday() < 5:
            days.append(d.toordinal())
        d += timedelta(days=1)
    vol = 0.01 * np.exp(np.cumsum(rng.normal(0, 0.05, n)) * 0.3)
    lr = rng.normal(0.0003, vol)
    lr[0] = 0.0
    return np.array(days, dtype=np.int64), 100 * np.exp(np.cumsum(lr))


@pytest.mark.parametrize("skip", [0, 1])
def test_weekly_replay_equals_frozen(skip: int) -> None:
    d, px = _market()
    m = pc.run_market("x", "g", d, px)
    x, g = m.daily["tsmom12"], m.pos["tsmom12"]
    o, share, sized, _ = oc.book_weekly(d, x, g, m.start, skip=skip)
    frozen = (
        m.daily["vt-own-70-x"]
        if skip == 0
        else qc.own_vol_weekly(d, x, g, m.start, 0.70, skip, pc.RESET_COST)[0]
    )
    assert np.array_equal(o, frozen)
    assert sized < len(x)
    assert np.all((share[m.start :] > 0) & (share[m.start :] <= 1 + 1e-12))


def test_monthly_replay_equals_frozen() -> None:
    rng = np.random.default_rng(5)
    r = rng.normal(0.004, 0.03, 400)
    pos, start = qc.decide_monthly(r, 1)
    g = pos["tsmom12"]
    x = g * r - 0.0002 * np.abs(np.diff(g, prepend=0.0))
    frozen, _ = qc.own_vol_monthly(x, g, start, 1, 0.70, pc.RESET_COST)
    o, _, _, _ = oc.book_monthly(x, g, start, 1)
    assert np.array_equal(o, frozen)


def _series(o: np.ndarray, f: np.ndarray, s: np.ndarray) -> Any:
    n = len(o)
    sr = oc.Series("x", "g", "w", o, f, s, np.arange(n) // 4)
    rng = np.random.default_rng(0)
    for p, names in oc.PARTS.items():
        sr.labels[p] = rng.integers(0, len(names), n).astype(np.int8)
    return sr


def test_split_adds_up_exactly() -> None:
    rng = np.random.default_rng(1)
    s = rng.normal(0.002, 0.02, 600)
    f = 0.6 * s + rng.normal(0, 1e-4, 600)
    o = s * rng.uniform(0.3, 1.0, 600)
    sr = _series(o, f, s)
    sp = oc.split(sr)
    assert sp["E"] + sp["M"] + sp["R"] == pytest.approx(sp["d"], abs=1e-12)
    assert sp["E"] == pytest.approx(oc.sharpe(f, 52) - oc.sharpe(s, 52), abs=1e-12)
    for p, names in oc.PARTS.items():
        for k in oc.TERMS:
            assert sum(sp[p][nm][k] for nm in names) == pytest.approx(sp[k], abs=1e-12)
        assert sum(sp[p][nm]["share"] for nm in names) == pytest.approx(1.0)


def test_constant_share_has_no_timing() -> None:
    rng = np.random.default_rng(2)
    s = rng.normal(0.002, 0.02, 300)
    sp = oc.split(_series(0.7 * s, 0.7 * s, s))
    assert sp["M"] == pytest.approx(0.0, abs=1e-12)
    assert sp["R"] == pytest.approx(0.0, abs=1e-12)
    assert sp["E"] == pytest.approx(0.0, abs=1e-12)


def test_fixed_twin_has_tsmom_sharpe_up_to_drift_and_cost() -> None:
    d, px = _market()
    m = pc.run_market("x", "g", d, px)
    x, g = m.daily["tsmom12"], m.pos["tsmom12"]
    f, share, _, _ = oc.book_weekly(d, x, g, m.start, fixed=0.6)
    assert np.allclose(share[m.start :][g[m.start :] == 0], share[m.start :][g[m.start :] == 0])
    sf = pc.sharpe(pc.weekly(d, f, m.start)[1])
    ss = pc.sharpe(pc.weekly(d, x, m.start)[1])
    assert abs(sf - ss) < 0.02


def test_labels_cover_and_match_zigzag() -> None:
    px = np.array([100, 110, 80, 70, 75, 95, 100, 120, 85, 90, 120, 125], dtype=float)
    ords = np.arange(len(px)) * 60 + 700000
    pairs, _ = oc.zigzag(px, 0.25, 0.25)
    assert pairs == [(1, 3), (7, 8)]
    lab = oc.fall_labels(ords, px, 0.25, 0.25)
    assert list(lab[2:4]) == [oc.SLOWC, oc.SLOWC]  # 120 days peak -> trough
    assert list(lab[4:8]) == [oc.REBC] * 4  # until the next peak
    assert lab[1] == oc.CALMC
    assert lab[8] == oc.FASTC  # 60 days
    reg = oc.regime_labels(lab, np.zeros(len(px)), "w")
    assert set(np.unique(reg)) <= set(range(len(oc.REGIMES)))
    vs = oc.vol_state(
        np.linspace(0.2, 1.0, 12), np.array([True] + [False] * 11), np.zeros(12, bool)
    )
    assert vs[0] == 0 and set(vs[1:]) == {2, 3, 4}


def test_whipsaw_window() -> None:
    pos = np.array([0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
    w = oc.whipsaw(oc.changes(pos), 2)
    assert w[2] and w[3] and not w[10]
