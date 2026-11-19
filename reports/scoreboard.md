# Scoreboard

Forward paper trading on real prices, fake money (10,000 USD start per strategy). Fills at the next open after each decision, after fees and slippage.

| Strategy | Since | Days | Equity (USD) | Return | Beats yardsticks | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| crypto_mean_reversion | 2026-11-12 | 8 | 10,000 | +0.0% | 4 of 4 | - | - | 0.0% | 0.00 |
| ts_momentum | 2026-11-12 | 8 | 9,896 | -1.0% | 4 of 4 | - | - | 1.3% | 15.28 |
| preset_careful | 2026-11-13 | 7 | 9,867 | -1.3% | 4 of 4 | - | - | 1.3% | 17.29 |
| vol_target_spy | 2026-11-12 | 8 | 9,856 | -1.4% | 4 of 4 | - | - | 1.6% | 20.77 |
| preset_middle | 2026-11-13 | 7 | 9,836 | -1.6% | 4 of 4 | - | - | 1.7% | 21.09 |
| sixty_forty | 2026-11-11 | 9 | 9,783 | -2.2% | - | - | - | 2.3% | 41.05 |
| buy_hold_spy | 2026-11-11 | 9 | 9,683 | -3.2% | - | - | - | 3.6% | 41.04 |
| risk_parity | 2026-11-12 | 8 | 9,616 | -3.8% | 2 of 4 | - | - | 3.8% | 46.75 |
| xs_momentum | 2026-11-12 | 8 | 9,531 | -4.7% | 2 of 4 | - | - | 5.4% | 46.84 |
| equal_weight | 2026-11-11 | 9 | 9,313 | -6.9% | - | - | - | 6.9% | 42.28 |
| buy_hold_btc | 2026-11-11 | 9 | 8,465 | -15.4% | - | - | - | 15.4% | 45.06 |

Rows started on different days, and Return runs from each row's own start: compare rows by "Beats yardsticks" (each yardstick restarted with fresh cash at that row's start), not by Return.

Prices through: BTC 2026-11-18, ETH 2026-11-18, SPY 2026-11-18, QQQ 2026-11-18, GLD 2026-11-18, TLT 2026-11-18.

Strategies tried so far (the record's plus the research lane's): 3103. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 3103 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.5 after six months, 5.2 after one year, 3.0 after three and 2.3 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.

Stored bars whose source later showed other prices: 3 (largest difference 0.01%). The stored values are kept; details in `data/revisions.jsonl`.
