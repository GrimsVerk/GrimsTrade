# Trend tune: what earns `tsmom12` its money, and does honest tuning beat the fixed rule?

Research run trend-tune, started 2026-11-18. Branch `trend-tune` (from `carry-2`). Research only:
fake money, the price cache already on disk, no change to the gym, the daily runner or the live
strategies.

`tsmom12` is the rule nothing has beaten in 14 research runs and the core of the live paper
system: each asset's equal slot is held while its 365-day return is positive, else cash, decided
on Fridays. This run looks inside that one rule (Part A) and then tests whether tuning it the
honest way, walk-forward, beats leaving it at 12 months (Part B). Another lane (deep-1) maps
failures across all models; this one stays on `tsmom12`.

## Write-up

Not written yet: the card below was committed and pushed before any new number was produced.

## Card (fixed 2026-11-18, before any new number)

### What had been seen when this was written

- Everything in `README.md`, `ideas.md`, `results/` and review 1 (`reviews/review-1.md` on branch
  `review-1`). In particular: `tsmom12` 1.05 Sharpe against 0.88 for equal weight over
  1994-2025, a tie since 2003 (1.20 against 1.19) with a worst loss of 37% against 47%; the
  review's remark that lookbacks of 9 to 12 months give 1.03 to 1.13 and 15 months or more 0.82
  to 0.89, and that any decision weekday gives 1.04 to 1.05; `ensemble-tsmom` (+0.05, p 0.21);
  `sma200`, `drawdown-control`, `trend-vol`, `trend-to-safe` (twins or risk dials).
- One plumbing run on this branch: the logged `tsmom12` baseline re-scored (1.05, 36.5%), to
  check the copied price cache. No other number.
- So the lookback grid below is written knowing roughly where the in-sample best lies (9 to 12
  months). That is why the surface in Part A is a description with no selection, and why Part B
  lets only past data choose.
- Not re-run here (already tested and dead): the 1/3/6/12-month blend, fractional
  differencing, drawdown control, the 200-day average, volatility caps, trend-to-safe.

### Shared definitions

- **L-month signal.** The asset's log return over the last round(365 x L / 12) calendar days is
  positive (`tsmom12` is L = 12, 365 days, unchanged). For L above 12, an eligible asset with
  less history than that uses the return since its first bar. Eligibility (a year of bars),
  equal slots, Friday decisions, fills and costs are the protocol's.
- **Paper series (gym-free, used by the tuner in Part B and for the stability table in Part A).**
  For asset a and lookback L: on each bar, the position is the L-month signal as of the latest
  Friday before that bar's date, computed only from the bars visible at that Friday's decision;
  the bar's return is position x close-to-close return, minus the gym's one-way cost (30 bps
  coins, 2 bps ETFs) when the position changes. Its Sharpe is annualised on the asset's own bar
  clock (252 or 365). For SPY the same series on the S&P 500 index from 1962 to 1993-01-28 is
  put in front (the warm-up rule of the ML protocol). The pooled series is the equal-slot book
  of the eligible assets' paper series on calendar days (the index standing in for SPY before
  1993).
- **Lookback grid for tuning (Part B):** 3, 6, 9, 12, 15, 18, 24 months (7 candidates).
- Windows shown everywhere: 1994-2025 and 2003-2025 (the review's window), plus the protocol's
  eras.

### Part A: anatomy of `tsmom12` (a description: no pass bar, no selection)

Every configuration below that goes through the harness is logged in `tries.md`. Nothing in
Part A may be used to choose a setting; Part B's procedures are fixed here, before Part A runs.

1. **By asset, on its own.** Each of the six assets alone over its own history, `tsmom12`
   against holding it (gym runs; the four ETFs alone are new `baseline` rows, idea
   `trend-tune-anatomy`; BTC and ETH alone were logged by `crypto-alone` and are re-scored).
   Sharpe, growth, worst loss, by window and era.
2. **In and out.** For each asset: the share of days the rule is in; the asset's return, risk
   and worst days while the rule is in and while it is out. The identity reported: the rule's
   log growth = the asset's log growth, minus the asset's log growth while the rule was out,
   minus costs and fill slippage.
3. **Being invested against stepping aside.** For each asset and for the book: the rule
   against a constant holding of the rule's own average size (which has the Sharpe of plain
   holding, since cash earns 0). The return gap is what timing added or cost; the risk gap
   (volatility, worst loss) is what stepping aside bought.
4. **Out-spells, flips and whipsaw.** Every spell out of each asset, from the exit fill to the
   re-entry fill: length, and the asset's price move between the two fills. A spell *saved*
   if the asset was lower at re-entry, and was a *whipsaw* if it was higher. Per asset: flips
   a year, spells by length (under 4 weeks, 4-13, 13-26, over 26), total saved, total whipsaw
   cost, trading cost, all in log points a year; the ten best and ten worst spells.
5. **Bear markets, rebounds, the rest.** Per asset, with a threshold of 20% (ETFs) or 50%
   (coins): a bear window runs from the highest close since the last bear low to the lowest
   close that follows it, once the fall has reached the threshold; the low is settled when the
   close has risen by the threshold from it. (Amended 2026-11-18, still before any number: the
   first wording, "to the lowest close before the next new high", would have filed QQQ's 2008
   fall under "the rest", because QQQ made no new high between 2000 and 2015.)
   A rebound window is the 365 days after that low (cut where the next bear window starts).
   Everything else is "the rest". For each bucket: what holding earned and what the rule
   earned, how far below the high the rule got out, and how far above the low it got back in.
6. **The book.** The six-asset `tsmom12` book and equal weight replayed through the gym with
   every fill kept: each asset's exact contribution to the book's return (value change minus
   cash put in; sums to the book's change in equity), by era and window, for both books, and
   the difference. Calendar years since 2003 in which the rule trailed or led equal weight
   most, with the asset responsible.
7. **Sensitivity surface (train, in sample).** Logged as `variant` rows, idea
   `trend-tune-surface`, because a cell could be picked by a reader even though none is picked
   here. All on the six assets, 1994-2025, with the 2003-2025 slice:
   - **Lookback x decision frequency (54 cells):** lookbacks 3 to 16 months in steps of one,
     then 18, 20, 22, 24; decided daily, weekly (Friday) or monthly (last business day).
     `L12` weekly is `tsmom12`.
   - **Fast and slow together (20 new cells):** every pair of two different lookbacks from 3,
     6, 9, 12, 18 months, combined as AND (held only if both signals are on: the faster one
     gets you out, the slower one must agree before you get back in) and as OR (held if either
     is on: slow to leave, quick to return).
   - **Entry and exit thresholds (24 new cells):** at lookbacks 6, 12 and 18 months, weekly.
     z = the L-month log return divided by (volatility x sqrt(days / 365)), volatility being
     the protocol's 60-bar-half-life EWMA. Enter when z > c + h, leave when z < c - h, else keep
     last week's state (first state: in if z > c). Centre c = -0.25, 0, +0.25 (lenient to
     strict); half-width h = 0, 0.25, 0.5 (the no-trade band). c = 0, h = 0 is the plain rule.
   - **The gym's rebalance band** for `tsmom12`: 0%, 2.5% and 5% instead of 1% (3
     `robustness` rows; "band" in the brief could mean either this or h above, so both are
     shown).
   - **Hindsight ceiling (2 cells):** the lookback from the tuning grid with the best
     full-train paper-series Sharpe, per asset (`hindsight-asset`) and for the pool
     (`hindsight-pooled`), run as a fixed rule. This is what perfect tuning could have earned
     at most; it is in sample by construction and cannot be selected.
   - **Reading.** For every cell: its Sharpe and the average of its grid neighbours. A plateau
     is a region where cells and neighbours agree; a spike is a cell more than 0.10 above its
     neighbours' average.
8. **Does the best lookback persist?** From the paper series, per asset and for the pool: the
   Sharpe of each grid lookback in each era, and the rank correlation of lookbacks between one
   era and the next. If last era's ranking says nothing about the next, no tuner can work.

Tables: `results/trend-tune-anatomy.md`.

### Part B: honest tuning (three procedures, each one try)

Each procedure is walk-forward: at each refit only bars visible at that refit's decision are
used. **Refit:** the first Friday of each calendar year; the choice holds until the next. The
score window is expanding (all history before the refit), which is what "trailing" means here.
Ties go to the lookback nearest 12, then the shorter.

1. **`wf-asset`: a lookback per asset.** At each refit each asset takes the grid lookback with
   the highest paper-series Sharpe on its own history. An asset with under 5 years of paper
   series uses 12 months.
2. **`wf-pooled`: one lookback for the book.** At each refit all assets take the grid lookback
   whose pooled paper series has the highest Sharpe. Under 5 years of pooled series: 12
   months.
3. **`wf-shrunk`: per asset, shrunk toward 12 months.** For each asset and lookback, the
   paper-series Sharpe advantage over the 12-month signal on that asset is multiplied by
   n / (n + 20), n being the asset's years of paper series (as if 20 years of "no difference"
   had already been seen). The asset moves to the lookback with the largest shrunk advantage
   only if that is at least 0.10; otherwise it stays at 12 months.

Each then trades like `tsmom12` with the chosen lookbacks: equal slots, Friday decisions, the
gym's fills and costs. With every choice at 12 months a procedure is `tsmom12` exactly (a test
proves it, and another proves the choices do not move when later bars are removed).

**Twin:** fixed `tsmom12`. **Benchmark:** equal weight. Idea name in `tries.md`: `trend-tune`.

**Out of universe.** Each procedure is refitted, unchanged, on each set's own history: the 8
other ETFs, the 6 other coins, and the indexes (`wf-asset` and `wf-shrunk` act on one asset at a
time, so each index alone and the four differences averaged; `wf-pooled` builds on a pool, so
the four indexes as one book). No S&P warm-up outside the six assets except where SPY is in
the set. Logged as `robustness` rows.

**Pass bar (each procedure judged alone; all must hold).**

1. Sharpe on the six assets, 1994-2025, beats `tsmom12` with bootstrap p < 0.033 (the
   protocol's 0.10 shared among three procedures).
2. Ahead of `tsmom12` in at least 4 of the 5 eras.
3. Max drawdown not more than 5 points worse than `tsmom12`'s.
4. The Sharpe difference has the same sign in at least two of the three out-of-universe sets.
5. Beats equal weight on Sharpe.
6. Not behind `tsmom12` on Sharpe over 2003-01-01 to the end of train.
7. Deflation: the Sharpe difference to `tsmom12` is larger than the best of 3 unskilled tries
   would be expected to show (Bailey and Lopez de Prado's expected maximum, with the standard
   error of that difference from the bootstrap). The same figure for 21 tries (3 procedures x
   7 grid lookbacks, as if the inner search were not walk-forward) is reported next to it; a
   pass that clears 3 but not 21 is labelled weak.

**Reported for every procedure, pass or fail:** the lookbacks chosen each year, how far its
weights are from `tsmom12`'s on average (active share), turnover, the stress windows. The
procedure with the largest train Sharpe difference is also run on raw prices and at double
costs (`robustness`).

**Held-out year (2025-11-11 to 2026-11-09).** Looked at once, for at most one procedure: one
that passes all seven bars (the one with the largest train Sharpe difference if several do).
It passes there if it is not behind `tsmom12`. If none passes train, the held-out year stays
unspent.

**What each outcome would mean.** All three fail: 12 months stays, and Part A's stability
table says whether that is because there is nothing to tune or too little data to find it. A
pass: a candidate revision of the live rule for the owner, after the held-out look.

Tables: `results/trend-tune.md`.

### Assumptions

- "Trailing Sharpe" is read as an expanding window; a rolling window would be a fourth
  procedure and a second knob.
- The tuner scores lookbacks on the gym-free paper series, not on gym runs. The paper series
  is part of the rule; every reported result comes from the gym.
- Shrinkage constants (20 years, 0.10) and the 5-year minimum are set here and not tuned.
- Part A's paper-series tables are not harness runs and have no `tries.md` rows; the tuner's
  inputs are the same numbers.
