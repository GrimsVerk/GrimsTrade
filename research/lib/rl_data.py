"""Build and cache the RL input tables (run rl-1), and check the simulator on real prices.

    uv run python research/lib/rl_data.py          # build research/data/rl/tables.pkl, check

Books: `six` (the live assets, decisions 1994-02-04 to 2025-11-07), `gspc` (S&P 500 index,
1962 to 1993-01-28, training only), and the out-of-universe sets `etf`, `coin`, `idx`. Train
bars only (`harness.load_history("train")`). The pickle holds our own arrays, nothing downloaded.
"""

from __future__ import annotations

import pickle
import sys
from datetime import date

import harness
import numpy as np
import rl_env
import rl_sim
from harness import OOU_COINS, OOU_ETFS, OOU_INDEXES, SYMS, TRAIN_END, TRAIN_START

from grimstrade import gym

PATH = harness.DATA / "rl" / "tables.pkl"
WARMUP_END = date(1993, 1, 28)


def books() -> dict[str, tuple[dict[str, list[harness.Bar]], date, date]]:
    gspc = harness.load_history("train", True, ["GSPC"])
    gspc["GSPC"] = [b for b in gspc["GSPC"] if date(1961, 1, 1) <= b.date <= WARMUP_END]
    return {
        "six": (harness.load_history("train"), TRAIN_START, TRAIN_END),
        "gspc": (gspc, date(1962, 1, 1), WARMUP_END),
        "etf": (harness.load_history("train", True, OOU_ETFS), TRAIN_START, TRAIN_END),
        "coin": (harness.load_history("train", True, OOU_COINS), TRAIN_START, TRAIN_END),
        "idx": (harness.load_history("train", True, OOU_INDEXES), TRAIN_START, TRAIN_END),
    }


def build() -> dict[str, rl_env.Table]:
    out = {}
    for name, (hist, a, b) in books().items():
        out[name] = rl_env.build_table(hist, rl_env.macro_vector, a, b)
        print(name, len(out[name].fridays), "Fridays", out[name].book.syms, flush=True)
    PATH.parent.mkdir(parents=True, exist_ok=True)
    with PATH.open("wb") as f:
        pickle.dump(out, f)
    return out


def load() -> dict[str, rl_env.Table]:
    with PATH.open("rb") as f:
        return pickle.load(f)  # type: ignore[no-any-return]


def check(tables: dict[str, rl_env.Table]) -> None:
    """Random weekly weights 2000-2025 on the six assets: batched replay == gym.simulate."""
    hist = harness.load_history("train")
    t = tables["six"]
    rng = np.random.default_rng(42)
    i0 = t.index(date(2000, 1, 7))
    n = len(t.fridays) - i0
    w = rng.dirichlet(np.ones(len(t.book.syms) + 1), size=n)[:, :-1] * t.elig[i0:]
    w = np.where(w > 1e-6, w, 0.0)
    decs = rl_env.daily_decisions(t, i0, w, TRAIN_END)
    res = gym.simulate(decs, hist)
    days, eq = harness._calendar(res.equity)
    daily = [np.array([d.weights.get(s, 0.0) for s in t.book.syms]) for d in decs]
    got = rl_sim.replay_daily(t.book, days[0], daily)
    m = min(len(got), len(eq))
    err = float(np.max(np.abs(got[:m] / eq[:m] - 1)))
    print(f"real-data check: {len(res.fills)} fills, {m} days, max relative error {err:.1e}")
    if err > 1e-9:
        sys.exit("batched replay differs from gym.simulate")


if __name__ == "__main__":
    check(build())
