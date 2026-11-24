# trend-age: hold a trend only once it has survived four weeks

Field: queueing / reliability theory (renewal process, hazard rate). It is mechanism Q5 of
`wide-1.md` step 1 ("the chance a trend ends depends on its age"), which wide-1 killed without a
test as "changes *when* the trend rule acts, not where the edge comes from".
Written 2026-11-18 11:14 UTC, run wide-2, before any test or number of this run. Seen before
writing: `wide-1.md`, `protocol.md`, `tries.md` and `ideas.md` (searched for age, hazard,
renewal, duration: no earlier test).

## Why this one of the 42 uncarded mechanisms

- Most of the 42 are a tested idea in other words, need data we do not have (page views, exit
  queues, unlock schedules, volume), or are "step out when X" gates with 4-7 episodes.
- Q5 needs only the six assets' weekly closes and the existing harness: one function, one run.
- It has hundreds of dated events (every start of an on-spell of the `tsmom12` signal, per
  asset), not a handful of bear markets.
- The kill reason was an argument, not a number. No try in `tries.md` conditions on the age of
  the signal.

## Claim

On-spells of the 12-month trend signal have a falling hazard rate: a spell that has just begun
is much more likely to end next week than one that has lasted a month (the 365-day return sits
near zero right after a flip, so noise flips it back). Those short spells are the whipsaws: buy
at the next open, sell a week or two later, pay costs twice (60 bps a round trip in coins).
Waiting until the signal has survived a few weeks skips them.

## Why it might not

The first weeks of a real new trend are given up too, and they may be the best ones. A
confirmation delay is also a slightly slower trend rule, and every smoother or slower trend rule
tested so far tied `tsmom12`. Exits are not delayed, so the rule holds strictly less than its
twin; with cash at 0 that costs return.

## Rule (fixed, no fitted parameter)

- Weekly decisions on Friday's close, equal slots among eligible assets, as `tsmom12`.
- An asset's slot is held only if its `tsmom12` signal (365-day return > 0) is true at this
  Friday's close **and** was true at each of the three previous Fridays' closes (dates
  Friday-7, -14, -21, each computed from bars visible on that date only). Else the slot is cash.
- So entry is three weeks later than the twin's; exit is the same week as the twin's.

## Variants (all that will be run)

1. `age4` (only variant): as above. Four weeks is fixed here and not varied.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight. Reported next to the backtest (descriptive, from the
twin's decisions on the six assets, train period): the number of on-spells per asset, how many
ended within 4 weeks, and the weekly hazard (share of spells alive at age a that end at age a)
for ages 1-4 against ages 5+.

## Out-of-universe

All three sets apply (the rule acts on one asset at a time): the 8 other ETFs and the 6 other
coins as equal-slot books, and the four indexes each alone (S&P 500 index cut at 1993-01-28).
The index set's sign is the sign of the mean of the four Sharpe differences.

## Pass bar

The default in `protocol.md` for `age4` against `tsmom12`, with one line made stricter:

1. (stricter) **p < 0.10 / 42 = 0.0024** instead of p < 0.10. This card was picked as the most
   promising of 42 uncarded mechanisms, so the bar is Bonferroni-corrected for that choice.
   With 2,000 bootstrap draws this means at most 4 draws in which the twin is ahead.
2. to 5. as in the protocol.

Held-out year: once, `age4` only, only if all bars pass.

## My guess before any number

Chance it passes: 3%. Expected difference to the twin: between -0.05 and +0.03 Sharpe. I expect
the hazard to be clearly higher in weeks 1-4 than later (that part is close to arithmetic), and
the skipped whipsaws to be paid for by the late entries.

## Result

See `results/trend-age.md` once tested.
