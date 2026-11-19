# dip-rsi2: buying short-term dips in stock indexes

Field: practitioner short-term mean reversion (Connors & Alvarez 2008; survey part 3, D1-D3).
Written 2026-11-12 01:50 UTC, before any test was run.

## Claim

SPY and QQQ bounce after sharp short-term drops in an uptrend. A fixed, published rule for buying
such dips earns more per day in the market than buy-and-hold, also after its publication (2008)
and with fills at the next open instead of the same close.

## Why it might work

Index returns have been negatively autocorrelated at daily and weekly horizons since about 2000
(Baltussen, van Bekkum, Da). ETF costs are tiny.

## Why it might not

AQR's "Hold the Dip" finds buy-the-dip worse than buy-and-hold on Sharpe across 196 variants.
Published results fill at the close that generated the signal; our next-open fill skips the first
night, where much of a bounce may sit. The rule is in the market only a few percent of the time.

## Rule (fixed, from the published version)

- Assets: SPY, QQQ, each alone. Decide daily (exception to the weekly rule).
- Entry signal at a close: RSI(2) < 5 (Wilder smoothing), close below its 5-day average, close
  above its 200-day average.
- Exit signal: first close above the 5-day average, or 5 trading days after entry.
- Long the asset between entry and exit, cash otherwise.

## Variants (all that will be run)

1. `rsi2` (the only one), on SPY and on QQQ.

## Twin and baselines

Twin `constant`: the same asset at a constant weight equal to the rule's average exposure. Also
shown: the same rule filled at the signal's close (computed outside the gym, to measure what the
next-open fill costs; a diagnostic, logged as a robustness row).

## Out-of-universe

IWM, EFA, EEM (other equity ETFs); S&P 500 index 1962-1993, Nikkei, FTSE, DAX. Not applicable to
bonds or coins (survey part 3: daily reversal in large coins is not real), counted as two sets.

## Pass bar

The default in `protocol.md` against the twin on both SPY and QQQ, AND the 2009-2025 part alone
(after publication) must not be behind the twin. Bar 5 is replaced by: mean return per day in the
market above buy-and-hold's mean daily return, t-statistic of the difference above 2.

## Result

See `results/dip-rsi2.md` once tested.
