# ml-linear: a regularised linear model on simple features

Field: machine learning, the simple baseline (ladder rung 3 in `docs/DESIGN.md`; Gu, Kelly & Xiu
2020 find linear models with shrinkage hard to beat on monthly returns).
Written 2026-11-12 02:15 UTC, run 2. Before any model was fitted. Seen before: every result of
run 1, including `tsmom12`, `sma200` and `ensemble-tsmom` on all universes.

## Claim

A logistic regression with ridge shrinkage, fed 15 plain features (trend at five horizons,
volatility, drawdown, cross-asset breadth) and trained to forecast whether an asset is higher
28 days later, sizes positions better than the 12-month trend rule alone.

## Why it might work

`tsmom12` uses one feature and one threshold. A fitted model can weigh several horizons, step
aside when volatility jumps, and learn how much each matters from the data.

## Why it might not

Monthly returns are almost unpredictable; the fitted weights are mostly noise, and with strong
shrinkage the model forecasts the average and turns into equal weight. Run 1: four horizons
instead of one gained +0.05 Sharpe, not distinguishable from zero.

## Rule (fixed)

Rows, features, labels, purged and embargoed walk-forward, position sizing, first-model rule
and S&P 500 warm-up: exactly as in `protocol.md`, section "Machine-learning tests".

- `logit` (primary): features standardised on the training rows; logistic regression, L2
  penalty, target `up`. Penalty strength C chosen by purged CV from {0.001, 0.01, 0.1, 1} at
  each yearly fit.
- `logit-hard`: the same model, full slot whenever P(up) > 0.5.
- `ridge`: ridge regression on `ra`, alpha chosen by purged CV from {10, 100, 1000, 10000}.

## Variants (all that will be run)

`logit`, `logit-hard`, `ridge`. Three tries.

## Twins and baselines

Twin `tsmom12`. Also shown: `sma200`, equal weight.

## Out-of-universe

Refitted unchanged on the 8 other ETFs, the 6 other coins and the four indexes (pooled).

## Pass bar

The default in `protocol.md`, against `tsmom12`.

## Also reported (not part of the bar)

Forecast skill of the walk-forward forecasts: AUC and hit rate against the realised 28-day
sign, next to what `up_12m` alone achieves; which features carry the weight.

## Result

See `results/ml-linear.md` once tested.
