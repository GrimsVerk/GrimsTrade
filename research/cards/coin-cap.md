# coin-cap: cap the combined coin weight inside tsmom12

Field: allocation. Written 2026-11-18 11:14 UTC, lane `coin-cap`, burst 1. Before any number of
this rule. Seen before (other lanes, train only): deep-1 found 8 of `tsmom12`'s 10 worst
drawdowns are coin tops; cointop-1 Part C found `stop-0.25` cuts the worst loss from 36.5% to
28.9% at 1-2 points less growth a year and read it as "a smaller coin position, not a better
rule"; `crypto-slot-size` (run 3) found the size of the coin slots matters more than timing.

## Claim

A plain cap on the combined coin weight inside `tsmom12` cuts the worst loss as much as
cointop-1's `stop-0.25`, and costs less growth.

## Why it might work

With six assets each coin has a 1/6 slot, so the coins are up to 1/3 of the book (1/5 while BTC
is the only coin) at 60-90% volatility. A cap removes that weight directly, with no extra
trades and no parameter fitted to coin tops.

## Why it might not

Bitcoin rose about a thousandfold in the sample: holding less of it costs return every year, a
stop only costs it after a fall. A cap does nothing about the timing of the loss. And this is a
choice of risk: the test can describe it, not validate it.

## Rule (fixed)

- Start from the weekly (Friday) `tsmom12` weights: equal slots over eligible assets, a slot held
  if its 365-day log return is above zero, else cash.
- Let `w` be the summed weight of the held coins (BTC, ETH). If `w > C`, scale every coin weight
  by `C / w`. The excess `w - C` goes:
  - `cash`: to cash;
  - `rest`: to the held non-coin slots, pro rata to their weights (cash if none is held).
- No leverage: weights sum to at most 1 by construction. No new data, no fitted parameter.

## Grid (all that will be run)

`C` in {10%, 15%, 20%, 25%} x {`cash`, `rest`} = 8 variants, named `cap10-cash` ... `cap25-rest`.
Six live assets, gym costs, full train (decisions 1994-02-01 .. 2025-11-09). Held-out year
untouched whatever the result.

## Selection (walk-forward, train years only)

For each calendar year Y from 2016 (three years of coin history) to 2025, pick the variant with
the highest ratio of annualised log growth to worst loss over all train days before Y-01-01
(ties: the smaller cap, then `cash`). The walk-forward series `cap-wf` is the stitch of each
year's pick's daily gym returns; before 2016 it is `cap15-cash` (the middle-low cell, fixed
here). Limit, stated now: the stitch leaves out the one switch trade at a year boundary (at most
15% of the book once a year, a few basis points).

## Twins and baselines

`tsmom12` (weekly, the twin) and cointop-1's `stop-0.25` rerun unlogged in the same script, both
through the gym on the same days. Equal weight for reference.

## Bar (for `cap-wf`; every fixed cell is reported the same way)

1. Worst loss no larger than `stop-0.25`'s (28.9% in cointop-1; the rerun number is used).
2. Growth cost smaller than `stop-0.25`'s: CAGR above `stop-0.25`'s CAGR.
3. Sharpe at least `tsmom12`'s and at least `stop-0.25`'s (point estimates; the paired
   block-bootstrap p-values are reported, not required).
4. Same reading at double costs (bars 1 and 2 hold against the 2x-cost twins).

All four hold: "a plain cap does the stop's job cheaper". Bar 1 holds and 2 fails: "the cap is
the same trade as the stop". Bar 1 fails: "the stop does something a cap of these sizes does
not". Nine series are looked at (8 cells + the stitch); with that many, a pass by a hair on
one cell is not a finding, the pattern across the grid is.

## Look-ahead

The cap is a function of the same-day `tsmom12` weights only. Checked two ways before any number:
`harness.check_against_gym` on the capped rule, and a unit test that the cap never raises a coin
weight, never exceeds `C` or a book of 1, and equals `tsmom12` when `C` = 1.

## Result

See `results/coin-cap.md` and `research/coin-cap.md` once run.

## Second reading: coin years only (added 2026-11-18 11:18 UTC, before any of its numbers)

Seen already: the first reading (`results/coin-cap.md`): every cell, `cap-wf` and `stop-0.25`
tie at a full-train worst loss of 28.9%, the dot-com fall, and the summed returns inside deep-1's
coin-crash windows favour the stop. Not seen: any drawdown measured from 2013 on, or any
drawdown inside a window.

Measures (fixed here):

- A. Worst loss on equity re-based at 2013-01-01, through 2025-11-09 (the coin years).
- B. The largest peak-to-trough fall inside each of deep-1's eight coin-crash windows (peak and
  trough both inside the window): the worst of the eight and their mean.
- CAGR over the same coin years, as the cost.

Series: the same 8 cells, `cap-wf`, `stop-0.25` and `tsmom12`, rerun unlogged from the same
code (configurations already logged). No new variant; counted as one more try (one tries row).
Normal costs only.

Bar: for `cap-wf`, A no larger than the stop's and coin-years CAGR above the stop's: "in the
coin years a plain cap does the stop's job cheaper". If no series with at least the stop's
CAGR has an A as small as the stop's: "the stop does more than a cap of the same cost".
Anything else: mixed, the whole frontier is reported. B is expected to favour the stop (its
summed returns in those windows are already seen, and the windows were drawn in hindsight);
A is the fresh number and carries the reading.

## Third reading, lane `coin-cap-2`: independent coin falls on the coin book (added 2026-11-18 19:05 UTC, before any of its numbers)

Branch `coin-cap-2` (from `coin-cap`). Why: the second reading's edge for the stop rests mostly
on one fall (BTC/ETH 2018-20). BTC and ETH have about four tops; the coin book has hundreds of
coin falls, but coins fall together, so the question is how many of them are separate episodes
and whether the stop's edge over a cap of the same cost holds across those episodes, not only in
2018-20.

Seen when this was written: everything on `coin-cap` and `cointop-1` (the coin book has 639
tops in about 19 effective top months; `stop-0.25` holds a coin 16% of the time against the
twin's 52% and is no better than its 26-weeks-late control on Sharpe). One coverage print of the
book (no return, no fall, no rule): eligible coins on 1 July of each year are 1 (BTC) in
2013-16, 13 in 2017, 15 in 2018, 36 in 2019, 87 in 2020, 100 from 2021; panel coins with a year
of prices: 1, 2, 6, 12 in 2013-16. No coin fall was located and no rule run for this section.

### Data and universe

- breadth-1's Coin Metrics book A, unchanged (`breadth_books.cm_book()`), train bars only:
  the top 100 coins by 30-day median market cap among those above the floors, dead coins
  included, as-of rule `x + 1`, 30 bps a side. **All its coins** (BTC, ETH and the six protocol
  coins included; they are also reported alone).
- **Extended in time:** the book's own eligibility from its first eligible day (2013), not from
  the day it first has 30 coins (2019-03-31). Before 2017 that is BTC alone; 2017-18 13 to 15
  coins. Same eligibility rule, just fewer coins. Weekly Friday decisions as in cointop-1.
- Per-coin paper series as cointop-1 (`cointop1_core.paper`): twin `TS` (slot held while
  `r(365) > 0`) and `stop-0.25` (twin and `dd_1y >= -0.25`), unchanged.

### The cap of matched cost

On one coin slot a cap is a fraction `f` of the twin's slot: its daily return is exactly `f`
times the twin's (costs scale too). **Matched cost:** `f*` = mean daily return of the stop / mean
daily return of the twin, pooled over all coin-days the book counts (cointop-1's mask), so the
cap and the stop give up the same arithmetic return per coin-day (what a small slot adds to a
diversified book). If `f*` is not in (0, 1) the comparison is reported and no cap matches.
Reported beside it, not used by the bar: `f_time` = the stop's share of time held / the twin's.
Limit, stated now: on the six assets the cap binds on the summed coin weight, here on each
coin's slot; and `f*` is a description made with the whole sample, not a rule parameter.

### Coin falls

- **Coin fall:** a cointop-1 top (`cointop1_core.find_tops`: high, then at least -50%; a low is
  settled by a doubling) whose lowest price is at least 60% below the high, of a coin in the
  universe on the top day, at which the twin held the coin (trend-on: the rules differ only
  where the twin is in). Top day up to 2025-11-09.
- **Window of a fall:** from 91 days before the top to the settled day (the doubling), at most
  365 days after the low; an unsettled fall ends at the end of train.

### Independent episodes (how coin falls are counted)

- **Market index:** equal weight of the universe's coins, daily simple returns averaged over
  the coins in the universe that day, compounded (BTC alone before 2017). **Market falls:** the
  same top definition on the index (high, then at least -50%, settled by a doubling).
- **Common falls:** a coin fall whose top lies between 60 days before a market top and that
  market fall's low belongs to that market fall's episode. All coin falls of one market fall
  are **one episode**, however many coins.
- **Coin-own falls:** every other coin fall. Sorted by top day, a new episode starts when the
  gap to the previous coin-own top exceeds 30 days (single linkage); each run is one episode.
- Reported: number of episodes (common and coin-own), coin falls per episode, and the
  effective number `1 / sum(share^2)` (share = an episode's coin falls over all coin falls).
  Beside it (not used by the bar), cointop-1's effective number of top months.

### Measures (per coin fall; per episode = mean over its coin falls, each coin fall counts once)

- **M (carries the bar): the deepest fall of the slot's P&L inside the window.** P&L path =
  running sum of the slot's daily simple returns; the largest peak-to-trough drop with both
  ends in the window. The cap's M is `f*` times the twin's, exactly. **Edge** = cap's M minus
  the stop's M (positive: the stop lost less at the same cost). Starting 91 days before the top
  and running into the rebound charges the stop for whipsaws and late re-entry.
- **S (as in the first reading):** the slot's summed return from the day after the top to the
  low. Edge = stop's S minus `f*` times the twin's S. Expected to favour the stop (top and low
  are hindsight; a stop is out by construction for most of a fall); reported, not used.

### Bar (fixed here)

**"Rule PR candidate, for the owner"** only if all hold:

1. At least 8 episodes by the definition above.
2. The stop's episode edge on M is positive in at least two thirds of the episodes, and the
   one-sided sign test over episodes has p < 0.10.
3. Not one episode: the mean episode edge on M stays positive with the episode of the largest
   edge left out (and a bootstrap over episodes, 2,000 draws, seed 0, is reported).
4. The eight coins kept out of choosing `stop-0.25` (BTC, ETH, LTC, XRP, BCH, ETC, XLM, DASH):
   their summed edge on M over their coin falls is positive.

If 1 fails: **"close: too few independent coin falls to tell"**. If 1 holds and 3 fails:
**"close: one-episode effect"**. If 1 and 3 hold and 2 or 4 fails: **"close: no edge across
episodes"**. A pass says the stop cuts coin falls better than a cap of the same cost across
independent falls; it would still be a risk choice for the owner (cointop-1: no Sharpe edge),
and the held-out year stays unspent unless the owner asks for the rule PR.

### Tries

Four rows, idea `coin-cap-2`, the book's equal-slot portfolio of the series (at least one coin
in the universe): `TS` twin (`baseline`), `stop-0.25` (`robustness`: chosen before), the
matched cap `f*` (`variant`) and the time-matched cap `f_time` (`variant`). Train only, normal
costs. A `DRY=1` run on random prices checks the plumbing and logs nothing.
