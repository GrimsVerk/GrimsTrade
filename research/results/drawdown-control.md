# drawdown-control: sell gradually into a drawdown

Card: `cards/drawdown-control.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs sma200 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d1.0 | 1.08 (0.18) | +14.6% | 13.5% | 37.2% | 3.5 | 64% | 1.22 | 0.05 | 1.67 | 1.76 | 0.70 | +0.07 (p=0.14; -0.03..+0.18) | 3/5 |
| d1.5 | 1.04 (0.18) | +16.0% | 15.5% | 48.1% | 2.6 | 75% | 1.29 | 0.02 | 1.70 | 1.70 | 0.70 | +0.03 (p=0.36; -0.11..+0.17) | 3/5 |
| sma200 | 1.01 (0.18) | +15.9% | 15.8% | 44.4% | 4.3 | 70% | 1.14 | 0.14 | 1.58 | 1.53 | 0.75 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.13 (p=0.83; -0.34..+0.09) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| d1.0 | -36% | -2% | -13% | -20% | -8% | -19% | -26% |
| d1.5 | -48% | -6% | -15% | -26% | -11% | -29% | -32% |
| sma200 | -33% | +2% | -14% | -12% | -4% | -23% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: d1.0 +13.6%, d1.5 +14.9%, sma200 +14.7%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs sma200@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d1.0@etf | 0.47 (0.20) | +3.3% | 7.5% | 17.4% | 3.0 | 60% | 0.52 | 0.39 | 0.67 | 0.31 | -0.06 (p=0.78; -0.19..+0.07) | 2/4 |
| sma200@etf | 0.53 (0.20) | +4.3% | 8.6% | 16.8% | 3.9 | 65% | 0.67 | 0.36 | 0.66 | 0.31 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.05 (p=0.60; -0.30..+0.20) | 3/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs sma200@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d1.0@coin | 0.67 (0.33) | +26.6% | 65.1% | 79.4% | 3.6 | 56% | 0.85 | 0.38 | +0.18 (p=0.06; -0.01..+0.36) | 1/2 |
| sma200@coin | 0.50 (0.34) | +11.3% | 73.1% | 89.8% | 6.1 | 46% | 0.59 | 0.38 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.22 (p=0.10; -0.07..+0.53) | 2/2 |

## Out of universe: GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs sma200@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d1.0@GSPC | 0.58 (0.18) | +4.3% | 7.7% | 15.5% | 3.9 | 57% | 0.41 | 0.76 | -0.16 (p=0.99; -0.27..-0.05) | 0/2 |
| sma200@GSPC | 0.74 (0.18) | +6.8% | 9.5% | 20.5% | 2.7 | 66% | 0.58 | 0.91 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | -0.25 (p=0.95; -0.48..+0.00) | 0/2 |

## Out of universe: N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs sma200@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d1.0@N225 | 0.43 (0.13) | +4.1% | 10.7% | 38.2% | 3.5 | 58% | 0.63 | 0.80 | 0.10 | 0.05 | 0.23 | 0.25 | 0.75 | +0.03 (p=0.32; -0.07..+0.12) | 4/7 |
| sma200@N225 | 0.41 (0.13) | +4.5% | 12.9% | 47.5% | 3.5 | 63% | 0.75 | 0.74 | 0.15 | 0.13 | 0.20 | -0.13 | 0.58 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.01 (p=0.52; -0.18..+0.16) | 5/7 |

## Out of universe: FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs sma200@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d1.0@FTSE | 0.32 (0.16) | +2.5% | 9.3% | 27.7% | 3.8 | 64% | 0.75 | 0.74 | 0.08 | -0.04 | -0.19 | 0.35 | +0.08 (p=0.12; -0.03..+0.18) | 4/6 |
| sma200@FTSE | 0.24 (0.16) | +2.0% | 10.9% | 43.0% | 4.6 | 68% | 0.50 | 0.71 | 0.21 | -0.24 | -0.15 | 0.04 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.15 (p=0.11; -0.05..+0.34) | 5/6 |

## Out of universe: GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs sma200@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d1.0@GDAXI | 0.53 (0.17) | +5.6% | 11.7% | 25.7% | 3.6 | 63% | 0.52 | 1.12 | 0.46 | 0.39 | 0.22 | 0.37 | -0.02 (p=0.62; -0.13..+0.09) | 3/6 |
| sma200@GDAXI | 0.55 (0.17) | +7.1% | 14.4% | 40.9% | 2.6 | 70% | 0.71 | 0.66 | 0.62 | 0.31 | 0.09 | 1.00 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | -0.08 (p=0.73; -0.30..+0.12) | 3/6 |

## Pass bar (primary variant `d1.0`)

- FAIL: 1. Sharpe beats twin `sma200` with p < 0.10 (difference +0.07, p = 0.14)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (3 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (37.2% vs 44.4%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.06, coin +0.18, idx -0.02)
- PASS: 5. Beats equal weight on Sharpe (1.08 vs 0.88)

**FAILS train.**
## Verdict (2026-11-12)

Dead as a replacement for the 200-day switch: it is the same thing. Sharpe 1.08 against 1.01
(p = 0.14), ahead in 3 of 5 eras, slightly better on the coins, slightly worse on the other ETFs
and the indexes. Selling gradually is not measurably better than selling at a crossing. If the
M1 lane wants a smoother version of its trend rule (lower turnover: 3.5 versus 4.3 a year, lower
drawdown: 37% versus 44%), this is one, but nothing here says it earns more.
