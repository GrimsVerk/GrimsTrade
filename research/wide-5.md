# Wide 5: dealer backlog and index extension, two structural flows in Treasuries

Research run wide-5, 2026-11-18. Branch `wide-5` (from `wide-4`), draft PR #71. Research only:
fake money, public data, no change to the gym, the daily runner or the live strategies.

## In plain words (results, 2026-11-18)

**Both new ideas fail against the 12-month trend rule (`tsmom12`, Sharpe 1.05). The held-out
year was not looked at.** Neither leaves a dose-response trace that would support its
mechanism.

| Idea (field) | In one line | Sharpe vs 1.05 | Why |
|---|---|---:|---|
| `dealer-backlog` (queueing, new W9) | Idle cash into TLT for five sessions after a 20/30-year auction in which primary dealers were left with more than their usual share | 1.02 (-0.026, p 0.95) | Long bonds did *worse* after auctions dealers had to absorb (-13 bps against +6 after the others; slope t -1.0): no paid-for recovery, if anything a small overhang |
| `extension-dose` (control theory, new W10) | Idle cash into TLT for the last four sessions only in months whose index extension is above its two-year median | 1.06 (+0.013, p 0.19) | High-extension months +32 bps against +17 for the rest, but the slope on the dose has t 0.8, the gap is all before 2014 (+46 against -3 since), and the whole book gain is the 2008-09 crisis |

Count: **56 mechanisms (46 listed + W1-W10), 14 tested, none passed. The next test is read at
p < 0.10 / 56 = 0.00179** (or 0.10 / (56 + k) if k new mechanisms are added first).

## Step 1. Two new mechanisms and a written choice rule

The W entries left on the list (W3 `lunar`, W5-W8) all carry priors of 1-2%. Two new ones were
invented first, by crossing queueing theory and control theory with the dose-response method
wide-4 used, and added to `wide-1.md` (last section) with a mechanism story, a test plan and a
prior. Then a six-point choice rule was written (structural cause, unseen cut, dose, power,
post-sample years, not a killed idea), scored for all seven untested W entries and pushed in
674430a before any number:

| # | Field x tool | Score of 6 |
|---|---|---:|
| W9 `dealer-backlog` | queueing x a server of last resort with a measured backlog (Grossman-Miller) | 5 |
| W10 `extension-dose` | control theory x feedforward of a known setpoint step (index extension) | 5 |
| W3 `lunar`, W5 `tidal-trigger`, W6 `payday-inflow` | | 4 |
| W8 `snapshot-shrink` | | 3 |
| W7 `fatigue-damage` | | 2 |

The ann-1 lesson (published calendar effects died after publication) is in the rule as
criterion 5 *or* 1: neither pick can be judged on years after its idea was formed (both were
formed today), so both had to qualify through a structural cause (the primary dealers'
obligation to bid; the index's monthly rebuild rule). W3 `lunar` is the only entry with
post-sample years, and its cause is mood.

Cards: `cards/dealer-backlog.md`, `cards/extension-dose.md` (42e9262). Code, tests and the
auction parser (8ef9d4f) before the logged runs.

## Step 2. The tests (train only, one logged run each, 2026-11-18 22:12 UTC)

### W9 `dealer-backlog`

**It fails, and the mechanism's sign is wrong.** Table: `results/dealer-backlog.md`; 3 rows in
`tries.md` (1 variant, 2 robustness: placebo `backlog-neg`, other ETFs into IEF).

| | `backlog` | `backlog-neg` (placebo) | `tsmom12` |
|---|---:|---:|---:|
| Sharpe, six assets | 1.02 | 1.03 | 1.05 |
| Difference to the twin (p) | -0.026 (0.95) | -0.02 (0.84) | |
| Eras 2000-09 / 2010-16 / 2017-21 / 2022-25 | 0.19 / 1.54 / 1.52 / 0.62 | | 0.19 / 1.55 / 1.50 / 0.88 |
| Turnover a year | 6.1 | 8.6 | 2.7 |
| Other ETFs (into IEF after 10-year auctions) | -0.008 (p 0.59) | | |

Event study, TLT at our fills (open of A+1 to open of A+6), minus an average 5-session return,
264 long auctions since 2008-07; u = dealer share minus its 12-auction median (sd 7.2 points):

| Period | u > 0 | u <= 0 | Slope per point of u (t) |
|---|---:|---:|---:|
| 2008-07 to 2025 | -13 bps (t -0.7), 108 | +6 (0.4), 156 | -1.4 (-1.0) |
| 2008-07 to 2016 | -1 (0.0) | +41 (1.6) | -1.8 (-0.5) |
| 2017 to 2025 | -20 (-0.8) | -12 (-0.8) | -0.8 (-0.7) |

Card's reading (a) slope > 0 with t >= 2, (b) u > 0 above u <= 0, (c) positive in both halves:
**no on all three.** IEF on 10-year auctions has a flat slope at fills (+0.1, t 0.1) and a
weakly positive one at closes (+0.9, t 1.2): also nothing.

What it shows: the Grossman-Miller story (dealers are paid for absorbing an auction by a
recovery) has no trace at our fills when auctions are sorted by how much dealers took. The
point estimates lean to the opposite story, an overhang (a weak auction is news about demand
that is not reversed within a week), at t -1. Neither is tradable here.

**Compared with my guess** (card): 2%, -0.01 to +0.02, TLT after u > 0 -10 to +25 bps, slope
t -1 to +2. It came out at -0.026 (below the range), -13 bps, slope t -1.0 (at the edge).

### W10 `extension-dose`

**It fails the pass bar (p 0.19 against 0.00179; 2 of 4 eras), though it beat its placebo by
a hair.** Table: `results/extension-dose.md`; 3 rows in `tries.md` (1 variant, 2 robustness:
placebo `ext-low`, other ETFs into IEF by the 7-10 year bucket).

| | `ext-high` | `ext-low` (placebo) | `tsmom12` |
|---|---:|---:|---:|
| Sharpe, six assets | 1.06 | 1.05 | 1.05 |
| Difference to the twin (p) | +0.013 (0.19) | +0.01 (0.34) | |
| Eras 2000-09 / 2010-16 / 2017-21 / 2022-25 | 0.25 / 1.57 / 1.49 / 0.86 | 0.16 / 1.55 / 1.50 / 1.00 | 0.19 / 1.55 / 1.50 / 0.88 |
| Turnover a year | 6.0 | 6.0 | 2.7 |
| Other ETFs (into IEF) | +0.020 (p 0.21) | | |

Event study, TLT open of T-3 to open of T+1, minus an average 4-session return, 279 month ends;
E(m) = extension of a 20+ year bucket built from the auction file (median +0.04 years, sd 0.14):

| Period | High months | Low months | Slope per year of E (t) |
|---|---:|---:|---:|
| 2002-07 to 2025 | +32 bps (t 2.2), 113 | +17 (1.4), 166 | +65 (0.8) |
| 2002-07 to 2013 | +56 (1.8), 37 | +12 (0.8), 100 | +70 (0.8) |
| 2014 to 2025 | +20 (1.3), 76 | +23 (1.2), 66 | +9 (0.0) |

Card's reading: (a) slope t >= 2 **no** (0.8), (b) high above low yes, (c) positive in both
halves yes (the second at t 0.0). **Not supported.** IEF against the 7-10 bucket goes the
other way: high months +12.5 bps, low months +17.9.

The book's +0.013 is lifted by the month-end mean found by looking (card); the comparison that
mattered, `ext-high` against `ext-low`, is 1.061 against 1.054.

**Compared with my guess** (card): 2%, 0 to +0.02 against the twin, -0.01 to +0.01 against the
placebo, slope t -1 to +2. It came out inside every range: +0.013, +0.007, t 0.8.


## Step 3. Where does the better of the two gain or lose against `tsmom12`? (fixed before looking)

Written 2026-11-18 after both verdicts, before any breakdown below was computed. The better
pick by its difference to the twin is `extension-dose` (`ext-high` +0.013, p 0.19; `backlog`
-0.026). Nothing is tuned: the same rule, placebo and twin as on the card, rerun without
`tries.md` rows (the configurations are already logged). Script `lib/wide5_deeper.py`.

Questions:

1. **By year** (2003-2025, TLT's full years): the return of `ext-high` minus that of
   `tsmom12`, and of `ext-low` minus `tsmom12`, in percentage points.
2. **Inside the windows or not**: the same yearly difference split into the days on which
   `ext-high` holds the extra TLT weight and all other days (outside the windows the two
   should only differ by trading costs).
3. **By regime**: TLT's excess over the last four sessions (the card's event-study number) in
   high minus low months, split by (a) bond bull and bear years (TLT's calendar-year return
   above or below zero), (b) 2003-2013 against 2014-2025, (c) months whose `tsmom12` book had
   at least a quarter idle against less (where the overlay is large or small).

Reading, fixed now: the gain is **consistent with the mechanism** only if the high-minus-low
excess is positive in both bull and bear bond years (index buying is a flow, not a bet on
direction) and not smaller after 2014 than before (passive bond assets grew several-fold).
If it lives only in bull years, it is TLT's drift; if only before 2014, it has faded or was
luck.

### Step 3, what came out (`results/wide-5-deeper.md`, script `lib/wide5_deeper.py`)

**The gain is the 2008-09 crisis, and the dose split has vanished since 2014: not consistent
with the mechanism by the reading fixed above.**

1. **By year**, summing the daily differences: `ext-high` gains +7.9 points over 2003-2025 on
   the days it holds the extra TLT; +8.1 of them come from 2008 (+5.4) and 2009 (+2.7). Over
   the other 21 years it nets about -0.3 points (best 2014 +1.9, 2019 +1.8; worst 2017 -4.1,
   2022 -2.9). Outside the windows the two books differ by a few hundredths a year (costs),
   as they should.
2. **Why 2008**: the trend rule was out of stocks and crypto, so idle cash was large, and the
   high-extension month ends of late 2008 coincided with TLT's crisis rally (TLT +34% that
   year). The rule's months simply landed on a few big days.
3. **By regime** (high minus low months, TLT window excess):

   | Split | High minus low | t |
   |---|---:|---:|
   | Bond bull years (TLT year > 0) | +15 bps | 0.6 |
   | Bond bear years | +24 bps | 0.6 |
   | 2003-2013 | +46 bps | 1.3 |
   | 2014-2025 | -3 bps | -0.1 |
   | Idle >= 25% at T-4 | +40 bps | 1.3 |
   | Idle < 25% | -6 bps | -0.3 |

   The first condition holds (positive in bull and bear years, both weak); the second fails
   clearly: since 2014, as passive bond assets grew several-fold, high-extension month ends
   are no better than the others. An index-buying flow should have grown, not vanished. The
   idle-cash split is the 2008-09 crisis again (large idle cash, few months).

**How sure.** Sure the rule as carded does not pass and that its book gain is two crisis years.
Not sure the month-end bond rally has nothing to do with index extension: the 20+ bucket
built from par amounts and maturities is a crude stand-in for the index's market-value
duration, and a single 30-year issue barely moves a 20+ bucket. A better dose would need the
index provider's published extension, which is not keyless.

## What wide-5 adds

- **Two structural Treasury flows, two non-results at our fills.** With wide-4's two, four
  forced-flow mechanisms in Treasuries (tax drain, coupon dose, dealer backlog, index
  extension) have now been tested with doses or regimes. None has a dose-response with t above
  1.3 in the direction its story predicts. The month-end bond rally stays unexplained here.
- **The dose method works as a filter**: in both tests the book-level comparison was
  ambiguous (one 0.01 behind, one 0.01 ahead), and the slope said clearly that the mechanism
  is not there.
- **A pattern across lanes**: book gains of +0.01 in these overlays keep tracing back to
  2008-09 or 2022 (large idle cash meeting one big TLT move). Any future idle-cash-into-TLT
  overlay should report its result without 2008-09 before anyone reads it.

## Status (2026-11-18)

**Done:** two new mechanisms and a choice rule; two cards; two train tests; step 3 breakdown;
`ideas.md`; `next-steps.md`. Both fail; held-out year unspent. Draft PR #71 (`wide-5` ->
`wide-4`).

**Doing:** nothing half-finished. No process running.

**Next (not started):** see `next-steps.md`.

### Disclosures

- **One dry run per script** (`DRY=1`, nothing logged), output to `/dev/null`, result files
  deleted unread; then one logged run each. The step 3 script reran the card's three
  configurations without `tries.md` rows (already logged).
- **Seen before the cards**: the auction dataset's field list; the new download's row count
  and per-year counts of filled dealer fields. Before the runs: the parser's counts (2,367
  nominal auctions 1979-10 to 2026-10, 1,390 with dealer data). Auctions after the end of
  train are in the file; the rules drop them (`dealer_surprises` is cut at the train end; the
  extension uses only auctions held by each decision day).
- **TLT tracked a Barclays 20+ index before 2016 and ICE's after**; the bucket follows neither
  exactly (par weights, maturity in place of duration, no buybacks, no Fed add-ons).
- **`ext-high` has 113 high months of 279**, not about half: the rule needs E strictly above
  the median, and E is often tied near zero in months with no new long issue.
- The yearly table compounds within a year: in years when the crypto slots tripled the book
  (2013, 2017) a small daily difference shows up as several points. The summed daily
  differences (columns "in windows", "outside") are the fair measure.
