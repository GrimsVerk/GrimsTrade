# Info 1: information the trend rule doesn't have (screen, don't trade)

Research run info-1, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-info-1.md`. Branch
`info-1` (from `rl-3`). Descriptive only: no backtest, no strategy, held-out year not loaded.

Question: RL 1-3, macro-1 and run 2 all say prices, macro and three on-chain inputs carry almost
no weekly information beyond the 12-month trend (best single weekly IC ~0.05, all together ~0
walk-forward; `rl-3.md`). Does any **new kind** of information reach the level where it is worth
anything on this book (weekly IC ~0.10, `rl-3.md` ceiling)?

## Card (written 2026-11-13 ~07:55 UTC, before any candidate data was read into a feature)

### Target, rows, period (same as `results/rl-3-inputs.md`)

- Target `z` = `rl3_plant.week_z` on RL 2's `six` table: the log return the Friday decision
  actually holds (first open after Friday to the first open after the next Friday), divided by
  the asset's EWMA vol x sqrt(7/365), clipped to +-5.
- Rows: every Friday 2000-01-07 .. end of train (2025-11-09) and asset of the six that is
  eligible (a year of bars) and has a finite target and a finite feature. Bars after the train
  cut are not loaded (the table stops there).

### As-of rule (macro-1's, made specific per source)

A number is used at the decision on Friday `d` only if it was public by `d - 1` (the day after
publication, as `lib/macro.py`):

- **CFTC COT**: positions as of Tuesday `t`, normally released Friday `t + 3` after the close of
  the US market -> usable from Saturday `t + 4`, i.e. at the Friday decision 10 days after `t`.
  Government shutdowns delayed releases; report dates inside these windows are **dropped** (the
  feature keeps the last earlier report): 2013-10-01..2013-10-29, 2018-12-21..2019-03-05,
  2025-09-30..end. Assumption, noted: release dates outside those windows were on schedule
  (holiday weeks shift a Friday release to Monday at worst; +4 days covers Monday only for
  reports usable from the Friday after anyway, since the next decision is Friday `t + 10`).
- **Market series** (Cboe indexes, Yahoo closes, put/call ratios, AAII): an observation dated
  `x` is used from `x + 1` (Thursday's value at the Friday decision). AAII publishes Thursday
  for the week to Wednesday: used from Friday.
- **Crypto** (Binance funding and premium, Deribit funding and DVOL, Fear & Greed, Coin
  Metrics daily): a row stamped UTC day `x` (or any time inside it) is used from `x + 2`: Coin
  Metrics publishes a day's value during the following UTC day; same rule for all crypto inputs
  for simplicity. Exchange flows are not used (revised attribution, as rl-2).
- A feature value older than 21 days at the decision (45 for monthly-ish data: none here) is
  missing.

### Candidates (fixed now; exact formulas)

Own-asset inputs (each asset gets its own market's number):

- **COT** (CFTC, futures only; markets: E-mini S&P 500 -> SPY, E-mini Nasdaq-100 -> QQQ, US
  Treasury bond -> TLT, gold (COMEX) -> GLD, CME bitcoin -> BTC, CME ether -> ETH; matched by
  CFTC contract code, checked by name in the result):
  `cot_spec` = (non-commercial long - short) / open interest (legacy report);
  `cot_spec_chg4` = `cot_spec` minus its value 4 reports earlier;
  `cot_spec_z3y` = (`cot_spec` - mean of the last 156 reports) / their sd (>= 104 reports);
  `cot_lev` = leveraged funds (long - short) / OI and `cot_am` = asset managers (long - short)
  / OI (Traders in Financial Futures, from 2006-06; not gold).
- **Crypto derivatives** (BTC, ETH only): `fund_bn` = mean Binance USDT-perp funding rate over
  the last 7 days; `prem_bn` = mean Binance premium index (hourly closes) over the last 7 days;
  `fund_drb` = mean Deribit perpetual funding (8h-equivalent) over the last 7 days; `dvol_rv` =
  log(DVOL / 30-day realised vol of the coin's daily closes) (Deribit DVOL; vol from the
  rl table's own closes visible at the decision).
- **On-chain** (Coin Metrics community, BTC and ETH; beyond rl-2's three): `puell` = log(IssTotUSD
  last value / its 365-day mean) (miners' revenue against its year, the "Puell multiple"),
  `hash_growth` = log(30-day / 365-day mean HashRate), `tx_growth` = log(30-day / 365-day mean
  TxCnt), `mcap_sply_act` skipped (not in community). ETH hash rate stops at the merge
  (2022-09-15): missing after (staleness rule).

Common inputs (one number per Friday, the same for every asset; their IC may have a different
sign per asset, which the per-asset slopes below allow):

- **Options / volatility (Cboe)**: `vix_term` = log(VIX / VIX3M); `vix_term6` = log(VIX / VIX6M);
  `skew_z` = (SKEW - mean of the last 252 observations) / sd; `vvix_vix` = log(VVIX / VIX);
  `vrp` = VIX - 100 x SPY's 21-day realised vol (annualised close-to-close, SPY bars of the
  table visible at the decision). Put/call: `pc_total`, `pc_equity` = 10-day mean of Cboe's
  total and equity put/call ratios (if Cboe's free history downloads; it covers about
  2006-2019).
- **Sentiment**: `aaii_bull_bear` = AAII bulls - bears, 4-week mean (only if the file downloads
  without an account or bot check); `fng` = crypto Fear & Greed index (alternative.me) 7-day
  mean / 100 (coins only: it is a crypto index).
- **Cross-asset (Yahoo closes in the cache)**: `usd_13w` = 91-day log return of the dollar
  index (DX-Y.NYB); `oil_13w` = 91-day log return of crude (CL=F); `hy_ief_13w` = 91-day log
  return of HYG minus IEF (credit risk appetite, from 2007).

25 candidates. With that many, the largest |IC| by chance is larger than one test's chance
level; the report lists that too.

### Measures (per candidate)

1. **Coverage**: first date, cells, weeks.
2. **In-sample IC**: Pearson correlation of the feature with `z`, pooled over all cells, and per
   asset. Spearman (rank) IC pooled as a check.
3. **Chance level**: the pooled IC with the feature's weekly series circularly shifted by a
   random offset of 52 weeks or more (same shift for all assets), 500 shifts (seed 0): the 95th
   percentile of |IC| is the chance level. This keeps the feature's own persistence and the
   assets' co-movement, which make 1/sqrt(cells) far too small for slow features.
4. **Walk-forward IC** (rl-3's scheme): ordinary least squares refitted every two years
   (2000, 2002, ..., 2024) on Fridays before `y0 - 1` (a year's gap), predicting `y0 .. y0 + 1`;
   inputs standardised on the training rows. Model: `z ~ asset dummies x feature` (a slope per
   asset, so a common input may help SPY and hurt TLT) and also the pooled single slope. A
   block is skipped if the training rows have fewer than 104 weeks with the feature. IC = the
   correlation of all out-of-sample predictions with `z`.
5. **Overlap with the trend rule's inputs**: the largest |correlation| of the feature with the
   seven trend inputs of `ml.py` (`z7 .. z365`, `up_12m`, `sma_gap`); and the **walk-forward
   gain**: walk-forward IC of `trend inputs + feature` (per-asset feature slopes) minus that of
   the trend inputs alone, on the same rows.

### What counts (fixed now)

- **Useful**: walk-forward IC (per-asset slopes or pooled, the better one; reported which)
  >= 0.10, or a walk-forward gain >= +0.05 over the trend inputs, and in-sample |IC| above its
  chance level. That is the level where `rl-3`'s ceiling shows a real Sharpe gain (+0.16 at 0.10,
  +0.03 at 0.05).
- **Worth a second look**: walk-forward IC >= 0.05 and in-sample |IC| above chance.
- Coin-only and post-2018 candidates have few independent weeks (BTC+ETH, ~300-400 weeks): their
  chance level is large; the report says so rather than calling them found.
- **If one is useful** and budget remains: RL 3's planted-signal gate logic on the real feature
  (residual agent with it vs `tsmom12`), written as its own card first.

### Logging

Every candidate gets a line in `tries.md` (kind `screen`: a descriptive IC row, not a backtest,
not selectable). The IC table goes to `results/info-1.md`. Downloads: `scripts/fetch_info1.py`
into the cache (write-once, manifest), never committed.
