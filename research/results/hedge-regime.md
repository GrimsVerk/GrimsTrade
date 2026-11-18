# hedge-regime: hold the long bond out of trend while it hedges stocks

Card: `cards/hedge-regime.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| hedge | 1.05 (0.18) | +17.9% | 17.0% | 35.8% | 2.6 | 79% | 1.34 | 0.20 | 1.59 | 1.50 | 0.79 | +0.00 (p=0.39; -0.01..+0.02) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| hedge | -28% | -4% | -22% | -17% | -4% | -22% | -24% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

TLT's rho is defined on 1163 Fridays (2003-08-01 on); below zero on 941 (81%); the sign changes 13 times (weekly).

| Year | mean rho | share of Fridays below zero |
|---|---:|---:|
| 2003 | -0.43 | 100% |
| 2004 | -0.16 | 100% |
| 2005 | -0.04 | 77% |
| 2006 | -0.03 | 73% |
| 2007 | -0.10 | 73% |
| 2008 | -0.46 | 100% |
| 2009 | -0.42 | 100% |
| 2010 | -0.47 | 100% |
| 2011 | -0.55 | 100% |
| 2012 | -0.67 | 100% |
| 2013 | -0.48 | 100% |
| 2014 | -0.27 | 100% |
| 2015 | -0.38 | 100% |
| 2016 | -0.40 | 100% |
| 2017 | -0.19 | 100% |
| 2018 | -0.18 | 100% |
| 2019 | -0.37 | 100% |
| 2020 | -0.48 | 100% |
| 2021 | -0.09 | 49% |
| 2022 | -0.05 | 85% |
| 2023 | +0.14 | 0% |
| 2024 | +0.16 | 0% |
| 2025 | +0.04 | 4% |

Fridays on which `hedge` holds TLT and the twin does not: 267. TLT over the next five sessions (close to close): mean +1.2 bps a week, t +0.12; sum +3.3% (log).

## Out of universe: the 8 other ETFs (IEF, LQD against IWM, EFA, EEM, VNQ)

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| hedge@etf | 0.59 (0.20) | +4.9% | 8.7% | 16.5% | 2.9 | 67% | -0.01 (p=0.78; -0.02..+0.01) | 2/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |

## Pass bar (only variant `hedge`)

- FAIL: 1. `hedge` beats twin `tsmom12` with p < 0.0022 (0.10 / 46) (difference +0.003, p = 0.3915)
- PASS: 2. Ahead of the twin in at least 3 of 4 eras (from 2000-09) (3 of 4)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (35.8% vs 36.5%)
- FAIL: 4. Positive, and positive on the one applicable out-of-universe set (ETF set -0.006 (p = 0.78))
- PASS: 5. Beats equal weight on Sharpe (1.05 vs 0.88)

**FAILS train.**

Difference since 2003-07-01 (TLT eligible): +0.004.
