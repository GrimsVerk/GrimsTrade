# opex-pin: idle cash into stocks for the option-expiry week

Field: physics (pinning in a potential well) x control theory (a damper that is removed on a
known date). It is W1, a new mechanism added to wide-1's list by wide-3 (`wide-1.md`, last
section), not one of the original 46.
Written 2026-11-18, run wide-3, before any test or number of this card. Seen before: every
earlier result in `tries.md`, including wide-3's `hedge-regime` and `attention-peak` (both
failed) and `month-end-liquidity` (a calendar rule, dead). No expiry-week return has been
printed by me or, as far as `tries.md` and `ideas.md` show, by any earlier run.

## Claim

Listed options on US stocks and indexes expire on the third Friday of each month. Dealers who
are net long options delta-hedge against moves: they buy dips and sell rallies, which damps the
market and pins it near large strikes into expiry. In the expiry week the hedged, damped market
drifts up (published for single stocks with much option activity; Stivers and Sun 2013 as I
remember). Holding stocks with the cash `tsmom12` leaves idle in that week adds return from a
source that is not the trend.

## Why it might work

Hundreds of dated events (about 380 since 1994), known years ahead, cheap to trade (one ETF
round trip a month at 4 bps), and the weekly harness fits it exactly: the overlay is bought on
the Friday decision before the expiry week and sold on the expiry Friday's decision.

## Why it might not

- The published effect is for single stocks with heavy option activity, sorted against stocks
  without; the index-level effect may be nothing.
- Dealers are not always net long options; when they are short (much of the 2020s' retail call
  buying, as far as I know), hedging amplifies instead of damping.
- The overlay only moves idle cash (about a quarter of the book on average): even a real 20 bps
  a week in the expiry week adds about +0.02 Sharpe. The bar of p < 0.0020 cannot be met by a
  gain that small; the event study is where the mechanism can show.

## Rule (fixed, no fitted parameter)

- Weekly decisions on Friday's close. Base weights are `tsmom12`'s.
- A Friday F is "pre-expiry" if F + 7 days falls on day 15 to 21 of its month (the next Friday
  is the third Friday). On a pre-expiry Friday, the idle cash (1 minus the sum of the base
  weights) is split equally among the set's eligible stock assets and added to their weights.
  Otherwise the twin's weights.
- Stock assets: SPY and QQQ (six); IWM, EFA, EEM and VNQ (other ETFs); all four indexes (`idx`).
  Coins, bonds and gold never receive the overlay.

## Variants (all that will be run)

1. `pin` (only variant): as above.
2. Placebo, logged as `robustness`, never selectable: `pin-after`, the same overlay one week
   later (on the expiry Friday's decision, held through the week after expiry).

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, `pin-after`, and an event study (descriptive, not a
strategy, no `tries.md` row): the expiry week's return minus the average weekly return of the
same period, close of the pre-expiry Friday to close of the expiry Friday, with t, for SPY
1994-2025 by era, and for the S&P 500 index 1962-01 to 1983-02 (before listed index options:
the placebo) and 1983-03 to 1993-01.

## Out-of-universe

The 8 other ETFs (overlay on IWM, EFA, EEM, VNQ) and the four indexes as one portfolio (the US
third-Friday calendar for all four; Nikkei options expire on the second Friday, so its leg is
partly a placebo). Coins: not applicable.

## Pass bar

The default in `protocol.md` for `pin` against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 49 = 0.0020**: every pick out of the list of 46 plus wide-3's three
   new mechanisms counts.
2. Ahead of the twin in at least 4 of 5 eras.
3. Max drawdown not more than 5 points worse than the twin's.
4. Positive, and positive on both applicable out-of-universe sets (other ETFs, indexes).
5. Beats equal weight on Sharpe.
6. (card) `pin` beats its placebo `pin-after` on Sharpe.

Reading of the event study, fixed now: the mechanism is supported only if the expiry-week
excess is positive with t >= 2 on SPY 1994-2025, and the 1962-1983 placebo is smaller than the
1983-1993 value. Either way it is evidence, not a pass.

Held-out year: once, `pin` only, only if all bars pass.

## My guess before any number

Chance it passes: 2%. Difference to the twin: -0.01 to +0.03 Sharpe. Event study on SPY:
+0 to +20 bps a week.

## Result

See `results/opex-pin.md` once tested.
