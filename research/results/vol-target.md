# vol-target: cap each slot by an absolute volatility budget

Card: `cards/vol-target.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs equal-weight (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| t40 | 0.87 (0.18) | +14.2% | 16.8% | 66.5% | 1.9 | 95% | 1.36 | 0.04 | 1.78 | 1.69 | 0.77 | -0.01 (p=0.54; -0.10..+0.08) | 5/5 |
| t25 | 0.94 (0.18) | +12.8% | 13.8% | 57.8% | 1.7 | 89% | 1.37 | 0.11 | 1.77 | 1.86 | 0.82 | +0.06 (p=0.23; -0.07..+0.18) | 5/5 |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | - | - |
| inverse-vol | 0.85 (0.18) | +12.4% | 15.1% | 61.1% | 0.7 | 100% | 1.35 | 0.10 | 1.69 | 1.87 | 0.87 | -0.03 (p=0.63; -0.19..+0.12) | 4/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| t40 | -66% | -17% | -16% | -33% | -4% | -27% | -35% |
| t25 | -58% | -13% | -12% | -26% | +0% | -18% | -27% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |
| inverse-vol | -61% | -10% | -14% | -27% | +11% | -9% | -27% |

Annualised log growth: t40 +13.3%, t25 +12.0%, equal-weight +16.7%, inverse-vol +11.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs equal-weight@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| t40@etf | 0.52 (0.20) | +6.4% | 13.7% | 36.8% | 0.4 | 99% | 0.49 | 0.46 | 0.73 | 0.50 | +0.03 (p=0.22; -0.03..+0.10) | 2/4 |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | - | - |
| inverse-vol@etf | 0.48 (0.20) | +4.8% | 11.0% | 36.6% | 0.4 | 100% | 0.35 | 0.68 | 0.87 | 0.35 | -0.00 (p=0.49; -0.10..+0.10) | 2/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs equal-weight@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| t40@coin | 0.80 (0.34) | +29.8% | 44.9% | 57.9% | 5.6 | 53% | 1.08 | 0.45 | +0.08 (p=0.24; -0.12..+0.26) | 1/2 |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | - | - |
| inverse-vol@coin | 0.73 (0.34) | +29.1% | 94.9% | 91.7% | 3.5 | 100% | 0.89 | 0.49 | +0.01 (p=0.27; -0.02..+0.04) | 2/2 |

## Out of universe: idx, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs equal-weight@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| t40@idx | 0.62 (0.13) | +7.3% | 12.6% | 58.3% | 0.3 | 100% | 0.70 | 0.99 | 1.11 | -0.07 | 0.65 | 0.58 | 0.93 | +0.01 (p=0.34; -0.01..+0.03) | 1/7 |
| equal-weight@idx | 0.62 (0.13) | +7.5% | 13.1% | 57.6% | 0.2 | 100% | 0.71 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | - | - |
| inverse-vol@idx | 0.60 (0.13) | +7.1% | 12.7% | 56.8% | 0.5 | 100% | 0.59 | 1.04 | 1.18 | -0.07 | 0.63 | 0.65 | 0.96 | -0.01 (p=0.84; -0.04..+0.01) | 4/7 |

## Pass bar (primary variant `t40`)

- FAIL: 1. Sharpe beats twin `equal-weight` with p < 0.10 (difference -0.01, p = 0.54)
- PASS: 2. Ahead of the twin in at least 4 of 5 eras (5 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (66.5% vs 68.8%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf +0.03, coin +0.08, idx +0.01)
- FAIL: 5. Beats equal weight on Sharpe (0.87 vs 0.88)

**FAILS train.**
