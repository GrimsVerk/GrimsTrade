# ensemble-tsmom: trend measured at four horizons at once

Field: trend following (survey part 1, testable idea 2; Man AHL on signal speed).
Written 2026-11-12 02:00 UTC, run 2. Before any test of this rule. Seen before: the plain
`tsmom12` and `sma200` results on all universes (they are the baselines).

## Claim

Holding each asset in proportion to how many of its 1-, 3-, 6- and 12-month returns are positive
beats the single 12-month rule: it leaves falling markets sooner, re-enters sooner, and never
bets everything on one lookback.

## Why it might work

No single lookback is right; averaging horizons is the standard defence against picking a lucky
one, and partial positions cut whipsaw cost.

## Why it might not

Short horizons are noise and add turnover (run 1: the fast-weighted fracdiff kernel lost badly to
12-month momentum). Three of the four horizons here are shorter than 12 months.

## Rule (fixed)

- Each Friday, each eligible asset: weight = equal slot x (number of positive returns among the
  last 30, 91, 182 and 365 calendar days) / 4.

## Variants (all that will be run)

1. `e4` (the only one).

## Twins and baselines

Twin `tsmom12`. Also shown: `sma200`, equal weight.

## Out-of-universe

Unchanged on the 8 other ETFs, the 6 other coins and each of the 4 index markets.

## Pass bar

The default in `protocol.md`.

## Result

See `results/ensemble-tsmom.md` once tested.
