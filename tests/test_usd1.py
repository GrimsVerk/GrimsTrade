"""The usd-1 replication measures what its card says (research/usd-1.md).

- S is minus the plain correlation over cells, for the series and for every rotation of it.
- A rotation only reorders the dollar inside its own span, by at least 52 weeks from either end.
- The `-resid` target has nothing left of the reference, asset by asset.
- The Coin Metrics target uses prices known the day before, earns from the day after, and carries
  a dead coin's last price.
- A planted "dollar up, then worse returns" comes out as S > 0 with a small p.
"""

from __future__ import annotations

import importlib
import math
import sys
from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from grimstrade import data

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def u1() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    pytest.importorskip("sklearn")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    mod = importlib.import_module("usd1")
    yield mod
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path


def test_s_is_minus_the_cell_correlation(u1: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    rng = np.random.default_rng(1)
    g, n = 300, 5
    x = rng.standard_normal(g)
    x[:20] = np.nan
    z = rng.standard_normal((g, n)) - 0.3 * np.nan_to_num(x)[:, None]
    z[rng.random((g, n)) < 0.2] = np.nan
    xr = u1.rotations(x, rng.random(4))
    got = u1.s_many(xr, z)
    for k in range(len(xr)):
        m = np.isfinite(z) & np.isfinite(xr[k])[:, None]
        xc = np.repeat(xr[k][:, None], n, 1)[m]
        assert got[k] == pytest.approx(-np.corrcoef(xc, z[m])[0, 1], abs=1e-12)
    assert got[0] > 0  # dollar up, then lower z: the card's sign


def test_rotation_stays_inside_the_span(u1: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    x = np.arange(500.0)
    x[:40] = np.nan
    us = np.array([0.0, 0.37, 0.999999])
    xr = u1.rotations(x, us)
    assert np.array_equal(xr[0], x, equal_nan=True)
    for k, u in enumerate(us):
        row = xr[k + 1]
        assert np.isnan(row[:40]).all()
        assert sorted(row[40:]) == sorted(x[40:])
        s = int(np.flatnonzero(row == 40.0)[0]) - 40
        assert 52 <= s <= 460 - 52
        assert s == 52 + int(u * (460 - 104))
    hole = x.copy()
    hole[100] = np.nan
    with pytest.raises(ValueError):
        u1.rotations(hole, us)
    filled, count = u1.fill_inside(hole)
    assert count == 1 and filled[100] == 99.0 and np.isnan(filled[:40]).all()


def test_residual_has_nothing_left_of_the_reference(u1: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    rng = np.random.default_rng(2)
    ref = rng.standard_normal(200)
    ref[:10] = np.nan
    z = np.column_stack(
        [0.8 * np.nan_to_num(ref) + rng.standard_normal(200) + 3.0, rng.standard_normal(200)]
    )
    z[150:, 1] = np.nan
    short = np.full(200, np.nan)
    short[20:40] = 1.0  # 20 cells: under the minimum
    r = u1.residual(np.column_stack([z, short]), ref)
    assert np.isnan(r[:, 2]).all()
    for j in range(2):
        m = np.isfinite(r[:, j])
        assert np.array_equal(m, np.isfinite(z[:, j]) & np.isfinite(ref))
        assert abs(r[m, j].mean()) < 1e-12
        assert abs(float(r[m, j] @ (ref[m] - ref[m].mean()))) < 1e-9


def test_coin_target_clock(u1: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    rng = np.random.default_rng(3)
    d_n, h = 400, 4
    px = np.exp(np.cumsum(0.03 * rng.standard_normal((d_n, 3)), axis=0))
    px[300:, 1] = np.nan  # coin 1 dies: its last price is day 299
    elig = np.ones((d_n, 3), dtype=bool)
    elig[:50] = False
    elig[:, 2] = False
    z = u1.cm_z(px, elig, h)
    assert np.isnan(z[:50]).all() and np.isnan(z[:, 2]).all()
    assert np.isnan(z[d_n - 1 - 7 * h :]).all() and np.isfinite(z[d_n - 2 - 7 * h, 0])
    lam = 0.5 ** (1 / 60)

    def vol(t: int, j: int) -> float:  # returns through the price stamped t - 1
        lr = np.diff(np.log(px[:t, j]))
        w = lam ** np.arange(len(lr))[::-1]
        return math.sqrt(float((w * lr * lr).sum() / w.sum()) * 365)

    for t in (60, 200, 350):
        want = math.log(px[t + 1 + 7 * h, 0] / px[t + 1, 0])
        want /= vol(t, 0) * math.sqrt(7 * h / 365)
        assert z[t, 0] == pytest.approx(max(-5.0, min(5.0, want)), abs=1e-9)
    # a window that straddles the death ends at the last price; later windows are flat
    t = 290
    want = math.log(px[299, 1] / px[t + 1, 1]) / (vol(t, 1) * math.sqrt(7 * h / 365))
    assert z[t, 1] == pytest.approx(max(-5.0, min(5.0, want)), abs=1e-9)
    assert z[320, 1] == 0.0
    # the price stamped on the decision day itself is not known yet and not earned: changing it
    # leaves that day's cell alone and moves the day before (its entry price) and the day after
    px2 = px.copy()
    px2[200, 0] *= 1.5
    z2 = u1.cm_z(px2, elig, h)
    assert z2[200, 0] == z[200, 0]
    assert z2[199, 0] != z[199, 0] and z2[201, 0] != z[201, 0]


def test_planted_dollar_effect_is_found_with_its_sign(u1: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    rng = np.random.default_rng(4)
    g, n, h = 1500, 4, 13
    fridays = [date(1990, 1, 5) + timedelta(days=7 * i) for i in range(g)]
    w = rng.standard_normal(g + h)
    x = np.array([w[i : i + h].sum() for i in range(g)]) / math.sqrt(h)  # a 13-week change
    e = rng.standard_normal((g + h, n))
    noise = np.stack([e[i : i + h].sum(0) for i in range(g)]) / math.sqrt(h)
    us = rng.random(300)
    xr = u1.rotations(x, us)
    eras = [("early", 1990, 2004), ("late", 2005, 2030)]
    hit = u1.measure("planted", noise - 0.3 * x[:, None], xr, fridays, h, list("abcd"), True, eras)
    assert hit["s"] > 0.2 and hit["p"] < 0.01 and hit["cells"] == g * n
    assert set(hit["eras"]) == {"early", "late"} and hit["blocks_neg"] == hit["blocks"] > 0
    assert hit["wf_pool"] > 0.1 and hit["nov_min"] > 0
    none = u1.measure("nothing", noise, xr, fridays, h, list("abcd"), True)
    assert abs(none["s"]) < 3 * none["sd"]
    # overlap is priced: far fewer independent observations than cells
    assert none["neff"] < g * n / 4
    pl = u1.pooled([hit, none])
    assert pl["positive"] >= 1 and 0.0 <= pl["p"] <= 1.0
    assert pl["stat"] == pytest.approx((hit["s"] / hit["sd"] + none["s"] / none["sd"]) / 2)
