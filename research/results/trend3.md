# trend3: long SPY, GLD, BTC above the long average

Card: `cards/trend3.md`. Protocol: `protocol.md`. Shared rules: `cards/yt-1.md`. 'six' = SPY, GLD, BTC here; out of universe the variant is `sma200` itself.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@trend3 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trend3-sma200@trend3 | 1.10 (0.18) | +19.8% | 17.9% | 34.7% | 4.1 | 73% | 1.14 | 0.36 | 1.46 | 1.43 | 1.23 | -0.01 (p=0.56; -0.15..+0.13) | 2/5 |
| trend3-10m@trend3 | 1.08 (0.18) | +19.7% | 18.2% | 30.0% | 3.9 | 74% | 1.16 | 0.38 | 1.50 | 1.31 | 1.20 | -0.03 (p=0.65; -0.15..+0.09) | 1/5 |
| tsmom12@trend3 | 1.11 (0.18) | +21.4% | 19.2% | 34.7% | 2.7 | 77% | 1.34 | 0.42 | 1.34 | 1.37 | 1.39 | - | - |
| equal-weight@trend3 | 1.05 (0.18) | +23.1% | 22.1% | 47.5% | 1.5 | 100% | 1.35 | 0.29 | 1.42 | 1.52 | 1.03 | -0.05 (p=0.71; -0.21..+0.10) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| trend3-sma200@trend3 | -24% | -1% | -9% | -5% | -20% | -26% | -17% |
| trend3-10m@trend3 | -24% | -1% | -18% | -7% | -20% | -30% | -19% |
| tsmom12@trend3 | -16% | -11% | -21% | -10% | -22% | -28% | -18% |
| equal-weight@trend3 | -48% | -22% | -23% | -32% | -38% | -41% | -39% |

Annualised log growth: trend3-sma200@trend3 +18.1%, trend3-10m@trend3 +18.0%, tsmom12@trend3 +19.4%, equal-weight@trend3 +20.8%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trend3-sma200@etf | 0.53 (0.20) | +4.3% | 8.6% | 16.8% | 3.9 | 65% | 0.67 | 0.36 | 0.66 | 0.31 | -0.07 (p=0.73; -0.24..+0.12) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trend3-sma200@coin | 0.50 (0.34) | +11.3% | 73.1% | 89.8% | 6.1 | 46% | 0.59 | 0.38 | -0.04 (p=0.61; -0.29..+0.21) | 0/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

## Out of universe: GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trend3-sma200@GSPC | 0.74 (0.18) | +6.8% | 9.5% | 20.5% | 2.7 | 66% | 0.58 | 0.91 | +0.29 (p=0.01; +0.10..+0.47) | 2/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | 0.26 | 0.62 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.05 (p=0.38; -0.18..+0.25) | 2/2 |

## Out of universe: N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trend3-sma200@N225 | 0.41 (0.13) | +4.5% | 12.9% | 47.5% | 3.5 | 63% | 0.75 | 0.74 | 0.15 | 0.13 | 0.20 | -0.13 | 0.58 | -0.14 (p=0.96; -0.28..-0.01) | 1/7 |
| tsmom12@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | 0.77 | 0.72 | 0.35 | 0.33 | 0.24 | 0.54 | 0.81 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.15 (p=0.94; -0.31..+0.01) | 3/7 |

## Out of universe: FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trend3-sma200@FTSE | 0.24 (0.16) | +2.0% | 10.9% | 43.0% | 4.6 | 68% | 0.50 | 0.71 | 0.21 | -0.24 | -0.15 | 0.04 | -0.13 (p=0.94; -0.28..+0.01) | 0/6 |
| tsmom12@FTSE | 0.37 (0.16) | +3.7% | 11.8% | 39.1% | 2.7 | 71% | 0.64 | 0.72 | 0.36 | -0.07 | -0.02 | 0.20 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.01 (p=0.43; -0.18..+0.20) | 5/6 |

## Out of universe: GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trend3-sma200@GDAXI | 0.55 (0.17) | +7.1% | 14.4% | 40.9% | 2.6 | 70% | 0.71 | 0.66 | 0.62 | 0.31 | 0.09 | 1.00 | +0.15 (p=0.09; -0.03..+0.34) | 4/6 |
| tsmom12@GDAXI | 0.40 (0.17) | +5.0% | 15.1% | 58.9% | 1.8 | 69% | 0.62 | 0.68 | 0.46 | 0.42 | -0.47 | 0.44 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | +0.07 (p=0.30; -0.14..+0.28) | 5/6 |

## Pass bar (primary variant `trend3-sma200`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.01, p = 0.56)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (34.7% vs 34.7%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.07, coin -0.04, idx +0.04)
- PASS: 5. Beats equal weight on Sharpe (1.10 vs 1.05)

**FAILS train.**

## Since 2003

| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |
|---|---:|---:|---:|---:|
| trend3-sma200@trend3 | 1.25 | +24.9% | 27.6% | +0.06 (0.27) |
| trend3-10m@trend3 | 1.22 | +24.6% | 30.0% | +0.04 (0.34) |
| tsmom12@trend3 | 1.18 | +24.8% | 34.7% |  |
| equal-weight@trend3 | 1.23 | +29.2% | 41.7% | +0.04 (0.33) |
