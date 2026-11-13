# RL 2: an agent that may only adjust the trend rule

Research run rl-2, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-rl-2.md`. Branch `rl-2`
(from `rl-1`). Question: rl-1's free-weight agents learned "hold coins" and lost to `tsmom12`.
If the agent may only tilt `tsmom12`'s weights a little, is rewarded only for beating it, is
stopped early on a validation slice, and (one variant) learns from 33 markets instead of six,
does it beat `tsmom12` out of sample?

## In plain words (results, 2026-11-13)

**Constraining the agent stopped it from losing, but it still adds nothing. No residual agent
beat `tsmom12`; all three fail their bar.** Three agents, ten seeds each, 13 walk-forward folds
2000-2025 (390 models), every decision replayed through the real gym. The held-out year was not
looked at.

- **Did constraining help?** Against rl-1, enormously: Sharpe 0.97-0.98 instead of 0.57-0.71,
  worst loss 35-36% instead of 60-87%. But only because the agent is now almost `tsmom12`. Against
  `tsmom12` itself (0.99 over 2000-2025, 1.19 since 2003) all three are a hair behind:
  `res-lin` -0.008 (bootstrap p = 0.71), `res-mlp` -0.020 (p = 0.87), `res-pool` -0.023
  (p = 0.92); since 2003 -0.007 to -0.021. One seed in ten is ahead for each. The seed spread is
  narrow (0.93 to 1.00) and the best seed of 30 merely ties `tsmom12`.
- **How much did it move?** Very little. Its weights differ from `tsmom12`'s by 1.8%
  (`res-lin`, under the 2% floor: "fail, it learned nothing to add") or 2.7% (the two MLPs) of
  the account on an average Friday. What it learned: hold uptrending assets a touch fuller (1.02
  to 1.04 slots instead of 1), keep a sliver of downtrending ones (0.01 to 0.03 slots), sit in
  cash 27% of the time instead of 30%. Coins stay at `tsmom12`'s 10% (the cap). It trades a
  little more (3.0-3.1 times equity a year against 2.8).
- **How sure?** Sure that it does not beat `tsmom12` on these inputs: three different set-ups,
  thirty seeds, all landing within 0.03 Sharpe of `tsmom12`, slightly on the wrong side. Not a
  near miss with a hidden edge: the edge is not there even in the training years.
- **Training discipline did what it should and showed why.** Early stopping kept zero tilt
  (pure `tsmom12`) in 44% of the fold models of `res-lin`, 34% of `res-mlp` and 26% of
  `res-pool`. Where it allowed a tilt, the gain on the training years was tiny (typically 0.70
  against 0.68 weekly Sharpe), the gain on the validation slice that chose it small, and out of
  sample the tilted folds were ahead in only 3 of 7 (`res-lin`), 5 of 11 (`res-mlp`) and 4 of 9
  (`res-pool`). The validation gain did not carry into the next two years: what the agent found
  was noise, just less of it than in rl-1.
- **The wider book did not help.** `res-pool`, trained on 33 markets, is no better than the
  six-asset MLP (0.97 and 0.97). More independent bets did not uncover a pattern that holds.
- **Out of universe:** the same picture on the 8 other ETFs, 6 other coins and 4 indexes: within
  0.03 Sharpe of `tsmom12`, mostly just behind. Bar 6 is formally "passed" only because those tiny
  differences share the six assets' negative sign.

### What next for the RL lane

The residual frame is the right harness and should be kept: it cannot lose much to `tsmom12`,
and it makes "the agent found nothing" visible instead of hiding it in a coin bet. What it
showed is that there is nothing in these inputs (prices and macro, weekly) for any learner to
find beyond the trend rule; run 2, macro-1, rl-1 and now rl-2 agree. In order:

1. **A planted-signal control** (cheap, a few hours): put a known weak signal into one input of
   the residual environment and check that this exact pipeline finds it and beats `tsmom12`.
   If it cannot, the learner or budget is the limit; if it can, the inputs are, and the lane
   needs new information before more training.
2. **New information for coins**, the only place it is likely to exist: Coin Metrics on-chain
   inputs (brief item 4; the cache in `~/data/grimstrade/coinmetrics`) with the macro as-of rule,
   and later perpetual funding rates (needs shorting in the gym).
3. Not worth a night: more seeds, bigger networks, longer training, other RL algorithms, or a
   wider book of the same price features.

## Plan (written 2026-11-13 ~05:10 UTC, before any rl-2 code or training)

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

### Settings fixed from the timing test (2026-11-13 ~05:15 UTC, before the first logged run)

- One fold of 60 updates takes about 8 s (`res-mlp`) to 12 s (`res-pool`) on one CPU core, so
  training runs on the CPU (`RL_DEVICE=cpu`), 4 jobs at a time (`rl_launch.py`, now
  parametrised by `RL_TRAIN`, `RL_VARIANTS`, `RL_TAG`; default 4 parallel). The GPU is not used:
  rl-1 already showed these networks do not need it.
- The timing test trained throwaway `res-mlp` and `res-pool` seed-0 models for folds 2024 and
  2000 (outside the model folder, deleted). It printed their validation scores (2024: update 0
  best for both; 2000 `res-pool`: update 60 best), which are inside the training windows. No
  out-of-sample number was computed. No setting was changed after it.
- A book enters a fold's training only with at least 26 training Fridays and a validation slice
  after its first eligible Friday; otherwise it is left out of that fold and its episodes are
  not reassigned (early `res-pool` folds have fewer books).
- Evaluation decisions: on each day the agent's weights are `residual` applied to that day's
  `tsmom12` decision (the logged baseline's own schedule, which on a holiday Friday keeps the
  previous Friday's weights) with the tilt scores of the Friday in force. This is what makes zero
  tilt equal `tsmom12` to the last digit (`rl2_data.py` check: error 0 over 9,440 days;
  `tests/test_rl2.py`). Training and the agent's view of its own account use rl-1's simulator,
  which repeats Friday's weights all week; the two differ only in holiday weeks.

### On-chain variant (card added 2026-11-13 ~06:00 UTC, after the three results above, before any on-chain code)

Brief item 4. One more variant, `res-mlp-chain`: `res-mlp` exactly (same books, budget, early
stopping, seeds, folds, bar), plus three on-chain inputs per coin (0 for every other asset,
like the halving clock). The three results above were seen first; this card is not tuned on
them beyond "`res-mlp` is the variant to extend" (the most active of the three).

- **Data:** Coin Metrics community daily asset metrics, cache
  `coinmetrics/full/2026-11-13/assets/<coin>/page-000.json` (complete for every coin we use;
  BTC from 2009/2010, ETH from 2015-07, the six other coins from their starts).
- **As-of rule (the macro layer's):** a value dated `d` is used from the day after; a Friday
  decision sees only rows dated before that Friday.
- **Inputs, fixed now:** `mvrv` = log of market cap / realised cap (`CapMVRVCur`, the latest
  value); `adr_growth` = log(30-day mean / 365-day mean of active addresses, `AdrActCnt`);
  `fee_growth` = the same for total fees in the coin's own units (`FeeTotNtv`). A value needs
  365 days of history; before that, or if the latest row is more than 7 days old, the input is 0.
- **Left out on purpose:** exchange flows and supply on exchanges. Coin Metrics revises which
  addresses belong to exchanges, and the cache holds today's version, not what was known then:
  using them would be look-ahead. The three inputs above are computed from the chain itself
  (realised cap needs each coin's last-moved price: mechanical, though methodology changes
  are a residual risk, noted).
- **Tries:** one `variant` row, ten seeds and three out-of-universe runs as `robustness`. The
  pass bar is the same seven bars. It is also compared with `res-mlp` (does on-chain add
  anything over the same agent without it?).

### Disclosure

- 2026-11-13 ~05:25 UTC: after all 390 fold models were trained, `rl2_eval.py` was run once in
  dry mode (`RL_DRY=1`, nothing logged) on `res-lin` to check the plumbing before logging. It
  printed `res-lin`'s out-of-sample verdict (behind `tsmom12` by 0.008 Sharpe, active share
  1.75%, fails). Nothing was changed after it; the logged run followed with the same code.
- Times in this file are UTC (an earlier draft wrote local time, UTC+1, by mistake; corrected
  before any result).

## Status (2026-11-13 ~05:50 UTC)

**Done:** plan, pass bar and protocol section before code; residual environment with tests (zero
tilt equals `tsmom12` exactly through the gym: synthetic test and real data, error 0); trainer
with purged validation and early stopping; 3 variants x 10 seeds x 13 folds trained on the CPU
(390 models, git-ignored in `research/data/rl/models2/`, about 12 minutes); evaluation through
the real gym, 42 rows in `tries.md` (3 `variant` ensembles, 30 seeds and 9 out-of-universe runs
as `robustness`); tables in `results/rl-2.md`; this write-up. All three fail. Held-out year
untouched.

**Doing:** nothing half-finished. No process left running.

**Next (not started):** planted-signal control, then on-chain inputs for coins (brief item 4),
see "What next for the RL lane".

Reproduce: `uv run python research/lib/rl2_data.py` (tables + zero-tilt check; needs rl-1's
`tables.pkl` from `rl_data.py`), then
`RL_TRAIN=rl2_train.py RL_VARIANTS=res-lin,res-mlp,res-pool RL_TAG=rl2- setsid -f uv run --with torch python research/lib/rl_launch.py`,
then `uv run --with torch python research/lib/rl2_eval.py` (logs tries: run once) and
`uv run python research/lib/rl2_eval.py --report`.
