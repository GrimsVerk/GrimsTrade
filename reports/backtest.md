# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 705 | 12,200 | +22.0% | 0.69 ±0.7 | 2% | 19.0% | 0.47 |
| vol_target_spy | 2024-12-12 | 705 | 11,124 | +11.2% | 0.57 ±0.7 | 2% | 11.8% | 5.09 |
| sixty_forty | 2024-12-12 | 705 | 10,768 | +7.7% | 0.38 ±0.7 | 1% | 11.9% | 0.82 |
| crypto_mean_reversion | 2024-12-12 | 705 | 10,265 | +2.7% | 0.18 ±0.7 | 0% | 9.1% | 10.39 |
| preset_middle | 2024-12-12 | 705 | 10,183 | +1.8% | 0.16 ±0.7 | 0% | 7.4% | 4.34 |
| ts_momentum | 2024-12-12 | 705 | 10,106 | +1.1% | 0.12 ±0.7 | 0% | 6.2% | 3.98 |
| preset_careful | 2024-12-12 | 705 | 10,032 | +0.3% | 0.06 ±0.7 | 0% | 7.8% | 5.01 |
| equal_weight | 2024-12-12 | 705 | 9,761 | -2.4% | 0.06 ±0.7 | 0% | 23.5% | 1.40 |
| risk_parity | 2024-12-12 | 705 | 9,500 | -5.0% | -0.21 ±0.7 | 0% | 11.1% | 0.95 |
| xs_momentum | 2024-12-12 | 705 | 6,882 | -31.2% | -0.80 ±0.7 | 0% | 36.3% | 2.17 |
| buy_hold_btc | 2024-12-12 | 705 | 6,436 | -35.6% | -0.31 ±0.7 | 0% | 53.1% | 0.58 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-17 | 365 | 11,174 | +11.7% | 0.88 ±1.0 | 2% | 9.1% | 0.92 |
| vol_target_spy | 2025-11-17 | 365 | 10,564 | +5.6% | 0.56 ±1.0 | 1% | 7.4% | 5.85 |
| sixty_forty | 2025-11-17 | 365 | 10,233 | +2.3% | 0.28 ±1.0 | 0% | 7.0% | 1.29 |
| preset_middle | 2025-11-17 | 365 | 10,183 | +1.8% | 0.22 ±1.0 | 0% | 7.4% | 8.25 |
| ts_momentum | 2025-11-17 | 365 | 10,106 | +1.1% | 0.16 ±1.0 | 0% | 6.2% | 7.59 |
| preset_careful | 2025-11-17 | 365 | 10,032 | +0.3% | 0.08 ±1.0 | 0% | 7.8% | 9.55 |
| crypto_mean_reversion | 2025-11-17 | 365 | 9,704 | -3.0% | -0.36 ±1.0 | 0% | 5.5% | 8.78 |
| risk_parity | 2025-11-17 | 365 | 9,500 | -5.0% | -0.30 ±1.0 | 0% | 11.1% | 1.83 |
| equal_weight | 2025-11-17 | 365 | 8,960 | -10.4% | -0.38 ±1.0 | 0% | 16.7% | 1.76 |
| xs_momentum | 2025-11-17 | 365 | 7,676 | -23.2% | -0.84 ±1.0 | 0% | 28.8% | 4.31 |
| buy_hold_btc | 2025-11-17 | 365 | 6,991 | -30.1% | -0.59 ±1.0 | 0% | 39.6% | 1.22 |

Strategies tried so far (the record's plus the research lane's): 296. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 296 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 6.5 after six months, 4.6 after one year, 2.6 after three and 2.0 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.
