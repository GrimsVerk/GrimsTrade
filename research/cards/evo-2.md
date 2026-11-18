# evo-2: a narrower evolved-rule search that must find a calibrated plant first

Field: genetic-programming rule search, redesigned after evo-1 failed its planted control.
Written 2026-11-18 ~19:40 UTC, run evo-2 (branch `evo-2` from `evo-1`), **before any evo-2 code
or number, synthetic or real**. Seen before writing: everything evo-1 produced (all synthetic:
toy smoke, controls, the greed grid and its confirmation, `research/evo-1.md`,
`research/results/evo-1.md`). No evo procedure, evo-1 or evo-2, has read a real price into a
fitness, a replay or a result. The held-out year has not been loaded by any evo script.

## Why a redesign, and what evo-1 showed

evo-1's search (72 inputs, 20 nodes, fitness on the S&P 500 index 1962-1993 plus the six-asset
book) could not recover the planted rule `H` in zero-mean worlds at any of six greed settings:
the procedures picked up the plant's "don't hold" half, not enough of the "hold" half to beat
cash. At 12 of 14 fits the search's best in-sample fitness was above `H`'s own: with ~600,000
formulas tried it overfits past the true rule. The plant was also not calibrated: the same
strength `k = 0.04` gave `H` a Sharpe of 0.72 in world 1 and 0.22-0.24 in worlds 11 and 21.

evo-2 changes four things, all fixed here, and nothing is tuned afterwards:

1. **8 inputs instead of 72** (below): fewer formulas means less luck for the best of them.
2. **Fitness on the six-asset book's days only** (1994-02-01 to the day before the fit), no S&P
   500 index warm-up. In evo-1 half the window was one index, where cross-asset structure does
   not exist and a per-asset rule gets one bet a day.
3. **Smaller rules**: at most 12 nodes and depth 5 (evo-1: 20 and 6). `H` is 6 nodes,
   `tsmom12` 4; a two-condition rule with a volatility cap still fits.
4. **The plant is calibrated per world** to a fixed ceiling (Sharpe of `H` itself out of
   sample), 0.8 and 0.5, so "found" means the same thing in every world.

One greed setting, fixed now, not tuned: **population 500, 10 generations after the initial
one, node penalty 0.02** (the middle of evo-1's grid; evo-1's tuning on synthetic worlds did not
transfer to fresh ones, so evo-2 does not tune). Everything else is evo-1's card unchanged:
grammar operators, constants and grids, leaves (`const`, `volcap`), the `slot`/`full` switch,
tournament 4, elite 5, operators 60/15/20/5, initial depths 2-4, five runs per fit (seeds `1000
x year + 0..4`), 14 walk-forward fits 1998-2024 (first Friday of every second year), the
candidates, the three procedures (`evo-top1`, `evo-ens10`, `evo-val`), the 20% invested rule,
the fast scorer for the search and `gym.simulate` for every reported number.

## The 8 inputs (fixed; each as defined on the evo-1 card)

| Input | Family | Why |
|---|---|---|
| `mom(30)` | M | 1-month trend |
| `mom(91)` | M | 3-month trend |
| `mom(182)` | M | 6-month trend |
| `mom(365)` | M | 12-month trend: `mom(365) > 0` is `tsmom12`, the lab's best rule |
| `gap(290)` | M | distance from the 200-day average: `gap(290) > 0` is `sma200`, the other twin |
| `dd(365)` | M | drawdown from the 1-year high (the drawdown-control idea, in rule form) |
| `lvol(30)` | V | short volatility: with `volcap` and the level grid, "is it a calm month" |
| `lvol(365)` | V | long volatility: against `lvol(30)`, "is volatility above its norm" |

The four trend lookbacks are the standard time-series-momentum horizons (1, 3, 6, 12 months).
No cross-asset inputs (rank, breadth, `univ`, `vrank`, `vbreadth`): they added 40 of evo-1's 72
inputs, and the lab's cross-asset ideas (breadth-1, absorption ratio) found nothing. The `coin`
condition stays.

**Disclosed:** `H` = `if(and(mom(91) > 0, lvol(365) > lvol(30)), 1, 0)` uses `mom(91)`,
`lvol(30)` and `lvol(365)`, all in the set: a plant must be expressible to be findable. So the
planted control measures the search's power for a rule *inside* its grammar; a real edge outside
these 8 inputs cannot be found by evo-2 at all. The set was chosen for the reasons in the table,
not tuned on any world; `H` was fixed by evo-1 before evo-2 existed.

Implementation: evo-1's `evo_feat` still computes all 72 inputs; the GP may only draw, mutate
and validate comparisons over these 8 (a mutation that would leave the set changes the constant
or swaps the sides instead).

## The calibrated plant

`H`'s edge is planted as in evo-1 (`evo_world.plant`: `+k s` on the open-to-close log return of
every bar a Friday decision trades into when `H` holds on that Friday's synthetic inputs, `-k s`
when not; `s` = the asset's real daily sd), on zero-mean-simple-return shuffle worlds (evo-1's
control worlds after the null fix), six assets only.

**Calibration, per world and target:** `k` is found by bisection on `[0, 0.5]` so that `H`'s
fast-scorer Sharpe over 2000-01-07 to 2025-11-09 in the planted world equals the target within
0.01 (at most 30 halvings; if `H` at `k = 0.5` is still below the target, or the bracket is not
monotone at its ends, the world is reported and the lane stops). The **ceiling** is then `H`
traded through the gym in that world, logged as a `control` row before any search runs on it.
Targets: **0.8** (the gate) and **0.5** (reported, not a gate).

## Controls (kind `control`, idea `evo-2-control`), fresh seeds

- **Noise:** shuffle worlds 31, 32, 33 (zero mean simple return). Found = some procedure's gym
  Sharpe (2000-01-07 to 2025-11-09) above 0 with bootstrap p against cash below 0.10.
- **Plant at ceiling 0.8:** shuffle worlds 34, 35, 36, `k` calibrated per world. Found = some
  procedure's gym Sharpe above 0, p below 0.10, and at least half the world's gym ceiling.
- **Plant at ceiling 0.5:** the same worlds 34-36, reported (the power curve), not a gate.

**Gate (all must hold, or evo-2 stops):** noise found in **0 of 3**, and the 0.8 plant found in
**at least 2 of 3** worlds.

If the gate fails: write up, recommend closing the evo line in `next-steps.md`, run no replay
and no real search.

## If the gate passes: replays, then one real search

- **40 replay worlds**, block bootstrap seeds **201-240** (evo-1's replay construction: mean
  block 20 bars, zero total log return, six assets only), the whole evo-2 search in each, logged
  as `control` rows (`evo-2-replay`, one per world) before the real search. Score of a world:
  the best of its three procedures' fast-scorer Sharpe differences to `tsmom12` out of sample.
- **One real search on train only** (decisions to 2025-11-09; the final fit on all train days
  for the description), logged: one `variant` row per procedure (`evo-2`), transfer rows
  (`@etf`, `@coin`, `@idx`), one `search` row.
- **Pass bar, per procedure** (evo-1's bars, bar 3 with 40 replays):
  1. Out of sample 2000-01-07 to 2025-11-09 through the gym against `tsmom12`: Sharpe ahead with
     bootstrap p x 3 < 0.10; ahead in at least 3 of the 4 eras; max drawdown at most 5 points
     worse; ahead of equal weight on Sharpe.
  2. Not behind `tsmom12` on Sharpe from 2003-01-01.
  3. At most 1 of the 40 replay scores at or above the procedure's real statistic (p <= 2/41).
  4. Transfer of the chosen rules, fit by fit, ahead of `tsmom12` in at least 2 of the 3
     out-of-universe sets.
  5. The gate above passed (noise 0 of 3).
- **Held-out year:** not loaded by this lane, pass or fail. A pass goes to the lead, who
  decides on the one held-out look.

Reading a fail: since the gate requires the 0.8 plant to be found, a real-data fail reads
"evo-2 finds nothing honest beyond `tsmom12` among rules of these 8 inputs", with power stated
by the 0.8 and 0.5 control results (an edge of real size, well below 0.8 over `tsmom12`, may
still be missed).

## Multiple testing: evo-2 is a new pick

- evo-2 counts as **one new idea** in the lab's count, with **3 selectable variants** (its three
  procedures, `variant` rows under `evo-2`) and one `search` row stating its rule evaluations
  (which count that many tries for any lab-wide deflation, as the protocol says for evo-1).
- Inside evo-2, the three procedures are charged by the x3 in bar 1, and the whole search's
  luck by the replay test (bar 3), which reruns the identical search on 40 worlds.
- evo-1 has no real-data number, so evo-2's real search is the **first real-data look of the
  evo line**. The redesign was chosen after evo-1's synthetic results only. Any later evo run
  after evo-2's real result is a second look at the same data and counts as another pick, said
  on its card.

## Tries and logging

`control` rows for every ceiling, control world and replay world; `variant`, transfer and
`search` rows for the real search; every row the moment it runs. Scratch JSON under
`<cache_root>/derived/evo-2/` (never committed). Results: `research/results/evo-2.md`; reading
and verdict: `research/evo-2.md`.
