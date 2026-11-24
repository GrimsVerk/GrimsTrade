# rp-1: `where-rp` (`where-vol` with inverse-vol slot sizes)

Card: `rp-1.md`, step 2 (pushed before any number). Train period only (decisions to 2025-11-09), total-return prices, the gym's fills and protocol costs, cash 0. Twin: `tsmom12`. Context (re-scores of logged configurations): `where-vol`, `inverse-vol`, equal weight. Held-out year not touched.

## Six assets, 1994-2025

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| where-rp | 1.05 (0.18) | +12.4% | 11.8% | 24.5% | 1.4 | 85% | 1.34 | 0.25 | 1.62 | 1.85 | 0.98 | +0.00 (p=0.50; -0.18..+0.19) | 4/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| where-vol | 1.07 (0.18) | +18.9% | 17.5% | 35.3% | 1.7 | 83% | 1.34 | 0.18 | 1.60 | 1.63 | 0.83 | +0.03 (p=0.27; -0.04..+0.10) | 2/5 |
| inverse-vol | 0.85 (0.18) | +12.4% | 15.1% | 61.1% | 0.7 | 100% | 1.35 | 0.10 | 1.70 | 1.87 | 0.87 | -0.20 (p=0.90; -0.45..+0.06) | 3/5 |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| where-rp | -23% | +2% | -13% | -21% | +15% | -4% | -22% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| where-vol | -28% | -4% | -22% | -26% | -3% | -21% | -33% |
| inverse-vol | -61% | -10% | -14% | -27% | +11% | -9% | -27% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## 2022 (the reason for the card)

| Book | Calendar 2022 | Rate shock 2022-01-03..10-12 |
|---|---:|---:|
| where-rp | -19.7% | -21.2% |
| where-vol | -26.6% | -26.9% |
| tsmom12 | -12.8% | -13.7% |
| inverse-vol | -25.2% | -27.6% |
| equal-weight | -36.5% | -37.4% |

Slot contributions, calendar 2022 (points, arithmetic, as in step 1):

| Book | SPY | QQQ | TLT | GLD | BTC | ETH | Sum |
|---|---:|---:|---:|---:|---:|---:|---:|
| where-rp | -3.2 | -3.1 | -8.2 | -0.0 | -5.5 | -0.9 | -21.0 |
| where-vol | -2.4 | -3.1 | -5.9 | +0.1 | -13.7 | -3.6 | -28.6 |
| tsmom12 | -2.4 | -3.1 | -0.8 | -1.4 | -1.4 | -3.6 | -12.7 |

`where-rp` mean invested share 85%; mean coin weight 7.1% from 2013 (`where-vol`: up to 33%).

## Out of universe (rule unchanged, each set one book)

### etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| where-rp@etf | 0.68 (0.20) | +4.3% | 6.5% | 14.2% | 2.3 | 76% | +0.08 (p=0.16; -0.05..+0.22) | 2/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |
| where-vol@etf | 0.65 (0.20) | +5.5% | 8.9% | 16.8% | 2.4 | 71% | +0.05 (p=0.08; -0.01..+0.10) | 3/4 |

### coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| where-rp@coin | 0.61 (0.34) | +20.0% | 77.7% | 91.8% | 4.0 | 58% | +0.08 (p=0.01; +0.02..+0.14) | 2/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | - | - |
| where-vol@coin | 0.61 (0.34) | +19.3% | 78.6% | 92.4% | 3.8 | 59% | +0.07 (p=0.01; +0.02..+0.13) | 1/2 |

### idx, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| where-rp@idx | 0.71 (0.13) | +6.0% | 8.8% | 29.5% | 2.4 | 73% | -0.01 (p=0.66; -0.07..+0.04) | 3/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.7% | 2.3 | 70% | - | - |
| where-vol@idx | 0.72 (0.13) | +6.2% | 9.0% | 27.4% | 2.3 | 72% | -0.00 (p=0.50; -0.04..+0.04) | 3/7 |

## Pass bar

- FAIL: 1. Sharpe beats `tsmom12`, one-sided p < 0.00135 (family 74) (1.05 vs 1.05, difference +0.003, p = 0.4955, 90% range -0.18..+0.19; project-wide bar p <= 4.9e-05: not met)
- PASS: 2. Ahead of `tsmom12` in at least 4 of 5 eras (4 of 5: 1994-99 1.34 vs 1.34, 2000-09 0.25 vs 0.19, 2010-16 1.62 vs 1.55, 2017-21 1.85 vs 1.50, 2022-25 0.98 vs 0.88)
- PASS: 3. Worst loss not more than 5 points deeper (24.5% vs 36.5%)
- PASS: 4. Out of universe: Sharpe up in 2 of 3 sets (etf +0.08, coin +0.08, idx -0.01)
- PASS: 5. Beats equal weight on Sharpe (1.05 vs 0.88)
- PASS: 6. Since 2003 not behind `tsmom12` nor equal weight (1.31 vs 1.20 and 1.19)

**`where-rp` FAILS train.**
