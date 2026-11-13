# fng: crypto Fear & Greed contrarian

Card: `cards/fng.md`. Protocol: `protocol.md`. Shared rules: `cards/yt-1.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fng-buyfear | 0.94 (0.18) | +16.8% | 18.2% | 47.8% | 3.0 | 77% | 1.34 | 0.19 | 1.55 | 1.35 | 0.46 | -0.10 (p=0.96; -0.20..-0.01) | 0/5 |
| fng-sellgreed | 0.97 (0.18) | +15.6% | 16.4% | 38.7% | 3.9 | 75% | 1.34 | 0.19 | 1.55 | 1.19 | 0.76 | -0.08 (p=0.98; -0.17..-0.01) | 0/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fng-buyfear | -28% | -4% | -21% | -30% | -6% | -43% | -38% |
| fng-sellgreed | -28% | -4% | -22% | -13% | -6% | -22% | -18% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: fng-buyfear +15.6%, fng-sellgreed +14.5%, tsmom12 +16.4%, equal-weight +16.7%

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fng-buyfear@coin | 0.44 (0.34) | +1.1% | 87.8% | 94.0% | 4.9 | 78% | 0.66 | 0.04 | -0.10 (p=0.77; -0.29..+0.11) | 1/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

## Pass bar (primary variant `fng-buyfear`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.10, p = 0.96)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (47.8% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 1 of 1 sets (coin -0.10)
- PASS: 5. Beats equal weight on Sharpe (0.94 vs 0.88)

**FAILS train.**

## Since 2003

| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |
|---|---:|---:|---:|---:|
| fng-buyfear | 1.04 | +19.3% | 47.8% | -0.15 (0.98) |
| fng-sellgreed | 1.09 | +17.5% | 38.7% | -0.11 (0.97) |
| tsmom12 | 1.20 | +20.7% | 36.5% |  |
| equal-weight | 1.19 | +24.9% | 47.0% | -0.00 (0.51) |

- FAIL: 6. Not behind `tsmom12` on Sharpe 2003-2025 (1.04 vs 1.20)

**Card verdict (bars 1-6): FAILS train.**

Information only (eras with Fear & Greed data): 2017-21 1.35 vs 1.50, 2022-25 0.46 vs 0.88
