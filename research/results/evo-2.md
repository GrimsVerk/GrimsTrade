# Evo 2: tables

Card: `research/cards/evo-2.md`; reading and verdict: `research/evo-2.md`. Every number below
is a `control` row of `evo-2-control` in `research/tries.md` (6 ceiling rows ~19:40 UTC, 33
control rows after them, 2026-11-18 by this machine's clock). No replay world, real-data
search or real-data number of evo-2 exists. The held-out year was not loaded.

Setup (card): 8 inputs (`mom` 30/91/182/365, `gap(290)`, `dd(365)`, `lvol` 30/365), at most 12
nodes and depth 5, fitness on the six-asset book's days only (no index warm-up), population
500, 10 generations, node penalty 0.02, 14 walk-forward fits x 5 runs, the three procedures.
Zero-mean-simple-return shuffle worlds. About 200,000-240,000 different formulas and
107,000-131,000 different behaviours per world (evo-1 at its card's setting: ~600,000 and
330,000-370,000); 0.011-0.014 CPU-hours of search per world.

## Calibrated ceilings (logged before any search ran on these worlds)

`k` found by the card note's scan-then-bisect so that `H`'s fast-scorer Sharpe out of sample
(2000-01-07 to 2025-11-09) is the target within 0.01; ceiling = `H` itself through the gym.

| World | target 0.8: `k` | `H` fast / gym | target 0.5: `k` | `H` fast / gym |
|---|---:|---|---:|---|
| 34 | 0.0379 | 0.790 / 0.783 | 0.0175 | 0.494 / 0.487 |
| 35 | 0.0588 | 0.800 / 0.799 | 0.0300 | 0.502 / 0.491 |
| 36 | 0.0725 | 0.797 / 0.796 | 0.0425 | 0.503 / 0.497 |

The same ceiling needs nearly twice the strength in world 36 as in world 34: calibration was
needed (evo-1's fixed `k = 0.04` gave 0.22-0.72).

## Controls (gym Sharpe 2000-01-07 to 2025-11-09; p = bootstrap p against cash)

Found (card): some procedure with Sharpe above 0 and p < 0.10, and for a plant at least half
the world's gym ceiling.

| World | equal weight | evo-top1 | evo-ens10 | evo-val | Found |
|---|---:|---|---|---|---|
| noise 31 | -0.01 | -0.11, p 0.705 | -0.15, p 0.734 | -0.21, p 0.824 | no |
| noise 32 | -0.10 | -0.26, p 0.922 | -0.26, p 0.937 | -0.37, p 0.975 | no |
| noise 33 | -0.06 | 0.11, p 0.269 | 0.05, p 0.402 | 0.10, p 0.308 | no |
| plant 34, ceiling 0.78 (need 0.392) | -0.48 | -0.07, p 0.632 | 0.29, p 0.064 | **0.391**, p 0.021 | no (by 0.001) |
| plant 35, ceiling 0.80 (need 0.399) | -0.84 | 0.37, p 0.039 | 0.28, p 0.079 | 0.17, p 0.203 | no |
| plant 36, ceiling 0.80 (need 0.398) | -1.26 | **0.69**, p 0.002 | **0.81**, p 0.000 | 0.33, p 0.059 | **yes** |
| plant 34, ceiling 0.49 (need 0.243) | -0.15 | **0.32**, p 0.056 | -0.08, p 0.653 | -0.42, p 0.977 | **yes** |
| plant 35, ceiling 0.49 (need 0.245) | -0.33 | 0.24, p 0.101 | 0.09, p 0.340 | -0.05, p 0.581 | no |
| plant 36, ceiling 0.50 (need 0.248) | -0.67 | 0.23, p 0.127 | 0.12, p 0.277 | 0.02, p 0.460 | no |

Equal weight in the 0.5-plant worlds was printed, not logged (the card logs that context row
once per world, with the 0.8 run). Fast scorer against gym: Sharpe gap at most 0.01 on all 27 procedure replays.

**Gate: noise found in 0 of 3 (passes); the 0.8 plant found in 1 of 3 (needs 2): FAIL.** The
0.5 plant (not a gate) was found in 1 of 3.

Recovery (mean of the three procedures over the ceiling): 0.8 plant 0.26 / 0.34 / 0.76 (mean
0.45); 0.5 plant -0.12 / 0.19 / 0.25. evo-1 at a 0.72 ceiling: 0.26.

Correlation of the chosen weights with `H`'s, out of sample (top1 / ens10 / val): 0.8 plant
world 34 0.47 / 0.65 / 0.45, world 35 0.49 / 0.60 / 0.45, world 36 0.51 / 0.76 / 0.50; 0.5 plant
0.27 / 0.37 / 0.26, 0.24 / 0.35 / 0.18, 0.36 / 0.51 / 0.40. Against equal weight in the same
world every 0.8-plant procedure is ahead (+0.42 to +2.07, p 0.000-0.030).

## What the search chose (diagnostic, scratch JSON, not a try)

Plant 0.8, world 34, `evo-top1` (the procedure that missed): 2000 `full: if(mom(182) > 0.5,
if(and(lvol(365) > lvol(30), mom(91) > mom(30)), 1, 0), 0)`; 2010 `full: if(or(or(lvol(30) >
lvol(365), mom(91) < 1), lvol(30) > -1.609), 0, 0.5)`; **2020 `slot: if(lvol(30) > lvol(365), 0,
if(mom(91) > 0, 1, 0))` (exactly `H`)**; 2024 `H` with an extra `mom(30) > gap(290)` gate and a
quarter slot. World 36 (found): 2020 `H` with `volcap(0.4)` in place of 1; 2024 `H`'s two
conditions plus a volatility-level cut. The search finds `H`'s two conditions once the window
is long; the early fits (1998-2002, SPY alone or SPY and QQQ for 4-8 years) pick other rules,
and the `full` switch (rescale to fully invested in what is held) changes `H`'s sizing.
