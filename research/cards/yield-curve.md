# yield-curve: Yield curve: step aside for a year after the curve inverts

Written 2026-11-13 02:00 UTC, run macro-1, before any test of this rule and before any macro
feature was plotted or printed. Seen before: every result of runs 1-3 (price data only), the
review (the `tsmom12` lead is 2000-2002), and public history of the cycle named below.

Field: macro / term structure (Estrella & Mishkin 1998; Harvey 1988; the 10y-2y inversion before
every US recession since the 1970s).

## Claim

An inverted curve (10-year yield below 2-year) foretells a recession within about two years.
Risk assets held only while the curve has not been inverted in the last 365 days beat the plain
trend rule.

## Why it might work

It is the best-known recession signal; recessions bring the large falls the trend rule is late
for.

## Why it might not

The lead time is long and varies (6 to 24 months); markets often rise after an inversion (1998,
2006, 2019, 2023). Inversions since 1994: about four (1998 briefly, 2000, 2006-07, 2019,
2022-24). The trend rule may already catch the falls that follow.

## Rule (fixed)

Hostile when `T10Y2Y` was below 0 on any day of the last 365 days (the inversion and the year
after it, when the curve re-steepens).

## Variants (all that will be run)

1. `curve-and` (primary). 2. `curve-alone`.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, and 2003-2025 next to 1994-2025.

## Pass bar

The default in `protocol.md`, plus card bar 6 ("Macro tests": not behind `tsmom12` on Sharpe
over 2003-2025). The `-alone` variant is reported, not judged: it tells whether the phase carries
information without the trend rule.

## Result

See `results/yield-curve.md` once tested.
