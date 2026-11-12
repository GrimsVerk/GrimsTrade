# dip-rsi2: buying short-term dips in stock indexes

Card: `cards/dip-rsi2.md`. Twin `constant` holds the same asset at the rule's average exposure. `equal-weight` is buy-and-hold of the asset.

## SPY, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@SPY (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rsi2@SPY | 0.50 (0.17) | +2.3% | 4.7% | 11.8% | 7.9 | 5% | 0.94 | 0.46 | 0.35 | 0.26 | 0.46 | -0.15 (p=0.78; -0.49..+0.17) | 1/5 |
| constant@SPY | 0.65 (0.18) | +0.6% | 0.9% | 3.3% | 0.0 | 5% | 1.30 | 0.07 | 0.83 | 1.06 | 0.73 | - | - |
| equal-weight@SPY | 0.63 (0.18) | +10.6% | 18.9% | 55.2% | 0.0 | 100% | 1.35 | 0.07 | 0.85 | 0.99 | 0.68 | -0.02 (p=0.91; -0.05..+0.00) | 2/5 |

Mean open-to-open return per day held +21.6 bps (376 days), per day not held +3.9 bps (7620 days), Welch t = 2.47. Days held before 2009-01-01: +32.3 bps; from 2009-01-01: +14.5 bps. Sharpe difference to the twin from 2009-01-01: -0.49.

## QQQ, from 2000-03-10

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@QQQ (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rsi2@QQQ | 0.32 (0.19) | +1.9% | 6.3% | 16.5% | 8.0 | 5% | 0.32 | 0.18 | 0.40 | 0.63 | -0.10 (p=0.68; -0.44..+0.24) | 1/4 |
| constant@QQQ | 0.42 (0.20) | +0.5% | 1.3% | 7.0% | 0.0 | 5% | -0.11 | 0.89 | 1.26 | 0.70 | - | - |
| equal-weight@QQQ | 0.41 (0.20) | +7.7% | 26.5% | 83.0% | 0.0 | 100% | -0.09 | 0.94 | 1.23 | 0.63 | -0.01 (p=0.71; -0.03..+0.02) | 2/4 |

Mean open-to-open return per day held +17.5 bps (327 days), per day not held +3.7 bps (6128 days), Welch t = 1.29. Days held before 2009-01-01: +21.9 bps; from 2009-01-01: +15.7 bps. Sharpe difference to the twin from 2009-01-01: -0.70.

# Out of universe: other ETFs

## IWM, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@IWM (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rsi2@IWM | 0.41 (0.20) | +1.9% | 4.9% | 15.0% | 7.9 | 5% | 0.41 | 0.44 | 0.26 | 0.59 | -0.03 (p=0.57; -0.40..+0.34) | 2/4 |
| constant@IWM | 0.44 (0.20) | +0.5% | 1.2% | 3.9% | 0.0 | 5% | 0.28 | 0.68 | 0.56 | 0.30 | - | - |
| equal-weight@IWM | 0.44 (0.20) | +8.0% | 23.8% | 58.6% | 0.0 | 100% | 0.27 | 0.71 | 0.59 | 0.27 | +0.00 (p=0.43; -0.02..+0.03) | 2/4 |

Mean open-to-open return per day held +16.9 bps (312 days), per day not held +3.6 bps (5837 days), Welch t = 1.61. Days held before 2009-01-01: +11.2 bps; from 2009-01-01: +18.9 bps. Sharpe difference to the twin from 2009-01-01: -0.12.

## EFA, from 2002-08-28

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@EFA (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rsi2@EFA | 0.35 (0.21) | +1.3% | 3.9% | 9.4% | 7.0 | 5% | 0.40 | 0.05 | 0.63 | 0.68 | -0.08 (p=0.63; -0.46..+0.30) | 1/4 |
| constant@EFA | 0.43 (0.21) | +0.4% | 1.0% | 4.0% | 0.0 | 5% | 0.47 | 0.21 | 0.66 | 0.49 | - | - |
| equal-weight@EFA | 0.45 (0.21) | +7.4% | 20.8% | 61.0% | 0.0 | 100% | 0.47 | 0.28 | 0.61 | 0.54 | +0.02 (p=0.19; -0.01..+0.05) | 3/4 |

Mean open-to-open return per day held +13.3 bps (261 days), per day not held +3.1 bps (5576 days), Welch t = 1.60. Days held before 2009-01-01: +9.2 bps; from 2009-01-01: +14.6 bps. Sharpe difference to the twin from 2009-01-01: -0.05.

## EEM, from 2004-04-14

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@EEM (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rsi2@EEM | 0.19 (0.22) | +0.8% | 4.7% | 11.2% | 6.9 | 4% | 0.13 | 0.37 | 0.17 | 0.11 | -0.15 (p=0.76; -0.53..+0.23) | 1/4 |
| constant@EEM | 0.35 (0.21) | +0.4% | 1.2% | 3.8% | 0.0 | 4% | 0.53 | 0.03 | 0.47 | 0.43 | - | - |
| equal-weight@EEM | 0.38 (0.21) | +7.0% | 27.4% | 66.4% | 0.0 | 100% | 0.57 | 0.09 | 0.52 | 0.39 | +0.04 (p=0.04; +0.00..+0.07) | 3/4 |

Mean open-to-open return per day held +9.8 bps (229 days), per day not held +3.7 bps (5199 days), Welch t = 0.66. Days held before 2009-01-01: +6.9 bps; from 2009-01-01: +10.6 bps. Sharpe difference to the twin from 2009-01-01: -0.15.

# Out of universe: indexes

## GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs constant@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rsi2@GSPC | 0.19 (0.18) | +0.5% | 3.1% | 22.0% | 10.3 | 7% | -0.46 | 0.84 | -0.33 (p=0.93; -0.75..+0.05) | 1/2 |
| constant@GSPC | 0.52 (0.18) | +0.5% | 1.0% | 4.2% | 0.0 | 7% | 0.31 | 0.75 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | -0.03 (p=0.99; -0.05..-0.01) | 0/2 |

Mean open-to-open return per day held +4.3 bps (564 days), per day not held +2.6 bps (7254 days), Welch t = 0.53. Days held before 2009-01-01: +4.3 bps; from 2009-01-01: +nan bps. Sharpe difference to the twin from 2009-01-01: +0.00.

## N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rsi2@N225 | 0.19 (0.13) | +0.7% | 4.4% | 18.8% | 7.0 | 5% | 0.13 | 0.37 | 0.19 | -0.25 | 0.24 | 0.50 | 0.38 | -0.23 (p=0.93; -0.47..+0.02) | 1/7 |
| constant@N225 | 0.42 (0.13) | +0.4% | 1.0% | 5.6% | 0.0 | 5% | 0.84 | 0.52 | 0.18 | -0.07 | 0.48 | 0.55 | 0.79 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.02 (p=0.98; -0.04..-0.00) | 2/7 |

Mean open-to-open return per day held +7.7 bps (747 days), per day not held +2.9 bps (13967 days), Welch t = 1.05. Days held before 2009-01-01: +5.4 bps; from 2009-01-01: +14.4 bps. Sharpe difference to the twin from 2009-01-01: -0.30.

## FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rsi2@FTSE | 0.20 (0.16) | +0.6% | 3.4% | 12.4% | 7.1 | 5% | -0.01 | 0.71 | 0.18 | 0.31 | 0.25 | -0.45 | -0.19 (p=0.82; -0.51..+0.15) | 3/6 |
| constant@FTSE | 0.39 (0.16) | +0.3% | 0.8% | 3.3% | 0.0 | 5% | 0.84 | 0.85 | 0.01 | 0.27 | 0.11 | 0.63 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | -0.00 (p=0.60; -0.03..+0.02) | 4/6 |

Mean open-to-open return per day held +7.0 bps (492 days), per day not held +2.4 bps (9826 days), Welch t = 1.01. Days held before 2009-01-01: +7.5 bps; from 2009-01-01: +6.0 bps. Sharpe difference to the twin from 2009-01-01: -0.22.

## GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rsi2@GDAXI | 0.26 (0.17) | +1.1% | 4.7% | 17.1% | 7.3 | 5% | -0.18 | 0.60 | 0.25 | 0.33 | -0.46 | 0.86 | -0.21 (p=0.83; -0.55..+0.14) | 2/6 |
| constant@GDAXI | 0.48 (0.17) | +0.5% | 1.1% | 5.3% | 0.0 | 5% | 0.62 | 1.03 | 0.09 | 0.54 | 0.45 | 0.69 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | -0.01 (p=0.77; -0.03..+0.01) | 3/6 |

Mean open-to-open return per day held +11.4 bps (443 days), per day not held +3.6 bps (8879 days), Welch t = 1.19. Days held before 2009-01-01: +13.1 bps; from 2009-01-01: +9.2 bps. Sharpe difference to the twin from 2009-01-01: -0.40.

# What the next-open fill costs

SPY: +21.4 bps per day held at close fills (376 days); QQQ: +18.7 bps per day held at close fills (327 days).

# Pass bar

(Bar 2, eras ahead, is read from the tables above.)

- FAIL: 1. Sharpe beats the twin with p < 0.10 on SPY and QQQ both (SPY -0.15 (p = 0.78), QQQ -0.10 (p = 0.68))
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (SPY 12% vs 3%, QQQ 16% vs 7%)
- FAIL: 4. Same sign out of universe in both applicable sets (other ETFs -0.09, indexes -0.24)
- FAIL: 5. (card) Return per day held above other days, t > 2, SPY and QQQ (SPY t = 2.47, QQQ t = 1.29)
- FAIL: 6. (card) Not behind the twin after publication, 2009-2025 (SPY -0.49, QQQ -0.70)

**FAILS train.**

## Verdict (2026-11-12)

Dead for our purposes. The bounce is real on SPY: 21.6 bps per day held against 3.9 on other
days (t = 2.5), and the next-open fill costs nothing (21.4 bps at close fills). But:

- it halved after publication (32 bps a day before 2009, 14.5 since), and behind its twin on Sharpe
  since 2009 on both SPY and QQQ;
- it is weak everywhere it was not designed: t between 0.5 and 1.6 on QQQ, IWM, EFA, EEM, the
  old S&P 500 index, the Nikkei, FTSE and DAX, and behind the twin on Sharpe in all seven;
- it is in the market 5% of the time. Unlevered that is +2.3% a year on SPY. A constant 5%
  holding has a better Sharpe (0.65 against 0.50) because the rule buys exactly when volatility
  is highest.

A dip rule only pays with leverage or as a way to time purchases already planned. Not for M3.
