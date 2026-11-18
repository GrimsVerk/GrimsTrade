# Evo 1: can an evolutionary search find a trading rule that survives an honest correction?

Research run evo-1, 2026-11-18. Branch `evo-1` (from `carry-2`). Research only: nothing here
touches the live runner, the gym's rules or the live strategies.

Question: after ~15 runs nothing beats `tsmom12` (hold each asset while its 365-day return is
positive). Hand-made ideas mostly turn out to be "a smoother trend rule". Here a computer
searches instead: **genetic programming** (GP: a population of small rule formulas is bred,
the better ones are kept, crossed and mutated, generation after generation). A big search always
finds winners in the data it searched. The question is whether anything is left once the search
is charged for its luck: selection done before the test period (walk-forward), a data-snooping
test over every rule tried, and assets the search never saw.

## Results

Not run yet. This file holds only the card until the runs are done.

## Build notes, burst 1 (2026-11-18 ~11:10 UTC): code and a toy smoke, no market data

Built and tested: `research/lib/evo_stats.py` (Reality Check, SPA, effective number, deflated
best; rules arrive in chunks), `research/lib/evo_gp.py` (the grammar, evaluation, the genetic
operators, one GP run), `research/lib/evo_smoke.py` (a toy world). Not built yet: the inputs
from real bars, the fast scorer, the walk-forward, the card's control worlds.

**The toy smoke is not one of the card's controls.** The toy world has no prices: the 72 inputs
are random numbers per day and asset, 6 assets, 3,000 days to search and 3,000 unseen days;
returns are noise plus the card's planted rule `H` at strength `k` (`k` = 0: noise). No costs.
12 runs, logged as `control` rows under `evo-1-smoke` in `tries.md`.

| Toy world | Search | Rules | Best fit Sharpe | Same rule, unseen days | `H`, unseen days | SPA p |
|---|---|---:|---:|---:|---:|---:|
| noise, seed 1 | 2,000 random rules, no evolution | 1,983 | 0.73 | 0.12 | - | 0.552 |
| noise, seed 2 | 2,000 random rules, no evolution | 1,986 | 0.75 | 0.04 | - | 0.476 |
| noise, seed 3 | 2,000 random rules, no evolution | 1,972 | 0.83 | -0.07 | - | 0.232 |
| noise, seed 1 | GP 200 x 15 | 2,274 | 1.49 | 0.19 | - | 0.002 |
| noise, seed 2 | GP 200 x 15 | 2,257 | 1.52 | 0.39 | - | 0.004 |
| noise, seed 3 | GP 200 x 15 | 2,243 | 1.36 | -0.06 | - | 0.006 |
| noise, seed 1 | GP 500 x 30 (the card's size, one seed) | 10,076 | 1.88 | -0.66 | - | 0.000 |
| plant k=0.05 | GP 200 x 15 | 2,101 | 1.09 | -0.19 | 1.33 | 0.090 |
| plant k=0.1 | GP 200 x 15 | 2,063 | 0.56 | -0.37 | 2.49 | 0.896 |
| plant k=0.2 | GP 200 x 15 | 2,053 | 1.64 | 1.16 | 4.74 | 0.000 |
| plant k=0.1 | GP 500 x 30 | 10,274 | 2.95 | 2.52 | 2.49 | 0.000 |
| plant k=0.2 | GP 500 x 30 | 10,013 | 3.15 | 2.70 | 4.74 | 0.000 |

What it shows:

- **The correction is right for a fixed set of rules and wrong for an evolved one.** Over 2,000
  random rules in pure noise the SPA p is 0.23 to 0.55, as it should be. Over the rules a GP run
  visited in the same noise it is 0.002 to 0.006, and 0.000 at the card's population and
  generations, while the "found" rule earns nothing on unseen days (0.19, 0.39, -0.06, -0.66).
  This is the card's "known weakness", and in the toy it is not small: it is a false find in 4
  of 4 noise runs. The reason: a GP builds its best rule out of the lucky parts of earlier
  rules, so the best is luckier than the best of any fixed list of the same length, and the
  bootstrap only replays the list.
- So bar 3 of the card (SPA consistent p < 0.10) is likely to pass for any evolved search,
  noise included. The card is not changed here: its noise control (bar 5, three worlds of
  shuffled real bars) is the pre-registered check of exactly this, and the walk-forward series
  is not affected. **For the lead to decide before the real search runs:** if the card's noise
  worlds also show small SPA p, bar 3 says nothing and should be replaced, by a dated card
  note made before any real number, with a test that replays the whole search (the best
  fitness of the real search against the best fitness of the same search in shuffled worlds).
- The search itself works at the card's size: the planted rule at k=0.1 is recovered (weights
  0.99 correlated with `H`'s, the same Sharpe on unseen days). At 200 x 15 it is not (only the
  trend half, and only at k=0.2). At k=0.2 with 500 x 30 the run got 2.70 of `H`'s 4.74.
- The toy is easier than the card's worlds in one way (no costs, inputs unrelated day to day,
  so every rule is a fresh bet) and one seed per row: treat the sizes as rough.

Details the card left open, fixed in code before any real-data run (2026-11-18):

- Initial population: a draw over 20 nodes or depth 6 is drawn again. A full tree of depth 4
  cannot fit in 20 nodes (it has at least 26), so "full" at depth 4 means: grown freely, redrawn
  until it reaches depth exactly 4.
- Random trees: a free branch stops with probability 0.4 at each level; a weight leaf is a
  constant 70% of the time, else `volcap`; a comparison is `coin` 10%, input against input 20%,
  input against a constant 70%; a subtree mutation inserts a freely grown subtree of depth 1 to
  3. `volcap` with an undefined 30-day volatility holds nothing.
- Reality Check and SPA: a resample that ties the observed statistic counts as reaching it; a
  rule identical to the benchmark on every resample is left out of the SPA (its standard error
  is zero).

## Card (written 2026-11-18 ~01:50 UTC, before any evo-1 code or number)

Seen before writing: every result in `ideas.md`, `tries.md` and `results/` up to carry-2. No
evolved rule, no fitness number and no timing of this pipeline had been seen.

### Claim

A GP search over trend, volatility, drawdown and cross-asset conditions finds rules that, traded
strictly after they were chosen, beat `tsmom12` on Sharpe, and the best rule found in sample is
better than luck over the whole search would give.

### Why it might work, why it might not

- Might: `tsmom12` is one comparison. If the true rule has two or three conditions (trend AND calm
  volatility; trend unless a deep drawdown), the search can reach them; the ML run looked for such
  interactions with boosted trees and failed, but trees were fitted to 28-day return direction,
  while GP is scored on what we care about, the Sharpe of the traded rule after costs.
- Might not: six assets that mostly move together and ~30 years hold very few independent bets
  (`results/ml-control.md`, `rl-3.md`). The literature is on the "not" side: Allen & Karjalainen
  (1999) evolved rules for the S&P 500 and found no excess return after costs out of sample;
  Sullivan, Timmermann & White (1999) showed the best of 7,846 technical rules loses its
  significance once the search is accounted for.

### The grammar (what a rule can be)

A rule gives every eligible asset a number from 0 to 1, each Friday, from closes visible at the
decision (the protocol's weekly decision; an asset is eligible after a year of bars).

**Lookbacks** `h` (calendar days): 7, 14, 30, 61, 91, 182, 290, 365. On an asset's own clock
`h` days are `b(h)` bars: `h` for coins; 5, 10, 21, 42, 63, 126, 200, 252 for ETFs and indexes.
`vref` = the asset's EWMA volatility, 60-bar half-life, annualised (`common.vol_series`).

**Inputs**, three families (a comparison only ever mixes inputs of one family):

- M (trend, in units of volatility): `mom(h)` = log return over the last `h` calendar days /
  (`vref` x sqrt(h/365)); `gap(h)` = log(close / average of the last `b(h)` closes), same
  scaling; `dd(h)` = log(close / highest of the last `b(h)` closes), same scaling (drawdown from
  the high, <= 0); `univ(h)` = the average `mom(h)` over the eligible assets (cross-asset).
- V (volatility): `lvol(h)` = log of the realised volatility of the last `b(h)` daily log
  returns, annualised.
- U (cross-asset, 0 to 1): `rank(h)` = rank of the asset's `mom(h)` among the eligible assets
  (0.5 when alone); `breadth(h)` = share of eligible assets with a positive `h`-day return;
  `vrank(h)` = rank of the asset's `lvol(h)`; `vbreadth(h)` = share of eligible assets whose
  `h`-day volatility is above their `vref`.

72 inputs. `mom(365) > 0` is exactly `tsmom12`; `gap(290) > 0` is exactly `sma200`. Cross-asset
inputs are computed inside whatever asset set the rule runs on, and no input names an asset, so
a rule can be run unchanged on other sets.

**Conditions** (true/false per asset): `input > c`, `input < c` with `c` from the family's
grid (M: -2, -1, -0.5, 0, 0.5, 1, 2; V: log of 10%, 15%, 20%, 30%, 45%, 60%, 90%; U: 0.2, 0.35,
0.5, 0.65, 0.8); `input > input` inside one family; `coin` (the asset is a coin); `and`, `or`,
`not`. A comparison with an undefined input is false.

**Weight map:** `if(condition, weight, weight)`, nested; a leaf is a constant (0, 0.25, 0.5,
0.75, 1) or `volcap(t)` = min(1, t / 30-day volatility) for t = 10%, 20%, 40%. One switch per
rule: `slot` (the number is the share of the asset's equal slot that is held, the rest of the
slot is cash: the twins' convention) or `full` (the numbers are rescaled to sum to 1 whenever
any is above 0: fully invested in what is held). Long only, never above 100%: the gym's rules.

**Limits:** at most 20 nodes (every `if`, `and`, `or`, `not`, comparison, `coin` and leaf counts
one; `tsmom12` is 4 nodes) and depth 6.

### Fitness

Sharpe of the rule's daily returns after costs over the fitness window, minus **0.01 per node**
(the complexity penalty), from the fast scorer below. A rule whose average invested share on the
window's Fridays is under 20% is invalid (a Sharpe from a handful of days in the market is
noise).

**Fitness window** at a fit dated `D`: the S&P 500 index alone from 1962-01-02 to 1993-01-28 (the
warm-up the ML and RL runs used, since before 2000 the six-asset book is SPY alone), then the
six assets from 1994-02-01 to the day before `D`, as one series of daily returns. Nothing dated
`D` or later enters a fit: a rule's weights on a Friday use only bars visible that Friday, and
the fitness uses only days before `D`.

### The search (all fixed here)

Hand-rolled GP in numpy. Population 500, 30 generations after the initial one, tournament of 4,
the 5 best copied unchanged; children by subtree crossover (60%), subtree mutation (15%), point
mutation (20%: one lookback, constant, comparison direction, leaf or the slot/full switch
changes), copy (5%); a child over the limits is replaced by its parent. Initial population:
random rules of depth 2 to 4, half grown freely, half full. No hand-made rule is put in: the
search has to find trend by itself. Five independent runs per fit (seeds `1000 x year + 0..4`).
That is at most 77,500 rule evaluations per fit.

Budget escape, used at most once and before any logged run: if a timing test (no result looked
at) shows the whole plan needs more than about 8 CPU-hours, the population is halved and the
change is noted here with its date.

### Scoring: a fast scorer for the search, the real gym for everything reported

`grimstrade.gym.simulate` is too slow for a million evaluations. The search uses a vectorised
scorer: daily return = sum over assets of (target weight x the asset's return), with the
weights of a Friday taking effect at each asset's next open (overnight and open-to-close parts
split on the fill day), minus (fee + slippage) x the weight change. It ignores the 1% band and
cash-limited buys. A test proves it stays within a stated tolerance of the gym on fixed rules.
**Every reported performance number of a walk-forward procedure comes from replaying its
decisions through `gym.simulate`** (the harness, unchanged). The data-snooping test, which needs
the return series of every rule tried, uses the fast scorer for all rules and for `tsmom12`.

### Walk-forward: the out-of-sample series includes the selection

Fits on the first Friday of every second year, 1998 to 2024 (14 fits), expanding window. At each
fit the **candidates** are the 20 best behaviourally different rules of each of the 5 runs (up to
100; "different" = different weights somewhere on the six-asset book). Three selection rules,
each a walk-forward procedure and one `variant` row in `tries.md`:

- `evo-top1`: the candidate with the highest fitness at this fit (ties: fewer nodes, then
  alphabetical).
- `evo-ens10`: going down the candidates by fitness, keep a rule if its daily returns on the
  window correlate below 0.95 with every rule already kept, up to 10; hold the plain average of
  their weights.
- `evo-val`: the candidates of the **previous** fit (evolved on data ending two years earlier)
  are scored, without the node penalty, on the six-asset days between the previous fit date and
  this one, two years their search never saw; the best trades (Allen & Karjalainen's
  train-then-select design).

The chosen rule trades from its fit date to the day before the next fit; the last block ends
2025-11-09. Out-of-sample window: **2000-01-07 to 2025-11-09** (the 1998 fit only supplies
`evo-val`'s first candidates). A final fit on all train data (to 2025-11-09) is run for the
description, the data-snooping test and the held-out rule; it is not traded on train.

### The correction (data snooping)

- **Universe:** every behaviourally different rule that any of the 15 fits scored, all seeds.
  The counts (evaluations, different formulas, different behaviours) are reported and logged.
- **Reality Check and SPA.** White's Reality Check (2000) asks: if no rule in the universe were
  truly better than the benchmark, how often would the best of them look this good by luck? It
  redraws history in blocks (stationary bootstrap, mean block 20 days, 1,000 draws, fixed seed),
  recomputes every rule's Sharpe difference to `tsmom12` on the six assets over 1994-02-01 to
  2025-11-09 and takes the best each time. Hansen's SPA (2005) is the sharper version: each
  difference is divided by its own standard error and clearly bad rules are not allowed to
  inflate the luck. Reported: Reality Check p, SPA lower / consistent / upper p. **The binding
  number is the SPA consistent p.**
- **Deflated Sharpe** (Bailey & Lopez de Prado 2014): the best in-sample rule's Sharpe
  difference to `tsmom12`, against the expected best of N unskilled tries with the spread of
  differences seen across the universe; N = the number of different behaviours (too harsh:
  near-copies count as separate tries) and N = an effective number (participation ratio of the
  correlation matrix of a fixed random sample of 2,000 rules). Reported, not binding.
- **Three procedures, one test:** the smallest bootstrap p among the three procedures is
  multiplied by 3 before it is compared with 0.10.
- **Known weakness, said now:** the Reality Check treats the set of rules as fixed, but a GP
  visits rules *because* they did well on this history, and never visits most of the space. That
  makes its p too small rather than too large. The noise control below measures this.

### Twin and baselines

Twin `tsmom12`. Also shown: `sma200`, equal weight, `inverse-vol`, re-scored from 2000-01-07
(logged baselines, not logged again).

### Pass bar (per procedure; stricter than the protocol default)

1. Protocol bars 1-5 against `tsmom12` on the walk-forward out-of-sample series through the gym,
   2000-01-07 to 2025-11-09 (Sharpe ahead with bootstrap p x 3 < 0.10; ahead in at least 3 of the
   4 eras; worst loss at most 5 points worse; ahead of equal weight on Sharpe; out of universe
   below).
2. Not behind `tsmom12` on Sharpe from 2003-01-01 (the lab's standing check: the trend rule's
   lead comes from 2000-2002).
3. SPA consistent p < 0.10.
4. Out of universe, **transfer**: the very rules the procedure chose on the six assets, fit date
   by fit date, run unchanged on the 8 other ETFs, the 6 other coins and the four indexes as one
   portfolio (each from 2000-01-07 or its own start); the Sharpe difference to `tsmom12` is
   positive in at least two of the three sets.
5. The controls do not undermine it: a pass is not believed if the noise control is "found" in
   two or more of its three worlds.

Reading a fail: "the search finds nothing honest" is only shown if the planted control is found
at its strongest strength; otherwise the verdict is "this search is too weak to tell".

**Held-out year** (2025-11-11 to 2026-11-09): once per procedure, only for a procedure that
passes 1-5. It is traded by the choice made at the final fit (for `evo-val`: the 2024 fit's
candidates scored on 2024-01-05 to 2025-11-09), with no refit inside the year. Passes if not
behind `tsmom12`. A finalist is also run on raw prices (`robustness`).

### Controls (run before the real search; kind `control`, idea `evo-1-control`)

A control **world** is synthetic: for each of the six assets and the S&P 500 index, the real
train-period bars' (overnight, open-to-close) log-return pairs are shuffled in time with a fixed
seed, independently per asset, and shifted so the asset's total log return is zero; calendars
and start dates stay. In such a world no long-only rule has any edge: every rule's true Sharpe
is zero before costs. The whole pipeline (15 fits, 5 seeds, three procedures, the correction)
runs unchanged on each world; the benchmark there is cash (Sharpe 0), not `tsmom12`.

- **Noise control:** worlds with seeds 1, 2, 3. A procedure "finds" noise if its out-of-sample
  Sharpe is above 0 with bootstrap p < 0.10. Also reported: each world's SPA p (it should not be
  small; this is the check on the known weakness above).
- **Planted control:** world 1 with a known rule's edge added. The planted rule `H` is "hold
  while the 91-day return is positive and 30-day volatility is below 365-day volatility"
  (`if(and(mom(91) > 0, lvol(365) > lvol(30)), 1, 0)`, 6 nodes, not a rule the lab has
  tested). Each Friday the state of `H` is read from the synthetic prices so far; the
  open-to-close log return of every bar until the next Friday's decision gets `+k x s` when `H`
  says hold and `-k x s` when it does not, `s` = the asset's real daily volatility. Strengths
  `k` = 0.01, 0.02, 0.04. The **ceiling** is `H` itself traded through the gym (no search),
  reported before any search result. A procedure **finds** the plant if its out-of-sample Sharpe
  is above 0 with p < 0.10 and at least half the ceiling's. Also reported: how close the chosen
  rules' weights are to `H`'s (correlation), and the SPA p.

### Also reported (not part of the bar)

- What the chosen rules are: the formulas, their size, the inputs they use, how close their
  weights are to `tsmom12`'s and `sma200`'s (correlation of weekly weights), and each
  procedure's **static twin** (each asset held at the constant share the chosen rule gave it on
  average over its fitness window, traded over the same block): the gap between a rule and its
  static twin is what its timing adds; the rest is just a choice of how much to hold.
- In-sample fitness against out-of-sample Sharpe, fold by fold, next to `tsmom12`'s.
- The fast scorer against the gym on the baselines.
- **Re-evolved** (`robustness`): the whole procedure run from scratch on each out-of-universe
  set's own history (no S&P 500 warm-up; fits every second year from the first even year with at
  least 5 years of fitness days; trading from the second fit).

### Tries and logging

One `variant` row per walk-forward procedure on the six assets (3 rows) and per transfer run
(`@etf`, `@coin`, `@idx`), `robustness` rows for static twins and re-evolved runs, `control` rows
for the worlds. One extra row of a new kind `search` states how many rules the search evaluated
(not one row per rule). The held-out year is not loaded by any evo-1 script unless a procedure
passes.
