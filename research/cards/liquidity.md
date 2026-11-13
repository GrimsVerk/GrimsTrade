# liquidity: Money supply and the Fed balance sheet: step aside when liquidity shrinks

Written 2026-11-13 02:00 UTC, run macro-1, before any test of this rule and before any macro
feature was plotted or printed. Seen before: every result of runs 1-3 (price data only), the
review (the `tsmom12` lead is 2000-2002), and public history of the cycle named below.

Field: macro / liquidity (owner idea: "money printing"; Howell 2020 "Capital Wars"; the common
claim that Bitcoin follows global M2).

## Claim

Asset prices follow the amount of money. Risk assets held only while real money growth is
positive (M2 growth above inflation) beat the plain trend rule. Second form: only while the Fed's
balance sheet is not shrinking (no quantitative tightening).

## Why it might work

Money growth below inflation means real money is shrinking; QT drains reserves. 2022 had both.

## Why it might not

M2 is published about four weeks late and revised. Real M2 went negative only a few times since
1994 (mid-1990s, 2005-07, 2022-23); the balance sheet shrank twice (2018-19, 2022-25), both with
strong markets for most of the time. Very few episodes.

## Rule (fixed)

- `m2-and` (primary): hostile when M2 growth over 12 months minus CPI inflation over 12 months
  (both `M2SL` and `CPIAUCSL` vintages published by then) is below 0.
- `walcl-and`: hostile when the Fed balance sheet (`WALCL`) is smaller than 52 weeks earlier.
  Data from 2003 (vintages from 2011; earlier values count as public a week late).

## Variants (all that will be run)

1. `m2-and` (primary). 2. `m2-alone`. 3. `walcl-and`.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, and 2003-2025 next to 1994-2025.

## Pass bar

The default in `protocol.md`, plus card bar 6 ("Macro tests": not behind `tsmom12` on Sharpe
over 2003-2025). The `-alone` variant is reported, not judged: it tells whether the phase carries
information without the trend rule.

## Result

See `results/liquidity.md` once tested.
