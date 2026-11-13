"""Input tables of run rl-2: rl-1's tables plus the sector book and `tsmom12`'s base weights.

    uv run python research/lib/rl2_data.py   # build research/data/rl/tables2.pkl, check

Books: rl-1's `six`, `gspc`, `etf`, `coin`, `idx` (from research/data/rl/tables.pkl, built by
`rl_data.py`) and `sec` (the 9 sector ETFs, run 2's pooled set). The check replays zero tilt on
the six assets from 2000-01-07 through `gym.simulate` and compares it with the `tsmom12` baseline.
"""

from __future__ import annotations

import pickle
import sys
from datetime import date

import common as c
import harness
import numpy as np
import rl2_env
import rl_data
import rl_env
from harness import SECTORS, TRAIN_END, TRAIN_START

from grimstrade import gym

PATH = harness.DATA / "rl" / "tables2.pkl"
OOS_START = date(2000, 1, 7)


def histories() -> dict[str, dict[str, list[harness.Bar]]]:
    out = {k: v[0] for k, v in rl_data.books().items()}
    out["sec"] = harness.load_history("train", True, SECTORS)
    return out


def build() -> dict[str, rl2_env.RTable]:
    tabs = rl_data.load()
    hist = histories()
    tabs["sec"] = rl_env.build_table(hist["sec"], rl_env.macro_vector, TRAIN_START, TRAIN_END)
    out = {}
    for k, t in tabs.items():
        out[k] = rl2_env.base_weights(hist[k], t)
        print(k, len(t.fridays), "Fridays", t.book.syms, flush=True)
    with PATH.open("wb") as f:
        pickle.dump(out, f)
    return out


def load() -> dict[str, rl2_env.RTable]:
    with PATH.open("rb") as f:
        return pickle.load(f)  # type: ignore[no-any-return]


def check(tabs: dict[str, rl2_env.RTable]) -> None:
    """Zero tilt on the six assets == the tsmom12 baseline, day by day, through the real gym."""
    rt = tabs["six"]
    t = rt.t
    hist = harness.load_history("train")
    i0 = t.index(OOS_START)
    bd = rl2_env.base_daily(hist, t.book.syms, OOS_START, TRAIN_END)
    zero = np.zeros((len(t.fridays) - i0, 1, len(t.book.syms)))
    res = gym.simulate(rl2_env.res_decisions(rt, i0, zero, bd, TRAIN_END), hist)
    base = harness.run(
        "rl-2", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), kind="baseline",
        history=hist, start=OOS_START, log=False,
    )  # fmt: skip
    _, eq = harness._calendar(res.equity)
    m = min(len(eq), len(base.equity))
    err = float(np.max(np.abs(eq[:m] / base.equity[:m] - 1)))
    print(f"zero tilt vs tsmom12 baseline: {m} days, max relative error {err:.1e}")
    if err > 1e-12:
        sys.exit("zero tilt does not reproduce tsmom12")


if __name__ == "__main__":
    check(load() if "--check" in sys.argv else build())
