# universal-portfolio: Cover's universal portfolio

Field: information theory (Cover 1991, "Universal Portfolios").
Written 2026-11-12 01:50 UTC, before any test was run.

## Claim

Cover's universal portfolio, which needs no forecasts, no statistics and no parameters, beats
the equal-weight benchmark on the six assets after costs.

## Why it might work

It is the wealth-weighted average of all constant-mix portfolios. Its wealth is guaranteed to
grow, in the long run, at the same exponential rate as the best constant mix chosen in
hindsight, for any price path at all. It is long-only and unlevered by construction, which is
exactly our gym. Cash can be one of the "assets", so it can learn to hold cash.

## Why it might not

The guarantee is asymptotic and the regret term is large for a few thousand days. In practice it
starts as equal weight and drifts slowly toward whatever did best, which is a very slow momentum
tilt. Published horse races find it close to equal weight. With Bitcoin in the set it will pile
into Bitcoin after the fact.

## Rule (fixed)

- Assets: the six plus cash (7 corners). 20,000 constant-mix portfolios drawn uniformly from the
  simplex (Dirichlet(1,...,1), seed 0).
- Each Friday: every constant-mix portfolio's wealth is multiplied by its return over the week
  (Friday close to Friday close on the business-day grid, no costs inside the learner; an asset
  not yet eligible counts as cash). The portfolio held for the next week is the wealth-weighted
  average of the 20,000 mixes; weight on a not-yet-eligible asset stays in cash.
- Costs are paid in the gym like for any strategy.

## Variants (all that will be run)

1. `up` (the only one).

## Twin and baselines

Twin: equal weight of the eligible assets (the benchmark). Also shown: the uniform mix with cash
(1/7 each), which is where the universal portfolio starts.

## Out-of-universe

Unchanged on the 8 other ETFs plus cash, the 6 other coins plus cash, the 4 indexes plus cash.

## Pass bar

The default in `protocol.md`, with equal weight as the twin.

## Result

See `results/universal-portfolio.md` once tested.
