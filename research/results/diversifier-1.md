# diversifier-1: a held 1/7 merger-arb slot next to `tsmom12`

Card: `cards/diversifier-1.md`. Train only, total-return prices, gym costs. Sharpe daily, 365 days, zero risk-free rate. Era columns are Sharpe ratios. Under water: calendar days below a prior peak.

## Primary: MERFX, 1994-2025

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| merfx7 | 1.09 (0.18) | +16.1% | 14.7% | 30.8% | 2.4 | 79% | 1.42 | 0.25 | 1.55 | 1.52 | 0.92 | +0.04 (p=0.00; +0.03..+0.05) | 5/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

vs `tsmom12`: dSharpe +0.041, bootstrap SE 0.008, z +4.86, one-sided p 0.000. vs equal weight: +0.207 (p 0.035).

| Book | Max DD | Worst year | Longest under water (from) | Share of days under water | 2008 crisis | covid crash | 2022 rate shock | 2020-Q1 (info) | 2022 (info) | dot-com bust (info) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| merfx7 | 30.8% | -18.7% (2000) | 2109 d (2000-03-26) | 91% | -3.7% | -19.3% | -11.5% | -5.6% | -10.9% | -23.3% |
| tsmom12 | 36.5% | -24.2% (2000) | 2227 d (2000-03-26) | 92% | -3.5% | -21.8% | -13.5% | -6.8% | -12.8% | -27.6% |

Weekly correlation of MERFX with SPY +0.48, with `tsmom12` +0.13.

Risk preference (card): smaller max DD True; better in 2 of 3 crash windows; under water not longer True -> **preferred on risk** (a preference, not an edge).

## Robustness: MNA, from 2010-11-17

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| mna7@mna | 1.37 (0.27) | +24.6% | 17.2% | 31.5% | 2.5 | 78% | 1.58 | 1.52 | 0.91 | +0.02 (p=0.05; +0.00..+0.04) | 3/3 |
| tsmom12 | 1.35 (0.27) | +28.1% | 19.9% | 36.5% | 2.8 | 74% | 1.57 | 1.50 | 0.88 | - | - |
| equal-weight | 1.31 (0.26) | +32.0% | 23.4% | 47.0% | 1.3 | 100% | 1.68 | 1.55 | 0.67 | -0.04 (p=0.59; -0.29..+0.20) | 2/3 |

vs `tsmom12`: dSharpe +0.019, bootstrap SE 0.012, z +1.60, one-sided p 0.049. vs equal weight: +0.061 (p 0.337).

| Book | Max DD | Worst year | Longest under water (from) | Share of days under water | 2008 crisis | covid crash | 2022 rate shock | 2020-Q1 (info) | 2022 (info) | dot-com bust (info) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| mna7@mna | 31.5% | -16.1% (2018) | 961 d (2018-01-13) | 91% | - | -19.9% | -11.9% | -6.4% | -11.1% | - |
| tsmom12 | 36.5% | -19.7% (2018) | 1026 d (2018-01-13) | 92% | - | -21.8% | -13.5% | -6.8% | -12.8% | - |

Weekly correlation of MNA with SPY +0.50, with `tsmom12` +0.21.

Risk preference (card): smaller max DD True; better in 2 of 3 crash windows; under water not longer True -> **preferred on risk** (a preference, not an edge).
