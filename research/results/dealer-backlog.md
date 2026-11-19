# dealer-backlog: idle cash into the long bond after auctions dealers absorbed

Card: `cards/dealer-backlog.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| backlog | 1.02 (0.18) | +17.3% | 17.1% | 35.0% | 6.1 | 77% | 1.34 | 0.19 | 1.54 | 1.52 | 0.62 | -0.03 (p=0.95; -0.06..-0.00) | 1/5 |
| backlog-neg | 1.03 (0.18) | +17.6% | 17.2% | 37.0% | 8.6 | 78% | 1.34 | 0.18 | 1.53 | 1.49 | 0.81 | -0.02 (p=0.84; -0.05..+0.01) | 0/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| backlog | -28% | -4% | -22% | -16% | -5% | -21% | -25% |
| backlog-neg | -28% | -4% | -23% | -16% | -7% | -23% | -20% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## Event study (descriptive): five sessions after the auction

Fills = open of A+1 to open of A+6; closes = close of A to close of A+5. Excess = log return minus the average 5-session log return of the same kind since 2008-07-01, in bps (t). u = dealer share of competitive awards minus the median of the previous 12 auctions of the group, in points. Slope = bps per point of u (OLS, HC1 t). TLT on 20- and 30-year auctions, IEF on 10-year auctions.

| Bond | Period | u > 0 | Excess (t) | u <= 0 | Excess (t) | Slope | t |
|---|---|---:|---:|---:|---:|---:|---:|
| TLT, fills | all | 108 | -13.4 (-0.68) | 156 | +5.9 (+0.41) | -1.39 | -0.97 |
| TLT, fills | 2008-07 to 2016 | 38 | -0.7 (-0.02) | 53 | +41.2 (+1.56) | -1.79 | -0.45 |
| TLT, fills | 2017 to end of train | 70 | -20.2 (-0.81) | 103 | -12.3 (-0.75) | -0.77 | -0.66 |
| TLT, closes | all | 108 | -4.6 (-0.24) | 156 | -6.6 (-0.44) | -0.89 | -0.53 |
| TLT, closes | 2008-07 to 2016 | 38 | +20.4 (+0.63) | 53 | +36.5 (+1.37) | -0.13 | -0.03 |
| TLT, closes | 2017 to end of train | 70 | -18.2 (-0.76) | 103 | -28.8 (-1.59) | -0.61 | -0.36 |
| IEF, fills | all | 79 | -0.4 (-0.03) | 129 | -5.3 (-0.60) | +0.09 | +0.14 |
| IEF, fills | 2008-07 to 2016 | 38 | +24.0 (+1.59) | 62 | +1.2 (+0.10) | -0.03 | -0.02 |
| IEF, fills | 2017 to end of train | 41 | -23.0 (-1.21) | 67 | -11.4 (-0.94) | +0.62 | +1.05 |
| IEF, closes | all | 79 | +10.4 (+0.86) | 129 | -8.7 (-1.00) | +0.85 | +1.15 |
| IEF, closes | 2008-07 to 2016 | 38 | +28.4 (+1.79) | 62 | -3.7 (-0.28) | +0.97 | +0.74 |
| IEF, closes | 2017 to end of train | 41 | -6.2 (-0.35) | 67 | -13.4 (-1.14) | +1.07 | +1.56 |

Long auctions since 2008-07 (TLT sessions): 264, of which 108 with u > 0; standard deviation of u 7.2 points.

Card's reading for TLT at our fills: (a) slope > 0 with t >= 2 no; (b) traded-group mean above the other no; (c) slope positive in both halves no. Mechanism **not supported**.

## Out of universe: the 8 other ETFs, overlay into IEF after 10-year auctions

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| backlog@etf | 0.59 (0.20) | +4.9% | 8.8% | 19.2% | 5.9 | 67% | -0.01 (p=0.59; -0.05..+0.04) | 2/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |

## Pass bar (only variant `backlog`)

- FAIL: 1. `backlog` beats twin `tsmom12` with p < 0.00179 (0.10 / 56) (difference -0.026, p = 0.9515)
- FAIL: 2. Ahead of the twin in at least 3 of 4 eras (from 2000-09) (1 of 4)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (35.0% vs 36.5%)
- FAIL: 4. Positive, and positive on the ETF set (etf -0.008)
- PASS: 5. Beats equal weight on Sharpe (1.02 vs 0.88)
- FAIL: 6. (card) Beats its placebo `backlog-neg` on Sharpe (1.022 vs 1.030)

**FAILS train.**
