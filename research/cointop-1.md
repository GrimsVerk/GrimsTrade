# cointop-1: learning coin-top exits on 100 coins, then carrying one setting back to BTC and ETH

Status: **done on train (2026-11-18): Parts A, B and C run; no rule passes; held-out year
unspent.** Branch `cointop-1` (from `deep-1`), draft PR #40. Research only: fake money, cached
data, no change to the gym, the daily runner or the live strategies. The card below the line is
as it was committed before any number; what differs from it is listed under "Changes after the
card".

## Write-up

Two runs, each once. The coin book (Parts A and B): `uv run python -I research/lib/cointop1.py
--log`, after the look-ahead tests (`tests/test_cointop1.py`) and a plumbing run on random
prices; tables `results/cointop-1-coins.md`; 16 rows in `tries.md` (idea `cointop-1-cm`). The
carry-back (Part C): `uv run python -I research/lib/cointop1_carry.py`, after its look-ahead
checks; tables `results/cointop-1.md`; 19 rows (3 `variant`, 15 `robustness`, 1 `baseline`).
Train only.

**In one line.** A fast exit learned on 100 coins does what it was built for (worst loss 36.5%
to 29%, the losses in the eight coin crashes cut by a third to a half) and adds nothing to
Sharpe: +0.03 to +0.04 over
`tsmom12`'s 1.05, p about 0.3, less than luck alone gives the best of three tries. No rule
passes on the coin book or on BTC and ETH. It is a smaller position, not a better rule.

### Part A: what coin tops look like

- **Many tops, few episodes.** 639 study tops on 223 of the 292 selection-set coins; the twin
  held the coin at 458 of them. They cluster: 2020Q1, 2020Q3, 2021Q2 to 2021Q4, 2024Q1 and
  2024Q4 hold 421 of the 639. The effective number of top months is 19.1 (14.2 for trend-on
  tops). That is the sample the settings were chosen on: more than BTC's and ETH's four tops,
  far fewer than 639. Only 21% of study tops lie within 30 days of a BTC top (BTC's own:
  2019-06-26, 2021-04-13, 2021-11-08).
- **The fall is fast at first.** Median price against the top: -19% after a week, -34% after
  four weeks, halved after 49 days, lowest at -72% after 134 days. 87% of the lows were later
  settled by a doubling. The 108 tops before 2019 (40 coins) look the same or steeper (halved
  in 30 days, low at -76%).
- **The twin is slow, as on BTC and ETH.** At a trend-on top the 12-month rule leaves a median
  106 days later, at -52%; it is still in at 80% of the tops when the coin has halved, and sits
  through 83% of the fall (median; 66% of all falls taken together). Near a BTC top it is worse:
  172 days, -65%, still in at 93%. Before 2019: 188 days, -60%.
- **Almost everything "marks tops" by the card's test, and that says little.** In the 14 days
  before a top the coin has high `z28` (AUC 0.79), high funding (0.78, survivors only), rising
  volume (0.75), a strong coin market (`breadth_28` 0.74), and is close to its one-year high
  (`dd_1y` 0.73). A top is a high by definition, so "the coin has just risen a lot" is partly
  built into the label, and only 899 of 14,639 held coin-weeks carry it: most such weeks are
  not tops. Just after a top the coin still looks strong on every slow feature (`z28` 0.72,
  `z91` 0.73, `dd_1y` 0.72); what has changed is the last week (`z7` 0.41), a volatility jump
  (`vol_shock` 0.74) and volume (0.75). Market cap rank and momentum decay mark nothing.

### Part B: the three exit rules on the coin book

| Rule | Chosen | Pooled single-coin Sharpe (twin 0.44) | Book Sharpe (twin 0.72) | Book worst loss (twin 64%) | Fall sat through, median (twin 83%) | Against its own control | Works there? |
|---|---|---|---|---:|---:|---|---|
| `stop` | `stop-0.25` | 0.42, -0.01 (p 0.55) | 1.00, +0.28 (p 0.16) | 37% | 28% | -0.02 (p 0.56) | no |
| `fade` | `fade-28` | 0.58, +0.14 (p 0.103) | 1.23, +0.51 (p 0.01) | 36% | 35% | +0.14 (p 0.17) | no |
| `breadth` | `breadth-28` | 0.61, +0.18 (p 0.14) | 1.12, +0.40 (p 0.09) | 43% | 30% | +0.15 (p 0.23) | no |

- **The chosen settings are the fastest on each grid.** For `fade` and `breadth` each half of
  the sample alone picks the same setting, and the score falls steadily as the window grows
  (182 days is worse than the twin). The best window may be shorter than 28 days; the card's
  grid stops there and is not extended.
- **Why none is labelled *works there*.** `fade-28` meets three of the four conditions (ahead
  in both halves, book not below, less of the fall sat through) and misses the first: p 0.103
  against the bar's 0.10. `breadth-28` the same, p 0.14. `stop-0.25` is not ahead on the
  selection score at all, and is behind in the first half. The bar was fixed before the run
  and is not moved.
- **Where the gain comes from.** All three leave about 20 days after the top, at -30% to -37%,
  instead of 106 days at -52%. Per coin a year (log points): +44 to +56 saved inside falls, 21
  to 41 given back in the rebounds after the lows, about 1 in costs; net +11 (`stop`), +20
  (`fade`), +24 (`breadth`). Half (`fade`, `breadth`) to three quarters (`stop`) of what a
  fast exit saves is paid back by coming late into the rebound.
- **The control.** Reading the same condition 26 weeks late keeps the time out of the market
  and removes the timing. `stop-0.25` is no better than its control (book 1.00 against 0.99):
  its book gain is the effect of holding 16% of the time instead of 52%, not of when. `fade-28`
  and `breadth-28` are ahead of theirs by +0.14 and +0.15, not significantly (p 0.17, 0.23).
- **`fade` against `breadth`.** 0.58 against 0.61: a hundred coins know about as much as the
  coin's own last four weeks, not more.
- **The second half is weak for everything.** The twin's pooled Sharpe is 0.72 before
  2022-07-01 and 0.09 after; the chosen `fade` and `breadth` reach 0.18 and 0.24.

### Part C: the three settings, unchanged, on BTC and ETH

Six assets, 1994-02-01 to 2025-11-09; only the BTC and ETH slots get the extra condition.

| Rule | Sharpe (`tsmom12` 1.05) | p | Growth a year (17.8%) | Worst loss (36.5%) | Eight coin crashes, summed (-156%) | Six other coins, Sharpe difference | Bars failed |
|---|---|---:|---:|---:|---:|---:|---|
| `stop-0.25` | 1.09, +0.04 | 0.33 | 15.6% | 28.9% | -72% (better in 7, worse in 1) | -0.03 | 1, 2, 4, 7 |
| `fade-28` | 1.09, +0.04 | 0.30 | 16.4% | 28.9% | -104% (better in 7, worse in 0) | +0.01 | 1, 2, 7 |
| `breadth-28` | 1.08, +0.03 | 0.34 | 16.9% | 29.9% | -97% (better in 4, worse in 0) | -0.02 | 1, 2, 4, 7 |

- **All three fail, on the same bars.** The Sharpe gain has p about 0.3 against bar 1's
  0.033, and is below the +0.06 to +0.07 that the best of three unskilled tries would
  show (bar 7). None is ahead in all three coin eras: `stop` is behind in 2022-25 (0.70 against
  0.88), `fade` in 2010-16 (1.54 against 1.55), and `breadth` equals its twin in 2010-16
  because the coin book starts in 2019.
- **They do cut the crashes (bar 3 passes for all).** Worst loss 29-30% instead of 36.5%. In
  the long 2018-20 bear market `stop` made +1.5% where `tsmom12` lost 36.5%. The price is 1 to 2
  points of growth a year and less time in coins (BTC alone is held 38-55% of the time
  instead of 76%): volatility falls from 17.1% to 14-16% in step, which is why Sharpe does
  not move.
- **Nothing on the six other coins, mixed alone.** Other coins: -0.03, +0.01, -0.02. BTC alone:
  all three behind (-0.02 to -0.07). ETH alone: all three ahead (+0.08 to +0.12, p about 0.35).
- **Double costs change nothing** (+0.02 to +0.03). **Daily decisions do not rescue the stop**
  (-0.01 against the daily twin; `fade` +0.05, p 0.25; `breadth` 0.00).
- **Before and after the coin book starts.** `stop` and `fade` are ahead in both parts of the
  coin years (2013 to March 2019: 1.86 and 1.70 against 1.61; after: 1.29 and 1.36 against
  1.20), so the direction is not an artefact of choosing on 2019-25. The size is too small to
  tell from luck in either part.

### What this means

By the card's readings this is "fails on the coin book", and the carry-back agrees with it: a
faster exit does not pay as a better rule, even with hundreds of tops to learn from. The
slowness of the 12-month rule is the price of staying in a coin that keeps rising: half to
three quarters of what a fast exit saves in falls it gives back in rebounds (coin book), and on
BTC and ETH what is left is a smaller, calmer coin position with the same Sharpe. That is the
same trade `trend-vol` and the plain average of all rules already offer (`deep-1.md`): a choice
of risk, not an edge.

What the coin book added: the tops are about 19 separate episodes, not 639, so even the wide
book cannot settle a difference of 0.04 Sharpe. Did the coin book predict BTC and ETH? Its
label did (none works there, none passes here). Its ranking did not: `breadth` and `fade` led
`stop` there by 0.16 to 0.19; here the three are within 0.01 of each other.

For the owner: nothing to decide. If a worst loss near 29% instead of 36.5% is wanted for 1 to
2 points less growth a year, `fade-28` on the coin slots is one more way to buy it, next to the
presets in `risk-map.md`. The held-out year is unspent (the card spends it only on a rule that
passes all seven bars).

Not done, and not planned: windows shorter than 28 days (the chosen settings sit on the fast
edge of their grids; that would be a new card), and any tuning on BTC or ETH.

---

## Card (fixed 2026-11-18, before any cointop-1 number)

Rules: `protocol.md`, all of it. Train period only (decisions to 2025-11-09; no bar after
2025-11-10 is loaded).

### Question

`tsmom12` (hold an asset while its 365-day return is positive) is slow out of a coin top: eight
of its ten deepest drawdowns are Bitcoin and Ether (`deep-1.md`, failure mode 1). BTC and ETH
have about four tops between them, so any exit rule tuned on them is fitted to four events.

1. What do coin tops look like on a book with hundreds of them, and what can be seen before
   and just after one?
2. Can an exit rule whose one setting is chosen on those coins only, by a procedure written
   here, make the trend rule lose less from a top without giving the gain back elsewhere?
3. Does that one setting, unchanged, help BTC and ETH inside the six-asset `tsmom12` book,
   which it was not chosen on?

### What had been seen when this card was written

- Everything on `deep-1` (all earlier runs' write-ups and tables), and the finished write-up of
  the `trend-tune` lane (`research/trend-tune.md` on its branch). What bears on this card:
  - trend-tune, six assets: entry and exit thresholds and lookbacks from 6 to 12 months all
    land within a few hundredths of `tsmom12`; "held only if a faster signal agrees" pointed
    down (-0.11 Sharpe, in sample); the rule was in for 74% of Bitcoin's crash time; three exits
    in four were bought back higher.
  - `drawdown-control` (sell in proportion to the fall from the one-year high): equal to
    `sma200` on the six assets, +0.18 on the six other coins (p 0.06).
  - `trend-vol` (volatility cap on the trend slot): same Sharpe as `tsmom12`, smaller drawdown.
  - breadth-1's coin book: wide `TS` 0.72 Sharpe, 64% worst loss; BTC `tsmom12` about 1.16.
  - The dates of BTC's and ETH's own tops are common knowledge. That is why nothing here is
    chosen on BTC or ETH, and why the choice is mechanical.
- One coverage print of the cached Coin Metrics panel (coins with a price, a year of history, a
  market cap, per year; no return, no top, no rule): 30 coins have a year of history in
  mid-2018, 93 in mid-2019. So the coin book cannot start before breadth-1's date (2019-03-31).
- Nothing else. No top was located, no exit rule run, on any data, for this card.

### Data and the coin book

- **Coin book:** breadth-1's book A, unchanged (`breadth_books.cm_book()`): Coin Metrics
  community snapshot `2026-11-13`, the 100 largest coins by 30-day median market cap on each
  date among those with a year of prices, volume and size above the floors, no stablecoins or
  wrappers; coins that later died are in it. Decisions from 2019-03-31. A value stamped day `x`
  is used from `x + 1`; a position decided on Friday `t` is set at the price stamped `t + 1`
  (breadth-1's as-of rule). Costs 30 bps a side.
- **Selection set:** the book without BTC, ETH and the protocol's six other coins (LTC, XRP,
  BCH, ETC, XLM, DASH). Those eight are what the setting is later tested on, so they take no
  part in choosing it. Honest limit, stated now: coins move together, so from 2019-03-31 the
  eight are out of sample by asset but not by time. BTC before 2019-03-31 (2013 on) and ETH
  (2017 on) are out of sample both ways.
- Read-only: the cached panel `<cache_root>/derived/breadth-1/cm-panel.npz`. New derived files
  go under `<cache_root>/derived/cointop-1/`. The held-out panel file is not opened unless a
  rule passes (below).

### Shared definitions

- `r(h)` = log return of the coin over the last `h` calendar days. `vol` = the protocol's
  volatility: EWMA of squared daily log returns, 60-bar half-life, annualised (the recursion of
  `common.vol_series`; unknown until 20 returns exist).
- **Twin (`TS` on the coin book, `tsmom12` in the gym):** the coin's slot is held while
  `r(365) > 0`.
- **A top (a description, made with hindsight; never an input to a rule).** Per coin, on its
  daily price: follow the highest price since the last settled low (or since the coin's first
  price). The first day the price is at or below half of that high, the high is a **top**. From
  there follow the lowest price; the first day the price is at or above twice that low, the low
  is **settled** and the search for the next top starts from the low's day. So a top is a high
  followed by a fall of at least 50%, and two tops of one coin are separated by at least a
  doubling. A high that has not yet lost 50% at the end of train is not a top (counted and
  reported as "open").
- **Study tops:** tops of selection-set coins that were in the book's universe on the top day.
  **Trend-on tops:** study tops at which the twin held the coin (`r(365) > 0` at the last
  Friday decision before the top). The exit rules exist for these.
- **Paper series (per coin, gym-free).** Position (0 or 1) decided each Friday by the rule,
  only while the coin is in the universe at that decision (else 0), set at the price stamped
  the next day; daily return = position x the coin's simple return, minus 30 bps x the change
  in position on the day it is set. A coin whose price stops is exited at its last price.
- **Pooled single-coin Sharpe:** mean / standard deviation x sqrt(365) of the paper-series
  returns over all coin-days of the selection set (days the coin was in the universe at the
  decision in force). It scores "one coin slot run by this rule, for the average coin", which
  is what BTC's and ETH's slots are; a 90-coin portfolio would average single-coin mistakes
  away. Differences are tested with a stationary bootstrap that resamples dates (mean block 20
  days, 2,000 draws, seed 0), every coin of a drawn date together, so that coins falling
  together do not count as independent.
- **Book Sharpe** (reported next to it): the equal-slot portfolio of the selection set, as
  breadth-1's `TS` (slot 1 / number of universe coins, weights reset each Friday, drift and
  costs as `breadth_xs.simulate`), with the protocol's paired bootstrap.

### Part A: the event study (a description; no pass bar, nothing selectable)

Tables in `results/cointop-1.md`:

1. **How many tops, and how many separate episodes.** Study tops and trend-on tops per coin
   and per calendar quarter; open tops; tops of coins whose price later stopped. Because coins
   top together, also the **effective number of top months**: 1 / sum of squared shares of tops
   per calendar month. That number, not the count of tops, is the number of roughly independent
   episodes the selection rests on. Also the share of study tops within 30 days of a BTC top.
2. **The shape of a fall.** Price relative to the top (median and quartiles) 7, 14, 28, 56, 91,
   182 and 365 days after it; days from the top to -50%; depth and day of the lowest price
   before the settled low.
3. **How slow the twin is.** Per trend-on top: days from the top to the twin's exit, the price
   at that exit relative to the top, the share of tops at which the twin is still in when the
   coin has halved, and the share of the top-to-low fall (in log points) the twin sat through.
   The same for buy-and-hold (100% by construction) as the yardstick.
4. **What precedes a top.** For every Friday coin-day of the selection set on which the twin
   holds the coin, two labels: `before` = a top of this coin falls in the next 14 days;
   `after` = a top of this coin fell in the last 14 days (the earliest a rule that reacts can
   know). For each feature below: its mean on labelled and unlabelled days, and the AUC (the
   chance that a labelled day has a higher value than an unlabelled one; 0.5 = no information),
   with a 90% interval from a bootstrap over dates, for the whole sample and for each half
   (decisions before / from 2022-07-01). A feature **marks tops** only if its whole-sample
   interval excludes 0.5 and both halves are on the same side. Features (all as of the
   decision, fixed here):
   - momentum: `z(7)`, `z(28)`, `z(91)`, `z(365)` (the protocol's `z(h)` = `r(h)` /
     (`vol` x sqrt(h / 365)), clipped to +-5), and momentum decay `z(28) - z(91)`;
   - drawdown: `dd_1y` = log(price / highest price of the last 365 days) / `vol`;
   - volatility: `log_vol`, and `vol_shock` = log(10-bar-half-life vol / `vol`);
   - volume and size: `vol_growth` = log(7-day mean volume / 91-day mean volume),
     `turnover` = log(30-day mean volume / 30-day mean market cap), `cap_rank` = rank of the
     coin's market cap in the universe (0 smallest, 1 largest);
   - the coin market: `breadth_28`, `breadth_91`, `breadth_365` = share of the universe's coins
     with a positive 28-, 91-, 365-day return; `btc_z28` = BTC's `z(28)`;
   - funding (only coins among breadth-1's 30 Binance pairs, from the day their funding
     history starts; those 30 were picked in 2026, so this row is survivors only):
     `funding_7` = mean funding rate of the last 7 days.
5. **Early tops (description only).** Tops before 2019-03-31 of every panel coin that had a
   year of prices at the top: count, the fall's shape and the twin's exit, as in tables 2 and
   3. Coin Metrics has few coins that early (30 with a year of history in mid-2018); this only
   says whether 2013-2018 looks like 2019-2025.

### Part B: three exit rules, one setting each, chosen on the coin book

Each rule is the twin plus one extra condition; the slot is held only while both hold. All
three are stateless (today's position depends on today's history only), decided on Fridays
like the twin. Forms and grids are fixed here; Part A's tables are not used to change them.

| Rule | The slot is held while `r(365) > 0` and ... | In plain words | Grid (one setting is chosen) |
|---|---|---|---|
| `stop-k` | `dd_1y >= -k` | the coin is within `k` years' worth of its own volatility of its one-year high | k = 0.25, 0.5, 0.75, 1.0 |
| `fade-L` | `r(L) > 0` | the coin itself is up over the last `L` days | L = 28, 56, 91, 182 |
| `breadth-L` | at least half of the coin book's coins have `r(L) > 0` | the median top-100 coin is up over the last `L` days | L = 28, 56, 91, 182 |

- `stop` reads the fall from the high; `fade` reads fading momentum of the coin itself;
  `breadth` asks the same question as `fade` of the whole coin market, so `fade` against
  `breadth` shows whether a hundred coins know more than the coin's own price. `breadth` needs
  the wide book and cannot exist on six assets.
- `breadth` uses the book's whole universe (BTC and ETH included as two coins in a hundred)
  and needs at least 30 coins with a known `r(L)`; before the book starts (2019-03-31) the
  condition counts as met, so the rule is its twin there (the protocol's rule for a gate whose
  input does not exist yet).
- Known overlap, accepted: `fade` on coins is the shape of trend-tune's "fast AND slow" cells,
  which pointed down on the six assets in sample. Here it acts on coin slots only and its
  setting comes from other coins. `stop` is a relative of `drawdown-control` (all-or-nothing
  instead of proportional, coins only, joined with the 12-month test). Neither earlier test
  was learned on a wide book or carried back; that is this card's question.

**Choosing the setting (per rule, on the selection set only).** Score of a grid value = its
pooled single-coin Sharpe. Smoothed score = the mean of its score and its grid neighbours'
scores (an edge value has one neighbour), so that a lone spike is not chosen. The chosen
setting is the one with the highest smoothed score; a tie goes to the looser setting (larger
`k`, longer `L`). Twelve grid runs, each a `variant` row (idea `cointop-1-cm`); the twin is a
`baseline` row.

**Reported for every grid value:** pooled single-coin Sharpe and its difference to the twin
(p from the date bootstrap); book Sharpe, difference and p; worst loss of the book; share of
time held; the setting each half of the sample would have chosen alone (decisions before /
from 2022-07-01); and where the difference to the twin comes from, in log points per coin a
year: inside falls (top to lowest price, study tops), inside rebounds (the 365 days after that
low), everywhere else, and costs. Per trend-on top: the rule's exit price relative to the top
and the share of the fall it sat through, next to the twin's (table A3).

**Does it work on the coin book?** The chosen setting of a rule is labelled *works there*
only if all hold: pooled single-coin Sharpe above the twin's with p < 0.10; ahead in both
halves; book Sharpe not below the twin's; and the median share of the fall sat through is
smaller than the twin's. This label is a reading, not a gate: **all three chosen settings are
carried back**, so that the run also shows whether success on the coin book predicts success
on BTC and ETH.

**Control (one `control` row per rule):** the chosen setting with its extra condition read 26
weeks late: the same amount of time out of the market at the wrong moments. A rule that does
not beat its own control has no timing in it.

### Part C: the carry-back test (through the gym)

The three chosen settings, unchanged. In the gym a coin's position comes from the bars closed
before the decision (the gym's rule); `breadth` reads the coin book as of the day before.

- **(a) Six assets, full train (1994-02-01 .. 2025-11-09; BTC from 2013, ETH from 2017).**
  SPY, QQQ, TLT and GLD keep plain `tsmom12`; the BTC and ETH slots get the rule. Twin
  `tsmom12`; benchmark equal weight. One `variant` row per rule (ideas `cointop-1-stop`,
  `cointop-1-fade`, `cointop-1-breadth`).
- **(b) The protocol's other coins** (LTC, XRP, BCH, ETC, XLM, DASH, from 2017-08-18), the rule
  on every slot: `robustness` rows. The other ETFs and the indexes do not apply: the rule is
  for coins, and its setting was learned on coins.
- Also `robustness`: BTC alone and ETH alone; the six assets at double costs; the six assets
  with every decision made daily instead of on Fridays (a stop that is only read once a week
  may be too slow; the twin daily too). None of these can rescue a fail.

**Coin-crash stress windows (fixed here from deep-1's atlas, table 4a: the eight of `tsmom12`'s
ten deepest drawdowns that coins drove, peak to trough):** 2013-04-09..2013-04-16,
2013-12-04..2014-04-10, 2017-06-13..2017-07-16, 2017-09-01..2017-09-14,
2018-01-13..2020-03-12, 2021-05-08..2021-07-20, 2021-11-08..2022-01-22,
2024-12-16..2025-04-08. Reported with the protocol's seven stress windows.

**Pass bar (each rule on its own; all must hold).** Twin: `tsmom12`.

1. Sharpe on the six assets, full train, beats `tsmom12` with bootstrap p < 0.033 (the
   protocol's 0.10 shared among three rules).
2. Ahead of `tsmom12` in all three eras in which the book holds a coin (2010-16, 2017-21,
   2022-25). The book is identical to its twin in 1994-2009 by construction, so the protocol's
   "4 of 5" cannot be met by any coin-only rule; 3 of 3 is the strictest reading left.
3. Worst loss smaller than `tsmom12`'s (stricter than the protocol's "not 5 points worse":
   the rule exists to cut losses), and over the eight coin-crash windows: a better summed
   return than the twin, and better in more windows than worse.
4. Out of universe: ahead of `tsmom12` on the six other coins (the only set it applies to).
5. Beats equal weight on Sharpe.
6. Ahead of `tsmom12` on the six assets in both parts of the coin years: 2013-01-01 ..
   2019-03-30 (before the coin book starts: out of sample by time and by asset) and
   2019-03-31 .. 2025-11-09. `breadth` is its twin before 2019-03-31, so only the second part
   applies to it, and a pass would be labelled "no out-of-time evidence".
7. Deflation: the Sharpe difference to `tsmom12` is larger than the best of 3 unskilled tries
   would be expected to show (Bailey and Lopez de Prado's expected maximum, standard error
   from the bootstrap). The figure for 12 tries (3 rules x 4 settings, as if the settings had
   been chosen on BTC and ETH) is shown beside it; a pass that clears 3 but not 12 is weak.

**Held-out year (2025-11-11 .. 2026-11-09).** Once per rule that passes all seven bars, and
for no other; it passes there if it is not behind `tsmom12`. For `breadth` that one run loads
breadth-1's held-out panel. If nothing passes, the year stays unspent.

**Look-ahead checks.** Unit tests on synthetic prices: a rule's position on a day does not
change when later prices are scrambled; the breadth series for day `d` uses no price stamped
after `d - 1`; a rule whose extra condition is always true gives `tsmom12`'s weights exactly.
`harness.check_against_gym` on six days for each carried rule.

**What each outcome would mean.**

- *Works on the coin book and passes on BTC/ETH:* a candidate change to the coin slots of the
  live rule, for the owner, after the held-out look.
- *Works on the coin book, fails on BTC/ETH:* small coins top differently from the two large
  ones, or six years of coins moving together hold too few separate episodes (table A1 says
  how many). The exit is not transferable; say which.
- *Fails on the coin book:* a faster exit does not pay even with hundreds of tops; the
  slowness is the price of staying in a coin that keeps rising. Then tables A3 and A4 say
  whether anything at all marks a top before the 12-month rule sees it.

### Assumptions

- The Friday decision and the protocol's volatility are kept; no second knob per rule.
- Coin Metrics prices are one reference rate per coin per UTC day; BTC and ETH in the gym are
  Bitstamp/Coinbase bars. The rules use each data set's own prices.
- Reported volume includes wash trading (breadth-1); volume features are descriptions only.
- The tops' 50% and the doubling that settles a low are round numbers taken from the brief and
  from trend-tune's bear-window threshold for coins; they are not tuned.

### Changes after the card

- **Where the tables are.** Parts A and B are in `results/cointop-1-coins.md` (written by the
  run); `results/cointop-1.md` is kept for Part C.
- **Buy and hold in table A3 is not 100%.** The card called it "100% by construction". The
  paper series holds a coin only while it is in the book's universe, so buy and hold leaves a
  coin that drops out of the top 100: still in when the coin has halved at 93% of tops, 87% of
  all falls sat through. The yardstick is reported as computed.
- **Details the card left open, fixed in the code before the run.** Table A4's interval:
  stationary bootstrap over decision weeks, mean block 4 weeks, 500 draws, seed 0; the two
  halves are point values. A coin-day counts in the pooled score on the days its decision is
  in force and on the day on either side (where entry and exit costs fall). The book needs at
  least 10 universe coins to hold anything. "Near a BTC top" uses BTC's tops by the same
  definition.
- **One code fix between the plumbing run and the real run:** the AUC bootstrap crashed when
  asked for zero draws (the half-sample columns). No number existed yet.
- **Part C's look-ahead checks ran in the script on the real bars, not as unit tests on
  synthetic prices.** Before any Part C number: the rule with an always-true extra condition
  gave `tsmom12`'s weights on every decision of the six-asset train run, and
  `harness.check_against_gym` passed on six days for each weekly rule (two days for each daily
  one). The scramble tests of Part B cover the core functions, not the gym versions of the
  conditions.
- **A plumbing run of Part C (`DRY=1`: the last 120 days of train, nothing logged) printed
  numbers before the real run.** The settings were already fixed and nothing was changed after
  it.
- **Twins in Part C.** `tsmom12` on the six assets, the six other coins, BTC alone, ETH alone
  and at double costs were already logged by earlier runs and are re-scored without a new row.
  The daily twin on the six assets is new: one `baseline` row (`cointop-1`, `tsmom12-daily`).
- **Bar 2 for `breadth`.** The card noted for bar 6 that `breadth` is its twin before
  2019-03-31; the same holds for bar 2's 2010-16 era, which it therefore cannot be ahead in.
  It fails bars 1, 4 and 7 regardless.
- **Bar 7's standard error** is the bootstrap's 90% range of the Sharpe difference divided by
  3.29 (as in `deflation.py`).
