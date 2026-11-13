# halving: Bitcoin's four-year cycle: step out of coins in the bear year after a halving

Written 2026-11-13 02:00 UTC, run macro-1, before any test of this rule and before any macro
feature was plotted or printed. Seen before: every result of runs 1-3 (price data only), the
review (the `tsmom12` lead is 2000-2002), and public history of the cycle named below.

Field: crypto cycles (owner idea; the "four-year cycle" folklore). Treated with deep suspicion,
as `docs/BACKLOG.md` asks.

## Claim

Bitcoin peaks 12 to 18 months after each halving and falls for about a year after that. Coins
held except from day 548 to day 912 after the last halving (months 18 to 30) beat the plain
trend rule on coins.

## Why it might work

Halvings cut new supply in half on a fixed schedule; if buyers are slow to price it, the cycle
repeats. Peaks: 2013-12, 2017-12, 2021-11, 2025-10.

## Why it might not

The window comes from the folklore, and the folklore was written by people who had seen exactly
these cycles. Inside train the test is in-sample by construction: three bear windows (2014,
2018, 2022), three independent episodes, none unseen. Only the fourth cycle (window from
2025-10-19, almost all in the held-out year) was not in the folklore's data, and it will be
looked at only if the rule passes train. Months 18-30 missed the 2014 winter's start (the peak
was 12 months after the 2012 halving).

## Rule (fixed)

Applies to coins only (BTC, ETH; other coins in the coin set). Hostile when 548 <= days since the
last halving < 913. Halvings 2012-11-28, 2016-07-09, 2020-05-11, 2024-04-19 (block-height
schedule, known years ahead). ETFs keep their plain `tsmom12` slot.

## Variants (all that will be run)

1. `halving-and` (primary). 2. `halving-alone` (coins held except in the window, no trend test).

## Out-of-universe

Coin set only (other coins share Bitcoin's cycle, so this is not an independent check; bar 4 is
read on that one set and counts for little).

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, and 2003-2025 next to 1994-2025.

## Pass bar

The default in `protocol.md`, plus card bar 6 ("Macro tests": not behind `tsmom12` on Sharpe
over 2003-2025). The `-alone` variant is reported, not judged: it tells whether the phase carries
information without the trend rule.

## Result

See `results/halving.md` once tested.
