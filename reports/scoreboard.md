# Scoreboard

Forward paper trading on real prices, fake money (10,000 USD start per strategy). Fills at the next open after each decision, after fees and slippage.

| Strategy | Since | Days | Equity (USD) | Return | Beats yardsticks | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| own_vol_70 | 2026-11-25 | 4 | 10,107 | +1.1% | 1 of 4 | - | - | 0.0% | 21.13 |
| crypto_mean_reversion | 2026-11-12 | 17 | 10,002 | +0.0% | 4 of 4 | - | - | 0.0% | 0.00 |
| ts_momentum | 2026-11-12 | 17 | 9,878 | -1.2% | 4 of 4 | - | - | 3.4% | 7.50 |
| preset_careful | 2026-11-13 | 16 | 9,841 | -1.6% | 3 of 4 | - | - | 3.3% | 9.39 |
| vol_target_spy | 2026-11-12 | 17 | 9,831 | -1.7% | 4 of 4 | - | - | 4.0% | 12.44 |
| sixty_forty | 2026-11-11 | 18 | 9,821 | -1.8% | - | - | - | 4.8% | 21.26 |
| preset_middle | 2026-11-13 | 16 | 9,815 | -1.8% | 3 of 4 | - | - | 4.2% | 9.65 |
| buy_hold_spy | 2026-11-11 | 18 | 9,658 | -3.4% | - | - | - | 8.9% | 21.02 |
| risk_parity | 2026-11-12 | 17 | 9,537 | -4.6% | 2 of 4 | - | - | 7.4% | 23.10 |
| xs_momentum | 2026-11-12 | 17 | 9,356 | -6.4% | 2 of 4 | - | - | 12.2% | 23.32 |
| equal_weight | 2026-11-11 | 18 | 9,096 | -9.0% | - | - | - | 12.0% | 22.92 |
| buy_hold_btc | 2026-11-11 | 18 | 8,029 | -19.7% | - | - | - | 21.1% | 23.69 |

Rows started on different days, and Return runs from each row's own start: compare rows by "Beats yardsticks" (each yardstick restarted with fresh cash at that row's start), not by Return.

Prices through: BTC 2026-11-27, ETH 2026-11-27, SPY 2026-11-27, QQQ 2026-11-27, GLD 2026-11-27, TLT 2026-11-27.

Strategies tried so far (the record's plus the research lane's): 4614. Sharpe: daily, 365 days/yr, above what idle cash earned in the gym (the 13-week T-bill rate; zero before the first stored rate, and in the live record a rate counts only from the day after it was stored), with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 4614 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.6 after six months, 5.3 after one year, 3.1 after three and 2.4 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.

Timing: the daily run is scheduled for 22:30 UTC, but GitHub starts it at about 02:00-06:13 UTC the next day. So a strategy that buys coins on its very first decision fills that buy one day later than in a 22:30 backtest started the same day. In 1994-2025 backtests, leaving out each strategy's first 30 days (a cut chosen after seeing the results), the two schedules differed by at most 0.004 Sharpe and 0.27 points of yearly return (`research/lagcost-1.md`).

Stored bars whose source later showed other prices: 3 (largest difference 0.01%). The stored values are kept; details in `data/revisions.jsonl`.
