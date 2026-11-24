# Scoreboard

Forward paper trading on real prices, fake money (10,000 USD start per strategy). Fills at the next open after each decision, after fees and slippage.

| Strategy | Since | Days | Equity (USD) | Return | Beats yardsticks | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| crypto_mean_reversion | 2026-11-12 | 13 | 10,000 | +0.0% | 4 of 4 | - | - | 0.0% | 0.00 |
| ts_momentum | 2026-11-12 | 13 | 9,858 | -1.4% | 4 of 4 | - | - | 3.4% | 9.48 |
| preset_careful | 2026-11-13 | 12 | 9,832 | -1.7% | 4 of 4 | - | - | 3.3% | 11.45 |
| vol_target_spy | 2026-11-12 | 13 | 9,810 | -1.9% | 4 of 4 | - | - | 4.0% | 14.37 |
| sixty_forty | 2026-11-11 | 14 | 9,792 | -2.1% | - | - | - | 4.8% | 27.34 |
| preset_middle | 2026-11-13 | 12 | 9,791 | -2.1% | 3 of 4 | - | - | 4.2% | 12.43 |
| buy_hold_spy | 2026-11-11 | 14 | 9,578 | -4.2% | - | - | - | 8.9% | 26.97 |
| risk_parity | 2026-11-12 | 13 | 9,558 | -4.4% | 2 of 4 | - | - | 7.4% | 29.71 |
| xs_momentum | 2026-11-12 | 13 | 9,379 | -6.2% | 2 of 4 | - | - | 12.1% | 30.26 |
| equal_weight | 2026-11-11 | 14 | 9,177 | -8.2% | - | - | - | 11.8% | 28.53 |
| buy_hold_btc | 2026-11-11 | 14 | 8,227 | -17.7% | - | - | - | 21.0% | 29.98 |

Rows started on different days, and Return runs from each row's own start: compare rows by "Beats yardsticks" (each yardstick restarted with fresh cash at that row's start), not by Return.

Prices through: BTC 2026-11-23, ETH 2026-11-23, SPY 2026-11-23, QQQ 2026-11-23, GLD 2026-11-23, TLT 2026-11-23.

Strategies tried so far (the record's plus the research lane's): 3103. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 3103 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.5 after six months, 5.2 after one year, 3.0 after three and 2.3 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.

Stored bars whose source later showed other prices: 3 (largest difference 0.01%). The stored values are kept; details in `data/revisions.jsonl`.
