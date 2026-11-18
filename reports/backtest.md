# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 706 | 12,076 | +20.8% | 0.66 ±0.7 | 2% | 19.0% | 0.47 |
| vol_target_spy | 2024-12-12 | 706 | 11,074 | +10.7% | 0.55 ±0.7 | 2% | 11.8% | 5.08 |
| sixty_forty | 2024-12-12 | 706 | 10,711 | +7.1% | 0.36 ±0.7 | 1% | 11.9% | 0.82 |
| crypto_mean_reversion | 2024-12-12 | 706 | 10,265 | +2.7% | 0.18 ±0.7 | 0% | 9.1% | 10.37 |
| preset_middle | 2024-12-12 | 706 | 10,147 | +1.5% | 0.14 ±0.7 | 0% | 7.4% | 4.34 |
| ts_momentum | 2024-12-12 | 706 | 10,077 | +0.8% | 0.09 ±0.7 | 0% | 6.2% | 3.97 |
| preset_careful | 2024-12-12 | 706 | 10,002 | +0.0% | 0.04 ±0.7 | 0% | 7.8% | 5.00 |
| equal_weight | 2024-12-12 | 706 | 9,737 | -2.6% | 0.05 ±0.7 | 0% | 23.5% | 1.40 |
| risk_parity | 2024-12-12 | 706 | 9,474 | -5.3% | -0.23 ±0.7 | 0% | 11.1% | 0.95 |
| xs_momentum | 2024-12-12 | 706 | 6,835 | -31.6% | -0.82 ±0.7 | 0% | 36.7% | 2.17 |
| buy_hold_btc | 2024-12-12 | 706 | 6,443 | -35.6% | -0.31 ±0.7 | 0% | 53.1% | 0.58 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-18 | 365 | 11,082 | +10.8% | 0.82 ±1.0 | 2% | 9.1% | 0.92 |
| vol_target_spy | 2025-11-18 | 365 | 10,532 | +5.3% | 0.53 ±1.0 | 1% | 7.4% | 5.85 |
| sixty_forty | 2025-11-18 | 365 | 10,197 | +2.0% | 0.25 ±1.0 | 0% | 7.0% | 1.29 |
| preset_middle | 2025-11-18 | 365 | 10,147 | +1.5% | 0.19 ±1.0 | 0% | 7.4% | 8.25 |
| ts_momentum | 2025-11-18 | 365 | 10,077 | +0.8% | 0.13 ±1.0 | 0% | 6.2% | 7.59 |
| preset_careful | 2025-11-18 | 365 | 10,002 | +0.0% | 0.05 ±1.0 | 0% | 7.8% | 9.55 |
| crypto_mean_reversion | 2025-11-18 | 365 | 9,704 | -3.0% | -0.36 ±1.0 | 0% | 5.5% | 8.78 |
| risk_parity | 2025-11-18 | 365 | 9,474 | -5.3% | -0.32 ±1.0 | 0% | 11.1% | 1.83 |
| equal_weight | 2025-11-18 | 365 | 8,888 | -11.1% | -0.42 ±1.0 | 0% | 16.6% | 1.83 |
| xs_momentum | 2025-11-18 | 365 | 7,546 | -24.5% | -0.90 ±1.0 | 0% | 29.2% | 4.38 |
| buy_hold_btc | 2025-11-18 | 365 | 6,933 | -30.7% | -0.61 ±1.0 | 0% | 39.6% | 1.23 |

Strategies tried so far (the record's plus the research lane's): 296. Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014). Both are shown after 30 days; before that they mean nothing. The deflated Sharpe is strict: with 296 strategies tried, 95% needs a Sharpe ratio (return for the risk taken) above about 6.5 after six months, 4.6 after one year, 2.6 after three and 2.0 after five; a very good strategy has about 1. A low number is not a verdict against a strategy; it says the record is still too short.
