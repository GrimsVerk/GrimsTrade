# yield-curve: step aside for a year after an inversion

Card: `cards/yield-curve.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| curve-and | 1.13 (0.18) | +15.7% | 13.7% | 29.9% | 2.1 | 60% | 1.39 | 0.57 | 1.55 | 1.61 | -0.10 | +0.08 (p=0.24; -0.11..+0.28) | 4/5 |
| curve-alone | 0.97 (0.18) | +15.8% | 16.5% | 47.8% | 2.0 | 69% | 1.40 | 0.19 | 1.65 | 1.48 | -0.06 | -0.08 (p=0.70; -0.32..+0.17) | 2/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| curve-and | -2% | +4% | +2% | -9% | -6% | -22% | -15% |
| curve-alone | -43% | -22% | +2% | -9% | -17% | -43% | -15% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: curve-and +14.6%, curve-alone +14.7%, tsmom12 +16.4%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| curve-and@etf | 0.55 (0.20) | +3.6% | 7.0% | 16.3% | 2.2 | 50% | 0.61 | 0.44 | 0.80 | 0.54 | -0.05 (p=0.67; -0.26..+0.16) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| curve-and@coin | 0.47 (0.34) | +9.6% | 70.1% | 89.6% | 2.5 | 33% | 0.65 | -0.05 | -0.07 (p=0.65; -0.36..+0.18) | 1/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

## Out of universe: GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| curve-and@GSPC | 0.27 (0.19) | +2.1% | 9.1% | 34.8% | 1.6 | 51% | 0.25 | 0.31 | -0.17 (p=0.94; -0.35..+0.01) | 0/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | 0.26 | 0.62 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.05 (p=0.38; -0.18..+0.25) | 2/2 |

## Out of universe: N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| curve-and@N225 | 0.54 (0.13) | +5.8% | 11.6% | 38.0% | 1.5 | 46% | 0.68 | 0.66 | 0.23 | 0.76 | 0.24 | 0.64 | 0.54 | -0.00 (p=0.52; -0.11..+0.11) | 3/7 |
| tsmom12@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | 0.77 | 0.72 | 0.35 | 0.33 | 0.24 | 0.54 | 0.81 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.15 (p=0.94; -0.31..+0.01) | 3/7 |

## Out of universe: FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| curve-and@FTSE | 0.36 (0.16) | +3.1% | 9.6% | 42.0% | 1.9 | 50% | 0.43 | 0.84 | 0.41 | -0.07 | 0.24 | 0.45 | -0.01 (p=0.51; -0.16..+0.15) | 4/6 |
| tsmom12@FTSE | 0.37 (0.16) | +3.7% | 11.8% | 39.1% | 2.7 | 71% | 0.64 | 0.72 | 0.36 | -0.07 | -0.02 | 0.20 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.01 (p=0.43; -0.18..+0.20) | 5/6 |

## Out of universe: GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| curve-and@GDAXI | 0.51 (0.17) | +5.2% | 11.3% | 34.8% | 1.3 | 45% | 0.69 | 1.15 | 0.63 | 0.42 | 0.14 | -0.84 | +0.11 (p=0.18; -0.09..+0.34) | 4/6 |
| tsmom12@GDAXI | 0.40 (0.17) | +5.0% | 15.1% | 58.9% | 1.8 | 69% | 0.62 | 0.68 | 0.46 | 0.42 | -0.47 | 0.44 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | +0.07 (p=0.30; -0.14..+0.28) | 5/6 |

## Pass bar (primary variant `curve-and`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference +0.08, p = 0.24)
- PASS: 2. Ahead of the twin in at least 4 of 5 eras (4 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (29.9% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.05, coin -0.07, idx -0.02)
- PASS: 5. Beats equal weight on Sharpe (1.13 vs 0.88)

**FAILS train.**

## Since 2003 (the review's window)

| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |
|---|---:|---:|---:|---:|
| curve-and | 1.17 | +17.5% | 29.9% | -0.02 (0.59) |
| curve-alone | 1.14 | +19.6% | 47.8% | -0.05 (0.66) |
| tsmom12 | 1.20 | +20.7% | 36.5% |  |
| equal-weight | 1.19 | +24.9% | 47.0% | -0.00 (0.51) |

- FAIL: 6. Not behind `tsmom12` on Sharpe 2003-2025 (1.17 vs 1.20)

**Card verdict (bars 1-6): FAILS train.**

## Hostile spells (independent episodes)

- `curve`, 1962-1993: 2 spells, 23% of days: 1978-08..1983-07, 1988-12..1991-04
- `curve`, 1994-2025: 5 spells, 31% of days: 1998-05..1999-07, 2000-02..2001-12, 2005-12..2008-06, 2019-08..2020-08, 2022-04..2025-09

## Verdict (2026-11-13)

Dead, the closest miss of the six. A year out after any inversion: +0.08 over `tsmom12` (p = 0.24), ahead in 4 of 5 eras, worst loss 30% against 37%; but since 2003 it is 1.17 against 1.20, and the sign is wrong on other ETFs, coins and indexes (S&P 500 1962-1993 included). The 1994-2025 gain comes from two calls: out of stocks through the dot-com bust (-2% against -28%) and through the covid crash a few months after the 2019 inversion (+2% against -22%, luck of timing: the curve did not foresee a virus). On the S&P 500 1962-1993 it was behind (-0.17). Five inversion spells since 1994, two before: one or two good calls, not a pattern.
