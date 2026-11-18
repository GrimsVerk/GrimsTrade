# month-end-bonds: hold the bond for the last four sessions of the month

Field: market microstructure / calendar (bond index funds that must buy when their index is
rebuilt at month end). Source: the post-hoc tables of run wide-1 (`results/wide-1-yields.md`);
a paper exists as far as wide-1 remembered (Hartley and Schwarz, "Predictable end-of-month
Treasury returns"), not opened.
Written 2026-11-18 11:08 UTC, lane `month-end-bonds`, before any number of this lane.

## Claim

Bonds earn most of their return in the last four trading sessions of each month. Money that
sits idle in the book could hold the long bond for those four sessions and be cash again after.

## Where the idea came from, and what has already been seen (disclosure)

The pattern was **found by looking**, not predicted. Everything below was seen before this card:

- TLT and IEF, 2003-07-31 to 2025-11-10 (wide-1, step 4): last four sessions +39 bps (TLT) and
  +24 bps (IEF) a month, both halves. This is where the pattern was found. **No test on TLT or
  IEF from 2003-07-31 on can confirm anything**, and none is run here.
- Bond returns built from Treasury yields, 1962 to 2025 (`DGS10`, `DGS30`; wide-1, step 4):
  not confirmed on 1962-2003 pooled; present 1990-2003. The 10-year table's "1990-2003/07" row
  contains the 12 months of TLT's first year as 12 of its 163 months, pooled, never shown alone.
- LQD is **not untouched**, though wide-1 never looked at it alone for this pattern:
  - `month-end-liquidity` (2026-11-12) ran LQD from 2003-07-31 with a seven-session window
    (T-3 .. T+3): Sharpe 0.51 against 0.56 for its twin (-0.05, p 0.58). That window contains
    this card's four sessions plus three more; the four alone were never shown.
  - `rebalance-pressure` (wide-1) used IEF and LQD together as the bond leg of a stock-minus-
    bond spread in sessions T-4 .. T, signed by the month's leader. LQD alone was never shown.
- Never loaded by any test: the first year of TLT and of LQD (2002-07-30 to 2003-07-30). The
  protocol holds an asset only after a year of bars, so every earlier run starts 2003-07-31.

Limits known before running: LQD is a corporate bond fund of about eight years' duration, so most
of its daily move is the same Treasury rate move that TLT and IEF made in the same months. A pass
on LQD 2003-2025 is the pattern showing up in a related fund over the same months. It is not a
test on new time. The only new time is the first year, 12 months, which can contradict the
pattern and cannot confirm it.

## Rule (fixed)

- T = the last trading session of a month (the asset's own trading dates; dates only, known in
  advance).
- Hold the asset at full weight for sessions T-3 .. T: the decision after the close of T-4 buys
  (fill at the open of T-3), the decision after the close of T sells (fill at the open of T+1).
  Cash otherwise. Daily decisions (an exception to the weekly rule; the card needs exact days).
- No eligibility year: the rule needs no history, so it runs from the asset's first bar. This is
  an exception to the protocol's one-year rule, made so that the first year can be tested.
- Train bars only (nothing after 2025-11-10 is loaded, not even dates). **The held-out year is
  not touched: spending it is the owner's call.**

In the paper book the rule would be: money that `tsmom12` leaves in cash goes into TLT for those
four sessions. That book is **not run here**: on the six assets it would be a test on exactly
the data the pattern was found in.

## Costs

The gym's, unchanged: fill at the next open, 2 bps a side in ETFs (4 bps a round trip, 12 round
trips a year), cash earns 0. The event numbers below are open to open with 4 bps taken off each
month.

## Variants (all that will be run: one run each)

1. `last4@LQD`: the rule on LQD alone, from its first bar (2002-07-30) to the end of train.
2. `last4@TLT-y1`: the rule on TLT alone, on its first year only (bars 2002-07-30 to
   2003-07-30).

No other window (three sessions, five sessions, T+1), no other asset. LQD's own first year is
part of run 1 and is also shown alone, as a row of the same run.

## Twin and baselines

Twin `constant`: the same asset held at a constant weight of 0.19 (four sessions in about 21),
the same average risk with no timing. Also shown: buy-and-hold of the asset.

Event numbers (computed from the same bars, the measurement the bar is read on): for each month
end, the return from the open of T-3 to the open of T+1, minus 4 bps of cost, minus four times
the average open-to-open session return of the asset in the period ("net excess"). Mean, t and
number of months; for LQD also by half (to 2013-12, from 2014-01) and for the first year alone.
Reported without a bar: the correlation of LQD's month-end window return with TLT's in the same
months (how much of an LQD result is the same Treasury move).

## Out-of-universe

Not applicable in the usual sense: this card *is* the out-of-sample check of a pattern found on
TLT and IEF. Coins and stocks have no bond index story.

## Pass bar

`last4@LQD` (the only run that can support the pattern), all of:

1. Net excess over all months is positive with t >= 2.0.
2. Net excess is positive in both halves (2002-2013 and 2014-2025).
3. Gym Sharpe above the twin `constant@LQD` with paired bootstrap p < 0.10.
4. Gym Sharpe above buy-and-hold LQD.

`last4@TLT-y1` (12 months, can only fail to contradict): net excess positive. Its t is shown
and means little.

Reading, fixed now:

- LQD passes and TLT's first year is positive: **replicated in a related fund, not contradicted
  on new time.** Still not proof (same months as TLT). The next clean steps are the held-out
  year (owner's call) and forward paper.
- LQD fails bar 1 or 2: **not replicated**; the lane ends, and the held-out year should not be
  spent on it.
- LQD passes bars 1 and 2 but fails 3 or 4: the effect is there and too small to trade alone at
  our costs; say so.

Held-out year: not run in this lane, whatever the result.

## Result

See `results/month-end-bonds.md` once tested.
