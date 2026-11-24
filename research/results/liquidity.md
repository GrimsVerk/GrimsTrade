# liquidity: step aside when real M2 shrinks (or the Fed runs QT)

Card: `cards/liquidity.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| m2-and | 0.95 (0.18) | +15.3% | 16.4% | 36.5% | 2.6 | 67% | 1.16 | 0.15 | 1.54 | 1.50 | 0.28 | -0.10 (p=0.98; -0.18..-0.02) | 0/5 |
| m2-alone | 0.79 (0.18) | +15.2% | 20.7% | 68.8% | 2.2 | 81% | 1.16 | -0.05 | 1.65 | 1.53 | 0.18 | -0.26 (p=0.99; -0.47..-0.06) | 2/5 |
| walcl-and | 0.95 (0.18) | +13.7% | 14.7% | 28.9% | 2.3 | 64% | 1.34 | 0.18 | 1.42 | 1.50 | -0.16 | -0.10 (p=0.85; -0.26..+0.07) | 1/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| m2-and | -28% | -4% | -22% | -14% | -6% | -22% | -20% |
| m2-alone | -69% | -27% | -22% | -25% | -17% | -43% | -30% |
| walcl-and | -28% | -4% | -22% | -13% | -6% | -2% | -20% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: m2-and +14.3%, m2-alone +14.2%, walcl-and +12.8%, tsmom12 +16.4%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| m2-and@etf | 0.55 (0.20) | +4.2% | 8.1% | 16.5% | 2.8 | 59% | 0.75 | 0.36 | 0.44 | 0.60 | -0.05 (p=0.77; -0.16..+0.06) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| m2-and@coin | 0.54 (0.34) | +14.0% | 75.4% | 92.4% | 3.7 | 44% | 0.64 | 0.44 | +0.00 (p=0.47; -0.10..+0.10) | 1/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

## Out of universe: GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| m2-and@GSPC | 0.28 (0.19) | +2.2% | 9.5% | 33.6% | 1.9 | 52% | 0.15 | 0.40 | -0.17 (p=0.96; -0.32..-0.01) | 0/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | 0.26 | 0.62 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.05 (p=0.38; -0.18..+0.25) | 2/2 |

## Out of universe: N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| m2-and@N225 | 0.52 (0.13) | +5.7% | 12.1% | 42.4% | 1.8 | 51% | 0.74 | 0.80 | 0.37 | 0.22 | 0.27 | 0.54 | 0.65 | -0.03 (p=0.70; -0.13..+0.07) | 4/7 |
| tsmom12@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | 0.77 | 0.72 | 0.35 | 0.33 | 0.24 | 0.54 | 0.81 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.15 (p=0.94; -0.31..+0.01) | 3/7 |

## Out of universe: FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| m2-and@FTSE | 0.31 (0.16) | +2.7% | 10.6% | 42.3% | 2.4 | 54% | 0.28 | 0.81 | 0.29 | -0.14 | -0.02 | 0.63 | -0.07 (p=0.80; -0.19..+0.06) | 3/6 |
| tsmom12@FTSE | 0.37 (0.16) | +3.7% | 11.8% | 39.1% | 2.7 | 71% | 0.64 | 0.72 | 0.36 | -0.07 | -0.02 | 0.20 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.01 (p=0.43; -0.18..+0.20) | 5/6 |

## Out of universe: GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| m2-and@GDAXI | 0.24 (0.17) | +2.3% | 13.8% | 57.6% | 1.9 | 54% | -0.33 | 0.78 | 0.39 | 0.31 | -0.47 | -0.01 | -0.16 (p=0.99; -0.27..-0.05) | 2/6 |
| tsmom12@GDAXI | 0.40 (0.17) | +5.0% | 15.1% | 58.9% | 1.8 | 69% | 0.62 | 0.68 | 0.46 | 0.42 | -0.47 | 0.44 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | +0.07 (p=0.30; -0.14..+0.28) | 5/6 |

## Pass bar (primary variant `m2-and`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.10, p = 0.98)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (36.5% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.05, coin +0.00, idx -0.11)
- PASS: 5. Beats equal weight on Sharpe (0.95 vs 0.88)

**FAILS train.**

## Since 2003 (the review's window)

| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |
|---|---:|---:|---:|---:|
| m2-and | 1.11 | +18.3% | 36.5% | -0.08 (0.92) |
| m2-alone | 1.12 | +21.7% | 47.8% | -0.07 (0.74) |
| walcl-and | 1.09 | +14.8% | 28.6% | -0.11 (0.77) |
| tsmom12 | 1.20 | +20.7% | 36.5% |  |
| equal-weight | 1.19 | +24.9% | 47.0% | -0.00 (0.51) |

- FAIL: 6. Not behind `tsmom12` on Sharpe 2003-2025 (1.11 vs 1.20)

**Card verdict (bars 1-6): FAILS train.**

## Hostile spells (independent episodes)

- `m2`, 1962-1993: 7 spells, 27% of days: 1973-11..1975-07, 1978-11..1981-05, 1981-08..1982-01, 1987-12..1988-03, 1989-03..1990-01, 1990-09..1992-02, 1992-04..1993-12
- `m2`, 1994-2025: 6 spells, 15% of days: 1994-02..1994-05, 1994-06..1995-09, 2005-10..2005-12, 2008-09..2008-10, 2010-02..2010-07, 2022-05..2024-10
- `walcl`, 1962-1993: 0 spells, 0% of days: 
- `walcl`, 1994-2025: 6 spells, 23% of days: 2009-11..2010-01, 2012-06..2012-11, 2015-11..2016-03, 2016-05..2017-09, 2017-11..2019-12, 2022-11..2025-11

## Verdict (2026-11-13)

Dead. Real M2 below zero: 0.95 against 1.05, behind in every era. The Fed balance sheet shrinking (QT): 0.95, and out of the market through most of 2017-2019 and 2023-2025, which were good years. Six spells each, and real M2 was negative in 2022 only after prices had already fallen.
