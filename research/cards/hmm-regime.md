# hmm-regime: a two-state hidden Markov model as a risk switch

Field: statistics / regime models (Hamilton 1989; Ang & Bekaert; Nystrup et al.).
Written 2026-11-12 01:50 UTC, before any test was run.

## Claim

A two-state Gaussian hidden Markov model fitted on an asset's own daily returns, using only past
data, tells calm from turbulent regimes in real time. Holding the asset only while the model says
"calm" beats two plain switches: a volatility threshold and the 200-day moving average.

## Why it might work

Volatility clusters and turbulent regimes carry lower (often negative) average returns in stocks.
An HMM estimates the regime with persistence built in (it does not flip on one bad day) and with a
threshold learned from the data rather than chosen by hand.

## Why it might not

On daily returns a two-state Gaussian HMM is close to a smoothed volatility threshold; the plain
twin should capture most of it. Regime models are known for good in-sample fits and late
real-time calls. For crypto, turbulent regimes have been the profitable ones as often as not.

## Rule (fixed)

- Per asset. States: two Gaussians (own mean and variance each), first-order Markov chain.
- Fit: Baum-Welch (EM) on all of the asset's log returns up to the fit date; at most 30
  iterations; first fit started from "calm = returns smaller than the median absolute return,
  turbulent = the rest" with 0.98 on the diagonal of the transition matrix; later fits start from
  the previous fit. Refit on the first Friday of each calendar year. No fit before 1,000 bars: until
  then the asset's slot is simply held (the twins follow the same rule).
- Each Friday: run the forward filter with the latest fitted parameters over all returns so far.
  "Calm" is the state with the smaller variance. Hold the asset's equal slot if
  P(calm | returns so far) > 0.5, else cash.

## Variants (all that will be run)

1. `hard` (primary): as above. 2. `soft`: slot weight = P(calm), no threshold.

## Twins and baselines

- Twin A `vol-calm`: hold the slot while the 30-bar-half-life EWMA volatility is below its own
  expanding median (all history so far); slot held before 1,000 bars.
- Twin B `sma200`.
- Benchmark: equal weight.

## Out-of-universe

Unchanged on the 8 other ETFs, the 6 other coins and the 4 index markets (equal slots).

## Pass bar

Stricter than the default: the default bar against twin A (p < 0.10), AND not behind twin B on
Sharpe on the six assets.

## Result

See `results/hmm-regime.md` once tested.
