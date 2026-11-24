# universal-portfolio: Cover's universal portfolio

Card: `cards/universal-portfolio.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs equal-weight (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| up | 0.85 (0.18) | +15.3% | 18.9% | 51.7% | 1.3 | 57% | 1.33 | 0.21 | 1.41 | 1.46 | 0.64 | -0.04 (p=0.64; -0.19..+0.12) | 1/5 |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | - | - |
| uniform-cash | 0.91 (0.18) | +12.9% | 14.4% | 42.7% | 1.0 | 54% | 1.34 | 0.22 | 1.62 | 1.55 | 0.66 | +0.03 (p=0.34; -0.10..+0.16) | 2/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| up | -26% | -12% | -20% | -40% | -21% | -50% | -50% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |
| uniform-cash | -26% | -11% | -18% | -32% | -11% | -38% | -38% |

Annualised log growth: up +14.2%, equal-weight +16.7%, uniform-cash +12.1%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs equal-weight@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| up@etf | 0.51 (0.20) | +5.5% | 11.9% | 39.2% | 0.2 | 78% | 0.43 | 0.45 | 0.76 | 0.50 | +0.02 (p=0.42; -0.11..+0.17) | 1/4 |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | - | - |
| uniform-cash@etf | 0.51 (0.20) | +5.5% | 11.8% | 38.8% | 0.2 | 78% | 0.43 | 0.45 | 0.78 | 0.53 | +0.03 (p=0.37; -0.10..+0.18) | 3/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs equal-weight@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| up@coin | 0.68 (0.35) | +25.5% | 63.7% | 82.1% | 2.4 | 71% | 0.85 | 0.45 | -0.05 (p=0.60; -0.31..+0.22) | 0/2 |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | - | - |
| uniform-cash@coin | 0.70 (0.35) | +27.6% | 62.1% | 81.5% | 2.4 | 69% | 0.90 | 0.46 | -0.02 (p=0.52; -0.31..+0.27) | 1/2 |

## Out of universe: idx, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs equal-weight@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| up@idx | 0.54 (0.13) | +5.0% | 10.0% | 51.0% | 0.1 | 67% | 0.70 | 0.85 | 1.08 | -0.07 | 0.67 | 0.67 | 0.94 | -0.08 (p=0.97; -0.15..-0.01) | 2/7 |
| equal-weight@idx | 0.62 (0.13) | +7.5% | 13.1% | 57.6% | 0.2 | 100% | 0.71 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | - | - |
| uniform-cash@idx | 0.54 (0.13) | +4.8% | 9.4% | 49.4% | 0.2 | 63% | 0.71 | 0.88 | 1.11 | -0.04 | 0.66 | 0.63 | 0.96 | -0.08 (p=0.96; -0.14..-0.01) | 5/7 |

## Pass bar (primary variant `up`)

- FAIL: 1. Sharpe beats twin `equal-weight` with p < 0.10 (difference -0.04, p = 0.64)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (1 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (51.7% vs 68.8%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf +0.02, coin -0.05, idx -0.08)
- FAIL: 5. Beats equal weight on Sharpe (0.85 vs 0.88)

**FAILS train.**
## Verdict (2026-11-12)

Dead. Cover's portfolio is indistinguishable from the constant mix it starts from (1/7 in each
asset and in cash): Sharpe 0.85 against 0.91 for that mix and 0.88 for equal weight, and the same
on the other ETFs, coins and indexes. Thirty years of weekly data are far too few for the
"learns the best mix" guarantee to matter; what little it learned was to tilt toward Bitcoin
after the fact, which raised volatility without raising Sharpe. Its lower drawdown than equal
weight comes only from holding cash for assets that did not exist yet.
