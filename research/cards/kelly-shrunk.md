# kelly-shrunk: fractional Kelly sizing under an equal-Sharpe prior

Field: information theory / gambling maths (Kelly 1956, Thorp, MacLean-Thorp-Ziemba).
Written 2026-11-12 01:50 UTC, before any test was run.

## Claim

Sizing the six assets by half Kelly, with returns NOT forecast but assumed proportional to risk
(every asset has the same Sharpe ratio), beats naive inverse-volatility weights on Sharpe and
drawdown, and beats equal weight clearly.

## Why it might work

The growth-optimal bet is f* = inverse(covariance) x expected returns. Expected returns cannot be
estimated from a few years of data, and full Kelly on a wrong estimate overbets (survey part 6,
item 11). The honest way out is a prior that needs no forecast: mean_i = S x vol_i. Then
f*_i = S x (inverse(correlation) x 1)_i / vol_i. This does two things inverse-vol does not:

- it counts correlated assets (SPY and QQQ; BTC and ETH) as partly the same bet;
- it has an absolute scale: when every volatility is high (2008, March 2020, crypto alone) the
  Kelly fractions add up to less than 1 and the rest is cash. Inverse-vol is always fully
  invested.

## Why it might not

With six assets and a no-leverage cap, the fractions add to more than 1 most of the time and get
scaled down to 1, leaving only the correlation correction. That correction is small and noisy.
The absolute scale only bites in crises, where it is plain volatility targeting.

## Rule (fixed)

- Each Friday. Assets: the eligible ones. Returns: business-day grid log returns, last 500 rows
  (fewer while an asset is young, never under 250), EWMA weights with a 60-row half-life.
- vol_i: annualised (252). Correlation: from the same weighted returns, shrunk halfway to the
  identity matrix (fixed 0.5, not fitted).
- f_i = k x (inverse(correlation) x 1)_i / vol_i, negatives set to 0. If the f_i add to more than
  1 they are scaled to add to 1. No other cap.
- k = fraction x prior Sharpe = 0.5 x 0.4 = **0.2** (half Kelly at a prior Sharpe of 0.4).

## Variants (all that will be run)

1. `k0.2` (primary). 2. `k0.1` (quarter Kelly). 3. `k0.4` (full Kelly at the same prior).

## Twin and baselines

Twin: `inverse-vol`. Benchmark: equal weight. Also shown: 60/40, buy-and-hold SPY and BTC.

## Out-of-universe

The same rule as a portfolio of (a) the 8 other ETFs, (b) the 6 other coins, where all
volatilities are high and the absolute Kelly scale should matter most, (c) the 4 index markets.
Twin there: inverse-vol of the same set.

## Pass bar

The default in `protocol.md`, on the primary variant. Also reported, not part of the bar:
annualised log growth (what Kelly maximises) against the twin.

## Result

See `results/kelly-shrunk.md` once tested.
