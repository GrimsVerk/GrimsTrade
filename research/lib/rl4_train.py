"""The RL variants of run rl-4 (research/rl-4.md, card part 1): rl-3's trainer and evaluator,
unchanged, on rl-3's planted tables cut to three inputs.

    uv run --with torch python research/lib/rl4_train.py <config> <seed> [fold years...]
    uv run --with torch python research/lib/rl4_train.py --eval <config ...>   # logs control rows

Configs: `ppo3-<rho>` = rl-3's `plant-mlp` (PPO, MLP 2 x 32, 60 updates, early stopping) whose
per-asset inputs are `up_12m`, `log_vol` and `peek` only; `ppo3-warm-<rho>` = a linear score
that starts at 10 x the `ols3` coefficients of the fold's training part (the card's follow-up).
The other 15 asset inputs and the 10 macro inputs are set to zero in the tables, which removes
them from the network (a zero input moves no score and gets no gradient) without touching rl-3's
code. Models go to research/data/rl/models4/ (git-ignored); the evaluation writes
research/data/rl/eval3-<config>.json and `rl-4-control` rows in tries.md.
"""

from __future__ import annotations

import dataclasses
import os
import sys
from pathlib import Path

import numpy as np
import rl2_data
import rl2_train as R
import rl3_train
import rl4_sup
from rl2_env import RTable

MODELS = Path(os.environ.get("RL_MODELS", str(rl2_data.harness.DATA / "rl" / "models4")))
KEEP = [rl4_sup.UP12, rl4_sup.LOG_VOL, rl4_sup.PEEK]


def config(name: str) -> tuple[rl3_train.PVariant, int, int, bool]:
    """-> (variant, max updates, eval every, keep last), as `rl3_train.config`."""
    arm, rho = name.rsplit("-", 1)
    hidden = {"ppo3": 32, "ppo3-warm": 0}[arm]
    return rl3_train.PVariant(name, hidden, R.SMALL, rho=float(rho)), 60, 5, False


def tables(rho: float) -> dict[str, RTable]:
    out = {}
    for k, s in rl3_train.rl3_plant.SEEDS.items():
        rt = rl3_train.rl3_plant.plant(rl2_data.load()[k], rho, s)
        t = rt.t
        x = np.zeros_like(t.X)
        x[:, :, KEEP] = t.X[:, :, KEEP]
        out[k] = dataclasses.replace(rt, t=dataclasses.replace(t, X=x, G=np.zeros_like(t.G)))
    return out


def install() -> None:
    """Point rl-3's trainer and evaluator at this run's configs, tables and model folder."""
    rl3_train.config = config  # type: ignore[assignment]
    rl3_train.tables = tables
    rl3_train.MODELS = MODELS


def main() -> None:
    install()
    if sys.argv[1] == "--eval":
        import rl3_eval

        rl3_eval.IDEA = rl4_sup.IDEA
        for name in sys.argv[2:]:
            r = rl3_eval.evaluate(name)
            print(name, f"d {r['vs_tsmom12']['diff']:+.3f} p {r['vs_tsmom12']['p']:.2f} "
                  f"seeds ahead {r['seeds']['ahead']}", flush=True)  # fmt: skip
    else:
        rl3_train.main()


if __name__ == "__main__":
    main()
