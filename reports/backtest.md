# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 710 | 11,373 | +13.7% | 0.47 ±0.7 | 0% | 19.0% | 0.47 |
| vol_target_spy | 2024-12-12 | 710 | 10,787 | +7.9% | 0.42 ±0.7 | 0% | 11.8% | 5.05 |
| sixty_forty | 2024-12-12 | 710 | 10,437 | +4.4% | 0.24 ±0.7 | 0% | 11.9% | 0.83 |
| crypto_mean_reversion | 2024-12-12 | 710 | 10,265 | +2.7% | 0.18 ±0.7 | 0% | 9.1% | 10.31 |
| preset_middle | 2024-12-12 | 710 | 9,879 | -1.2% | -0.04 ±0.7 | 0% | 8.6% | 4.31 |
| ts_momentum | 2024-12-12 | 710 | 9,856 | -1.4% | -0.08 ±0.7 | 0% | 7.2% | 3.95 |
| preset_careful | 2024-12-12 | 710 | 9,792 | -2.1% | -0.11 ±0.7 | 0% | 8.4% | 4.97 |
| equal_weight | 2024-12-12 | 710 | 9,183 | -8.2% | -0.08 ±0.7 | 0% | 25.3% | 1.40 |
| risk_parity | 2024-12-12 | 710 | 9,105 | -8.9% | -0.42 ±0.7 | 0% | 13.7% | 0.96 |
| xs_momentum | 2024-12-12 | 710 | 6,362 | -36.4% | -0.97 ±0.7 | 0% | 41.5% | 2.16 |
| buy_hold_btc | 2024-12-12 | 710 | 5,967 | -40.3% | -0.39 ±0.7 | 0% | 53.1% | 0.58 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-22 | 365 | 10,407 | +4.1% | 0.35 ±1.0 | 0% | 11.5% | 0.92 |
| vol_target_spy | 2025-11-22 | 365 | 10,242 | +2.4% | 0.27 ±1.0 | 0% | 7.5% | 5.71 |
| sixty_forty | 2025-11-22 | 365 | 9,880 | -1.2% | -0.07 ±1.0 | 0% | 7.3% | 1.27 |
| preset_middle | 2025-11-22 | 365 | 9,879 | -1.2% | -0.06 ±1.0 | 0% | 8.6% | 8.25 |
| ts_momentum | 2025-11-22 | 365 | 9,856 | -1.4% | -0.11 ±1.0 | 0% | 7.2% | 7.59 |
| preset_careful | 2025-11-22 | 365 | 9,792 | -2.1% | -0.16 ±1.0 | 0% | 8.4% | 9.55 |
| crypto_mean_reversion | 2025-11-22 | 365 | 9,704 | -3.0% | -0.36 ±1.0 | 0% | 5.5% | 8.79 |
| risk_parity | 2025-11-22 | 365 | 9,105 | -8.9% | -0.59 ±1.0 | 0% | 13.7% | 1.86 |
| equal_weight | 2025-11-22 | 365 | 8,703 | -13.0% | -0.51 ±1.0 | 0% | 21.0% | 1.84 |
| xs_momentum | 2025-11-22 | 365 | 7,472 | -25.3% | -0.93 ±1.0 | 0% | 34.6% | 4.30 |
| buy_hold_btc | 2025-11-22 | 365 | 7,050 | -29.5% | -0.57 ±1.0 | 0% | 39.6% | 1.12 |

Strategies tried so far (the record's plus the research lane's): 3103. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 3103 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.5 after six months, 5.2 after one year, 3.0 after three and 2.3 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.
