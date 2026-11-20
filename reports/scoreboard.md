# Scoreboard

Forward paper trading on real prices, fake money (10,000 USD start per strategy). Fills at the next open after each decision, after fees and slippage.

| Strategy | Since | Days | Equity (USD) | Return | Beats yardsticks | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| crypto_mean_reversion | 2026-11-12 | 9 | 10,000 | +0.0% | 4 of 4 | - | - | 0.0% | 0.00 |
| ts_momentum | 2026-11-12 | 9 | 9,829 | -1.7% | 4 of 4 | - | - | 2.0% | 13.61 |
| preset_careful | 2026-11-13 | 8 | 9,802 | -2.0% | 4 of 4 | - | - | 2.0% | 15.17 |
| vol_target_spy | 2026-11-12 | 9 | 9,770 | -2.3% | 4 of 4 | - | - | 2.5% | 18.52 |
| preset_middle | 2026-11-13 | 8 | 9,757 | -2.4% | 4 of 4 | - | - | 2.4% | 18.50 |
| sixty_forty | 2026-11-11 | 10 | 9,675 | -3.2% | - | - | - | 3.2% | 37.06 |
| risk_parity | 2026-11-12 | 9 | 9,502 | -5.0% | 3 of 4 | - | - | 5.0% | 41.73 |
| buy_hold_spy | 2026-11-11 | 10 | 9,493 | -5.1% | - | - | - | 5.4% | 37.15 |
| xs_momentum | 2026-11-12 | 9 | 9,349 | -6.5% | 2 of 4 | - | - | 7.2% | 42.36 |
| equal_weight | 2026-11-11 | 10 | 9,181 | -8.2% | - | - | - | 8.2% | 38.26 |
| buy_hold_btc | 2026-11-11 | 10 | 8,321 | -16.8% | - | - | - | 16.8% | 40.91 |

Rows started on different days, and Return runs from each row's own start: compare rows by "Beats yardsticks" (each yardstick restarted with fresh cash at that row's start), not by Return.

Prices through: BTC 2026-11-19, ETH 2026-11-19, SPY 2026-11-19, QQQ 2026-11-19, GLD 2026-11-19, TLT 2026-11-19.

Strategies tried so far (the record's plus the research lane's): 3103. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 3103 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.5 after six months, 5.2 after one year, 3.0 after three and 2.3 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.

Stored bars whose source later showed other prices: 3 (largest difference 0.01%). The stored values are kept; details in `data/revisions.jsonl`.
