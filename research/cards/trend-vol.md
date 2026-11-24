# trend-vol: 12-month trend, with each slot capped by volatility

Field: trend following plus volatility targeting; the combination the survey singles out (part 1,
Kim-Tse-Wald: trend without volatility scaling is about buy-and-hold; part 5, Nagel: the best
machine-learning timing model is volatility-timed momentum underneath).
Written 2026-11-12 02:00 UTC, run 2. Before any test of this rule, but AFTER run 1: `tsmom12` is
the strongest plain rule seen on train, and volatility sizing looked useful on coins. This card
combines two things already seen to work in-sample, so its train result will flatter it. That is
why its bar is stricter and why only the held-out year and forward paper can confirm it.

## Claim

Hold each asset's equal slot only when its 12-month return is positive, and scale that slot down
when the asset's recent volatility is above 40%. This beats plain 12-month trend on Sharpe and
drawdown.

## Why it might work

Trend removes the long bear markets; volatility sizing removes the overweight of crypto in the
book's risk and the worst weeks inside an uptrend. The two protect against different things.

## Why it might not

Both step aside in the same episodes, so the second layer may add little but lost return.

## Rule (fixed)

- Each Friday, each eligible asset: weight = equal slot x [365-day return > 0] x
  min(1, 40% / vol20), vol20 as on the vol-target card.

## Variants (all that will be run)

1. `tv40` (the only one).

## Twins and baselines

Twin `tsmom12`. Also shown: equal weight.

## Out-of-universe

Unchanged on the 8 other ETFs, the 6 other coins and each of the 4 index markets.

## Pass bar

Stricter than the default: bar 1 at p < 0.05 instead of 0.10, and the Sharpe difference must be
positive in all three out-of-universe sets, not two.

## Result

See `results/trend-vol.md` once tested.
