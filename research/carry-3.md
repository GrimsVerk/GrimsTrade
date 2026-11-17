# Carry 3: does the funding carry survive real costs?

Research run carry-3, started 2026-11-17. Branch `carry-3` (from `carry-2`). Research only: fake
money, public keyless market-data endpoints only, no change to the gym, the daily runner or the
live strategies. Nothing here can reach an exchange account.

Question: carry-2 found that `ls-funding` (each week, long the third of perpetuals with the
lowest 7-day funding, short the third with the highest) earns on venues and coins it was not
designed on at 10 bps a side (pooled Sharpe 0.69, p 0.04), but it trades ~42 times its size a
year and is about zero at 30 bps. **Does it survive the costs a small fake-money account would
really pay, and does it hold in the held-out year?**

## In plain words

Not run yet. The card below was committed and pushed before any new number.

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
