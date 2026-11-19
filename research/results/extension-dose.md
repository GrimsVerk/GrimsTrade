# extension-dose: the month-end bond window only when the index extends a lot

Card: `cards/extension-dose.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ext-high | 1.06 (0.18) | +18.1% | 17.1% | 35.8% | 6.0 | 77% | 1.34 | 0.25 | 1.57 | 1.49 | 0.86 | +0.01 (p=0.19; -0.01..+0.04) | 2/5 |
| ext-low | 1.05 (0.18) | +18.1% | 17.2% | 36.1% | 6.0 | 77% | 1.34 | 0.16 | 1.55 | 1.50 | 1.00 | +0.01 (p=0.34; -0.02..+0.03) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ext-high | -28% | +0% | -22% | -17% | -4% | -23% | -22% |
| ext-low | -28% | -6% | -22% | -11% | -6% | -22% | -16% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## Event study (descriptive): open of T-3 to open of T+1

Excess = log return minus the average 4-session open-to-open log return since 2002-07-30, in bps (t). High = E(m) above the median of the previous 24 months (the rule's months). Slope = bps per year of extension (OLS, HC1 t). TLT against the 20+ year bucket, IEF against the 7-10 year bucket.

| Bond | Period | High months | Excess (t) | Low months | Excess (t) | Slope | t |
|---|---|---:|---:|---:|---:|---:|---:|
| TLT | all | 113 | +32.1 (+2.19) | 166 | +16.7 (+1.35) | +65.41 | +0.79 |
| TLT | 2002-07 to 2013 | 37 | +56.4 (+1.80) | 100 | +12.3 (+0.76) | +70.21 | +0.80 |
| TLT | 2014 to end of train | 76 | +20.3 (+1.31) | 66 | +23.4 (+1.23) | +8.87 | +0.04 |
| IEF | all | 140 | +12.5 (+1.78) | 139 | +17.9 (+2.87) | +29.96 | +0.46 |
| IEF | 2002-07 to 2013 | 67 | +12.6 (+1.05) | 70 | +16.8 (+2.01) | +38.29 | +0.39 |
| IEF | 2014 to end of train | 73 | +12.5 (+1.58) | 69 | +19.0 (+2.04) | +18.63 | +0.23 |

- TLT, 20+: 279 month ends, 113 high; E(m) median +0.043 years, standard deviation 0.143, range +0.000 to +0.933.
- IEF, 7-10: 279 month ends, 140 high; E(m) median +0.083 years, standard deviation 0.078, range -0.050 to +0.417.

Card's reading for TLT at our fills: (a) slope > 0 with t >= 2 no; (b) traded-group mean above the other yes; (c) slope positive in both halves yes. Mechanism **not supported**.

## Out of universe: the 8 other ETFs, overlay into IEF by the 7-10 bucket

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ext-high@etf | 0.62 (0.20) | +5.2% | 8.8% | 16.4% | 6.9 | 68% | +0.02 (p=0.21; -0.02..+0.06) | 3/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |

## Pass bar (only variant `ext-high`)

- FAIL: 1. `ext-high` beats twin `tsmom12` with p < 0.00179 (0.10 / 56; biased up by the seen month-end mean) (difference +0.013, p = 0.1895)
- FAIL: 2. Ahead of the twin in at least 3 of 4 eras (from 2000-09) (2 of 4)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (35.8% vs 36.5%)
- PASS: 4. Positive, and positive on the ETF set (etf +0.020)
- PASS: 5. Beats equal weight on Sharpe (1.06 vs 0.88)
- PASS: 6. (card) Beats its placebo `ext-low` on Sharpe (1.061 vs 1.054)

**FAILS train.**
