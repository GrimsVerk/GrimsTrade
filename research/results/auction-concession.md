# auction-concession: step aside while dealers make room for a Treasury auction

Card: `cards/auction-concession.md`. Protocol: `protocol.md`.

Auctions from 2003-08 to the end of train: 277 of 20/30-year bonds (TLT), 462 of 7/10-year notes (IEF).

## `six`: the six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| six | 1.06 (0.18) | +18.1% | 17.1% | 35.9% | 4.2 | 74% | 1.34 | 0.18 | 1.56 | 1.51 | 0.95 | +0.01 (p=0.14; -0.01..+0.03) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| six | -28% | -4% | -19% | -13% | -8% | -23% | -19% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Sharpe difference to `tsmom12` from 2013-01-01: +0.03.

# `tlt`: TLT alone, held except in the five sessions ending with the auction

## TLT, from 2003-07-31

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@TLT (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tlt@TLT | 0.50 (0.21) | +5.7% | 12.6% | 44.1% | 25.4 | 78% | 0.53 | 0.54 | 0.84 | 0.01 | +0.17 (p=0.05; -0.00..+0.35) | 2/4 |
| constant@TLT | 0.33 (0.21) | +3.1% | 11.2% | 39.7% | 0.1 | 78% | 0.53 | 0.54 | 0.53 | -0.49 | - | - |
| equal-weight@TLT | 0.33 (0.21) | +3.8% | 14.5% | 48.4% | 0.0 | 100% | 0.52 | 0.55 | 0.53 | -0.49 | +0.00 (p=0.41; -0.00..+0.00) | 3/4 |

Mean open-to-open return per day held +3.4 bps (4375 days), per day not held -3.6 bps (1230 days), Welch t = 2.37. Days held before 2013-01-01: +4.2 bps; from 2013-01-01: +2.7 bps. Sharpe difference to the twin from 2013-01-01: +0.24.

Read: "days held" are the sessions outside the auction window, "days not held" the five sessions ending with an auction day.

# Out of universe: the 8 other ETFs, IEF gated by 7- and 10-year auctions

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| six@etf | 0.57 (0.20) | +4.7% | 8.7% | 16.9% | 6.1 | 62% | 0.78 | 0.41 | 0.41 | 0.57 | -0.03 (p=1.00; -0.05..-0.02) | 0/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |

## IEF, from 2003-07-31

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@IEF (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tlt@IEF | 0.26 (0.21) | +1.3% | 5.7% | 22.7% | 41.3 | 66% | 0.49 | 0.35 | 0.46 | -0.37 | -0.29 (p=0.99; -0.48..-0.09) | 0/4 |
| constant@IEF | 0.55 (0.21) | +2.4% | 4.5% | 16.2% | 0.0 | 66% | 0.79 | 0.74 | 0.68 | -0.14 | - | - |
| equal-weight@IEF | 0.55 (0.21) | +3.5% | 6.8% | 23.9% | 0.0 | 100% | 0.78 | 0.74 | 0.68 | -0.14 | -0.00 (p=0.95; -0.01..+0.00) | 1/4 |

Mean open-to-open return per day held +1.4 bps (3730 days), per day not held +1.7 bps (1875 days), Welch t = -0.30. Days held before 2013-01-01: +2.5 bps; from 2013-01-01: +0.4 bps. Sharpe difference to the twin from 2013-01-01: -0.31.

# Pass bar (primary variant `six`)

- FAIL: 1. `six` beats twin `tsmom12` with p < 0.10 (difference +0.011, p = 0.14)
- PASS: 2. Ahead of the twin in at least 3 of 4 eras (from 2000-09) (3 of 4)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (35.9% vs 36.5%)
- FAIL: 4. Same sign out of universe: the ETF-set book and IEF alone (ETF set -0.030 (p = 1.00), IEF alone -0.29 (p = 0.99))
- PASS: 5. Beats equal weight on Sharpe (1.06 vs 0.88)
- PASS: 6. (card) `tlt` beats its `constant` twin with p < 0.10 (+0.17, p = 0.05)
- PASS: 7. (card) From 2013-01-01: `six` not behind `tsmom12`, `tlt` not behind `constant` (+0.027, +0.24)

**FAILS train.**

Welch t of in-window against out-of-window days: TLT +2.37, IEF -0.30 (positive = the days held earned more).
