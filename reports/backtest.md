# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 701 | 12,483 | +24.8% | 0.76 ±0.7 | 3% | 19.0% | 0.47 |
| vol_target_spy | 2024-12-12 | 701 | 11,240 | +12.4% | 0.62 ±0.7 | 2% | 11.8% | 5.12 |
| sixty_forty | 2024-12-12 | 701 | 10,936 | +9.4% | 0.45 ±0.7 | 1% | 11.9% | 0.83 |
| preset_middle | 2024-12-12 | 701 | 10,312 | +3.1% | 0.24 ±0.7 | 1% | 7.4% | 4.37 |
| crypto_mean_reversion | 2024-12-12 | 701 | 10,265 | +2.7% | 0.18 ±0.7 | 0% | 9.1% | 10.45 |
| ts_momentum | 2024-12-12 | 701 | 10,213 | +2.1% | 0.20 ±0.7 | 0% | 6.2% | 4.00 |
| equal_weight | 2024-12-12 | 701 | 10,198 | +2.0% | 0.16 ±0.7 | 0% | 23.5% | 1.40 |
| preset_careful | 2024-12-12 | 701 | 10,129 | +1.3% | 0.13 ±0.7 | 0% | 7.8% | 5.04 |
| risk_parity | 2024-12-12 | 701 | 9,751 | -2.5% | -0.08 ±0.7 | 0% | 11.1% | 0.94 |
| xs_momentum | 2024-12-12 | 701 | 7,186 | -28.1% | -0.70 ±0.7 | 0% | 35.2% | 2.17 |
| buy_hold_btc | 2024-12-12 | 701 | 7,087 | -29.1% | -0.20 ±0.7 | 0% | 53.1% | 0.58 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-13 | 365 | 11,376 | +13.8% | 1.02 ±1.0 | 3% | 9.1% | 0.92 |
| vol_target_spy | 2025-11-13 | 365 | 10,632 | +6.3% | 0.61 ±1.0 | 1% | 7.4% | 5.89 |
| sixty_forty | 2025-11-13 | 365 | 10,341 | +3.4% | 0.39 ±1.0 | 1% | 7.0% | 1.29 |
| preset_middle | 2025-11-13 | 365 | 10,312 | +3.1% | 0.34 ±1.0 | 1% | 7.4% | 8.25 |
| ts_momentum | 2025-11-13 | 365 | 10,213 | +2.1% | 0.28 ±1.0 | 0% | 6.2% | 7.59 |
| preset_careful | 2025-11-13 | 365 | 10,129 | +1.3% | 0.18 ±1.0 | 0% | 7.8% | 9.55 |
| risk_parity | 2025-11-13 | 365 | 9,751 | -2.5% | -0.11 ±1.0 | 0% | 11.1% | 1.81 |
| crypto_mean_reversion | 2025-11-13 | 365 | 9,704 | -3.0% | -0.36 ±1.0 | 0% | 5.5% | 8.78 |
| equal_weight | 2025-11-13 | 365 | 9,153 | -8.5% | -0.29 ±1.0 | 0% | 16.7% | 1.83 |
| xs_momentum | 2025-11-13 | 365 | 7,695 | -23.1% | -0.83 ±1.0 | 0% | 27.6% | 4.35 |
| buy_hold_btc | 2025-11-13 | 365 | 7,114 | -28.9% | -0.55 ±1.0 | 0% | 41.7% | 1.31 |

Strategies tried so far (the record's plus the research lane's): 296. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 296 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 6.5 after six months, 4.6 after one year, 2.6 after three and 2.0 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.
