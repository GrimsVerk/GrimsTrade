# lagcost-1: what execution lag costs each live paper book

Lane `lagcost-1`, 2026-11-24. Descriptive robustness check (how fragile each live rule is to a
delayed fill), not a strategy search: no row here is selectable.

## Question

`docs/DECISIONS.md` (2026-11-24, delayed schedule): the daily job is due 22:30 UTC but GitHub
starts it at 02:00-06:13 UTC the next day. A signal from ETF bar D fills at the D+1 open; a signal
from crypto bar D fills at the D+2 00:00 open, 18-22 hours after the decision. `docs/BACKLOG.md`
proposes a second, crypto-only run just after 00:00 UTC. Before anyone builds it: does the lag
matter, per live book, and does the delayed schedule bias live-vs-backtest comparisons?

## Card (fixed before any number is computed)

**Lag, in bars of the asset's own clock.** A decision whose newest bar of an asset class is bar d
fills that class at the open of bar d+1+k. k = 0 is "fill at the first price after the signal"
(for crypto, 24/7, the open of d+1 is the close of d: Connors' close-of-signal execution). Today,
live and in backtests, ETFs run at k = 0 and coins at k = 1 (a signal from crypto bar d fills at
the open of d+2; DECISIONS 2026-11-12 and 2026-11-24).

**Harness** (`research/lib/lagcost1.py`): one decision per calendar day D, stamped D+1 00:00 UTC
minus 1 microsecond. The strategy (the live `decide` function, unchanged, from
`grimstrade.strategies.LIVE`) sees each ETF's bars dated <= D minus its last k_etf bars, and each
coin's bars dated <= D - k_coin. `gym.simulate` (unchanged) fills each asset at its first open
after the stamp: coins at D+1 00:00, ETFs at the next ETF open. So the newest coin bar seen is
d = D - k_coin and it fills at d+1+k_coin; the newest ETF bar seen is the k_etf-th before the
last ETF bar <= D, and it fills k_etf ETF bars later than at k_etf = 0. Checks (tests, before the
run): (e0, c1) gives exactly the decisions and the equity of `gym.backtest` at 22:30; lag k
delays a planted signal's first fill by exactly k bars of that class; no decision sees a bar that
closes after the earliest fill it can cause.

**Configurations** (each book, each period):
- reference: (e0, c0), both classes at k = 0;
- ETFs only: (e1, c0), (e2, c0), (e5, c0);
- coins only: (e0, c1), (e0, c2), (e0, c5); (e0, c1) is today's backtest schedule (22:30);
- both: (e1, c1), (e2, c2), (e5, c5);
- the live schedule: one decision at 03:00 UTC on D+1 with the gym's own visibility rule (ETF bars
  through D, coin bars through D; coins fill at D+2 00:00, ETFs at D+1 13:30). Not expressible as
  one (e, c) pair: the ETF leg fills before the coin leg and each decision pairs ETF and coin bars
  of the same date.
A configuration whose decisions are identical to an earlier one of the same book and period (for
example coin lags for an ETF-only book) is not run again; the table points to the identical row.

**Books:** all 11 in `LIVE` on `main` at 0ae7104: `buy_hold_btc`, `buy_hold_spy`,
`sixty_forty`, `equal_weight`, `ts_momentum`, `xs_momentum`, `vol_target_spy`, `risk_parity`,
`crypto_mean_reversion`, `preset_careful`, `preset_middle`.

**Data and periods:** the research cache (`research/lib/fetch.py`; the six live assets,
dividend-adjusted ETF prices as in every research run), train only: no bar after 2025-11-10 is
loaded (`harness.load_history("train")`). Primary test: decisions 1994-02-01..2025-11-09. Coin
period: decisions 2012-01-02..2025-11-09 (the project's usual coin window; BTC bars from
2012-01-01, ETH from 2016-05-18). Gym costs as on `main` (Kraken taker tiers + 5 bps for coins,
2 bps for ETFs, 1% band). Cash earns nothing (protocol convention; a paired comparison of the
same book hardly depends on it).

**Metrics:** Sharpe (daily returns, 365 days, zero risk-free rate), CAGR, worst loss (maximum
drawdown), turnover per year (`report.score`). Against the reference (e0, c0), on the same days:
paired Sharpe difference with its stationary-bootstrap SE (1,000 resamples, mean block 20 days,
seed 0) and 95% interval, and the paired CAGR difference with its 95% interval.

**Logging:** every run gets a row in `research/tries.md` as `robustness`, idea = the book's live
name, variant `lag-e<k>-c<k>` or `sched-0300` (tagged `@coin` for the coin period). Robustness
rows are not selectable, so N for a new pick does not change. Project-wide context, quoted from
`research/register/BAR.md` (rows through 2026-11-19 00:30): 3,130 distinct tries, N for a new pick
1,032, effectively 486 independent; a new pick needs z >= 4.69 over `tsmom12` (Bonferroni
p <= 1.0e-04). Nothing here is a pick, so that bar is not applied.

**Decision rules (fixed now):**
1. A crypto-only early run (BACKLOG) is worth building only if, for `crypto_mean_reversion` (the
   one live crypto-only book whose result can depend on timing; `buy_hold_btc` only enters
   once), going from c1 to c0 recovers at least +0.10 Sharpe with the 95% interval above zero on
   both the primary test and the coin period. Otherwise: not worth building now. Also reported:
   the Sharpe and CAGR recovered, with intervals, for every book. Caveat stated in advance: an
   early run at about 00:15 UTC would reach c0 only if the gym were allowed to fill at a price
   after the run (an hourly bar or a quote); under today's rule (first bar open after the
   decision) a 00:15 run still fills at D+2 00:00. c0 is therefore the most such a run could
   recover.
2. The scoreboard should carry a note on the delayed schedule if, for any book, the live schedule
   (sched-0300) differs from the backtest schedule (e0, c1) by |dSharpe| >= 0.05 or
   |dCAGR| >= 0.5 points a year, or the 95% interval of either excludes zero.

## Results (run 2026-11-24, `main` at 0ae7104 + this branch)

Tables: [`results/lagcost-1.md`](results/lagcost-1.md) (one table per book and period, every
configuration) and [`results/lagcost-1-burn30.md`](results/lagcost-1-burn30.md) (the same runs
re-scored, not re-logged, with the paired statistics started 30 days after the first decision;
see "Deviation" below). 157 `robustness` rows in `tries.md` (11 books x 2 periods, identical
curves logged once). Tests: `tests/test_lagcost1.py` (27 cases, all pass).

### Per book

Sharpe, CAGR and worst loss at the reference (e0-c0) and at today's schedule (e0-c1), and the
paired Sharpe difference (bootstrap SE) of a few lags against e0-c0. "0" columns are books
that do not hold that asset class (identical curves). Full grid and 95% intervals in the results
file.

| Book | Period | Sharpe e0-c0 / e0-c1 | CAGR e0-c0 / e0-c1 | Worst loss e0-c0 / e0-c1 | Turnover/yr | dSharpe (SE): e1-c0 | e0-c1 | e0-c2 | e0-c5 | e5-c5 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_btc | primary | 0.87 / 0.87 | +37.1% / +37.1% | 84.9% / 84.9% | 0.00 | 0 | +0.000 (0.000) | +0.000 (0.000) | +0.000 (0.000) | +0.000 (0.000) |
| buy_hold_spy | primary | 0.63 / 0.63 | +10.7% / +10.7% | 55.2% / 55.2% | 0.01 | +0.000 (0.000) | 0 | 0 | 0 | +0.000 (0.000) |
| sixty_forty | primary | 0.77 / 0.77 | +8.2% / +8.2% | 30.5% / 30.5% | 0.47 | +0.000 (0.000) | 0 | 0 | 0 | +0.000 (0.000) |
| equal_weight | primary | 1.01 / 1.01 | +22.1% / +22.1% | 66.7% / 66.7% | 1.52 | +0.000 (0.002) | +0.000 (0.002) | -0.002 (0.004) | -0.001 (0.007) | -0.005 (0.008) |
| ts_momentum | primary | 1.09 / 1.09 | +13.8% / +13.8% | 28.4% / 28.4% | 4.31 | +0.027 (0.019) | -0.002 (0.012) | -0.017 (0.013) | -0.022 (0.016) | +0.021 (0.032) |
| xs_momentum | primary | 0.94 / 0.94 | +31.3% / +31.3% | 77.6% / 77.4% | 3.66 | +0.000 (0.003) | +0.001 (0.003) | -0.005 (0.004) | -0.012 (0.007) | -0.020 (0.009) |
| vol_target_spy | primary | 0.74 / 0.74 | +7.4% / +7.4% | 33.4% / 33.4% | 3.93 | -0.016 (0.013) | 0 | 0 | 0 | -0.018 (0.025) |
| risk_parity | primary | 0.83 / 0.82 | +12.1% / +12.0% | 62.0% / 62.0% | 0.58 | -0.001 (0.003) | -0.003 (0.003) | +0.002 (0.004) | -0.003 (0.004) | +0.007 (0.011) |
| crypto_mean_reversion | primary | 0.09 / 0.04 | +0.2% / -0.6% | 39.5% / 58.3% | 6.71 | 0 | -0.048 (0.090) | -0.137 (0.123) | +0.179 (0.135) | +0.179 (0.135) |
| preset_careful | primary | 0.95 / 0.95 | +9.2% / +9.3% | 22.0% / 22.0% | 4.76 | +0.051 (0.023) | +0.006 (0.005) | +0.001 (0.005) | +0.007 (0.006) | +0.058 (0.034) |
| preset_middle | primary | 1.02 / 1.03 | +13.9% / +14.1% | 30.9% / 30.9% | 4.90 | +0.034 (0.019) | +0.010 (0.010) | -0.011 (0.009) | -0.013 (0.016) | +0.025 (0.030) |
| buy_hold_btc | coin | 1.31 / 1.31 | +104.1% / +104.1% | 84.9% / 84.9% | 0.00 | 0 | +0.000 (0.000) | +0.000 (0.000) | +0.000 (0.000) | +0.000 (0.000) |
| buy_hold_spy | coin | 0.91 / 0.91 | +14.8% / +14.8% | 33.7% / 33.7% | 0.02 | +0.000 (0.000) | 0 | 0 | 0 | +0.000 (0.000) |
| sixty_forty | coin | 0.93 / 0.93 | +9.6% / +9.6% | 27.3% / 27.3% | 0.49 | +0.000 (0.000) | 0 | 0 | 0 | +0.000 (0.000) |
| equal_weight | coin | 1.44 / 1.45 | +39.7% / +39.7% | 47.7% / 47.8% | 1.55 | +0.000 (0.000) | +0.001 (0.003) | +0.001 (0.005) | +0.003 (0.009) | +0.003 (0.009) |
| ts_momentum | coin | 1.57 / 1.55 | +19.2% / +19.3% | 20.1% / 20.0% | 4.45 | +0.017 (0.029) | -0.018 (0.027) | -0.056 (0.031) | -0.072 (0.041) | -0.068 (0.054) |
| xs_momentum | coin | 1.29 / 1.29 | +67.0% / +67.1% | 77.7% / 77.4% | 3.65 | +0.001 (0.001) | +0.002 (0.005) | -0.008 (0.007) | -0.020 (0.011) | -0.020 (0.011) |
| vol_target_spy | coin | 1.00 / 1.00 | +10.1% / +10.1% | 13.3% / 13.3% | 3.87 | -0.056 (0.018) | 0 | 0 | 0 | -0.062 (0.046) |
| risk_parity | coin | 1.43 / 1.42 | +16.8% / +16.7% | 29.9% / 29.8% | 0.60 | -0.017 (0.010) | -0.012 (0.011) | -0.012 (0.011) | -0.018 (0.012) | -0.014 (0.012) |
| crypto_mean_reversion | coin | 0.14 / 0.07 | +0.4% / -1.3% | 39.5% / 58.3% | 15.11 | 0 | -0.073 (0.131) | -0.208 (0.188) | +0.271 (0.199) | +0.271 (0.199) |
| preset_careful | coin | 1.25 / 1.27 | +9.1% / +9.3% | 12.4% / 12.2% | 5.01 | +0.028 (0.042) | +0.020 (0.017) | +0.007 (0.015) | +0.024 (0.018) | -0.026 (0.070) |
| preset_middle | coin | 1.41 / 1.43 | +20.0% / +20.4% | 23.7% / 23.9% | 5.11 | +0.019 (0.029) | +0.021 (0.020) | -0.029 (0.020) | -0.033 (0.036) | -0.029 (0.050) |

On the primary test the two coin-only books hold cash until 2012, which dilutes their Sharpe;
the coin period is the one to read for them. Turnover per year is per calendar year of the test,
so it is lower on the primary test for the same reason.

What it shows:
- **Lag barely matters for ten of the eleven books.** Every difference against e0-c0 is under
  0.075 Sharpe in point estimate (crypto_mean_reversion aside; largest -0.072, `ts_momentum`
  with a 5-bar coin delay on 2012-2025), most under 0.02. CAGR moves under 1 point a year except
  `xs_momentum` with a 5-bar coin delay on 2012-2025 (-1.67 points, of a CAGR of 67%). Of 128 paired comparisons with a non-zero SE, 6 have a 95% interval
  that excludes zero, about what chance gives (6.4 expected at 5%), and 3 of the 6 say a delay
  *helped* (ETF lag 1 on the presets, primary test). The interval is two-sided and the
  comparisons are correlated, so none of the six is a finding on its own.
- The clearest cost of delay: `vol_target_spy` with a one-bar ETF delay on 2012-2025, -0.056
  Sharpe (SE 0.018; 95% -0.091..-0.022), -0.49 CAGR points a year; -0.016 (SE 0.013) on the
  primary test. A one-month volatility signal is the most perishable input among the live
  books. ETFs already fill at k = 0, so nothing follows from it.
- Trend books (`ts_momentum`, presets, `xs_momentum`) lose at most 0.02-0.07 Sharpe from a
  2-5 bar coin delay on 2012-2025; their 12-month and 6-month signals do not care about a day.
- **`crypto_mean_reversion` is the only timing-sensitive book, and its lag curve is noise.**
  Coin period: Sharpe 0.14 at c0, 0.07 at c1 (today), -0.07 at c2, 0.41 at c5. A real
  short-horizon edge would decay with delay; this one goes down, then up above the start. SEs
  are 0.13-0.20, so the whole curve is within about 1.5 SE of zero. Worst loss 39.5% at c0,
  58.3% at c1.

### Recommendation 1: the crypto-only early run (BACKLOG) is not worth building now

Rule 1 (card) fails. For `crypto_mean_reversion`, c1 -> c0 recovers (from the summary table;
the 30-day burn-in re-score gives the same to 0.001):

| Period | dSharpe (95%) | dCAGR, points a year (95%) |
|---|---:|---:|
| primary 1994-2025 | +0.048 (-0.113..+0.235) | +0.74 (-1.84..+3.56) |
| coin 2012-2025 | +0.073 (-0.172..+0.340) | +1.70 (-4.10..+7.84) |

Below the +0.10 asked and both intervals include zero (and include losses as large as the
gain). `buy_hold_btc` recovers nothing (it only enters once). For the mixed books a run before
00:00 UTC for all books (e0-c0 against today's live schedule) would recover between -0.022 and
+0.019 Sharpe, every interval across zero. Two more reasons against: an early run at about 00:15
UTC reaches c0 only if the gym may fill at a price after the run (an hourly bar or a quote);
under today's rule (first bar open after the decision) it still fills at D+2 00:00, so the
build would include a gym change. And BACKLOG says re-timing a live strategy is a new try under
a new name, which adds to N. Keep the BACKLOG line with a pointer to this file; revisit only if a
live coin rule with a short signal and a positive train Sharpe at c1 appears.

### Recommendation 2: the scoreboard needs no bias note for the delayed schedule

Live schedule (decision at 03:00 UTC the next day) minus today's backtest schedule (22:30), per
book, after the first 30 days: |dSharpe| <= 0.004 and |dCAGR| <= 0.27 points a year on both
periods, every 95% interval across zero (`results/lagcost-1-burn30.md`, last two columns).
For ETF-only and coin-only books the two schedules give the same trades (identical in bars, as
DECISIONS says); for the mixed books the ETF-leg-before-coin-leg ordering costs nothing
measurable. So comparing the live record with 22:30 backtests is fair.

One exception, and it is a start effect only: a book that starts from cash enters coins one day
later on the live schedule (its first decision fills at D+2). Over the full window (no burn-in)
this shows up once, in `buy_hold_btc` on 2012-2025: +0.92 CAGR points a year, from one day of
2012 BTC; read literally, rule 2 (card) triggers on that row. It is one day, and it no longer
shows after the first 30 days. A scoreboard line is only worth it while the live record is
weeks long, if anyone compares a book's first days with a backtest: "live runs start
02:00-06:13 UTC; a first coin entry fills one day later than a 22:30 backtest". Optional, not
required by the data.

### Deviation from the card

The card did not say the paired statistics drop a burn-in. The first run (as carded) is in
`results/lagcost-1.md` and its rows are the logged ones. The 30-day burn-in re-score
(`--burn 30 --no-log`, nothing logged again) was added after seeing the `buy_hold_btc`
first-entry effect; elsewhere it changes no Sharpe difference by more than 0.007 and no CAGR
difference by more than 0.3 points a year (`equal_weight`, c5, 2012-2025). Both readings are
given above.
