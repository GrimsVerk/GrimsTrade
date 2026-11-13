# Test protocol (fixed 2026-11-12, before any idea was tested)

The rules every idea test follows. Changing a rule after seeing a result is not allowed; a new
rule gets a new dated section at the bottom and applies only to later tests.

## Data

- Longest keyless history: SPY from 1993-01-29, QQQ 1999-03-10, TLT 2002-07-30, GLD 2004-11-18
  (Yahoo); BTC from 2012-01-01 (Bitstamp to 2015-07-19, Coinbase after); ETH from 2016-05-18
  (Coinbase). Fetched by `lib/fetch.py` into git-ignored `data/`.
- **Total-return prices are the primary data.** ETF bars are dividend-adjusted. Reason: raw TLT is
  flat over 23 years (0.99x) while its holders earned 2.28x with coupons; raw prices would make
  any rule that avoids bonds look clever for the wrong reason. The live paper system still trades
  raw prices, so every finalist is also run on raw prices (`robustness`), and crediting dividends
  is a request to the M1 lane (see README).
- Cash earns 0 (the gym's rule). This is harsh on rules that sit in cash in the 1990s and 2000s,
  when cash paid 3-6%. It is kept because it is what the gym does; it biases against timing rules.
- Fills, fees and slippage come from `grimstrade.gym.simulate`, unchanged: next open, 30 bps a
  side in crypto, 2 bps a side in ETFs, 1% rebalance band.

## Periods

- **Train:** decisions 1994-02-01 .. 2025-11-09. Bars after 2025-11-10 are not loaded.
- **Held-out:** decisions 2025-11-11 .. 2026-11-09. Checked at most once per idea, only for an
  idea that passed on train, and logged in `tries.md`. The harness refuses a second look.
- **Eras** (reported separately, always): 1994-99, 2000-09, 2010-16, 2017-21, 2022-25.
- **Stress windows** (total return inside each): dot-com bust 2000-03-24..2002-10-09, 2008 crisis
  2007-10-09..2009-03-09, covid crash 2020-02-19..2020-03-23, 2022 rate shock
  2022-01-03..2022-10-12, crypto winters 2013-12-04..2015-01-14, 2017-12-17..2018-12-15,
  2021-11-10..2022-11-21.

## Conventions shared by every strategy and baseline

- An asset can be held once it has one year of bars (252 ETF bars, 365 crypto bars).
- Signals are re-decided weekly, on Friday's close; the same weights are repeated on other days.
- Sharpe: daily returns on all calendar days, 365 days a year, zero risk-free rate (the repo's
  convention). Standard errors by Mertens (2002). Differences between two strategies: paired
  stationary bootstrap (mean block 20 days, 2,000 draws), one-sided p-value.
- Anything with fitted parameters is walk-forward: fitted only on bars before the decision,
  refitted on a fixed schedule written on the card.

## Baselines and plain twins

Benchmarks (from `docs/DESIGN.md`): buy-and-hold BTC, buy-and-hold SPY, 60/40 SPY/TLT, equal
weight of the eligible assets. Plain twins that an exotic idea has to beat to justify itself:

- `sma200`: each asset's equal slot is held when its close is above its 200-trading-day average,
  else cash.
- `tsmom12`: the slot is held when the asset's 365-day return is positive, else cash.
- `inverse-vol`: weights proportional to 1 / (60-day-half-life EWMA volatility), summing to 1.

Every card names its twin. An idea that only matches its twin is dead: the twin is simpler.

## Out-of-universe sets (chosen before any test)

An idea built on our six assets is also run, unchanged, on assets it was not designed on:

- **Other ETFs:** IWM, EFA, EEM, IEF, LQD, VNQ, DBC, SLV (small caps, foreign and emerging
  stocks, mid-term Treasuries, corporate bonds, real estate, commodities, silver).
- **Other coins:** LTC, XRP, BCH, ETC, XLM, DASH: coins that were among the largest in January
  2018 and that Coinbase or Bitstamp list with long history. Picked from an old ranking on
  purpose: picking today's large coins would only test the winners.
- **Other markets (price indexes, local currency, no dividends):** S&P 500 index 1962-1993 (the
  30 years before SPY existed), Nikkei 225 from 1965, FTSE 100 from 1984, DAX from 1988. Caveat:
  Yahoo's index "open" before about 2010 is often the previous close, so a next-open fill there
  is a fill at the signal's own close (slightly kind; the same for strategy and twin).

How the sets are run: rules that act on one asset at a time run on a set as an equal-slot
portfolio (ETFs, coins) and on each index alone (the S&P 500 index cut at 1993-01-28). Rules that
build a portfolio (kelly-shrunk, universal-portfolio) run the four indexes as one portfolio with
the S&P 500 index kept to 2025; after 1993 that leg overlaps SPY and is flagged.

## Pass bar (default; a card may be stricter, never looser)

An idea **passes train** only if all of these hold:

1. Sharpe on the six assets, full train period, beats its plain twin with bootstrap p < 0.10.
2. It is ahead of the twin in at least 3 of the eras both have data for (4 if all 5 exist).
3. Max drawdown is not more than 5 points worse than the twin's.
4. Out-of-universe: the Sharpe difference to the twin has the same sign in at least two of the
   three out-of-universe sets (as far as the idea applies to them; the card says which).
5. It beats the equal-weight benchmark on Sharpe (otherwise there is no reason to run it).

Only then is the held-out year looked at, once. Held-out passes if the idea is not behind its twin
there (12 months cannot prove anything; it can only fail to contradict). Pass on both makes the
idea an M3 paper candidate. Everything else is dead or parked, with the reason in `ideas.md`.

## Counting tries

Every configuration run through the harness appends a row to `tries.md` at the moment it runs:
`variant` (could have been selected), `baseline`, or `robustness` (same configuration on other
data, costs or prices, after the choice was made). Cards fix the variants in advance; the number
of variants per idea is kept small because each one raises the bar the deflated Sharpe sets.

## Disclosures

- 2026-11-12: while smoke-testing the harness, one unlogged run of the `sma200` twin on 2017-2025
  raw prices was seen (Sharpe 1.38). It is a baseline, not an idea, and is re-run and logged under
  this protocol.
- 2026-11-12: a data sanity print covered the whole cache and showed the largest one-day moves
  per symbol, two of which fall in the held-out year (GLD and SLV, 2026-01-30). No strategy
  result was involved. Sanity scripts now stop at the train cut.

## Note added 2026-11-12, after the tests

"Cash earns 0 ... biases against timing rules" (Data section) was checked afterwards in
`results/cash-interest.md`: with T-bill interest on cash the cautious rules gain 0.5-0.8% a year
and no ranking changes. The rule stays as written; the bias is small.

## Machine-learning tests (added 2026-11-12 02:15 UTC, run 2, before any model was fitted)

Everything above still applies. These rules are for models fitted on features (`lib/ml.py`).

**Rows.** One row per asset per Friday, for every Friday the asset is eligible (a year of bars)
and every feature exists. Pooled across the assets of the universe: one model for all of them.

**Features (15, all from closes visible at the decision; fixed here, never tuned).**
With `vol` = EWMA volatility (60-bar half-life, annualised) and `z(h)` = the log return over the
last `h` calendar days divided by `vol x sqrt(h/365)`, clipped to +-5:

- Trend: `z(7)`, `z(30)`, `z(91)`, `z(182)`, `z(365)`; `up_12m` (1 if the 365-day return is
  positive: the `tsmom12` signal); `sma_gap` = log(close / 200-day average) / `vol`.
- Volatility: `log_vol` = log(`vol`); `vol_shock` = log(10-bar-half-life vol / `vol`).
- Drawdown: `dd_1y` = log(close / highest close of the last year) / `vol`; `since_high` = bars
  since that high, as a share of a year.
- Cross-asset (the same for every asset on a given Friday): `breadth` = share of eligible assets
  with a positive 365-day return; `univ_mom_1m` = mean `z(30)` over eligible assets;
  `univ_vol_shock` = mean `vol_shock`; and per asset `rank_12m` = rank of its `z(365)` among the
  eligible assets, 0 to 1 (0.5 when alone).

**Labels.** The log return over the next 28 days, between the closes visible at the two Friday
decisions. `up` = 1 if positive (classifiers). `ra` = that return divided by
`vol x sqrt(28/365)`, clipped to +-3 (regressors).

**Walk-forward with purge and embargo (López de Prado).** A model is refitted on the first Friday
of each calendar year (run 1's schedule for fitted rules), on an expanding window. A row may be
used at a fit only if its 28-day label window ended at least 7 days before the fit date: the
purge removes every label that overlaps the period the model will trade, the 7 days are the
embargo. That model then decides every Friday until the next fit. Nothing is ever fitted,
scaled or selected on data from after the decision.

**Choosing a setting inside the walk-forward.** Where a card says a setting is "chosen by purged
CV", the choice is redone at every fit, on the training rows only: 5 folds in time order; for
each validation fold the training rows whose 28-day label window overlaps the fold's are dropped
(purge), as are the rows of the 28 days after those (embargo); score = log loss (classifiers) or
squared error (regressors); the best mean score wins. The backtest then is one try, and the
settings chosen each year are listed in the result.

**From forecast to position (long only, no leverage).** Each eligible asset has an equal slot,
like the twins. Confidence `q` = (forecast - neutral) / (average label in the training rows -
neutral), where neutral is 0.5 for P(up) and 0 for `ra`. The slot is held in proportion:
weight = slot x clip(q, 0, 1). So: nothing when the model expects a loss, the full slot when it
is at least as confident as the long-run average, in between otherwise. A model with no skill
forecasts the average and so holds everything: it becomes equal weight. `-hard` variants hold
the full slot whenever q > 0. The denominator is floored at 0.05, so a universe whose average
has been at or below neutral (falling coins) still has a rule: full slot from P(up) = 0.55.

**First model and warm-up.** The first model is fitted at the first yearly fit date that has at
least 1,000 rows; trading starts there, and the twins are re-scored from the same day (same
configuration as the logged baseline, so not logged again). For any universe that contains SPY,
the S&P 500 index from 1962 to 1993-01-28 (the 30 years before SPY existed) is added to the
training rows, so the six-asset test covers the usual 1994-2025.

**Out of universe.** The procedure is refitted, unchanged, on each set's own history: the 8
other ETFs, the 6 other coins, and the four indexes as one pooled portfolio.

**Tries.** Every backtested model configuration is a row in `tries.md`, sweeps included.
Forecast-skill numbers (AUC and the like) are read from those same runs. Seeds are fixed.

## Two more ways from forecast to position (added 2026-11-12 02:25 UTC, run 2)

Written after `ml-linear`, `ml-gbm`, `ml-filter` and the first positive control
(`results/ml-control.md`) had been seen. The control showed that the rule above (full slot at
average confidence) hardly moves the position, so it cannot turn even a planted signal into
Sharpe. These two rules apply to later tests only; the three cards above stay judged as run.

- `-prop` (proportional): weight = slot x clip(q / 2, 0, 1). Average confidence holds half a
  slot, twice the average a full one, an expected loss nothing. A model with no skill holds
  half of everything: equal weight at half size, the same Sharpe as equal weight.
- `-low` (step aside on the weakest forecasts): the full slot, unless the forecast is below
  the 25th percentile of the model's own out-of-fold forecasts on its training rows (purged
  CV folds as above, with the setting in force). A model with no skill is out a quarter of
  the time at random; `tsmom12` is out 24% of the time.

A converter is only worth believing if the control shows it works: planted correlation 0.10
must come out ahead of `tsmom12` on the six assets. The control is rerun with each rule.

## Payoff-weighted training (added 2026-11-12 02:30 UTC, run 2)

Written after `ml-linear`, `ml-gbm`, `ml-filter`, `ml-sizing` and the control had been seen.
For later tests only.

A classifier on `up` treats a month that lost 30% like one that lost 1%. With "payoff weights"
each training row counts in proportion to the size of its 28-day log return (|return| divided
by the mean |return| of the training rows). The weighted chance of "up" is above one half
exactly when the expected log return is positive, so "hold the full slot when the weighted
P(up) > 0.5" is the hold-or-not rule that would have grown the training rows' money fastest.
Purged CV scores use the same weights. The `raw` regression target is the 28-day log return
itself, unscaled and unclipped; hold the full slot when the forecast is positive.

## Pooled training (added 2026-11-12 06:37 UTC, run 2)

Written after `ml-linear`, `ml-gbm`, `ml-filter`, `ml-sizing`, `ml-payoff` and the control had
been seen. For `ml-pooled` and later tests only.

A pooled model is fitted on the rows of five sets together: the six live assets, the 8 other
ETFs, the 9 sector ETFs (until now signal inputs only), the 6 other coins and the four indexes
(33 markets). Each set's cross-asset features (`breadth`, `univ_mom_1m`, `univ_vol_shock`,
`rank_12m`) are computed inside that set. Every row counts once, with no weights by set. The
S&P 500 warm-up rows are left out, because the index set already holds the S&P 500 from 1962;
after 1993 the index and SPY are both in (two rows for nearly the same asset: accepted). The
walk-forward, purge and embargo are unchanged: at a fit, a row of any set is usable only if
its label window ended at least 7 days before the fit date. The training rows do not depend on
which universe is traded. Trading starts on the same day as for the unpooled models (the
first-model rule applied to the traded universe's own rows), so the tables compare.

## Weekly labels (added 2026-11-12 06:45 UTC, run 2)

Written after the six earlier ML cards, the control and `results/ml-feature-skill.md` had been
seen. For `ml-weekly` only.

The label horizon is 7 days instead of 28 (`ML_HORIZON=7`): the log return between the closes
visible at two consecutive Friday decisions; `ra` divides by `vol x sqrt(7/365)`. Everything
that was 28 days because of the label becomes 7: a row is usable at a fit if its 7-day label
window ended at least 7 days before the fit date (the embargo stays 7 days), and in purged CV
the purge and the embargo are 7 days each. Features, yearly refits, first-model rule, position
rules and weekly decisions are unchanged.

## Macro tests (added 2026-11-13 01:55 UTC, run macro-1, before any macro test)

Everything above still applies. These rules are for rules that read macro data (`lib/macro.py`).

**What may be known when.** A number is used at the decision on day `d` only from the day after
it became public. Revised series (PAYEMS, M2SL, CPIAUCSL, UNRATE, INDPRO, WALCL) come from ALFRED
vintages: a feature on day `d` is computed from the vintage current on `d - 1`, never from
today's revised numbers. Observations older than a series' first vintage (WALCL before
2011-07-07) take the first vintage's value and count as public 7 days (weekly) or 45 days
(monthly, from the 1st of the month) after the observation date. Unrevised market series (DFF,
DGS10, T10Y2Y, BAA10Y, VIXCLS) are used from the day after the observation. Tests in
`tests/test_macro_asof.py` prove the rule on synthetic data, including a scrambled future.

**Risk and safe assets.** A macro gate acts only on risk assets. Safe assets are TLT, GLD, IEF
and LQD; every other asset (stocks, indexes, real estate, commodities, silver, coins) is a risk
asset. A safe asset keeps its plain `tsmom12` slot whatever the gate says.

**Rule shapes.** `<card>-and`: the `tsmom12` slot of a risk asset is held only while the gate is
not hostile (trend AND macro). `<card>-alone`: the equal-weight slot of a risk asset is held
while the gate is not hostile, with no trend test (does the macro phase carry information on its
own?); safe assets keep their `tsmom12` slot here too. A gate whose input does not exist yet (NaN)
is not hostile, so the rule is its twin until the data starts. Weekly decisions, as always.

**Card bar 6 (all macro cards).** Besides the default bar: the primary variant must not be behind
`tsmom12` on Sharpe over 2003-01-01 to the end of train (the review's window: the trend rule's
lead comes from 2000-2002). Every result shows 2003-2025 next to 1994-2025.

**Episodes.** Each result counts the hostile spells the gate had in 1994-2025 (runs of hostile
days, gaps under 30 days merged, spells under 30 days dropped). That count, not the number of
days, is the number of independent tests a result rests on.

**Out of universe.** Macro gates are US data. They run on the 8 other ETFs and on the S&P 500
index 1962-1993 (before SPY existed: the only test with cycles our six assets never saw; gates
start when their data starts), and on the Nikkei, FTSE and DAX as "does the US cycle reach
abroad". The coin set gets the gate like any risk asset. A halving gate applies to coins only,
so only the coin set applies to it.

## Reinforcement-learning tests (added 2026-11-13 02:10 UTC, run rl-1, before any RL code or training)

Everything above still applies, the macro as-of rule included. The full design is the plan in
`rl-1.md`; these are the rules a result is judged by.

- **Fidelity.** Training may use a faster simulator only if a test proves it gives the same
  daily equity as `grimstrade.gym.simulate` for the same weights. Every reported number comes
  from replaying the agent's decisions through `gym.simulate` itself.
- **Walk-forward.** Retrain every two years on an expanding window; a model that trades from
  1 January Y is trained only on Fridays whose one-week reward ended at least 7 days before it.
  Out-of-sample window 2000-01-07 to 2025-11-09. Inputs are scaled with training-window
  statistics only.
- **Seeds.** Ten fixed seeds per variant and fold. The selectable strategy of a variant is the
  average of its ten seeds' weights (one `variant` row); each seed is logged as `robustness`.
  The spread across seeds is always reported.
- **Budget.** The training budget (environment steps) is the same for every variant, seed and
  fold, set from a timing test before the first logged run, never from results.
- **Pass bar.** As written in `rl-1.md` ("Pass bar"), against `tsmom12`, `sma200`, `inverse-vol`
  and equal weight re-scored from 2000-01-07; 7 of 10 seeds ahead; not behind `tsmom12` since
  2003; out-of-universe sign in 2 of 3 sets. Held-out year: once, one finalist, only on a pass.
- **No tuning on the out-of-sample window.** Hyperparameters are fixed in the plan. If a
  variant fails to train at all (a bug, a divergence), the fix is noted with its date and every
  variant is rerun with it; a fix is never chosen by out-of-sample Sharpe.
