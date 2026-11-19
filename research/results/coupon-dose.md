# coupon-dose: idle cash into the long bond when Treasury cash is paid back

Card: `cards/coupon-dose.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| dose | 1.04 (0.18) | +17.7% | 17.2% | 36.3% | 6.3 | 77% | 1.34 | 0.24 | 1.49 | 1.53 | 0.73 | -0.01 (p=0.71; -0.04..+0.02) | 2/5 |
| dose-neg | 1.04 (0.18) | +17.6% | 17.1% | 36.8% | 5.9 | 77% | 1.34 | 0.20 | 1.56 | 1.50 | 0.76 | -0.01 (p=0.80; -0.03..+0.01) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| dose | -28% | -1% | -23% | -14% | -8% | -22% | -23% |
| dose-neg | -28% | -3% | -22% | -13% | -6% | -22% | -20% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## Event study (descriptive): sessions P .. P+3, close of P-1 to close of P+3

Excess = log return minus the average 4-session log return since 2002-07-30, in bps (t). Slope = bps of excess per 1% of outstanding notes and bonds paid back net (OLS, HC1 t).

| Bond | Period | Positive doses | Excess (t) | Non-positive | Excess (t) | Slope | t |
|---|---|---:|---:|---:|---:|---:|---:|
| TLT | all | 146 | +1.8 (+0.12) | 133 | +17.7 (+1.27) | +17.8 | +0.98 |
| TLT | 2002-07 to 2013 | 70 | +31.2 (+1.34) | 67 | +38.3 (+1.76) | +23.2 | +1.09 |
| TLT | 2014 to end of train | 76 | -25.2 (-1.41) | 66 | -3.1 (-0.18) | -3.6 | -0.14 |
| IEF | all | 146 | -0.2 (-0.03) | 133 | +6.1 (+0.93) | +8.5 | +1.01 |
| IEF | 2002-07 to 2013 | 70 | +17.0 (+1.42) | 67 | +13.7 (+1.32) | +12.5 | +1.28 |
| IEF | 2014 to end of train | 76 | -16.1 (-2.07) | 66 | -1.6 (-0.20) | -7.0 | -0.61 |

Mid-month days since 2002-07 (TLT): 279, of which 146 with a positive net dose; median net dose +1.2 $bn; standard deviation of the dose 0.747% of outstanding.

Card's reading for TLT: (a) slope > 0 with t >= 2 no; (b) positive-dose mean above the rest no; (c) slope positive in both halves no. Mechanism **not supported**.

## Out of universe: the 8 other ETFs, overlay into IEF

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| dose@etf | 0.57 (0.20) | +4.7% | 8.8% | 18.5% | 6.9 | 68% | -0.03 (p=0.89; -0.08..+0.01) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |

## Pass bar (only variant `dose`)

- FAIL: 1. `dose` beats twin `tsmom12` with p < 0.00185 (0.10 / 54) (difference -0.011, p = 0.7120)
- FAIL: 2. Ahead of the twin in at least 3 of 4 eras (from 2000-09) (2 of 4)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (36.3% vs 36.5%)
- FAIL: 4. Positive, and positive on the ETF set (etf -0.032)
- PASS: 5. Beats equal weight on Sharpe (1.04 vs 0.88)
- PASS: 6. (card) Beats its placebo `dose-neg` on Sharpe (1.037 vs 1.036)

**FAILS train.**
