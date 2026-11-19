# opex-pin: idle cash into stocks for the option-expiry week

Card: `cards/opex-pin.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pin | 1.01 (0.18) | +18.0% | 18.0% | 40.6% | 9.4 | 81% | 1.37 | 0.26 | 1.55 | 1.47 | 0.65 | -0.04 (p=0.76; -0.13..+0.05) | 2/5 |
| pin-after | 1.03 (0.18) | +18.4% | 18.0% | 35.3% | 9.4 | 81% | 1.34 | 0.10 | 1.60 | 1.53 | 1.02 | -0.02 (p=0.64; -0.09..+0.06) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| pin | -40% | -1% | -22% | -25% | -4% | -23% | -29% |
| pin-after | -30% | -16% | -22% | -10% | -5% | -24% | -14% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Fridays on which `pin` differs from the twin: 193.

## Event study (descriptive): expiry week minus the average week, close to close

| Series and period | Expiry weeks | Excess, bps a week | t |
|---|---:|---:|---:|
| SPY 1994-2025 | 381 | -0.3 | -0.02 |
| SPY 1994-99 | 71 | +26.3 | +1.10 |
| SPY 2000-09 | 120 | +8.1 | +0.30 |
| SPY 2010-16 | 84 | +5.4 | +0.26 |
| SPY 2017-21 | 60 | -38.1 | -1.12 |
| SPY 2022-25 | 46 | -25.5 | -0.67 |
| S&P 500 index 1962-01 to 1983-02 (placebo) | 254 | -0.2 | -0.02 |
| S&P 500 index 1983-03 to 1993-01 | 119 | +18.8 | +0.97 |

Card's reading: SPY excess positive with t >= 2 and placebo below 1983-1993: **not supported**.

## Out of universe

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| pin@etf | 0.46 (0.20) | +4.7% | 11.4% | 28.8% | 10.5 | 73% | -0.14 (p=0.90; -0.32..+0.04) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| pin@idx | 0.64 (0.13) | +6.0% | 9.9% | 36.3% | 8.7 | 77% | -0.08 (p=0.93; -0.18..+0.01) | 2/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.7% | 2.3 | 70% | - | - |

## Pass bar (only variant `pin`)

- FAIL: 1. `pin` beats twin `tsmom12` with p < 0.0020 (0.10 / 49) (difference -0.040, p = 0.7555)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (40.6% vs 36.5%)
- FAIL: 4. Positive, and positive on both applicable out-of-universe sets (etf -0.140, idx -0.082)
- PASS: 5. Beats equal weight on Sharpe (1.01 vs 0.88)
- FAIL: 6. (card) Beats its placebo `pin-after` on Sharpe (1.008 vs 1.029)

**FAILS train.**
