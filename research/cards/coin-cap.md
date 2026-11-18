# coin-cap: cap the combined coin weight inside tsmom12

Field: allocation. Written 2026-11-18 11:14 UTC, lane `coin-cap`, burst 1. Before any number of
this rule. Seen before (other lanes, train only): deep-1 found 8 of `tsmom12`'s 10 worst
drawdowns are coin tops; cointop-1 Part C found `stop-0.25` cuts the worst loss from 36.5% to
28.9% at 1-2 points less growth a year and read it as "a smaller coin position, not a better
rule"; `crypto-slot-size` (run 3) found the size of the coin slots matters more than timing.

## Claim

A plain cap on the combined coin weight inside `tsmom12` cuts the worst loss as much as
cointop-1's `stop-0.25`, and costs less growth.

## Why it might work

With six assets each coin has a 1/6 slot, so the coins are up to 1/3 of the book (1/5 while BTC
is the only coin) at 60-90% volatility. A cap removes that weight directly, with no extra
trades and no parameter fitted to coin tops.

## Why it might not

Bitcoin rose about a thousandfold in the sample: holding less of it costs return every year, a
stop only costs it after a fall. A cap does nothing about the timing of the loss. And this is a
choice of risk: the test can describe it, not validate it.

## Rule (fixed)

- Start from the weekly (Friday) `tsmom12` weights: equal slots over eligible assets, a slot held
  if its 365-day log return is above zero, else cash.
- Let `w` be the summed weight of the held coins (BTC, ETH). If `w > C`, scale every coin weight
  by `C / w`. The excess `w - C` goes:
  - `cash`: to cash;
  - `rest`: to the held non-coin slots, pro rata to their weights (cash if none is held).
- No leverage: weights sum to at most 1 by construction. No new data, no fitted parameter.

## Grid (all that will be run)

`C` in {10%, 15%, 20%, 25%} x {`cash`, `rest`} = 8 variants, named `cap10-cash` ... `cap25-rest`.
Six live assets, gym costs, full train (decisions 1994-02-01 .. 2025-11-09). Held-out year
untouched whatever the result.

## Selection (walk-forward, train years only)

For each calendar year Y from 2016 (three years of coin history) to 2025, pick the variant with
the highest ratio of annualised log growth to worst loss over all train days before Y-01-01
(ties: the smaller cap, then `cash`). The walk-forward series `cap-wf` is the stitch of each
year's pick's daily gym returns; before 2016 it is `cap15-cash` (the middle-low cell, fixed
here). Limit, stated now: the stitch leaves out the one switch trade at a year boundary (at most
15% of the book once a year, a few basis points).

## Twins and baselines

`tsmom12` (weekly, the twin) and cointop-1's `stop-0.25` rerun unlogged in the same script, both
through the gym on the same days. Equal weight for reference.

## Bar (for `cap-wf`; every fixed cell is reported the same way)

1. Worst loss no larger than `stop-0.25`'s (28.9% in cointop-1; the rerun number is used).
2. Growth cost smaller than `stop-0.25`'s: CAGR above `stop-0.25`'s CAGR.
3. Sharpe at least `tsmom12`'s and at least `stop-0.25`'s (point estimates; the paired
   block-bootstrap p-values are reported, not required).
4. Same reading at double costs (bars 1 and 2 hold against the 2x-cost twins).

All four hold: "a plain cap does the stop's job cheaper". Bar 1 holds and 2 fails: "the cap is
the same trade as the stop". Bar 1 fails: "the stop does something a cap of these sizes does
not". Nine series are looked at (8 cells + the stitch); with that many, a pass by a hair on
one cell is not a finding, the pattern across the grid is.

## Look-ahead

The cap is a function of the same-day `tsmom12` weights only. Checked two ways before any number:
`harness.check_against_gym` on the capped rule, and a unit test that the cap never raises a coin
weight, never exceeds `C` or a book of 1, and equals `tsmom12` when `C` = 1.

## Result

See `results/coin-cap.md` and `research/coin-cap.md` once run.
