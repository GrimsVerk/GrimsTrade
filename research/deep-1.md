# deep-1: a failure atlas of the tested models, then one honest combination test

Status: **card only** (2026-11-18). No deep-1 number exists yet. The write-up goes above this
line when the run is done; the card below is not edited after its commit, only added to under
"Changes after the card" with a date.

---

## Card (fixed 2026-11-18, before any deep-1 number)

Branch `deep-1` from `carry-2`. Rules: `protocol.md`, all of it. Research only; six live assets
(SPY, QQQ, TLT, GLD, BTC, ETH), total-return prices, gym fills and costs, train period
1994-02-01 .. 2025-11-09.

### What had been seen when this card was written

Everything on `carry-2`, `summary-1`, `review-1`: every result table of runs 1-3, macro-1, rl-1
to rl-3, info-1, breadth-1, short-1, carry-2, and the review. In particular: `tsmom12` and equal
weight tie since 2003 (1.20 / 1.19); `ensemble-tsmom` and `drawdown-control` are ahead of
`tsmom12` since 2003 without proof; equal weight beats `tsmom12` in the year after a fall;
`inverse-vol` scores 0.85 over 1994-2025; the halving gate looks good and is not believed. One
unlogged timing run of the `tsmom12` baseline (Sharpe 1.05, the logged figure) was made to
measure how long a backtest takes. Nothing else was computed for this card.

### Question

Why does each tested model fail where it fails (which years, which assets, which state of the
market, which drawdown), and do the models' strengths cover each other's weaknesses well enough
that a combination, chosen with past data only, beats `tsmom12`?

**Out of scope** (lead's note, 2026-11-18): `tsmom12`'s own anatomy and tuning (lookbacks, exit
rules, walk-forward tuning) belong to the `trend-tune` lane. Here `tsmom12` is the yardstick:
its state and its drawdown episodes are the cuts the other models are laid against, and no
parameter of it is varied.

### Part A: the atlas (a description; no pass bar, nothing selectable)

**Models.** One daily return series per model on the six assets, train period.

- *Rebuilt from code with positions* (re-scores of configurations already in `tries.md`, so
  not logged again; each is checked against its logged Sharpe): the benchmarks and twins
  (`equal-weight`, `tsmom12`, `sma200`, `inverse-vol`, `vol-calm`, `bh-spy`, `bh-btc`,
  `sixty-forty`); the primary variant of every run-1 card (`kelly-shrunk` k0.2, `hmm-regime`
  hard, `fracdiff-momentum` d0.4, `drawdown-control` d1.0, `universal-portfolio` up,
  `absorption-ratio` six, `hawkes-clustering` down2, `vol-target` t40, `ensemble-tsmom` e4,
  `trend-vol` tv40, `trend-to-safe` safe); the primary variant of every run-2 card (`logit`,
  `gbm`, `meta-gbm`, `gbm-prop`, `gbm-pay`, `gbm-pool`, `gbm-wk`); the primary `-and` variant of
  every macro card (`hike-and`, `real-and`, `curve-and`, `m2-and`, `walcl-and`, `spread-and`,
  `halving-and`). The two single-asset timing cards (`month-end-liquidity`, `dip-rsi2`) are
  rebuilt on SPY alone and shown apart: they are not six-asset rules.
- *Read from saved out-of-sample equity curves, no positions* (the curves the runs wrote under
  their worktrees' git-ignored `research/data/runs/`; copied read-only to
  `<cache_root>/derived/deep-1/`): the five rl-1 ensembles and the four rl-2 ensembles
  (2000-01-07 on), and the primary variants of the ideas-1 rules. Regenerating RL positions
  needs the torch pipeline and is not worth it for agents that lost badly (rl-1) or copied
  `tsmom12` (rl-2). These series get every cut below except the per-asset one.

**Cuts** (all fixed here):

1. *Era*: the five protocol eras, plus 2003-2025 (the review's window) and the full period.
2. *Asset*: for models with positions, each asset's contribution to the daily return
   (yesterday's target weight times the asset's close-to-close return; the gap to the gym's
   return is shown as "costs and fills"). Reported over the full period and inside drawdowns.
3. *Trend state*, by `tsmom12`'s own position: `breadth` = share of eligible assets `tsmom12`
   holds at its decision in force. `off` if at most 1/3, `on` if at least 2/3, else `mixed`.
4. *Volatility state*: realised volatility of the equal-weight book over the 60 days to
   yesterday, cut into thirds of its whole train-period distribution (a description, so the
   full-sample cut-offs are allowed here; Part B never uses them).
5. *Stress windows*: the seven of the protocol, and the *rebound* after each: the 182 days
   that follow the window's last day.
6. *`tsmom12`'s ten deepest drawdown episodes* (high-water mark to the next new high; peak,
   trough, recovery): every model's return from peak to trough and over the 182 days after the
   trough, and which assets drove `tsmom12`'s loss.
7. *Correlation with `tsmom12`* on weekly returns (7-day blocks): overall, in the weeks
   `tsmom12` lost, and inside its drawdown episodes (peak to trough).
8. *Rolling three-year windows* (a new window every quarter): Sharpe minus `tsmom12`'s; share of
   windows ahead, worst, median, best.
9. Each model's own three deepest drawdowns: dates, depth, the asset that drove it.

Output: `results/deep-1-atlas.md` (compact tables) and, in this file, the three to six failure
modes that matter, each with a mitigation idea. Part A selects nothing and spends no tries; a
component run that is not yet in `tries.md` is logged as `robustness` under idea `deep-1`.

### Part B: three combination rules (fixed here, before Part A's numbers)

The rules are mechanical: every choice inside them is made by the rule itself from past data,
so nothing in Part A's tables can be used to pick a winner. They are the walk-forward test of
whether three of the atlas tables (correlation in losses, the trend-state table, the overall
return table) can be traded.

**Pool.** `tsmom12` plus 29 complements: every rebuilt six-asset model above except `bh-spy`
and `bh-btc` (single assets, not rules) and `halving-and` (its window was taken from folklore
that had seen the winters; macro-1 judged it "not believed"). The two SPY-only timing cards are
not in the pool.

**Machinery shared by the three rules.**

- A *sleeve* is a pool model: its own daily target weights, and the daily returns of its own
  gym replay (costs included) on the same universe from the same first day.
- The combined book's target weights on a day are the sleeve shares times each sleeve's target
  weights, summed per asset. It goes through `gym.simulate` like any strategy (one account, so
  trades between sleeves net out and every real trade pays the gym's costs).
- Sleeve shares are refitted on the first Friday of each calendar year (the protocol's
  schedule for fitted rules) from sleeve returns up to the day before, and held until the next
  refit. A decision on day `d` uses sleeve returns up to `d - 1` only (the gym's equity for day
  `d` includes the crypto close at midnight, after the 22:30 decision).
- Statistics use weekly returns: 7-day blocks counted back from the day before the refit,
  expanding window from each model's first day.
- A complement is *eligible* at a refit once it has 104 weekly returns since the first day it
  could act (the ML models' first fit day, `absorption-ratio` from 2002) with non-zero variance.
  Until the first refit at which `tsmom12` itself has 104 weeks, the book is `tsmom12`.
- Sharpe of weekly returns with zero variance counts as 0.

**B1 `stack`** (risk-based stacking with the complement least like `tsmom12` when it loses).
At each refit: among eligible complements with a positive Sharpe to date, pick the one whose
weekly returns have the lowest correlation with `tsmom12`'s over the weeks in which `tsmom12`
lost money (at least 26 such weeks; a complement with zero variance on them is skipped). The book
is two sleeves, `tsmom12` and that complement, with shares proportional to 1 / variance of each
sleeve's weekly returns over the last 156 weeks (all there are, if fewer), summing to 1. If no
complement qualifies, `tsmom12` alone.

**B2 `switch`** (a switch by trend state). The state on a Friday is the atlas's trend state
(`off`, `mixed`, `on`) from `tsmom12`'s decision that day. At each refit, for each state: the
model held in that state until the next refit is the one, among `tsmom12` and the eligible
complements, with the highest Sharpe over the past weeks that began in that state (a complement
needs 104 such weeks; ties and no data go to `tsmom12`). The book holds, each week, the full
target weights of the model assigned to that week's state.

**B3 `meta`** (a ridge meta-learner on the sleeves' returns). At each refit: ridge regression
of the constant 1 on the weekly returns of `tsmom12` and all eligible complements, no intercept
(Britten-Jones 1999: unpenalised, the coefficients are the mean-variance weights). Penalty
`lambda x T x v`, with `T` the number of weeks and `v` the average second moment of the
sleeves; `lambda` chosen from 0.1, 1, 10 at every fit by 5-fold cross-validation in time order
on those past weeks (squared error on the left-out block). Coefficients below zero are set to
zero and the rest scaled to sum to 1: those are the sleeve shares. All zero: `tsmom12` alone.

Three variants, no sweep. Each is logged as `variant` under ideas `deep-1-stack`,
`deep-1-switch`, `deep-1-meta` when it runs.

**Pass bar (each rule on its own; fixed now).** Twin: `tsmom12`.

1. Sharpe on the six assets, full train period, beats `tsmom12` with bootstrap p < 0.033
   (the protocol's 0.10 shared among three rules).
2. Ahead of `tsmom12` in at least 4 of the 5 eras.
3. Max drawdown not more than 5 points worse than `tsmom12`'s.
4. Out of universe: the Sharpe difference to `tsmom12` has the same sign in at least two of
   three sets: the 8 other ETFs, the 6 other coins, the four indexes as one portfolio from 1962.
   The rule is rerun unchanged on each set with the pool rebuilt there: every pool model that
   exists on the set, ML models refitted on the set's own history as the protocol says,
   `sixty-forty` dropped (it needs SPY and TLT), `absorption-ratio` switching off the set's risk
   assets (the card's list for ETFs; every coin; every index), macro gates as in the protocol.
5. Beats equal weight on Sharpe.
6. Not behind `tsmom12` on Sharpe over 2003-01-01 to the end of train, and not behind equal
   weight there (the review's window).

Also reported, not a bar: the average distance of the book's weights from `tsmom12`'s (a rule
that passes while holding `tsmom12` is not a finding), the sleeves chosen at every refit, and
the Sharpe of the best single pool model with hindsight (what perfect selection would have
given).

**Held-out year** (2025-11-11 .. 2026-11-09): once, for a rule that passes all six bars, and
for no other. The walk-forward simply continues into it; the sleeves' own held-out returns are
computed only inside that one run and logged as `robustness`. If nothing passes, the year stays
unspent.

**Look-ahead check.** A unit test (synthetic returns, scrambled future) proves the sleeve
shares at a refit do not change when later returns change; `lib/deep1_combo.py check` recomputes
the three books' weights on six days from history truncated at each day.

**What would count as what.** Pass: a combination candidate for the paper lane, with the
held-out look. Fail with the book far from `tsmom12`: the models' differences are real but not
predictable from their own past, which is the usual finding for strategy timing. Fail with the
book equal to `tsmom12`: the pool holds no complement at all.

### Changes after the card

(none yet)
