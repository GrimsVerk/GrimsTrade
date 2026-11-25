"""The pooled-2 engine (research/lib/pooled2_core.py; card research/cards/pooled-2.md).

- With no publication lag the weekly engine is pooled-1's code exactly (`decide`, `own_vol`).
- No look-ahead: weekly decisions never read a session that was not public by the Friday, and
  are unchanged when later bars change; own-vol shares ignore the last week before a reset;
  monthly positions never read a month inside the gap.
- The pooled test: a variant identical to its twin gives D = 0 in every draw; month cells give
  the same Sharpe as the returns themselves.
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


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def qc() -> ModuleType:
    pytest.importorskip("numpy")
    sys.path.insert(0, str(LIB))
    _load("pooled1_core")
    return _load("pooled2_core")


def market(seed: int, years: float = 6.0, vol: float = 0.12) -> tuple[Any, Any]:
    import numpy as np

    rng = np.random.default_rng(seed)
    days: list[int] = []
    d = date(1981, 1, 2)
    while len(days) < int(252 * years):
        if d.weekday() < 5:
            days.append(d.toordinal())
        d += timedelta(days=1)
    drift = np.repeat(rng.choice([-0.3, 0.3], len(days) // 60 + 1), 60)[: len(days)] / 252
    lr = drift + rng.normal(0, vol / math.sqrt(252), len(days))
    lr[0] = 0.0
    return np.array(days, dtype=np.int64), 100 * np.exp(np.cumsum(lr))


def next_bday(o: int) -> int:
    x = date.fromordinal(o) + timedelta(days=1)
    while x.weekday() >= 5:
        x += timedelta(days=1)
    return x.toordinal()


def monday_after(o: int) -> int:
    x = date.fromordinal(o)
    return (x + timedelta(days=7 - x.weekday())).toordinal()


@pytest.mark.parametrize("seed", [1, 2])
def test_zero_lag_is_pooled1(qc: ModuleType, seed: int) -> None:
    import numpy as np

    pc = sys.modules["pooled1_core"]
    d, px = market(seed)
    mine = qc.decide_weekly(d, px, d.copy())
    ref = pc.decide(d, px)
    assert mine.first_ok == ref.first_ok
    for r in ("tsmom12", "e4"):
        assert mine.at[r] == ref.at[r]
    m = pc.run_market("x", "g", d, px)
    a, pa = qc.own_vol_weekly(d, m.daily["tsmom12"], m.pos["tsmom12"], m.start, 0.7, skip=0)
    b, pb = pc.own_vol(d, m.daily["tsmom12"], m.pos["tsmom12"], m.start, 0.7)
    assert np.array_equal(a, b) and pa == pb


@pytest.mark.parametrize("lagger", [next_bday, monday_after])
def test_signal_reads_only_public_sessions(qc: ModuleType, lagger: Any) -> None:
    import numpy as np

    pc = sys.modules["pooled1_core"]
    d, px = market(3)
    av = np.array([lagger(int(o)) for o in d], dtype=np.int64)
    full = qc.decide_weekly(d, px, av)
    checked = 0
    for fri, j in pc.fridays(d)[260::7]:
        public = av <= fri
        last_public = int(np.nonzero(public)[0].max())
        assert last_public < j or not public[j]  # the Friday's own close is never public yet
        alt = px.copy()
        alt[last_public + 1 :] *= 0.5  # not yet public at the Friday: must not matter
        dec = qc.decide_weekly(d, alt, av, upto=j)
        for r in ("tsmom12", "e4"):
            assert dec.at[r][j] == full.at[r][j]
        checked += 1
    assert checked > 5


@pytest.mark.parametrize("seed", [4, 5])
def test_weekly_decisions_do_not_use_later_bars(qc: ModuleType, seed: int) -> None:
    import numpy as np

    d, px = market(seed)
    av = np.array([next_bday(int(o)) for o in d], dtype=np.int64)
    full = qc.decide_weekly(d, px, av)
    for cut in (400, 777, len(px) - 30):
        part = qc.decide_weekly(d[: cut + 1], px[: cut + 1].copy(), av[: cut + 1])
        for r, at in full.at.items():
            for j, v in at.items():
                if j < cut:
                    assert part.at[r][j] == v, (r, j)


def test_own_vol_skips_the_last_week(qc: ModuleType) -> None:
    import numpy as np

    pc = sys.modules["pooled1_core"]
    d, px = market(7, years=8)
    m = pc.run_market("x", "g", d, px)
    x, g = m.daily["tsmom12"], m.pos["tsmom12"]
    _, plan = qc.own_vol_weekly(d, x, g, m.start, 0.7, skip=1)
    resets = [k for k in sorted(plan) if k > m.start + 3 * 252]
    assert len(resets) > 10
    for k in resets[::5]:
        x2 = x.copy()
        late = d >= d[k] - 7  # the last week before the reset (and everything after)
        x2[late] = np.where(g[late] > 0, 0.05, -0.05)
        _, plan2 = qc.own_vol_weekly(d, x2, g, m.start, 0.7, skip=1)
        assert plan2[k] == pytest.approx(plan[k], abs=1e-12)
    assert all(0.0 <= v <= 1.0 for v in plan.values())


@pytest.mark.parametrize("gap", [0, 1, 2, 3])
def test_monthly_positions_respect_the_gap(qc: ModuleType, gap: int) -> None:
    import numpy as np

    rng = np.random.default_rng(gap)
    r = rng.normal(0.002, 0.03, 300)
    pos, first = qc.decide_monthly(r, gap)
    assert first == 12 + gap
    for t in (first, 50, 151, 299):
        r2 = r.copy()
        r2[t - gap :] = -0.2  # returns t-gap.. are inside the gap or later
        pos2, _ = qc.decide_monthly(r2, gap)
        for k in pos:
            assert pos2[k][t] == pos[k][t]
    lv = np.concatenate([[1.0], np.cumprod(1 + r)])
    t = 100
    assert pos["tsmom12"][t] == float(lv[t - gap] > lv[t - gap - 12])


@pytest.mark.parametrize("gap", [1, 2])
def test_monthly_own_vol_uses_only_the_past(qc: ModuleType, gap: int) -> None:
    import numpy as np

    rng = np.random.default_rng(10 + gap)
    x = rng.normal(0.003, 0.03, 400) * np.repeat(rng.choice([0.5, 2.0], 40), 10)
    g = (rng.random(400) > 0.3).astype(float)
    start = 14
    _, plan = qc.own_vol_monthly(x, g, start, gap)
    late = [t for t in sorted(plan) if t > start + 36 + 30]
    assert late and len({round(plan[t], 6) for t in late}) > 5  # sizing is active
    for t in late[::20]:
        x2 = x.copy()
        x2[t - gap :] = 0.3
        _, plan2 = qc.own_vol_monthly(x2, g, start, gap)
        assert plan2[t] == pytest.approx(plan[t], abs=1e-12)


def _mkt(qc: ModuleType, name: str, freq: str, n: int, seed: int, first: date) -> Any:
    import numpy as np

    rng = np.random.default_rng(seed)
    step = 7 if freq == "w" else 31
    per = []
    x = first
    for _ in range(n):
        per.append(x.toordinal())
        x = x + timedelta(days=step)
        if freq == "m":
            x = x.replace(day=1)
    m = qc.Mkt(name, "G", freq, np.array(per, dtype=np.int64))
    base = rng.normal(0.002, 0.02, n)
    m.rets = {"tsmom12": base, "e4": base.copy(), "vt-own-70-x": base * 0.5 + 0.001}
    return m


def test_identical_variant_zero_and_cells_match_sharpe(qc: ModuleType) -> None:
    import numpy as np

    ms = [
        _mkt(qc, "a", "w", 900, 1, date(1990, 1, 5)),
        _mkt(qc, "b", "m", 300, 2, date(1985, 1, 1)),
        _mkt(qc, "c", "w", 500, 3, date(2000, 1, 7)),
    ]
    c = qc.cells(ms)
    bt = qc.bootstrap(c, {"all": np.ones(3, bool)}, block=12, draws=60)
    assert np.allclose(bt.d[0], 0.0)
    assert np.allclose(bt.draws[0, 0], 0.0)
    assert np.std(bt.draws[0, 1]) > 0
    sh = qc.sharpe_from(
        *(s.sum(-1) for s in c.S), np.array([52.0, 12.0, 52.0]), np.array([52.0, 12.0, 52.0])
    )
    for i, m in enumerate(ms):
        assert sh[0, i] == pytest.approx(qc.stats(m, "tsmom12")[0])


def test_gold_reader_stops_before_the_held_out_year(tmp_path: Path) -> None:
    sys.path.insert(0, str(LIB))
    p2 = _load("pooled2")
    f = tmp_path / "monthly.csv"
    f.write_text("Date,Price\n2025-09,1.0\n2025-10,2.0\n2025-11,3.0\n2026-01,x\n")
    assert list(p2._gold_lines(f)) == ["Date,Price\n", "2025-09,1.0\n", "2025-10,2.0\n"]
