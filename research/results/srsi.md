# srsi: monthly stochastic RSI leaves overbought

Card: `cards/srsi.md`. Protocol: `protocol.md`. Shared rules: `cards/yt-1.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| srsi-and | 0.82 (0.18) | +11.1% | 13.9% | 28.9% | 2.3 | 52% | 1.02 | 0.10 | 1.15 | 1.44 | 0.48 | -0.23 (p=0.99; -0.38..-0.07) | 0/5 |
| srsi-alone | 0.69 (0.18) | +11.6% | 18.2% | 68.8% | 2.2 | 65% | 1.03 | -0.06 | 1.24 | 1.54 | 0.52 | -0.36 (p=0.99; -0.59..-0.12) | 1/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| srsi-and | -28% | +5% | -12% | -2% | -11% | -20% | -2% |
| srsi-alone | -69% | -11% | -11% | -13% | -22% | -35% | -15% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: srsi-and +10.5%, srsi-alone +11.0%, tsmom12 +16.4%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| srsi-and@etf | 0.44 (0.20) | +2.5% | 6.1% | 11.6% | 2.2 | 43% | 0.76 | 0.17 | 0.47 | -0.42 | -0.16 (p=0.92; -0.34..+0.03) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| srsi-and@coin | 0.56 (0.34) | +16.6% | 71.1% | 90.7% | 3.7 | 39% | 0.68 | 0.42 | +0.02 (p=0.41; -0.11..+0.15) | 2/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

## Out of universe: GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| srsi-and@GSPC | 0.24 (0.19) | +1.6% | 7.9% | 34.8% | 1.4 | 30% | 0.05 | 0.39 | -0.20 (p=0.90; -0.44..+0.05) | 0/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | 0.26 | 0.62 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.05 (p=0.38; -0.18..+0.25) | 2/2 |

## Out of universe: N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| srsi-and@N225 | 0.28 (0.13) | +2.2% | 9.4% | 35.5% | 1.5 | 33% | 0.23 | 0.47 | 0.44 | 0.17 | 0.03 | 0.03 | 0.89 | -0.27 (p=1.00; -0.42..-0.10) | 2/7 |
| tsmom12@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | 0.77 | 0.72 | 0.35 | 0.33 | 0.24 | 0.54 | 0.81 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.15 (p=0.94; -0.31..+0.01) | 3/7 |

## Out of universe: FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| srsi-and@FTSE | 0.35 (0.16) | +2.7% | 8.8% | 32.2% | 2.0 | 44% | 1.23 | 0.50 | 0.05 | -0.30 | 0.04 | -0.06 | -0.02 (p=0.60; -0.23..+0.20) | 2/6 |
| tsmom12@FTSE | 0.37 (0.16) | +3.7% | 11.8% | 39.1% | 2.7 | 71% | 0.64 | 0.72 | 0.36 | -0.07 | -0.02 | 0.20 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.01 (p=0.43; -0.18..+0.20) | 5/6 |

## Out of universe: GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| srsi-and@GDAXI | 0.33 (0.17) | +3.2% | 11.4% | 23.6% | 1.3 | 40% | 0.57 | 0.33 | 0.29 | 0.28 | -0.02 | 0.52 | -0.07 (p=0.71; -0.27..+0.14) | 2/6 |
| tsmom12@GDAXI | 0.40 (0.17) | +5.0% | 15.1% | 58.9% | 1.8 | 69% | 0.62 | 0.68 | 0.46 | 0.42 | -0.47 | 0.44 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | +0.07 (p=0.30; -0.14..+0.28) | 5/6 |

## Pass bar (primary variant `srsi-and`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.23, p = 0.99)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (28.9% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.16, coin +0.02, idx -0.14)
- FAIL: 5. Beats equal weight on Sharpe (0.82 vs 0.88)

**FAILS train.**

## Since 2003

| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |
|---|---:|---:|---:|---:|
| srsi-and | 1.02 | +13.0% | 28.5% | -0.18 (0.92) |
| srsi-alone | 1.11 | +17.1% | 40.1% | -0.09 (0.73) |
| tsmom12 | 1.20 | +20.7% | 36.5% |  |
| equal-weight | 1.19 | +24.9% | 47.0% | -0.00 (0.51) |

- FAIL: 6. Not behind `tsmom12` on Sharpe 2003-2025 (1.02 vs 1.20)

**Card verdict (bars 1-6): FAILS train.**

## Hostile spells (independent episodes)

- `srsi` on SPY, 1994-2025: 10 spells, 46% of days: 1996-08..1997-07, 2004-08..2006-02, 2006-07..2008-07, 2010-07..2011-06, 2011-08..2015-09, 2018-03..2019-02, 2020-03..2021-03, 2021-11..2022-10, 2023-11..2024-10, 2025-03..2025-11
- `srsi` on BTC, 2013-2025: 5 spells, 47% of days: 2016-10..2017-09, 2018-02..2019-01, 2019-10..2020-09, 2021-06..2022-05, 2023-10..2025-11
