# tax-drain: step out of stocks and long bonds while tax receipts drain reserves

Card: `cards/tax-drain.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| drain | 1.03 (0.18) | +17.5% | 17.0% | 37.9% | 5.7 | 73% | 1.34 | 0.19 | 1.42 | 1.49 | 0.99 | -0.02 (p=0.88; -0.04..+0.01) | 2/5 |
| drain-ttl | 1.04 (0.18) | +17.4% | 16.8% | 36.5% | 3.0 | 72% | 1.24 | 0.21 | 1.55 | 1.50 | 0.88 | -0.01 (p=0.62; -0.05..+0.03) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| drain | -28% | -3% | -22% | -11% | -9% | -22% | -17% |
| drain-ttl | -25% | +0% | -22% | -13% | -6% | -22% | -20% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Sharpe difference to `tsmom12` from 2008-12-16: -0.026. Placebo `drain-ttl`: -0.008 (p 0.62).

Decision days with the gate on (TGA era): 415.

## First stage (descriptive): does the Treasury's account at the Fed rise?

Change in the TGA's closing balance from session D-2 to D+1 (Daily Treasury Statement, from 2005-10-03), minus the average 3-session change of the same regime.

| Series | Regime | Tax dates | Excess | t |
|---|---|---:|---:|---:|
| TGA | A (TT&L era, placebo) | 14 | +1.3 $bn | +2.03 |
| TGA | B (TGA era, abundant reserves) | 56 | +72.4 $bn | +10.17 |
| TGA | C (TGA era, reserves shrinking) | 27 | +121.9 $bn | +11.17 |
| TGA | B+C (TGA era) | 83 | +88.5 $bn | +13.68 |
| TGA | C, quarterly corporate dates only | 22 | +127.7 $bn | +12.34 |

## Event study (descriptive): sessions D-1 .. D+3, close to close

Log return from the close of D-2 to the close of D+3, minus the average 5-session return of the same regime.

| Series | Regime | Tax dates | Excess | t |
|---|---|---:|---:|---:|
| SPY | A (TT&L era, placebo) | 77 | -9.1 bps | -0.31 |
| SPY | B (TGA era, abundant reserves) | 56 | -10.9 bps | -0.44 |
| SPY | C (TGA era, reserves shrinking) | 27 | -61.6 bps | -1.30 |
| SPY | B+C (TGA era) | 83 | -27.4 bps | -1.21 |
| SPY | C, quarterly corporate dates only | 22 | -85.3 bps | -1.68 |
| TLT | A (TT&L era, placebo) | 30 | +6.6 bps | +0.24 |
| TLT | B (TGA era, abundant reserves) | 56 | -6.6 bps | -0.36 |
| TLT | C (TGA era, reserves shrinking) | 27 | -47.1 bps | -1.42 |
| TLT | B+C (TGA era) | 83 | -19.8 bps | -1.20 |
| TLT | C, quarterly corporate dates only | 22 | -17.7 bps | -0.50 |
| IEF | A (TT&L era, placebo) | 30 | +7.1 bps | +0.44 |
| IEF | B (TGA era, abundant reserves) | 56 | -13.6 bps | -1.55 |
| IEF | C (TGA era, reserves shrinking) | 27 | -21.9 bps | -1.37 |
| IEF | B+C (TGA era) | 83 | -16.3 bps | -2.08 |
| IEF | C, quarterly corporate dates only | 22 | -7.0 bps | -0.42 |
| LQD | A (TT&L era, placebo) | 30 | +16.7 bps | +1.27 |
| LQD | B (TGA era, abundant reserves) | 56 | -12.2 bps | -1.06 |
| LQD | C (TGA era, reserves shrinking) | 27 | -25.5 bps | -1.28 |
| LQD | B+C (TGA era) | 83 | -16.6 bps | -1.64 |
| LQD | C, quarterly corporate dates only | 22 | -16.0 bps | -0.75 |

Card's reading: (a) first stage yes; (b) SPY negative with t <= -2 in B+C or C no; (c) placebo A not more negative yes. Mechanism **not supported**.

## Out of universe

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| drain@etf | 0.59 (0.20) | +4.8% | 8.6% | 17.0% | 5.5 | 63% | -0.01 (p=0.73; -0.05..+0.03) | 2/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| drain@idx | 0.72 (0.13) | +6.1% | 8.8% | 26.7% | 3.4 | 70% | -0.01 (p=0.75; -0.02..+0.01) | 2/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.7% | 2.3 | 70% | - | - |

## Pass bar (only variant `drain`)

- FAIL: 1. `drain` beats twin `tsmom12` with p < 0.0020 (0.10 / 49) (difference -0.016, p = 0.8825)
- FAIL: 2. Ahead of the twin in at least 3 of 4 eras (from 2000-09) (2 of 4)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (37.9% vs 36.5%)
- FAIL: 4. Positive, and positive on both out-of-universe sets (etf -0.013, idx -0.005)
- PASS: 5. Beats equal weight on Sharpe (1.03 vs 0.88)
- FAIL: 6. (card) Gain over the twin larger than the placebo `drain-ttl`'s (-0.016 vs -0.008)

**FAILS train.**
