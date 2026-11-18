# Carry 3: does the funding carry survive real costs?

Research run carry-3, started 2026-11-17. Branch `carry-3` (from `carry-2`). Research only: fake
money, public keyless market-data endpoints only, no change to the gym, the daily runner or the
live strategies. Nothing here can reach an exchange account.

Question: carry-2 found that `ls-funding` (each week, long the third of perpetuals with the
lowest 7-day funding, short the third with the highest) earns on venues and coins it was not
designed on at 10 bps a side (pooled Sharpe 0.69, p 0.04), but it trades ~42 times its size a
year and is about zero at 30 bps. **Does it survive the costs a small fake-money account would
really pay, and does it hold in the held-out year?**

## In plain words (train results, 2026-11-18; held-out line to follow)

HELDOUT-PLACEHOLDER

**On the train years: yes, for a small account. The costs a 10,000 USD account would really pay
are lower than carry-2 assumed, and the book survives them.** Tables: `results/carry-3.md`;
126 rows in `tries.md`.

- **What trading really costs.** About **8 bps a side** (0.08% of each trade): 5 bps is the
  venue's fee at the lowest tier, ~1.5 bps is half the bid-ask gap, ~1.5 bps is the price moving
  against the order (a deliberately pessimistic formula: orders walked through today's real
  order books cost about half of what the model charges). Carry-2 guessed 10 bps; the gym's
  crypto setting is 30 bps.
- **The rule fixed in advance (`band`)**: once a week, long the third of perps with the lowest
  7-day funding, short the third with the highest, but a coin already held stays until it
  leaves its half of the ranking, and small weight changes are not traded. On ~550 coins on
  three venues, 2021-2025, after those costs and every funding payment it made **10.8% a year
  with a 17% worst loss, Sharpe 0.79** (p 0.025; Sharpe = return per unit of risk, 1 is good).
  It passes all four bars of the card, positive on every venue and in both eras.
- **Where the money comes from.** It collects 7.7% of the account a year in funding and pays
  2.5% in costs (1.6% fees, 0.3% spread, 0.6% impact). The fee is two thirds of the cost.
- **Next to the paper system's own rule.** BTC/ETH `tsmom12` on spot made Sharpe 0.70 over the
  same 4.7 years with a 52% worst loss. Half in each: **0.91, worst loss 27%** (p 0.037). The
  two are unrelated day to day (correlation -0.09). That is the case for it: not a better
  rule, a different one.
- **It is small-money only.** With 100,000 USD: 0.69. With 1,000,000 USD: 0.41 (no longer
  distinguishable from luck), because the orders start to move thin coins. At the gym's 30 bps:
  0.28. It lives on the perp venues' low fees.
- **Trading slower did not help much.** The band cut trading from 45x to 32x the account a year
  and ended where the plain weekly book did (0.78). Rebalancing every 2 weeks scored best
  (1.01), every 4 weeks worse (0.69, negative on Bybit), a 30-day funding average much worse
  (0.29). So the information is in *recent* funding and fades within a month; and since costs
  are only ~2.5% a year, turnover was not the real problem once fees were right.

| Pooled, 2021-02 .. 2025-11, realistic cost (10,000 USD) | Sharpe (p>0) | Per year | Worst loss | Traded/yr | Funding/yr | Costs/yr | B-out / Bybit / Hyperliquid | Blend with BTC/ETH `tsmom12` (0.70 alone) |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| `w1`: carry-2's weekly book | 0.78 (0.025) | +11.3% | 18% | 45x | +8.9% | -3.5% | 0.72 / 0.39 / 0.50 | 0.92 |
| `w2`: every 2 weeks, two halves | 1.01 (0.003) | +14.0% | 15% | 27x | +8.0% | -2.0% | 0.97 / 0.39 / 0.66 | 0.96 |
| `w4`: every 4 weeks, four quarters | 0.69 (0.035) | +8.1% | 16% | 15x | +5.9% | -1.0% | 0.58 / -0.07 / 0.51 | 0.85 |
| **`band`: weekly with a no-trade band (primary)** | **0.79 (0.025)** | **+10.8%** | **17%** | **32x** | **+7.7%** | **-2.5%** | **0.72 / 0.45 / 0.61** | **0.91** |
| `f30`: 30-day funding signal | 0.29 (0.22) | +3.2% | 19% | 25x | +8.4% | -2.0% | 0.10 / 0.37 / 0.30 | 0.77 |
| `band`, no costs at all | 0.96 | +13.4% | 17% | 32x | | 0 | 0.85 / 0.63 / 0.74 | 0.95 |
| `band`, spread and impact doubled | 0.73 (0.036) | +9.8% | 17% | | | | 0.67 / 0.38 / 0.55 | 0.89 |
| `band`, 100,000 USD | 0.69 (0.043) | +9.2% | 17% | | | | 0.64 / 0.35 / 0.50 | 0.88 |
| `band`, 1,000,000 USD | 0.41 (0.14) | +4.9% | 20% | | | | 0.47 / 0.11 / 0.15 | 0.80 |
| `band`, flat 30 bps (the gym's crypto cost) | 0.28 (0.24) | +3.1% | 22% | | | | 0.22 / -0.12 / 0.27 | 0.77 |
| `band`, 60% of fills as maker (assumed) | 0.87 (0.014) | +12.1% | 17% | | | | 0.79 / 0.54 / 0.67 | 0.93 |
| `band`, all Binance perps instead of B-out | 1.07 | +16.4% | 16% | | | | 1.15 / 0.45 / 0.61 | |

### How sure (train)

- **Probably real, not proven.** The primary was named before any number, so its own p (0.025)
  is the test. Counting the five shapes scored here it is 0.12, and with carry-2's two signals
  0.17; the deflated Sharpe probability is 0.84 (0.95 would be convincing). 4.7 years give a
  Sharpe an error bar of about +-0.45.
- **Luck in the calendar is large.** The two halves of `w2` differ only in which week they
  rebalance: one scored 0.56, the other 1.22. So `w2`'s lead over `band` (1.01 against 0.79) is
  well inside the noise, and by the card `w2` is a lead (its p x 5 is 0.015), not a result. The
  four phase books of `w4` range from 0.11 to 1.29.
- **Venues are not independent**, and only Binance is clear on its own (0.72, p 0.035); Bybit
  (0.45, 3.5 years, survivors only) and Hyperliquid (0.61, 2.4 years, ~13 coins) are positive
  but each could be luck. 2023 was flat (-0.08).
- **The cost of the past is partly assumed.** Fees are published facts. The spread curve is
  today's order book applied to past volume. The check that was meant to show whether spreads
  drifted (a spread estimate from daily highs and lows) came out as pure noise, as the card
  warned it might, so it says nothing. The guard is the doubled row (0.73): spread and impact
  could have been twice as large and the result stands, because the fee dominates.
- **The model errs on the dear side** for the small account: measured cost of a 300 USD market
  order in today's books was 0.3-0.5 of the model's on every venue.

### Where the carry fails (what the tables show)

- **By holding period:** fine at 1-2 weeks, fading at 4. A 30-day signal still collects the
  funding (8.4% a year) but gives about half of it back on price, where the 7-day signal gains
  on price too. Likely reading, not tested: a coin whose funding has been high for a month is
  one that keeps rising against its shorts.
- **By venue:** weakest on Bybit (0.45 with costs, 0.63 without), where the set is survivors
  only and the short leg lost most.
- **By year:** 2023 (flat) and, on Binance's smaller coins, 2025 (+0.26); best in 2024 (+1.74).
- **By size of the account:** impact takes over between 100,000 and 1,000,000 USD; Hyperliquid's
  13-coin book breaks first (38 bps a side at 1,000,000).
- **By leg:** neither leg earns alone (0.14 and 0.16); the short leg collects the funding
  (+8.2% a year) and gives it back on price in rallies, the long leg hedges it. It only works
  as a pair.

## What going live in paper would need (described, not built)

"Live in paper" = the daily runner decides on real data and the gym keeps a fake-money account,
as it does today for long-only BTC/ETH and the ETFs. Nothing below places an order anywhere.
Sizes: **S** = under a day of agent work, **M** = 1-3 days, **L** = about a week.

**Gym (`src/grimstrade/gym.py`)**

1. **Signed weights and a perpetual instrument (M).** `validate` rejects weights below 0 and
   sums above 1, and `_execute` assumes cash buys units. A perp needs: its own instrument per
   venue (`BTC-PERP@hyperliquid`), weights in [-1, 1] with the sum of absolute weights <= 1,
   and margin accounting (a trade moves no cash except costs; equity = cash + open profit).
   Test: equal to `research/lib/carry3_engine.simulate` on the same decisions.
2. **Funding as a cash flow (M).** A new replay event: at each funding time,
   `cash -= quantity x mark price x rate`. Needs an append-only funding store next to the bars
   (`data/funding/<instrument>.csv`). Hourly on Hyperliquid, 8/4/1-hourly on Binance and Bybit:
   booked as published.
3. **Costs by venue and coin (M).** `Costs` is one fee and one slippage per asset class. Port
   `carry3_cost.CostModel` (taker fee per venue + half-spread from the coin's volume + impact
   from the order's size), with the calibration file under version control and a dated
   re-calibration (the snapshot script) every quarter. The gym's 1% rebalance band has to become
   per strategy: this book holds ~25-70 positions of 0.7-2% of equity each, so a 1% band would
   block most of its trades; the book brings its own band and a 10 USD smallest order.
4. **Margin, liquidation, delisting (S-M).** At gross 1 a liquidation needs a short coin to rise
   ~90% inside one bar, but the gym should still check each bar's high/low against a
   maintenance margin and close at the worst price plus a fee. A delisted perp is closed at its
   last price.

**Data ingest (`sources.py`, `data.py`, `run_daily.py`)**

5. **A perp universe feed (L, the biggest piece).** Today: 6 symbols. Needed per venue: daily
   bars with quote volume and every funding event for every live perp (180 on Hyperliquid, ~520
   on Binance, ~830 on Bybit), plus the instrument list saved every day, so listings and
   delistings come from the record and not from hindsight. All keyless: Hyperliquid `info`
   (`candleSnapshot`, `fundingHistory`, `meta`), Binance `fapi/v1` or its public archive, Bybit
   v5 `market`. Storage on the `paper-trail` branch grows from 6 files to hundreds: one file per
   venue per day is the simpler append-only shape.
6. **Which venue can the unattended runner reach? (S to test, decides the design.)** The runner
   is a GitHub-hosted job. Binance's and Bybit's APIs are known to refuse US addresses, where
   those runners sit; Hyperliquid's API and Binance's public archive (one day late) are open.
   One manual test run settles it. If only Hyperliquid answers, the first paper book is
   Hyperliquid alone (about 13 tradable coins in train, ~25 today): a thin book.
7. **History to start from (S).** A coin needs 365 days of bars and 30 days of funding before
   its first decision: a one-off import from the research cache into the trail.

**Daily runner and strategy**

8. **The strategy file (M).** `strategies/funding_carry.py`: universe rule, 7-day funding rank
   per venue, the `band` rule. The band needs the book's current weights, and
   `decide(history)` sees only bars: either the runner passes the gym's positions in, or the
   strategy replays its own past decisions from the ledger. It decides on Fridays and must be
   able to say "no change" on other days.
9. **One implementation (S).** `long_short`, `band_weights` and the universe rule move to `src/`;
   research imports them, with a test that pins the research numbers.

**Scoreboard and ledger (`report.py`, `ledger.py`)**

10. **What the owner must see (S-M).** Per strategy: price profit, funding received, fees and
    spread paid, gross and net exposure, number of positions, turnover; next to the long-only
    `tsmom12` twin and the 50/50 blend. A market-neutral book judged on return alone looks dull;
    judged on what it adds to the trend book it may not be.
11. **Tries (S).** The book registers with the count of shapes scored in research (5 here, 2 in
    carry-2), so the scoreboard's deflated Sharpe is honest.

Total: about three to four weeks of agent work. The first milestone that proves the plumbing is
a Hyperliquid-only sleeve (smallest feed, no address block), 10,000 USD fake money, gross 1.

## Funding as an input for the ML/RL work

Numbers: not run yet (the table is the last section of `results/carry-3.md`).

### What an ML/RL rung on the perp cross-section would look like (card sketch, not run)

- **Why here and not on the six assets.** rl-3's limit was few independent bets: six assets
  that move together, long-only, half-slot tilts. A cross-section of ~100 perps ranked against
  each other every week has far more of them, and a long-short book can use both ends of a
  ranking. The same weak input is worth more there (skill grows with the square root of the
  number of independent bets).
- **Rows.** One per tradable coin per Friday per venue (carry-3's universe). About 25,000 on
  Binance for 2021-2025, against ~1,300 weeks x 6 assets before; but coins move together, so
  the honest count is nearer the number of weeks times a handful.
- **Inputs (at most five, ranked 0..1 inside the venue each week; rl-3: few inputs):** 7-day
  funding, 30-day funding, 7-day premium, 28-day return, 30-day volume rank.
- **Target.** Next week's return of a long position including funding, minus the venue's mean
  that week (so the model learns ranking, not the market).
- **Gate 1 (cheap, before any model):** each input's weekly cross-sectional IC on train with
  t >= 3 and the same sign in both halves; inputs that fail are dropped, and if funding itself
  fails there is no rung.
- **Gate 2 (rl-3's rule):** plant a known cross-sectional signal in one input and show the
  learner finds it at the strength of the real inputs, before any real run.
- **Learners, in order, each only if the one before adds something:** a pooled ridge regression
  on the ranks, yearly walk-forward refits with a 7-day purge; a small gradient-boosted model
  on the same five inputs; only then an RL agent whose action is a bounded tilt on `band`'s
  weights (rl-2's residual shape) with this card's cost model as the penalty.
- **Book and bar.** Long-short thirds on the model's score with the `band` rule and this card's
  costs. Twin: `band` on raw 7-day funding. Pass: beats the twin pooled with p < 0.10, same sign
  on 2 of 3 venues, still ahead at `x2`. The held-out year is spent by carry-3 if `band` passes
  train here; then the only clean test left is forward paper trading.

## Card (written 2026-11-17, before any new number)

Words used: a *perpetual* ("perp") is a futures contract with no expiry. *Funding* is the fee
longs pay shorts (or the reverse) every few hours to keep the perp near the spot price. *bps* =
hundredths of a percent. *Taker* = an order that trades at once against the book and pays the
spread; *maker* = an order that waits in the book. *Half-spread* = half the gap between the best
buy and sell price: what a taker loses against the mid price. *ADV* = a coin's typical daily
traded value in USD. *Turnover* = how much is traded per year, in multiples of the account.

### What was already seen (disclosure)

Everything in `research/carry-2.md` and `results/carry-2.md`: `ls-funding` weekly at flat 10 and
30 bps, pooled and per venue (B-out 0.57, Bybit 0.31, Hyperliquid 0.47; pooled 0.69 / 0.09), per
year, its turnover (~42x), its legs, and that it is stronger on large coins (all Binance perps
1.17, short-1's 30 coins 1.10). So the direction of the signal and the liquidity effect are
known. **Not seen:** any slower rebalance, any no-trade band, any longer funding window, any
size-dependent cost, any order-book number, any bar after 2025-11-10. Before this card only two
things were checked: the venues' public fee pages (facts below) and that the order-book
endpoints answer (HTTP status only, no content read).

### Cost model (fixed now; every term from public facts)

Cost per side, as a fraction of the traded value, for a trade of `Q` USD in coin `i` on venue
`v` on day `t`:

    cost = taker_fee(v) + m_v x [ half_spread_v(ADV) + vol x sqrt(Q / ADV) ]

- **Fees** (lowest tier, no VIP, no token or staking or referral discount; checked 2026-11-17):

  | Venue | Maker | Taker | Source |
  |---|---:|---:|---|
  | Binance USDT-M futures, regular user | 0.020% | 0.050% | Binance FAQ "Futures fee structure" (updated 2026-05-01); the fee table page itself needs scripts |
  | Bybit linear perpetuals, non-VIP | 0.020% | 0.055% | Second-hand: Bybit's help pages timed out for a plain client (not worked around); 2026 guides quoting Bybit's fee page agree |
  | Hyperliquid perps, tier 0 (14-day volume < 5M USD) | 0.015% | 0.045% | Hyperliquid docs, "Fees" |

- **Fills are taker** (default, conservative): the fee above plus the half-spread plus impact.
- **`ADV`** = the coin's 30-day median daily quote volume in USD on that venue, as known at the
  decision (the same number the universe rule uses). **`vol`** = the standard deviation of its
  daily log returns over the last 30 days (at least 24 present; otherwise the venue's median
  that day).
- **Half-spread** `half_spread_v(ADV) = exp(a_v + b_v x log ADV)` (in bps, clipped to 0.1..100;
  `ADV` clipped to the range seen in the calibration). `a_v`, `b_v` come from **public order-book
  snapshots of today's book, for calibration only**: three snapshots at least one hour apart
  (2026-11-17/18) of every live USDT/USD perpetual on the venue (Binance `fapi/v1/depth` and
  `ticker/24hr`, Bybit v5 `orderbook` and `tickers`, Hyperliquid `l2Book` and
  `metaAndAssetCtxs`); per coin the median over snapshots of the quoted half-spread
  `(ask - bid) / (2 mid)` and of the 24-hour quote volume; least squares of log half-spread on
  log volume over coins with 24-hour volume >= 1M USD. Fallback, fixed now: a venue with fewer
  than 30 such coins, a refused endpoint, or a fitted `b_v > 0` uses the fit over the other
  venues' coins together.
- **Impact** `vol x sqrt(Q / ADV)`: the square-root law with coefficient 1 (the usual size in the
  literature; it overstates tiny orders that fit inside the best quote, which is the
  conservative side for a small account).
- **Check of the model against the book (can only raise costs).** From the same snapshots, the
  measured cost of a market order of 300 and 10,000 USD (walking the visible book, both sides
  averaged; a book too thin to fill it is left out and counted). Per venue,
  `R_v(Q)` = median over coins with 24-hour volume >= 5M of measured / model. If
  `max(R_v(300), R_v(10,000)) > 1.5`, the venue's `m_v` is that ratio rounded up to the next
  half; otherwise `m_v = 1`. The model is never made cheaper by the check.
- **Did spreads drift over the years?** Described only, changes nothing: the Abdi-Ranaldo
  (2017) close-high-low spread estimate on each perp's own daily bars, pooled by ADV third and
  year, next to the model's spread. On daily bars of coins that move 5% a day it is too noisy
  to price a 2 bps spread; it can only show a large drift.
- **Account size and trade size.** `Q = |weight change| x A x (share of the venue)`, the venue
  share being 1 / (number of venue books trading that day). `A` = **10,000 USD** (the gym's
  account; primary), kept fixed. Robustness: 100,000 and 1,000,000 USD.
- **Smallest order:** 10 USD. A trade below that is not made (the weight is left to drift),
  except closing a position.
- **Not modelled:** lot-size rounding, the hour of execution (fills at the UTC daily close, as
  carry-2), exchange outages, margin calls (gross exposure stays near 1, no borrowing),
  interest on collateral (0, as the protocol's cash rule).
- **Caveat stated now:** the spread curve is today's book applied to past volume. If books were
  thinner in 2021-23 at the same volume, past costs are understated. The `x2` row (spread and
  impact doubled, fee unchanged) is the guard.
- **Maker fills (robustness only, one row):** 60% of every trade fills as maker (maker fee, no
  spread paid, none earned: the earned spread is assumed lost to adverse selection), 40% as
  taker at the full cost. The 60% is an assumption, not a measurement.

### Shapes (fixed now; 5 scored rows, all on the funding signal)

All use carry-2's universe (perp paid funding in the last two days, 365 days of its own
history, 30-day median volume >= 5M USD, at least 10 coins), carry-2's signal (minus the 7-day
mean funding rate) unless stated, ranks inside each venue, decisions on Friday's close, +0.5 of
equity over the long leg and -0.5 over the short leg, funding booked at every event.

| Row | Shape |
|---|---|
| `w1` (reference) | carry-2's book unchanged: every week, top third long, bottom third short, equal weights, rebalanced in full. |
| `w2` | The money split in 2 halves; each half is `w1` but rebalanced every 2 weeks, one week apart. No netting between the halves (costs are charged on each). |
| `w4` | The same with 4 quarters, each rebalanced every 4 weeks, one week apart. |
| **`band`** (primary) | Weekly, with a no-trade band. A coin **enters** a leg when it is in that leg's third and **stays** until it leaves that leg's half (top or bottom `floor(n/2)` of the `n` ranked coins). Each leg's target is 0.5 split equally over its members. A member already held is traded only if its weight is more than 25% (relative) away from the target; entries and exits trade in full. A coin that stops being tradable is closed. |
| `f30` | `w1` with a slower signal: the 30-day mean funding rate (at least half the days present) instead of 7-day. |

`band` is the primary because a buffer is the standard way to cut turnover without going blind
for a month; the 1/3 - 1/2 zone and the 25% are round numbers picked here and never tuned. The
phase books of `w2`/`w4` are logged as `robustness`.

Sets, as carry-2: **B-out** (Binance USDT-M perps outside short-1's 30, delisted included),
**Bybit**, **Hyperliquid**; **pooled** = equal capital per venue book on each day it exists.
Twin: `tsmom12` long-only on the same venue's coins, 30 bps flat, no funding (carry-2's twin,
unchanged). Period: train only, decisions to 2025-11-09, no bar after 2025-11-10 loaded.

### Pass bar on train (fixed now)

Judged on **`band` at the realistic cost** (taker, `A` = 10,000 USD). It **passes train** if all
of 1-4 hold:

1. **Pooled:** Sharpe above 0, one-sided stationary-bootstrap p < 0.10 (mean block 20 days,
   2,000 draws, against a zero series).
2. **Every venue:** Sharpe above 0 on B-out, on Bybit and on Hyperliquid (stricter than
   carry-2's "B-out and one other").
3. **Blend with the twin, pooled:** 50% twin + 50% the book beats the pooled twin, p < 0.10.
4. **Eras:** pooled Sharpe above 0 in both eras with data (2020-21, 2022-25).

Reported next to it, not part of the train pass:

5. **The paper-system bar.** The wide-coin twin is a weak book (0.20), so bar 3 is easy. What
   the owner needs: does 50% of the paper system's own rule (`tsmom12` long-only on BTC/ETH
   spot, 30 bps, short-1's data) + 50% the pooled book beat that rule alone on the same days,
   p < 0.10, with a max drawdown not more than 5 points worse? Without bar 5 the book is at best
   "real but not worth adding".
6. **Cost stress:** pooled Sharpe above 0 with spread and impact doubled (`x2`), and at
   `A` = 100,000 USD.

The other four rows are scored by the same bars and shown. None of them can unlock the held-out
year; a non-primary row counts as a lead only if its pooled p x 5 < 0.10 (Bonferroni).

### Multiple testing

Five rows are scored here on the pooled set. The primary was named before any number, so its
own p is the test; its p x 5 (Bonferroni over this card) and p x 7 (adding carry-2's two
signals, of which funding was the better) and the deflated Sharpe (5 trials, the spread of the
five Sharpes) are reported beside it and stated in "how sure".

### The held-out year (2025-11-11 .. 2026-11-09): spent at most once

- **Only if `band` passes train (bars 1-4).** If it fails, the held-out year stays unspent and
  the held-out bars are not even downloaded.
- **One run, the primary only:** `band` at the realistic cost, pooled and per venue, with its
  twin and blend, the BTC/ETH blend of bar 5, and the same run's cost rows (no cost, flat
  10 bps, `x2`) and funding received. No other shape, signal or parameter is ever run on those
  bars under this card.
- **Passes** if the pooled Sharpe is above 0 and the pooled blend is not behind the twin.
  Twelve months cannot prove anything; they can only fail to contradict. Per-venue signs are
  shown and not judged (three one-year samples).
- **Guard:** the run first appends a `heldout` claim row to `tries.md`, then loads the bars. A
  second call finds the claim and refuses (tested offline). The book is simulated from the
  start of train so the band's state carries over; the train part of that run must equal the
  train run to the last digit (a look-ahead check), and only days from 2025-11-11 are scored.
- Bybit serves no delisted contracts, so its held-out book is survivors only (as in carry-2).

### Robustness rows (after the choice; never selectable)

For `band`: no cost, flat 10 and 30 bps (carry-2's costs), `x2`, `A` = 100,000 and 1,000,000,
maker, a liquidity floor (only the 50 highest-ADV tradable coins per venue), all Binance perps
(B-all) in place of B-out, long and short leg alone. For `w1`: flat 10 bps (must reproduce
carry-2's pooled 0.69: a check that the copied code is the same book). The realistic cost of
every row is split into fee, spread and impact, with turnover, cost per year and funding per
year.

### Funding as an input for ML/RL (descriptive, `robustness` rows)

rl-3 found a learner needs a weekly IC (rank correlation between an input and next week's
return) of about 0.10 on few inputs; info-1 found funding had none on BTC/ETH through time.
Here, on train data already seen: the weekly **cross-sectional** Spearman IC of the funding
signal (7-day and 30-day) across the tradable coins of each venue (B-out, Bybit, Hyperliquid,
and B-all), against next week's (a) price return and (b) return of a long position including
funding; mean, t-statistic, share of weeks positive, both halves. At least 10 coins a week.

### Logging

Every scored row gets a line in `research/tries.md` when it runs: `variant` for the five rows on
each set and pooled, `baseline` for twins, `robustness` for the rest, `heldout` period for the
one held-out run. Code: `research/lib/carry3.py`, `carry3_panel.py`, `carry3_cost.py` (copies;
carry-2's modules are not edited), `scripts/fetch_carry3.py`. Tables: `results/carry-3.md`.

### Details fixed while coding (2026-11-18, before the snapshots were parsed or any row was run)

- **Book check, the coin's `vol`:** the snapshots hold no bars, so the model side of `R_v` uses
  each coin's 30-day daily volatility at the end of train (the venue's median for a coin not in
  the train panel).
- **Held-out guard, restart rule:** the run writes its result rows, its file and its printout
  only at the very end, together. A run that crashed before that has shown no number and has
  left only its claim row: it may be restarted. Once a result row exists the guard refuses.
- **Look-ahead check:** the train run drops its last Friday (2025-11-07, as carry-2: no full
  week follows it), the long run does not, so the two are compared up to 2025-11-06.
- **BTC/ETH in the held-out year:** the cache has no held-out spot bars, so the held-out blend of
  bar 5 uses the same `tsmom12` rule on Binance BTC/ETH perp closes (30 bps, no funding). On
  train both versions are shown.
- **`nocost` and flat-cost rows** have no smallest-order rule (they are reference rows).
- **Snapshots:** the first was taken 2026-11-17 22:57 UTC, right after the card was pushed; the
  code that reads them was written after. Requests use a generic client name.
- **Where downloads go:** everything this run downloads or derives is written under the cache's
  `carry-3/` and `derived/carry-3/` folders only. Held-out bars are kept out of the shared venue
  folders so no other loader can pick them up by accident. (The first snapshot's manifest lines
  had already been appended to the cache's shared `manifest.jsonl`; later ones go to
  `carry-3/manifest.jsonl`.)
- **Copy check:** `carry3.py --check` reproduces carry-2 exactly (`w1` at flat 10 bps: 0.57 /
  0.31 / 0.47, pooled 0.69; twin 0.20): the copied code is the same book. No new number.
