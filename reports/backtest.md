# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage, T-bill interest on cash). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 715 | 12,071 | +20.7% | 0.41 ±0.7 | 0% | 18.7% | 0.47 |
| crypto_mean_reversion | 2024-12-12 | 715 | 11,466 | +14.7% | 0.35 ±0.7 | 0% | 8.2% | 10.36 |
| vol_target_spy | 2024-12-12 | 715 | 11,373 | +13.7% | 0.30 ±0.7 | 0% | 11.4% | 5.07 |
| sixty_forty | 2024-12-12 | 715 | 11,241 | +12.4% | 0.23 ±0.7 | 0% | 11.2% | 0.81 |
| own_vol_70 | 2024-12-12 | 715 | 10,796 | +8.0% | 0.03 ±0.7 | 0% | 4.4% | 1.15 |
| preset_middle | 2024-12-12 | 715 | 10,639 | +6.4% | -0.05 ±0.7 | 0% | 7.9% | 4.35 |
| ts_momentum | 2024-12-12 | 715 | 10,619 | +6.2% | -0.09 ±0.7 | 0% | 6.4% | 3.99 |
| preset_careful | 2024-12-12 | 715 | 10,524 | +5.2% | -0.14 ±0.7 | 0% | 7.5% | 5.05 |
| risk_parity | 2024-12-12 | 715 | 9,912 | -0.9% | -0.37 ±0.7 | 0% | 13.4% | 1.07 |
| equal_weight | 2024-12-12 | 715 | 9,468 | -5.3% | -0.18 ±0.7 | 0% | 24.8% | 1.49 |
| xs_momentum | 2024-12-12 | 715 | 6,785 | -32.1% | -0.98 ±0.7 | 0% | 41.4% | 2.27 |
| buy_hold_btc | 2024-12-12 | 715 | 5,997 | -40.0% | -0.48 ±0.7 | 0% | 53.1% | 0.58 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-27 | 365 | 10,632 | +6.3% | 0.24 ±1.0 | 0% | 11.4% | 0.95 |
| vol_target_spy | 2025-11-27 | 365 | 10,393 | +3.9% | 0.07 ±1.0 | 0% | 7.4% | 5.78 |
| own_vol_70 | 2025-11-27 | 365 | 10,379 | +3.8% | 0.04 ±1.0 | 0% | 4.4% | 2.20 |
| crypto_mean_reversion | 2025-11-27 | 365 | 10,240 | +2.4% | -0.14 ±1.0 | 0% | 3.9% | 8.92 |
| preset_middle | 2025-11-27 | 365 | 10,228 | +2.3% | -0.07 ±1.0 | 0% | 7.9% | 8.26 |
| ts_momentum | 2025-11-27 | 365 | 10,208 | +2.1% | -0.13 ±1.0 | 0% | 6.4% | 7.60 |
| sixty_forty | 2025-11-27 | 365 | 10,207 | +2.1% | -0.11 ±1.0 | 0% | 6.8% | 1.25 |
| preset_careful | 2025-11-27 | 365 | 10,117 | +1.2% | -0.19 ±1.0 | 0% | 7.5% | 9.63 |
| risk_parity | 2025-11-27 | 365 | 9,529 | -4.7% | -0.52 ±1.0 | 0% | 13.4% | 2.05 |
| equal_weight | 2025-11-27 | 365 | 8,547 | -14.5% | -0.75 ±1.0 | 0% | 20.8% | 1.98 |
| xs_momentum | 2025-11-27 | 365 | 7,310 | -26.9% | -1.13 ±1.0 | 0% | 34.4% | 4.60 |
| buy_hold_btc | 2025-11-27 | 365 | 6,573 | -34.3% | -0.81 ±1.0 | 0% | 39.6% | 1.22 |

Strategies tried so far (the record's plus the research lane's): 4614. Sharpe: daily, 365 days/yr, above what idle cash earned in the gym (the 13-week T-bill rate; zero before the first stored rate, and in the live record a rate counts only from the day after it was stored), with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 4614 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 7.6 after six months, 5.3 after one year, 3.1 after three and 2.4 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.
