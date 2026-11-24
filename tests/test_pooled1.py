"""The pooled-1 engine (research/lib/pooled1_core.py; card research/cards/pooled-1.md).

- No look-ahead: every rule's Friday decisions, and own-vol's reset shares, are the same when
  every later bar is removed or changed.
- The fill is one session late: a decision on session j's close earns from session j + 2.
- `arm3-12` leaves at every `tsmom12` exit; OR / AND rules sit on the right side of the twin.
- The pooled test: a variant identical to its twin gives D = 0 in every draw, and the week sums
  give the same Sharpe as the weekly returns themselves.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def pc() -> ModuleType:
    pytest.importorskip("numpy")
    spec = importlib.util.spec_from_file_location("pooled1_core", LIB / "pooled1_core.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["pooled1_core"] = mod
    spec.loader.exec_module(mod)
    return mod


def market(seed: int, years: float = 4.0, vol: float = 0.25) -> tuple[Any, Any]:
    import numpy as np

    rng = np.random.default_rng(seed)
    days: list[int] = []
    d = date(2001, 1, 2)
    while len(days) < int(252 * years):
        if d.weekday() < 5:
            days.append(d.toordinal())
        d += timedelta(days=1)
    # regime drift so the trend rules switch often
    drift = np.repeat(rng.choice([-0.4, 0.4], len(days) // 60 + 1), 60)[: len(days)] / 252
    lr = drift + rng.normal(0, vol / math.sqrt(252), len(days))
    lr[0] = 0.0
    return np.array(days, dtype=np.int64), 100 * np.exp(np.cumsum(lr))


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_decisions_do_not_use_later_bars(pc: ModuleType, seed: int) -> None:
    d, px = market(seed)
    full = pc.decide(d, px)
    for cut in (300, 451, 700, len(px) - 40):
        part = pc.decide(d[: cut + 1], px[: cut + 1].copy())
        changed = px.copy()
        changed[cut + 1 :] *= 3.0  # a later crash or boom must not matter
        alt = pc.decide(d, changed, upto=cut)
        for r, at in full.at.items():
            for j, v in at.items():
                if j < cut:
                    assert part.at[r][j] == v, (r, j)
                    assert alt.at[r][j] == v, (r, j)


def test_fill_is_one_session_late(pc: ModuleType) -> None:
    h = pc.held(10, {3: 1.0, 6: 0.5})
    assert list(h) == [0, 0, 0, 0, 0, 1.0, 1.0, 1.0, 0.5, 0.5]
    paper = pc.held(10, {3: 1.0}, lag=0)
    assert paper[4] == 1.0 and paper[3] == 0.0


def test_own_vol_shares_use_only_the_past(pc: ModuleType) -> None:
    import numpy as np

    d, px = market(7, years=6)
    m = pc.run_market("x", "g", d, px)
    x, g = m.daily["tsmom12"], m.pos["tsmom12"]
    _, plan = pc.own_vol(d, x, g, m.start, 0.7)
    cut = m.start + 4 * 252
    x2 = x.copy()
    x2[cut:] = np.where(g[cut:] > 0, 0.05, 0.0)  # wild later returns
    _, plan2 = pc.own_vol(d, x2, g, m.start, 0.7)
    resets = sorted(plan)
    assert len([k for k in resets if k > m.start + 3 * 252]) > 5  # past the warm-up
    for k in resets:
        if k < cut:
            assert plan2[k] == pytest.approx(plan[k], abs=1e-12)
    assert all(0.0 <= v <= 1.0 for v in plan.values())


@pytest.mark.parametrize("seed", [4, 5])
def test_rule_shapes(pc: ModuleType, seed: int) -> None:
    dec = pc.decide(*market(seed, years=8))
    ts = dec.at["tsmom12"]
    exits = [
        j for a, j in zip(sorted(ts), sorted(ts)[1:], strict=False) if ts[a] == 1.0 and ts[j] == 0.0
    ]
    assert exits, "the test needs tsmom12 exits"
    for j in exits:
        assert dec.at["arm3-12"][j] == 0.0
    for j, v in ts.items():
        assert dec.at["or3-12"][j] >= v
        assert dec.at["fade-28"][j] <= v and dec.at["stop-0.25"][j] <= v
        assert dec.at["tv40"][j] <= v and (v == 0.0) == (dec.at["tv40"][j] == 0.0)
        assert 0.0 <= dec.at["e4"][j] <= 1.0
    assert any(dec.at["arm3-12"][j] > ts[j] for j in ts)  # it does re-enter early sometimes


def test_identical_variant_gives_zero_in_every_draw(pc: ModuleType) -> None:
    import numpy as np

    rng = np.random.default_rng(0)
    R = rng.normal(0.002, 0.02, (3, 5, 400))
    R[:, 3, :150] = np.nan  # a late starter
    R[1] = R[0]
    p = pc.Panel(np.arange(400) * 7, list("abcde"), list("ggghh"), R)
    bt = pc.bootstrap(p, {"all": np.ones(5, bool)}, block=20, draws=50)
    assert np.allclose(bt.d[0], 0.0)
    assert np.allclose(bt.draws[0, 0], 0.0)
    assert np.std(bt.draws[0, 1]) > 0


def test_week_sums_match_sharpe(pc: ModuleType) -> None:
    import numpy as np

    rng = np.random.default_rng(1)
    R = rng.normal(0.001, 0.02, (2, 1, 300))
    R[:, 0, :40] = np.nan
    sh = pc.sharpe_from(*pc.sums(R))
    assert sh[0, 0] == pytest.approx(pc.sharpe(R[0, 0, 40:]))
    # block sums over a circular window equal a direct sum
    n, s1, _ = pc.block_sums(R, 25)
    idx = [(290 + i) % 300 for i in range(25)]
    assert s1[1, 0, 290] == pytest.approx(np.nansum(R[1, 0, idx]))
    assert n[1, 0, 290] == 10  # weeks 290-299 only: 0-14 wrap into the missing start
