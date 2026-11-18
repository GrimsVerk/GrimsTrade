# rebalance-pressure: lean against the month-end trades of balanced funds

Card: `cards/rebalance-pressure.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| me | 1.04 (0.18) | +17.7% | 17.0% | 37.3% | 5.4 | 75% | 1.34 | 0.20 | 1.54 | 1.47 | 0.89 | -0.01 (p=0.67; -0.02..+0.01) | 2/5 |
| me-rebound | 1.03 (0.18) | +17.6% | 17.1% | 39.8% | 7.0 | 75% | 1.34 | 0.18 | 1.53 | 1.44 | 0.92 | -0.01 (p=0.83; -0.04..+0.01) | 1/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| me | -28% | -3% | -22% | -13% | -6% | -22% | -20% |
| me-rebound | -28% | -3% | -22% | -13% | -5% | -22% | -19% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Decision days on which `me` differs from `tsmom12`: 1172.

## Event study: SPY minus TLT, open to open, around month ends

| Period | Months | Acted (|g| >= 2%) | Pressure: bps per month, signed against g (t) | Rebound: bps, signed with g (t) | corr(g, window spread), all months |
|---|---:|---:|---:|---:|---:|
| 2003-2013 | 125 | 92 | +56.3 (+1.45) | +62.8 (+2.08) | -0.35 |
| 2014-2025 | 142 | 97 | +21.0 (+0.90) | +13.0 (+0.46) | -0.08 |
| all | 267 | 189 | +38.2 (+1.71) | +37.2 (+1.80) | -0.26 |

Pressure window: bought at the open of T-4, sold at the open of T+1. Rebound window: open of T+1 to open of T+4. A positive number is the sign the card predicts.

## Out of universe: the 8 other ETFs (stocks IWM, EFA, EEM, VNQ; bonds IEF, LQD)

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| me@etf | 0.63 (0.20) | +5.2% | 8.6% | 15.8% | 6.9 | 65% | 0.85 | 0.46 | 0.49 | 0.60 | +0.03 (p=0.14; -0.02..+0.07) | 4/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |

| Period | Months | Acted (|g| >= 2%) | Pressure: bps per month, signed against g (t) | Rebound: bps, signed with g (t) | corr(g, window spread), all months |
|---|---:|---:|---:|---:|---:|
| 2003-2013 | 125 | 89 | +68.4 (+1.68) | +72.1 (+2.49) | -0.50 |
| 2014-2025 | 142 | 74 | +19.7 (+0.88) | -37.5 (-1.70) | -0.05 |
| all | 267 | 163 | +46.3 (+1.90) | +22.4 (+1.17) | -0.40 |

## Pass bar (primary variant `me`)

- FAIL: 1. `me` beats twin `tsmom12` with p < 0.10 (difference -0.005, p = 0.67)
- FAIL: 2. Ahead of the twin in at least 3 of 4 eras (from 2000-09) (2 of 4)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (37.3% vs 36.5%)
- FAIL: 4. Same sign on the one applicable out-of-universe set (ETF set +0.028 (p = 0.14))
- PASS: 5. Beats equal weight on Sharpe (1.04 vs 0.88)
- PASS: 6. (card) Signed window spread positive in 2003-2013 and in 2014-2025 (2003-2013 +56.3 bps, 2014-2025 +21.0 bps)

**FAILS train.**

`me-rebound` against `tsmom12`: -0.014 (p = 0.83), ahead in 1 of 4 eras.
