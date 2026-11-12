# Backtest (hindsight, NOT the record)

The live strategies replayed over the stored price history with the same gym rules (next-open fills, fees, slippage). This is hindsight: the strategies were chosen knowing roughly how such rules did in the past. Only the forward record in `scoreboard.md` counts as evidence.

## All stored history

Strategies that need a year of history sit in cash at first.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2024-12-12 | 700 | 12,527 | +25.3% | 0.77 | 6% | 19.0% | 0.47 |
| vol_target_spy | 2024-12-12 | 700 | 11,259 | +12.6% | 0.63 | 5% | 11.8% | 5.12 |
| sixty_forty | 2024-12-12 | 700 | 11,024 | +10.2% | 0.49 | 3% | 11.9% | 0.83 |
| crypto_mean_reversion | 2024-12-12 | 700 | 11,014 | +10.1% | 0.53 | 3% | 7.9% | 10.58 |
| equal_weight | 2024-12-12 | 700 | 10,408 | +4.1% | 0.21 | 1% | 23.5% | 1.36 |
| ts_momentum | 2024-12-12 | 700 | 10,270 | +2.7% | 0.25 | 1% | 6.1% | 4.02 |
| risk_parity | 2024-12-12 | 700 | 9,900 | -1.0% | -0.00 | 1% | 11.1% | 0.94 |
| buy_hold_btc | 2024-12-12 | 700 | 7,367 | -26.3% | -0.15 | 0% | 53.1% | 0.59 |
| xs_momentum | 2024-12-12 | 700 | 7,277 | -27.2% | -0.67 | 0% | 34.9% | 2.17 |

## Last 365 days

With under two years stored, a strategy needing a year of history may still start this window in cash.

| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe | Max drawdown | Turnover/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| buy_hold_spy | 2025-11-12 | 365 | 11,163 | +11.6% | 0.88 | 5% | 9.1% | 0.94 |
| vol_target_spy | 2025-11-12 | 365 | 10,448 | +4.5% | 0.45 | 2% | 7.4% | 6.07 |
| sixty_forty | 2025-11-12 | 365 | 10,274 | +2.7% | 0.32 | 1% | 7.0% | 1.23 |
| ts_momentum | 2025-11-12 | 365 | 10,270 | +2.7% | 0.34 | 1% | 6.1% | 7.61 |
| crypto_mean_reversion | 2025-11-12 | 365 | 10,015 | +0.1% | 0.06 | 1% | 3.5% | 8.89 |
| risk_parity | 2025-11-12 | 365 | 9,900 | -1.0% | -0.00 | 1% | 11.1% | 1.81 |
| equal_weight | 2025-11-12 | 365 | 9,085 | -9.2% | -0.32 | 0% | 16.4% | 1.87 |
| xs_momentum | 2025-11-12 | 365 | 7,568 | -24.3% | -0.88 | 0% | 27.3% | 4.40 |
| buy_hold_btc | 2025-11-12 | 365 | 7,250 | -27.5% | -0.51 | 0% | 42.6% | 1.33 |

Strategies tried so far (the record's plus the research lane's): 112. Sharpe: daily, 365 days/yr, zero risk-free rate. Deflated Sharpe: how confident we can be that the Sharpe beats the best that luck alone would give across all the strategies tried (Bailey & López de Prado 2014); shown after 30 days.
