# RL 4: a learner that passes the planted-signal gate

Research run rl-4, 2026-11-17. Branch `rl-4` (from `carry-2`). Part 1 is a **control
experiment**: no model in it is a strategy, and every row it writes to `tries.md` is marked
`control`. Part 2 (real data) only happens if a learner passes part 1, and gets its own card
section below before any real-data number.

Question: rl-3 planted a known weak signal and found that the pipeline only sees a weekly IC of
0.20 and misses 0.10, because 28 mostly-noise inputs are fitted on a few thousand weekly rows.
Which of the cheap fixes rl-3 listed makes a learner find 0.10, and does that learner then find
anything real on a wide book (the perpetual-futures cross-section of carry-2)?

Words used below. **IC** (information coefficient): the correlation between an input (or a
forecast) and the return of the coming week. **Planted**: an artificial input that is built from
next week's return on purpose, so we know exactly how much there is to find. **Ceiling**: what a
rule that is simply told the planted signal earns; no learner can be expected to beat it.
**Shrinkage**: fitting that pulls every input's weight toward zero unless the data insist.

## Card, part 1: the gate (written 2026-11-17 ~23:00 UTC, before any rl-4 code or number)

### What was already seen (disclosure)

All of rl-3 (`research/rl-3.md`, `results/rl-3.md`): on the six assets, 2000-2025, `tsmom12` has
Sharpe 0.99; the ceiling is +0.030 at IC 0.05, **+0.155 at 0.10** and +0.446 at 0.20; a rule
told pure noise loses 0.04-0.15; rl-3's PPO agents gain -0.003/-0.019 at 0.10 and +0.038/+0.094
at 0.20, and lose 0.011/0.023 on noise; least squares on all 28 inputs gains -0.079 at 0.10.
Nothing of rl-4 has been run.

### What stays exactly as rl-3

The planted input `peek` (`lib/rl3_plant.py`: exact IC in every calendar year, the same noise
draw at every strength, seeds 301 for the six assets and 302 for the S&P 500 warm-up book), the
target (`week_z`: the risk-adjusted return of the week a Friday decision holds), the residual
action (`tsmom12` plus a tilt of at most half a slot, coins never above `tsmom12`, sum at most
1), the 13 walk-forward folds 2000-2024 with the 7-day embargo, the six-asset book, the
out-of-sample window 2000-01-07 to 2025-11-09, every decision replayed through `gym.simulate`,
the paired stationary bootstrap against `tsmom12`. Train period only; the held-out year is not
used by a control.

**Strengths:** IC 0.00 (planted noise), 0.05, 0.10, 0.20.

### The learners (fixed now; cheapest first)

Forecasters (variants 1-4 and the reference) are fitted once per fold, with no random seed, on
every eligible cell with a known target before the fold's cut. Inputs are standardised with the
training rows' mean and standard deviation; a missing macro value becomes 0 after that. The
forecast is of `week_z`, so it is in units of "standard deviations of a week's return".

**From forecast to tilt (one rule for every forecaster, fixed now):**
`score = 10 x (forecast - intercept)`, fed to rl-3's residual action. Why 10: a clean forecast
with IC 0.10 has a spread of 0.10, so times 10 it has the unit scale of `peek`, which is rl-3's
known-signal rule with k = 1. The 10 is not tuned and is the same at every strength. A forecast
that is all zeros gives `tsmom12` exactly. (rl-3's post-hoc check divided the forecast by its
own spread instead, which blows pure noise up to full size; that is not done here.)

| # | Name | rl-3 fix | Inputs | Training rows | Fit |
|---|---|---|---|---|---|
| ref | `ols28` | none (rl-3's failing check under this card's rules) | all 28: 17 asset inputs, `peek`, 10 macro | six assets + S&P 500 warm-up | least squares |
| 1 | `ols3` | (a) few inputs | 3: `peek`, the trend flag `up_12m`, volatility `log_vol` | same | least squares |
| 2 | `ridge28` | (b) shrinkage | all 28 | same | ridge, penalty chosen by purged CV |
| 3 | `lasso28` | (b) shrinkage | all 28 | same | lasso, penalty chosen by purged CV |
| 4 | `ols28-pool` | (c) more rows | all 28 | the 33 markets: six assets, 8 other ETFs, 9 sector ETFs, 6 other coins, 4 indexes, S&P 500 warm-up | least squares |
| 5 | `ppo3` | (a), with RL | 3 (as `ols3`) plus the account state | six assets + S&P 500 warm-up | PPO, rl-3's MLP agent unchanged |

- `ols28` is the reference: rl-3's `sup-ols` with this card's score rule and training rows. It is
  expected to fail and shows what the rule change alone does. It is judged by the gate like the
  others.
- **Purged CV (variants 2 and 3)**, redone at every fit on the training rows only: 5 folds in
  time order with equal numbers of rows; training rows within 14 days of a validation fold are
  dropped (7 days purge + 7 days embargo, on both sides); score = mean squared error; the best
  mean wins. Ridge grid: penalty / number of rows in {0.01, 0.03, 0.1, 0.3, 1, 3, 10}. Lasso grid
  (scikit-learn's `alpha`, which is roughly "ignore inputs whose correlation with the target is
  below this"): {0.005, 0.01, 0.02, 0.03, 0.05, 0.08}. The chosen values are reported per fold.
- **`ols28-pool`** tests "more rows", not "a wider traded book": the forecaster learns from 33
  markets and is still judged on the six assets, so the gate and the ceiling are the same for
  every variant. `peek` is planted in every book it trains on, with the same rule (new fixed
  noise seeds 303-306 for the four extra books). The wide traded book is part 2.
- **`ppo3`** is the RL variant. It is rl-3's `plant-mlp` (PPO, MLP 2 x 32, at most 60 updates,
  early stopping on the purged two-year validation slice, ten seeds 0-9, seed ensemble) with one
  change: the per-asset inputs are cut to `up_12m`, `log_vol` and `peek` (plus the asset's own
  weight and its `tsmom12` weight, as before), and the 10 macro inputs are set to zero (the cash
  weight stays). Fix (a) is the one that carries over to PPO without a new algorithm, and it
  makes `ppo3` against `ols3` a comparison of learners on identical inputs.
- **One follow-up, only if `ppo3` fails the gate and a forecaster passes:** `ppo3-warm`, PPO that
  starts from the forecaster instead of from zero. A linear score whose weights on the three
  inputs start at 10 x the `ols3` coefficients (fitted on PPO's own training part of the fold);
  then PPO as in `ppo3`, with update 0 (the forecaster's policy) among the checkpoints early
  stopping may keep. It would pass mostly because of where it starts; the write-up will say
  whether PPO's fine-tuning added or removed anything against `ols3`.

Not tried, as rl-3 measured they do not help: more updates, no early stopping, bigger networks.

### The gate (fixed now)

Everything is measured on the six assets over 2000-01-07 to 2025-11-09, against `tsmom12` on
the same days. Gain = the learner's Sharpe minus `tsmom12`'s. For `ppo3` the learner is the
ten-seed ensemble. A learner **passes the gate** if all of these hold:

1. **Finds 0.10:** at planted IC 0.10 the gain is above 0 with a one-sided paired stationary
   bootstrap p < 0.10 (rl-3's bar 1: mean block 20 days, 2,000 draws).
2. **Captures a third of it:** at 0.10 the gain is at least **33% of the ceiling**, i.e. at
   least +0.052 Sharpe of the +0.155 that rl-3's best known-signal rule earned. (rl-3's agents
   captured -2% and -13%.)
3. **Finds the stronger rung too:** bar 1 also holds at IC 0.20.
4. **No false discovery and no loss on noise:** at IC 0.00, bar 1 does not hold, and the gain
   is not below -0.025 (rl-3's PPO lost up to 0.023 on noise; a learner that trades noise harder
   than that fails).
5. **RL only:** at 0.10 at least 7 of the 10 seeds are individually ahead of `tsmom12` (rl-3's
   bar 5).

Reported for every learner and strength, not part of the gate: rl-3's other bars (eras ahead,
worst loss, since 2003, active share), the captured share at 0.20, the 0.05 rung (its ceiling,
+0.03, is not itself significant), the forecast's out-of-sample IC, how closely the tilt follows
`peek`, and the penalties chosen.

**Best passing learner** (the one part 2 uses): among those that pass, the largest gain at 0.10;
if two are within 0.01, the one with fewer inputs, then the one with no tuned penalty.

### What each outcome means (fixed now)

- **A forecaster passes and `ppo3` passes:** the fix works for RL too; part 2 uses the best
  passing learner.
- **A forecaster passes, `ppo3` does not:** the inputs were not PPO's only limit (its small,
  early-stopped moves are another). `ppo3-warm` is run. Part 2 uses the best passing learner.
- **Nothing passes:** part 2 is skipped and the write-up says why.

### Compute, tries and logging

- Forecasters: seconds to fit; each replay through the gym about half a minute. `ppo3`:
  4 strengths x 10 seeds x 13 folds = 520 fold models, about 50 CPU-minutes, three processes at
  a time on the CPU (as rl-3). `ppo3-warm`, if run, the same again. No GPU.
- Idea name `rl-4-control`, kind `control` for every row. One row per forecaster and strength
  (5 x 4 = 20); `ppo3`: one ensemble row and ten seed rows per strength (44). The ceiling is
  rl-3's, already logged, and is not rerun.
- Code: `lib/rl4_sup.py` (forecasters and the gate), `lib/rl4_train.py` (the 3-input tables for
  rl-3's trainer), report in `results/rl-4.md`. A plumbing check may run before the logged run;
  it prints shapes only, no performance number.
