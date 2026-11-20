# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 708 | 11,803 | +18.0% | 0.58 ±0.7 | 0% | 19.0% | 0.47 |
| vol_target_spy | 2024-12-12 | 708 | 10,962 | +9.6% | 0.50 ±0.7 | 0% | 11.8% | 5.06 |
| sixty_forty | 2024-12-12 | 708 | 10,611 | +6.1% | 0.32 ±0.7 | 0% | 11.9% | 0.82 |
| crypto_mean_reversion | 2024-12-12 | 708 | 10,265 | +2.7% | 0.18 ±0.7 | 0% | 9.1% | 10.34 |
| preset_middle | 2024-12-12 | 708 | 10,064 | +0.6% | 0.08 ±0.7 | 0% | 7.4% | 4.33 |
| ts_momentum | 2024-12-12 | 708 | 10,008 | +0.1% | 0.04 ±0.7 | 0% | 6.2% | 3.96 |
| preset_careful | 2024-12-12 | 708 | 9,933 | -0.7% | -0.01 ±0.7 | 0% | 7.8% | 4.99 |
| equal_weight | 2024-12-12 | 708 | 9,475 | -5.2% | -0.01 ±0.7 | 0% | 23.5% | 1.40 |
| risk_parity | 2024-12-12 | 708 | 9,308 | -6.9% | -0.32 ±0.7 | 0% | 11.5% | 0.94 |
| xs_momentum | 2024-12-12 | 708 | 6,680 | -33.2% | -0.87 ±0.7 | 0% | 38.2% | 2.17 |
| buy_hold_btc | 2024-12-12 | 708 | 6,148 | -38.5% | -0.36 ±0.7 | 0% | 53.1% | 0.58 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-20 | 365 | 10,926 | +9.3% | 0.71 ±1.0 | 0% | 9.1% | 0.91 |
| vol_target_spy | 2025-11-20 | 365 | 10,496 | +5.0% | 0.50 ±1.0 | 0% | 7.4% | 5.74 |
| sixty_forty | 2025-11-20 | 365 | 10,127 | +1.3% | 0.18 ±1.0 | 0% | 7.0% | 1.23 |
| preset_middle | 2025-11-20 | 365 | 10,064 | +0.6% | 0.11 ±1.0 | 0% | 7.4% | 8.25 |
| ts_momentum | 2025-11-20 | 365 | 10,008 | +0.1% | 0.05 ±1.0 | 0% | 6.2% | 7.59 |
| preset_careful | 2025-11-20 | 365 | 9,933 | -0.7% | -0.02 ±1.0 | 0% | 7.8% | 9.55 |
| crypto_mean_reversion | 2025-11-20 | 365 | 9,704 | -3.0% | -0.36 ±1.0 | 0% | 5.5% | 8.78 |
| risk_parity | 2025-11-20 | 365 | 9,308 | -6.9% | -0.44 ±1.0 | 0% | 11.5% | 1.83 |
| equal_weight | 2025-11-20 | 365 | 8,944 | -10.6% | -0.39 ±1.0 | 0% | 17.7% | 1.82 |
| xs_momentum | 2025-11-20 | 365 | 7,752 | -22.5% | -0.81 ±1.0 | 0% | 30.9% | 4.27 |
| buy_hold_btc | 2025-11-20 | 365 | 7,111 | -28.9% | -0.55 ±1.0 | 0% | 39.6% | 1.14 |

Strategies tried so far (the record's plus the research lane's): 3103. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 3103 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.5 after six months, 5.2 after one year, 3.0 after three and 2.3 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.
