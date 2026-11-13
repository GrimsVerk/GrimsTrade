# Breadth 1: do weak signals pay on a wide book or at a higher frequency?

Research run breadth-1, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-breadth-1.md`.
Branch `breadth-1` (from `info-1`). Research only: no live change. Held-out year not loaded
unless a candidate passes on train (then once).

Question: every run so far says the six-asset weekly book has no usable information beyond the
12-month trend (best weekly IC ~0.05; `rl-3.md`, `info-1.md`). A weak signal's value grows with
the square root of the number of independent bets (the "fundamental law": IR ~ IC x sqrt(bets
per year)). Does a wide cross-section (many coins, 33 markets) or a higher frequency (hourly
BTC/ETH) turn a weak signal into a gain over `tsmom12`-style baselines after costs?

## Card (written 2026-11-13 ~08:00 UTC, before any number below was computed)

### Periods and data hygiene

- Train only: decisions up to 2025-11-09 (`TRAIN_END`); no bar after 2025-11-10 is loaded.
  Held-out (2025-11-11 .. 2026-11-09): at most once per survivor, only if it passes on train.
- Downloads are read with `python -I`; aggregates (daily and hourly bars, panels) are cached
  under the data root (`<cache_root>/derived/breadth-1/`), never committed.
- Eras reported: 2010-16, 2017-21, 2022-25 (crypto); the protocol's five for the traditional
  book.

### Book A: wide crypto (Coin Metrics, daily, all coins it has)

- **Data.** Coin Metrics community, snapshot `coinmetrics/full/2026-11-13/`, every asset (3,547):
  `PriceUSD`, `CapMrktEstUSD` (fallback `CapMrktCurUSD`), `volume_reported_spot_usd_1d`,
  `AdrActCnt`. Coins that later died are in it (e.g. LUNA, FTT keep a price series); what is
  missing is any coin Coin Metrics never covered or dropped from its catalog (said in the result).
- **As of.** A value stamped UTC day `x` is used only at decisions on `x + 1` or later, and a
  position decided on day `t` earns the return from the price stamped `t + 1` onward (a one-day
  skip; Coin Metrics publishes a day's value during the next day). Conservative for short-term
  reversal; stated.
- **Point-in-time universe** (re-formed at every decision): the coin has a price for at least
  365 days (the protocol's year of bars), its 30-day median reported volume is >= 1M USD and its
  30-day median market cap >= 10M USD; not a stablecoin (90-day annualised vol of daily log
  returns < 20%) and not a wrapper (90-day correlation of daily returns with BTC or ETH > 0.95,
  BTC and ETH themselves kept). The 100 largest by 30-day median market cap that pass. Decisions
  start once 30 coins pass. A coin whose price stops while held is exited at its last price
  (count reported).
- **Signals** (from data the as-of rule allows at `t`; "ret(a, b)" = log price change from day
  `t - a` to `t - b`). The tilt direction is fixed here, from the literature, not from results:
  - `mom_7` = ret(7, 0), long high. `mom_28` = ret(28, 0), long high. `mom_91` = ret(91, 7),
    long high. `mom_365` = ret(365, 28), long high (Liu-Tsyvinski-Wu find 1-4 week momentum in
    coins; 12-1 is the classic).
  - `rev_1` = -ret(1, 0), long high (short-term reversal; daily book only).
  - `size` = -log(7-day mean market cap), long high (small coins).
  - `turnover` = -log(30-day mean volume / market cap), long high (illiquid coins).
  - `vol_growth` = log(7-day mean volume / 91-day mean volume), long high (attention).
  - `low_vol` = -(90-day vol), long high.
  - `addr_growth` = log(30-day / 365-day mean `AdrActCnt`), long high (on-chain growth; only the
    coins that have it).
- **Frequencies.** Weekly: decision every Friday, held 7 days. Daily: decision every day, held
  one day. Both from the same daily panel.

### Book A2: the 30 Binance USDT pairs (spot 1-minute klines)

- **Data.** `binance/spot/monthly/klines/<S>/1m/`, aggregated per file to daily and hourly bars
  (UTC); USDT-perp funding (`fundingRate`) and premium index (`premiumIndexKlines`, 1h) where
  present. Eligible after 365 days of daily bars and 30-day median quote volume >= 5M USD.
- **Survivorship: biased, stated up front.** The 30 pairs were picked in 2026 from today's large
  coins, so every coin in this book survived. Momentum and size results here are flattered;
  Book A (which includes dead coins) is the primary crypto answer, A2 the check that adds
  funding and exact UTC fills.
- **As of.** Bars close on UTC boundaries: a decision at the close of day `t` uses bars through
  `t` and fills at the next bar's open (= `t`'s close, the gym's rule). Funding and premium: the
  rows stamped before the decision's close.
- **Signals.** Book A's (with quote volume instead of reported volume, `size` from Coin Metrics
  market cap where the coin maps, else skipped) plus `funding` = -(7-day mean funding rate),
  long high (crowded longs pay), and `premium` = -(7-day mean premium index), long high.
- **Hourly screen** (IC only, no portfolio): `rev_1h` = -(last hour's return), `mom_24h`,
  against the next hour's return, with the break-even IC the costs imply.

### Book B: run 2's 33-market pooled set

- `ml.POOL_SETS` (six live, 8 other ETFs, 9 sectors, 6 coins, 4 indexes), total-return bars,
  train period, cash 0. A market is eligible once it has a year of bars (protocol). Costs: the
  gym's, 2 bps a side for ETFs and indexes, 30 bps for coins. The S&P 500 index and SPY are both
  in after 1993 (accepted, as in the pooled ML card).
- **Signals** (vol-scaled where the assets differ in risk, as `ml.py`'s `z(h)`: log return over
  the window / (EWMA vol, 60-bar half-life, x sqrt(window/365))): `mom_7`, `mom_28` (long high),
  `rev_7` = -z(7) (reversal; reported as the mirror of `mom_7` and not counted twice),
  `mom_91` = z over days 91..7, `mom_365` = z over days 365..28 (long high), `low_vol` = -vol,
  `high_52w` = log(close / 365-day high close), long high. Weekly and daily decisions.

### Measures (all books, all signals, both frequencies)

1. **IC**: on each decision date, the Spearman rank correlation of the signal with the coming
   holding-period return across the eligible assets (dates with >= 10 assets). Mean IC, its
   t-statistic (mean / sd x sqrt(dates); the holding periods do not overlap), share of dates
   positive, mean IC in each half of the sample.
2. **Tilt portfolios, long only, through costs.** `EW` = equal weight of the eligible set.
   `TOP` = equal weight of the top third by the signal. `TS` = the `tsmom12`-style baseline:
   `EW`'s slots, each held only while the asset's 365-day return is positive, else cash.
   `TOP-TS` = `TOP` with the same trend condition, slot 3 / N (fully invested when every top
   coin trends up). Weights are reset at each decision and drift with prices in between.
   Cost = (cost per side) x sum |weight change| at each decision (drift included). Costs: 30 bps
   a side in crypto (protocol), 2 bps ETFs/indexes, 30 bps the coins in book B. Daily portfolio
   returns, Sharpe on 365 days (repo convention).
3. **Gain over the baseline.** Sharpe of `TOP-TS` minus `TS` and of `TOP` minus `EW`, with a
   paired stationary bootstrap (mean block 20 days, 2,000 draws, seed 0), one-sided p. Per era.
4. **Breakeven**: the cost per side at which `TOP-TS` stops beating `TS` (from the gross and net
   numbers; linear in cost).

### Book C: higher frequency in BTC and ETH

- **Data.** Hourly bars from 1-minute history: Bitstamp BTC/USD 2011-08 .. 2025-11-09 (the
  longest), Bitstamp ETH/USD 2017-08 .., and Binance BTCUSDT/ETHUSDT 2017-08 .. (check venue).
  Coinbase and Bitfinex 1-minute files are a second check only if budget remains (said if not).
- **Features at the close of hour `h`** (bars closed by `h`; each divided by the 30-day EWMA
  hourly vol x sqrt(window)): `r_1h`, `r_4h`, `r_24h`, `r_168h`; `vol_shock` = log(24h realised
  vol / 30-day vol); `volu_shock` = log(24h volume / 30-day mean 24h volume); `hour_mean` = the
  mean next-hour return at that hour of day in all earlier calendar years (none in the first
  year).
- **IC**: hourly Spearman IC of each feature with the next 1h and the next 24h return, pooled
  over the series. Chance level: 1.96 / sqrt(independent periods) for the 24h target uses one
  observation a day.
- **Rule, cost-aware.** Walk-forward OLS of the next-24h vol-scaled return on all seven
  features, refitted on 1 January each year on all earlier hours (24h purge), first fit after two
  years of data. Forecast `f` in log-return units (x vol). Position in {0, 1}, decided every
  hour, filled at the next hour's open: go long when `f > b`, go flat when `f < -b`, otherwise
  keep the position; `b` = 30 bps (`hf-band`). Variant `hf-band-ts`: the same, but only while
  daily `tsmom12` (365-day return > 0 at the last UTC midnight) is on, else flat. Costs 30 bps a
  side; 10 bps reported as robustness only (a Binance taker with fee discount plus ~1 bp spread),
  never for the verdict.
- **Baselines**: buy-and-hold and daily `tsmom12`, same venue, same span, same costs.

### Pass bars (fixed now)

A cross-sectional signal **clears** on a book and frequency only if all hold:

1. Mean rank IC t-statistic >= 3.0 (about 40 signal-book-frequency tests: a Bonferroni-sized bar)
   and the same sign in both halves of the sample.
2. `TOP-TS` beats `TS` on Sharpe after costs, bootstrap p < 0.10.
3. `TOP-TS` ahead of `TS` in a majority of the eras with data.
4. `TOP` beats `EW` on Sharpe after costs (otherwise the gain is only the trend rule's).
5. Max drawdown of `TOP-TS` not more than 5 points worse than `TS`'s.

A higher-frequency rule **clears** if, after 30 bps: its Sharpe beats daily `tsmom12` with
bootstrap p < 0.10 on both BTC venues, it is ahead in a majority of eras, and ETH agrees in sign.

**Weak-but-real** (reported, not a pass): IC t >= 3 with a positive gross tilt that costs erase.
That is information the owner could only use with cheaper execution or a short side.

If something clears and budget remains: the held-out year once for it, then RL 3's gate logic
(residual agent with the input vs `tsmom12`) as its own card. Nothing is tuned after a result;
anything added later is marked as such.

### Logging

Every signal x book x frequency gets one `tries.md` row: kind `screen` for an IC-only row
(hourly screens), `variant` for a tilt (the row shows `TOP-TS`'s Sharpe, return, drawdown,
turnover), `baseline` for `EW`, `TS`, buy-and-hold and daily `tsmom12`, `robustness` for the
10 bps HF run. Tables: `results/breadth-1.md`.
