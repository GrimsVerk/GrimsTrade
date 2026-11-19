# trend-age: hold a trend only once it has survived four weeks

Card: `cards/trend-age.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| age4 | 0.99 (0.18) | +16.4% | 16.7% | 37.9% | 1.9 | 71% | 1.33 | 0.19 | 1.49 | 1.33 | 0.81 | -0.06 (p=0.97; -0.11..-0.01) | 0/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| age4 | -22% | -4% | -22% | -12% | -6% | -22% | -18% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## On-spells of the twin's signal (descriptive)

| Asset | On-spells | Ended within 4 weeks | Median length (weeks) |
|---|---:|---:|---:|
| BTC | 7 | 3 | 57 |
| ETH | 9 | 3 | 8 |
| SPY | 23 | 12 | 4 |
| QQQ | 19 | 6 | 19 |
| GLD | 28 | 15 | 4 |
| TLT | 25 | 11 | 10 |

| Age (weeks) | Spells alive | Ended at that age | Weekly hazard |
|---|---:|---:|---:|
| 1 | 111 | 23 | 20.7% |
| 2 | 88 | 13 | 14.8% |
| 3 | 75 | 11 | 14.7% |
| 4 | 64 | 3 | 4.7% |
| 5+ | 3968 spell-weeks | 61 | 1.5% |

## Out of universe

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| age4@etf | 0.60 (0.20) | +4.7% | 8.1% | 17.0% | 1.6 | 58% | +0.00 (p=0.48; -0.09..+0.11) | 3/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| age4@coin | 0.37 (0.34) | +1.6% | 71.6% | 90.8% | 3.4 | 47% | -0.17 (p=0.94; -0.38..+0.01) | 0/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| age4@GSPC | 0.41 (0.19) | +3.9% | 10.5% | 33.2% | 1.1 | 64% | -0.03 (p=0.73; -0.12..+0.05) | 0/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| age4@N225 | 0.53 (0.13) | +6.2% | 13.0% | 45.0% | 1.5 | 60% | -0.02 (p=0.73; -0.07..+0.04) | 2/7 |
| tsmom12@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| age4@FTSE | 0.28 (0.16) | +2.5% | 11.3% | 40.4% | 1.5 | 65% | -0.09 (p=0.97; -0.17..-0.01) | 1/6 |
| tsmom12@FTSE | 0.37 (0.16) | +3.7% | 11.8% | 39.1% | 2.7 | 71% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| age4@GDAXI | 0.47 (0.17) | +6.1% | 14.7% | 55.2% | 1.0 | 65% | +0.08 (p=0.02; +0.02..+0.14) | 5/6 |
| tsmom12@GDAXI | 0.40 (0.17) | +5.0% | 15.1% | 58.9% | 1.8 | 69% | - | - |

## Pass bar (only variant `age4`)

- FAIL: 1. `age4` beats twin `tsmom12` with p < 0.0024 (0.10 / 42) (difference -0.058, p = 0.9675)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (37.9% vs 36.5%)
- FAIL: 4. Positive, and the same sign in at least 2 of 3 out-of-universe sets (etf +0.003, coin -0.168, idx -0.017)
- PASS: 5. Beats equal weight on Sharpe (0.99 vs 0.88)

**FAILS train.**
