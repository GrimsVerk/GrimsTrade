# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage, T-bill interest on cash). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 716 | 12,266 | +22.7% | 0.46 ±0.7 | 0% | 18.7% | 0.47 |
| crypto_mean_reversion | 2024-12-12 | 716 | 11,467 | +14.7% | 0.35 ±0.7 | 0% | 8.2% | 10.35 |
| vol_target_spy | 2024-12-12 | 716 | 11,433 | +14.3% | 0.33 ±0.7 | 0% | 11.4% | 5.06 |
| sixty_forty | 2024-12-12 | 716 | 11,297 | +13.0% | 0.25 ±0.7 | 0% | 11.2% | 0.81 |
| own_vol_70 | 2024-12-12 | 716 | 10,852 | +8.5% | 0.08 ±0.7 | 0% | 4.4% | 1.15 |
| preset_middle | 2024-12-12 | 716 | 10,729 | +7.3% | 0.00 ±0.7 | 0% | 7.9% | 4.34 |
| ts_momentum | 2024-12-12 | 716 | 10,696 | +7.0% | -0.04 ±0.7 | 0% | 6.4% | 3.98 |
| preset_careful | 2024-12-12 | 716 | 10,576 | +5.8% | -0.10 ±0.7 | 0% | 7.5% | 5.04 |
| risk_parity | 2024-12-12 | 716 | 9,966 | -0.3% | -0.34 ±0.7 | 0% | 13.4% | 1.06 |
| equal_weight | 2024-12-12 | 716 | 9,509 | -4.9% | -0.17 ±0.7 | 0% | 24.8% | 1.49 |
| xs_momentum | 2024-12-12 | 716 | 6,896 | -31.0% | -0.94 ±0.7 | 0% | 41.4% | 2.26 |
| buy_hold_btc | 2024-12-12 | 716 | 5,934 | -40.7% | -0.49 ±0.7 | 0% | 53.1% | 0.58 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-28 | 365 | 10,839 | +8.4% | 0.37 ±1.0 | 0% | 11.4% | 0.94 |
| vol_target_spy | 2025-11-28 | 365 | 10,470 | +4.7% | 0.14 ±1.0 | 0% | 7.4% | 5.78 |
| own_vol_70 | 2025-11-28 | 365 | 10,432 | +4.3% | 0.11 ±1.0 | 0% | 4.4% | 2.20 |
| sixty_forty | 2025-11-28 | 365 | 10,337 | +3.4% | 0.02 ±1.0 | 0% | 6.8% | 1.25 |
| preset_middle | 2025-11-28 | 365 | 10,314 | +3.1% | 0.00 ±1.0 | 0% | 7.9% | 8.26 |
| ts_momentum | 2025-11-28 | 365 | 10,281 | +2.8% | -0.05 ±1.0 | 0% | 6.4% | 7.60 |
| crypto_mean_reversion | 2025-11-28 | 365 | 10,240 | +2.4% | -0.14 ±1.0 | 0% | 3.9% | 8.92 |
| preset_careful | 2025-11-28 | 365 | 10,166 | +1.7% | -0.15 ±1.0 | 0% | 7.5% | 9.63 |
| risk_parity | 2025-11-28 | 365 | 9,580 | -4.2% | -0.48 ±1.0 | 0% | 13.4% | 2.06 |
| equal_weight | 2025-11-28 | 365 | 8,565 | -14.3% | -0.74 ±1.0 | 0% | 20.9% | 1.95 |
| xs_momentum | 2025-11-28 | 365 | 7,418 | -25.8% | -1.07 ±1.0 | 0% | 34.5% | 4.60 |
| buy_hold_btc | 2025-11-28 | 365 | 6,530 | -34.7% | -0.83 ±1.0 | 0% | 39.6% | 1.21 |

Strategies tried so far (the record's plus the research lane's): 4614. Sharpe: daily, 365 days/yr, above what idle cash earned in the gym (the 13-week T-bill rate; zero before the first stored rate, and in the live record a rate counts only from the day after it was stored), with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 4614 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.6 after six months, 5.3 after one year, 3.1 after three and 2.4 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.
