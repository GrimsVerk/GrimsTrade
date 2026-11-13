# fed-hiking: Fed policy: step aside while the Fed is hiking

Written 2026-11-13 02:00 UTC, run macro-1, before any test of this rule and before any macro
feature was plotted or printed. Seen before: every result of runs 1-3 (price data only), the
review (the `tsmom12` lead is 2000-2002), and public history of the cycle named below.

Field: macro / monetary policy (owner idea 2026-11-12; Jensen, Mercer, Johnson 1996 "Business
conditions, monetary policy and expected security returns"; Thorbecke 1997).

## Claim

Cheap money lifts asset prices; tightening hurts them. Risk assets held only while the Fed is not
in a hiking phase beat the plain trend rule.

## Why it might work

Rate rises raise discount rates and funding costs; 1994, 2000, 2022 were hiking years with weak
or falling risk assets.

## Why it might not

The trend rule already leaves falling markets. Hikes come in strong economies (2004-06, 2017-18
were good years for stocks), and the worst falls (2001, 2008) came while the Fed was cutting.
About six hiking phases since 1994: very few independent tests.

## Rule (fixed)

Fed funds rate = 30-day mean of the daily effective rate (`DFF`). Hostile when it is more than
0.25 points above its level 182 days earlier.

## Variants (all that will be run)

1. `hike-and` (primary). 2. `hike-alone`.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, and 2003-2025 next to 1994-2025.

## Pass bar

The default in `protocol.md`, plus card bar 6 ("Macro tests": not behind `tsmom12` on Sharpe
over 2003-2025). The `-alone` variant is reported, not judged: it tells whether the phase carries
information without the trend rule.

## Result

See `results/fed-hiking.md` once tested.
