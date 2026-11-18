# Scoreboard

Forward paper trading on real prices, fake money (10,000 USD start per strategy). Fills at the next open after each decision, after fees and slippage.

| Strategy | Since | Days | Equity (USD) | Return | Beats yardsticks | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| crypto_mean_reversion | 2026-11-12 | 7 | 10,000 | +0.0% | 4 of 4 | - | - | 0.0% | 0.00 |
| ts_momentum | 2026-11-12 | 7 | 9,894 | -1.1% | 4 of 4 | - | - | 1.3% | 17.45 |
| vol_target_spy | 2026-11-12 | 7 | 9,870 | -1.3% | 4 of 4 | - | - | 1.5% | 23.71 |
| preset_careful | 2026-11-13 | 6 | 9,868 | -1.3% | 4 of 4 | - | - | 1.3% | 20.16 |
| preset_middle | 2026-11-13 | 6 | 9,835 | -1.7% | 4 of 4 | - | - | 1.7% | 24.58 |
| sixty_forty | 2026-11-11 | 8 | 9,767 | -2.3% | - | - | - | 2.3% | 46.13 |
| buy_hold_spy | 2026-11-11 | 8 | 9,712 | -2.9% | - | - | - | 3.3% | 46.04 |
| risk_parity | 2026-11-12 | 7 | 9,671 | -3.3% | 2 of 4 | - | - | 3.3% | 53.28 |
| xs_momentum | 2026-11-12 | 7 | 9,561 | -4.4% | 2 of 4 | - | - | 5.1% | 53.35 |
| equal_weight | 2026-11-11 | 8 | 9,433 | -5.7% | - | - | - | 5.7% | 47.33 |
| buy_hold_btc | 2026-11-11 | 8 | 8,719 | -12.8% | - | - | - | 13.8% | 50.18 |

Rows started on different days, and Return runs from each row's own start: compare rows by "Beats yardsticks" (each yardstick restarted with fresh cash at that row's start), not by Return.

Prices through: BTC 2026-11-17, ETH 2026-11-17, SPY 2026-11-17, QQQ 2026-11-17, GLD 2026-11-17, TLT 2026-11-17.

Strategies tried so far (the record's plus the research lane's): 296. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 296 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 6.5 after six months, 4.6 after one year, 2.6 after three and 2.0 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.

Stored bars whose source later showed other prices: 3 (largest difference 0.01%). The stored values are kept; details in `data/revisions.jsonl`.
