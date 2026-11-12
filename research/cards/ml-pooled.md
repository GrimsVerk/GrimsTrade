# ml-pooled: the same models trained on 33 markets instead of six

Field: machine learning, pooled ("global") models across assets (Gu, Kelly, Xiu 2020 train one
model on every stock; Lim, Zohren, Roberts 2019 one network on 88 futures).
Written 2026-11-12 06:37 UTC, run 2. **After** seeing `ml-linear`, `ml-gbm`, `ml-filter`,
`ml-sizing`, `ml-payoff` (all failed, forecast AUC 0.48 to 0.51) and the control. The control
showed that with 6,214 forecasts on six assets a real signal weaker than a correlation of
about 0.10 cannot be told from zero, and the models had 1,600 to 7,600 rows to learn from.

## Claim

The six-asset models failed for lack of data, not lack of signal. Trained on about five times
as many rows (33 markets, the same 15 features), the same models forecast the six live assets
with real skill.

## Why it might work

A weak pattern shared by many markets (trend, volatility clustering, rebounds after
drawdowns) needs many examples to be told from noise. More markets are the only way to get
more examples without waiting decades.

## Why it might not

More rows do not help if there is nothing to find, and rows from other markets teach other
markets' habits: 1970s stock indexes, sector funds that are slices of SPY (nine near-copies
of one asset are not nine times the information), and coins that mostly fell. The control says
that even a real forecast as good as a 0.20 correlation only ties `tsmom12` on six assets.

## Rule (fixed)

Features, labels, walk-forward, purge and embargo, position rules: `protocol.md`,
"Machine-learning tests". Training rows: `protocol.md`, "Pooled training". The forecasts for
the six assets use the six assets' own features, as before. Start 1994-02-01, as the earlier
cards.

## Variants (all that will be run)

1. `gbm-pool` (primary): the `ml-gbm` primary setting and position rule, pooled rows.
2. `logit-pool`: the `ml-linear` logistic model (C by purged CV), pooled rows.
3. `gbm-pool-low`: `gbm-pool` under the `-low` position rule.

Three tries.

## Twins and baselines

Twin `tsmom12`. Also shown: equal weight, and `gbm` and `logit` (the same models on six-asset
rows), which are the direct comparison.

## Out of universe

The same pooled model traded on the 8 other ETFs, the 6 other coins and the four indexes, each
from the start day of the earlier cards. Unlike the earlier cards these sets are in the
training rows (walk-forward, so still out of sample in time); this asks whether one model for
all markets works on each, not whether a rule built on six carries over.

## Pass bar

The default in `protocol.md`, against `tsmom12`. The control says that bar is out of reach of
any plausible forecast, so a second reading is fixed here, before the run: **forecast skill
on the six assets.** AUC of `gbm-pool` at or above 0.53 (clearly above the 12-month flag
alone at 0.522, and where a planted correlation of 0.10 lands) would not pass the card but
would be a reason to keep widening the data. Below 0.53, "too little data" is answered as far
as public daily prices can answer it.

## Result

See `results/ml-pooled.md` once tested.
