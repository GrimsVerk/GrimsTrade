"""The forecasters and the gate of run rl-4 do what the card says (research/rl-4.md).

- The purged CV never trains within 14 days of the rows it validates on.
- The score has no intercept, is zero for a zero forecast, and is 10 x the forecast.
- Each fit puts its largest weight on a planted input among noise inputs.
- The gate's bars are the card's.
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def sup() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    pytest.importorskip("sklearn")
    saved = list(sys.path)
    sys.path.insert(0, str(LIB))
    yield importlib.import_module("rl4_sup")
    sys.path[:] = saved


def rows(np: Any, n: int = 3000, k: int = 20, ic: float = 0.2) -> tuple[Any, Any, Any]:
    rng = np.random.default_rng(5)
    x = rng.standard_normal((n, k))
    y = ic * x[:, 3] + np.sqrt(1 - ic**2) * rng.standard_normal(n)
    days = 730_000 + 7 * (np.arange(n) // 6)  # six rows per Friday
    return x, y, days


def test_cv_is_purged(sup: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    _, _, days = rows(np)
    folds = sup.cv_folds(days)
    assert len(folds) == sup.CV_FOLDS
    assert (sum(va.astype(int) for _, va in folds) == 1).all()  # each row validated once
    for tr, va in folds:
        assert not (tr & va).any()
        gap = np.abs(days[tr][:, None] - days[va][None, ::50]).min()
        assert gap > sup.CV_GAP
        assert tr.sum() > len(days) / 2


@pytest.mark.parametrize("kind", ["ols", "ridge", "lasso"])
def test_fit_finds_the_planted_input(sup: ModuleType, kind: str) -> None:
    np: Any = pytest.importorskip("numpy")
    x, y, days = rows(np)
    f = sup.fit(kind, x, y, days)
    assert int(np.argmax(np.abs(f.beta))) == 3
    assert 0.1 < f.beta[3] < 0.3
    assert (f.penalty is None) == (kind == "ols")
    # no intercept in the score: shifting the target changes nothing
    g = sup.fit(kind, x, y + 5.0, days)
    assert np.allclose(f.score(x[:50]), g.score(x[:50]), atol=1e-6)
    # score = C x forecast on standardised inputs, and a missing input counts as its mean
    xs = (x[:50] - f.mu) / f.sd
    assert np.allclose(f.score(x[:50]), sup.C * xs @ f.beta)
    hole = x[:1].copy()
    hole[0, 3] = np.nan
    mean = x[:1].copy()
    mean[0, 3] = f.mu[3]
    assert np.allclose(f.score(hole), f.score(mean))


def test_zero_forecast_is_zero_score(sup: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    x, _, _ = rows(np)
    f = sup.Fit(x.mean(0), x.std(0), np.zeros(x.shape[1]), None)
    assert (f.score(x) == 0).all()


def test_gate_bars(sup: ModuleType) -> None:
    good = {
        "0.00": {"diff": -0.01, "p": 0.7},
        "0.10": {"diff": 0.06, "p": 0.02, "seeds_ahead": 8},
        "0.20": {"diff": 0.30, "p": 0.00},
    }
    assert all(sup.gate(good, 0.155).values())
    assert all(sup.gate(good, 0.155, rl=True).values())
    assert len(sup.gate(good, 0.155, rl=True)) == 5

    def change(rho: str, **kw: float) -> dict[str, dict[str, float]]:
        return {**good, rho: {**good[rho], **kw}}

    assert not all(sup.gate(change("0.10", p=0.2), 0.155).values())  # not significant
    assert not all(sup.gate(change("0.10", diff=0.04), 0.155).values())  # under a third
    assert not all(sup.gate(change("0.20", diff=-0.1), 0.155).values())
    assert not all(sup.gate(change("0.00", diff=-0.03), 0.155).values())  # trades noise
    assert not all(sup.gate(change("0.00", diff=0.05, p=0.01), 0.155).values())  # false find
    assert not all(sup.gate(change("0.10", seeds_ahead=6), 0.155, rl=True).values())


# --- part 2: the perp cross-section helpers (research/lib/rl4_perp.py) ---


@pytest.fixture(scope="module")
def perp(sup: ModuleType) -> ModuleType:
    return importlib.import_module("rl4_perp")


def panel(np: Any, days: int = 520, n: int = 14) -> tuple[Any, Any, Any, Any, Any]:
    rng = np.random.default_rng(11)
    px = 100 * np.exp(np.cumsum(rng.normal(0, 0.03, (days, n)), 0))
    px[:40, 0] = np.nan  # a coin listed later
    px[300:, 1] = np.nan  # a coin delisted
    fund = rng.normal(0.0003, 0.0005, (days, n))
    fund7 = rng.normal(0, 1, (days, n))
    prem7 = rng.normal(0, 1, (days, n))
    prem7[:, 2] = np.nan  # a coin without premium history
    tradable = np.isfinite(px)
    tradable[:380] = False
    return px, fund, fund7, prem7, tradable


def test_week_total_is_price_minus_funding(perp: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    px, fund, *_ = panel(np)
    t = 400
    got = perp.week_total(px, fund, t)
    want = np.log(px[t + 7, 5] / px[t, 5]) - fund[t + 1 : t + 8, 5].sum()
    assert got[5] == pytest.approx(want)
    assert np.isnan(got[1])  # no price on day t
    # a coin that stops trading inside the week exits at its last price
    px2 = px.copy()
    px2[t + 4 :, 6] = np.nan
    assert perp.week_total(px2, fund, t)[6] == pytest.approx(
        np.log(px[t + 3, 6] / px[t, 6]) - fund[t + 1 : t + 8, 6].sum()
    )


def test_rows_do_not_look_ahead(perp: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    px, fund, fund7, prem7, tradable = panel(np)
    days = perp.decision_days(tradable, 0, 505)  # day 0 is a Monday here
    assert len(days) > 10 and ((days % 7) == 4).all() and (days + 7 < len(px)).all()
    raw = perp.raw_inputs(px, fund7, prem7)
    r = perp.build_rows(px, fund, tradable, raw, days)
    k = 6
    t = int(days[k])
    # scramble everything after the decision day: the inputs of that Friday do not move
    rng = np.random.default_rng(1)
    px2, f72, p72 = px.copy(), fund7.copy(), prem7.copy()
    px2[t + 1 :] *= np.exp(rng.normal(0, 0.2, px2[t + 1 :].shape))
    f72[t + 1 :] += 5
    p72[t + 1 :] -= 5
    r2 = perp.build_rows(px2, fund, tradable, perp.raw_inputs(px2, f72, p72), days)
    assert np.allclose(r.x[k], r2.x[k]) and np.allclose(r.raw[k], r2.raw[k], equal_nan=True)
    assert not np.allclose(r.y[k], r2.y[k])  # the target is the future, and did move
    # scramble everything after the target week: that week's target does not move
    px3, fund3 = px.copy(), fund.copy()
    px3[t + 8 :] *= 3
    fund3[t + 8 :] += 1
    r3 = perp.build_rows(px3, fund3, tradable, raw, days)
    assert np.allclose(r.y[k], r3.y[k])
    # ranks are centred, missing inputs sit in the middle, coins outside the set are 0
    assert r.x[k][r.m[k]].min() == -0.5 and r.x[k][r.m[k]].max() == 0.5
    assert (r.x[:, 2, 1] == 0).all() and (r.x[:, 1] == 0).all() and not r.m[:, 1].any()


def test_fit_rows_respect_the_embargo(perp: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    day = np.array([100, 107, 114, 121])
    assert perp.usable(day, 128).tolist() == [True, True, True, False]  # 114 + 7 + 7 = 128
    ic = np.array([0.1, 0.2, -0.5, -0.5])
    sign = perp.walk_forward_sign(day, ic, [121, 128])
    assert sign.tolist() == [0.0, 0.0, 0.0, 1.0]  # at 121 only weeks 100 and 107 are usable


def test_no_position_without_a_forecast(perp: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    m = np.array([True] * 12 + [False] * 2)
    assert (perp.long_short(np.zeros(14), m) == 0).all()
    w = perp.long_short(np.arange(14.0), m)
    assert w.sum() == pytest.approx(0) and np.abs(w).sum() == pytest.approx(1)
    assert (w[8:12] > 0).all() and (w[:4] < 0).all() and (w[12:] == 0).all()
