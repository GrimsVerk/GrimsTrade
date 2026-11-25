# coin-drift-2: wide-16's `band05@coin`, unchanged, on six coins and years it never saw

Lane coin-drift-2, written 2026-11-25 (about 01:15 UTC), **before any return of the books
below was computed**. One pre-registered test of the post-hoc lead `coin-drift-run`
(`ideas.md`), seen in wide-16 (`wide-16.md`, `cards/cost-band.md`) and checked once in
coin-drift-1 (`coin-drift-1.md`, `cards/coin-drift-run.md`: not confirmed, +0.033, z 1.80).

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-25 00:50): **4,119 tries,
N 1,115 for a new pick; measured rho 0.55 gives N_eff 506: a new rule needs z >= 4.70 against
`tsmom12` on the primary test; Bonferroni p <= 9.9e-05.** This card cannot make a pick: it runs
on coins the live strategies do not trade, and `cost-band` already failed the bar on the
primary test (z 2.76). Its job is to say whether the post-hoc story survives on data that did
not suggest it.

## What was seen before this card (disclosed)

- wide-16: `band05` (gym band 0.05 of equity instead of 0.01) on `tsmom12`'s six assets
  +0.049 Sharpe (z 2.76), +0.054 with coin fills free in both books; on its six other coins
  (`OOU_COINS`: LTC, XRP, BCH, ETC, XLM, DASH; returns 2017-08-18 .. 2025-11-09) `band05@coin`
  +0.039 (z 2.47). Gain in the 2017 and 2020-21 coin runs.
- coin-drift-1: on ~90 coins (no BTC, ETH or the six), returns 2019-04-07 .. 2025-11-10,
  the band carried as a share of the slot: +0.033 (z 1.80), drift part with costs zero +0.014
  (z 0.71), no better than its no-trend placebos.
- cointop-1 looked at coin tops before 2019 (108 tops on 40 coins, prices only), never at a
  rebalance band.
- Market caps on 2018-01-01 (below), read to pick the coins; no return of any book below.

## What data neither earlier test saw (the search, written down)

| Candidate | Seen by | Unseen part | Used? |
|---|---|---|---|
| BTC | wide-16 from its gym bars (2012-01-01; held from 2013) | Coin Metrics BTC 2010-07 .. 2011-12: held at most 2011-07 .. 2012-12, one coin, one crash | No: one coin cannot drift against itself in a one-coin book, 1.5 years |
| ETH | wide-16 from 2016-05-18 (held from 2017-05) | CM ETH 2015-08 .. 2016-05: held at most 2016-08 .. 2017-05 | No: one coin, under a year |
| wide-16's six (`OOU_COINS`) | wide-16 from 2017-08-18 | CM histories before 2017-08 (LTC from 2013, XRP/DASH 2014, XLM 2015, ETC 2016) | No: a second book in the same years as the one used; kept as the obvious next test if this one is ambiguous |
| The ~90 coins of coin-drift-1 | coin-drift-1 from 2019-04-07 | Everything before 2019-04-01 | **Yes: six of them, below** |
| Binance 1h panel (from 2017-07), other coin caches | breadth lanes, not the band | the same coins and years as the CM rows | No: same prices, another vendor |

So the only multi-coin history that neither wide-16 nor coin-drift-1 traded is the coins
other than BTC, ETH and the six, **before 2019-04**. Independent by asset and by the window
of each asset; **not independent by calendar**: the book's years 2015-2019 overlap wide-16's
BTC (2013+) and ETH (2017+) years, including the 2017 run that carried wide-16. Coins move
together, so a gain in 2017 here is partly the same episode.

## Data: the "next six" large caps of January 2018

- Source: the Coin Metrics community snapshot `2026-11-13` (breadth-1's `cm_panel`), keyless.
- **The coins, by a rule fixed here and taken from wide-16's own set rule** (`OOU_COINS` are
  "large caps of January 2018"): the six coins with the largest 30-day median market cap on
  2017-12-31 among those eligible in breadth-1's book A on 2018-01-01 (`cm_book().elig`: a
  year of prices, 30-day median volume >= 1 M USD and cap >= 10 M USD, 90-day volatility >=
  20%, not a BTC/ETH copy), excluding BTC, ETH, the six `OOU_COINS` and USDT (a stablecoin;
  book A's volatility floor lets it through in 2017-18). Read from caps only: **XEM, XMR,
  ZEC, DOGE, DCR, REP** (caps 6.0, 4.9, 1.4, 0.64, 0.55, 0.47 bn USD).
- Bars: each coin's CM `PriceUSD`, as breadth-book-1 builds CM bars (`bbook1.prep_coins`: a
  bar on day d opens at the price of the previous known day and closes at d's price, volume
  0), **cut after 2019-03-31** (coin-drift-1's first return day is 2019-04-07; the script
  asserts no bar after 2019-03-31 is in the history). Written under new names (`XEM-CD2` ..)
  so no other lane's file is touched.
- Period, as wide-16's `common.ctx` sets it for an out-of-universe set: returns from the
  first coin's first bar + 366 days (DOGE: 2015-01-24) to the last bar - 1 day (2019-03-30),
  about 4.2 years. A coin joins the book once it has 365 bars (`common.eligible`): DOGE
  2015-01, XMR 2015-05, XEM 2016-04, DCR 2017-05, REP and ZEC 2017-10.
- Stated weaknesses: (1) chosen by size on 2018-01-01, i.e. coins that grew in 2017
  (survivorship toward 2017 winners, the same bias wide-16's set had); the 2018-01-01 ..
  2019-03-30 part, after the choice, is reported separately. (2) 2015-16 is a one- or two-coin
  book of thinly traded coins (reported volume under 1 M USD a day); the gym's costs still
  apply as if they traded on Kraken. (3) About one coin rally (2017, into January 2018) and
  one bust (2018).

## The rule and the comparator (wide-16's, unchanged)

- Weights: `tsmom12` exactly (`wide16.rule()`: each Friday each eligible coin gets 1/(number
  of eligible coins) when its 365-day log return is above zero, else cash).
- **Rule `band05`**: the gym's rebalance band 0.05 of equity (`harness.run(band=0.05)`).
- **Comparator**: the same book with the gym's plain band, `gym.BAND` = 0.01.
- Nothing else differs. No other band is run (`band02` was wide-16's secondary, not the lead).
- Costs: the gym's (`gym.COSTS`): Kraken taker tiers on the book's 30-day coin volume (0.80%
  at no volume), 0.05% slip; start 10,000 USD.

## Statistic

- Daily returns, cash earns 0 (wide-16's convention for its coin set). dSharpe =
  Sharpe(`band05`) - Sharpe(comparator). SE and one-sided p: `wide16.boot` (paired stationary
  bootstrap, 2,000 draws, mean block 20 days, seed 0); z = dSharpe / SE.
- Reported, not scored: the same with coin fills free in both books (the drift part, as
  wide-16's post hoc split); with idle cash at the 13-week bill (Sharpe above bills); dSharpe
  per calendar year and for 2018-01-01 .. 2019-03-30 (after the choice); fills, fees, tracking
  error and correlation of the pair; max drawdowns.

## Bars, stated in advance

- **Project bar** (BAR.md, measured rho 0.55): z >= 4.70. Not reachable as a pick here
  (other data, rule already failed on the primary test); reported for the record.
- **"Real small effect" bar**: dSharpe > 0 with **z >= 2.5**, net of costs, cash 0.

| Outcome | Reading for `coin-drift-run` |
|---|---|
| z >= 2.5 and the costs-free dSharpe > 0 | **Small effect supported** on unseen data (still not a pick; a selectable claim needs the primary test at z >= 4.70, which wide-16 already used up) |
| z >= 2.5 but costs-free dSharpe <= 0 | **Fees, not drift**: the story is not supported |
| 1.0 <= z < 2.5, dSharpe > 0 | **Not confirmed** (consistent with a small effect; this test is underpowered for one); lead stays closed |
| z < 1.0 or dSharpe <= 0 | **Killed**: no support on the only unseen multi-coin data; `coin-drift-run` marked dead |

## Power (written before the run)

wide-16's `band05@coin` had SE 0.016 over 8.3 years. Here 4.2 years, with one or two coins
for the first 15 months (no or little drift to differ on), so SE about 0.02-0.04. At wide-16's
size (+0.039) the expected z is about 1-2; z 2.5 needs about +0.05 to +0.10, i.e. an effect at
least as large as wide-16's costs-free +0.054. **Expected outcome: not confirmed**, unless the
drift premium on these coins is larger than on the six. A fail does not disprove a small
effect; a pass would be the first support from data that did not suggest the idea.

## Checks before the real run

- `tests/test_coindrift2.py` (offline, synthetic): the coin pick excludes the named coins and
  ranks by cap among eligible only; the bar builder cuts after the last day and builds bars as
  breadth-book-1 does.
- A plumbing run on the last 120 days of the window prints **no numbers** (row counts and
  dates only), then one real run, logged.

## Rows in `tries.md` (idea `coin-drift-run`)

`tsmom12@cd2` (`baseline`, band 0.01) and `band05@cd2` (`robustness`: wide-16's configuration
on other data), through `harness.run`; one `note` row with the costs-free split and the
bills reading. Nothing else is run.

## Not run, and why

The six `OOU_COINS` before 2017-08, BTC 2010-12, ETH 2015-16 (table above); `band02`; any
other set, date, band or period; the held-out year.
