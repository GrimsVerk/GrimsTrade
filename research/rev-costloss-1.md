# rev-costloss-1: the `tsmom12` exit scored as a crash warning

Lane rev-costloss-1, 2026-11-25 (night, UTC). Branch `rev-costloss-1`, PR #182. Research only:
fake money, files already in the data cache, no change to the gym, the daily runner or the live
strategies. A descriptive re-score of a logged configuration (`tsmom12`) with insure-1's and
gap-2002-1's loaders: no new rule, nothing selected. Train data only: no session after
2025-10-31 is used. Card: [`cards/rev-costloss-1.md`](cards/rev-costloss-1.md) (pushed before
any number). Tables: [`results/rev-costloss-1.md`](results/rev-costloss-1.md). Code:
`lib/revcostloss1.py`, tests `tests/test_revcostloss1.py`.

## Question

Read the exit the way meteorology scores a warning (the static cost-loss model; Murphy 1977,
Richardson 2000): every Friday the rule either warns (it is out for the next week) or not; the
event is a fall of at least 10% below that Friday's close within 13 weeks. For which cost/loss
ratios C/L is that warning worth having, and does the answer match the calm drag against crash
gain that insure-2 and gap-2002-1 measured in money?

## The answer on one screen

**The exit is a real but narrow warning. On the US market since 1927 it has clear skill (hit
rate 0.49, false-alarm rate 0.21, Peirce score 0.28, against -0.01 for the same warnings at
random dates, p 0.000), but it beats climatology only for users whose cost/loss ratio is
between about 0.10 and 0.29. A plain holder's own ratio, read off the weekly returns, is 0.27:
inside the band but at its top edge, where the warning's value is +0.06 of a perfect
forecast's, and in money -0.01. So yes, it matches: in warning terms too the exit is
worth about nothing to a holder, because what it gains in falls it pays in false alarms, and
the largest single block of those false alarms is the rebound after the low.**

| Set (10% fall within 13 weeks) | Base rate | Out | H | F | Peirce H - F | Random dates, median (95%) | V > 0 for C/L | Holder's C/L | V at holder's C/L | Money V |
|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|
| US market 1927-2025 | 0.15 | 0.25 | 0.49 | 0.21 | **+0.28** | -0.01 (+0.13) | 0.105-0.290 | 0.27 | +0.06 | -0.01 |
| US market 1927-1961 | 0.17 | 0.29 | 0.57 | 0.23 | +0.34 | -0.02 (+0.16) | 0.110-0.340 | 0.28 | +0.15 | +0.14 |
| US market 1962-2001 | 0.12 | 0.23 | 0.43 | 0.21 | +0.23 | -0.02 (+0.15) | 0.090-0.220 | 0.26 | -0.10 | -0.14 |
| US market 2002-2025 | 0.16 | 0.21 | 0.43 | 0.17 | +0.25 | -0.03 (+0.24) | 0.115-0.310 | 0.27 | +0.08 | -0.11 |
| 11 French series, pooled | 0.17 | 0.27 | 0.45 | 0.23 | +0.23 | +0.00 (+0.09) | 0.130-0.295 | 0.29 | +0.01 | -0.04 |
| SPY / QQQ | 0.14 / 0.24 | 0.19 / 0.22 | 0.47 / 0.43 | 0.15 / 0.15 | +0.32 / +0.28 | p 0.000 / 0.007 | 0.095-0.350 / 0.180-0.470 | 0.26 / 0.32 | +0.17 / +0.20 | -0.05 / +0.05 |
| GLD / TLT | 0.11 / 0.09 | 0.31 / 0.35 | 0.31 / 0.41 | 0.31 / 0.35 | -0.00 / +0.06 | p 0.42 / 0.24 | none / 0.085-0.105 | 0.23 / 0.15 | -0.43 / -0.22 | -0.28 / -0.22 |
| BTC / ETH | 0.54 / 0.65 | 0.25 / 0.38 | 0.23 / 0.37 | 0.26 / 0.40 | -0.04 / -0.03 | p 0.57 / 0.53 | none | 0.78 / 0.79 | -0.57 / -0.45 | -0.04 / -0.02 |
| Six, pooled | 0.23 | 0.27 | 0.36 | 0.24 | +0.12 | -0.01 (+0.05) | 0.200-0.305 | 0.39 | -0.16 | -0.04 |

(V: relative economic value, 1 = a perfect warning, 0 = climatology, i.e. always or never
protecting, whichever is cheaper. Money V: (rule - hold) / (perfect - hold) in weekly log
returns, cash 0, where "perfect" is out exactly in event weeks. Holder's C/L: C = mean weekly
return in weeks with no event, L = C minus the mean in event weeks.)

- **Skill: yes, on stocks; none on gold, bonds and coins.** On every US stock set and era the
  Peirce score is 0.13-0.34 and above all random-date shifts' 95th percentile (p 0.000-0.015).
  That is the warning form of insure-1's "0.50 of each fall against 0.27 at random dates". On
  GLD, TLT, BTC and ETH the score is about 0 (p 0.24-0.57): as a 10% (or 20%, coins) crash
  warning the exit is no better than its own warnings at random dates. Pooled, the six reach
  only +0.12, carried by SPY and QQQ.
- **Value: a narrow band around the base rate.** V peaks at C/L = base rate (where V = Peirce)
  and turns negative fast on both sides: on the US market V > 0 only for C/L 0.105-0.290; at
  0.05 V is -0.90 (cheap protection: always protect, because the exit misses half the falls),
  at 0.50 V is -0.70 (dear protection: never protect, because about 7 in 10 warnings are false). The
  card's expectation ("V > 0 from a few percent up to about 0.5") was too wide.
- **For a holder it is worth about nothing, in both framings.** The holder's own ratio (0.26-0.32
  on US stocks: 0.26-0.30 on the French sets and eras, SPY 0.26, QQQ 0.32) falls inside the
  band, near its top: V +0.06 (market), +0.01 (11 series). The
  money version, which weights each week by its actual return, is -0.01 and -0.04. Both say
  what gap-2002-1 measured: the fall gain about cancels the rebound lag plus the calm drag.
  By era the two agree in sign before 2002 (1927-61 +0.15 / +0.14, 1962-2001 -0.10 / -0.14);
  since 2002 the binary score is slightly positive (+0.08) while money is -0.11: the
  binary table counts every missed or caught 10% fall the same, while money also charges the
  size of the rebound missed after the low. SPY and QQQ show the same: V at the holder's ratio
  +0.17 and +0.20, money V -0.05 and +0.05 (the card's "binary score flatters" reading).
- **Bigger falls are forecast better, but the holder's ratio leaves the band.** For a 20% fall
  within 13 weeks the US market's Peirce score rises to 0.37 (hit rate 0.60), but the band
  shrinks to C/L 0.025-0.105 while a holder's ratio for that event is 0.15: V there -0.29, money
  -0.02. Against rarer, larger falls the exit is a better forecast, but a holder pays its cost
  in every week out, so the rarer the event, the less a weekly warning is worth to him.
- **Where the false alarms sit: rebounds first.** On the US market 43% of false-alarm weeks are
  in the year after a 25% low (51% since 2002), 29% in calm markets, 28% inside the falls
  themselves (weeks out with no further 10% drop to come). The rule is out in 68% of fall weeks,
  58% of rebound weeks and 8% of calm weeks. The rebound share is the warning form of
  insure-2's "handed back in the rebound"; the calm share is the calm drag. Misses: 49% in calm
  markets (10% drops without a 25% fall), 44% inside 25% falls.
- **Fast falls are the blind spot, as known.** Hit rate on event weeks inside US market falls
  of 92 days or less 0.35 (only 26 event weeks, overlapping
  Fridays from about 2-3 independent episodes such as 1987 and 2020), 93-365 days 0.61, over a
  year 0.71; outside any 25% fall 0.21. Pooled over the 11 series 0.47 / 0.55 / 0.69 / 0.21;
  the four ETFs 0.46 / 0.58 / 0.72 / 0.13.
- **The whole event grid** (5/10/20% within 4/13/26 weeks, results file) gives the same picture
  for the US sets: Peirce 0.12-0.37, above random dates in every cell (p <= 0.023), V at the
  holder's ratio between -1.03 and +0.14 and money V between -0.16 and -0.00. Nowhere is the warning
  worth much to a holder in money.

## What this changes

Nothing for the live rule, and no new claim: it restates insure-1/insure-2/gap-2002-1 in a
second language. The useful sentence for SUMMARY's insurance bullets: as a crash warning the
exit has real skill on stocks (none on gold, bonds or coins), but it pays only for someone
whose protection costs between about a tenth and a third of the loss it prevents; a plain
holder sits at the top edge of that band, where it is worth about nothing (V +0.06; in money
-0.01). Whether to hold the insurance stays a drawdown preference (`owner-decisions.md`: `tsmom12` is a risk
choice, not an edge).

## How sure, and what was chosen

- Card pushed before any number (commit cc5a8ae, 2026-11-25 00:19 UTC; the card's own header says 00:30, written ahead). Two runs, both after the card push; the first had a bug in one
  row (the pooled ETF set: "Four ETFs, pooled" took BTC, ETH, SPY and QQQ instead of SPY, QQQ,
  GLD and TLT); fixed before the results commit, no other row changed. A lint-only refactor afterwards reproduced the file byte for byte.
- Defaults not fixed by the card: for the six, the random-date shift uses one common fraction
  of each series' length (the series have different lengths); event closes on the six are the
  dividend-adjusted closes (the project's total-return convention). The fall-speed and part
  labels use insure-1's 25% / 25% zigzag on each series' own index.
- Weekly forecasts overlap (a 13-week window covers 13 Fridays), so counts overstate the
  information; the random-date shifts keep that overlap and are the fair null. Fast-fall
  counts on the US market are thin (26 event weeks).
- The static cost-loss model fixes L per event and ignores how much more than X the fall
  turns out to be; the money V covers that part. Neither is a strategy test.
- Bar for scale only (BAR.md): N 504, z >= 4.70, Bonferroni p <= 9.9e-05 for a new pick. Not
  applicable: nothing picked; 1,000 rotations cannot reach it. One `tries.md` row of kind
  `note`; nothing for `ledger/tries.jsonl` (no strategy try).
