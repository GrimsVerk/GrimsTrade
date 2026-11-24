# vol-echo: the day a shock leaves other people's volatility window

Card: `cards/vol-echo.md`. Twin `constant` holds the same asset at the rule's average exposure. `equal-weight` is buy-and-hold of the asset.

## SPY, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@SPY (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo21@SPY | 0.25 (0.18) | +1.4% | 6.4% | 23.4% | 20.8 | 14% | 0.49 | -0.18 | 0.14 | 1.25 | 0.61 | -0.38 (p=0.98; -0.66..-0.08) | 1/5 |
| constant@SPY | 0.63 (0.18) | +1.6% | 2.6% | 9.6% | 0.0 | 14% | 1.37 | 0.05 | 0.84 | 0.99 | 0.68 | - | - |
| equal-weight@SPY | 0.63 (0.18) | +10.6% | 18.9% | 55.2% | 0.0 | 100% | 1.35 | 0.07 | 0.85 | 0.99 | 0.68 | +0.00 (p=0.34; -0.01..+0.01) | 3/5 |

Mean open-to-open return per day held +5.8 bps (1107 days), per day not held +4.6 bps (6889 days), Welch t = 0.34. Days held before 2010-01-01: +1.6 bps; from 2010-01-01: +9.5 bps. Sharpe difference to the twin from 2010-01-01: -0.27.

## QQQ, from 2000-03-10

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@QQQ (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo21@QQQ | 0.13 (0.20) | +0.7% | 8.3% | 38.6% | 20.3 | 14% | -0.38 | -0.01 | 1.28 | 0.87 | -0.28 (p=0.92; -0.61..+0.04) | 2/4 |
| constant@QQQ | 0.41 (0.20) | +1.5% | 3.8% | 19.1% | 0.1 | 14% | -0.09 | 0.95 | 1.22 | 0.63 | - | - |
| equal-weight@QQQ | 0.41 (0.20) | +7.7% | 26.5% | 83.0% | 0.0 | 100% | -0.09 | 0.94 | 1.23 | 0.63 | +0.00 (p=0.32; -0.01..+0.01) | 3/4 |

Mean open-to-open return per day held +4.2 bps (901 days), per day not held +4.5 bps (5554 days), Welch t = -0.05. Days held before 2010-01-01: -11.7 bps; from 2010-01-01: +12.0 bps. Sharpe difference to the twin from 2010-01-01: -0.33.

# Out of universe: other stock ETFs

## IWM, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@IWM (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo21@IWM | 0.04 (0.20) | -0.0% | 7.3% | 35.7% | 17.7 | 12% | -0.02 | -0.27 | 0.84 | -0.26 | -0.40 (p=0.95; -0.79..-0.01) | 1/4 |
| constant@IWM | 0.43 (0.20) | +1.2% | 2.8% | 8.8% | 0.1 | 12% | 0.25 | 0.71 | 0.57 | 0.27 | - | - |
| equal-weight@IWM | 0.44 (0.20) | +8.0% | 23.8% | 58.6% | 0.0 | 100% | 0.27 | 0.71 | 0.59 | 0.27 | +0.01 (p=0.08; -0.00..+0.02) | 4/4 |

Mean open-to-open return per day held +2.1 bps (726 days), per day not held +4.5 bps (5423 days), Welch t = -0.45. Days held before 2010-01-01: +1.0 bps; from 2010-01-01: +2.6 bps. Sharpe difference to the twin from 2010-01-01: -0.48.

## EFA, from 2002-08-28

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@EFA (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo21@EFA | -0.01 (0.21) | -0.4% | 7.6% | 27.8% | 21.1 | 14% | -0.13 | 0.34 | 0.47 | -0.80 | -0.46 (p=0.99; -0.84..-0.12) | 1/4 |
| constant@EFA | 0.45 (0.21) | +1.3% | 2.9% | 10.8% | 0.1 | 14% | 0.49 | 0.26 | 0.61 | 0.57 | - | - |
| equal-weight@EFA | 0.45 (0.21) | +7.4% | 20.8% | 61.0% | 0.0 | 100% | 0.47 | 0.28 | 0.61 | 0.54 | -0.00 (p=0.57; -0.01..+0.01) | 2/4 |

Mean open-to-open return per day held +0.7 bps (811 days), per day not held +4.0 bps (5026 days), Welch t = -0.74. Days held before 2010-01-01: -2.0 bps; from 2010-01-01: +1.8 bps. Sharpe difference to the twin from 2010-01-01: -0.37.

## EEM, from 2004-04-14

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@EEM (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo21@EEM | -0.09 (0.22) | -1.3% | 9.6% | 36.8% | 19.1 | 13% | -0.07 | 0.10 | -0.40 | -0.17 | -0.45 (p=0.99; -0.81..-0.12) | 1/4 |
| constant@EEM | 0.36 (0.21) | +1.2% | 3.6% | 11.9% | 0.1 | 13% | 0.53 | 0.07 | 0.49 | 0.41 | - | - |
| equal-weight@EEM | 0.38 (0.21) | +7.0% | 27.4% | 66.4% | 0.0 | 100% | 0.57 | 0.09 | 0.52 | 0.39 | +0.02 (p=0.01; +0.01..+0.04) | 3/4 |

Mean open-to-open return per day held -1.8 bps (706 days), per day not held +4.8 bps (4722 days), Welch t = -1.09. Days held before 2010-01-01: -1.5 bps; from 2010-01-01: -1.9 bps. Sharpe difference to the twin from 2010-01-01: -0.38.

# Out of universe: foreign indexes

## N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo21@N225 | 0.24 (0.13) | +1.3% | 6.2% | 40.6% | 19.3 | 13% | 0.77 | 0.31 | -0.16 | -0.28 | 1.00 | 0.15 | -0.19 | -0.16 (p=0.87; -0.39..+0.08) | 1/7 |
| constant@N225 | 0.40 (0.13) | +1.0% | 2.7% | 16.2% | 0.1 | 13% | 0.85 | 0.49 | 0.16 | -0.12 | 0.48 | 0.54 | 0.78 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.00 (p=0.73; -0.01..+0.00) | 4/7 |

Mean open-to-open return per day held +5.6 bps (1976 days), per day not held +2.8 bps (12738 days), Welch t = 1.12. Days held before 2010-01-01: +4.3 bps; from 2010-01-01: +9.5 bps. Sharpe difference to the twin from 2010-01-01: -0.14.

## FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo21@FTSE | 0.38 (0.16) | +1.9% | 5.4% | 18.0% | 19.3 | 13% | 0.48 | 1.15 | 0.14 | 0.30 | 0.36 | 0.00 | -0.01 (p=0.52; -0.30..+0.29) | 4/6 |
| constant@FTSE | 0.39 (0.16) | +0.8% | 2.2% | 8.1% | 0.0 | 13% | 0.82 | 0.86 | 0.02 | 0.29 | 0.12 | 0.63 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | -0.00 (p=0.62; -0.01..+0.01) | 3/6 |

Mean open-to-open return per day held +7.4 bps (1327 days), per day not held +1.9 bps (8991 days), Welch t = 1.95. Days held before 2010-01-01: +10.2 bps; from 2010-01-01: +4.3 bps. Sharpe difference to the twin from 2010-01-01: -0.04.

## GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo21@GDAXI | 0.27 (0.16) | +1.7% | 7.2% | 20.9% | 21.0 | 14% | 0.02 | 0.98 | -0.02 | 0.42 | 0.05 | 0.37 | -0.21 (p=0.87; -0.51..+0.10) | 0/6 |
| constant@GDAXI | 0.47 (0.17) | +1.4% | 3.0% | 14.7% | 0.1 | 14% | 0.67 | 1.02 | 0.07 | 0.53 | 0.44 | 0.75 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | -0.01 (p=0.84; -0.02..+0.00) | 2/6 |

Mean open-to-open return per day held +6.9 bps (1268 days), per day not held +3.6 bps (8054 days), Welch t = 0.85. Days held before 2010-01-01: +7.2 bps; from 2010-01-01: +6.5 bps. Sharpe difference to the twin from 2010-01-01: -0.25.

# Placebo: the S&P 500 index 1962-1993 (before volatility-control funds)

## GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs constant@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo21@GSPC | 0.42 (0.18) | +1.8% | 4.4% | 14.6% | 18.6 | 12% | 0.30 | 0.55 | -0.09 (p=0.67; -0.47..+0.27) | 1/2 |
| constant@GSPC | 0.51 (0.18) | +0.8% | 1.7% | 7.2% | 0.0 | 12% | 0.29 | 0.75 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | -0.02 (p=0.98; -0.03..-0.00) | 0/2 |

Mean open-to-open return per day held +7.0 bps (970 days), per day not held +2.1 bps (6848 days), Welch t = 1.82. Days held before 2010-01-01: +7.0 bps; from 2010-01-01: +nan bps. Sharpe difference to the twin from 2010-01-01: +0.00.

# Variant `echo63` (63-day window, a tenth of its variance)

## SPY, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@SPY (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo63@SPY | -0.22 (0.17) | -1.0% | 4.3% | 43.0% | 10.8 | 7% | 0.85 | -0.59 | -0.57 | 0.18 | -0.10 | -0.85 (p=1.00; -1.18..-0.50) | 0/5 |
| constant@SPY | 0.63 (0.18) | +0.9% | 1.4% | 5.2% | 0.0 | 7% | 1.33 | 0.06 | 0.86 | 1.00 | 0.69 | - | - |
| equal-weight@SPY | 0.63 (0.18) | +10.6% | 18.9% | 55.2% | 0.0 | 100% | 1.35 | 0.07 | 0.85 | 0.99 | 0.68 | -0.00 (p=0.55; -0.02..+0.02) | 2/5 |

Mean open-to-open return per day held -3.9 bps (585 days), per day not held +5.4 bps (7411 days), Welch t = -2.17. Days held before 2010-01-01: -4.7 bps; from 2010-01-01: -3.3 bps. Sharpe difference to the twin from 2010-01-01: -1.08.

## QQQ, from 2000-03-10

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@QQQ (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| echo63@QQQ | -0.17 (0.20) | -1.1% | 5.8% | 39.0% | 10.5 | 7% | -0.19 | -0.73 | 0.60 | -0.12 | -0.59 (p=1.00; -0.93..-0.23) | 0/4 |
| constant@QQQ | 0.41 (0.20) | +0.8% | 1.9% | 9.7% | 0.0 | 7% | -0.07 | 0.90 | 1.24 | 0.59 | - | - |
| equal-weight@QQQ | 0.41 (0.20) | +7.7% | 26.5% | 83.0% | 0.0 | 100% | -0.09 | 0.94 | 1.23 | 0.63 | -0.00 (p=0.60; -0.02..+0.02) | 2/4 |

Mean open-to-open return per day held -4.4 bps (454 days), per day not held +5.1 bps (6001 days), Welch t = -1.43. Days held before 2010-01-01: -7.4 bps; from 2010-01-01: -3.2 bps. Sharpe difference to the twin from 2010-01-01: -1.09.

# Before and after 2010 (the mechanism should be absent before)

| Asset | Period | Days held | bps a day held | Days not held | bps a day not held | Welch t |
|---|---|---:|---:|---:|---:|---:|
| SPY | before 2010 | 523 | +1.6 | 3486 | +4.0 | -0.41 |
| SPY | from 2010 | 584 | +9.5 | 3403 | +5.1 | +1.01 |
| QQQ | before 2010 | 297 | -11.7 | 2171 | +0.6 | -1.09 |
| QQQ | from 2010 | 604 | +12.0 | 3383 | +6.9 | +0.97 |
| GSPC | before 2010 | 970 | +7.0 | 6848 | +2.1 | +1.82 |
| GSPC | from 2010 | - | - | - | - | - |

`echo63`:

| Asset | Period | Days held | bps a day held | Days not held | bps a day not held | Welch t |
|---|---|---:|---:|---:|---:|---:|
| SPY | before 2010 | 252 | -4.7 | 3757 | +4.3 | -1.27 |
| SPY | from 2010 | 333 | -3.3 | 3654 | +6.6 | -1.86 |
| QQQ | before 2010 | 134 | -7.4 | 2334 | -0.5 | -0.42 |
| QQQ | from 2010 | 320 | -3.2 | 3667 | +8.6 | -1.85 |

# Pass bar (primary variant `echo21`)

(Bar 2, eras ahead, is read from the tables above.)

- FAIL: 1. `echo21` beats the twin with p < 0.10 on SPY and QQQ both (SPY -0.38 (p = 0.98), QQQ -0.28 (p = 0.92))
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (SPY 23% vs 10%, QQQ 39% vs 19%)
- FAIL: 4. Same sign in both out-of-universe sets (other stock ETFs -0.44, foreign indexes -0.12)
- FAIL: 5. Sharpe above buy-and-hold of the same asset, SPY and QQQ (SPY 0.25 vs 0.63, QQQ 0.13 vs 0.41)
- FAIL: 6. From 2010: not behind the twin, SPY and QQQ (SPY -0.27, QQQ -0.33)

**FAILS train.**
