# crowded-trend: halve the book when every asset is in trend

Field: evolutionary game theory (frequency-dependent fitness). It is mechanism G2 of
`wide-1.md` step 1 ("when every trend signal agrees, the trade is crowded"), which wide-1 killed
without a test as "leaving early".
Written 2026-11-18 11:19 UTC, run wide-2, before any test or number of this card. Seen before
writing: the results of `trend-age` (-0.06) and `patch-leaving` (-0.19), both failures. After
those two I wrote that I saw no reason to card a third price-only mechanism; this card is made
because the coordinator asked for a third pick, and my prior is low.

## Why this one, as the third pick of the 42

- Price-only, one function, one run on the existing harness.
- The share of assets in trend (`breadth`) was an ML input with no skill, but no row in
  `tries.md` runs it as a rule.
- It acts in many separate weeks, not in 4-7 bear markets.

## Claim

A strategy's payoff falls as more players use it. When all assets are in an up-trend at once,
trend followers everywhere hold the same full book; the next shock makes them all sell together.
Holding half then avoids part of the common fall.

## Why it might not

"All in trend" is also simply a good market. Halving the book then gives up return in the best
periods, and cash earns 0. Every "step out when X" gate tested so far failed.

## Rule (fixed, no fitted parameter)

- Weekly decisions on Friday's close; base weights are `tsmom12`'s (equal slots).
- If at least three assets are eligible and every eligible asset has a positive 365-day return,
  every weight is halved. Otherwise the weights are the twin's.

## Variants (all that will be run)

1. `crowd` (only variant): as above.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, and the share of Fridays on which the rule acts.

## Out-of-universe

All three sets: the 8 other ETFs and the 6 other coins as books, the four indexes as one
portfolio (`idx`).

## Pass bar

The default in `protocol.md` for `crowd` against `tsmom12`, with bar 1 stricter:

1. (stricter) **p < 0.10 / 42 = 0.0024.** Three of wide-1's 42 uncarded mechanisms have now
   been picked (`trend-age`, `patch-leaving`, this). The bar counts every pick out of the 42,
   so each test is read at 0.10 / 42.
2. to 5. as in the protocol.

Held-out year: once, `crowd` only, only if all bars pass.

## My guess before any number

Chance it passes: 1%. Expected difference to the twin: -0.10 to +0.02 Sharpe.

## Result

See `results/crowded-trend.md` once tested.
