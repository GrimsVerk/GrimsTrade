"""Smoke test of the evo-1 search and correction on a TOY world. Not the card's controls.

The toy world has no prices: every input of the grammar is drawn at random per day and asset,
and each asset's return of the day is noise plus `k` x its volatility when the card's planted
rule `H` says hold, minus that when it does not (`k` = 0: pure noise). It only shows that the
GP code and the Reality Check / SPA code work end to end. The card's controls (shuffled real
bars, inputs computed from the synthetic prices, the fast scorer, walk-forward) are a later step.

Run: `uv run python research/lib/evo_smoke.py` (prints one line per world).
"""

from __future__ import annotations

import math
import time

import evo_gp as gp
import evo_stats
import numpy as np
import stats

ASSETS = 6
SIGMA = 0.01
H: gp.Node = (
    "if",
    ("and", ("gtc", ("mom", 91), 0.0), ("gt", ("lvol", 365), ("lvol", 30))),
    ("const", 1.0),
    ("const", 0.0),
)


def toy_world(seed: int, days: int, k: float) -> tuple[gp.Feats, np.ndarray]:
    """Random inputs and the returns of the day they are known before."""
    rng = np.random.default_rng(seed)
    feats: gp.Feats = {}
    for inp in gp.INPUTS:
        fam = gp.FAMILY[inp[0]]
        if fam == "M":
            feats[inp] = rng.normal(0.0, 1.0, size=(days, ASSETS))
        elif fam == "V":
            feats[inp] = rng.normal(math.log(0.3), 0.5, size=(days, ASSETS))
        else:
            feats[inp] = rng.random(size=(days, ASSETS))
    feats["coin"] = np.arange(ASSETS) < 2
    feats["vol30"] = np.exp(feats[("lvol", 30)])
    ret = rng.normal(0.0, SIGMA, size=(days, ASSETS))
    ret += k * SIGMA * np.where(gp.evaluate(H, feats), 1.0, -1.0)
    return feats, ret


def cut(feats: gp.Feats, sl: slice) -> gp.Feats:
    return {key: (v if key == "coin" else v[sl]) for key, v in feats.items()}


def run(
    seed: int, k: float, days: int = 3000, population: int = 200, generations: int = 15
) -> dict[str, float | str]:
    """Search on the first `days`, test the search's whole universe there, then score the best
    rule on the next `days`, which the search never saw."""
    feats, ret = toy_world(seed, 2 * days, k)
    fit_f, oos_f = cut(feats, slice(0, days)), cut(feats, slice(days, None))
    fit_r, oos_r = ret[:days], ret[days:]
    elig = np.ones((days, ASSETS), dtype=bool)
    behaviours: dict[bytes, np.ndarray] = {}
    evaluations = 0

    def fitness(rule: gp.Rule) -> float:
        nonlocal evaluations
        evaluations += 1
        w = gp.weights(rule, fit_f, elig)
        if w.sum(axis=1).mean() < 0.2:
            return -math.inf
        r = (w * fit_r).sum(axis=1)
        behaviours.setdefault(w.tobytes(), r)
        return stats.sharpe(r) - gp.NODE_PENALTY * gp.size(rule[1])

    scored = gp.evolve(fitness, seed, population, generations)
    best = gp.order(scored)[0]
    test = evo_stats.SnoopTest(np.zeros(days), draws=500, seed=seed)
    series = list(behaviours.values())
    for i in range(0, len(series), 256):
        test.add(np.column_stack(series[i : i + 256]))
    out = test.result()
    w_best = gp.weights(best, oos_f, elig)
    w_h = gp.weights(("slot", H), oos_f, elig)
    oos = (w_best * oos_r).sum(axis=1)
    return {
        "k": k,
        "evaluations": evaluations,
        "formulas": len(scored),
        "behaviours": len(series),
        "best": gp.show_rule(best),
        "best_fit_sharpe": scored[best] + gp.NODE_PENALTY * gp.size(best[1]),
        "best_oos_sharpe": stats.sharpe(oos),
        "h_oos_sharpe": stats.sharpe((w_h * oos_r).sum(axis=1)),
        "weight_corr_h": float(np.corrcoef(w_best.ravel(), w_h.ravel())[0, 1]),
        "rc_p": out["rc_p"],
        "spa_lower_p": out["spa_lower_p"],
        "spa_consistent_p": out["spa_consistent_p"],
        "spa_upper_p": out["spa_upper_p"],
    }


def main() -> None:
    for seed, k in ((1, 0.0), (2, 0.0), (3, 0.0), (1, 0.05), (1, 0.1), (1, 0.2)):
        t0 = time.time()
        res = run(seed, k)
        cells = [
            f"{key}={v:.3f}" if isinstance(v, float) else f"{key}={v}" for key, v in res.items()
        ]
        print(f"seed={seed} " + " ".join(cells) + f" [{time.time() - t0:.1f}s]", flush=True)


if __name__ == "__main__":
    main()
