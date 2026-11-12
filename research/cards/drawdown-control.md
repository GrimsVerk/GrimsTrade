# drawdown-control: sell gradually into a drawdown

Field: optimal stopping / stochastic control (Grossman & Zhou 1993; Kaminski & Lo 2014 on when
stop rules help).
Written 2026-11-12 01:50 UTC, before any test was run.

## Claim

Cutting an asset's position in proportion to its drawdown from its one-year high, scaled by the
asset's own volatility, beats the all-or-nothing 200-day moving-average switch: similar
protection, fewer whipsaws.

## Why it might work

The optimal policy under a drawdown limit holds risk in proportion to the cushion left (Grossman
& Zhou). Kaminski & Lo show stop rules add value exactly when returns trend, which is the same
condition the moving-average switch relies on, but a proportional rule never bets everything on
one crossing.

## Why it might not

A proportional rule is a moving average of many all-or-nothing rules; on average it should earn
what they earn. It sells low and buys back higher by construction and needs trends to pay for
that. It is slow to get back in after a V-shaped crash.

## Rule (fixed)

- Per asset. DD = 1 - close / (highest close of the last 252 bars; 365 for crypto).
- Tolerance D = 1.0 x the asset's annualised volatility (EWMA, 250-bar half-life).
- Each Friday: weight = equal slot x max(0, 1 - DD / D). Example: SPY with 16% volatility is half
  sold at 8% below its high and fully sold at 16%.

## Variants (all that will be run)

1. `d1.0` (primary). 2. `d1.5` (tolerance 1.5 x volatility).

## Twin and baselines

Twin `sma200`. Benchmark: equal weight.

## Out-of-universe

Unchanged on the 8 other ETFs, the 6 other coins and the 4 index markets.

## Pass bar

The default in `protocol.md` against the twin.

## Result

See `results/drawdown-control.md` once tested.
