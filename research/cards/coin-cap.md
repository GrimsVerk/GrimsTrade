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

## Fourth reading, lane `coin-cap-3`: the same stop checked daily (added 2026-11-18 19:15 UTC, before any of its numbers)

Branch `coin-cap-3` (from `coin-cap-2`). Why: the third reading's stop trails a cap of matched
cost in 6 of 21 episodes, the fast ones (BTC 2013-04 and 2013-14, the 2017 summer falls, XRP
2020-11, 2021-05) and on BTC alone in 4 of 5 falls. A stop read on Fridays cannot act inside a
fall of a few days. Does reading the same stop every day fix those losses, or do the extra
exits and re-entries (whipsaw, fees) cost more than they save?

Seen when this was written: everything on `coin-cap-2` (`results/coin-cap-2.md`,
`results/coin-cap-2-posthoc.md`: the 21 episodes, their edges, BTC's five falls with its own
`f*`) and cointop-1's daily rows on the six assets (`stop-0.25-daily`: Sharpe 1.05, worst loss
30.9%, turnover 7.96, against the weekly 1.09, 28.9%, 3.81; there the trend part was daily too).
No daily-checked series on the coin book has been computed or looked at.

### Variants (all that will be run; fixed here)

Same book, universe, coins, prices, costs and weekly twin `TS` as the third reading. The twin's
trend part stays weekly (Friday); only the stop condition (`dd_1y >= -0.25`, cointop-1's `dd`,
unchanged) is read more often.

- **`stop-0.25-d` (daily check):** every calendar day `t`, hold the coin iff the twin's latest
  Friday decision at or before `t` holds it and the stop condition holds at `t`. Exits and
  re-entries both on any day. On a Friday it equals the weekly stop exactly.
- **`stop-0.25-dx` (daily exit, Friday re-entry):** as the weekly stop, but if the stop condition
  fails on any day after the Friday decision in force, the coin is out until the next Friday
  decision, which applies the weekly stop rule as usual. Exits on any day, re-entry only on
  Fridays (no new parameter: the wait is the weekly rhythm already in the rule).

**Timing (no look-ahead).** The book's own as-of rule, unchanged from the weekly stop: a decision
on day `t` uses values stamped `t - 1` or earlier (the inputs are lagged one day) and the position
earns the returns from the price stamped `t + 1` on (`bb.decisions(..., "daily")`, skip 1). That
is one day later than DESIGN.md's "decision on the close, fill at the next open" would allow with
Coin Metrics' publication lag, so it is conservative, and it is the same timing as the weekly stop:
daily and weekly differ only in how often the condition is read. A unit test checks that a
variant's hold at decision `t` does not change when prices after `t - 1` are scrambled, and that
both variants equal the weekly stop on Fridays.

### Comparison (fixed here)

- The same 445 coin falls, windows and **21 episodes** as the third reading (they depend on the
  twin and prices only, not on the stop), the same measure M (deepest fall of the slot's P&L in
  the window, summed daily simple returns after costs).
- **Against a matched cap:** each variant gets its own `f*_v` = its mean daily return per counted
  coin-day / the twin's (the third reading's definition); edge M = `f*_v` x twin's M minus the
  variant's M. Whipsaw and fees lower the variant's mean return, so they lower `f*_v` too: the
  matched cap of a costlier stop is smaller.
- **Against the weekly stop:** per episode, the weekly stop's M minus the variant's M (raw, no
  cost match), and the difference of the two edges against their own matched caps.
- **Fee and turnover accounting** (30 bps a side, the protocol's crypto cost = gym fee 25 + slip
  5; no rebalance band applies to a 0/1 slot): per variant and the weekly stop, position changes
  per held coin-year, fee drag in bp per counted coin-day (paper series with and without costs),
  short round trips (out and back in within 7 days) per coin-year, and everything again at double
  costs (60 bps a side, `f*` recomputed at that cost for every series).

### Bar (fixed here; each variant judged alone)

Multiple testing: this lane counts every coin-cap pick so far. Rows of kind `variant` under
`coin-cap` (9) and `coin-cap-2` (2) plus this reading's 2 variants: **m = 13**. The sign test
must reach p < 0.10 / 13 = 0.0077, which on 21 episodes means at least **17 of 21** (16 of 21
gives 0.013). For reference only, computed from numbers already seen: the weekly stop's 15 of 21
(p 0.039) would not meet this corrected bar.

"**The daily check replaces the weekly one in the rule-PR recommendation**" only if all hold:

1. Corrected sign test: edge M against its own matched cap positive in at least 17 of the 21
   episodes.
2. Fast crashes fixed: edge M against its own matched cap positive in at least 4 of the 6
   episodes the weekly stop trailed (market-0, market-2, own-0, own-1, own-3, market-6).
3. Gain not eaten: mean episode edge M at least the weekly stop's (+16.2% of a slot), and still
   positive with the episode of the largest edge left out.
4. Fees: at double costs the variant's mean episode edge M is at least the weekly stop's mean
   episode edge M at double costs.
5. The eight held-aside coins (BTC, ETH, LTC, XRP, BCH, ETC, XLM, DASH): summed edge M positive.

If both variants pass, `stop-0.25-d` is named (fewer rules). If 2 holds and any of 1, 3, 4, 5
fails: "**fixes the fast crashes, not overall: the weekly stop stays the recommendation**". If 2
fails: "**the daily check does not fix the fast crashes**". Independent of the verdict, the
result says plainly whether any stop (weekly or daily) meets the corrected sign test.

### BTC mechanism note (descriptive, post-hoc by nature)

For BTC's five falls: the weekly and daily stops' exits and re-entries in each window (date,
price as % of the top), where each series' deepest P&L fall starts and ends, and the twin's exit,
to see whether the stop is hit and then a sharp rebound pays for the re-entry. Marked post-hoc;
not in the bar.

### Tries

Logged rows, idea `coin-cap-3`, the book's equal-slot portfolio of each series (as in the third
reading): `stop-0.25-d` and `stop-0.25-dx` (`variant`), the same two at double costs, the weekly
stop at double costs (`robustness`) and the twin at double costs (`baseline`): 6 rows. Train
only. A `DRY=1` run on random prices checks the plumbing and logs nothing.

## Fifth reading, lane `coin-cap-4`: the last candidates as one set (added 2026-11-18 22:10 UTC, before any of their numbers)

Branch `coin-cap-4` (from `coin-cap-3`). The remaining next-step cards of coin-cap 1-3, carded
together with one decision rule so the family bar counts them once and honestly: a stop whose
band is a price drawdown instead of volatility units, and a 25% cap together with the stop.
Time under water is not a rule: it is a risk measure reported for every series.

Seen when this was written: everything on `coin-cap` .. `coin-cap-3`, and step 1 of this lane
(`results/coin-cap-4-modes.md`, descriptive): the weekly stop loses mainly in the first leg of
fast falls while still fully in (exit at -44% in the six lost episodes), partly because its
volatility band is wide at hot tops (-34% in price; own-0 -44%), and also by re-entering
bounces (falls with two or more re-entries: mean edge -3%). No price-drawdown series and no
capped-plus-stopped series has been computed on any data.

### Candidate A: `pstop` (price-drawdown stop, weekly)

- Coin book, the third reading's book, twin and timing unchanged: on each Friday decision,
  hold a coin iff the twin holds it and `close / highest close of the last 365 days - 1 >= -X`,
  from values stamped the day before (the book's as-of shift, as `stop-0.25`). An unknown high
  is not held. Read on Fridays only (coin-cap-3: daily reading does not fix the fast crashes).
- **`X` is fixed by exposure, not by returns:** from the grid 0.10, 0.11, ..., 0.50, the `X`
  whose pooled time held over the twin's (counted coin-days, cointop-1's mask) is closest to
  the weekly stop's (0.311 in the third reading; the rerun number is used); ties: the smaller
  `X`. Computed from positions only, printed, and frozen before any return, M or edge of
  `pstop` is computed (the script asserts the order). Then the band no longer widens with
  volatility, and the comparison with the weekly stop is at the same time in the market.
- Six assets: the same `X`, carried unchanged into `tsmom12`'s coin slots through the gym
  (`c.weekly`, the gym's own as-of rule), as cointop-1 Part C did for `stop-0.25`.

### Candidate B: `cap25+stop` (six assets only)

`tsmom12` with the weekly `stop-0.25` on the coin slots (cointop-1's rule), then the summed coin
weight capped at 25%, the excess to cash (`coin_cap_core.cap_coins`, mode `cash`). It binds
only while BTC and ETH are both held and both pass the stop. **Stated now:** on the coin book
a cap on one coin's slot is a constant fraction of it, so `cap x stop` has exactly the stop's
edge pattern against a matched cap (edge scales by the fraction, signs do not change: 15 of
21). B therefore cannot pass the episode sign test by construction; it is judged only as a
size choice on the live book, and at most can be "a risk preference, not a proven rule".

### Time under water (reported for every series, the only bar use is B3)

- Coin book, per coin fall: **TUW** = the longest run of consecutive days inside the fall's
  window on which the slot's P&L path (summed daily returns from 0 at the window's start) is
  below its running high. A cap of any size has its twin's TUW (scale does not change it).
  Per episode: the mean over its falls. Series: twin (= every cap), weekly `stop-0.25`,
  `stop-0.25-d` (coin-cap-3, reference, unlogged) and `pstop`.
- Six assets, coin years (2013-01-01 .. 2025-11-09, equity re-based): the longest stretch
  below a previous equity high (days), and the share of days 10% or more below it. Series:
  `tsmom12`, `cap25-cash`, `stop-0.25`, `cap25+stop`, `pstop`.

### Family bar (counts every coin-cap pick)

coin-cap 13 picks (9 + 2 + 2) plus this reading's 2 (`pstop`, `cap25+stop`): **m = 15**; the
sign test needs p < 0.10 / 15 = 0.0067, on 21 episodes at least **17 of 21** (p 0.0036; 16 of
21 is 0.013).

### One decision rule (fixed here)

**A, "`pstop` replaces the weekly stop as the coin-stop candidate"**, only if all hold:

1. Edge M against its own matched cap (`f*` of `pstop`, the third reading's definition)
   positive in at least 17 of the 21 episodes.
2. Shallower losses, not a cheaper cap: raw M smaller than the weekly stop's in at least 14 of
   21 episodes (two thirds; the two are at the same time in the market by construction).
3. Mean episode edge M at double costs at least the weekly stop's at double costs.
4. The eight held-aside coins (BTC, ETH, LTC, XRP, BCH, ETC, XLM, DASH): summed edge M > 0.
5. Six assets, coin years: worst loss no larger than `stop-0.25`'s and CAGR no more than 1.0
   point a year below it.

**B, "`cap25+stop` is worth adding to the stop" (a size preference)**, only if all hold on the
six assets, coin years, against `stop-0.25` alone:

1. Worst loss at least 2.0 points smaller.
2. CAGR at most 1.0 point a year lower.
3. Longest stretch under water no longer.
4. 1 and 2 also hold at double costs (both series at double costs).

**Combined reading (exactly one line each):**

- If A holds: "`pstop` meets the family bar and replaces the weekly stop". If only A1 holds:
  "meets the sign bar, not the rest: reported, not acted on". Otherwise: "no candidate meets the
  family bar: the weekly stop stays a risk preference" (and whether the weekly stop or `-d` meet
  it is restated from coin-cap-3, not retested).
- If B holds: "a 25% cap on top of the stop is an optional size choice (not provable on
  episodes)". Otherwise: "a 25% cap adds nothing worth its cost to the stop".
- BTC's five falls, the six episodes the weekly stop trailed, and TUW are reported for every
  series; none of them is a bar (except B3).

### Tries

Idea `coin-cap-4`, train only: `pstop` on the coin book's equal-slot portfolio (`variant`) and
at double costs (`robustness`); on the six assets through the gym `pstop` (`variant`),
`cap25+stop` (`variant`), and both at double costs (`robustness`): 6 rows. A `DRY=1` run on
random prices / the last 120 days checks the plumbing and logs nothing. Look-ahead: a unit test
that `pstop`'s hold at a decision does not change when later prices are scrambled and is never
on where the twin is off; `harness.check_against_gym` on both six-asset rules before any
number. Held-out year unspent.

## Sixth reading, lane `stop-reentry`: one re-entry rule for the weekly stop (added 2026-11-18 22:36 UTC, before any of its numbers)

Branch `stop-reentry` (from `coin-cap-4`). The weekly `stop-0.25` loses in two ways that are
both about **re-entry**, not exit:

- **Bounce buying** (coin-cap-4 step 1): after a crash its volatility band widens (the band is
  0.25 x the coin's own 60-day EWMA vol, which the crash itself raises), so a bounce brings the
  coin back inside the band and the stop buys it before a second leg down. Falls with two or
  more re-entries: mean edge M -3% (no re-entry: +25%).
- **Late re-entry** (combo-1, PR #70): the stop measures the distance to the one-year high, so
  after a deep fall the coin stays out until the price is back within the band of the *old*
  top or the top is a year old, long after the twin's 12-month trend has turned. On the six
  assets: -21% a year against `tsmom12` in the six months after its ten deepest lows.

Seen when this was written: everything on `coin-cap` .. `coin-cap-4` and combo-1's map. No
series with a cool-off or a reset reference high has been computed on any data.

### The rule (one, fixed here, no grid): `stop-cool-13`

Same book, universe, coins, prices, costs, twin `TS` and Friday timing (inputs stamped the day
before, the book's as-of shift) as the third to fifth readings. Per coin, on each Friday
decision:

1. **Stop-out.** The coin was held at the previous decision, the twin holds it now, and the
   stop condition (below) is known and fails: out, and a **cool-off of 13 Friday decisions**
   starts (91 days).
2. **Cool-off.** During it the coin is out, whatever the twin or the price do.
3. **Reference high reset.** The stop condition is cointop-1's, `log(close / H) / vol >= -0.25`
   (60-day EWMA vol), but `H` is the highest close of the last 365 days **not before the latest
   stop-out decision** (its own close counts). Without a stop-out yet, `H` is the plain one-year
   high (then the rule equals the weekly stop).
4. Otherwise: hold iff the twin holds and the stop condition holds (an unknown vol is not held
   and starts no cool-off).

**Why this targets both failures (mechanism, not outcomes).** The cool-off blocks re-entry in
the acute phase, when the crash's own volatility has widened the band (bounce buying). The
reset high drops the old top from the stop's reference, so after the cool-off the coin comes
back when it is near the highs it has made *since* the exit (not in a second leg down: then the
stop condition fails against the bounce high), without waiting to be near the old top (late
re-entry). After 365 days the rule is the plain weekly stop again.

**Why 13 weeks (set from earlier descriptive numbers, stated before results).** The cool-off
should last until the slow twin has had its usual time to decide on the fall, then hand the
re-entry back to it: the 12-month rule leaves a coin top after a median **106 days**
(cointop-1), and the weekly stop exits on average on **day 15** after the top in the episodes
it leads (coin-cap-4 step 1). 106 - 15 = 91 days = 13 weeks. If the fall is real, the twin is
off by then and the coin stays out on the twin; if the twin still holds, the fall has not
turned the trend and the coin goes back in at the post-exit highs. No other `N` is run.

**Six assets.** The same rule, unchanged, on `tsmom12`'s coin slots through the gym (Friday
decisions, the gym's own as-of rule, `c.weekly`): the state is replayed from past Fridays'
views only (`view.at`), memoised per panel; `harness.check_against_gym` on it before any
number.

### Measures (all reported for the twin, every cap where it applies, the weekly stop and `stop-cool-13`)

- Coin book: edge M against its own matched cap `f*` (the third reading's definition) per
  episode; raw M against the weekly stop; **time under water** per fall (coin-cap-4's TUW);
  **six months after the low**: the slot's summed daily return over the 182 days after each
  fall's low (rows `low + 1 .. low + 182`, clipped at the data's end), per episode the mean;
  re-entries per fall; pooled Sharpe; all at normal and double costs.
- Six assets (full train 1994-2025 and coin years 2013-25): worst loss, CAGR, Sharpe, longest
  stretch under water, share of days 10%+ under water, and combo-1's **turn** measure: excess
  return over `tsmom12`, % a year (mean daily excess x 365), in the 182 days after each of
  `tsmom12`'s ten deepest lows (`deep1_atlas.episodes` on this lane's `tsmom12` gym run).

### Family bar

coin-cap picks so far m = 15; this reading adds one: **m = 16**. The sign test needs
p < 0.10 / 16 = 0.00625; on 21 episodes that is at least **17 of 21** (p 0.0036; 16 of 21 is
0.013).

### One decision rule (fixed here)

"**`stop-cool-13` meets the family bar and replaces the weekly stop**" only if all hold:

1. Edge M against its own matched cap positive in at least 17 of the 21 episodes.
2. Late re-entry fixed: mean (over episodes) six-months-after-low return on the coin book at
   least the weekly stop's, and the six-asset turn excess (full train) above the weekly stop's.
3. Bounce buying fixed: on the weekly stop's falls with two or more re-entries (fixed by the
   weekly stop's positions, 25 falls), mean edge M of `stop-cool-13` above the weekly stop's.
4. Fall protection kept: six assets, coin years, worst loss at most 1.0 point above the weekly
   stop's (17.7% in coin-cap-4), and mean episode edge M at double costs at least the weekly
   stop's at double costs.
5. The eight held-aside coins (BTC, ETH, LTC, XRP, BCH, ETC, XLM, DASH): summed edge M > 0.

Readings (exactly one):

- All hold: as above.
- 1 fails, 2 to 5 hold: "**fixes the re-entry costs without proof: if a coin stop is wanted,
  `stop-cool-13` is the better risk preference, still not a proven rule**".
- Otherwise: "**the re-entry rule does not fix the stop: the weekly stop stays the (unproven)
  risk preference**".

Independent of the reading: unless bar 1 holds, the coin line stays parked (no rule PR from
this lane; the held-out year stays unspent).

### Tries

Idea `stop-reentry`, train only: `stop-cool-13` on the coin book's equal-slot portfolio
(`variant`) and at double costs (`robustness`); on the six assets through the gym (`variant`)
and at double costs (`robustness`): 4 rows. A `DRY=1` run on random prices / the last 120
days checks the plumbing and logs nothing. Look-ahead: unit tests that the hold at a decision
does not change when later prices are scrambled, is never on where the twin is off, and equals
the weekly stop while no stop-out has happened; `check_against_gym` on the six-asset rule.
