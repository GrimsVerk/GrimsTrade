# ml-payoff: train the model on what a position earns, not on which way the price goes

Field: machine learning, cost-sensitive learning (Elkan 2001; López de Prado 2018, ch. 4, on
weighting samples by return).
Written 2026-11-12 02:30 UTC, run 2. **After** seeing `ml-linear`, `ml-gbm`, `ml-filter`,
`ml-sizing` (all failed) and the control. What those showed: forecasting direction has no
skill here; `up_12m` itself calls direction worse than "always up" yet earns the best Sharpe,
because the months it sits out are the large losses; and the direction models underweight
Bitcoin for going up less often. No model has been trained with payoff weights.

## Claim

The earlier models were aimed at the wrong target. Trained on payoff (each month counted by
its size), a model learns the rule the trend rule approximates, "be out when the expected
return is negative", and with 15 features to choose from it does so better than `tsmom12`.

## Why it might work

`tsmom12` is one split on one feature. The best payoff-weighted split may sit elsewhere (a
different horizon, a drawdown, volatility), and two or three splits may beat one.

## Why it might not

Payoff weights hand the training to the largest moves: a few crypto months and a few crashes.
That is a handful of events; a rule fitted to them is fitted to anecdotes. And the control
showed that on six assets even a strong forecast only ties the trend rule.

## Rule (fixed)

Rows, features, walk-forward, first-model rule, warm-up: `protocol.md`, "Machine-learning
tests". Weights and targets: `protocol.md`, "Payoff-weighted training". Position: the full
slot when the weighted P(up) > 0.5 (or the `raw` forecast > 0), else nothing.

## Variants (all that will be run)

1. `gbm-pay` (primary): the `ml-gbm` primary setting, payoff weights.
2. `logit-pay`: the `ml-linear` logistic model (C by purged CV), payoff weights.
3. `tree-pay`: one decision tree, depth 2, at least 200 rows per leaf, payoff weights: the
   best rule of at most two questions. Printed in the result, so it can be read.
4. `gbm-raw`: boosted regression on the `raw` target, same setting, no weights.

Four tries.

## Twins and baselines

Twin `tsmom12`. Also shown: equal weight, and `gbm` and `logit` from the earlier cards.

## Out-of-universe

Primary refitted unchanged on the 8 other ETFs, the 6 other coins and the four indexes (pooled).

## Pass bar

The default in `protocol.md`, against `tsmom12`. Given the control, matching `tsmom12` without
passing would still be worth stating: it would mean the model rediscovered the trend rule.

## Result

See `results/ml-payoff.md` once tested.
