# patch-leaving: leave an asset when its trend is below the average

Card: `cards/patch-leaving.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| mvt | 0.85 (0.19) | +18.6% | 23.2% | 53.2% | 9.7 | 76% | 1.34 | 0.02 | 1.10 | 1.42 | 0.60 | -0.19 (p=0.97; -0.36..-0.02) | 0/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| mvt | -41% | +0% | -17% | -15% | -9% | -23% | -21% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Assets held on an average invested Friday: 2.1 (twin 3.1). Average weight in BTC and ETH: 10.5% (twin 9.2%).

## Out of universe

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mvt@etf | 0.54 (0.20) | +4.8% | 9.6% | 20.1% | 8.7 | 65% | -0.06 (p=0.73; -0.22..+0.10) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mvt@coin | 0.14 (0.35) | -17.1% | 78.6% | 97.4% | 10.0 | 55% | -0.39 (p=1.00; -0.56..-0.25) | 0/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mvt@idx | 0.66 (0.13) | +6.6% | 10.4% | 33.3% | 9.2 | 70% | -0.06 (p=0.80; -0.17..+0.05) | 2/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.7% | 2.3 | 70% | - | - |

## Pass bar (only variant `mvt`)

- FAIL: 1. `mvt` beats twin `tsmom12` with p < 0.0024 (0.10 / 42) (difference -0.194, p = 0.9685)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (53.2% vs 36.5%)
- FAIL: 4. Positive, and the same sign in at least 2 of 3 out-of-universe sets (etf -0.057, coin -0.393, idx -0.059)
- FAIL: 5. Beats equal weight on Sharpe (0.85 vs 0.88)

**FAILS train.**
