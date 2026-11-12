# ml-gbm: gradient boosting on simple features

Field: machine learning (ladder rung 3 in `docs/DESIGN.md`; López de Prado 2018 for the
validation; Gu, Kelly & Xiu 2020 for trees on return forecasting).
Written 2026-11-12 02:15 UTC, run 2. Before any model was fitted. Seen before: every result of
run 1. Nothing from `ml-linear` (its card was written at the same time).

## Claim

Boosted trees on the same 15 features find what a linear model cannot: thresholds (trend on or
off), and interactions (trend matters more when volatility is high; a drawdown means something
different in a broad sell-off). Their forecasts size positions better than `tsmom12`, and
better than the linear model.

## Why it might work

`tsmom12` is itself a one-split tree. If the true rule has two or three splits, boosting should
find it.

## Why it might not

About 8,000 overlapping weekly rows hold only some 400 independent asset-months per decade of
signal that is tiny to begin with. Trees fit noise eagerly; what looks like an interaction in
1994-2010 need not hold in 2011-2025.

## Rule (fixed)

Rows, features, labels, purged and embargoed walk-forward, position sizing, first-model rule
and S&P 500 warm-up: exactly as in `protocol.md`, section "Machine-learning tests".

Model: scikit-learn `HistGradientBoostingClassifier` on target `up`, no early stopping,
`random_state=0`. The primary setting is small on purpose:

- `gbm` (primary): learning rate 0.05, 100 trees, depth 3, at least 100 rows per leaf, L2 1.0.

## Variants (all that will be run)

1. `gbm` (primary).
2. `gbm-hard`: same model, full slot whenever P(up) > 0.5.
3. `gbm-reg`: `HistGradientBoostingRegressor`, same setting, squared error on `ra`.
4. `gbm-cv`: depth from {1, 3} and trees from {25, 100, 400} chosen by purged CV at each
   yearly fit (rest as the primary).
5. Sweep, one change each from the primary, to show how much the answer depends on the
   setting: `gbm-d1` (depth 1: no interactions), `gbm-d6` (depth 6), `gbm-n25` (25 trees),
   `gbm-n400` (400 trees), `gbm-leaf20` (20 rows per leaf).

Nine tries.

## Twins and baselines

Twin `tsmom12`. Also shown: `ml-linear/logit`, `sma200`, equal weight.

## Out-of-universe

Primary refitted unchanged on the 8 other ETFs, the 6 other coins and the four indexes (pooled).

## Pass bar

Stricter than the default: the default bar in `protocol.md` against `tsmom12`, AND on the six
assets the primary is not behind `ml-linear/logit` on Sharpe (else boosting adds nothing),
AND the median Sharpe of the five sweep settings is ahead of `tsmom12` (else the result
hangs on one setting).

## Also reported (not part of the bar)

Forecast skill (AUC, hit rate) of the walk-forward forecasts next to the linear model's and
`up_12m` alone; permutation importance of the features in the last fit of the train period.

## Result

See `results/ml-gbm.md` once tested.
