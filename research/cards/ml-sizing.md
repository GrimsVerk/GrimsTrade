# ml-sizing: the same models with a position rule that follows the forecast

Field: machine learning, bet sizing (López de Prado 2018, ch. 10; Grinold's "alpha is
proportional to the forecast").
Written 2026-11-12 02:25 UTC, run 2. **After** seeing `ml-linear`, `ml-gbm`, `ml-filter` (all
failed; forecast AUC 0.49 to 0.51) and the first positive control, which showed that the
sizing rule used there wastes most of a signal. No model has been run with the rules below.

## Claim

The first three cards failed partly because of how forecasts were turned into positions. With
a rule that lets the position follow the forecast, the same models beat `tsmom12`.

## Why it might work

The control: a planted signal of correlation 0.20 only matched `tsmom12` under the old rule. If
the real models hold a weak signal, a better converter could show it. Sizing by forecast also
picks up what the trees leaned on (less when volatility is high).

## Why it might not

The skill tables do not depend on sizing and show no skill (AUC about 0.50, below the single
flag `up_12m`). A converter cannot create what the forecast does not hold; a sharper one turns
forecast noise into more trading.

## Rule (fixed)

Models, rows, features, labels, walk-forward: as in `protocol.md`, "Machine-learning tests".
Position rules `-prop` and `-low`: as in `protocol.md`, "Two more ways from forecast to
position".

## Variants (all that will be run)

1. `gbm-prop` (primary): the `ml-gbm` primary model, proportional rule.
2. `logit-prop`. 3. `gbm-low`. 4. `logit-low`.
5. `gbm-reg-prop`, 6. `ridge-prop`: the two regressors on risk-adjusted return, where the
   proportional rule is the textbook one (position in proportion to expected return per unit
   of risk).

Six tries.

## Twins and baselines

Twin `tsmom12`. Also shown: equal weight, and the same models under the old rule.

## Out-of-universe

Primary refitted unchanged on the 8 other ETFs, the 6 other coins and the four indexes (pooled).

## Pass bar

The default in `protocol.md`, against `tsmom12`. And a check on the test itself, reported next
to the verdict: on the control, the same rule with a planted correlation of 0.10 must come out
ahead of `tsmom12`. If it does not, the Sharpe comparison had no power and the card is judged on
forecast skill alone.

## Result

See `results/ml-sizing.md` and `results/ml-control.md` once tested.
