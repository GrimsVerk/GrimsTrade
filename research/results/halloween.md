# halloween: stock trend slots only from November to April

Card: `cards/halloween.md`. Survey: `survey-4.md` (pick B). Protocol: `protocol.md`. No-look-ahead check against `gym.backtest` on 1999-10-01, 2008-10-10, 2018-12-21, 2023-06-02: passed.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| halloween | 0.96 (0.18) | +14.3% | 15.0% | 38.8% | 3.2 | 51% | 1.31 | 0.15 | 1.46 | 1.39 | 0.67 | -0.08 (p=0.87; -0.20..+0.04) | 0/5 |
| halloween-alone | 0.88 (0.18) | +14.4% | 17.0% | 49.4% | 3.0 | 58% | 1.31 | 0.03 | 1.51 | 1.43 | 0.79 | -0.17 (p=0.95; -0.35..+0.00) | 0/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| halloween | -23% | -1% | -21% | -14% | -10% | -23% | -20% |
| halloween-alone | -42% | -10% | -22% | -14% | -10% | -23% | -19% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Sharpe above T-bills with T-bill interest on cash (`cash_interest.rescored`; no row):

- `halloween`: 0.89 (gym: 0.96)
- `halloween-alone`: 0.80 (gym: 0.88)
- `tsmom12`: 0.93 (gym: 1.05)
- `equal-weight`: 0.77 (gym: 0.88)

## Out of universe

Other ETFs (gate on IWM, EFA, EEM):

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| halloween@etf | 0.69 (0.21) | +4.6% | 6.8% | 16.5% | 2.7 | 51% | 0.88 | 0.77 | 0.45 | 0.40 | +0.09 (p=0.17; -0.06..+0.26) | 3/4 |
| halloween-alone@etf | 0.68 (0.21) | +5.8% | 9.0% | 22.5% | 2.6 | 58% | 0.80 | 0.78 | 0.46 | 0.46 | +0.08 (p=0.30; -0.15..+0.32) | 2/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |

Four indexes as one portfolio from 1962 (gate on all four):

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| halloween@idx | 0.85 (0.13) | +5.0% | 5.9% | 22.9% | 2.5 | 35% | 0.85 | 1.30 | 1.57 | 0.53 | 0.82 | 0.02 | 0.42 | +0.13 (p=0.12; -0.06..+0.33) | 5/7 |
| halloween-alone@idx | 0.85 (0.13) | +7.4% | 8.8% | 33.1% | 2.1 | 50% | 1.19 | 1.33 | 1.46 | 0.23 | 0.99 | 0.32 | 0.70 | +0.13 (p=0.18; -0.11..+0.36) | 4/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.7% | 2.3 | 70% | 0.76 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |

## In and after the samples: Sharpe minus the twin's

| Run | 1994 - 1998-10 (in R12's sample) | 1998-11 - 2012-04 (R13's new data) | 2012-05 to end of train (after) |
|---|---:|---:|---:|
| halloween | -0.109 | +0.057 | -0.137 |
| halloween-alone | -0.103 | -0.186 | -0.079 |

## Event study (descriptive): winter minus summer weeks, bps a day

Mean daily log return by the rule's week assignment (the Monday after the governing Friday in November-April = winter). SPY: next open to next open; S&P 500 index: close to close. All days, whatever the trend.

| Asset | Window | n winter / summer | winter | summer | spread (t) |
|---|---|---:|---:|---:|---:|
| GSPC (close) | 1962-1969 (before R12) | 982 / 1005 | +4.4 | -1.6 | +6.0 (+2.08) |
| GSPC (close) | 1970-1993 (in R12's sample) | 2881 / 2950 | +5.3 | +0.1 | +5.2 (+2.04) |
| SPY (open) | 1994 - 1998-10 (in R12's sample) | 555 / 645 | +9.2 | +6.5 | +2.7 (+0.43) |
| SPY (open) | 1998-11 - 2012-04 (R13's new data) | 1729 / 1666 | +4.2 | -1.6 | +5.9 (+1.26) |
| SPY (open) | 2012-05 to end of train (after) | 1609 / 1792 | +5.1 | +5.6 | -0.5 (-0.13) |
| QQQ (open) | 1998-11 - 2012-04 (R13's new data) | 1642 / 1666 | +1.6 | +0.3 | +1.3 (+0.18) |
| QQQ (open) | 2012-05 to end of train (after) | 1609 / 1792 | +5.7 | +8.0 | -2.2 (-0.49) |

## Pass bar: `halloween`

- FAIL: 1. Beats twin `tsmom12` with p < 0.00154 (0.10 / 65) (difference -0.084, p = 0.8725)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (38.8% vs 36.5%)
- PASS: 4. Positive on the ETF and index sets (etf +0.094, idx +0.134)
- PASS: 5. Beats equal weight on Sharpe (0.96 vs 0.88)
- FAIL: 6. (card) Not behind the twin from 1998-11-01 (-0.054)
- FAIL: 7. (card) Not behind the twin from 2012-05-01, SPY winter-minus-summer > 0 (-0.137; SPY -0.5 bps a day (t -0.13))

**FAILS train.**

## Pass bar: `halloween-alone`

- FAIL: 1. Beats twin `tsmom12` with p < 0.00154 (0.10 / 65) (difference -0.170, p = 0.9470)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (49.4% vs 36.5%)
- PASS: 4. Positive on the ETF and index sets (etf +0.076, idx +0.128)
- FAIL: 5. Beats equal weight on Sharpe (0.88 vs 0.88)
- FAIL: 6. (card) Not behind the twin from 1998-11-01 (-0.142)
- FAIL: 7. (card) Not behind the twin from 2012-05-01, SPY winter-minus-summer > 0 (-0.079; SPY -0.5 bps a day (t -0.13))

**FAILS train.**
