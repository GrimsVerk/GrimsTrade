# coin-cap: cap the combined coin weight inside tsmom12

Lane `coin-cap`, burst 1, 2026-11-18. Card (written and pushed before any number):
`cards/coin-cap.md`. Tables: `results/coin-cap.md`. Code: `lib/coin_cap.py`,
`lib/coin_cap_core.py`; test `tests/test_coin_cap.py`. Run once. Train years only, gym costs,
six live assets, 1994-02-01 .. 2025-11-09. The held-out year is unspent.

## Question

deep-1: 8 of `tsmom12`'s 10 worst drawdowns are coin tops. cointop-1: `stop-0.25` on the coin
slots cuts the worst loss from 36.5% to 28.9% for about 2 points less growth a year, "a smaller
coin position, not a better rule". Is a plain cap on the summed coin weight as good, cheaper?

## What was run

8 fixed cells (cap 10/15/20/25% x excess to cash / to the held non-coin slots pro rata), the
walk-forward stitch `cap-wf` (each year from 2016 the cell with the best growth over worst loss
on all earlier train days), all again at double costs; `tsmom12` and `stop-0.25` rerun unlogged
in the same script. 18 rows in `tries.md` (8 cells, `cap-wf`, 8 cells and `cap-wf` at 2x cost).

## Result

| | Sharpe | CAGR | Worst loss | Coin-crash windows summed | Crypto winter 2018 |
|---|---:|---:|---:|---:|---:|
| `tsmom12` | 1.05 | +17.8% | 36.5% | -156% | -22% |
| `stop-0.25` | 1.09 | +15.6% | 28.9% | -72% | -4% |
| `cap-wf` | 1.05 | +15.7% | 28.9% | -117% | -17% |
| `cap25-rest` | 1.07 | +16.9% | 28.9% | -129% | -17% |
| `cap20-rest` | 1.09 | +16.3% | 28.9% | -110% | -14% |
| `cap15-rest` | 1.06 | +14.6% | 28.9% | -84% | -10% |
| `cap10-rest` | 1.02 | +12.9% | 28.9% | -58% | -7% |

1. **Worst loss: a tie, and not a coin number.** Every cap from 10% to 25%, the stitch and
   the stop all have a worst loss of 28.9%. That is the 2000-02 dot-com fall (-28% in the
   stress table), years before there is a coin in the book. Any rule that takes roughly a
   quarter off the coin weight uncovers the same floor; no coin rule can go below it. So "worst
   loss 36.5% -> 28.9%" does not rank these rules at all.
2. **On worst loss alone the cap is cheaper.** `cap25` reaches the same 28.9% for 1.0 to 1.1
   points of CAGR a year against the stop's 2.2; `cap20` for 1.5 to 1.8. Four of eight cells
   (both 20% and both 25%) have the stop's worst loss and more growth, also at double costs.
3. **Inside the coin crashes the stop is better than any cap of the same cost.** Summed over
   deep-1's eight coin-crash windows the stop loses 72%; `cap20` (more growth than the stop)
   loses 110%, `cap15` (less growth than the stop) still loses 82 to 84%. A cap needs to go to
   10% (5 to 5.6 points of growth a year) to lose less than the stop there. So the stop is not
   only a smaller coin position: per point of growth given up it takes off about twice as much
   coin-crash loss as a cap does.
4. **Sharpe: nothing to tell apart.** All cells are within 0.05 of `tsmom12` (p 0.14 to 0.71);
   `cap-wf` against `stop-0.25` is -0.04 (p 0.69).
5. **Walk-forward picks the loosest caps**: `cap20-cash` for 2016-17, then `cap25` every year.
   Growth over worst loss on a sample where Bitcoin went up a thousandfold favours more coin.

## The bar, as the card set it (`cap-wf`)

- Bar 1 (worst loss no larger than the stop's): **tie**. 28.9% against 28.9%; the script prints
  FAIL because the stitched equity is rebuilt from returns and differs in the last float digit.
  All 8 fixed cells, which need no stitch, hold it. Read as held, with point 1 as the caveat.
- Bar 2 (CAGR above the stop's): holds by a hair, +15.69% against +15.61%. Not a finding.
- Bar 3 (Sharpe at least `tsmom12`'s and the stop's): **fails** (1.048 against 1.048 and 1.091).
- Bar 4 (bars 1 and 2 at double costs): same tie as bar 1; CAGR +15.57% against +15.27%.

Not all four hold, so the card's "a plain cap does the stop's job cheaper" is not claimed.

## Reading

A cap of 20 to 25% on the coins buys the same headline worst loss as the stop for about half
the growth cost, but only because the headline number stops measuring coins once it hits the
dot-com floor. Measured where the coins hurt, the stop does more per point of growth. Both are
risk choices with Sharpe differences inside noise; neither is a better rule than `tsmom12`.

Limits: one run on one history with two coins; the crash windows were drawn in hindsight by
deep-1; `stop-0.25` was chosen on the coin book, the cap grid here; the stitch leaves out one
switch trade a year; nine series were looked at.

## Second reading: the coin years only (2026-11-18, card section dated 11:18 UTC, pushed first)

Same 8 cells, `cap-wf`, `stop-0.25` and `tsmom12`, rerun unlogged; equity re-based at
2013-01-01. One more tries row. Tables: `results/coin-cap-years.md`; code
`lib/coin_cap_years.py`.

| | A: worst loss 2013-25 | CAGR 2013-25 | Sharpe 2013-25 | B: worst fall inside a window |
|---|---:|---:|---:|---:|
| `tsmom12` | 36.5% | +31.4% | 1.40 | 36.5% |
| `stop-0.25` | 17.7% | +25.4% | 1.57 | 14.6% |
| `cap-wf` | 27.2% | +25.6% | 1.44 | 27.2% |
| `cap25-rest` | 27.2% | +28.7% | 1.47 | 27.2% |
| `cap20-cash` | 21.1% | +26.5% | 1.52 | 21.1% |
| `cap15-cash` | 17.2% | +21.6% | 1.54 | 17.1% |
| `cap10-cash` | 15.2% | +16.5% | 1.57 | 14.2% |

- **The tie was the dot-com floor; without it the stop wins.** In the coin years the stop's
  worst loss is 17.7%. No series with at least the stop's growth gets there: `cap20` has
  21.1 to 22.6%, `cap25` and `cap-wf` 27.2%. The card's bar for `cap-wf` does not hold, and its
  second branch does: "the stop does more than a cap of the same cost".
- **To match the stop's worst loss a cap must go to 15% to cash** (17.2%), which costs 3.8
  points of coin-years CAGR more than the stop; 10% to cash (15.2%) costs 8.9 points more.
- **Where the gap comes from:** the long 2018-20 window. The stop's largest fall inside it is
  12.0%; `cap25` 27.2%, `cap20` 21 to 22%, `cap10` 14 to 17%. In the short windows (2013,
  2017-09) the stop is no better than a 20% cap, in 2017-09 no better than `tsmom12`.
- Excess to cash beats excess to the rest on worst loss at every cap (the rest fell with the
  coins in 2020 and 2022) and costs 0.3 to 1.6 points of growth.

This replaces point 2 of the first reading: "the cap is cheaper" was true only of a number
that had stopped measuring coins. Same limits as above, plus: one long window (2018-20) drives
A, so this is close to one observation; the windows and the 2013 start are hindsight choices.

## Third reading, lane `coin-cap-2`: independent coin falls on the coin book (2026-11-18)

Card section "Third reading" (19:05 UTC, pushed before any number). Code
`lib/coin_cap2.py`, `lib/coin_cap2_core.py` (test `tests/test_coin_cap2.py`); run once, 4 tries
rows (idea `coin-cap-2`). Tables: `results/coin-cap-2.md` (the card's measures and bar) and
`results/coin-cap-2-posthoc.md` (splits written after the numbers were seen; not in the bar).

**Setup.** breadth-1's Coin Metrics book, every coin, from its first eligible day (2013; BTC
alone until 2017). Per-coin slots run by the twin and by `stop-0.25`. A cap of matched cost is
`f*` = 0.663 of the twin's slot: the stop keeps two thirds of the twin's mean return (pooled
single-coin Sharpe 0.46 against 0.47, so it also has about two thirds of the volatility) while
holding a coin only 31% as often. Coin fall = a top of a held coin with the low at least 60%
below. Measure M = deepest fall of the slot's P&L from 91 days before the top to the settled
day; edge = matched cap's M minus the stop's.

**How many independent falls.** 445 coin falls on 197 coins; 10 falls of the equal-weight coin
index. By the card's grouping: **21 episodes** (9 common to an index fall, 12 coin-own runs);
effective number by fall shares 7.6 (two index falls, 2021-22 and 2024-25, hold most coins).
The card's episodes overlap in time (coins that topped between two index falls are their own
runs), so 21 is an upper count; one unit per calendar year of the top gives 10.

**Result: the card's bar holds; verdict by the card "rule PR candidate, for the owner".**

| Bar | Needed | Got |
|---|---|---|
| 1. Episodes | at least 8 | 21 |
| 2. Stop ahead | 2/3 of episodes, sign p < 0.10 | 15 of 21, p 0.039 |
| 3. Not one episode | mean edge > 0 without the largest | +16.2% of a slot, +14.9% without `own-5` |
| 4. Eight held-aside coins | summed edge > 0 | +713% of a slot over 39 falls |

- **Not one episode.** The stop beats the matched cap in the 2018-20 fall (+38% of a slot),
  and also in 2020-03 (+35%), 2021-22 (+34%, +42%) and 2024-25 (+17%, +23%). Per year of the top
  (post-hoc): ahead in 9 of 10 years, behind only in 2013. Per coin fall: 339 of 445.
- **Where it loses: fast crashes and BTC.** Behind in 6 of 21 episodes: BTC's 2013-04 one-week
  crash (-19%) and 2013-14 (-8%), the 2017 summer falls (-7%, -8%), XRP 2020-11 (-15%) and the
  big 2021-05 crash (88 falls, -4%). A stop read once a week cannot act inside a fall of days.
  **BTC alone: 1 of 5 falls** (with BTC's own `f*` 0.657: -19%, -8%, -2%, +10%, -6%); ETH alone
  6 of 6 (+3% to +63%). BTC has five falls; that is too few to tell, but nothing says the stop
  beats a cap on BTC.
- **Out of time for the stop's choice** (`stop-0.25` was picked on this book's 2019-25
  selection coins, on Sharpe): coin falls with a top before 2019-03-31 are ahead (41 falls,
  +28% mean, 32 positive), carried by 2018 (25 of 27); the early episodes alone are 1 of 5
  (2013 BTC twice and the 2017 summer behind, 2018-20 ahead).
- **A tail choice, not more return.** Book of the series (tries rows): stop Sharpe 1.34, worst
  loss 37%; twin 1.14, 83%; matched cap 1.15, 66%; time-matched cap (`f_time` 0.311) 1.17,
  37.5% at a tenth of the stop's growth. Against the time-matched cap the stop's edge M is
  negative (5 of 21): the stop is a smaller position on average, placed where falls are not.

**Reading.** The second reading's doubt was that the stop's edge over a cap was one fall
(2018-20). On 445 coin falls it is not: across separate falls, at the same mean return and
about the same volatility, the stop's deepest losses are smaller than a cap's in most
episodes and most years. Two limits stay: it loses in fast crashes, and on BTC itself (five
falls) it does not show the edge; the live coin slots are BTC and ETH. And Sharpe per coin is
unchanged (0.46 against 0.47); what the stop buys is a shallower worst loss for the same
growth, the owner's choice of risk.

Limits: tops, lows and windows are hindsight descriptions; `f*` uses the whole sample; summed
simple returns treat each slot as a constant stake; the episode rule's 60-day lead and 30-day
gap were fixed on the card, not tested for sensitivity; the year table and the BTC/ETH splits
were written after the run.

## Fourth reading, lane `coin-cap-3`: the same stop checked daily (2026-11-18)

Card section "Fourth reading" (19:15 UTC, pushed before any number). Code `lib/coin_cap3.py`,
`lib/coin_cap3_core.py` (test `tests/test_coin_cap3.py`: Fridays equal the weekly stop, no
look-ahead when later prices are scrambled); run once, 6 tries rows (idea `coin-cap-3`).
Tables: `results/coin-cap-3.md`.

**Setup.** The third reading's book, twin, coin falls and 21 episodes, unchanged. The trend part
stays weekly; only the stop condition (`dd_1y >= -0.25`) is read every day, with the book's own
timing (inputs stamped the day before, position earns from the day after: one day later than
DESIGN.md's next open would allow, the same as the weekly stop). `stop-0.25-d` exits and
re-enters on any day; `stop-0.25-dx` exits on any day and re-enters only at the next Friday.
Each gets its own matched cap `f*_v`. Bar corrected for all 13 coin-cap picks: sign test
p < 0.0077, at least 17 of 21 episodes.

| | Weekly `stop-0.25` | `stop-0.25-d` | `stop-0.25-dx` |
|---|---:|---:|---:|
| Matched cap `f*` (2x cost) | 0.663 (0.656) | 0.708 (0.668) | 0.646 (0.629) |
| Switches per coin-year | 3.5 | 8.5 | 5.1 |
| Fee drag, bp per coin-day | 0.29 | 0.70 | 0.42 |
| Out and back within 7 days, per coin-year | 0.47 | 2.58 | 0.91 |
| ... bought back vs sold at | +14.2% | +3.5% | +6.5% |
| Pooled single-coin Sharpe (twin 0.47) | 0.46 | 0.49 | 0.48 |
| Episodes with edge M > 0 (sign p) | 15 of 21 (0.039) | **18 of 21 (0.0007)** | 16 of 21 (0.013) |
| Of the 6 the weekly trailed | 0 | 3 | 2 |
| Mean episode edge M (without the largest) | +16.2% (+14.9%) | +20.5% (+19.2%) | +17.2% (+15.9%) |
| Mean episode edge M at 2x cost | +15.4% | +15.9% | +15.1% |
| Raw M, daily lost less than weekly | - | 10 of 21, mean 0.0 | 12 of 21, +2.6% |
| Fast coin falls (low within 60 days, 74): mean edge | +15.9% | +23.8% | +20.2% |

**Verdict by the card: the daily check does not fix the fast crashes; the weekly stop stays the
recommendation.** Bar 2 (at least 4 of the 6 episodes the weekly stop trailed) fails for both:
`-d` turns the 2017 summer falls (own-0, own-1) and 2021-05 (market-6) around, but not BTC
2013-04, BTC 2013-14 or XRP 2020-11 (worse there: -29% against -15%); `-dx` fixes only the 2017
summer. `-d` holds every other bar (corrected sign test, mean edge, double costs, held-aside
coins +852%); `-dx` also fails the corrected sign test and double costs.

What the daily check does and does not do:

- **It does not make the stop's deepest losses smaller.** Raw M, daily against weekly: `-d`
  loses less in 10 of 21 episodes, the same on average. The fastest falls are faster than any
  rule that reads yesterday's close and fills a day later (BTC 2013-04: -64% in the two days
  after the top; every stop is out only on day 3 or 4, at -52 to -58%).
- **It keeps more of the return.** 2.4 times the switches and 2.4 times the fee drag, but its
  re-entries are cheap (bought back 3.5% above the exit, against 14% for the weekly stop, which
  must wait for Friday), so its mean return is 0.708 of the twin's against 0.663. Its edge over
  a cap grows because the matched cap grows, not because its falls are shallower.
- **That gain is mostly fees away at double costs:** +15.9% against +15.4% (`f*` 0.668 against
  0.656). Whipsaw does not eat the gain at 30 bps; at 60 bps it nearly does.
- **Multiple testing.** With all 13 coin-cap picks counted, the weekly stop's own 15 of 21
  (p 0.039) no longer meets the bar; `-d`'s 18 of 21 (p 0.0007) does, the only series that does.
  The card named `-d` the replacement only if all five bars held, so this is reported, not
  acted on.

**BTC mechanism note (post-hoc, descriptive; `results/coin-cap-3.md`, last section).** The
weekly stop trails a cap on BTC in four falls, for three different reasons:

1. **Too fast (2013-04).** The deepest loss is taken in two days from the top; the stop sells
   after it. A cap wins only by being two thirds the size. No daily close can help here.
2. **Stop hit, sharp rebound, re-entry, second leg down (2013-12, 2017-12).** Weekly: out
   2013-12-21 at -47%, back in 12-28 at -37%, out again 2014-02-08 at -40%; out 2017-12-30 at
   -34%, back in 2018-01-06 at -13%, out 01-13 at -28%. Yes: this is the "hit, then rebound"
   pattern. The daily check does not cure it: it trades the same bounce more often (12 position
   changes in the 2013-14 window, 10 in 2017-18) and its M is 2 to 3 points deeper. A plausible
   cause, not checked: the band is in volatility units, so after a crash raises volatility a
   rebound to -37% already counts as inside it.
3. **The twin does the job itself (2021-11).** The twin is out at -39% by 2022-02-05 and stays
   out through 2022; a cap of that twin is a small, already-good rule. The stop's M here
   includes its 2023 re-entry loss.

On BTC alone, against each variant's matched cap (pooled `f*`): weekly ahead in 1 of 5 falls,
`-d` 1 of 5, `-dx` 3 of 5 (+3%, +2%, +12%; behind by 21% and 13% in the 2013 falls). Five falls
are too few to read; nothing here says a daily check rescues BTC.

**Reading.** The daily check is not the fix for fast crashes: the losses that matter come
before any close-based rule can act, or from re-entering a bounce, which daily reading does more
of. It is a slightly better-paid stop (more return for the same exits) whose advantage over the
weekly stop is about fees, and it is sensitive to them. For the rule-PR question it changes
nothing by the card. It does weaken the case for the weekly stop: counted against everything
coin-cap has tried, the weekly stop's episode edge is not significant.

Limits: one book, one history; `f*` uses the whole sample; the six fast-crash episodes were
picked from the third reading's result (so "fixed" partly measures regression to the mean); the
2x-cost reading uses the same paper fills; the BTC note was read after the numbers; tries rows
are the equal-slot books (worst loss 66 to 70%, set by BTC's 2013-14 fall while it is the only
coin).

## Fifth reading, lane `coin-cap-4`, step 1: why the weekly stop fails (2026-11-18, descriptive)

Post-hoc by nature, no bar, nothing logged. Code `lib/coin_cap4_modes.py` (rebuilds the
third reading's series, falls and 21 episodes in memory); tables `results/coin-cap-4-modes.md`.
For each coin fall: speed (worst price in the first 7 days, days to -50%), gap (worst single
day in the first 30), the weekly stop's first exit (day, price), its band in price terms
(`exp(-0.25 x vol) - 1`), re-entries after the first exit, and where its deepest P&L fall (M)
ends.

| Episodes (each once) | Worst 7 days | Days to -50% | Worst day | Stop's exit price | Leg-1 return | Band at top | After exit (re-entries) | M ends in first leg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Weekly stop trails (6) | -38% | 19 | -30% | -44% | -49% | -34% | -2% | 60% of falls |
| Weekly stop leads (15) | -23% | 82 | -17% | -21% | -23% | -29% | -5% | 37% of falls |

**Failure mode 1, the first leg (the main one).** In the six lost episodes the coin falls
-38% in its first week on average and reaches -50% in 19 days, with single days of -20% to
-49%. The weekly stop is still in at the top in 5 of the 6 and gets out only at -44% (leg-1
loss -49% of a slot, twice the leading episodes'). The loss is taken before a Friday close can
see it, and in 2013-04 before any close can (two days to -50%). Re-entry losses are small
there (-2% after the exit).

**Failure mode 2, a wide band at the top.** The band is in volatility units, so a coin that
was rising wildly is allowed a wide fall before the stop fires: the 2017 summer coins (own-0)
had a band of -44% in price at their tops, and exited at -55%. Across the six the band at the
top is -34% against -29%. This is the case a price-drawdown band is meant for.

**Failure mode 3, re-entry into a bounce (BTC's).** Over all 445 falls: no re-entry after the
first exit, mean edge +25% (257 of 310 positive); one re-entry +11% (71 of 110); two or more
-3% (11 of 25); each re-entry costs about 20% of a slot on average. On BTC this is the 2017-12
fall (back in at -13%, -18% after the exit) and 2021-11 (back in 2023 at -55% with a band
of only -10%). The band at re-entry is not wider than at the top on average (-30% against
-29%), so "the band loosens after a crash" is not the general cause; the re-entries are bounces
the rule reads as new uptrends.

**Speed alone does not sink the stop.** By the first week: falls of -40% or worse (31) still
have a mean edge of +6% (18 positive); -10% to -40% about +20%. The stop loses when a fast
first leg meets a wide band or a coin it is still fully in.

**BTC's five falls:** 2013-04, two days to -50%, worst day -49%: nothing close-based helps.
2013-12, -38% in a week, out at -47% (band -29%). 2017-12, re-entry. 2019-06, ahead (+11%).
2021-11, a slow fall (-6% in the first week) where the twin itself is out at day 89, so the
cap of the twin is hard to beat, plus a 2023 re-entry. Three different reasons in four
losses; five falls cannot tell which matters.

**What this says for the remaining candidates.** A price-drawdown band addresses mode 2 and,
for high-volatility coins, part of mode 1 (an earlier exit); it does nothing for 2013-04 and
may re-enter bounces just the same (mode 3). A cap on top of the stop shrinks every loss in
proportion, including the first leg, and changes no timing. Time under water is the measure
that shows mode 3 (a stop that waits out a fall flat is under water as long as it is out).

## Changes after the card

None to the rule, grid, selection or bar. One reading note: bar 1 is reported as a tie (above).

Third reading: none to its definitions, measures or bar. Added after its numbers were seen
and kept out of the verdict: `lib/coin_cap2_posthoc.py` (by year of the top, before/after the
book start, fast/slow falls, BTC and ETH alone with their own `f*`); it reuses the run's
series and logs nothing.

Fourth reading: none to its variants, measures or bar. Found while running it: in
`lib/coin_cap2.py` the book series were sliced twice (`portfolio`), so coin-cap-2's 4 tries rows
cover 2015-09-23 .. 2025-11-09, not the 2013-02-10 their "From" column says (rows not edited;
the third reading's bar never used them). Fixed in the code for any rerun; coin-cap-3's rows
start on 2013-02-10 as stated.

## Next steps

- Done in the second reading above: worst loss from 2013 on. Time under water is still unread.
- A cap and the stop together (cap 25% + `stop-0.25`) is the obvious combination; card first.
- Nothing here argues for spending the held-out year.
