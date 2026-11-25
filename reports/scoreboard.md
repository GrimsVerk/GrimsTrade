# Scoreboard

Forward paper trading on real prices, fake money (10,000 USD start per strategy). Fills at the next open after each decision, after fees and slippage.

| Strategy | Since | Days | Equity (USD) | Return | Beats yardsticks | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| crypto_mean_reversion | 2026-11-12 | 14 | 10,000 | +0.0% | 4 of 4 | - | - | 0.0% | 0.00 |
| own_vol_70 | 2026-11-25 | 1 | 10,000 | +0.0% | 0 of 4 | - | - | 0.0% | 0.00 |
| ts_momentum | 2026-11-12 | 14 | 9,818 | -1.8% | 4 of 4 | - | - | 3.4% | 8.81 |
| preset_careful | 2026-11-13 | 13 | 9,802 | -2.0% | 4 of 4 | - | - | 3.3% | 11.55 |
| vol_target_spy | 2026-11-12 | 14 | 9,788 | -2.1% | 4 of 4 | - | - | 4.0% | 15.10 |
| sixty_forty | 2026-11-11 | 15 | 9,754 | -2.5% | - | - | - | 4.8% | 25.53 |
| preset_middle | 2026-11-13 | 13 | 9,744 | -2.6% | 3 of 4 | - | - | 4.2% | 11.48 |
| buy_hold_spy | 2026-11-11 | 15 | 9,531 | -4.7% | - | - | - | 8.9% | 25.20 |
| risk_parity | 2026-11-12 | 14 | 9,454 | -5.5% | 2 of 4 | - | - | 7.4% | 28.02 |
| xs_momentum | 2026-11-12 | 14 | 9,236 | -7.6% | 2 of 4 | - | - | 12.2% | 28.24 |
| equal_weight | 2026-11-11 | 15 | 9,020 | -9.8% | - | - | - | 12.0% | 27.39 |
| buy_hold_btc | 2026-11-11 | 15 | 8,013 | -19.9% | - | - | - | 21.1% | 28.15 |

Rows started on different days, and Return runs from each row's own start: compare rows by "Beats yardsticks" (each yardstick restarted with fresh cash at that row's start), not by Return.

Prices through: BTC 2026-11-24, ETH 2026-11-24, SPY 2026-11-24, QQQ 2026-11-24, GLD 2026-11-24, TLT 2026-11-24.

Strategies tried so far (the record's plus the research lane's): 4158. Sharpe: daily, 365 days/yr, above what idle cash earned in the gym (the 13-week T-bill rate; zero before the first stored rate, and in the live record a rate counts only from the day after it was stored), with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 4158 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.6 after six months, 5.3 after one year, 3.1 after three and 2.4 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.

Stored bars whose source later showed other prices: 3 (largest difference 0.01%). The stored values are kept; details in `data/revisions.jsonl`.
