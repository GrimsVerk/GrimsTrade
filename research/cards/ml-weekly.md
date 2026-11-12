# ml-weekly: the same models forecasting one week ahead instead of four

Field: machine learning; breadth (Grinold 1989: the worth of a forecast grows with the square
root of the number of independent bets).
Written 2026-11-12 06:45 UTC, run 2. **After** seeing all six earlier ML cards fail, the
control (a forecast must reach a correlation of 0.2 to 0.3 to beat `tsmom12` at 13 bets a
year per asset) and `results/ml-feature-skill.md`, where the 7-day return ranked the next 28
days at AUC 0.524 with the smallest standard error of any feature (0.007).

## Claim

The monthly horizon was the handicap. Forecasting one week ahead gives four times as many
independent bets from the same history (and four times as many independent training labels),
so a signal too weak to pay monthly pays weekly.

## Why it might work

The portfolios already decide every Friday; only the label changes. Short-horizon effects
(one-week continuation or reversal, volatility shocks) are what a 28-day label blurs.

## Why it might not

A week of returns is mostly noise, so the forecast has to be found in a worse
signal-to-noise ratio. A model that changes its mind weekly trades more, and crypto costs 60
basis points a round trip. Run 1 found the weekly-scale effects it tested (`dip-rsi2`, daily
crypto reversal) real but tiny or gone.

## Rule (fixed)

Everything as `protocol.md`, "Machine-learning tests", except the label: `protocol.md`,
"Weekly labels". Same 15 features, same yearly refits, same position rules, weekly decisions,
start 1994-02-01.

## Variants (all that will be run)

1. `gbm-wk` (primary): the `ml-gbm` primary setting and position rule, 7-day labels.
2. `logit-wk`: the `ml-linear` logistic model (C by purged CV), 7-day labels.
3. `gbm-wk-low`: `gbm-wk` under the `-low` position rule.

Three tries.

## Twins and baselines

Twin `tsmom12`. Also shown: equal weight. The 28-day versions of the same models are in
`results/ml-gbm.md` and `results/ml-linear.md` (`gbm` 0.81, `logit` 0.89).

## Out of universe

Primary refitted unchanged on the 8 other ETFs, the 6 other coins and the four indexes.

## Pass bar

The default in `protocol.md`, against `tsmom12`. Second reading, fixed here: AUC of `gbm-wk`
for the next week's direction on the six assets at or above 0.52. With about 6,300 forecasts
that hardly overlap, 0.52 is more than two standard errors from a coin toss; below it there
is no weekly forecast to speak of either.

## Result

See `results/ml-weekly.md` once tested.
