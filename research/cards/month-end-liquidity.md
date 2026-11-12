# month-end-liquidity: the turn-of-month window

Field: market microstructure / calendar (Etula, Rinne, Suominen, Vaittinen 2020, "Dash for
Cash"; survey part 3, E1-E3).
Written 2026-11-12 01:50 UTC, before any test was run.

## Claim

Stocks and long Treasuries earn more per day in the window around the month end (from 3 trading
days before the last trading day to 3 after it) than on other days, because institutions sell
before month end to raise cash and prices recover. Still true after the paper's sample (ends 2013).

## Why it might work

A dated, mechanical cause (payment cycles and settlement lags), found in 23 markets. One round
trip a month at about 4 bps is cheap.

## Why it might not

A competing paper says the turn-of-month effect vanished after 2001. Settlement moved from T+3
to T+2 (2017) and T+1 (2024), which shifts or removes the cause. We fill at the open, and cash
earns 0 for the other two thirds of the month.

## Rule (fixed)

- Assets: SPY, QQQ, TLT, each alone. T = last trading day of the month. The trading calendar
  (dates only, never prices) is taken as known in advance, as it is in real life.
- Decide daily (an exception to the weekly rule; the card needs exact days): be long from the open
  of T-3 to the open of T+4, else cash. That is, the decision after the close of T-4 buys and the
  decision after the close of T+3 sells.

## Variants (all that will be run)

1. `window` (the only one), on each of SPY, QQQ, TLT.

## Twin and baselines

Twin `constant`: the same asset held at a constant weight equal to the rule's average exposure
(about one third). Same average risk taken, no timing. Also shown: mean daily return inside and
outside the window, with a t-test.

## Out-of-universe

IWM, EFA, EEM, IEF, LQD (other ETFs); S&P 500 index 1962-1993, Nikkei, FTSE, DAX (indexes). Not
applicable to coins (no month-end settlement story), counted as two sets.

## Pass bar

The default in `protocol.md` against the twin for SPY and TLT both, AND the 2014-2025 part alone
(after the paper's sample) must not be behind the twin. Since the rule is in cash two thirds of
the time, bar 5 (beat equal weight) is replaced by: Sharpe above buy-and-hold of the same asset.

## Result

See `results/month-end-liquidity.md` once tested.
