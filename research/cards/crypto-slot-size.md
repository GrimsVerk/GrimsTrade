# crypto-slot-size: how big should the crypto slots be?

Field: allocation (survey part 2, F1-F3: small Bitcoin allocations; part 6: power-law tails).
Written 2026-11-12 02:05 UTC, run 3. Before any test of this rule. Seen before: in run 2 the
size of the crypto position mattered more than the timing rule on it (`results/crypto-alone.md`),
and equal weight with 1/6 in each of BTC and ETH fell 42% in two crypto winters.

## Claim

Since 2013, a book with small fixed crypto slots (5% in each of BTC and ETH, the rest equally in
the four ETFs) has a higher Sharpe and a much smaller worst loss than equal 1/6 slots.

## Why it might work

At 60-90% volatility a 1/6 slot in each coin is over half the book's risk. Diversification pays
most for the first few percent of an uncorrelated, volatile asset.

## Why it might not

Bitcoin rose about a thousandfold in this sample. Any rule that holds less of it looks worse on
return, and Sharpe over one bull-dominated decade says little about the next. This is a choice
of risk, and the test can only describe it, not validate it.

## Rule (fixed)

- Each Friday: each eligible coin gets weight c; the eligible ETFs share the rest equally.
- Decisions from 2013-01-01 (before that there is no crypto and all sizes are the same book).

## Variants (all that will be run)

1. `c05` (5% per coin, primary). 2. `c10` (10%). 3. `c00` (no crypto: the four ETFs only).

## Twin and baselines

Twin: equal weight (1/6 per asset once all exist).

## Out-of-universe

None applies: there is no second set of "coins next to ETFs". Stated as a limit; this card can
describe, not confirm.

## Pass bar

Reported, not passed or failed: Sharpe difference to equal weight with its bootstrap p-value,
growth, worst loss, and the crypto winters, for each size.

## Result

See `results/crypto-slot-size.md` once tested.
