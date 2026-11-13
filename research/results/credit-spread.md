# credit-spread: step aside when corporate spreads widen

Card: `cards/credit-spread.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| spread-and | 0.99 (0.18) | +15.0% | 15.3% | 38.8% | 2.9 | 65% | 1.09 | 0.54 | 1.48 | 1.19 | 0.78 | -0.06 (p=0.77; -0.19..+0.07) | 1/5 |
| spread-alone | 0.80 (0.18) | +13.5% | 17.8% | 60.3% | 3.0 | 73% | 1.10 | 0.07 | 1.37 | 1.09 | 0.72 | -0.25 (p=0.98; -0.46..-0.05) | 0/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| spread-and | -7% | +2% | -22% | -17% | -6% | -22% | -23% |
| spread-alone | -56% | +2% | -23% | -27% | -17% | -42% | -31% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: spread-and +14.0%, spread-alone +12.6%, tsmom12 +16.4%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| spread-and@etf | 0.56 (0.20) | +4.2% | 7.9% | 16.6% | 2.7 | 59% | 0.85 | 0.31 | 0.35 | 0.57 | -0.04 (p=0.66; -0.18..+0.11) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| spread-and@coin | 0.48 (0.34) | +8.6% | 76.1% | 91.5% | 4.6 | 52% | 0.58 | 0.30 | -0.06 (p=0.85; -0.17..+0.03) | 0/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

## Out of universe: GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| spread-and@GSPC | 0.41 (0.19) | +3.9% | 10.8% | 34.8% | 2.2 | 67% | 0.26 | 0.56 | -0.04 (p=0.85; -0.10..+0.02) | 0/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | 0.26 | 0.62 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.05 (p=0.38; -0.18..+0.25) | 2/2 |

## Out of universe: N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| spread-and@N225 | 0.56 (0.13) | +6.5% | 12.8% | 47.4% | 2.1 | 60% | 0.77 | 0.63 | 0.18 | 0.47 | 0.44 | 0.26 | 0.83 | +0.01 (p=0.47; -0.07..+0.08) | 3/7 |
| tsmom12@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | 0.77 | 0.72 | 0.35 | 0.33 | 0.24 | 0.54 | 0.81 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.15 (p=0.94; -0.31..+0.01) | 3/7 |

## Out of universe: FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| spread-and@FTSE | 0.29 (0.16) | +2.6% | 10.9% | 37.8% | 2.4 | 63% | 0.46 | 0.48 | 0.36 | -0.14 | 0.01 | 0.32 | -0.09 (p=0.93; -0.17..+0.01) | 2/6 |
| tsmom12@FTSE | 0.37 (0.16) | +3.7% | 11.8% | 39.1% | 2.7 | 71% | 0.64 | 0.72 | 0.36 | -0.07 | -0.02 | 0.20 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.01 (p=0.43; -0.18..+0.20) | 5/6 |

## Out of universe: GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| spread-and@GDAXI | 0.46 (0.17) | +5.4% | 13.2% | 49.4% | 1.7 | 59% | 0.15 | 0.80 | 0.75 | 0.55 | -0.29 | 0.39 | +0.07 (p=0.19; -0.06..+0.21) | 4/6 |
| tsmom12@GDAXI | 0.40 (0.17) | +5.0% | 15.1% | 58.9% | 1.8 | 69% | 0.62 | 0.68 | 0.46 | 0.42 | -0.47 | 0.44 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | +0.07 (p=0.30; -0.14..+0.28) | 5/6 |

## Pass bar (primary variant `spread-and`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.06, p = 0.77)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (1 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (38.8% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.04, coin -0.06, idx -0.01)
- PASS: 5. Beats equal weight on Sharpe (0.99 vs 0.88)

**FAILS train.**

## Since 2003 (the review's window)

| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |
|---|---:|---:|---:|---:|
| spread-and | 1.06 | +17.3% | 38.8% | -0.13 (0.99) |
| spread-alone | 1.03 | +18.8% | 46.4% | -0.16 (0.93) |
| tsmom12 | 1.20 | +20.7% | 36.5% |  |
| equal-weight | 1.19 | +24.9% | 47.0% | -0.00 (0.51) |

- FAIL: 6. Not behind `tsmom12` on Sharpe 2003-2025 (1.06 vs 1.20)

**Card verdict (bars 1-6): FAILS train.**

## Hostile spells (independent episodes)

- `spread`, 1962-1993: 6 spells, 3% of days: 1988-01..1988-03, 1989-07..1989-08, 1989-11..1990-01, 1990-10..1991-03, 1991-12..1992-01, 1992-09..1992-11
- `spread`, 1994-2025: 13 spells, 26% of days: 1995-12..1996-02, 1998-09..1999-06, 2000-04..2001-05, 2001-09..2001-12, 2002-07..2003-01, 2007-11..2009-07, 2010-06..2010-12, 2011-08..2012-08, 2015-05..2016-04, 2018-12..2019-03, 2020-03..2020-11, 2022-05..2022-09, 2022-10..2022-11
