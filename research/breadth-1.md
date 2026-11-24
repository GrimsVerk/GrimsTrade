# Breadth 1: do weak signals pay on a wide book or at a higher frequency?

Research run breadth-1, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-breadth-1.md`.
Branch `breadth-1` (from `info-1`). Research only: no live change. Held-out year not loaded
unless a candidate passes on train (then once).

Question: every run so far says the six-asset weekly book has no usable information beyond the
12-month trend (best weekly IC ~0.05; `rl-3.md`, `info-1.md`). A weak signal's value grows with
the square root of the number of independent bets (the "fundamental law": IR ~ IC x sqrt(bets
per year)). Does a wide cross-section (many coins, 33 markets) or a higher frequency (hourly
BTC/ETH) turn a weak signal into a gain over `tsmom12`-style baselines after costs?

## In plain words (results, 2026-11-13)

**Breadth helped in one place only. Frequency did not help anywhere.** Of about 40 signal,
book and frequency combinations, one passed the card's bar: in a wide coin book (the 100
largest coins on each date, coins that later died included), favouring the third of coins whose
trading volume is small relative to their market cap (`turnover`), inside the same trend rule,
lifted Sharpe from 0.72 to 1.06 after 30 bps costs (2019-2025). Drawdown was shallower too (54%
against 64%). It held at 100 bps a side, on the top 50 coins and in the held-out year (0.61
against 0.31). **But this is not a reason to widen the crypto slot.** Over nearly the same years,
plain `tsmom12` on BTC alone made about 1.16 (Binance, 2020-2025), more than the wide book with
the tilt. The tilt only repairs part of the drag that altcoins put on a wide book. Everything else
either has no information or has information too weak to beat 30 bps. Tables:
`results/breadth-1.md`.

- **Wide coin book (Coin Metrics, 306 coins over time, ~89 a date, from 2019-03).**
  - `turnover`: weekly IC +0.060 (t 5.1), daily +0.039 (t 9.1). Both halves of the sample
    agree. Weekly `TOP-TS` against `TS`: +0.34 Sharpe (bootstrap p < 0.01), ahead in both eras
    with data. A random-score placebo run through the same test never got above +0.18 (99th
    percentile +0.15). Not stale prices (0.2% zero-return days). It overlaps partly with low
    volatility (rank correlation 0.44).
  - Real but too weak to pay after the trend rule: `low_vol` (IC +0.08, t 6.1; less volatile
    coins do better) and `size` (IC -0.05, t -4.3: *large* coins beat small ones, the opposite of
    the card's direction, so the "small" tilt lost). One- to four-week momentum is slightly
    *negative* (IC -0.01 to -0.02), not the positive effect papers report for earlier years.
    On-chain address growth: nothing (34 coins have it).
- **The 30 Binance pairs (liquid survivors, from 2020).** The same pattern in the ICs (`turnover`
  +0.076, `low_vol` +0.10, `size` -0.075, funding and premium +0.025 to +0.043), but no tilt beats
  the trend rule after costs. That includes `turnover` (-0.03), so the wide-book result doesn't
  carry over to the 21 liquid coins a day that are actually easy to trade. Funding and premium carry
  real daily information (t ~4.7), but a long-only tilt pays more in costs than it earns.
- **33 markets (ETFs, sectors, indexes, coins, 2000-2025).** Nothing. The best is
  cross-sectional 12-1 momentum (IC +0.017 to +0.025), and on top of the trend rule it loses Sharpe.
  The time-series trend already holds what cross-sectional momentum knows here.
- **Hourly BTC/ETH (Bitstamp 2011+, Binance 2017+).** The last hour's move partly reverses in
  the next hour (IC -0.06 to -0.09, chance ~0.006), on both venues and both coins: real, and the
  strongest information found in any run. But a walk-forward model that trades only when the
  24-hour forecast clears a 30 bps band trails daily `tsmom12` on all four series (BTC -0.04 to
  -0.07, ETH -0.3 to -0.4). Even at 10 bps it is not ahead. Across the 30 pairs the hourly reversal
  has IC 0.06, and a long-only tilt would need about 0.58 to beat 30 bps. The costs are ten times
  the edge.
- **How sure.** Sure about the misses on the 33 markets and the hourly rules: long samples, and
  the gaps are clear. Moderately sure `turnover` is real information in the wide coin book: t 5,
  placebo, held-out and cost checks all agree. Not sure it is money. It rests on 6.6 years (two
  eras), on Coin Metrics' *reported* volume (which includes wash trading, so the signal may be
  "avoid coins with inflated volume"), and it vanished in the liquid Binance subset.

### What this means for the owner's choices

1. **Universe.** Don't widen the traditional book for signal reasons: 33 markets add nothing over
   the trend rule. Widening crypto to many coins makes the trend book *worse* than BTC (and ETH)
   with the trend rule (wide `TS` 0.72 and wide `TOP-TS` 1.06 from 2019-03; BTC `tsmom12` 1.16 on
   Binance from 2020; the spans differ by nine months).
2. **Crypto slot.** If the owner ever wants alts, the evidence says: keep the trend filter,
   prefer large, calmer coins with low turnover, and expect no better than BTC. The paper venues
   (Kraken, Coinbase) don't list many of the top-100 coins, which is a second reason not to.
3. **Short side.** Most information found here is relative: low-vol beats high-vol, large beats
   small, high funding underperforms, the last hour reverses. A long-only book can use only half
   of that, and these runs cannot say how much a short side would add (borrow and funding costs
   were not modelled). If the owner wants that answer, it is the next card, on perpetuals, with
   funding costs.
4. **Cheaper execution matters more than more signals** for the daily and hourly information.
   Every gross gain found at daily frequency was eaten by 30 bps.

### What to feed the RL agent next

Not the six-asset agent: the one survivor is a cross-sectional coin feature, and it does not
exist on a six-asset book. If RL runs again, the only lead is a **coin-book agent**: weights over
the top 50 coins, the trend rule as the residual base (as rl-2), `turnover` and `low_vol` as
inputs, and rl-3's planted-signal gate first. That needs its own environment and card. It was
not run here: it is too big for the remaining budget, and the plain `TOP-TS` rule already shows
the size of the prize (+0.3 Sharpe over wide `TS`, still below BTC's trend rule).

## Card (written 2026-11-13 ~07:50 UTC, before any number below was computed)

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

### Disclosures (2026-11-13)

- **Departures from the card, found while building, before any measure was computed:** Coin
  Metrics has market-cap estimates for most small coins only from 2019, so book A starts
  2019-03-31 (the first day 30 coins pass), not in the early 2010s. Binance book starts
  2020-01-30 and book B 1999-12-22 (the first day 10 assets are eligible: the IC and tilt need 10
  a date). Book B fills: weekly decisions on Friday fill at Monday's close (3 days later), daily
  decisions Monday to Thursday fill at the next day's close. The card left this open, and using
  the decision's own close would have been kind.
- Each book was run once with `--log` (rows in `tries.md`). Before that, only coverage was printed
  (asset counts, start dates, how many coins later died; no IC, no return). Book C had a plumbing
  smoke test (row counts only) before its logged run.
- After the logged runs: formatting, the rolling helpers moved to `breadth_xs.py` (the test must
  not import `harness`, which changes the global asset list), and `cm_book` got `top_n` and
  `last` parameters for the checks. Defaults unchanged, no logic change.
- Survivor checks were chosen after seeing the result and are logged as `robustness`. The
  placebo is logged as a `control`. The held-out year was looked at once, for weekly `turnover`
  only (the daily twin is the same signal; it was not looked at). A marker file blocks a
  second look.
- `size`'s IC is negative: large coins did better. The card fixed the tilt as "long small", and it
  was not re-run reversed. A reversed tilt would be a new, post-hoc idea.
- The turnover column in the tables is target-weight turnover (drift ignored). Costs in the returns
  include drift.
- Coinbase and Bitfinex 1-minute files were not used (budget). Bitstamp and Binance are the two
  venues.
- Book C's first walk-forward fit: Bitstamp BTC 2014-01-01, the others 2020-01-01 (two full years
  of data first).

## Status (2026-11-13 ~08:01 UTC)

**Done:** card; `lib/breadth_agg.py` (1-minute files to hourly, cached outside the repo);
`lib/breadth_xs.py` (IC, tilt engine, rolling helpers; `tests/test_breadth_xs.py`);
`lib/breadth_books.py` (books A, A2, B); `lib/breadth_hf.py` (book C, hourly cross-section);
`lib/breadth_robust.py` (survivor checks, held-out once); `results/breadth-1.md`; rows in
`tries.md`; this write-up. Draft PR #22 (`breadth-1` -> `info-1`).

**Doing:** nothing half-finished. No process left running.

**Next (not started, owner's choice):** a short-side card on perpetuals with funding costs
(low-vol, size, funding and reversal are relative signals), or a coin-book RL agent with rl-3's gate
(see above). Neither is worth it while the paper system stays on BTC/ETH with long-only trend.

Reproduce: `uv run python -I research/lib/breadth_agg.py all`, then
`uv run python -I research/lib/breadth_books.py cm|binance|trad`,
`uv run python -I research/lib/breadth_hf.py` and `research/lib/breadth_robust.py` (`--log`
writes `tries.md` rows: once only). Needs the shared cache (`research/macro.local.json`) and
`research/data` (copied read-only from the info-1 worktree).
