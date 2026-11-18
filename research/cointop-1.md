# cointop-1: learning coin-top exits on 100 coins, then carrying one setting back to BTC and ETH

Status: **card fixed, nothing run yet** (2026-11-18). Branch `cointop-1` (from `deep-1`).
Research only: fake money, cached data, no change to the gym, the daily runner or the live
strategies. The write-up goes above this line when the run is done; the card below is as it was
committed before any number.

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

(none yet)
