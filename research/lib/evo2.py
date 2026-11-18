"""evo-2 (research/cards/evo-2.md): evo-1's search, narrowed, against a calibrated plant.

What evo-2 changes, all set by `configure()` on evo-1's modules (nothing else differs):

- the GP draws and mutates comparisons over 8 inputs only (`INPUTS8`), rules of at most 12
  nodes and depth 5;
- the fitness window is the six-asset book's days only (no S&P 500 index warm-up);
- one fixed greed: population 500, 10 generations, node penalty 0.02;
- rows are logged under `evo-2-control`, `evo-2-replay` and `evo-2`; scratch goes to
  `<cache_root>/derived/evo-2/`.

The plant is `evo_world.plant` (`H`) on zero-mean-simple-return shuffle worlds, with `k` found
per world by bisection so that `H`'s fast-scorer Sharpe out of sample (2000-01-07 ..
2025-11-09) hits a target ceiling.

Commands (from the repo root, `uv run python research/lib/evo2.py ...`):

- `ceilings`: calibrate `k` for worlds 34-36 at ceilings 0.8 and 0.5; log each ceiling (`H`
  through the gym) as a `control` row before any search runs on that world.
- `controls`: noise worlds 31-33 and the six planted worlds through the whole pipeline; the
  card's gate (noise 0 of 3, the 0.8 plant found in at least 2 of 3).
- `replays FIRST LAST`: replay worlds FIRST..LAST (the card: 201-240); refuses unless the gate
  passed.
- `real`: the one real search on train only (`evo_real`); refuses unless the gate passed and
  the 40 replay rows exist.
"""

from __future__ import annotations

import json
import sys
import time
from collections.abc import Callable, Sequence
from typing import Any

import evo_feat
import evo_gp as gp
import evo_score as es
import evo_wf as wf
import evo_world as ew
import stats
from harness import Panel

INPUTS8: tuple[tuple[str, int], ...] = (
    ("mom", 30),
    ("mom", 91),
    ("mom", 182),
    ("mom", 365),
    ("gap", 290),
    ("dd", 365),
    ("lvol", 30),
    ("lvol", 365),
)
MAX_NODES, MAX_DEPTH = 12, 5
POPULATION, GENERATIONS, PENALTY = 500, 10, 0.02
NOISE_WORLDS = (31, 32, 33)
PLANT_WORLDS = (34, 35, 36)
TARGETS = (0.8, 0.5)
GATE_TARGET = 0.8
REPLAY_FIRST, REPLAY_LAST = 201, 240
K_MAX, K_TOL, K_STEPS, K_GRID = 0.5, 0.01, 30, 0.005


def configure() -> None:
    """Switch evo-1's modules (and the workers they fork) to the evo-2 card."""
    gp.INPUT_SET = INPUTS8
    gp.MAX_NODES, gp.MAX_DEPTH = MAX_NODES, MAX_DEPTH
    wf.IDEA, wf.WARMUP, wf.SETTING = "evo-2", False, "evo-2"
    wf.POPULATION, wf.GENERATIONS, wf.PENALTY = POPULATION, GENERATIONS, PENALTY


def real_six() -> ew.World:
    """The real train bars of the six assets (no index: evo-2 has no warm-up)."""
    real = ew.load_real()
    return ew.World(real.six, {}, real.sd, "real")


def h_fast(w: ew.World) -> float:
    """`H`'s fast-scorer Sharpe in a world over the out-of-sample window."""
    panel = Panel(w.six)
    fridays = es.fridays_between(wf.SIX_START, wf.SIX_END)
    feats, elig = evo_feat.friday_feats(panel, fridays)
    book = es.Book(panel, fridays, wf.OOS_START, wf.SIX_END)
    return stats.sharpe(book.daily(gp.weights(ew.H_RULE, feats, elig)))


def calibrate(
    base: ew.World,
    target: float,
    score: Callable[[ew.World], float] = h_fast,
    k_max: float = K_MAX,
    tol: float = K_TOL,
    steps: int = K_STEPS,
    grid: float = K_GRID,
) -> tuple[float, float]:
    """The smallest plant strength `k` at which `H` scores `target` in `base`, and that score
    (card note of 2026-11-18 ~19:55 UTC): `k` is raised in steps of `grid` up to `k_max` until
    the score reaches the target, then bisected inside the last step until within `tol`. The
    score is not monotone in `k` (the plant drives `H`'s own 91-day trend, so a large `k` can
    push an asset into a fall `H` never leaves), hence the scan before the bisection."""
    lo, f_lo = 0.0, score(ew.plant(base, 0.0))
    if f_lo >= target:
        raise RuntimeError(f"{base.label}: H already scores {f_lo:.3f} with no plant")
    hi = None
    for i in range(1, round(k_max / grid) + 1):
        k = i * grid
        f = score(ew.plant(base, k))
        if abs(f - target) <= tol:
            return k, f
        if f > target:
            hi = k
            break
        lo = k
    if hi is None:
        raise RuntimeError(f"{base.label}: H stays below {target} for every k up to {k_max}")
    for _ in range(steps):
        k = (lo + hi) / 2
        f = score(ew.plant(base, k))
        if abs(f - target) <= tol:
            return k, f
        if f < target:
            lo = k
        else:
            hi = k
    raise RuntimeError(f"{base.label}: no k within {tol} of {target} (last {k:.5f}: {f:.3f})")


def _base(real: ew.World, seed: int) -> ew.World:
    return ew.world(real, "shuffle", seed, wf.CONTROL_ZERO)


def _load(name: str) -> Any:
    path = wf.scratch() / name
    return json.loads(path.read_text()) if path.exists() else None


def ceilings() -> None:
    real = real_six()
    out: dict[str, dict[str, Any]] = {}
    for seed in PLANT_WORLDS:
        base = _base(real, seed)
        out[str(seed)] = {}
        for target in TARGETS:
            t0 = time.process_time()
            k, fast = calibrate(base, target)
            w = ew.plant(base, k)
            p = wf.prepare(w)
            wh = gp.weights(ew.H_RULE, p.six_feats, p.six_elig)
            run = wf.gym_run(p, "evo-2-control", "H", wh)
            gym = stats.sharpe(run.rets)
            print(f"{w.label}: target {target}, k {k:.5f}, H fast {fast:.3f}, gym {gym:.3f} "
                  f"({time.process_time() - t0:.0f} CPU s)", flush=True)  # fmt: skip
            wf._log_control(
                run,
                f"{w.label}: ceiling, H itself through the gym, no search (k calibrated to a "
                f"fast-scorer ceiling of {target:g}: fast {fast:.3f})",
            )
            out[str(seed)][str(target)] = {"k": k, "fast": fast, "gym": gym}
    (wf.scratch() / "ceilings.json").write_text(json.dumps(out, indent=1))


def gate(noise: Sequence[dict[str, Any]], plants: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """The card's gate: noise found in 0 of 3 and the 0.8 plant found in at least 2 of 3."""
    noise_found = sum(bool(r["found"]) for r in noise)
    plant_found = sum(bool(r["found"]) for r in plants)
    return {
        "noise_found": noise_found,
        "plant_found": plant_found,
        "pass": noise_found == 0 and plant_found >= 2,
    }


def controls() -> None:
    cal = _load("ceilings.json")
    if cal is None:
        raise SystemExit("run `ceilings` first")
    real = real_six()
    noise = [
        wf.control("noise", str(n), real=real, context=True, tagged=True) for n in NOISE_WORLDS
    ]
    plants: dict[str, list[dict[str, Any]]] = {}
    for target in TARGETS:
        plants[str(target)] = [
            wf.control(
                "plant",
                repr(cal[str(seed)][str(target)]["k"]),
                world_seed=seed,
                real=real,
                context=target == TARGETS[0],
                tagged=True,
            )
            for seed in PLANT_WORLDS
        ]
    g = gate(noise, plants[str(GATE_TARGET)])
    g["plant_found_0.5"] = sum(bool(r["found"]) for r in plants["0.5"])
    verdict = "PASS" if g["pass"] else "FAIL"
    print(f"gate: noise found {g['noise_found']}/3, plant 0.8 found {g['plant_found']}/3 "
          f"(0.5: {g['plant_found_0.5']}/3): {verdict}", flush=True)  # fmt: skip
    (wf.scratch() / "controls.json").write_text(
        json.dumps({"noise": noise, "plants": plants, "gate": g}, indent=1, default=str)
    )


def _gate_passed() -> bool:
    c = _load("controls.json")
    return bool(c and c["gate"]["pass"])


def replays(first: int, last: int) -> None:
    if not _gate_passed():
        raise SystemExit("the controls' gate has not passed: no replay (card)")
    real = real_six()
    for seed in range(first, last + 1):
        wf.replay(seed, real)


def real_search() -> None:
    import evo_real

    if not _gate_passed():
        raise SystemExit("the controls' gate has not passed: no real search (card)")
    evo_real.main([wf.SETTING])


def main(argv: Sequence[str]) -> None:
    configure()
    if argv[:1] == ["ceilings"]:
        ceilings()
    elif argv[:1] == ["controls"]:
        controls()
    elif argv[:1] == ["replays"] and len(argv) == 3:
        replays(int(argv[1]), int(argv[2]))
    elif argv[:1] == ["real"]:
        real_search()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
