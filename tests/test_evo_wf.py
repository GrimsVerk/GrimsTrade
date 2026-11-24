"""The evo-1 worlds and walk-forward driver do what the card says, on a small synthetic world.

Worlds (`evo_world`):
- a shuffled world keeps every asset's (overnight, open-to-close) pairs, only reordered, and has
  zero total log return; a block world draws blocks of consecutive pairs; both are fixed by
  their seed; a `simple` world has zero mean simple daily return;
- the planted edge is exactly `+k s` on the open-to-close part of every bar a Friday decision
  trades into when `H` holds on that Friday's inputs (`evo_feat`), `-k s` when not.

Driver (`evo_wf`, with a tiny population and few fits):
- a fit dated `D` gives the same fitness when every bar from `D` on is scrambled;
- the walk-forward is repeatable, `evo-top1` takes the fittest candidate, `evo-val` starts at
  the second fit, the out-of-sample weights are zero before the first traded fit, and the gym
  replay of the procedure stays close to the fast scorer;
- the replay statistic is the best procedure's Sharpe difference to `tsmom12`, and `tsmom12`
  chosen at every fit scores exactly 0.
"""

from __future__ import annotations

import importlib
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
from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    names = ("harness", "evo_gp", "evo_feat", "evo_score", "evo_world", "evo_wf", "stats")
    mods = {n: importlib.import_module(n) for n in names}
    # harness registers its extra symbols on first import only; another module may have reset them
    data.UNIVERSE.update(mods["harness"].UNIVERSE_EXTRA)
    yield mods
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path


def _bars(
    seed: int, first: date, last: date, coin: bool, scramble: date | None = None
) -> list[Bar]:
    rng = random.Random(seed)
    late = random.Random(seed + 99)
    out, px, trend = [], 100.0, 0.0
    d = first
    while d <= last:
        if coin or d.weekday() < 5:
            trend = 0.98 * trend + rng.gauss(0, 0.0003)
            r = rng.gauss(trend, 0.03 if coin else 0.012)
            g = rng.gauss(0, 0.003)
            if scramble is not None and d >= scramble:
                r, g = late.gauss(0, 0.05), late.gauss(0, 0.01)
            o = px * math.exp(g)
            px = o * math.exp(r)
            out.append(Bar(d, o, max(o, px), min(o, px), px, 1.0))
        d += timedelta(days=1)
    return out


def _world(lib: dict[str, ModuleType], scramble: date | None = None) -> Any:
    ew = lib["evo_world"]
    end = date(2021, 6, 30)
    six = {
        "SPY": _bars(1, date(2014, 1, 2), end, False, scramble),
        "GLD": _bars(2, date(2014, 6, 2), end, False, scramble),
        "BTC": _bars(3, date(2015, 1, 1), end, True, scramble),
    }
    gspc = {"GSPC": _bars(4, date(2008, 1, 2), date(2015, 12, 31), False, scramble)}
    sd = {s: ew._sd(b) for s, b in {**six, **gspc}.items()}
    return ew.World(six, gspc, sd, "synthetic")


@pytest.fixture
def small(lib: dict[str, ModuleType], monkeypatch: pytest.MonkeyPatch) -> Any:
    wf = lib["evo_wf"]
    monkeypatch.setattr(wf, "SIX_START", date(2015, 2, 2))
    monkeypatch.setattr(wf, "SIX_END", date(2021, 6, 25))
    monkeypatch.setattr(wf, "GSPC_START", date(2009, 1, 5))
    monkeypatch.setattr(wf, "GSPC_END", date(2015, 12, 30))
    monkeypatch.setattr(wf, "OOS_START", wf.first_friday(2019))
    monkeypatch.setattr(wf, "FIT_YEARS", (2018, 2019, 2020))
    monkeypatch.setattr(wf, "SEEDS", 2)
    monkeypatch.setattr(wf, "POPULATION", 24)
    monkeypatch.setattr(wf, "GENERATIONS", 2)
    monkeypatch.setattr(wf, "CANDIDATES", 5)
    return wf


def test_worlds_reorder_pairs_and_take_out_the_drift(lib: dict[str, ModuleType]) -> None:
    import numpy as np

    ew = lib["evo_world"]
    real = _world(lib)
    for kind in ("shuffle", "block"):
        a, b = ew.world(real, kind, 1), ew.world(real, kind, 1)
        assert a.six == b.six and a.gspc == b.gspc  # fixed by the seed
        assert ew.world(real, kind, 2).six != a.six
        for s, bars in {**a.six, **a.gspc}.items():
            src = real.six.get(s) or real.gspc[s]
            assert [x.date for x in bars] == [x.date for x in src]
            assert abs(math.log(bars[-1].close / bars[0].close)) < 1e-9
            on, oc = ew._pairs(bars)
            on0, _ = ew._pairs(src)
            if kind == "shuffle":
                assert np.allclose(np.sort(on), np.sort(on0))
            else:
                pos = {round(float(x), 10): i for i, x in enumerate(on0)}
                steps = np.diff([pos[round(float(x), 10)] for x in on])
                assert (steps == 1).mean() > 0.9  # mostly runs of consecutive bars


def test_zero_mean_simple_return_worlds(lib: dict[str, ModuleType]) -> None:
    import numpy as np

    ew = lib["evo_world"]
    real = _world(lib)
    w = ew.world(real, "shuffle", 1, zero="simple")
    assert w.label == "shuffle 1 zero-mean"
    for s, bars in w.six.items():
        cl = np.array([b.close for b in bars])
        assert abs((cl[1:] / cl[:-1] - 1).mean()) < 1e-12
        on, _ = ew._pairs(bars)
        on0, _ = ew._pairs(ew.world(real, "shuffle", 1).six[s])
        assert np.allclose(on, on0)  # same draw, only the shift differs


def test_plant_follows_h_on_the_world_inputs(lib: dict[str, ModuleType]) -> None:
    import numpy as np

    names = ("evo_world", "evo_feat", "evo_score", "evo_gp", "harness")
    ew, ef, es, gp, h = (lib[n] for n in names)
    base = ew.world(_world(lib), "shuffle", 3)
    k = 0.05
    planted = ew.plant(base, k)
    checked = 0
    for s in ("SPY", "BTC"):
        bars0, bars1 = base.six[s], planted.six[s]
        _, oc0 = ew._pairs(bars0)
        _, oc1 = ew._pairs(bars1)
        diff = (oc1 - oc0) / (k * base.sd[s])
        panel = h.Panel({s: bars1})
        fridays = es.fridays_between(bars1[400].date, bars1[-10].date)
        feats, _ = ef.friday_feats(panel, fridays)
        hold = gp.evaluate(ew.H_RULE[1][1], feats)[:, 0]
        opens = [data.open_time(data.UNIVERSE[s], b.date) for b in bars1]
        for t, f in enumerate(fridays[:-1]):
            lo = next(i for i, o in enumerate(opens) if o > h.decide_time(f))
            assert diff[lo - 1] == pytest.approx(1.0 if hold[t] else -1.0)
            checked += 1
        assert hold.any() and not hold.all()
    assert checked > 300
    assert np.isfinite(diff).all()


def test_fitness_ignores_bars_from_the_fit_date(lib: dict[str, ModuleType], small: Any) -> None:
    import numpy as np

    wf, gp = small, lib["evo_gp"]
    d = wf.first_friday(2019)
    a = wf.prepare(_world(lib))
    b = wf.prepare(_world(lib, scramble=d))
    rng = np.random.default_rng(3)
    rules = [gp.TSMOM12] + [gp.random_rule(rng, 3, False) for _ in range(30)]
    fa, fb = wf.Fitness(a, d), wf.Fitness(b, d)
    later = wf.Fitness(a, wf.first_friday(2020)), wf.Fitness(b, wf.first_friday(2020))
    assert [fa(r) for r in rules] == [fb(r) for r in rules]
    assert [later[0](r) for r in rules] != [later[1](r) for r in rules]  # the scramble bites


def test_walk_forward_procedures(lib: dict[str, ModuleType], small: Any) -> None:
    import numpy as np

    wf, gp, st = small, lib["evo_gp"], lib["stats"]
    p = wf.prepare(_world(lib))
    runs = wf.search(p, workers=1)
    assert len(runs) == 3 * 2 and all(r["evaluations"] <= 24 * 3 for r in runs)
    again = wf.search(p, workers=1)
    assert [r["candidates"] for r in runs] == [r["candidates"] for r in again]
    procs = wf.select(p, runs)
    assert set(procs) == set(wf.PROCS)
    assert sorted(procs["evo-val"].chosen) == [2019, 2020]
    for y in wf.FIT_YEARS:
        best = max(c[1] for r in runs if r["year"] == y for c in r["candidates"])
        top = procs["evo-top1"].chosen[y][0]
        assert wf.Fitness(p, wf.first_friday(y))(top) == best
        assert 1 <= len(procs["evo-ens10"].chosen[y]) <= wf.ENSEMBLE
    first = int(np.searchsorted(p.six_fridays, wf.OOS_START))
    for proc in procs.values():
        w = proc.weights
        assert w is not None and not w[:first].any() and w[first:].any()
        assert (w >= 0).all() and (w.sum(axis=1) <= 1 + 1e-9).all()
        g = wf.gym_run(p, "test", proc.name, w)
        fast = p.oos_book.daily(w)
        assert len(fast) == len(g.rets)
        assert abs(st.sharpe(fast) - st.sharpe(g.rets)) < 0.05
    assert all(gp.valid(r[1]) for proc in procs.values() for rs in proc.chosen.values() for r in rs)
    st = wf.replay_stats(p, procs)
    assert st["best"] == max(st[n] for n in wf.PROCS)
    twin = wf.Procedure("twin", weights=wf.oos_weights(p, {y: [gp.TSMOM12] for y in wf.FIT_YEARS}))
    assert wf.replay_stats(p, {**procs, "evo-top1": twin})["evo-top1"] == 0.0


def test_greed_grid_and_pick_rule(lib: dict[str, ModuleType]) -> None:
    wf = lib["evo_wf"]
    assert len(wf.SETTINGS) == 6 and wf.SETTINGS["A"] == (0.01, 30)

    def res(noise: int, rec: float) -> dict[str, Any]:
        return {"noise_found": noise, "plant": {"recovery": rec}}

    grid = {"A": res(1, 0.9), "B": res(0, 0.50), "C": res(0, 0.495), "E": res(0, 0.3)}
    assert wf.pick(grid) == "C"  # B and C tie within 0.01: same generations, larger penalty
    grid["F"] = res(0, 0.492)
    assert wf.pick(grid) == "F"  # fewer generations wins the tie
    assert wf.pick({"A": res(1, 0.9)}) is None
    try:
        wf.use("E")
        assert (wf.PENALTY, wf.GENERATIONS) == (0.03, 10)
    finally:
        wf.use("A")


def test_transfer_weights_match_the_walk_forward(lib: dict[str, ModuleType], small: Any) -> None:
    import numpy as np

    wf, gp = small, lib["evo_gp"]
    real = importlib.import_module("evo_real")
    p = wf.prepare(_world(lib))
    rng = np.random.default_rng(5)
    chosen = {y: [gp.random_rule(rng, 3, False)] for y in wf.FIT_YEARS}
    got = real.chosen_weights(chosen, p.six_fridays, p.six_feats, p.six_elig)
    assert np.array_equal(got, wf.oos_weights(p, chosen))


# --- evo-2 (research/cards/evo-2.md) ---


@pytest.fixture
def evo2(lib: dict[str, ModuleType], monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    """`evo2.configure()` with every module global it touches restored afterwards."""
    gp, wf = lib["evo_gp"], lib["evo_wf"]
    for mod, names in (
        (gp, ("INPUT_SET", "MAX_NODES", "MAX_DEPTH")),
        (wf, ("IDEA", "WARMUP", "SETTING", "POPULATION", "GENERATIONS", "PENALTY")),
    ):
        for n in names:
            monkeypatch.setattr(mod, n, getattr(mod, n))
    mod = importlib.import_module("evo2")
    mod.configure()
    return mod


_KIDS = {"if": (1, 2, 3), "and": (1, 2), "or": (1, 2), "not": (1,)}


def _walk(node: Any) -> list[Any]:
    """Every node of a tree."""
    return [node] + [x for i in _KIDS.get(node[0], ()) for x in _walk(node[i])]


def _inputs(node: Any) -> set[Any]:
    out: set[Any] = set()
    for n in _walk(node):
        if n[0] in ("gtc", "ltc"):
            out.add(n[1])
        elif n[0] == "gt":
            out |= {n[1], n[2]}
    return out


def test_evo2_grammar_uses_only_the_eight_inputs(lib: dict[str, ModuleType], evo2: Any) -> None:
    import numpy as np

    gp, ew = lib["evo_gp"], lib["evo_world"]
    assert len(evo2.INPUTS8) == 8 and set(evo2.INPUTS8) <= set(gp.INPUTS)
    assert gp.valid(ew.H_RULE[1]) and gp.within_limits(ew.H_RULE[1])  # the plant is reachable
    assert gp.valid(gp.TSMOM12[1])
    rng = np.random.default_rng(7)
    pop = [gp.random_rule(rng, 2 + i % 3, full=i % 2 == 1) for i in range(300)]
    for _ in range(3000):
        a, b = pop[int(rng.integers(len(pop)))], pop[int(rng.integers(len(pop)))]
        u = rng.random()
        if u < 0.4:
            child = gp.crossover(a, b, rng)
        elif u < 0.6:
            child = gp.subtree_mutation(a, rng)
        else:
            child = gp.point_mutation(a, rng)
        pop.append(child)
    used = {x for r in pop for x in _inputs(r[1])}
    assert used == set(evo2.INPUTS8)  # every one is reachable, nothing else is
    assert all(gp.valid(r[1]) and gp.size(r[1]) <= 12 and gp.depth(r[1]) <= 5 for r in pop)
    assert any(n[0] == "gt" for r in pop for n in _walk(r[1]))  # input against input occurs


def test_evo1_draws_unchanged_by_the_narrowing_code(lib: dict[str, ModuleType]) -> None:
    import numpy as np

    gp = lib["evo_gp"]
    assert gp.INPUT_SET == gp.INPUTS
    rng = np.random.default_rng(11)
    rules = [gp.random_rule(rng, 3, False) for _ in range(50)]
    used = {x for r in rules for x in _inputs(r[1])}
    assert len(used) > 30  # the full 72 are drawn from, not the eight
    assert all(gp.valid(r[1]) for r in rules)


def test_evo2_fitness_ignores_the_index(lib: dict[str, ModuleType], small: Any, evo2: Any) -> None:
    import numpy as np

    wf, gp, ew = small, lib["evo_gp"], lib["evo_world"]
    assert wf.WARMUP is False and wf.PENALTY == 0.02 and wf.IDEA == "evo-2"
    a = _world(lib)
    other = _world(lib, scramble=date(2008, 1, 2))  # every index bar differs
    b = ew.World(a.six, other.gspc, a.sd, "b")
    pa, pb = wf.prepare(a), wf.prepare(b)
    assert pa.gspc_book is None and pa.gspc_feats is None
    rng = np.random.default_rng(2)
    rules = [gp.TSMOM12] + [gp.random_rule(rng, 3, False) for _ in range(20)]
    d = wf.first_friday(2020)
    fa, fb = wf.Fitness(pa, d), wf.Fitness(pb, d)
    assert [fa(r) for r in rules] == [fb(r) for r in rules]
    st = lib["stats"]
    six = pa.six_book.daily(gp.weights(gp.TSMOM12, pa.six_feats, pa.six_elig), before=d)
    assert fa(gp.TSMOM12) == pytest.approx(st.sharpe(six) - 0.02 * 4)
    runs = wf.search(pa, workers=1)
    procs = wf.select(pa, runs)
    assert all(gp.valid(r[1]) for p in procs.values() for rs in p.chosen.values() for r in rs)


def test_evo2_plant_calibration_hits_the_target(
    lib: dict[str, ModuleType], small: Any, evo2: Any
) -> None:
    ew = lib["evo_world"]
    base = ew.world(_world(lib), "shuffle", 4, "simple")
    k, got = evo2.calibrate(base, 1.0, tol=0.02, k_max=0.5)
    assert 0 < k < 0.5 and abs(got - 1.0) <= 0.02
    assert evo2.h_fast(ew.plant(base, k)) == got  # the world it reports is the world it builds
    with pytest.raises(RuntimeError):
        evo2.calibrate(base, 50.0, k_max=0.01)


def test_evo2_gate(evo2: Any) -> None:
    def r(found: bool) -> dict[str, bool]:
        return {"found": found}

    assert evo2.gate([r(False)] * 3, [r(True), r(True), r(False)])["pass"]
    assert not evo2.gate([r(False), r(True), r(False)], [r(True)] * 3)["pass"]
    assert not evo2.gate([r(False)] * 3, [r(True), r(False), r(False)])["pass"]
