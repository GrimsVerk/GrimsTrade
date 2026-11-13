# halving: out of coins in the bear year after a halving

Card: `cards/halving.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| halving-and | 1.20 (0.18) | +19.9% | 16.2% | 28.9% | 2.7 | 74% | 1.34 | 0.19 | 1.67 | 1.94 | 1.11 | +0.15 (p=0.00; +0.06..+0.25) | 3/5 |
| halving-alone | 1.28 (0.18) | +22.8% | 17.2% | 29.7% | 2.5 | 76% | 1.34 | 0.19 | 1.81 | 2.10 | 1.25 | +0.23 (p=0.00; +0.12..+0.36) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| halving-and | -28% | -4% | -22% | -8% | +4% | +3% | -7% |
| halving-alone | -28% | -4% | -21% | -8% | +4% | +3% | -10% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: halving-and +18.1%, halving-alone +20.6%, tsmom12 +16.4%, equal-weight +16.7%

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| halving-and@coin | 0.86 (0.33) | +44.2% | 68.5% | 69.5% | 4.3 | 41% | 1.14 | 0.38 | +0.33 (p=0.02; +0.06..+0.61) | 1/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

## Pass bar (primary variant `halving-and`)

- PASS: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference +0.15, p = 0.00)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (3 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (28.9% vs 36.5%)
- PASS: 4. Same sign out of universe in at least 1 of 1 sets (coin +0.33)
- PASS: 5. Beats equal weight on Sharpe (1.20 vs 0.88)

**FAILS train.**

## Since 2003 (the review's window)

| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |
|---|---:|---:|---:|---:|
| halving-and | 1.42 | +23.6% | 28.8% | +0.23 (0.00) |
| halving-alone | 1.52 | +27.9% | 29.7% | +0.33 (0.00) |
| tsmom12 | 1.20 | +20.7% | 36.5% |  |
| equal-weight | 1.19 | +24.9% | 47.0% | -0.00 (0.51) |

- PASS: 6. Not behind `tsmom12` on Sharpe 2003-2025 (1.42 vs 1.20)

**Card verdict (bars 1-6): FAILS train.**

## Hostile spells (independent episodes)

- `halving`, 1962-1993: 0 spells, 0% of days: 
- `halving`, 1994-2025: 3 spells, 9% of days: 2014-05..2015-05, 2018-01..2019-01, 2021-11..2022-11
