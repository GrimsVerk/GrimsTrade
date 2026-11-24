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

## Results

(Written after the run.)
