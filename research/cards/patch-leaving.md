# patch-leaving: leave an asset when its trend is below the average of all assets

Field: behavioural ecology (optimal foraging, Charnov's marginal value theorem). It is mechanism
E6 of `wide-1.md` step 1 ("leave a patch when its yield falls below the average of all patches,
net of travel cost"), which wide-1 killed without a test as "relative momentum with a switching
band".
Written 2026-11-18 11:17 UTC, run wide-2, before any test or number of this card. Seen before
writing: everything `cards/trend-age.md` lists, and that card's result (fails: a delayed entry
trails `tsmom12` by 0.06).

## Why this one, as the second pick of the 42

- Needs only the six assets' weekly closes and the existing harness: one function, one run.
- No row in `tries.md` runs relative (cross-sectional) momentum on the six assets: breadth-1
  ran it on 33 markets and on coins, short-1 as a long-short book, the ML runs only as an input
  (`rank_12m`). The kill was by analogy.
- It decides every week for every asset, so it does not rest on a handful of episodes.
- Unlike the first pick it does not sit in cash: wide-1's lesson 3 was that stepping out of an
  asset is an expensive way to trade a relative effect.

## Claim

A forager should leave a patch when its intake rate drops below the habitat's average. Read for
the book: an asset whose trend is positive but weaker (per unit of risk) than the average asset's
is a depleted patch; its slot earns more in the assets that are above average.

## Why it might not

Relative momentum added nothing on top of trend in breadth-1. Moving the freed weight into the
strongest assets concentrates the book (often into coins), which raises risk and drawdown.

## Rule (fixed, no fitted parameter)

- Weekly decisions on Friday's close. n = number of eligible assets; `tsmom12` holds 1/n in
  each asset whose 365-day return is positive. H = the number it holds.
- z(asset) = 365-day log return / EWMA volatility (60-bar half-life, annualised): the
  protocol's `z(365)`. m = mean of z over all eligible assets (in trend or not).
- Stay set S = assets that `tsmom12` holds and whose z >= m. S is never empty when H > 0.
- Weights: the twin's total weight H/n, split equally among the assets in S. So total exposure
  equals the twin's at every decision; only where it sits differs. No band beyond the gym's
  costs (the "travel cost" is paid there).

## Variants (all that will be run)

1. `mvt` (only variant): as above.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight.

## Out-of-universe

All three sets: the 8 other ETFs and the 6 other coins as books, and the four indexes as one
portfolio (`idx`; the rule builds a portfolio).

## Pass bar

The default in `protocol.md` for `mvt` against `tsmom12`, with bar 1 stricter:

1. (stricter) **p < 0.10 / 42 = 0.0024.** Two of wide-1's 42 uncarded mechanisms have now been
   picked (this and `trend-age`). The bar counts every pick out of the 42, so each test is read
   at 0.10 / 42, the same line `trend-age` was read at.
2. to 5. as in the protocol. Bar 3 (max drawdown at most 5 points worse) is the one I expect
   concentration to break.

Held-out year: once, `mvt` only, only if all bars pass.

## My guess before any number

Chance it passes: 2%. Expected difference to the twin: -0.15 to +0.05 Sharpe, with a clearly
deeper drawdown.

## Result

See `results/patch-leaving.md` once tested.
