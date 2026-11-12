# hawkes-clustering: self-exciting crash days

Field: point processes (Hawkes 1971; Bacry, Mastromatteo, Muzy 2015).
Written 2026-11-12 01:50 UTC, before any test was run.

## Claim

Large down days arrive in clusters: each one raises the chance of the next for a while. A Hawkes
process fitted to past large down days gives a "crash intensity"; stepping aside while the
intensity is above its long-run average beats the plain volatility switch.

## Why it might work

A Hawkes model separates the background rate of shocks from the self-excited part and has its own
memory length (fitted), instead of a fixed volatility window. It reacts to the count and timing
of shocks, not to their size, so a single huge day does not dominate.

## Why it might not

At daily frequency the intensity is an exponentially weighted count of large down days, which is
nearly the same thing as an exponentially weighted variance. The Hawkes literature is about
ticks; at daily bars it is used as a risk model, not a signal. Stepping aside after shocks also
misses the rebounds that follow them.

## Rule (fixed)

- Per asset. Event on day t: log return below -2 x the EWMA volatility (60-bar half-life)
  estimated through day t-1.
- Intensity: lambda_t = mu + alpha x sum over earlier events of exp(-beta x bars since event).
- Fit (mu, alpha, beta) by maximum likelihood (daily Bernoulli approximation) on all events so
  far; refit on the first Friday of each calendar year; no fit before 1,000 bars (slot held until
  then, as for the twin). Constraint alpha < beta (stationary).
- Each Friday: hold the asset's equal slot if lambda_t is at or below the model's long-run average
  intensity mu / (1 - alpha/beta), else cash.

## Variants (all that will be run)

1. `down2` (the only one).

## Twin and baselines

Twin `vol-calm` (as on the hmm-regime card: EWMA volatility below its expanding median).
Benchmark: equal weight.

## Out-of-universe

Unchanged on the 8 other ETFs, the 6 other coins and the 4 index markets.

## Pass bar

The default in `protocol.md` against the twin.

## Result

See `results/hawkes-clustering.md` once tested.
