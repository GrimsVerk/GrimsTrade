# Scoreboard

Forward paper trading on real prices, fake money (10,000 USD start per strategy). Fills at the next open after each decision, after fees and slippage.

| Strategy | Since | Days | Equity (USD) | Return | Beats yardsticks | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2026-11-11 | 4 | 10,003 | +0.0% | - | - | - | 0.4% | 91.15 |
| vol_target_spy | 2026-11-12 | 3 | 10,001 | +0.0% | 3 of 4 | - | - | 0.2% | 55.02 |
| crypto_mean_reversion | 2026-11-12 | 3 | 10,000 | +0.0% | 3 of 4 | - | - | 0.0% | 0.00 |
| ts_momentum | 2026-11-12 | 3 | 9,999 | -0.0% | 3 of 4 | - | - | 0.3% | 40.53 |
| preset_careful | 2026-11-13 | 2 | 9,968 | -0.3% | 3 of 4 | - | - | 0.3% | 60.20 |
| preset_middle | 2026-11-13 | 2 | 9,959 | -0.4% | 2 of 4 | - | - | 0.4% | 73.31 |
| sixty_forty | 2026-11-11 | 4 | 9,933 | -0.7% | - | - | - | 0.7% | 91.62 |
| xs_momentum | 2026-11-12 | 3 | 9,912 | -0.9% | 2 of 4 | - | - | 1.6% | 121.97 |
| risk_parity | 2026-11-12 | 3 | 9,862 | -1.4% | 2 of 4 | - | - | 1.4% | 122.80 |
| equal_weight | 2026-11-11 | 4 | 9,708 | -2.9% | - | - | - | 2.9% | 92.69 |
| buy_hold_btc | 2026-11-11 | 4 | 9,170 | -8.3% | - | - | - | 8.3% | 95.65 |

Rows started on different days, and Return runs from each row's own start: compare rows by "Beats yardsticks" (each yardstick restarted with fresh cash at that row's start), not by Return.

Prices through: BTC 2026-11-13, ETH 2026-11-13, SPY 2026-11-13, QQQ 2026-11-13, GLD 2026-11-13, TLT 2026-11-13.

Strategies tried so far (the record's plus the research lane's): 296. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 296 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 6.5 after six months, 4.6 after one year, 2.6 after three and 2.0 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.

Stored bars whose source later showed other prices: 3 (largest difference 0.01%). The stored values are kept; details in `data/revisions.jsonl`.
