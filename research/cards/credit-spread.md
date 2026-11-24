# credit-spread: Credit spreads: step aside when corporate spreads widen

Written 2026-11-13 02:00 UTC, run macro-1, before any test of this rule and before any macro
feature was plotted or printed. Seen before: every result of runs 1-3 (price data only), the
review (the `tsmom12` lead is 2000-2002), and public history of the cycle named below.

Field: macro / credit (Gilchrist & Zakrajšek 2012 "Credit spreads and business cycle
fluctuations"; the backlog's "risk-off warning").

## Claim

Credit markets see trouble before stock markets. Risk assets held only while the Baa corporate
spread is not widening beat the plain trend rule.

## Why it might work

Spreads widened from mid-2007, a quarter before stocks peaked; the excess bond premium predicts
recessions and stock returns in the literature.

## Why it might not

Spreads and stock prices move together day to day, so the warning may be no earlier than the
price trend. Large widenings since 1994: 1998, 2000-02, 2007-09, 2011, 2015-16, 2020, 2022: about
seven, more than any other gate here, but still few.

## Rule (fixed)

Spread = 20-day mean of `BAA10Y` (Moody's Baa yield minus the 10-year Treasury). Hostile when it
is more than 0.5 points above its lowest value of the last 365 days.

## Variants (all that will be run)

1. `spread-and` (primary). 2. `spread-alone`.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, and 2003-2025 next to 1994-2025.

## Pass bar

The default in `protocol.md`, plus card bar 6 ("Macro tests": not behind `tsmom12` on Sharpe
over 2003-2025). The `-alone` variant is reported, not judged: it tells whether the phase carries
information without the trend rule.

## Result

See `results/credit-spread.md` once tested.
