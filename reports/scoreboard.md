# Scoreboard

Forward paper trading on real prices, fake money (10,000 USD start per strategy). Fills at the next open after each decision, after fees and slippage.

| Strategy | Since | Days | Equity (USD) | Return | Beats yardsticks | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| xs_momentum | 2026-11-12 | 2 | 10,070 | +0.7% | 4 of 4 | - | - | 0.0% | 151.06 |
| buy_hold_spy | 2026-11-11 | 3 | 10,040 | +0.4% | - | - | - | 0.0% | 121.35 |
| ts_momentum | 2026-11-12 | 2 | 10,026 | +0.3% | 3 of 4 | - | - | 0.0% | 60.69 |
| vol_target_spy | 2026-11-12 | 2 | 10,018 | +0.2% | 3 of 4 | - | - | 0.0% | 82.44 |
| crypto_mean_reversion | 2026-11-12 | 2 | 10,000 | +0.0% | 2 of 4 | - | - | 0.0% | 0.00 |
| preset_careful | 2026-11-13 | 1 | 10,000 | +0.0% | 0 of 4 | - | - | 0.0% | 0.00 |
| preset_middle | 2026-11-13 | 1 | 10,000 | +0.0% | 0 of 4 | - | - | 0.0% | 0.00 |
| risk_parity | 2026-11-12 | 2 | 9,972 | -0.3% | 1 of 4 | - | - | 0.3% | 157.31 |
| sixty_forty | 2026-11-11 | 3 | 9,972 | -0.3% | - | - | - | 0.3% | 121.89 |
| equal_weight | 2026-11-11 | 3 | 9,882 | -1.2% | - | - | - | 1.2% | 122.39 |
| buy_hold_btc | 2026-11-11 | 3 | 9,592 | -4.1% | - | - | - | 4.1% | 124.33 |

Rows started on different days, and Return runs from each row's own start: compare rows by "Beats yardsticks" (each yardstick restarted with fresh cash at that row's start), not by Return.

Prices through: BTC 2026-11-12, ETH 2026-11-12, SPY 2026-11-12, QQQ 2026-11-12, GLD 2026-11-12, TLT 2026-11-12.

Strategies tried so far (the record's plus the research lane's): 296. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 296 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 6.5 after six months, 4.6 after one year, 2.6 after three and 2.0 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.

Stored bars whose source later showed other prices: 3 (largest difference 0.01%). The stored values are kept; details in `data/revisions.jsonl`.
