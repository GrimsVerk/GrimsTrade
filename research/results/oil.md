# oil: oil supply shock regime

Card: `cards/oil.md`. Protocol: `protocol.md`. Shared rules: `cards/yt-1.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| oil-and | 1.10 (0.18) | +17.4% | 15.7% | 36.5% | 2.7 | 65% | 1.27 | 0.40 | 1.57 | 1.38 | 1.01 | +0.05 (p=0.20; -0.04..+0.15) | 3/5 |
| oil-alone | 1.01 (0.18) | +18.0% | 17.9% | 56.3% | 2.4 | 73% | 1.27 | 0.20 | 1.65 | 1.43 | 1.13 | -0.04 (p=0.64; -0.21..+0.14) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| oil-and | -18% | +6% | -22% | -8% | -6% | -22% | -16% |
| oil-alone | -47% | -3% | -23% | -8% | -6% | -22% | -16% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: oil-and +16.0%, oil-alone +16.5%, tsmom12 +16.4%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| oil-and@etf | 0.63 (0.21) | +4.6% | 7.6% | 16.6% | 2.7 | 56% | 0.92 | 0.51 | 0.01 | 0.78 | +0.03 (p=0.38; -0.11..+0.16) | 3/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

## Out of universe: GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| oil-and@GSPC | 0.31 (0.19) | +2.7% | 10.4% | 34.8% | 2.0 | 64% | 0.26 | 0.37 | -0.14 (p=0.99; -0.24..-0.05) | 0/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | 0.26 | 0.62 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.05 (p=0.38; -0.18..+0.25) | 2/2 |

## Out of universe: N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| oil-and@N225 | 0.53 (0.13) | +6.0% | 12.3% | 40.2% | 1.9 | 55% | 0.77 | 0.51 | 0.10 | 0.61 | 0.35 | 0.24 | 0.86 | -0.02 (p=0.63; -0.11..+0.08) | 3/7 |
| tsmom12@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | 0.77 | 0.72 | 0.35 | 0.33 | 0.24 | 0.54 | 0.81 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.15 (p=0.94; -0.31..+0.01) | 3/7 |

## Out of universe: FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| oil-and@FTSE | 0.31 (0.16) | +2.6% | 9.9% | 40.7% | 2.5 | 53% | 0.33 | 0.63 | 0.69 | -0.13 | -0.41 | 0.43 | -0.06 (p=0.73; -0.18..+0.09) | 2/6 |
| tsmom12@FTSE | 0.37 (0.16) | +3.7% | 11.8% | 39.1% | 2.7 | 71% | 0.64 | 0.72 | 0.36 | -0.07 | -0.02 | 0.20 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.01 (p=0.43; -0.18..+0.20) | 5/6 |

## Out of universe: GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| oil-and@GDAXI | 0.39 (0.17) | +4.3% | 13.0% | 57.7% | 1.6 | 53% | 0.46 | 0.47 | 0.72 | 0.41 | -0.92 | 0.96 | -0.01 (p=0.54; -0.15..+0.13) | 2/6 |
| tsmom12@GDAXI | 0.40 (0.17) | +5.0% | 15.1% | 58.9% | 1.8 | 69% | 0.62 | 0.68 | 0.46 | 0.42 | -0.47 | 0.44 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | +0.07 (p=0.30; -0.14..+0.28) | 5/6 |

## Pass bar (primary variant `oil-and`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference +0.05, p = 0.20)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (3 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (36.5% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 2 sets (etf +0.03, idx -0.06)
- PASS: 5. Beats equal weight on Sharpe (1.10 vs 0.88)

**FAILS train.**

## Since 2003

| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |
|---|---:|---:|---:|---:|
| oil-and | 1.20 | +20.2% | 36.5% | +0.00 (0.45) |
| oil-alone | 1.32 | +23.3% | 34.4% | +0.12 (0.01) |
| tsmom12 | 1.20 | +20.7% | 36.5% |  |
| equal-weight | 1.19 | +24.9% | 47.0% | -0.00 (0.51) |

- PASS: 6. Not behind `tsmom12` on Sharpe 2003-2025 (1.20 vs 1.20)

**Card verdict (bars 1-6): FAILS train.**

## Hostile spells (independent episodes)

- `oil` on SPY, 1994-2025: 7 spells, 27% of days: 1999-05..2000-09, 2002-05..2003-01, 2004-10..2005-04, 2007-07..2009-01, 2009-06..2010-08, 2016-07..2017-08, 2020-09..2022-12
- `oil` on BTC, 2013-2025: 2 spells, 26% of days: 2016-07..2017-08, 2020-09..2022-12
