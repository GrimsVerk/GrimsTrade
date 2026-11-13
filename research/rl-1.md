# RL 1: a first honest reinforcement-learning agent in the gym

Research run rl-1, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-rl-1.md`. Branch `rl-1`
(from `macro-1`). Question: can an RL agent that sets portfolio weights on our six assets beat
the 12-month trend rule (`tsmom12`) out of sample, and if not, what would it need?

## In plain words (results, 2026-11-13)

**No. No RL agent came close to beating the 12-month trend rule out of sample.** Five agents,
ten seeds each, walk-forward over 2000-2025 (13 retrainings, every model trained only on data
before it traded), every decision replayed through the real gym. All five fail the bar fixed
before training, by a wide margin, and all fifty seeds lose to `tsmom12`. The held-out year was
not looked at.

- **How far behind:** Sharpe 0.57 to 0.71 against `tsmom12`'s 0.99 over 2000-2025 (0.72 to 0.81
  against 1.19 since 2003). They are also behind equal weight (0.81) and the other plain twins.
  Worst losses were 60% to 87% against 37%. The bootstrap puts them behind with p = 0.96 to
  1.00. These are not near misses.
- **Spread across seeds:** modest and all on the wrong side. Per seed, `ppo-mlp` ran from 0.55
  to 0.75, `ppo-lin` 0.52-0.69, the prices-only MLP 0.64-0.78, the drawdown-penalised MLP
  0.37-0.70 (the widest), ES 0.51-0.64. The best of the 50 seeds (0.78) is still 0.21 behind
  `tsmom12`. The result does not hang on a lucky or unlucky seed.
- **What the agents learned:** to hold coins. Each training window from 2013 on contains
  Bitcoin's (and later Ether's) huge run, and the cheapest way to raise the training reward was
  to put a third of the book in coins (32-41% on average, against 10% for `tsmom12`, whose
  equal slots give coins a sixth each only while they trend up). They half-follow the trend
  flag: an asset in a 12-month downtrend still gets 0.6 to 0.8 of a slot, where `tsmom12` holds
  none. So they kept most of the crypto crashes, which is where the 77-87% worst losses come
  from. They also trade 7 to 10 times their equity a year (`tsmom12`: 2.8), much of it in coins
  at 30 bps a side.
- **What overfits:** the training window. Fold by fold, the MLP agents score 1.15 (and the
  drawdown-penalised one 1.44) on the years they were trained on, and 0.63 and 0.51 on the two
  years each then traded; `tsmom12` scores 0.87 and 0.92 on the same windows. The linear
  policy, with 42 parameters, overfits less (0.84 in sample, 0.73 out) and is still worse:
  the problem is not only network size, it is that the reward on a few thousand weekly bars
  mostly says "the asset that went up most in the past kept going up", and that held for coins
  only until it did not. The largest gaps to `tsmom12` are in the 2002-03, 2012-13 and 2022-23
  folds (for `ppo-mlp`: -0.14 against 0.99, 0.74 against 2.90, 0.01 against 0.59).
- **The sanity check agrees:** the evolution strategy, which optimises the same linear policy's
  training growth directly with no PPO machinery, does no better (0.57). PPO's optimiser is not
  what limits the result; the information in the inputs is.
- **Macro inputs:** no help. The prices-only MLP (0.71) did a little better than the same MLP
  with macro inputs (0.66), within the seed spread. A drawdown penalty in the reward made the
  agent sit in cash (54% on average) without making it smarter (0.57).
- **Out of universe:** the six-asset models, run unchanged on other ETFs and on the four stock
  indexes, also lose to `tsmom12` (-0.08 to -0.35); on the six other coins they are a little
  ahead (+0.02 to +0.11), the only place where "hold coins, follow trend loosely" did not
  hurt.
- **A telling detail:** in the dry plumbing check (disclosed below), models trained for 2
  updates instead of 500 scored 0.86, closer to equal weight. Training made the agent worse out
  of sample. That is the signature of fitting noise.

### What the next rung would need

The agent sees what run 2's models saw (price features, plus macro), and run 2 already showed
those carry almost no forecast skill on six assets decided weekly. RL adds a way to fit the
training years harder, and that is what it did. Before more RL on this book, in order of what
should matter most:

1. **Constrain it to adjust the trend rule, not replace it.** A residual policy (`tsmom12`'s
   weights plus a bounded tilt), a reward measured against `tsmom12` (active log return), and a
   cap on coin weight (the owner's crypto slot choice from `risk-map.md`). Then the agent can
   only add value where it has some, and cannot "discover" crypto's past bull run.
2. **Many more independent bets.** A wider book (the 33 markets of run 2's pooled set, or 30+
   ETFs) so a shared policy learns from cross-sectional differences, not from six assets' one
   history. Or higher frequency in crypto: the local hourly and 1-minute history (Bitstamp
   2011+, Coinbase, Bitfinex, Binance in `~/data/grimstrade`) gives far more decisions, but costs
   of 30 bps a side kill fast trading, so it needs a cost-aware action (trade only past a band)
   and maker-fee assumptions the gym does not yet have.
3. **Information the trend rule does not have.** Coin Metrics on-chain data (active addresses,
   exchange flows, realised cap) and perpetual funding rates are the obvious candidates for
   coins; funding needs perpetual futures and shorting, which the gym does not model.
4. **Training discipline.** Early stopping on a purged validation slice inside each training
   window, a turnover penalty, and a much smaller budget: the 2-update models did better than
   the 500-update ones.

Until one of those changes the inputs or the constraints, more seeds, bigger networks or other
RL algorithms on this setup are not worth a night: the evolution strategy, a completely
different optimiser, landed in the same place.

### GPU

The 5080 ran PyTorch 2.15 (CUDA 13.2 build, compute capability 12.0) for three hours at about
97% reported utilisation but only about 80 W and 9.4 GB for four processes: the networks are tiny
and the GPU waits on kernel launches, not arithmetic. Each process did about 21,000
environment-weeks a second with four sharing the GPU. A CPU-only run would likely have been
as fast; nothing here needed the GPU. It will matter for bigger inputs (minute bars, wide
books, sequence models), not for this rung.

## Plan (written 2026-11-13, before any environment code or training)

### The bar it has to clear, and why it is hard

`tsmom12` is 1.05 Sharpe over 1994-2025 and 1.20 since 2003; equal weight is 0.88 and 1.19. The
review (`review-1`) showed the trend rule's lead is the dot-com bust on a two-asset book, and that
since 2003 nothing, the trend rule included, has beaten holding everything. Run 2 showed that 15
price features carry almost no forecast skill (AUC 0.48-0.51), and macro-1 that the macro
features are regime inputs, not forecasts. An RL agent sees the same information. So the honest
prior is that it will not beat `tsmom12`; the run is built to find out cleanly, and to say what
overfits and what a next rung would need.

### Environment (`research/lib/rl_env.py`)

- **Book:** the six live assets (SPY, QQQ, TLT, GLD, BTC, ETH), total-return prices, the train
  period only (`harness.load_history("train")`: no bar after 2025-11-10 is loaded).
- **Decisions:** weekly, at 22:30 UTC on each calendar Friday (the protocol's weekly rule); the
  same target weights are repeated on every other day, exactly as `common.weekly` strategies are
  replayed, so the gym's 1% band rebalances drift daily as it does for every other strategy.
- **Fills and costs:** the gym's rules exactly: each order fills at the asset's next open with
  slippage, fee on traded value (crypto 25 bps + 5 bps slip, ETFs 2 bps slip), 1% rebalance band
  except full exits, sells before buys, buys limited by cash. A batched numpy simulator replays
  these rules day by day for many episodes at once (training speed). Tests prove that for a fixed
  sequence of weights it gives the same daily equity as `grimstrade.gym.simulate`.
- **Eligibility:** an asset can be held once it has a year of bars (252 ETF bars, 365 crypto
  bars) and its features exist. Ineligible assets are masked out of the action.
- **Action:** a score per eligible asset plus a score for cash; target weights are the softmax
  over those scores. Long-only, sums to 1 with cash (so risk assets sum to <= 1), no leverage.
- **Observation at a Friday decision**, all from data public before that decision:
  - per asset: the 15 features of run 2 (`ml.rows_at`: trend z-scores at five horizons, the
    12-month flag, the 200-day gap, volatility level and shock, drawdown, time since the high,
    breadth, universe momentum and volatility shock, the 12-month rank), whether it is a coin,
    days since the last halving (coins only, else 0), and the asset's current weight (drifted
    since the last fill);
  - shared: the macro features macro-1 recommends, through `lib/macro.py`'s as-of rule (fed
    funds 30-day mean and its 6-month change, the real policy rate, the 10y-2y curve, the Baa
    spread, real M2 growth, the 3-month rise in unemployment, CPI inflation, the 10-year yield,
    VIX) and the cash weight. Missing macro values (before a series starts) are 0 after scaling.
  - Scaling: each input is centred and scaled by its mean and standard deviation over the
    fold's training Fridays only.
- **Reward:** the week's log return of the account after the gym's fees and slippage (Friday
  22:30 to the next Friday 22:30, equity marked at the last prices). One variant adds a drawdown
  penalty fixed now: reward = log return - 1.0 x (increase in the log drawdown from the
  running peak of the episode), so a week that deepens a drawdown counts twice.

### Agents (fixed now; nothing is added after the first result without a dated note)

The policy is **shared across assets**: one scoring function reads an asset's features plus the
shared features and returns that asset's score, so the same few parameters serve every asset
(and can be run unchanged on other asset sets). Cash has its own score from the shared features.
That is a strong prior against overfitting: the linear policy has about 60 parameters.

| Variant | Policy | Trained by | Reward | Inputs |
|---|---|---|---|---|
| `ppo-lin` | linear score | PPO | log return | prices + macro |
| `ppo-mlp` | MLP 2 x 32 score | PPO | log return | prices + macro |
| `ppo-mlp-dd` | MLP 2 x 32 score | PPO | log return with drawdown penalty | prices + macro |
| `ppo-mlp-px` | MLP 2 x 32 score | PPO | log return | prices only (macro inputs zeroed) |
| `es-lin` | linear score | evolution strategy (sanity check) | mean log growth of the episode | prices + macro |

- **PPO:** Gaussian noise on the scores (learned scale), clipped objective (0.2), GAE
  (gamma 0.99, lambda 0.95), value network on pooled asset features and the shared features,
  Adam 3e-4, 64 parallel episodes of 52 weeks from random start Fridays inside the training
  window, a fixed budget of environment steps per fold (the same for every variant and seed;
  set in `rl_train.py` from a timing test before the first logged run, not from results). The
  deployed action is the mean score (no noise).
- **Evolution strategy:** antithetic Gaussian perturbations of the linear policy's parameters,
  the objective is the mean log growth over the same kind of training episodes, the same step
  budget. It checks that PPO's optimiser is not what limits the result.
- **Extra training history:** like run 2's models, every fold also trains on episodes on the
  S&P 500 index from 1963 to 1993-01-28 (before SPY exists; price index, no dividends), a
  quarter of the parallel episodes. It is the only history with the inflation decades in it.
- **Hardware:** PyTorch with CUDA on the RTX 5080, installed per run with
  `uv run --with torch` so the repo's checks and CI stay light. GPU memory and use are logged.
  The networks are tiny, so the GPU mostly saves little; the log says so honestly.

### Walk-forward (the protocol's rule: fitted only on data before the decision)

- A model is retrained every two years, on an expanding window: the model that trades from the
  first Friday of year Y to the first Friday of Y + 2 is trained on Fridays whose one-week reward
  ended at least 7 days before 1 January Y (embargo), Y = 2000, 2002, ..., 2024. Thirteen folds.
- **Out-of-sample window:** 2000-01-07 to 2025-11-09, the concatenation of the folds. The 2000
  fold has only SPY 1994-1999 and the S&P 500 index to learn from: that is the honest situation
  of anyone starting in 2000.
- **Seeds:** 10 per variant and fold (seeds 0-9, fixed). Every seed is replayed through the real
  `grimstrade.gym.simulate` and logged in `tries.md` as `robustness` (the same configuration),
  and the spread is reported. The variant's strategy is the **seed ensemble**: the average of
  the ten seeds' target weights each Friday, fixed now as the one thing selected per variant.
  It is logged as the `variant` row. Five variants: five selectable tries.
- **In-sample check:** each fold's model is also scored on its own training window, so the gap
  between training and out-of-sample Sharpe (overfitting) is measured.
- **Held-out year (2025-11-11 to 2026-11-09):** looked at most once, for at most one finalist,
  and only if a variant passes the bar below. Otherwise untouched.

### Pass bar (fixed now, before any training)

A variant passes only if its seed ensemble, over the out-of-sample window, on the six assets:

1. beats `tsmom12` on Sharpe with paired bootstrap p < 0.10 (protocol test);
2. is ahead of `tsmom12` in at least 3 of the 4 eras inside the window (2000-09, 2010-16,
   2017-21, 2022-25);
3. has a worst loss no more than 5 points worse than `tsmom12`'s;
4. is not behind `tsmom12` on Sharpe from 2003-01-01 (bar 6 of the macro cards), and is ahead of
   the other plain twins (`sma200`, `inverse-vol`) and of equal weight on Sharpe over the
   window and since 2003;
5. at least 7 of its 10 seeds are individually ahead of `tsmom12` over the window;
6. out of universe: the fold models, unchanged, on the 8 other ETFs, the 6 other coins and the
   four indexes as one book (decisions from 2000, or from each set's first eligible Friday):
   the Sharpe difference to `tsmom12` has the same sign as on the six assets in at least 2 of
   the 3 sets.

`tsmom12` and the twins are re-scored from the same first day (2000-01-07) with the logged
configuration (not logged again).

### What is reported, pass or fail

Per variant: ensemble and per-seed Sharpe (median, range), worst loss, growth, turnover,
average cash, eras, 2003-2025, stress windows; in-sample against out-of-sample Sharpe per fold
(the overfitting gap); and in plain words what the agent learned to do (how its cash share and
coin share move with trend, volatility and macro inputs). Every variant gets rows in `tries.md`.

### Tests (`tests/` stays offline and light; torch-free)

- The batched simulator equals `gym.simulate` for fixed weights (random weights on synthetic bars
  with weekends, holidays and assets that start late; and on the real cache in `rl_check.py`).
- No look-ahead: the observation for a Friday is unchanged when every bar and macro record after
  that decision is scrambled or deleted; features equal those built from history truncated by
  the gym's visibility rule.

### Settings fixed from the timing test (2026-11-13, before the first logged run)

- One process trains about 40,000 environment-weeks a second (numpy simulator, networks on the
  GPU). Budget per fold, every variant and seed: **1,664,000 environment-weeks** (PPO: 500
  updates of 64 episodes x 52 weeks; ES: 125 iterations of 32 members x 8 episodes x 52 weeks).
  For the last fold that is about a thousand passes over the six-asset training history, enough
  to overfit if overfitting is there to be had.
- PPO details: initial noise scale 0.7 on the scores, rewards x 10 inside the optimiser, entropy
  bonus 0.001, gradient clip 0.5, 4 epochs of 4 minibatches. The end of a 52-week episode is
  treated as terminal (no bootstrap).
- ES: sigma 0.1, Adam 0.02, 16 antithetic pairs, all members on the same 8 episodes (6 six-asset,
  2 S&P 500 index) per iteration, deterministic policy.
- Test-time support: numpy and scikit-learn joined the repo's dev group so the environment tests
  run in the checks (`tests/test_rl_env.py`); torch stays outside (`uv run --with torch`).
- Prices for this worktree were copied from the macro-1 worktree's cache (fetched 2026-11-13 by
  `lib/fetch.py`); the macro cache is the shared one in `~/data/grimstrade`.

### Disclosure

- 2026-11-13 ~02:55 UTC: `rl_eval.py` was checked in dry mode (`RL_DRY=1`, nothing logged) on
  throwaway `ppo-mlp` models trained for 2 updates per fold (about 0.2% of the budget). It
  printed baseline Sharpe ratios from 2000-01-07 (`tsmom12` 0.99, 1.19 since 2003) and the
  near-untrained ensemble's numbers. No setting was changed after it.
- The first launch ran 16 training jobs at once and filled the PC's memory; it was stopped by
  PID before any fold finished and restarted with 4 at a time. No result was involved.

## Status (2026-11-13 ~05:30 UTC)

**Done:** plan and protocol section before any code; gym-exact batched simulator and weekly
environment with tests (equal to `gym.simulate` to 1e-10 on synthetic bars and 3e-15 on the
real six assets); five agents x ten seeds x thirteen walk-forward folds trained (650 models,
git-ignored in `data/rl/models/`); evaluation through the real gym, 70 rows in `tries.md` (5
`variant` ensembles, 50 seeds and 15 out-of-universe runs as `robustness`); tables in
`results/rl-1.md`; this write-up. All five fail. Held-out year untouched.

**Doing:** nothing half-finished. No process left running.

**Next (not started):** the residual-policy rung (item 1 above) is the cheapest honest next
step: same environment, `tsmom12` plus a bounded tilt, reward relative to `tsmom12`, coin cap.
Write its card and bar first.

Reproduce: `uv run python research/lib/rl_data.py` (tables + real-data check), then
`setsid -f uv run --with torch python research/lib/rl_launch.py` (about 3 hours, 4 jobs at a
time), then `uv run --with torch python research/lib/rl_eval.py` (logs tries: run once) and
`uv run python research/lib/rl_report.py`.
