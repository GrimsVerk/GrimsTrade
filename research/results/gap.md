# gap: stocks near highs, consumers gloomy

Card: `cards/gap.md`. Protocol: `protocol.md`. Shared rules: `cards/yt-1.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gap-and | 0.95 (0.18) | +15.3% | 16.3% | 36.5% | 2.6 | 58% | 1.34 | 0.03 | 1.32 | 1.44 | 0.82 | -0.09 (p=0.98; -0.17..-0.02) | 0/5 |
| gap-alone | 0.78 (0.18) | +14.0% | 19.3% | 68.8% | 2.4 | 70% | 1.35 | -0.14 | 1.36 | 1.48 | 0.88 | -0.27 (p=1.00; -0.45..-0.10) | 1/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| gap-and | -28% | +5% | -22% | -8% | -10% | -22% | -16% |
| gap-alone | -69% | -19% | -23% | -10% | -10% | -22% | -15% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: gap-and +14.2%, gap-alone +13.1%, tsmom12 +16.4%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gap-and@etf | 0.46 (0.20) | +2.6% | 5.9% | 16.5% | 2.6 | 45% | 0.48 | 0.43 | 0.36 | 0.78 | -0.14 (p=0.86; -0.35..+0.05) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

## Out of universe: GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gap-and@GSPC | 0.31 (0.19) | +2.6% | 9.7% | 34.8% | 2.0 | 56% | 0.26 | 0.38 | -0.13 (p=0.96; -0.25..-0.01) | 0/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | 0.26 | 0.62 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.05 (p=0.38; -0.18..+0.25) | 2/2 |

## Out of universe: N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gap-and@N225 | 0.47 (0.13) | +4.6% | 10.6% | 40.0% | 1.6 | 45% | 0.77 | 0.66 | 0.35 | 0.03 | 0.32 | 0.14 | 0.22 | -0.08 (p=0.81; -0.21..+0.06) | 2/7 |
| tsmom12@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | 0.77 | 0.72 | 0.35 | 0.33 | 0.24 | 0.54 | 0.81 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.15 (p=0.94; -0.31..+0.01) | 3/7 |

## Out of universe: FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gap-and@FTSE | 0.29 (0.16) | +2.3% | 9.2% | 39.1% | 1.8 | 41% | 0.61 | 0.72 | -0.08 | -0.32 | -0.11 | - | -0.08 (p=0.80; -0.23..+0.08) | 0/5 |
| tsmom12@FTSE | 0.37 (0.16) | +3.7% | 11.8% | 39.1% | 2.7 | 71% | 0.64 | 0.72 | 0.36 | -0.07 | -0.02 | 0.20 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.01 (p=0.43; -0.18..+0.20) | 5/6 |

## Out of universe: GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gap-and@GDAXI | 0.20 (0.17) | +1.8% | 12.2% | 53.5% | 1.4 | 38% | 0.69 | 0.68 | 0.00 | 0.06 | -0.61 | - | -0.19 (p=0.97; -0.37..-0.02) | 2/5 |
| tsmom12@GDAXI | 0.40 (0.17) | +5.0% | 15.1% | 58.9% | 1.8 | 69% | 0.62 | 0.68 | 0.46 | 0.42 | -0.47 | 0.44 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | +0.07 (p=0.30; -0.14..+0.28) | 5/6 |

## Pass bar (primary variant `gap-and`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.09, p = 0.98)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (36.5% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 2 sets (etf -0.14, idx -0.12)
- PASS: 5. Beats equal weight on Sharpe (0.95 vs 0.88)

**FAILS train.**

## Since 2003

| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |
|---|---:|---:|---:|---:|
| gap-and | 1.07 | +17.1% | 36.5% | -0.12 (0.97) |
| gap-alone | 1.11 | +18.8% | 34.4% | -0.09 (0.84) |
| tsmom12 | 1.20 | +20.7% | 36.5% |  |
| equal-weight | 1.19 | +24.9% | 47.0% | -0.00 (0.51) |

- FAIL: 6. Not behind `tsmom12` on Sharpe 2003-2025 (1.07 vs 1.20)

**Card verdict (bars 1-6): FAILS train.**

## Hostile spells (independent episodes)

- `gap` on SPY, 1994-2025: 6 spells, 41% of days: 2003-09..2004-04, 2005-05..2008-06, 2009-10..2014-06, 2020-06..2021-03, 2021-08..2022-10, 2023-04..2025-11
- `gap` on BTC, 2013-2025: 5 spells, 41% of days: 2013-01..2013-08, 2013-11..2014-06, 2020-06..2021-03, 2021-10..2022-05, 2023-02..2025-11
