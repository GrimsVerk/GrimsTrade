# Short 1: what would a short side on perpetuals add?

Research run short-1, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-short-1.md`.
Branch `short-1` (from `breadth-1`). Research only: the gym and the live system are not
changed. Fake money only; nothing here can reach an exchange account.

Question: most information found so far is relative (low-vol beats high-vol, large beats small,
high funding underperforms, yesterday reverses). A long-only book can use only half of it. On
Binance USDT perpetuals, after fees, slippage and the funding every position pays or receives,
does a short side add a gain worth its risk over `tsmom12` long-only on the same coins?

## In plain words (results)

(Filled in after the runs; see Status.)

## Card (written 2026-11-13 ~08:20 UTC, before any number below was computed)

### What was already seen (disclosure)

This card is not blind. Breadth-1 already measured, on the same 30 Binance pairs and the same
years, the long-only ICs of every signal used here (`results/breadth-1.md`, book A2): `low_vol`
+0.10, `turnover` +0.076, `size` -0.075 (large coins win), `funding` +0.043, `premium` +0.030
(weekly), `rev_1` +0.019 (daily). The tilt directions below follow those signs, so the
train-period numbers are a measurement of what is known, not a test of it. Only the held-out
year (at most once per survivor) is a clean test. No long-short return, no funding cash flow
and no short `tsmom12` had been computed before this card.

### Books

- **P30: the Binance USDT perpetuals of breadth-1's 30 pairs.** Survivors picked in 2026 (stated:
  every coin here is alive today, which flatters longs and hurts shorts). Point-in-time listing: a
  coin is tradable on day `t` only if its perpetual paid funding within the two days before `t`
  (the perp exists then; the cache's funding history starts 2020-01, so earlier listings are
  cut to that date) and it has 365 days of spot bars and a 30-day median spot quote volume
  >= 5M USD (breadth-1's rule). Decisions start once 10 coins are tradable.
- **BTC/ETH:** the same rules on BTCUSDT and ETHUSDT alone (the simplest case).

### Prices and funding

- **Price.** No perpetual price bars are in the cache, so the perp's daily return is the spot
  pair's (UTC daily close from breadth-1's hourly bars). The perp trades within a small,
  mean-reverting basis of spot (the premium index, mostly within +-0.1%), so this adds noise,
  not drift. Stated as a limitation.
- **Funding** (cached `fundingRate` history, every event, 8-hourly; TON 4-hourly). Return day
  `t` covers the close of `t - 1` to the close of `t`, i.e. events stamped in (00:00 of `t`,
  00:00 of `t + 1`]. A position with weight `w` (negative = short) earns `-w x rate` at every
  event: a positive rate means longs pay shorts. Weights drift with prices between decisions.
- **As of.** Signals use bars and funding events up to the decision's close; positions take
  that close as entry (the gym's next-open fill, which in crypto is the same tick). The 365-day
  trend uses closes through the decision day.

### Costs (fixed now)

- **Perp trading: 10 bps a side** = 5 bps taker fee (Binance USDT-M, base tier) + 5 bps
  slippage, on every unit of weight change, long or short. **30 bps a side** is rerun for every
  shape as robustness (the protocol's crypto cost; an account that pays retail spot prices).
- **Spot long-only baseline: 30 bps a side** (the paper system's cost, protocol).
- **Leverage and margin.** Every shape has gross exposure <= 1 (sum of |weights| <= 1 of
  equity), so no money is borrowed; the USDT collateral covers every position in full. The
  carrying cost of a perp position is its funding, charged in full above. Collateral earns 0
  (protocol: cash earns 0; on Binance it could earn some yield, so this is harsh). If equity
  falls to 0 the book is dead (cannot happen at gross 1 unless a short leg rises > 100% in a
  day: checked, reported).

### Signals (direction fixed from breadth-1's signs, see disclosure)

All as breadth-1's book A2 computed them, at the decision: `low_vol` = -(90-day vol), long
calm; `size` = +log(7-day mean market cap, Coin Metrics, lagged a day), long large (breadth-1's
measured sign, the opposite of its card); `turnover` = -log(30-day quote volume / market cap),
long low turnover; `funding` = -(7-day mean funding rate), long low funding; `premium` =
-(7-day mean premium index), long low premium; `trend` = log return over days 365..28 (12-1),
long high; `rev_1` = -(last day's log return), long losers (daily only); `combo` = the mean of
the cross-sectional ranks (0..1) of `low_vol`, `size`, `turnover` and `funding` (the four with
weekly IC t >= 2.8 in breadth-1), fixed now.

### Shapes

- **`ls-<signal>` (market-neutral long-short).** At each decision rank the tradable coins; long
  the top third, short the bottom third, equal weight, +0.5 and -0.5 of equity in total (gross
  1, net 0). Weekly (Friday close) for every signal except `rev_1` (daily). 8 variants.
- **`tsmom12-ls` (trend that may go short).** Each tradable coin has an equal slot 1/N: long
  while its 365-day return is positive, short otherwise (instead of cash). Weekly. On P30 and
  on BTC/ETH: 2 variants.
- **Baselines** (logged as `baseline`): `tsmom12` long-only spot at 30 bps (the paper system's
  rule, primary twin), `tsmom12` long-only on perps at 10 bps with funding (same venue), equal
  weight perps. On both books.
- **Blend** (how a market-neutral book would actually be used): 50% of equity in `tsmom12`
  long-only spot, 50% in the long-short book, daily returns averaged (the two sleeves are
  re-split daily at no cost: a small idealisation). Not a separate variant: it is the test of
  each `ls-` variant.

10 variants, 6 baselines; 30 bps reruns logged as `robustness`.

### Pass bars (fixed now)

**`ls-<signal>`** passes train only if all hold:

1. The blend beats `tsmom12` (spot, 30 bps) on Sharpe, paired stationary bootstrap (mean block
   20 days, 2,000 draws) one-sided p < 0.10.
2. The `ls-` book alone has a positive Sharpe in every era with data (2020-21, 2022-25) and
   overall, after 10 bps and funding.
3. The blend's max drawdown is not more than 5 points worse than `tsmom12`'s.
4. The `ls-` book's worst week and max drawdown are reported; it fails if its max drawdown is
   deeper than `tsmom12`'s.
5. It stays ahead (bar 1 at p < 0.20, bar 2 overall) at 30 bps a side.

**`tsmom12-ls`** passes train only if all hold (it replaces the long-only rule, so it is
compared directly):

1. Sharpe beats `tsmom12` long-only spot (30 bps) with bootstrap p < 0.10 AND is not behind
   `tsmom12` long-only on perps (10 bps + funding): the gain must come from the short side, not
   from cheaper fees.
2. Ahead of spot `tsmom12` in every era with data.
3. Max drawdown not more than 5 points worse than spot `tsmom12`'s.

**Held-out year** (2025-11-11 .. 2026-11-09): at most once per survivor, only after a train
pass; passes if not behind its twin there.

### Reported for every shape

Sharpe (365-day, repo convention), CAGR, max drawdown, worst week, per era, funding paid or
received per year, turnover per year, correlation with `tsmom12`, and the number of
independent episodes it rests on: for `ls-` books the number of non-overlapping holding weeks
and the number of drawdown spells deeper than 10%; for `tsmom12-ls` the number of short spells
(runs of a coin's 365-day return below 0, gaps < 30 days merged, spells < 30 days dropped),
per coin and for BTC alone (the coins' downtrends overlap, so BTC's count is the honest one).

### Logging

Every variant, baseline and 30 bps rerun gets one row in `research/tries.md` at the moment it
runs (kind `variant`, `baseline`, `robustness`). Tables: `research/results/short-1.md`. Code:
`research/lib/short1.py` (reuses breadth-1's cached aggregates; streams nothing new).

## Status

**Doing:** card written; code next.
