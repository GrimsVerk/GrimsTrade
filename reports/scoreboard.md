# Scoreboard

Forward paper trading on real prices, fake money (10,000 USD start per strategy). Fills at the next open after each decision, after fees and slippage.

| Strategy | Since | Days | Equity (USD) | Return | Beats yardsticks | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| crypto_mean_reversion | 2026-11-12 | 11 | 10,000 | +0.0% | 4 of 4 | - | - | 0.0% | 0.00 |
| ts_momentum | 2026-11-12 | 11 | 9,681 | -3.2% | 4 of 4 | - | - | 3.4% | 11.20 |
| preset_careful | 2026-11-13 | 10 | 9,666 | -3.3% | 4 of 4 | - | - | 3.3% | 12.20 |
| vol_target_spy | 2026-11-12 | 11 | 9,614 | -3.9% | 4 of 4 | - | - | 4.0% | 15.25 |
| preset_middle | 2026-11-13 | 10 | 9,582 | -4.2% | 4 of 4 | - | - | 4.2% | 14.91 |
| sixty_forty | 2026-11-11 | 12 | 9,517 | -4.8% | - | - | - | 4.8% | 31.90 |
| risk_parity | 2026-11-12 | 11 | 9,291 | -7.1% | 3 of 4 | - | - | 7.4% | 35.09 |
| buy_hold_spy | 2026-11-11 | 12 | 9,147 | -8.5% | - | - | - | 8.9% | 31.41 |
| xs_momentum | 2026-11-12 | 11 | 8,906 | -10.9% | 1 of 4 | - | - | 12.1% | 35.70 |
| equal_weight | 2026-11-11 | 12 | 8,900 | -11.0% | - | - | - | 11.8% | 33.19 |
| buy_hold_btc | 2026-11-11 | 12 | 8,075 | -19.2% | - | - | - | 21.0% | 34.75 |

Rows started on different days, and Return runs from each row's own start: compare rows by "Beats yardsticks" (each yardstick restarted with fresh cash at that row's start), not by Return.

Prices through: BTC 2026-11-21, ETH 2026-11-21, SPY 2026-11-20, QQQ 2026-11-20, GLD 2026-11-20, TLT 2026-11-20.

Strategies tried so far (the record's plus the research lane's): 3103. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 3103 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.5 after six months, 5.2 after one year, 3.0 after three and 2.3 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.

Stored bars whose source later showed other prices: 3 (largest difference 0.01%). The stored values are kept; details in `data/revisions.jsonl`.
