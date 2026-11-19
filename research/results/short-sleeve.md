# short-sleeve: `tsmom12` + 10% SPY/QQQ downtrend short vs + 10% T-bill slot

Card `cards/short-sleeve.md`. Train window, decisions 1994-02-01..2025-11-09; returns on calendar days 1994-02-02..2025-11-10. Cash, slot, collateral and short proceeds earn the 13-week T-bill; borrow 1%/yr; 5 bps a side on leg trades; mix reset to 90/10 daily. Average bill yield 2.43%.

## Whole window

| Book | Sharpe above bills | CAGR | Vol | Max DD |
|---|---:|---:|---:|---:|
| `bill10` (control) | 0.933 | +16.84% | 15.3% | 32.1% |
| `short10` (test) | 0.922 | +16.71% | 15.4% | 32.8% |
| `tsmom12` (cash at bills, for reference) | 0.933 | +18.39% | 17.1% | 35.6% |

**Sharpe above bills, `short10` - `bill10`: d = -0.0109, bootstrap SE 0.0140, z = -0.78, one-sided p = 0.7870** (paired stationary bootstrap, 2000 draws, mean block 20 days). Family bar p < 0.00147; project bar z >= 4.65 (N_eff 433), Bonferroni p <= 1.2e-4.

Sleeve alone (over the bill slot, share of the book): -0.105% a year; book turnover 2.60/yr (sleeve 0.13).
- SPY leg: short 19% of the days it could be; contribution -0.067% of the book a year, sum -2.2 log points.
- QQQ leg: short 22% of the days it could be; contribution -0.038% of the book a year, sum -1.3 log points.

## Crash windows (total return)

| Window | `bill10` | `short10` | Difference | SPY leg | QQQ leg |
|---|---:|---:|---:|---:|---:|
| 2008 (2008-01-01..2008-12-31) | -0.0% | +2.5% | +2.6% | +1.3% | +1.4% |
| 2020-Q1 (2020-01-01..2020-03-31) | -5.9% | -6.9% | -1.0% | -0.4% | -0.6% |
| 2022 (2022-01-01..2022-12-31) | -9.9% | -8.8% | +1.1% | +0.3% | +0.9% |
| dot-com bust (2000-03-24..2002-10-09) | -19.8% | -13.6% | +6.2% | +2.4% | +5.3% |
| 2008 crisis (2007-10-09..2009-03-09) | -2.1% | +2.5% | +4.5% | +2.7% | +2.1% |
| covid crash (2020-02-19..2020-03-23) | -21.2% | -21.0% | +0.2% | +0.3% | +0.0% |
| 2022 rate shock (2022-01-03..2022-10-12) | -11.5% | -10.1% | +1.5% | +0.6% | +1.0% |

## Calendar years: worst and the sleeve's best and worst

- Worst year: `bill10` 2000 -20.7%; `short10` 2000 -19.9%.
- Sleeve's worst years (difference): 2009 -3.1%, 2020 -2.7%, 2003 -2.1%, 2023 -1.6%, 2016 -1.5%
- Sleeve's best years (difference): 2002 +2.8%, 2008 +2.6%, 2001 +2.1%, 2022 +1.1%, 2000 +0.7%
- Years the sleeve added: 6 of 32.

## By era: Sharpe above bills

| Era | `bill10` | `short10` | d |
|---|---:|---:|---:|
| 1994-99 | 1.05 | 1.05 | -0.001 |
| 2000-09 | 0.04 | 0.06 | +0.020 |
| 2010-16 | 1.54 | 1.52 | -0.022 |
| 2017-21 | 1.47 | 1.45 | -0.022 |
| 2022-25 | 0.73 | 0.71 | -0.017 |

## Insurance, insure-1 style (log points of `short10` - `bill10`)

### SPY (US market, primary): 25% falls (zigzag on total-return closes)

| Peak | Trough | Fall | I (fall) | B (rebound) | I + B |
|---|---|---:|---:|---:|---:|
| 2000-03-24 | 2002-10-09 | 48% | +7.4 | -3.6 | +3.8 |
| 2007-10-09 | 2009-03-09 | 55% | +4.5 | -5.2 | -0.6 |
| 2020-02-19 | 2020-03-23 | 34% | +0.3 | -1.9 | -1.6 |

Episodes 3, I > 0 in 3. Sum I +12.3, sum B -10.7, calm C -5.2, total -3.7 log points. **Premium P = -(B + C) / I: 1.30.**

### QQQ (second series): 25% falls (zigzag on total-return closes)

| Peak | Trough | Fall | I (fall) | B (rebound) | I + B |
|---|---|---:|---:|---:|---:|
| 2000-03-27 | 2000-05-23 | 36% | +0.0 | +0.0 | +0.0 |
| 2000-09-01 | 2001-01-02 | 48% | +1.5 | -1.6 | -0.1 |
| 2001-01-23 | 2001-04-04 | 50% | +4.3 | -3.0 | +1.3 |
| 2001-05-21 | 2001-09-21 | 45% | +4.3 | -3.2 | +1.2 |
| 2001-12-06 | 2002-10-09 | 53% | +5.1 | -3.6 | +1.5 |
| 2007-10-31 | 2008-11-20 | 53% | +4.4 | -5.1 | -0.6 |
| 2020-02-19 | 2020-03-16 | 29% | +0.0 | -1.6 | -1.6 |
| 2021-12-27 | 2022-11-03 | 35% | +1.5 | -1.6 | -0.2 |

Episodes 8, I > 0 in 6. Sum I +21.1, sum B -19.7, calm C -5.0, total -3.7 log points. **Premium P = -(B + C) / I: 1.17.**
