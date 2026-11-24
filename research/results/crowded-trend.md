# crowded-trend: halve the book when every asset is in trend

Card: `cards/crowded-trend.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| crowd | 0.98 (0.18) | +14.8% | 15.2% | 28.9% | 3.3 | 62% | 1.34 | -0.02 | 1.41 | 1.57 | 0.78 | -0.07 (p=0.87; -0.16..+0.03) | 1/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| crowd | -28% | -2% | -8% | -13% | -7% | -17% | -20% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Fridays on which the rule halves the book: 451 of 1658 (27%).

## Out of universe

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| crowd@etf | 0.47 (0.20) | +3.3% | 7.4% | 16.2% | 3.8 | 53% | -0.12 (p=0.99; -0.22..-0.03) | 0/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| crowd@coin | 0.59 (0.33) | +20.0% | 66.3% | 91.5% | 5.0 | 47% | +0.05 (p=0.29; -0.10..+0.21) | 1/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| crowd@idx | 0.71 (0.13) | +4.8% | 7.0% | 24.6% | 2.9 | 56% | -0.01 (p=0.62; -0.10..+0.07) | 2/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.7% | 2.3 | 70% | - | - |

## Pass bar (only variant `crowd`)

- FAIL: 1. `crowd` beats twin `tsmom12` with p < 0.0024 (0.10 / 42) (difference -0.068, p = 0.8745)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (1 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (28.9% vs 36.5%)
- FAIL: 4. Positive, and the same sign in at least 2 of 3 out-of-universe sets (etf -0.125, coin +0.055, idx -0.013)
- PASS: 5. Beats equal weight on Sharpe (0.98 vs 0.88)

**FAILS train.**
