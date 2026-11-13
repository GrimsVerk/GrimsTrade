# RL 3: a planted-signal control (is it the inputs or the learner?)

Research run rl-3, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-rl-3.md`. Branch `rl-3`
(from `rl-2`). A **control experiment**: no model here is a strategy, and every row it writes
to `tries.md` is marked `control`.

Question: RL 1 and RL 2 found nothing beyond `tsmom12`. Is that because the inputs hold no extra
information, or because this learner and budget cannot find it? Plant a known, weak, genuinely
predictive signal into one input of RL 2's residual environment, change nothing else, and see at
what strength the pipeline finds it.

## Card (written 2026-11-13 ~05:40 UTC, before any rl-3 code or training)

### What is planted

One extra input per asset, `peek`, appended to the 17 asset inputs of RL 2. For asset `j` on
Friday `i` it is a noisy copy of the return the asset will earn over the coming week:

- **Target.** `z` = the asset's log return from the first open after Friday `i` (the fill of
  Friday's decision) to the first open after Friday `i + 1`, divided by its EWMA volatility at
  the decision (the `log_vol` input) x sqrt(7/365), clipped to +-5. This is the week the agent's
  Friday decision actually holds.
- **Signal.** `peek = rho x z' + sqrt(1 - rho^2) x e'`, where, separately in every calendar year
  of every book, `z'` is `z` standardised over that year's eligible cells and `e'` is fixed
  Gaussian noise with its correlation to `z'` removed and rescaled to unit variance. So the
  realised correlation (information coefficient, IC) between `peek` and the coming week's
  risk-adjusted return is **exactly `rho` in every calendar year**, not just on average: no lucky
  or unlucky draw of the noise decides the result. One noise draw per book (seed fixed), the
  same draw for every strength, so strengths differ only in `rho`.
- **Where.** In every book the agent trains on (the six assets and the S&P 500 warm-up book),
  every asset, every eligible Friday; 0 where an asset is not eligible (like every input).
- **Strengths:** `rho` = 0.00 (planted noise: the false-find control), 0.02, 0.05, 0.10, 0.20.
  0.02-0.10 are the brief's; 0.20 is one rung above as a "must find" check for the plumbing.

### What stays exactly as RL 2

Everything else is RL 2's code and settings, unchanged (`rl2_env.py`, `rl2_train.py`): residual
action (tilt of at most half a slot, coins never above `tsmom12`, sum at most 1), reward (active
log growth minus 0.001 per unit change of the active position), books (six assets + S&P 500
warm-up, 48 + 16 episodes per update), PPO settings, at most 60 updates, early stopping on the
purged two-year validation slice (best of 13 checkpoints, update 0 = `tsmom12`), 13 walk-forward
folds 2000-2024, ten seeds (0-9), the seed ensemble, training-window scaling (the scaler sees
`peek` like any input), evaluation through `gym.simulate` from 2000-01-07 to 2025-11-09.

**Learners:** RL 2's two six-asset set-ups, both run on every strength:

- `plant-lin-<rho>` = `res-lin` (linear score; the RL 2 set-up closest to `tsmom12`);
- `plant-mlp-<rho>` = `res-mlp` (MLP 2 x 32; the most active RL 2 set-up).

`res-pool` is left out: planting into 33 markets would change the breadth, not just the input.
Ten configurations, 1,300 fold models.

### The ceiling: what the planted signal allows

A rule that is told the signal and needs no learning: score = `k x peek` (the residual
action of the same agent, so the same constraints and costs), replayed through `gym.simulate` on
the same window, for `k` in {0.5, 1, 2, 4, sign} (sign = the full half-slot tilt in the
direction of `peek`). The **ceiling** at a strength is the best of the five on Sharpe, picked in
hindsight on purpose: it is an upper reference, not a strategy. **Captured share** =
(agent ensemble Sharpe - `tsmom12`) / (ceiling Sharpe - `tsmom12`).

A rough formula for intuition (written before any run): with tilt `h x sign(peek)` per asset,
`h` = half a slot = 0.5/n, the expected active return per asset-week is
`h x rho x sigma_w x sqrt(2/pi)`; over `n` assets and 52 weeks that is about
`0.5 x 0.8 x rho x sigma_w x 52` a year, `sigma_w` ~ 2.5-3% (ETF weekly vol): about **0.6 x rho
per year** (6% a year at `rho` = 0.10, 1.2% at 0.02), before costs and before the constraints
(downtrending assets cannot go below 0, coins cannot go up, the sum cap). The active risk is
about `h x sigma_w x sqrt(n x 52)`, 4-5% a year on 4-6 assets, so in theory even 0.05 is worth
roughly +0.5 information ratio. The gym rule above replaces this guess with a measured number.

### "Found" (fixed now, before any training)

A learner **finds** the signal at a strength if its seed ensemble, on the six assets over
2000-01-07 to 2025-11-09 (RL 2's bar without the out-of-universe and plain-twin parts, which
do not apply to a planted input):

1. beats `tsmom12` on Sharpe with paired bootstrap p < 0.10;
2. is ahead of `tsmom12` in at least 3 of the 4 eras (2000-09, 2010-16, 2017-21, 2022-25);
3. has a worst loss no more than 5 points worse than `tsmom12`'s;
4. is ahead of `tsmom12` on Sharpe since 2003-01-01;
5. has at least 7 of 10 seeds individually ahead of `tsmom12`;
6. has an average active share of at least 2%.

It finds it **reliably** if it also finds every stronger rung. **The smallest signal this
pipeline finds** = the smallest `rho` found reliably by either learner (both reported).
**False finds:** if `rho` = 0.00 is "found" by either learner, the pipeline's finds cannot be
trusted and the write-up says so first; the number of its seeds ahead of `tsmom12` is the
measured false-find rate per seed.

### What each outcome means (fixed now)

- **Smallest found <= 0.05:** the learner can find a weak weekly signal; RL 2's null then means
  the real inputs hold less usable information beyond `tsmom12` than that. The inputs are the
  limit: next is new information (cache inventory), not a new learner.
- **Smallest found = 0.10:** both matter. A 0.10 weekly IC is near the best published
  forecasts; inputs weaker than that would be missed. Next: the learner fixes below, and new
  information.
- **Smallest found 0.20 or none:** the learner and budget are the limit; "found nothing" in
  RL 1/RL 2 says little about the inputs. Next: change the learner.

**Pre-registered diagnostics** (run only if neither learner finds 0.05 reliably; MLP only, at
0.05 and 0.10, everything else as above):

- `diag-long`: 300 updates instead of 60, checkpoints every 25 (still 13): is the budget the
  limit?
- `diag-noes`: 60 updates, the last checkpoint kept (no early stopping): is the validation
  choice the limit?

### Tries and logging

Idea name `rl-3-control`, kind `control` for every row (ensembles, seeds, ceiling rules): not
selectable, not counted as strategy tries. Each configuration: one ensemble row and ten seed
rows; each strength: five ceiling rows. Out-of-universe runs are not done (no planted signal
there). The held-out year is not needed and not looked at.

### Settings and disclosures (2026-11-13 ~05:47 UTC, before the first logged run)

- Code: `lib/rl3_plant.py` (the planted input; `tests/test_rl3.py` proves the held week and the
  exact yearly IC), `lib/rl3_train.py` (RL 2's `train_fold` on the planted tables). One change
  to `rl2_train.py`: a `KEEP_LAST` switch, off by default (RL 2's behaviour unchanged), for the
  `diag-noes` diagnostic only.
- Realised pooled IC over all years is a little below `rho` (0.049 at 0.05, 0.197 at 0.20)
  because the years' means differ; inside each year it is exact.
- Timing test: `plant-mlp-0.00`, seed 0, folds 2024 and 2000, to a throwaway folder (deleted):
  7.8 s and 5.4 s per fold model, about 1 GB of memory per process. It printed validation
  scores inside the training windows (2024: update 30 best; 2000: all zero, since the 2000 fold
  holds only SPY, which a full slot cannot tilt up). No out-of-sample number was computed and
  nothing was changed after it. Training: 3 processes at a time on the CPU (the brief's cap).
- Price and RL 2 table caches (git-ignored) were copied from the rl-2 worktree, read only.
- Times in this file are UTC. The first push wrote 06:55 for the card, which was local time
  (UTC+1); corrected to 05:40.

### Note after the ceiling, before any agent result (2026-11-13 ~06:05 UTC)

The known-signal rules (no training) were run first; they need no models. They show the rough
formula above was far too generous: on this book, with this action and the gym's costs, the
best rule gains **-0.01 Sharpe at rho 0.02** (i.e. none: every rule is behind `tsmom12`),
**+0.03 at 0.05** (p = 0.15), **+0.16 at 0.10** (p = 0.00 to 0.04) and **+0.45 at 0.20**. Planted
noise (0.00) costs 0.04 to 0.15 (random tilts add turnover and risk). Reasons, measured not
guessed: half the tilts are blocked most of the time (an asset already at a full slot can only
go up by pushing the sum over 1, which scales everything down; an asset out of the trend can
only go up; coins can only be cut), and the gain in Sharpe of adding a modest active return to
a 1.0 Sharpe book is much smaller than the active return's own information ratio.

Consequence, said now so it is not read into the agent results later: the "found" bar can
only be passed from rho = 0.10 up, because even a rule that is told the signal cannot pass it at
0.05. So "not found at 0.02 or 0.05" is not a learner failure, and the outcome "smallest found
<= 0.05" in the card cannot happen. Nothing in the card changes; the reading adds two measures
that do not depend on Sharpe being reachable: the **captured share** at 0.10 and 0.20, and
**corr(tilt, peek)** at every strength (does the agent move its weights with the planted input
at all?). The pre-registered diagnostics are triggered by the card's own rule (neither learner
can find 0.05) and will be run as written.
