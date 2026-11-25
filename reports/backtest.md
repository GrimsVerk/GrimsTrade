# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage, T-bill interest on cash). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 713 | 12,106 | +21.1% | 0.42 ±0.7 | 0% | 18.7% | 0.47 |
| crypto_mean_reversion | 2024-12-12 | 713 | 11,463 | +14.6% | 0.35 ±0.7 | 0% | 8.2% | 10.40 |
| vol_target_spy | 2024-12-12 | 713 | 11,382 | +13.8% | 0.31 ±0.7 | 0% | 11.4% | 5.09 |
| sixty_forty | 2024-12-12 | 713 | 11,219 | +12.2% | 0.23 ±0.7 | 0% | 11.2% | 0.81 |
| own_vol_70 | 2024-12-12 | 713 | 10,801 | +8.0% | 0.03 ±0.7 | 0% | 4.4% | 1.15 |
| preset_middle | 2024-12-12 | 713 | 10,657 | +6.6% | -0.04 ±0.7 | 0% | 7.9% | 4.36 |
| ts_momentum | 2024-12-12 | 713 | 10,630 | +6.3% | -0.08 ±0.7 | 0% | 6.4% | 3.99 |
| preset_careful | 2024-12-12 | 713 | 10,533 | +5.3% | -0.13 ±0.7 | 0% | 7.5% | 5.06 |
| risk_parity | 2024-12-12 | 713 | 9,877 | -1.2% | -0.39 ±0.7 | 0% | 13.4% | 1.06 |
| equal_weight | 2024-12-12 | 713 | 9,431 | -5.7% | -0.19 ±0.7 | 0% | 24.8% | 1.49 |
| xs_momentum | 2024-12-12 | 713 | 6,808 | -31.9% | -0.97 ±0.7 | 0% | 41.4% | 2.27 |
| buy_hold_btc | 2024-12-12 | 713 | 5,921 | -40.8% | -0.49 ±0.7 | 0% | 53.1% | 0.58 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-25 | 365 | 10,714 | +7.1% | 0.29 ±1.0 | 0% | 11.4% | 0.94 |
| vol_target_spy | 2025-11-25 | 365 | 10,435 | +4.3% | 0.11 ±1.0 | 0% | 7.4% | 5.81 |
| own_vol_70 | 2025-11-25 | 365 | 10,386 | +3.9% | 0.05 ±1.0 | 0% | 4.4% | 2.18 |
| preset_middle | 2025-11-25 | 365 | 10,248 | +2.5% | -0.06 ±1.0 | 0% | 7.9% | 8.26 |
| crypto_mean_reversion | 2025-11-25 | 365 | 10,240 | +2.4% | -0.14 ±1.0 | 0% | 3.9% | 8.93 |
| sixty_forty | 2025-11-25 | 365 | 10,230 | +2.3% | -0.08 ±1.0 | 0% | 6.8% | 1.25 |
| ts_momentum | 2025-11-25 | 365 | 10,221 | +2.2% | -0.11 ±1.0 | 0% | 6.4% | 7.59 |
| preset_careful | 2025-11-25 | 365 | 10,128 | +1.3% | -0.18 ±1.0 | 0% | 7.5% | 9.63 |
| risk_parity | 2025-11-25 | 365 | 9,497 | -5.0% | -0.54 ±1.0 | 0% | 13.4% | 2.04 |
| equal_weight | 2025-11-25 | 365 | 8,624 | -13.8% | -0.71 ±1.0 | 0% | 20.8% | 1.95 |
| xs_momentum | 2025-11-25 | 365 | 7,501 | -25.0% | -1.03 ±1.0 | 0% | 34.5% | 4.58 |
| buy_hold_btc | 2025-11-25 | 365 | 6,784 | -32.2% | -0.74 ±1.0 | 0% | 39.6% | 1.16 |

Strategies tried so far (the record's plus the research lane's): 4158. Sharpe: daily, 365 days/yr, above what idle cash earned in the gym (the 13-week T-bill rate; zero before the first stored rate, and in the live record a rate counts only from the day after it was stored), with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 4158 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.6 after six months, 5.3 after one year, 3.1 after three and 2.4 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.
