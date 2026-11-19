# Trend tune: what earns `tsmom12` its money, and does honest tuning beat the fixed rule?

Research run trend-tune, started 2026-11-18. Branch `trend-tune` (from `carry-2`). Research only:
fake money, the price cache already on disk, no change to the gym, the daily runner or the live
strategies.

`tsmom12` is the rule nothing has beaten in 14 research runs and the core of the live paper
system: each asset's equal slot is held while its 365-day return is positive, else cash, decided
on Fridays. This run looks inside that one rule (Part A) and then tests whether tuning it the
honest way, walk-forward, beats leaving it at 12 months (Part B). Another lane (deep-1) maps
failures across all models; this one stays on `tsmom12`.

## In plain words (results, 2026-11-18)

**Tuning the trend rule does not help: 12 months stays. And the rule is now understood: it
pays only on stocks, by sitting out the wildest stretches of long bear markets, and it hands
most of that back by returning late.** Nothing new has earned a paper slot. Held-out year not
looked at. Tables: `results/trend-tune-anatomy.md` (Part A) and `results/trend-tune.md`
(Part B); 129 rows in `tries.md`.

Sharpe is return per unit of risk (higher is better); `tsmom12` scores 1.05 over 1994-2025 and
1.20 since 2003.

| Question | Answer | Number |
|---|---|---|
| Does letting past data pick the lookback beat 12 months? | No, three ways | 1.01, 1.02 and 1.05 against 1.05; since 2003 -0.01, -0.01, 0.00 |
| What would a tuner with perfect hindsight have gained? | Very little | +0.10 |
| Does last period's best lookback stay best? | No | ranks 4.2 of 7 next period (chance: 4) |
| Is there a better setting nearby? | No: a flat plateau | 6 to 12 months give 1.02 to 1.13; the best of 98 settings is +0.08, luck alone gives +0.17 |
| Where does the rule beat holding? | Stocks only, 2000-2009 | SPY +0.09, QQQ +0.11; gold -0.08, bonds -0.06, BTC +0.01, ETH -0.02 |
| What does it give back after a fall? | Nearly all it saved | +13.6 saved in falls, -14.4 lost in rebounds (log points a year, average asset) |
| How late is it back in? | Seven months | sells 21% below the high, buys back 23% above the low |
| How often is an exit a mistake? | Three times in four | 82 of 112 exits were bought back higher |
| What has it been since 2003? | "Hold three quarters of everything" | same Sharpe (1.20 against 1.19), same worst loss (36% against 38%) |

**Part B, honest tuning.** Three procedures chose the lookback each January from past data
only: one per asset, one for the whole book, and one per asset that leaves 12 months only on
strong evidence. The first two moved (mostly to 6 and 9 months), traded half again as much and
ended slightly behind. The third never found evidence strong enough to move and stayed
`tsmom12` to the cent. On 18 other markets the differences are small and of both signs. All
three fail the bar fixed on the card.

**Part A, anatomy.**

- **What earns the money.** A few long absences from falling stock markets (2000-2003,
  2008-2009, 2022). The rule does not avoid losses on balance: on five of the six assets the
  price rose, in total, while the rule was out. What it avoids on stocks is rough days: days
  out were almost twice as volatile as days in (SPY 29% against 16%), and 12 of the 20 worst
  stock days fell while it was out. That lifts return per unit of risk even though it costs
  growth.
- **Why not elsewhere.** On bonds, gold and coins the days out were no rougher than the days
  in. Coin crashes come out of uptrends: the rule was in for 74% of Bitcoin's crash time. So
  there it gives up return and buys no calm.
- **Where it bleeds.** (1) Late re-entry: the 12 months after a low cost about what the fall
  saved. Its worst years against holding everything are the years after a fall (2003, 2009,
  2019, 2020, 2023: 20 to 39 points behind). (2) Whipsaw: 84 short trips out (under 13 weeks)
  cost a net 339 log points across the six slots; 22 long ones earned 247, a third of it one
  trade (QQQ out from November 2000 to June 2003). Fees are a rounding error next to this.
- **The settings do not matter.** Lookback anywhere from 6 to 12 months, deciding daily,
  weekly or monthly, two lookbacks together, entry and exit thresholds: all within a few
  hundredths. Slowing the rule down to avoid whipsaw does not help, because the later exits
  cost what the fewer whipsaws save. A wider no-trade band cuts trading by a quarter to a
  third at the same Sharpe; that is a cost saving, not an edge.

### What this means

1. **Leave the live rule at 12 months.** No tuned version is worth a slot or a revision.
2. **Expect `tsmom12` to trail "hold everything" in most years** (17 of 23 since 2003) and
   badly in the year after a fall. That is the rule working as built, not a fault.
3. **Its value is insurance on the stock slots.** On the bond, gold and coin slots the
   backtest shows cost without benefit on Sharpe, though it did shrink the worst losses there
   (TLT 33% against 48%). Whether to keep the filter on those slots is a risk choice like the
   ones in `risk-map.md`; a test of it is next lane 2.

### How sure

- **Tuning (Part B): fairly sure it is not a large win.** The test measures the gap to
  `tsmom12` with a standard error of 0.05 to 0.08: it would have seen +0.15 and would likely
  have missed +0.05. Three procedures, six assets and 18 other markets agree, and the
  hindsight ceiling (+0.10) says there was little to find.
- **Anatomy (Part A): a description of one history, in sample.** The stock result rests on
  three bear markets and two funds that move together. "Rough days cluster in stock
  downtrends" is a well-known property of stocks, but here it is two assets; next lane 1
  tests it on data no run has seen.
- **The 98 settings are a descriptive surface, not candidates.** They were logged as `variant`
  rows to be conservative for the deflated Sharpe; none may be picked from this table.
- The card was pushed before any number (commit `81ea406`; one amendment, the bear-window
  wording, also before any number). The held-out year is unspent.
- Two places where the card's wording met the data: the pooled hindsight pick (9 months) is
  already a cell of the surface, so it has no row of its own; and the card's robustness runs
  (raw prices, double costs) go to the procedure with the largest train difference, which is
  `wf-shrunk` at 0.00, so on total-return prices they compare `tsmom12` with itself.

### Next lanes

1. **`trend-1926`: does the stock result hold on 35 years nobody here has looked at?** The US
   market and 10 industries, daily from 1926 (Ken French's data library, already in the cache,
   keyless), cash at the T-bill rate in the same file. Run `tsmom12` against holding over
   1926-1961 (1929-32, 1937, the 1940s) and check the mechanism directly: were the days out
   rougher than the days in? If yes, "insurance on stocks" is a property; if no, it was
   2000-2002. Our only earlier evidence before 1994 is the S&P 500 index 1962-1993, where the
   rule did not beat holding (0.45 against 0.49).
2. **`trend-where-it-pays`: use the filter only where it buys calm.** Each January, an asset
   keeps its trend filter only if, on its own past, its days out were rougher than its days
   in; otherwise it is simply held. A yes/no per asset with no number to tune, walk-forward,
   tested on the 8 other ETFs, 4 indexes and 6 coins. The bar must include the worst loss:
   holding bonds and coins through their winters deepens it, and this lane would show the
   owner that trade in one table.
3. **`fast-reentry`: a mitigation for the worst bleed.** The only direction on the surface
   that pointed up was "slow to leave, quick to return" (held if the 3-month OR the 12-month
   return is positive: +0.01 over 1994-2025, +0.08 since 2003; in sample, one of 98 cells).
   "Quick to leave" pointed down (-0.11). One pre-registered rule, tested only where it has
   not been seen (the three out-of-universe sets, then the held-out year), deflated for 98
   cells. Expect little; it is the cheapest honest shot at the rebound give-back.

Cost note for the M1 lane (not a research lane): a 2.5% to 5% rebalance band gave the same
Sharpe (1.07 against 1.05) with 15% to 25% less trading in the backtest.

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
