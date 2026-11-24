# fracdiff-momentum: a power-law memory for trend

Field: fractional calculus / long-memory time series (Hosking 1981; Lopez de Prado 2018, ch. 5).
Written 2026-11-12 01:50 UTC, before any test was run.

## Claim

A fractionally differenced log price weights past returns by a slowly decaying power law. Used as
a trend signal (long when positive, else cash), it beats the two classic trend signals: the
12-month return (flat weights, hard cut-off) and the 200-day average (linearly falling weights).

## Why it might work

Fractional differencing of order d keeps as much memory as stationarity allows. Its return
weights have no cliff: a crash leaves the signal gradually instead of dropping out on day 253,
and recent returns count more than old ones, so the signal should turn faster at tops.

## Why it might not

It is a linear filter of past returns, like every moving-average rule (survey part 6, items 2-3).
All three signals are kernels on the same returns; the literature finds trend results insensitive
to the kernel. Heavier weight on recent days means more turnover.

## Rule (fixed)

- Per asset. Fractional-differencing weights for order d: w_0 = 1, w_k = -w_(k-1) (d - k + 1) / k.
  Return weights c_j = w_0 + ... + w_j (positive, falling like j^-d). Window K = 500 bars for
  ETFs and indexes, 730 for crypto (about two years on each clock).
- Signal m = sum over j < K of c_j x (log return j bars ago). This is the fractionally
  differenced log price without the leftover price-level term that the truncation leaves.
- Each Friday: hold the asset's equal slot if m > 0, else cash. Needs K bars; before that the
  slot is in cash, as for the twins before their own warm-up.
- d = **0.4** (the middle of the 0.3-0.5 range reported as the least differencing that makes
  price series stationary).

## Variants (all that will be run)

1. `d0.4` (primary). 2. `d0.3`. 3. `d0.5`.

## Twins and baselines

Twin A `tsmom12`, twin B `sma200`, both started at the same date as this rule (after K bars) so
that warm-up does not decide the comparison. Benchmark: equal weight.

## Out-of-universe

Unchanged on the 8 other ETFs, the 6 other coins and the 4 index markets (equal slots).

## Pass bar

The default in `protocol.md` against the better of the two twins.

## Result

See `results/fracdiff-momentum.md` once tested.
