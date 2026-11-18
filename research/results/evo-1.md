# Evo 1: tables

Card and reading: `research/evo-1.md`. Every number below is a `control` row of `evo-1-control`
in `research/tries.md` (33 rows 2026-11-18 19:05-19:09 UTC, 27 rows 19:20-19:24 UTC). No
real-data search, replay world or real-data number of evo-1 exists yet.

## Controls after the null fix (2026-11-18 ~19:20 UTC): zero mean simple return worlds

Card note of 2026-11-18 (lead's decision, option b): the same worlds, each asset's returns
shifted so its mean simple daily return is 0, the plant on top; all controls and ceilings
rerun. Gym Sharpe 2000-01-07 to 2025-11-09; p against cash; in the last column each
procedure's Sharpe difference to equal weight in the same world, with its p (secondary).

| World | equal weight | evo-top1 | evo-ens10 | evo-val | Found | vs equal weight (top1 / ens10 / val) |
|---|---:|---|---|---|---|---|
| noise 1 | -0.10 | -0.29, p 0.929 | -0.19, p 0.831 | 0.22, p 0.132 | none | -0.19 / -0.09 / +0.32 (p 0.052) |
| noise 2 | -0.01 | -0.03, p 0.542 | -0.09, p 0.632 | -0.26, p 0.908 | none | -0.03 / -0.08 / -0.26 |
| noise 3 | 0.05 | -0.34, p 0.968 | -0.14, p 0.772 | -0.21, p 0.880 | none | -0.39 / -0.19 / -0.26 |
| plant k=0.01 (ceiling 0.08) | -0.24 | 0.02, p 0.448 | -0.11, p 0.697 | -0.00, p 0.510 | none | +0.26 / +0.13 / +0.24 |
| plant k=0.02 (ceiling 0.30) | -0.41 | -0.28, p 0.926 | -0.09, p 0.653 | -0.05, p 0.602 | none | +0.14 / +0.33 / +0.36 |
| plant k=0.04 (ceiling 0.72) | -0.75 | 0.10, p 0.317 | 0.19, p 0.178 | 0.27, p 0.073 | none | +0.85 / +0.94 / +1.02 (p 0.000) |

Correlation of the chosen weights with `H`'s: k=0.04 0.32 / 0.48 / 0.39; k=0.02 0.31 / 0.47 /
0.26; k=0.01 0.27 / 0.37 / 0.25. Fast scorer against gym: Sharpe gap at most 0.02.

Diagnostic (not a try; scratch script, k=0.04 world): `H`'s own in-sample fitness against the
best fitness the five runs found, per fit. The search beats the true rule in sample at 12 of 14
fits by 0.01-0.12 (e.g. 1998: `H` 0.579, best 0.652; 2010: 0.528 vs 0.597; only 2014 and 2016
below), with rules that hold up far worse out of sample. The search does not fail to reach `H`'s
fitness: it overfits past it.

| Fit | 1998 | 2000 | 2002 | 2004 | 2006 | 2008 | 2010 | 2012 | 2014 | 2016 | 2018 | 2020 | 2022 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `H` fitness | 0.579 | 0.562 | 0.560 | 0.568 | 0.539 | 0.541 | 0.528 | 0.515 | 0.490 | 0.489 | 0.473 | 0.498 | 0.537 | 0.577 |
| best found | 0.652 | 0.645 | 0.677 | 0.646 | 0.625 | 0.636 | 0.597 | 0.551 | 0.482 | 0.487 | 0.528 | 0.566 | 0.545 | 0.611 |

## First controls (2026-11-18 ~19:05 UTC): zero log-drift worlds (superseded)

These worlds paid a holder about half the variance a day (equal weight Sharpe 0.32-0.47 in
noise), so cash was the wrong null; kept for the record.

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
