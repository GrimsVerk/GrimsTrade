# absorption-ratio: market "tightness" from the eigenvalues of sector correlations

Field: random matrix theory / principal components (Kritzman, Li, Page, Rigobon 2011,
"Principal Components as a Measure of Systemic Risk").
Written 2026-11-12 01:50 UTC, before any test was run.

## Claim

When a few principal components suddenly explain much more of the variance of US sector returns
(the market gets "tightly coupled"), risk assets are fragile. Stepping out of risk assets on a
one-sigma jump in this absorption ratio beats the same rule built on plain volatility.

## Why it might work

The original paper reports that most large US drawdowns were preceded by a spike in the ratio.
It was published with data to 2010, so 2011-2025 is a real post-publication test: the authors
never saw it.

## Why it might not

With N = 6 assets random matrix theory has nothing to clean (survey part 6); the only usable
piece is the top-eigenvalue share, and that rises with volatility because the market mode is
what gets volatile. The plain twin may carry all of it. Published timing signals usually decay.

## Rule (fixed, parameters as published)

- Inputs: daily log returns of the 9 original sector ETFs (XLK XLF XLE XLV XLY XLP XLI XLB XLU),
  available from 1998-12-22.
- AR = share of total variance explained by the top 2 eigenvectors (about one fifth of 9) of
  their covariance matrix over the last 500 trading days, exponentially weighted with a 250-day
  half-life. Computed each trading day.
- Shift = (mean AR over the last 15 days - mean AR over the last 252 days) / standard deviation
  of AR over the last 252 days.
- Each Friday: if shift > +1, the risk assets (SPY, QQQ, BTC, ETH) go to cash; GLD and TLT keep
  their slots. Otherwise equal weight of the eligible assets. Test starts when the shift exists
  (about 2001-12).

## Variants (all that will be run)

1. `six` (primary): as above. 2. `spy`: SPY alone, in or out, the cleanest replication.

## Twin and baselines

Twin `vol-shift`: the identical rule with AR replaced by SPY's 20-day realised volatility (same
15-day versus 252-day standardised shift, same threshold of +1). Benchmark: equal weight (and
buy-and-hold SPY for the `spy` variant).

## Out-of-universe

The US signal applied to (a) the other ETFs (IWM, EFA, EEM, VNQ, DBC, SLV as risk assets; IEF,
LQD kept), (b) the Nikkei, FTSE and DAX indexes, each in or out. Not applicable to the coin set
separately (no sector data), counted as two sets.

## Pass bar

The default in `protocol.md` against the twin, AND the 2011-2025 part alone must not be behind the
twin (the post-publication check). Reported separately: 2001-2010 versus 2011-2025.

## Result

See `results/absorption-ratio.md` once tested.
