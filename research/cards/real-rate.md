# real-rate: Real rates: step aside while the real policy rate rises fast

Written 2026-11-13 02:00 UTC, run macro-1, before any test of this rule and before any macro
feature was plotted or printed. Seen before: every result of runs 1-3 (price data only), the
review (the `tsmom12` lead is 2000-2002), and public history of the cycle named below.

Field: macro / monetary policy (owner idea; real rates as the price of money, e.g. Erb & Harvey
2013 on gold, Neely 2015).

## Claim

What bites is the real rate: the fed funds rate minus inflation. Risk assets held only while the
real policy rate is not rising fast beat the plain trend rule.

## Why it might work

A rising real rate tightens conditions even when the nominal rate is flat (inflation falling),
and it is what makes cash and bonds compete with risky assets.

## Why it might not

Inflation is known late (CPI for a month comes out mid-next-month, and is revised). The real
rate rose fastest in 1980-82 and 2022-23; inside our train window that is about four episodes.

## Rule (fixed)

Real policy rate = 30-day mean of `DFF` minus CPI inflation over 12 months (`CPIAUCSL`, the
vintage published by then). Hostile when it is more than 1.0 point above its level 365 days
earlier.

## Variants (all that will be run)

1. `real-and` (primary). 2. `real-alone`.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, and 2003-2025 next to 1994-2025.

## Pass bar

The default in `protocol.md`, plus card bar 6 ("Macro tests": not behind `tsmom12` on Sharpe
over 2003-2025). The `-alone` variant is reported, not judged: it tells whether the phase carries
information without the trend rule.

## Result

See `results/real-rate.md` once tested.
