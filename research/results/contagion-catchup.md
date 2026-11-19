# contagion-catchup: buy the assets a shock has not reached yet

Card: `cards/contagion-catchup.md`. Protocol: `protocol.md`.

## The 21 ETFs, from 1999-12-22

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs TS@etf21 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catchup@etf21 | 0.50 (0.20) | +4.7% | 10.4% | 21.4% | 47.9 | 66% | 0.46 | 0.65 | 0.57 | 0.15 | -0.11 (p=0.87; -0.26..+0.05) | 1/4 |
| nbr@etf21 | 0.33 (0.20) | +2.7% | 9.6% | 36.8% | 49.4 | 70% | -0.05 | 0.63 | 0.52 | 0.58 | -0.27 (p=0.99; -0.47..-0.08) | 0/4 |
| rev7@etf21 | 0.53 (0.20) | +5.2% | 10.6% | 20.6% | 48.0 | 65% | 0.43 | 0.79 | 0.55 | 0.14 | -0.08 (p=0.76; -0.24..+0.09) | 2/4 |
| TS@etf21 | 0.60 (0.20) | +5.3% | 9.3% | 20.8% | 2.7 | 70% | 0.41 | 0.76 | 0.71 | 0.62 | - | - |
| EW@etf21 | 0.55 (0.20) | +7.5% | 15.4% | 41.5% | 0.2 | 100% | 0.25 | 0.82 | 0.96 | 0.67 | -0.06 (p=0.67; -0.27..+0.16) | 3/4 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catchup@etf21 | -7% | -6% | -18% | -13% | +10% | -2% | -8% |
| nbr@etf21 | -24% | -10% | -17% | -8% | +7% | -9% | -9% |
| rev7@etf21 | -9% | -6% | -19% | -13% | +12% | -3% | -8% |
| TS@etf21 | -16% | -8% | -19% | -8% | +10% | -4% | -6% |
| EW@etf21 | -39% | -41% | -29% | -17% | +10% | -3% | -9% |

Weekly rank IC (signal against the return from the next open to the open a week later, across the eligible ETFs):

| Signal | Weeks | Mean rank IC | t | Share of weeks > 0 | First half | Second half |
|---|---:|---:|---:|---:|---:|---:|
| `catchup` | 1349 | +0.019 | +2.2 | 52% | +0.019 | +0.019 |
| `nbr` | 1349 | -0.015 | -1.4 | 49% | -0.022 | -0.008 |
| `rev7` | 1349 | +0.030 | +2.9 | 54% | +0.034 | +0.026 |

## Out of universe: 8 coins (BTC, ETH and the six other coins), from 2019-08-08

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs TS@coin8 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| catchup@coin8 | 0.38 (0.40) | +2.2% | 69.3% | 70.2% | 46.1 | 56% | 0.61 | 0.12 | -0.36 (p=0.99; -0.65..-0.08) | 0/2 |
| TS@coin8 | 0.74 (0.40) | +29.4% | 59.5% | 64.3% | 4.2 | 57% | 0.98 | 0.51 | - | - |
| EW@coin8 | 0.81 (0.40) | +38.2% | 77.6% | 83.4% | 2.5 | 100% | 1.18 | 0.50 | +0.08 (p=0.31; -0.24..+0.36) | 1/2 |

| Signal | Weeks | Mean rank IC | t | Share of weeks > 0 | First half | Second half |
|---|---:|---:|---:|---:|---:|---:|
| `catchup` | 325 | +0.009 | +0.3 | 48% | +0.014 | +0.003 |
| `nbr` | 325 | +0.024 | +1.0 | 50% | +0.013 | +0.034 |
| `rev7` | 325 | +0.010 | +0.4 | 48% | +0.016 | +0.004 |

## Pass bar (primary variant `catchup`)

- FAIL: 1. `catchup` beats `TS` with p < 0.10 (difference -0.11, p = 0.87)
- FAIL: 2. Ahead of `TS` in at least 3 of 4 eras (1 of 4)
- PASS: 3. Max drawdown not more than 5 points worse than `TS` (21.4% vs 20.8%)
- FAIL: 4. Same sign on the coin set after 30 bps (-0.36 (p = 0.99))
- FAIL: 5. Beats `EW` on Sharpe (0.50 vs 0.55)
- FAIL: 6. Beats `rev7` (plain one-week reversal) on Sharpe (-0.03 (p = 0.71))
- FAIL: 7. Weekly rank IC of `catchup`: t >= 3, positive in both halves (mean +0.019, t +2.2, halves +0.019 / +0.019)

**FAILS train.**

`nbr` against `TS`: -0.27 (p = 0.99), ahead in 0 of 4 eras.
