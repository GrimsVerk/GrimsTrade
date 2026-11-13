# RL 2: an agent that may only adjust the trend rule

Research run rl-2, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-rl-2.md`. Branch `rl-2`
(from `rl-1`). Question: rl-1's free-weight agents learned "hold coins" and lost to `tsmom12`.
If the agent may only tilt `tsmom12`'s weights a little, is rewarded only for beating it, is
stopped early on a validation slice, and (one variant) learns from 33 markets instead of six,
does it beat `tsmom12` out of sample?

## In plain words

(Written after the results.)

## Plan (written 2026-11-13 ~05:35 UTC, before any rl-2 code or training)

### Prior

rl-1 found no forecast skill an agent could use on these inputs; a constrained agent cannot
create skill, it can only stop the agent from losing money by fitting coins' past. The honest
expectation is that early stopping often keeps the tilt near zero and the agent ends up as
`tsmom12` with small noise. That counts as a fail, and is said plainly.

### What stays from rl-1

Environment, simulator, inputs, walk-forward and evaluation are rl-1's, unchanged
(`rl_sim.py`, `rl_env.py`, `rl-1.md` "Environment" and "Walk-forward"): weekly Friday decisions,
the gym's fills and costs, run 2's 15 price features + coin flag + halving clock per asset, the
ten macro inputs, training-window scaling, 13 two-year folds 2000-2024 with a 7-day embargo,
out-of-sample window 2000-01-07 to 2025-11-09, ten seeds, the seed ensemble (average of the ten
seeds' weights) as the one selectable strategy per variant, every number from `gym.simulate`.

### What changes

**Action: a bounded tilt on `tsmom12` (residual policy).** Each Friday the base weights `b` are
`tsmom12`'s own (`common.slots(common.tsmom_signal)`, computed by the same code as the logged
baseline): an equal slot `1/n` per live asset, held when its 365-day return is positive. The
policy's shared per-asset score `s_j` (as in rl-1, plus the asset's base weight as an input)
becomes a tilt `t_j = 0.5 x (1/n) x tanh(s_j)`: at most half a slot either way. Then

- `w_j = clip(b_j + t_j, 0, cap_j)`, where `cap_j = b_j` for a coin and 1 otherwise;
- if the weights sum to more than 1, all are scaled down to sum to 1 (no leverage).

Assets without features (no tilt input) keep their base weight. **Coin cap:** the agent may never
hold more of a coin than `tsmom12` does, i.e. the risk map's "Trend rule, a sixth per coin" row
is the ceiling and the agent can only cut coins. Reason: rl-1's agents beat their training
reward by adding coins; this removes that door entirely. With every score at zero, `w = b`
exactly: the agent is `tsmom12`. A test proves it through `gym.simulate`.

**Reward: active log return after the gym's costs, minus a turnover penalty.** Every training
episode runs a `tsmom12` account beside the agent's, from the same Friday, in the same
simulator. Weekly reward = log growth of the agent's account - log growth of the `tsmom12`
account - 0.001 x sum over assets of |change in the active position|, where the active position
is `w - b` (so changing the tilt costs 10 bps per unit, on top of the gym's fees; `tsmom12`'s own
trades cost nothing extra). Inside the optimiser rewards are x 100.

**Training discipline.**

- **Validation slice:** the last 104 usable Fridays (two years) of each fold's training window.
  The training part is the Fridays before it whose week ends at least 7 days before the first
  validation Friday (purge + embargo). The S&P 500 warm-up book (1962-1993) is all training.
- **Small budget:** at most 60 PPO updates per fold (rl-1 used 500; its 2-update models did
  better). The deterministic policy is scored on the validation slice at updates 0, 5, ..., 60
  (13 checkpoints; update 0 is the untrained policy = zero tilt = `tsmom12`). Score = mean weekly
  reward over the validation slice, the account run continuously from its first Friday. The
  checkpoint with the best score is kept (earliest on ties). It is not refitted on the
  validation years. If no checkpoint beats zero tilt, the fold model is `tsmom12`.
- **Initialisation:** the last layer of the score starts at zero, so training starts from
  `tsmom12` and moves away only if the gradient says so. Action noise: Gaussian on the scores,
  starting scale 0.5 (learned). Everything else is rl-1's PPO (clip 0.2, gamma 0.99, lambda 0.95,
  Adam 3e-4, 4 epochs x 4 minibatches, gradient clip 0.5, entropy 0.001, 64 parallel 52-week
  episodes per update).
- **Gap reported per fold:** weekly Sharpe of the ensemble and of `tsmom12` on the training
  part, the validation slice and the two out-of-sample years, and the updates chosen per seed.

**Wider book (one variant).** `res-pool` trains one shared policy on episodes from 33 markets,
run 2's pooled set as five books: the six assets, the 8 other ETFs, the 9 sector ETFs, the 6 other
coins and the four indexes (each book with its own `tsmom12` base, cross-asset features inside
the book), plus the S&P 500 warm-up book. Parallel episodes per update: six 16, ETFs 12, sectors
12, coins 8, indexes 8, warm-up 8. Its validation score is the mean of the five books' scores.
It is still traded and judged on the six assets. The coin cap holds on the coin book too.

### Variants (fixed now; nothing is added after the first result without a dated note)

| Variant | Score function | Training books |
|---|---|---|
| `res-lin` | linear | six assets + S&P 500 warm-up |
| `res-mlp` | MLP 2 x 32 | six assets + S&P 500 warm-up |
| `res-pool` | MLP 2 x 32 | 33 markets in five books + S&P 500 warm-up |

All read prices + macro inputs. Brief item 4 (on-chain inputs for coins) is run only if these
three are done and budget remains; it would get its own dated card first.

### Pass bar (fixed now, before any training)

A variant passes only if its seed ensemble, over 2000-01-07 to 2025-11-09 on the six assets:

1. beats `tsmom12` on Sharpe with paired bootstrap p < 0.10 (protocol test);
2. is ahead of `tsmom12` in at least 3 of the 4 eras (2000-09, 2010-16, 2017-21, 2022-25);
3. has a worst loss no more than 5 points worse than `tsmom12`'s;
4. is **ahead** of `tsmom12` on Sharpe from 2003-01-01 (stricter than rl-1's "not behind"), and
   ahead of `sma200`, `inverse-vol` and equal weight on Sharpe over the window and since 2003;
5. at least 7 of its 10 seeds are individually ahead of `tsmom12` over the window;
6. the fold models, unchanged, on the 8 other ETFs, the 6 other coins and the four indexes: the
   Sharpe difference to `tsmom12` has the same sign as on the six in at least 2 of the 3 sets.
   For `res-pool` these sets were in its training books (earlier years only, walk-forward), so
   for it this is an out-of-time check, not out-of-universe; said so in the result;
7. its average active share (half the sum of |w - b| over assets, averaged over Fridays) is at
   least 2%. Below that the agent is `tsmom12` and the verdict is "fail: it learned nothing to
   add", whatever the other numbers say.

Held-out year (2025-11-11 to 2026-11-09): at most once, one finalist, only if a variant passes.

### Settings fixed from the timing test

(Filled in before the first logged run.)

## Status

Plan written. No code, no training yet.
