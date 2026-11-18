"""The deep-1 combination rules use only past sleeve returns (research/lib/deep1_mix.py)."""

from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
import pytest

PATH = Path(__file__).resolve().parents[1] / "research" / "lib" / "deep1_mix.py"
START = date(2001, 1, 1)
N = 365 * 9


@pytest.fixture(scope="module")
def mix() -> ModuleType:
    spec = importlib.util.spec_from_file_location("deep1_mix_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def world(seed: int = 0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Days, daily returns of five sleeves (column 0 is the twin) and the twin's breadth."""
    rng = np.random.default_rng(seed)
    days = np.arange(START.toordinal(), START.toordinal() + N + 1)
    base = rng.normal(0.0004, 0.01, N)
    r = np.column_stack(
        [
            base,
            base + rng.normal(0, 0.002, N),  # a near clone
            rng.normal(0.0003, 0.004, N),  # independent, calm
            0.5 * base + rng.normal(0.0002, 0.006, N),
            rng.normal(0.0005, 0.02, N),  # independent, wild
        ]
    )
    r[:800, 4] = np.nan  # a sleeve that starts late
    breadth = rng.choice([0.0, 0.5, 1.0], size=N, p=[0.3, 0.3, 0.4])
    return days, r, breadth


def test_blocks_stop_a_week_before_the_refit(mix: Any) -> None:
    r = np.full(70, 0.01)
    b, starts = mix.blocks(r, 35)
    assert list(starts) == [0, 7, 14, 21]  # the week from day 28 is still running
    assert np.allclose(b, 1.01**7 - 1)


def test_refits_are_first_fridays(mix: Any) -> None:
    days, _, _ = world()
    ks = mix.refit_days(days)
    assert len(ks) == 9
    for k in ks:
        d = date.fromordinal(int(days[k]))
        assert d.weekday() == 4 and d.month == 1 and d.day <= 7


def test_shares_ignore_the_future(mix: Any) -> None:
    days, r, breadth = world()
    pool = [1, 2, 3, 4]
    full = mix.plan(days, r, breadth, 0, pool)
    ks = mix.refit_days(days)
    rng = np.random.default_rng(1)
    for i in (3, 5, 8):
        k = ks[i]
        hi = ks[i + 1] if i + 1 < len(ks) else N
        r2, b2 = r.copy(), breadth.copy()
        r2[k - 1 :] = rng.normal(0, 0.05, r2[k - 1 :].shape)  # everything a decision cannot see
        b2[k + 1 :] = rng.choice([0.0, 0.5, 1.0], size=N - k - 1)
        cut = mix.plan(days, r2, b2, 0, pool)
        assert np.array_equal(full.stack[k:hi], cut.stack[k:hi])
        assert np.array_equal(full.meta[k:hi], cut.meta[k:hi])
        assert full.switch[k] == cut.switch[k]
        assert full.log[i - 1]["switch"] == cut.log[i - 1]["switch"]  # first refit: no data


def test_before_enough_history_the_book_is_the_twin(mix: Any) -> None:
    days, r, breadth = world()
    p = mix.plan(days, r, breadth, 0, [1, 2, 3, 4])
    first = next(k for k in mix.refit_days(days) if k // 7 - 1 >= mix.MIN_WEEKS)
    for a in (p.stack, p.meta):
        assert np.array_equal(a[:first, 0], np.ones(first))
        assert a[:first, 1:].sum() == 0
    assert (p.switch[:first] == 0).all()
    assert np.allclose(p.stack.sum(axis=1), 1) and np.allclose(p.meta.sum(axis=1), 1)
    assert (p.stack >= 0).all() and (p.meta >= 0).all()


def test_stack_picks_the_sleeve_least_like_the_twin_when_it_loses(mix: Any) -> None:
    days, r, _ = world()
    b, _ = mix.blocks(r, mix.refit_days(days)[-1])
    comp, share = mix.stack(b, 0, [1, 2, 3, 4])
    assert comp in (2, 4)  # the two independent sleeves, never the clone
    lose = b[:, 0] < 0
    assert abs(np.corrcoef(b[lose, comp], b[lose, 0])[0, 1]) < 0.2
    vt, vm = b[-156:, 0].var(), b[-156:, comp].var()
    assert share == pytest.approx((1 / vt) / (1 / vt + 1 / vm))


def test_stack_skips_a_sleeve_that_lost_money(mix: Any) -> None:
    days, r, _ = world()
    r = r.copy()
    r[:, 2] -= 0.002
    r[:, 4] -= 0.004
    b, _ = mix.blocks(r, mix.refit_days(days)[-1])
    comp, _ = mix.stack(b, 0, [2, 4])
    assert comp is None


def test_switch_holds_the_sleeve_that_was_best_in_each_state(mix: Any) -> None:
    days, r, _ = world()
    r = r.copy()
    k = mix.refit_days(days)[-1]
    _, starts = mix.blocks(r, k)
    state = np.random.default_rng(2).integers(0, 3, len(starts))
    for s, x in zip(starts, state, strict=True):
        r[s : s + 7, 3] = (0.004 if x == mix.OFF else -0.004) + 0.001 * r[s : s + 7, 3]
    b, _ = mix.blocks(r, k)
    got = mix.switch(b, state, 0, [1, 2, 3])
    assert got[mix.OFF] == 3
    assert got[mix.MIXED] != 3 and got[mix.ON] != 3


def test_meta_treats_identical_sleeves_alike(mix: Any) -> None:
    days, r, _ = world()
    r = r.copy()
    r[:, 1] = r[:, 0]
    b, _ = mix.blocks(r, mix.refit_days(days)[-1])
    shares, lam = mix.meta(b, 0, [1, 2, 3, 4])
    assert lam in mix.LAMBDAS
    assert shares.sum() == pytest.approx(1.0) and (shares >= 0).all()
    assert shares[0] == pytest.approx(shares[1])
