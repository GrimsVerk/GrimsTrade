"""Run every (variant, seed) of rl-1 training, a few at a time, with a GPU log.

    setsid -f uv run --with torch python research/lib/rl_launch.py

Writes research/data/rl/launch.pid (this process), launch.log (one line per finished job) and
gpu.csv (nvidia-smi every 30 s while jobs run). Stop it by the PID in launch.pid only.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

LIB = Path(__file__).resolve().parent
OUT = LIB.parents[0] / "data" / "rl"
PARALLEL = int(os.environ.get("RL_PARALLEL", "16"))
VARIANTS = ["ppo-lin", "ppo-mlp", "ppo-mlp-dd", "ppo-mlp-px", "es-lin"]
SEEDS = range(10)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "launch.pid").write_text(f"{os.getpid()}\n")
    log = (OUT / "launch.log").open("a")
    env = {**os.environ, "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
    gpu = subprocess.Popen(
        ["nvidia-smi", "--query-gpu=timestamp,utilization.gpu,memory.used,power.draw",
         "--format=csv", "-l", "30"],
        stdout=(OUT / "gpu.csv").open("a"), stderr=subprocess.DEVNULL,
    )  # fmt: skip
    jobs = [(v, s) for s in SEEDS for v in VARIANTS]
    running: list[tuple[subprocess.Popen[bytes], str, float]] = []
    while jobs or running:
        while jobs and len(running) < PARALLEL:
            v, s = jobs.pop(0)
            out = (OUT / f"train-{v}-s{s}.out").open("ab")
            p = subprocess.Popen(
                [sys.executable, str(LIB / "rl_train.py"), v, str(s)],
                stdout=out, stderr=subprocess.STDOUT, env=env,
            )  # fmt: skip
            running.append((p, f"{v} s{s}", time.time()))
        time.sleep(5)
        for item in list(running):
            p, name, t0 = item
            if p.poll() is not None:
                log.write(f"{time.strftime('%H:%M:%S')} {name} exit {p.returncode} "
                          f"{time.time() - t0:.0f}s\n")  # fmt: skip
                log.flush()
                running.remove(item)
    gpu.terminate()
    log.write("all done\n")
    log.close()


if __name__ == "__main__":
    main()
