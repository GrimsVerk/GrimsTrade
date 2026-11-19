# trend-where: keep the trend filter only where its days out were rougher

Card: `trend-where.md`. Train period only (decisions to 2025-11-09), total-return prices, the gym's fills and costs. Each January every asset answers yes (keep the `tsmom12` filter) or no (just hold the slot) from its own past bars. Twin: always-on `tsmom12`. Benchmark: equal weight (buy and hold).

## The six live assets, 1994-2025

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| where-vol | 1.07 (0.18) | +18.9% | 17.5% | 35.3% | 1.7 | 83% | 1.34 | 0.18 | 1.60 | 1.63 | 0.83 | +0.03 (p=0.27; -0.04..+0.10) | 2/5 |
| where-dd | 1.05 (0.18) | +18.4% | 17.5% | 35.7% | 2.4 | 82% | 1.34 | 0.18 | 1.55 | 1.63 | 0.77 | +0.01 (p=0.45; -0.06..+0.07) | 2/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| where-vol | -28% | -4% | -22% | -26% | -3% | -21% | -33% |
| where-dd | -28% | -4% | -22% | -27% | -6% | -22% | -34% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## The same runs from 2003

| Variant | Sharpe | Against `tsmom12` | Growth/yr | Worst loss |
|---|---:|---:|---:|---:|
| where-vol | 1.23 | +0.03 | +22.2% | 35.3% |
| where-dd | 1.20 | +0.00 | +21.5% | 35.7% |
| tsmom12 | 1.20 | - | +20.7% | 36.5% |
| equal-weight | 1.19 | -0.00 | +24.9% | 47.0% |

## The answers, year by year

A row is shown when an answer changed; `-` means not in the book yet.

### `where-vol`

| Refit (first Friday of) | SPY | QQQ | TLT | GLD | BTC | ETH |
|---|---|---|---|---|---|---|
| 1994 | yes | - | - | - | - | - |
| 2000 | yes | yes | - | - | - | - |
| 2003 | yes | yes | yes | - | - | - |
| 2005 | yes | yes | yes | yes | - | - |
| 2009 | yes | yes | no | yes | - | - |
| 2012 | yes | yes | no | yes | yes | - |
| 2015 | yes | yes | no | no | yes | - |
| 2017 | yes | yes | no | no | yes | yes |
| 2019 | yes | yes | no | no | no | yes |
| 2023 | yes | yes | no | no | no | no |

What the last refit saw:

| Asset | Years | Out bars | In bars | Out: volatility a year | In: volatility a year | Keep filter |
|---|---:|---:|---:|---:|---:|---|
| SPY | 30.9 | 1518 | 6268 | 28.9% | 15.5% | yes |
| QQQ | 24.8 | 1379 | 4864 | 40.1% | 21.3% | yes |
| TLT | 21.4 | 1864 | 3528 | 14.1% | 14.8% | no |
| GLD | 19.1 | 1547 | 3264 | 16.4% | 18.4% | no |
| BTC | 12.0 | 1124 | 3254 | 64.7% | 84.6% | no |
| ETH | 7.6 | 980 | 1798 | 86.2% | 95.3% | no |

### `where-dd`

| Refit (first Friday of) | SPY | QQQ | TLT | GLD | BTC | ETH |
|---|---|---|---|---|---|---|
| 1994 | yes | - | - | - | - | - |
| 2000 | yes | yes | - | - | - | - |
| 2003 | yes | yes | yes | - | - | - |
| 2005 | yes | yes | yes | yes | - | - |
| 2009 | yes | yes | no | yes | - | - |
| 2011 | yes | yes | no | no | - | - |
| 2012 | yes | yes | no | no | yes | - |
| 2016 | yes | yes | no | yes | yes | - |
| 2017 | yes | yes | no | yes | yes | yes |
| 2019 | yes | yes | no | yes | no | yes |
| 2023 | yes | yes | yes | yes | no | no |

What the last refit saw:

| Asset | Years | Out bars | In bars | Out: worst chained fall | In: worst chained fall | Keep filter |
|---|---:|---:|---:|---:|---:|---|
| SPY | 30.9 | 1518 | 6268 | 59.0% | 26.7% | yes |
| QQQ | 24.8 | 1379 | 4864 | 73.0% | 39.4% | yes |
| TLT | 21.4 | 1864 | 3528 | 40.8% | 28.1% | yes |
| GLD | 19.1 | 1547 | 3264 | 35.8% | 34.1% | yes |
| BTC | 12.0 | 1124 | 3254 | 66.8% | 80.4% | no |
| ETH | 7.6 | 980 | 1798 | 73.9% | 91.6% | no |

## Out of universe (each set one book, refitted on its own history)

`where-vol` on etf, answers at the last refit: IWM yes, EFA yes, EEM yes, IEF yes, LQD yes, VNQ yes, DBC no, SLV no.

`where-dd` on etf, answers at the last refit: IWM yes, EFA yes, EEM yes, IEF yes, LQD yes, VNQ yes, DBC yes, SLV yes.

### etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| where-vol@etf | 0.65 (0.20) | +5.5% | 8.9% | 16.8% | 2.4 | 71% | 0.81 | 0.51 | 0.55 | 0.66 | +0.05 (p=0.08; -0.01..+0.10) | 3/4 |
| where-dd@etf | 0.53 (0.20) | +4.4% | 8.9% | 19.5% | 2.6 | 71% | 0.81 | 0.24 | 0.50 | 0.45 | -0.07 (p=0.99; -0.14..-0.02) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

`where-vol` on coin, answers at the last refit: LTC no, XRP no, BCH no, ETC no, XLM yes, DASH yes.

`where-dd` on coin, answers at the last refit: LTC no, XRP no, BCH yes, ETC no, XLM yes, DASH yes.

### coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| where-vol@coin | 0.61 (0.34) | +19.3% | 78.6% | 92.4% | 3.8 | 59% | 0.64 | 0.64 | +0.07 (p=0.01; +0.02..+0.13) | 1/2 |
| where-dd@coin | 0.59 (0.34) | +18.2% | 78.3% | 92.4% | 3.8 | 59% | 0.64 | 0.60 | +0.06 (p=0.01; +0.02..+0.11) | 1/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

`where-vol` on idx, answers at the last refit: GSPC yes, N225 yes, FTSE yes, GDAXI yes.

`where-dd` on idx, answers at the last refit: GSPC yes, N225 yes, FTSE yes, GDAXI yes.

### idx, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| where-vol@idx | 0.72 (0.13) | +6.2% | 9.0% | 27.4% | 2.3 | 72% | 0.72 | 1.00 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | -0.00 (p=0.50; -0.04..+0.04) | 3/7 |
| where-dd@idx | 0.69 (0.13) | +6.1% | 9.2% | 30.3% | 2.2 | 73% | 0.67 | 1.00 | 1.24 | 0.33 | 0.37 | 0.33 | 0.79 | -0.03 (p=0.80; -0.09..+0.02) | 2/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.7% | 2.3 | 70% | 0.76 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| equal-weight@idx | 0.62 (0.13) | +7.5% | 13.1% | 57.6% | 0.2 | 100% | 0.71 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | -0.10 (p=0.84; -0.27..+0.07) | 5/7 |

## Pass bar (each variant judged alone)

### `where-vol`

- FAIL: 1. Sharpe beats `tsmom12` with p < 0.05 (difference +0.03, p = 0.27)
- PASS: 2. Worst loss not more than 5 points worse (35.3% vs 36.5%)
- PASS: 3. Since 2003: not behind on Sharpe, worst loss not more than 5 points worse (difference +0.03; 35.3% vs 36.5%)
- PASS: 4. Out of universe: Sharpe up in 2 of 3 sets, worst loss within 5 points in 2 of 3 (etf +0.05, 16.8% vs 16.5%; coin +0.07, 92.4% vs 92.4%; idx -0.00, 27.4% vs 25.7%)
- PASS: 5. Beats equal weight on Sharpe (1.07 vs 0.88)

**FAILS train.**

### `where-dd`

- FAIL: 1. Sharpe beats `tsmom12` with p < 0.05 (difference +0.01, p = 0.45)
- PASS: 2. Worst loss not more than 5 points worse (35.7% vs 36.5%)
- PASS: 3. Since 2003: not behind on Sharpe, worst loss not more than 5 points worse (difference +0.00; 35.7% vs 36.5%)
- FAIL: 4. Out of universe: Sharpe up in 2 of 3 sets, worst loss within 5 points in 2 of 3 (etf -0.07, 19.5% vs 16.5%; coin +0.06, 92.4% vs 92.4%; idx -0.03, 30.3% vs 25.7%)
- PASS: 5. Beats equal weight on Sharpe (1.05 vs 0.88)

**FAILS train.**

## Held-out year

Not looked at (the card: not in this run, pass or fail).
