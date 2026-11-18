# Evo 1: tables

Card and reading: `research/evo-1.md`. Every number below is a `control` row of `evo-1-control`
in `research/tries.md` (33 rows, 2026-11-18 19:05-19:09 UTC). No real-data search, replay world
or real-data number of evo-1 exists yet.

## Controls (2026-11-18): synthetic worlds through the whole pipeline

Worlds: shuffled train bars with zero total log return per asset (`evo_world.py`), 14 walk-forward
fits x 5 GP runs (500 x 30) each, about 600,000 different formulas and 330,000-370,000
different behaviours per world. Out of sample 2000-01-07 to 2025-11-09, gym replay of each
procedure's decisions (fast scorer in brackets). p = one-sided stationary-bootstrap p against
cash. "Found" (card): Sharpe above 0 with p < 0.10, and for a plant at least half the ceiling.

| World | evo-top1 | evo-ens10 | evo-val | smallest p x 3 | Found by |
|---|---|---|---|---:|---|
| noise 1 | 0.04 (0.04), p 0.418 | 0.01 (0.01), p 0.491 | 0.18 (0.18), p 0.197 | 0.591 | none |
| noise 2 | -0.07 (-0.05), p 0.636 | 0.12 (0.14), p 0.240 | 0.01 (0.01), p 0.476 | 0.720 | none |
| noise 3 | 0.24 (0.24), p 0.122 | 0.31 (0.32), p 0.051 | 0.37 (0.38), p 0.024 | 0.072 | ens10, val |
| plant k=0.01 (ceiling 0.32) | -0.06, p 0.641 | -0.03, p 0.579 | 0.00, p 0.503 | 1.000 | none |
| plant k=0.02 (ceiling 0.45) | 0.26, p 0.074 | 0.23, p 0.099 | 0.42, p 0.018 | 0.053 | all three |
| plant k=0.04 (ceiling 0.82) | 0.46 (0.47), p 0.009 | 0.51, p 0.002 | 0.24, p 0.117 | 0.006 | top1, ens10 |

Correlation of the chosen weights with `H`'s (out of sample): k=0.01 0.19 / 0.32 / 0.25; k=0.02
0.26 / 0.44 / 0.39; k=0.04 0.47 / 0.56 / 0.35 (top1 / ens10 / val). The ceiling is `H` itself
through the gym, logged before any search ran.

Plain rules, no search, in the same worlds (context rows, gym, same window):

| World | equal weight | `tsmom12` |
|---|---|---|
| noise 1 | 0.32, p 0.057 | 0.13, p 0.262 |
| noise 2 | 0.41, p 0.013 | 0.05, p 0.394 |
| noise 3 | 0.47, p 0.007 | 0.46, p 0.008 |
| plant k=0.01 | 0.19 | 0.06 |
| plant k=0.02 | 0.06 | 0.06 |
| plant k=0.04 | -0.26 | -0.10 |

Fast scorer against the gym on the 18 procedure replays: Sharpe gap at most 0.02.
