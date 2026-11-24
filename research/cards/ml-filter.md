# ml-filter: the 12-month trend rule with a model deciding how much to trust it

Field: machine learning, meta-labelling (López de Prado 2018, ch. 3).
Written 2026-11-12 02:15 UTC, run 2. Before any model was fitted. Seen before: every result of
run 1. Nothing from `ml-linear` or `ml-gbm` (cards written at the same time).

## Claim

`tsmom12` decides when to hold an asset. A model trained only on the weeks the rule was
holding, to forecast whether those positions gained over the next 28 days, can cut the rule's
bad trades (late entries, tops) and so beat it.

## Why it might work

The model has an easier job than forecasting everything: the trend rule already picked the
side, the model only grades the trade. That is the standard argument for meta-labelling.

## Why it might not

A model that finds nothing leaves the rule as it is. One that finds noise removes good trades
as often as bad ones and adds turnover.

## Rule (fixed)

As in `protocol.md`, section "Machine-learning tests", with two changes: training rows are
only those where `up_12m` = 1 (the rule was holding), and a position is only ever taken where
`tsmom12` holds. Weight = slot x clip(q, 0, 1) if `tsmom12` is on, else 0. The average label
in q is taken over those training rows.

## Variants (all that will be run)

1. `meta-gbm` (primary): the `ml-gbm` primary setting.
2. `meta-logit`: the `ml-linear` primary model.
3. `and-gbm`: no separate training: the `ml-gbm` primary model's weight, but only where
   `tsmom12` is on.

Three tries.

## Twins and baselines

Twin `tsmom12`. Also shown: equal weight.

## Out-of-universe

Primary refitted unchanged on the 8 other ETFs, the 6 other coins and the four indexes (pooled).

## Pass bar

The default in `protocol.md`, against `tsmom12`.

## Result

See `results/ml-filter.md` once tested.
