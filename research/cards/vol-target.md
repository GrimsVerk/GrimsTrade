# vol-target: cap each slot by an absolute volatility budget

Field: volatility targeting (Harvey et al. 2018, Man Group; survey part 2) and Kelly sizing.
Written 2026-11-12 02:00 UTC, run 2. Before any test of this rule, but AFTER run 1.

What was already seen (so this card is not blind): in run 1 the kelly-shrunk rule, which also
sizes by absolute volatility, gave the same growth at 37% volatility instead of 95% on the six
other coins, and its quarter-Kelly variant avoided part of the dot-com bust. The parameters below
are the ones survey part 2 proposed before those results (40%, 20 days), not tuned on them.

## Claim

Scaling each asset's equal slot down when its own recent volatility is above 40% a year beats
plain equal weight on Sharpe and on drawdown. In practice this sizes BTC and ETH down most of the
time and the ETFs only in crises.

## Why it might work

Volatility is persistent and forecastable; returns are not. Published evidence: targeting cuts
tails reliably and helps Sharpe for risk assets. Crypto volatility of 60-100% makes an equal slot
dominate the book's risk.

## Why it might not

Without leverage only the "scale down" half exists, and with cash at 0 every scaled-down dollar
gives up return. Run 1's volatility switch (`vol-calm`) was worse than doing nothing.

## Rule (fixed)

- Each Friday, each eligible asset: weight = equal slot x min(1, 40% / vol20), where vol20 is the
  annualised root-mean-square of its last 20 daily log returns.

## Variants (all that will be run)

1. `t40` (primary). 2. `t25` (target 25%).

## Twins and baselines

Twin: equal weight. Also shown: `inverse-vol`.

## Out-of-universe

Unchanged on the 8 other ETFs, the 6 other coins, and the 4 indexes as one portfolio.

## Pass bar

The default in `protocol.md`.

## Result

See `results/vol-target.md` once tested.
