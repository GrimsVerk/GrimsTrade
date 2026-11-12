# month-end-liquidity: the turn-of-month window

Card: `cards/month-end-liquidity.md`. Twin `constant` holds the same asset at the rule's average exposure. `equal-weight` is buy-and-hold of the asset.

## SPY, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@SPY (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@SPY | 0.56 (0.18) | +5.6% | 10.8% | 18.9% | 24.0 | 34% | 0.82 | 0.43 | 0.60 | 0.75 | 0.25 | -0.07 (p=0.68; -0.33..+0.20) | 1/5 |
| constant@SPY | 0.63 (0.18) | +3.9% | 6.4% | 22.0% | 0.1 | 34% | 1.36 | 0.06 | 0.85 | 0.98 | 0.67 | - | - |
| equal-weight@SPY | 0.63 (0.18) | +10.6% | 18.9% | 55.2% | 0.0 | 100% | 1.35 | 0.07 | 0.85 | 0.99 | 0.68 | +0.00 (p=0.23; -0.00..+0.01) | 4/5 |

Mean open-to-open return per day held +7.7 bps (2669 days), per day not held +3.2 bps (5327 days), Welch t = 1.61. Days held before 2014-01-01: +8.7 bps; from 2014-01-01: +6.0 bps. Sharpe difference to the twin from 2014-01-01: -0.35.

## QQQ, from 2000-03-10

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@QQQ (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@QQQ | 0.34 (0.20) | +4.2% | 15.4% | 46.9% | 24.0 | 34% | 0.12 | 0.62 | 0.84 | 0.29 | -0.07 (p=0.66; -0.33..+0.20) | 1/4 |
| constant@QQQ | 0.41 (0.20) | +3.3% | 9.0% | 40.4% | 0.2 | 34% | -0.09 | 0.94 | 1.22 | 0.63 | - | - |
| equal-weight@QQQ | 0.41 (0.20) | +7.7% | 26.5% | 83.0% | 0.0 | 100% | -0.09 | 0.94 | 1.23 | 0.63 | +0.00 (p=0.36; -0.00..+0.01) | 2/4 |

Mean open-to-open return per day held +6.9 bps (2156 days), per day not held +3.2 bps (4299 days), Welch t = 0.83. Days held before 2014-01-01: +6.3 bps; from 2014-01-01: +7.6 bps. Sharpe difference to the twin from 2014-01-01: -0.44.

## TLT, from 2003-07-31

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@TLT (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@TLT | 0.15 (0.21) | +0.9% | 8.4% | 25.7% | 24.0 | 34% | 0.00 | 0.10 | 0.33 | 0.23 | -0.18 (p=0.87; -0.45..+0.09) | 1/4 |
| constant@TLT | 0.32 (0.21) | +1.5% | 4.9% | 19.3% | 0.1 | 34% | 0.53 | 0.54 | 0.53 | -0.49 | - | - |
| equal-weight@TLT | 0.33 (0.21) | +3.8% | 14.5% | 48.4% | 0.0 | 100% | 0.52 | 0.55 | 0.53 | -0.49 | +0.00 (p=0.20; -0.00..+0.01) | 3/4 |

Mean open-to-open return per day held +2.0 bps (1872 days), per day not held +1.8 bps (3733 days), Welch t = 0.08. Days held before 2014-01-01: +0.9 bps; from 2014-01-01: +2.9 bps. Sharpe difference to the twin from 2014-01-01: +0.06.

# Out of universe: other ETFs

## IWM, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@IWM (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@IWM | 0.41 (0.20) | +4.8% | 13.6% | 25.1% | 24.0 | 34% | 0.60 | 0.45 | 0.32 | 0.00 | -0.03 (p=0.59; -0.34..+0.27) | 1/4 |
| constant@IWM | 0.44 (0.20) | +3.3% | 8.0% | 23.2% | 0.2 | 34% | 0.27 | 0.71 | 0.59 | 0.27 | - | - |
| equal-weight@IWM | 0.44 (0.20) | +8.0% | 23.8% | 58.6% | 0.0 | 100% | 0.27 | 0.71 | 0.59 | 0.27 | +0.00 (p=0.40; -0.01..+0.01) | 3/4 |

Mean open-to-open return per day held +7.3 bps (2056 days), per day not held +2.7 bps (4093 days), Welch t = 1.13. Days held before 2014-01-01: +11.4 bps; from 2014-01-01: +2.9 bps. Sharpe difference to the twin from 2014-01-01: -0.30.

## EFA, from 2002-08-28

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@EFA (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@EFA | 0.41 (0.21) | +4.2% | 11.5% | 26.4% | 24.0 | 34% | 0.84 | 0.15 | 0.34 | -0.06 | -0.02 (p=0.58; -0.33..+0.26) | 1/4 |
| constant@EFA | 0.44 (0.21) | +2.8% | 7.0% | 25.6% | 0.1 | 34% | 0.46 | 0.27 | 0.60 | 0.54 | - | - |
| equal-weight@EFA | 0.45 (0.21) | +7.4% | 20.8% | 61.0% | 0.0 | 100% | 0.47 | 0.28 | 0.61 | 0.54 | +0.01 (p=0.00; +0.00..+0.02) | 3/4 |

Mean open-to-open return per day held +6.1 bps (1949 days), per day not held +2.3 bps (3888 days), Welch t = 1.17. Days held before 2014-01-01: +11.9 bps; from 2014-01-01: +0.6 bps. Sharpe difference to the twin from 2014-01-01: -0.44.

## EEM, from 2004-04-14

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@EEM (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@EEM | 0.59 (0.21) | +8.3% | 15.6% | 34.2% | 24.0 | 34% | 0.78 | 0.63 | 0.44 | 0.34 | +0.22 (p=0.10; -0.06..+0.47) | 2/4 |
| constant@EEM | 0.37 (0.21) | +3.0% | 9.2% | 28.2% | 0.2 | 34% | 0.54 | 0.08 | 0.51 | 0.39 | - | - |
| equal-weight@EEM | 0.38 (0.21) | +7.0% | 27.4% | 66.4% | 0.0 | 100% | 0.57 | 0.09 | 0.52 | 0.39 | +0.01 (p=0.00; +0.00..+0.02) | 3/4 |

Mean open-to-open return per day held +11.2 bps (1813 days), per day not held +0.3 bps (3615 days), Welch t = 2.48. Days held before 2014-01-01: +19.2 bps; from 2014-01-01: +4.6 bps. Sharpe difference to the twin from 2014-01-01: -0.05.

## IEF, from 2003-07-31

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@IEF (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@IEF | 0.42 (0.21) | +1.6% | 4.0% | 11.4% | 24.0 | 34% | 0.18 | 0.47 | 0.71 | 0.46 | -0.13 (p=0.78; -0.42..+0.17) | 2/4 |
| constant@IEF | 0.55 (0.21) | +1.2% | 2.3% | 8.6% | 0.0 | 34% | 0.79 | 0.73 | 0.69 | -0.14 | - | - |
| equal-weight@IEF | 0.55 (0.21) | +3.5% | 6.8% | 23.9% | 0.0 | 100% | 0.78 | 0.74 | 0.68 | -0.14 | -0.01 (p=0.94; -0.01..+0.00) | 1/4 |

Mean open-to-open return per day held +2.6 bps (1872 days), per day not held +0.9 bps (3733 days), Welch t = 1.36. Days held before 2014-01-01: +2.0 bps; from 2014-01-01: +3.0 bps. Sharpe difference to the twin from 2014-01-01: +0.20.

## LQD, from 2003-07-31

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@LQD (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@LQD | 0.51 (0.22) | +2.4% | 4.9% | 11.6% | 24.0 | 34% | 0.38 | 0.75 | 0.99 | 0.28 | -0.05 (p=0.58; -0.34..+0.27) | 2/4 |
| constant@LQD | 0.56 (0.21) | +1.6% | 2.8% | 9.1% | 0.0 | 34% | 0.56 | 1.02 | 0.67 | -0.02 | - | - |
| equal-weight@LQD | 0.55 (0.21) | +4.4% | 8.4% | 25.0% | 0.0 | 100% | 0.55 | 1.02 | 0.67 | -0.02 | -0.00 (p=0.84; -0.01..+0.00) | 1/4 |

Mean open-to-open return per day held +3.5 bps (1872 days), per day not held +1.0 bps (3733 days), Welch t = 1.67. Days held before 2014-01-01: +3.9 bps; from 2014-01-01: +3.2 bps. Sharpe difference to the twin from 2014-01-01: +0.11.

# Out of universe: indexes

## GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs constant@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@GSPC | 0.81 (0.18) | +6.3% | 7.9% | 28.4% | 24.0 | 34% | 0.55 | 1.14 | +0.32 (p=0.06; -0.01..+0.63) | 2/2 |
| constant@GSPC | 0.50 (0.18) | +2.3% | 4.8% | 19.3% | 0.1 | 34% | 0.27 | 0.74 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | -0.00 (p=0.82; -0.01..+0.00) | 0/2 |

Mean open-to-open return per day held +8.2 bps (2607 days), per day not held -0.0 bps (5211 days), Welch t = 3.98. Days held before 2014-01-01: +8.2 bps; from 2014-01-01: +nan bps. Sharpe difference to the twin from 2014-01-01: +0.00.

## N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@N225 | 0.50 (0.13) | +5.3% | 11.6% | 38.9% | 24.0 | 35% | 1.01 | 0.77 | 0.13 | 0.59 | 0.17 | 0.06 | -0.09 | +0.11 (p=0.20; -0.11..+0.31) | 3/7 |
| constant@N225 | 0.40 (0.13) | +2.5% | 7.0% | 38.5% | 0.2 | 35% | 0.84 | 0.48 | 0.16 | -0.11 | 0.48 | 0.53 | 0.79 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | +0.00 (p=0.42; -0.00..+0.00) | 4/7 |

Mean open-to-open return per day held +7.4 bps (5026 days), per day not held +0.9 bps (9688 days), Welch t = 3.13. Days held before 2014-01-01: +9.3 bps; from 2014-01-01: -0.0 bps. Sharpe difference to the twin from 2014-01-01: -0.61.

## FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@FTSE | 0.72 (0.16) | +6.7% | 9.6% | 20.7% | 24.0 | 34% | 1.14 | 1.15 | 0.68 | 0.43 | 0.38 | 0.40 | +0.34 (p=0.01; +0.07..+0.58) | 5/6 |
| constant@FTSE | 0.38 (0.16) | +2.1% | 5.9% | 21.2% | 0.1 | 34% | 0.83 | 0.85 | -0.01 | 0.32 | 0.11 | 0.65 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.00 (p=0.11; -0.00..+0.01) | 4/6 |

Mean open-to-open return per day held +8.8 bps (3431 days), per day not held -0.5 bps (6887 days), Welch t = 4.21. Days held before 2014-01-01: +10.8 bps; from 2014-01-01: +3.8 bps. Sharpe difference to the twin from 2014-01-01: +0.03.

## GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| window@GDAXI | 0.64 (0.16) | +7.5% | 12.6% | 33.0% | 24.0 | 34% | 0.94 | 1.06 | 0.86 | 0.07 | 0.35 | 0.30 | +0.17 (p=0.15; -0.10..+0.42) | 3/6 |
| constant@GDAXI | 0.47 (0.17) | +3.3% | 7.4% | 33.2% | 0.2 | 34% | 0.66 | 1.02 | 0.08 | 0.55 | 0.43 | 0.71 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | -0.00 (p=0.81; -0.01..+0.00) | 3/6 |

Mean open-to-open return per day held +10.0 bps (3096 days), per day not held +1.1 bps (6226 days), Welch t = 3.00. Days held before 2014-01-01: +13.9 bps; from 2014-01-01: +1.6 bps. Sharpe difference to the twin from 2014-01-01: -0.43.

# Pass bar

(Bar 2, eras ahead, is read from the tables above.)

- FAIL: 1. Sharpe beats the twin with p < 0.10 on SPY and TLT both (SPY -0.07 (p = 0.68), QQQ -0.07 (p = 0.66), TLT -0.18 (p = 0.87))
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (SPY 19% vs 22%, QQQ 47% vs 40%, TLT 26% vs 19%)
- FAIL: 4. Same sign out of universe in both applicable sets (other ETFs -0.00, indexes +0.23)
- FAIL: 5. (card) Sharpe above buy-and-hold of the same asset, SPY and TLT (SPY 0.56 vs 0.63, QQQ 0.34 vs 0.41, TLT 0.15 vs 0.33)
- FAIL: 6. (card) Not behind the twin after the paper's sample, 2014-2025, SPY and TLT (SPY -0.35, QQQ -0.44, TLT +0.06)

**FAILS train.**

## Verdict (2026-11-12)

Dead as a strategy; the effect itself was real and has faded.

- The window days did earn more. SPY: 7.7 bps a day inside against 3.2 outside (t = 1.6). In
  markets and decades the rule was not designed on it is unmistakable: S&P 500 index 1962-1993,
  8.2 against 0.0 bps (t = 4.0); FTSE t = 4.2; Nikkei t = 3.1; DAX t = 3.0. On those four indexes
  the rule beat its twin by +0.23 Sharpe on average.
- It has decayed since the paper's sample ended. From 2014 the window days earn 0.0 bps on the
  Nikkei, 1.6 on the DAX, 0.6 on EFA, 2.9 on IWM; on SPY and QQQ the rule is behind its twin by
  0.35 and 0.44 Sharpe. TLT never showed it (2.0 against 1.8 bps).
- Even where it worked it does not suit our gym. The rule is fully invested a third of the time;
  a constant one-third holding takes the same average risk far more smoothly, and cash earns 0
  the rest of the month. On SPY the rule's Sharpe is 0.56 against 0.63 for the constant holding.
  Earning double per day is not enough to pay for bunching the risk.

Practical leftover, not a strategy: when the paper system has to buy stocks anyway, a few days
before month end has been a better time than a few days after.
