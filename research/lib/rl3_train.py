"""Train the rl-3 planted-signal controls (research/rl-3.md): RL 2's trainer, unchanged, on RL 2's
tables with the planted input `peek` appended.

    uv run --with torch python research/lib/rl3_train.py <config> <seed> [fold years...]

Configs: `plant-lin-<rho>` (= res-lin), `plant-mlp-<rho>` (= res-mlp) for rho in RHOS, and the
pre-registered diagnostics `diag-long-<rho>` (MLP, 300 updates, checkpoints every 25) and
`diag-noes-<rho>` (MLP, 60 updates, last checkpoint kept). Saves
research/data/rl/models3/<config>/s<seed>/<Y>.pt (git-ignored) and log.jsonl.
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import rl2_data
import rl2_train as R
import rl3_plant
import torch
from rl2_env import RTable

MODELS = Path(os.environ.get("RL_MODELS", str(rl2_data.harness.DATA / "rl" / "models3")))
RHOS = ["0.00", "0.02", "0.05", "0.10", "0.20"]
BASE = {"lin": R.VARIANTS["res-lin"], "mlp": R.VARIANTS["res-mlp"]}


@dataclass(frozen=True)
class PVariant(R.Variant):
    rho: float = 0.0

    @property
    def a_dim(self) -> int:
        return R.A_DIM + 1  # + peek


def config(name: str) -> tuple[PVariant, int, int, bool]:
    """-> (variant, max updates, eval every, keep last)."""
    kind, arm, rho = name.split("-")
    if kind == "plant":
        b, upd, every, last = BASE[arm], 60, 5, False
    elif kind == "diag" and arm == "long":
        b, upd, every, last = BASE["mlp"], 300, 25, False
    elif kind == "diag" and arm == "noes":
        b, upd, every, last = BASE["mlp"], 60, 5, True
    else:
        raise ValueError(name)
    return PVariant(name, b.hidden, b.books, rho=float(rho)), upd, every, last


def tables(rho: float) -> dict[str, RTable]:
    tabs = rl2_data.load()
    return {k: rl3_plant.plant(tabs[k], rho, s) for k, s in rl3_plant.SEEDS.items()}


def main() -> None:
    torch.set_num_threads(1)
    v, upd, every, last = config(sys.argv[1])
    R.MAX_UPDATES, R.EVAL_EVERY, R.KEEP_LAST = upd, every, last
    seed = int(sys.argv[2])
    years = [int(y) for y in sys.argv[3:]] or R.FOLDS
    dev = torch.device("cpu")
    tabs = tables(v.rho)
    out = MODELS / v.name / f"s{seed}"
    out.mkdir(parents=True, exist_ok=True)
    for y in years:
        if (out / f"{y}.pt").exists():
            continue
        t0 = time.time()
        net, sc, info = R.train_fold(v, tabs, y, seed, dev)
        torch.save({"state": net.state_dict(), "scaler": sc.__dict__, "hidden": v.hidden,
                    **info}, out / f"{y}.pt")  # fmt: skip
        rec = {"variant": v.name, "seed": seed, "fold": y, "seconds": round(time.time() - t0, 1),
               "max_updates": upd, **info}  # fmt: skip
        with (out / "log.jsonl").open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
