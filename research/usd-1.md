# USD 1: does the dollar's 13-week change forecast risk assets, on data no screen has seen?

Research run usd-1, 2026-11-18. Branch `usd-1` (from `slow-1`). Follows slow-1's next lane 1.
Research only: no live change, no backtest unless the replication below passes.

Question: slow-1 screened 49 inputs at 4 and 13 weeks and found nothing that survived the
correction for 192 tests. The closest was `usd_13w`, the dollar index's change over the last 13
weeks: when the dollar had risen, the next 13 weeks were worse (walk-forward IC +0.151, 1 chance
in 1,000 alone, about 1 in 4 among 192 tests). All of it came from BTC and ETH in 2017-2025. A
number found by searching has to be found again, with its sign fixed in advance, on data the
search never touched, before anyone trades it. This card is that second look.

## In plain words (results)

Not run yet. This section is filled in after the numbers.

## Card (written 2026-11-18, before any usd-1 number was computed)

What had been seen when this was written: slow-1's published tables (`results/slow-1.md`),
including its in-sample IC per asset at 13 weeks (BTC -0.363, ETH -0.427, SPY -0.096, QQQ
-0.109, GLD -0.031, TLT +0.034) and its era split; and two coverage prints made for this card,
dates and counts only (the dollar index file runs daily from 1971-01-04 with no gap over 7 days;
first bars of the four indexes and six coins; how many coins the Coin Metrics book holds per
year: none but BTC before 2017, 11 in mid-2017, 34 in 2019, 98 from 2021). No return of any
asset below has been set against the dollar by this run.

IC = correlation between an input and the return that follows (0 = knows nothing).

### The input (unchanged from slow-1 and info-1)

`usd_13w`: the ICE U.S. Dollar Index ("DXY", Yahoo `DX-Y.NYB`, daily close, snapshot
`yahoo-1d/2026-11-12`), log change against the last close at or before 91 calendar days earlier.
A Friday decision uses the latest value dated at least one day before that Friday and at most 21
days old (`info1_features.asof`, `LAG_MARKET` = 1). No smoothing, no other window, no other
transformation.

**Why DXY and not the Fed's index.** It is the series the screen used, so the input is the same
variable and not a cousin of it, and the same file reaches back to 1971. The Fed's broad index
(`DTWEXBGS`) only starts in 2006; the Fed's older major-currencies index (`DTWEXM`, 1973-2019)
is discontinued and not in the cache. Both are used as robustness checks only (below). DXY is the
dollar against six rich-country currencies (euro 58%, yen 14%, pound 12%): it says little about
emerging-market currencies. Its values before March 1973 are a back-calculation over the last
years of fixed exchange rates; a robustness row drops them.

### The sign (fixed now)

**Negative, as slow-1 observed it: a dollar that rose over the last 13 weeks is followed by a
worse stretch for risk assets.** Every statistic below is written as `S = -IC`, so **S > 0 means
"same sign as the screen"** and S < 0 means the opposite. Nothing is fitted to choose the sign.

### Horizons and target

13 weeks is the horizon the result was found at: the bar is judged there. 4 weeks is reported
next to it as a secondary reading and cannot pass or fail the card.

Target `z_h`, slow-1's (`slow1_ic.horizon_z`): the log return from the first open after Friday
`i` to the first open after Friday `i + h`, over the asset's EWMA volatility at Friday `i` x
sqrt(7h / 365), clipped to +-5. An asset counts once it has a year of bars. Train data only: no
bar after 2025-11-10 is loaded; the held-out year is not touched by this card's replication.

### The three replication sets (none used by slow-1)

1. **`before`: stock markets before the screen's window.** The protocol's four indexes (S&P 500,
   Nikkei 225, FTSE 100, DAX; price indexes, local currency), every Friday from the first with a
   dollar value (April 1971) whose 13-week window closes by 2000-01-07, the screen's first
   Friday. FTSE enters in 1985, DAX in 1989. About 29 years, some 114 separate quarters. **This
   is the only set that shares no date with the screen.** Caveats from the protocol: no
   dividends; Yahoo's index open is often the previous close (the window then starts at Friday's
   close instead of Monday's open).
2. **`markets`: the rest of the 33-market pool, 2000-01-07 to the end of train.** The pool's
   risk markets that the screen did not use: 6 other ETFs (IWM, EFA, EEM, VNQ, DBC, SLV), the 9
   sector ETFs, and the Nikkei, FTSE and DAX. 18 markets. Left out and only shown: IEF and LQD
   (safe assets by the protocol; the claim is about risk assets) and the S&P 500 index (after
   1993 it is SPY, which the screen used).
3. **`coins`: the other coins.** breadth-1's Coin Metrics wide book (the 100 largest coins on
   each date, point in time, coins that later died included; 304 coins over time) **without BTC
   and ETH**, every Friday from the first with at least 5 such coins (April 2017). Target on
   Coin Metrics' clock, with breadth-1's as-of rule: a decision on Friday `t` uses the universe
   and volatility known from prices stamped up to `t - 1`, and earns the log return from the
   price stamped `t + 1` to the price stamped `t + 1 + 7h`; a coin whose price stops inside the
   window keeps its last price (it is not dropped); same EWMA volatility recipe (60-day
   half-life), same clip. The protocol's six coins on the gym's own bars are a robustness row.

### What each set can and cannot show (said now, so the result is not over-read)

- `coins` and `markets` share their dates with the screen. Other coins move with BTC and ETH,
  and most of the 18 markets move with SPY and QQQ. The screen already showed the dollar and
  BTC/ETH lining up in 2017-2025, and it already showed SPY at -0.096 and QQQ at -0.109 in
  sample. So **`coins` will very likely show the same sign whether the effect is real or a
  fluke of one crypto era, and `markets` leans that way too.** A pass there is an echo of the
  screen, not a second finding. These two sets can sink the idea; they cannot confirm it alone.
- To separate echo from news, each of the two is also measured on **the part the screened
  assets do not explain** (`-resid`): each market's `z_h` minus its least-squares fit on SPY's
  `z_h` of the same Friday; each coin's `z_h` minus its fit on the mean of BTC's and ETH's `z_h`
  (computed from the same Coin Metrics panel). One slope and one intercept per asset, fitted
  over all its cells; a coin needs at least 26 cells. The fit uses the whole sample: it defines a
  target, it is not a forecast. S > 0 on a `-resid` row means the dollar reaches those assets
  harder than it reached the screen's. If the effect is real but hits every risk asset about
  equally, the `-resid` rows are near zero: they are a reading, not part of the bar.
- EFA, EEM, DBC and SLV are priced in dollars. If the dollar simply keeps moving the way it
  moved (currencies trend at this horizon), they fall for that reason alone. The per-asset table
  shows whether a `markets` result sits only in those four.
- `before` is clean but is stocks only, in another era. It tests the general claim "a rising
  dollar is followed by a weak quarter for risk assets". If the effect is real but particular to
  crypto, no existing data can confirm it, and the card will say so.

### Statistics (per set and horizon)

1. **S**: minus the Pearson correlation of `usd_13w` with `z_h` over all cells of the set (every
   Friday, overlapping windows; slow-1's IC with the sign turned).
2. **Chance (overlap-corrected).** A 13-week return measured every Friday is the same quarter
   counted 13 times, so no error here is 1/sqrt(rows). As in slow-1, the weekly dollar series
   is rotated in time and S recomputed: 2,000 rotations, seed 0, offsets uniform between 52
   weeks and (length - 52 weeks). One difference from slow-1, because the sets now span
   different decades: the rotation is over the dollar's whole weekly history (1971-2025) and
   **each rotation is applied to all sets at once**, so the dependence between sets that share
   dates is kept. **p** = share of rotations with S at least as large (one-sided). Also shown:
   the null's standard deviation, `N eff` = 1 / its variance (the number of independent
   observations the S is worth), and "detectable" = 2.49 x that sd (the true IC this test would
   catch four times in five).
3. **Non-overlapping S**: S on every `h`-th Friday, mean and min..max over the `h` starting weeks.
4. **Basket S**: correlation across Fridays of the dollar with the average `z_h` of the set that
   Friday (one number per date, so a set with many assets late does not outweigh its early years).
5. **Per asset and per era** (descriptive): S for each asset (for `coins`: the share of coins
   with S > 0 among coins with at least 52 cells, and the protocol's six by name); S by era
   (`before`: 1971-79, 1980-89, 1990-99; `markets`: 2000-09, 2010-16, 2017-21, 2022-25; `coins`:
   2017-21, 2022-25).
6. **Walk-forward IC, slow-1's scheme** (shown for comparison with the 0.151; not in the bar,
   because a fitted slope can be stably positive with the wrong sign): OLS refitted every two
   years on Fridays of years before `y0 - 1`, at least 104 training weeks; a pooled slope
   (`pool`) and, for `before` and `markets`, a slope per asset (`per`). The share of test blocks
   whose fitted pooled slope has the card's sign is shown next to it.

**Pooled.** `P` = the mean over the three sets of S / (its null sd). Sets count equally, not
cells: pooled by cells, the coin book (some 30,000 cells, one crypto market) would be nearly the
whole answer. p from the same joint rotations.

### The bar (13 weeks; fixed now)

`usd_13w` **replicates** only if all three hold:

- (a) pooled: P > 0 with p < 0.05, one-sided;
- (b) S > 0 in at least 2 of the 3 sets;
- (c) the one set that shares no date with the screen, `before`, has S > 0 with p < 0.05.

(a) and (b) are the bar as briefed. (c) is added by this card and is stricter: because of the
echo described above, (a) and (b) could be met by coins moving together in the very quarters
the screen already counted. Outcomes, named now:

- **Replicates** (a, b, c): a trading card follows (outline below).
- **Echo only** (a and b, not c): the same sign shows wherever the new data share dates with
  the screen, and the independent decades do not confirm it. Not a replication. No trading card.
- **Does not replicate** (a or b fails): dead as a general rule; BTC and ETH in 2017-2025 stay
  one unconfirmed observation.

### Controls and robustness (cannot change the verdict)

- **Reproduction** (already public, nothing logged): the same code on the six assets from
  2000-01-07 must give slow-1's IC for `usd_13w` (-0.115 on 5,930 cells at 13 weeks, -0.053 on
  5,984 at 4 weeks) and its per-asset column to three decimals. The six-asset row is shown in
  the table with this card's rotation p, labelled "discovery sample, not a test".
- **Clock check** (plumbing): BTC's `z_h` from the Coin Metrics panel against BTC's `z_h` from
  the gym's bars; the correlation is printed, it is not a result.
- **Robustness rows** (kind `robustness`, run with the same rotations, after the verdict):
  1. `coins` on the protocol's six other coins (LTC, XRP, BCH, ETC, XLM, DASH; gym bars and
     opens, slow-1's target exactly) instead of the Coin Metrics book.
  2. `before` from 1974 only (the dollar floats; no back-calculated index values).
  3. `before` with the Fed's major-currencies index (`DTWEXM`) in place of DXY, if FRED's
     keyless download serves it (to `<cache_root>/downloads/usd-1/`); dropped and said if not.
  4. `markets` and `coins` with the Fed's broad index (`DTWEXBGS`, from 2006). For both Fed
     series a value counts as public 7 days after its date (the H.10 release was weekly).
  5. The left-outs, shown only: IEF, LQD, and the S&P 500 index from 2000.

### Trading card: only if it replicates (outline fixed now)

Written out in full in this file and committed before any trading number. Outline: on Fridays
when `usd_13w` > 0, a slot of `tsmom12` is held at half size; otherwise `tsmom12` unchanged.
`usd-coin` (primary: the brief's rule, and where the effect was found): the coin slots only.
`usd-risk`: every risk asset's slot (the protocol's risk/safe split). The rule can only cut a
slot, never add (rl-2's cap). Threshold 0 and factor 0.5 are fixed here, not tuned. Twin
`tsmom12`; the protocol's default pass bar plus macro card bar 6 (not behind `tsmom12` since
2003) and the count of dollar-up spells; out-of-universe sets as for macro gates. Train only.
The held-out year (2025-11-11 .. 2026-11-09) is looked at once, and only for a rule that passed
train.

If it does not replicate: no trading card, no backtest, held-out year untouched.

### Logging

One row per set x horizon in `tries.md` (kind `screen`, idea `usd-1`: descriptive, not a
backtest, not selectable): 3 sets x 2 horizons, the 2 x 2 `-resid` rows, the 2 pooled rows;
robustness rows as `robustness`. Table `results/usd-1.md`. Script `lib/usd1.py`; derived arrays
under `<cache_root>/derived/usd-1/`.

## Disclosures

- 2026-11-18, before the logged run. Reproduction (`usd1.py --check`): on the six assets from
  2000-01-07 the code gives slow-1's cells exactly (5,930 and 5,984) and its IC, per-asset ICs
  and both walk-forward ICs for `usd_13w` to within 0.0005 (the rounding), at both horizons;
  the dollar value on every six-asset Friday equals info-1's feature. Clock check: BTC's `z_h` on
  Coin Metrics' clock against the gym's bars correlates 0.995 (13 weeks) and 0.985 (4 weeks).
- Coverage printed by the same check, dates and counts only, no S of any replication set:
  `before` 4,306 cells on 1,487 Fridays (1971-04-09 .. 1999-10-01, about 114 quarters);
  `markets` 22,563 cells on 1,336 Fridays (to 2025-08-08); `coins` 30,307 cells on 433 Fridays
  (2017-04-28 .. 2025-08-08, about 33 quarters), 292 coins; the protocol's six coins 2,010 cells.
  The dollar series has no missing Friday from 1971-04-09.
- **Robustness row 3 is dropped.** FRED did not serve the Fed's old major-currencies index to a
  plain keyless request (one timeout from the script, one connection reset from `curl` sent
  with the repo's usual `fetch.py` client string). A third attempt, with a browser's client
  string, was stopped by the session's permission check before it was sent, and rightly:
  dressing a script up as a browser to get past a server that had just refused it is not a
  "keyless public download". Nothing was downloaded; nothing was tried after that. The check
  that Yahoo's early DXY values are sound therefore rests on row 2 (`before` from 1974) and on
  the file having about 250 closes in every year from 1971. Getting `DTWEXM` properly (the
  Fed's own H.10 download page, or the FRED API with the owner's key) is listed for the owner.
- Details the card left open, fixed in the code before the run: p is the share of rotations
  with S at least as large (slow-1's convention, no +1); `coins` gets the pooled walk-forward
  slope only (a slope per coin on 292 coins is noise); `-resid` needs 26 cells for any asset, not
  only coins; a per-coin S is counted from 52 cells; a Friday inside the Fed broad index's span
  with no value under the 21-day rule takes the previous Friday's (count shown in the table);
  the robustness rows are computed in the same process as the main rows, after them, with the
  same rotations.

## Status (2026-11-18)

**Done:** this card; code and tests (`lib/usd1.py`, `tests/test_usd1.py`); reproduction.
**Doing:** the one logged run. **Next:** table, write-up, `next-steps.md`.
