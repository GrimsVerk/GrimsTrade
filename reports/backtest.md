# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 707 | 12,039 | +20.4% | 0.65 ±0.7 | 0% | 19.0% | 0.47 |
| vol_target_spy | 2024-12-12 | 707 | 11,059 | +10.6% | 0.54 ±0.7 | 0% | 11.8% | 5.07 |
| sixty_forty | 2024-12-12 | 707 | 10,728 | +7.3% | 0.37 ±0.7 | 0% | 11.9% | 0.82 |
| crypto_mean_reversion | 2024-12-12 | 707 | 10,265 | +2.7% | 0.18 ±0.7 | 0% | 9.1% | 10.36 |
| preset_middle | 2024-12-12 | 707 | 10,149 | +1.5% | 0.14 ±0.7 | 0% | 7.4% | 4.33 |
| ts_momentum | 2024-12-12 | 707 | 10,078 | +0.8% | 0.09 ±0.7 | 0% | 6.2% | 3.97 |
| preset_careful | 2024-12-12 | 707 | 10,001 | +0.0% | 0.04 ±0.7 | 0% | 7.8% | 4.99 |
| equal_weight | 2024-12-12 | 707 | 9,612 | -3.9% | 0.02 ±0.7 | 0% | 23.5% | 1.40 |
| risk_parity | 2024-12-12 | 707 | 9,419 | -5.8% | -0.26 ±0.7 | 0% | 11.1% | 0.95 |
| xs_momentum | 2024-12-12 | 707 | 6,812 | -31.9% | -0.83 ±0.7 | 0% | 37.0% | 2.17 |
| buy_hold_btc | 2024-12-12 | 707 | 6,255 | -37.5% | -0.34 ±0.7 | 0% | 53.1% | 0.58 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-19 | 365 | 10,849 | +8.5% | 0.65 ±1.0 | 0% | 9.1% | 0.93 |
| vol_target_spy | 2025-11-19 | 365 | 10,374 | +3.7% | 0.39 ±1.0 | 0% | 7.4% | 5.84 |
| preset_middle | 2025-11-19 | 365 | 10,149 | +1.5% | 0.19 ±1.0 | 0% | 7.4% | 8.25 |
| sixty_forty | 2025-11-19 | 365 | 10,102 | +1.0% | 0.15 ±1.0 | 0% | 7.0% | 1.22 |
| ts_momentum | 2025-11-19 | 365 | 10,078 | +0.8% | 0.13 ±1.0 | 0% | 6.2% | 7.59 |
| preset_careful | 2025-11-19 | 365 | 10,001 | +0.0% | 0.05 ±1.0 | 0% | 7.8% | 9.55 |
| crypto_mean_reversion | 2025-11-19 | 365 | 9,704 | -3.0% | -0.36 ±1.0 | 0% | 5.5% | 8.78 |
| risk_parity | 2025-11-19 | 365 | 9,419 | -5.8% | -0.36 ±1.0 | 0% | 11.1% | 1.83 |
| equal_weight | 2025-11-19 | 365 | 8,785 | -12.1% | -0.47 ±1.0 | 0% | 16.8% | 1.86 |
| xs_momentum | 2025-11-19 | 365 | 7,616 | -23.8% | -0.87 ±1.0 | 0% | 29.5% | 4.38 |
| buy_hold_btc | 2025-11-19 | 365 | 6,844 | -31.6% | -0.63 ±1.0 | 0% | 39.6% | 1.21 |

Strategies tried so far (the record's plus the research lane's): 3103. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 3103 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.5 after six months, 5.2 after one year, 3.0 after three and 2.3 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.
