"""Research run trend-1926 (research/lib/trend_1926.py): French daily returns through the gym.

- The loader reads only the value-weighted block, marks missing values, and parses nothing
  after its last date.
- The bars carry the returns exactly, and the two fill conventions mean what the card says:
  a hand replay of `tsmom12` (no gym, no harness) gives the gym's equity on every day, for a
  fill at the signal's own close (primary) and for a fill one session later (`late`).
- In/out states, spells, the rotation test, the window cuts and the T-bill re-scoring.
"""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from grimstrade import data

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
FIRST = date(1930, 1, 2)
HOLIDAYS = {date(1930, 7, 4), date(1931, 12, 25), date(1932, 1, 1)}
SLIP = 0.0002


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    saved_mods = {k: sys.modules.get(k) for k in ("harness", "common", "trend_tune", "stats")}
    sys.path.insert(0, str(LIB))
    mods: dict[str, ModuleType] = {}
    for name in ("harness", "common", "trend_1926"):
        spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        mods[name] = mod
    yield mods
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path
    for k, v in saved_mods.items():
        if v is None:
            sys.modules.pop(k, None)
        else:
            sys.modules[k] = v


def sessions(n_days: int) -> list[date]:
    """Six sessions a week (Saturdays included, as before 1952), a few holidays."""
    out = []
    for k in range(n_days):
        d = FIRST + timedelta(days=k)
        if d.weekday() != 6 and d not in HOLIDAYS:
            out.append(d)
    return out


def wave(days: list[date], seed: int = 1) -> list[float]:
    """Daily returns with a slow up-and-down drift, so the 12-month signal flips now and then."""
    rng = random.Random(seed)
    return [
        round(rng.gauss(0.002 * math.sin(2 * math.pi * k / 400), 0.01), 4) for k in range(len(days))
    ]


# --- loader ---

FACTORS = """This file was created by using the 202609 CRSP database.

,Mkt-RF,SMB,HML,RF
19260701,    0.09,   -0.23,   -0.28,    0.01
19260702,    0.45,   -0.34,   -0.03,    0.01
19611229,   -0.10,    0.00,    0.00,    0.02
19620102,    9.99,    0.00,    0.00,    0.02

Copyright
"""

INDUSTRY = """Missing data are indicated by -99.99 or -999.

  Average Value Weighted Returns -- Daily
,NoDur,Durbl,Manuf,Enrgy,HiTec,Telcm,Shops,Hlth,Utils,Other
19260701,   0.02,  -0.28,  -0.23,   0.57,  -0.21,  -0.02,  -0.01, -99.99,   0.61,   0.20
19260702,   0.29,   1.07,   0.81,   0.64,   0.36,   0.26,   0.01,   0.13,   0.47,   0.10


  Average Equal Weighted Returns -- Daily
,NoDur,Durbl,Manuf,Enrgy,HiTec,Telcm,Shops,Hlth,Utils,Other
19260701,   7.00,   7.00,   7.00,   7.00,   7.00,   7.00,   7.00,   7.00,   7.00,   7.00
19260706,   7.00,   7.00,   7.00,   7.00,   7.00,   7.00,   7.00,   7.00,   7.00,   7.00
"""


def test_factors_total_return_and_cut(lib: dict[str, ModuleType]) -> None:
    t = lib["trend_1926"]
    fac = t.parse_factors(FACTORS.splitlines())
    assert list(fac) == [date(1926, 7, 1), date(1926, 7, 2), date(1961, 12, 29)]  # 1962 not parsed
    mkt, rf = fac[date(1926, 7, 1)]
    assert mkt == pytest.approx(0.0010) and rf == pytest.approx(0.0001)  # Mkt-RF + RF


def test_industries_value_weighted_block_only(lib: dict[str, ModuleType]) -> None:
    t = lib["trend_1926"]
    ind = t.parse_industries(INDUSTRY.splitlines())
    assert list(ind) == [date(1926, 7, 1), date(1926, 7, 2)]  # the equal-weighted block is not read
    assert ind[date(1926, 7, 1)][0] == pytest.approx(0.0002)
    assert math.isnan(ind[date(1926, 7, 1)][7])  # -99.99 is missing, not a 100% loss
    bad = INDUSTRY.replace("NoDur,Durbl", "Durbl,NoDur")
    with pytest.raises(ValueError):
        t.parse_industries(bad.splitlines())


def test_bars_carry_the_returns(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    t = lib["trend_1926"]
    days = sessions(30)
    ret = np.array(wave(days))
    ret[5] = math.nan
    for late in (False, True):
        bars = t.bars(days, ret, late)
        assert [b.date for b in bars] == days[:5] + days[6:]  # a missing return gives no bar
        kept = [x for x in ret if not math.isnan(x)]
        prev = 100.0
        for b, x in zip(bars, kept, strict=True):
            assert b.close == pytest.approx(prev * (1 + x), rel=1e-12)
            assert b.open == (b.close if late else prev)
            prev = b.close


# --- fidelity: a hand replay against the gym, for both fill conventions ---


def hand_replay(days: list[date], ret: list[float], start: date, late: bool) -> dict[date, float]:
    """`tsmom12` on one asset from the rules as written on the card: signal from the bars up to
    the last Friday on or before the decision day, a decision every day, filled at the next
    session's open. Primary: the open is the previous close. Late: the open is that day's close."""
    close = [100.0]
    for x in ret:
        close.append(close[-1] * (1 + x))
    close = close[1:]
    eq, pos = 1.0, False
    out: dict[date, float] = {}
    for i, d in enumerate(days):
        if d <= start:
            continue
        ratio = close[i] / close[i - 1]
        decided = d - timedelta(days=1)  # the decision in force at this bar's open
        friday = decided - timedelta(days=(decided.weekday() - 4) % 7)
        seen = [k for k, x in enumerate(days) if x <= friday]
        last = seen[-1]
        target = days[last] - timedelta(days=365)
        base = max((k for k in seen if days[k] <= target), default=None)
        want = len(seen) >= 252 and base is not None and close[last] > close[base]
        if late and pos:
            eq *= ratio  # the session belongs to the position held before the late fill
        if want != pos:
            eq = eq / (1 + SLIP) if want else eq * (1 - SLIP)
            pos = want
        if not late and pos:
            eq *= ratio
        out[d] = eq
    return out


@pytest.mark.parametrize("late", [False, True])
def test_gym_matches_hand_replay(lib: dict[str, ModuleType], late: bool) -> None:
    np: Any = pytest.importorskip("numpy")
    t, h, c = lib["trend_1926"], lib["harness"], lib["common"]
    days = sessions(1500)
    ret = wave(days)
    raw = t.Raw("test", days, {"X": np.array(ret)}, np.zeros(len(days)))
    u = t.universe(raw, ["X"], "X", late)
    start = FIRST + timedelta(days=400)
    run = h.run("t", "rule", t.rule(), panel=u.panel, history=u.hist, start=start,
                end=u.end, log=False)  # fmt: skip
    want = hand_replay(days, ret, start, late)
    got = dict(zip(run.days, run.equity / 10_000.0, strict=True))
    flips = sum(1 for a, b in zip(run.decisions, run.decisions[1:], strict=False)
                if bool(a.weights) != bool(b.weights))  # fmt: skip
    assert flips >= 4  # the rule really trades in this fixture
    for d in days:
        if start < d <= u.end:
            assert got[d] == pytest.approx(want[d], rel=1e-9), d
    assert c.eligible(u.panel.view(h.decide_time(start)), "F-X")


# --- in and out, spells, the rotation test, windows, cash ---


def test_states_and_spells(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    t = lib["trend_1926"]
    state = t.states(10, 2, {2: True, 4: False, 6: True, 9: False})
    assert state.tolist() == [False, False, True, True, False, False, True, True, True, False]
    dates = [FIRST + timedelta(days=k) for k in range(10)]
    o = np.array([10.0, 10, 10, 10, 8, 9, 12, 12, 12, 6])
    cl = np.array([10.0, 10, 10, 8, 9, 12, 12, 12, 6, 3])
    sp = t.spells_of(dates, o, cl, state, 2)
    assert [(s.out, s.back, s.closed) for s in sp] == [
        (dates[4], dates[6], True),
        (dates[9], dates[9], False),
    ]
    assert sp[0].move == pytest.approx(math.log(12 / 8))  # sold at 8, bought back at 12: whipsaw
    assert sp[1].move == pytest.approx(math.log(3 / 6))  # still out: marked at the last close


def test_rotation_p_sees_rough_days_out(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    t = lib["trend_1926"]
    rng = np.random.default_rng(0)
    n = 4000
    state = np.ones(n, bool)
    for a in (300, 1500, 2900):
        state[a : a + 250] = False
    calm = rng.normal(0, 0.01, n)
    rough = np.where(state, calm, calm * 3)
    assert t.rotation_p(rough, state, draws=400) < 0.02
    assert t.rotation_p(calm, state, draws=400) > 0.10


def test_window_masks(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    t = lib["trend_1926"]
    w = {x.key: x for x in t.WINDOWS}
    ords = np.array([date(y, 6, 30).toordinal() for y in (1928, 1929, 1932, 1933, 1945, 1946)])
    assert w["whole"].mask(ords).all()
    assert w["1927-45"].mask(ords).tolist() == [True, True, True, True, True, False]
    assert w["1946-61"].mask(ords).tolist() == [False, False, False, False, False, True]
    assert w["d1"].mask(ords).tolist() == [True, False, False, True, True, True]
    assert w["d3"].mask(ords).tolist() == [False, False, False, True, True, True]
    edge = np.array([date(1929, 9, 2).toordinal(), date(1929, 9, 3).toordinal(),
                     date(1932, 7, 8).toordinal(), date(1932, 7, 9).toordinal()])  # fmt: skip
    assert w["d2"].mask(edge).tolist() == [True, False, False, True]


def test_above_bills(lib: dict[str, ModuleType]) -> None:
    np: Any = pytest.importorskip("numpy")
    t, h = lib["trend_1926"], lib["harness"]
    days = sessions(1200)
    raw = t.Raw("test", days, {"X": np.array(wave(days))}, np.full(len(days), 0.0001))
    u = t.universe(raw, ["X"], "X")
    start = FIRST + timedelta(days=400)
    rf = dict.fromkeys(days, 0.0001)
    kw: dict[str, Any] = {"panel": u.panel, "history": u.hist, "start": start, "end": u.end,
                          "log": False}  # fmt: skip
    held = h.run("t", "hold", t.hold(), **kw)
    ex = t.above_bills(held, rf)
    is_session = np.array([d in rf for d in held.days[1:]])
    assert np.allclose(ex, held.rets - 0.0001 * is_session)  # fully invested: return minus bills
    ruled = h.run("t", "rule", t.rule(), **kw)
    ex = t.above_bills(ruled, rf)
    decs = ruled.decisions
    flat = np.array([not a.weights and not b.weights for a, b in zip(decs, decs[1:], strict=False)])
    assert flat.sum() > 50
    # flat[k]: out at the decisions of days k and k+1, so the exit fill (and its cost) is past
    # by the return from day k+1 to k+2: in cash it earns the bill, which is zero above it
    assert np.allclose(ex[1 : len(flat) + 1][flat[: len(ex) - 1]], 0.0)
