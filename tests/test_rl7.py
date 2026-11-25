"""rl-7 learner plumbing (research/lib/rl7.py; card research/cards/rl-7.md), on made-up data.

- Features read only returns through t - 1 - gap: changing the return of month t or later
  never changes the row of month t.
- `up12` is `tsmom12`'s own signal; net returns charge cost on position changes and restart
  from flat at each segment.
- Purged folds never fit on months within the purge of the validation block.
- Both learners find a strong planted input on made-up rows and ignore pure noise.
- The split is fixed by spans and the seed: short-after-1990 series train, short-before hold.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _load(name: str) -> ModuleType:
    sys.path.insert(0, str(LIB))
    spec = importlib.util.spec_from_file_location(name, LIB / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


rl7 = _load("rl7")


def _r(n: int, seed: int = 1) -> np.ndarray:
    return np.random.default_rng(seed).normal(0.005, 0.04, n)


def test_features_use_only_the_past() -> None:
    r = _r(120)
    for gap in (0, 1, 2):
        t, X, sig = rl7.features(r, gap)
        assert t[0] == 36 + gap
        j = 30
        r2 = r.copy()
        r2[t[j] - gap :] += 0.5  # change month t - gap and later
        t2, X2, _ = rl7.features(r2, gap)
        assert t2[j] == t[j]
        np.testing.assert_allclose(X2[j], X[j])
        if gap > 0:
            r3 = r.copy()
            r3[t[j] - gap - 1] += 0.5  # the last month the row may read
            assert not np.allclose(rl7.features(r3, gap)[1][j], X[j])


def test_up12_is_tsmom12_sign() -> None:
    r = _r(100)
    t, X, _ = rl7.features(r, 1)
    lv = np.concatenate([[1.0], np.cumprod(1 + r)])
    for j, tt in enumerate(t):
        s = tt - 1
        assert X[j, rl7.FEATURES.index("up12")] == float(lv[s] / lv[s - 12] > 1)


class _S:
    def __init__(self, name: str, group: str, segs: list, gap: int = 0) -> None:
        self.name, self.group, self.cls, self.gap, self.segs = name, group, "equity", gap, segs
        self.cost = 0.001


def test_net_costs_and_segment_restart() -> None:
    rows = rl7.build_rows([_S("A", "US10", [(0, _r(40)), (100, _r(40, 2))])])
    sel = np.ones(len(rows.k), dtype=bool)
    p = np.ones(len(rows.k))
    n = rl7.net(rows, sel, p)
    starts = np.concatenate([[True], rows.seg[1:] != rows.seg[:-1]])
    np.testing.assert_allclose(n[starts], rows.r[starts] - 0.001)
    np.testing.assert_allclose(n[~starts], rows.r[~starts])


def test_purged_folds() -> None:
    k = np.repeat(np.arange(600), 3)
    for fit, val in rl7.purged_folds(k):
        lo, hi = k[val].min(), k[val].max()
        kf = k[fit]
        assert not ((kf >= lo - rl7.PURGE) & (kf <= hi + rl7.PURGE)).any()
        assert len(val) > 0 and len(fit) > 0


def test_learners_find_planted_and_ignore_noise() -> None:
    rng = np.random.default_rng(0)
    n = 6000
    y = rng.standard_normal(n) + 0.1
    X = rng.standard_normal((n, 4))
    X[:, 0] = 0.3 * y + np.sqrt(1 - 0.09) * rng.standard_normal(n)
    k = np.arange(n) // 10
    m = rl7.fit_lasso(X, y, k)
    assert m.w[0] > 0.1 and np.all(np.abs(m.w[1:]) < 0.05)
    pg = rl7.fit_pg(X, y)
    assert pg.w[0] > 0 and abs(pg.w[0]) > 3 * np.abs(pg.w[1:]).max()
    p = pg.position(X)
    assert 0 < p.min() and p.max() < 1


def test_split_rule() -> None:
    long = [(rl7.ed.mi(1950, 1), _r(900, i)) for i in range(4)]
    ss = [_S(f"L{i}", "US10", [seg]) for i, seg in enumerate(long)]
    ss.append(_S("old", "P4", [(rl7.ed.mi(1880, 1), _r(300, 9))]))
    ss.append(_S("new", "ETF8", [(rl7.ed.mi(2000, 1), _r(300, 8))]))
    rows = rl7.build_rows(ss)
    tr = rl7.split(rows)
    assert tr[4] and not tr[5]
    assert tr[:4].sum() == 2
    np.testing.assert_array_equal(tr, rl7.split(rows))
