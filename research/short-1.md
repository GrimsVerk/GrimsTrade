# Short 1: what would a short side on perpetuals add?

Research run short-1, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-short-1.md`.
Branch `short-1` (from `breadth-1`). Research only: the gym and the live system are not
changed. Fake money only; nothing here can reach an exchange account.

Question: most information found so far is relative (low-vol beats high-vol, large beats small,
high funding underperforms, yesterday reverses). A long-only book can use only half of it. On
Binance USDT perpetuals, after fees, slippage and the funding every position pays or receives,
does a short side add a gain worth its risk over `tsmom12` long-only on the same coins?

## In plain words (results, 2026-11-13)

**No. On these coins and these years, a short side does not add a gain worth its risk, and
nothing passed the card.** Tables: `results/short-1.md`. 10 variants were run, none passed;
the held-out year was not looked at (it is still unspent).

- **`tsmom12` that goes short in downtrends instead of cash loses.** Sharpe 0.73 against 0.88
  for long-only on the same perps and 1.03 for long-only on spot (30 coins, 2020-2025); on
  BTC/ETH alone 0.76 against 0.98 and 1.19. Shorting a coin whose 12-month return is negative
  lost money: downtrends end in sharp rallies, and the rule sits short through them. It also
  rests on very little: BTC had only **2** downtrend spells in these six years (90 counting
  every coin, but those overlap heavily).
- **Perpetuals are an expensive place to be long.** Longs paid funding in almost every month of
  the bull years: about **11-13% of equity a year** for `tsmom12` and equal weight on perps
  (BTC/ETH 12.9%). Same rule, same coins: spot at 30 bps beats perps at 10 bps by 0.15-0.2
  Sharpe. Any plan that moves the long book onto perps to make shorting possible pays this.
- **The "relative" signals do not survive being turned into long-short books.** `low_vol`,
  `size` (large over small), `turnover` and the combination of the four all have a positive
  long-only rank IC (t 3-5), yet as market-neutral books they lost 17-28% a year (Sharpe -0.3 to
  -0.6). The legs show why: the long legs earn (Sharpe 0.6-0.8 alone), but the short legs, which
  hold the most volatile, smallest, most-traded coins, lost 43-48% a year, three quarters or more of that in
  2020-21 when those coins rose most. A dollar-neutral book that is long calm coins and short
  wild ones is net short the market's beta, and in a crypto bull market that swamps a rank
  edge. Rank IC counts how often the order is right; a short book pays for the size of the
  rare 10x coin it is short. The daily one-day reversal is hopeless at any cost (483x turnover).
- **The one near miss is a carry trade: short the coins whose perpetual is most expensive.**
  `ls-premium` (long the third with the lowest 7-day premium, short the highest; `ls-funding` is
  nearly the same book) made Sharpe 0.83 at 10 bps, positive in both eras, almost uncorrelated
  with `tsmom12` (0.08). Half of equity in it and half in spot `tsmom12` lifted Sharpe from 1.03 to
  1.25 (p 0.096) and cut the drawdown from 62% to 34%. It fails the card because it does not hold
  at 30 bps (blend +0.10, p 0.28): it trades 40x a year, so costs eat a third of it. Its short
  leg still lost money (-26% a year) despite collecting about 19% a year in funding on the short
  notional: the gain is the long leg plus the funding, not prices falling. Its worst week was
  -30% and its drawdown 49% at gross 1, so this is not a calm book either.
- **How sure.** Sure that a short-capable trend rule and dollar-neutral low-vol/size books lose
  here: the gaps are large and both eras agree. Not sure about the premium/funding carry: it
  rests on 5.7 years, one exchange, 30 coins that all survived (which makes shorting look worse,
  not better), spot prices standing in for perp prices, and directions chosen after breadth-1
  had seen the long-only ICs on the same data. It is a lead, not a result.

### What this means for the owner's choices

1. **Don't add a short side to the paper system now.** The simplest version (short in
   downtrends) is worse than cash, and the market-neutral books that use the "relative"
   information mostly lose. The paper system's long-only BTC/ETH trend on spot remains the best
   rule measured (Sharpe 1.19 on BTC/ETH 2020-2025).
2. **If a short side is ever wanted, the only shape with evidence is a funding/premium carry
   book**, sized small next to the trend book, and only with cheap execution (<= 10 bps a side)
   or slower trading. Its clean test is still available: the held-out year 2025-11 .. 2026-11
   has never been looked at for it. A new card could fix the rule (as above, plus perhaps a
   slower rebalance written before the look) and spend that year once.
3. **Do not move the long book to perpetuals** to make room for shorts: funding costs the long
   side ~12% a year in bull markets.

### What the gym would need (described, not built)

- **Signed weights.** `gym.validate` rejects weights < 0 and sums > 1. A short side needs
  weights in [-1, 1] with sum of |w| <= 1 (gross limit; the card's shapes never borrow), and a
  separate instrument per perp (`BTC-PERP`) so spot and perp positions never net silently.
- **Funding as a cash flow.** Every 8 hours (some coins 4): `cash -= weight x equity x rate` for
  each open perp position, from a funding-rate history appended like the bars (the ledger needs
  a funding row per event or per day, append-only). Shorts receive positive funding.
- **Perp prices.** Mark price or perp klines, not spot (this run used spot; the gap is the
  premium). Fills at the next open of the perp bar, fee 5 bps taker + slippage.
- **Margin and liquidation.** Cross-margin equity check every bar: if equity falls below the
  maintenance margin (about 0.5-1% of notional on Binance for small positions) the position is
  closed at the bar's worst price plus a liquidation fee. At gross <= 1 this never triggers
  unless a short coin rises > ~90% within a bar; the gym should still model it.
- **Data source in paper.** The paper venues (Kraken, Coinbase spot) do not offer these
  perpetuals for every coin; the runner would need a public, keyless funding and mark-price feed.
  Fake money only: nothing would place an order anywhere.
- **Benchmarks and ledger.** A short book's scoreboard should show funding paid/received and
  gross exposure next to the return, and compare against the long-only twin.

### What it means for the RL agent

A short side widens the agent's action from "weights in [0, 1], sum <= 1" to "weights in
[-1, 1], gross <= 1": twice the range, plus funding as a state input and a cost in the reward.
On this evidence the extra range would mostly give the agent new ways to lose: the only short
exposure that paid was the carry book's, and its edge (premium/funding as a cross-sectional
input) needs about 20 coins, not the six-asset book. rl-3's gate (plant a known signal first)
would have to pass on the wider action before any training run. Not recommended now.

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

### Disclosures (2026-11-13)

- One logged run (`short1.py --log`), then one logged diagnostic after seeing it (`--legs --log`:
  each long-short book split into its legs, kind `robustness`, nothing selectable). No rerun,
  nothing tuned. The pass bars were not changed after the result.
- While writing the engine's test, before any logged run, a bug was found and fixed: the first
  entry's cost was booked on a day the series did not return. breadth-1's `breadth_xs.simulate`
  has the same one-time omission (one entry cost per book, at most 30 bps once over six years);
  its tables were not rerun.
- The Binance funding history in the cache starts 2020-01 (BTCUSDT's perp listed 2019-09), so
  early listings are cut to that date. MKR's perp stops paying funding in 2025-09: it leaves the
  tradable set two days later.
- `ls-premium`'s blend p is 0.0955 (shown as 0.10 in the table).
  It fails bar 5 either way.
- The held-out year was not loaded: no variant passed train.

## Status (2026-11-13 ~08:45 UTC)

**Done:** card; `lib/short_engine.py` (signed weights, funding, tests in
`tests/test_short_engine.py`); `lib/short1.py` (books, shapes, verdicts, legs diagnostic);
`results/short-1.md`; rows in `tries.md`; this write-up. Draft PR #23 (`short-1` ->
`breadth-1`).

**Doing:** nothing half-finished. No process left running.

**Next (owner's choice, not started):** a held-out-only card for the premium/funding carry
book (fix the rule and costs first, spend 2025-11 .. 2026-11 once), or nothing: the paper
system's long-only BTC/ETH trend on spot is still the best rule measured.

Reproduce: `uv run python -I research/lib/short1.py` (add `--log` to write `tries.md` rows: done
once already), then `--legs`. Needs the shared cache (`research/macro.local.json`) with
breadth-1's aggregates under `<cache_root>/derived/breadth-1/`.
