# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 704 | 12,438 | +24.4% | 0.75 ±0.7 | 3% | 19.0% | 0.47 |
| vol_target_spy | 2024-12-12 | 704 | 11,221 | +12.2% | 0.61 ±0.7 | 2% | 11.8% | 5.09 |
| sixty_forty | 2024-12-12 | 704 | 10,893 | +8.9% | 0.44 ±0.7 | 1% | 11.9% | 0.82 |
| preset_middle | 2024-12-12 | 704 | 10,279 | +2.8% | 0.22 ±0.7 | 1% | 7.4% | 4.35 |
| crypto_mean_reversion | 2024-12-12 | 704 | 10,265 | +2.7% | 0.18 ±0.7 | 0% | 9.1% | 10.40 |
| ts_momentum | 2024-12-12 | 704 | 10,185 | +1.9% | 0.18 ±0.7 | 0% | 6.2% | 3.98 |
| preset_careful | 2024-12-12 | 704 | 10,106 | +1.1% | 0.11 ±0.7 | 0% | 7.8% | 5.01 |
| equal_weight | 2024-12-12 | 704 | 9,874 | -1.3% | 0.08 ±0.7 | 0% | 23.5% | 1.39 |
| risk_parity | 2024-12-12 | 704 | 9,603 | -4.0% | -0.16 ±0.7 | 0% | 11.1% | 0.95 |
| xs_momentum | 2024-12-12 | 704 | 7,031 | -29.7% | -0.75 ±0.7 | 0% | 35.3% | 2.16 |
| buy_hold_btc | 2024-12-12 | 704 | 6,486 | -35.1% | -0.30 ±0.7 | 0% | 53.1% | 0.58 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-16 | 365 | 11,262 | +12.6% | 0.94 ±1.0 | 3% | 9.1% | 0.93 |
| vol_target_spy | 2025-11-16 | 365 | 10,562 | +5.6% | 0.56 ±1.0 | 1% | 7.4% | 5.89 |
| preset_middle | 2025-11-16 | 365 | 10,279 | +2.8% | 0.31 ±1.0 | 1% | 7.4% | 8.25 |
| sixty_forty | 2025-11-16 | 365 | 10,278 | +2.8% | 0.33 ±1.0 | 1% | 7.0% | 1.17 |
| ts_momentum | 2025-11-16 | 365 | 10,185 | +1.9% | 0.25 ±1.0 | 0% | 6.2% | 7.59 |
| preset_careful | 2025-11-16 | 365 | 10,106 | +1.1% | 0.16 ±1.0 | 0% | 7.8% | 9.55 |
| crypto_mean_reversion | 2025-11-16 | 365 | 9,704 | -3.0% | -0.36 ±1.0 | 0% | 5.5% | 8.78 |
| risk_parity | 2025-11-16 | 365 | 9,603 | -4.0% | -0.22 ±1.0 | 0% | 11.1% | 1.83 |
| equal_weight | 2025-11-16 | 365 | 8,937 | -10.6% | -0.39 ±1.0 | 0% | 16.9% | 1.71 |
| xs_momentum | 2025-11-16 | 365 | 7,750 | -22.5% | -0.80 ±1.0 | 0% | 27.6% | 4.30 |
| buy_hold_btc | 2025-11-16 | 365 | 6,890 | -31.1% | -0.62 ±1.0 | 0% | 39.6% | 1.24 |

Strategies tried so far (the record's plus the research lane's): 296. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 296 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 6.5 after six months, 4.6 after one year, 2.6 after three and 2.0 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.
