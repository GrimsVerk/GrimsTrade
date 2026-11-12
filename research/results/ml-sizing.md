# ml-sizing: the same models with a position rule that follows the forecast

Card: `cards/ml-sizing.md`. Protocol: `protocol.md`.

## The six live assets, train period, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-prop | 0.75 (0.18) | +8.4% | 11.6% | 36.6% | 9.2 | 51% | 1.14 | 0.05 | 1.20 | 1.24 | 0.98 | -0.30 (p=0.98; -0.53..-0.06) | 1/5 |
| logit-prop | 0.75 (0.18) | +8.4% | 11.6% | 46.2% | 2.5 | 53% | 1.16 | -0.09 | 1.64 | 1.56 | 0.63 | -0.30 (p=1.00; -0.46..-0.13) | 2/5 |
| gbm-low | 0.80 (0.18) | +12.0% | 15.8% | 52.6% | 9.7 | 73% | 1.12 | 0.07 | 1.06 | 1.41 | 1.01 | -0.25 (p=0.95; -0.49..-0.00) | 1/5 |
| logit-low | 0.82 (0.18) | +12.1% | 15.4% | 37.7% | 6.6 | 73% | 1.31 | 0.05 | 1.04 | 1.41 | 0.65 | -0.23 (p=0.99; -0.40..-0.06) | 0/5 |
| gbm-reg-prop | 0.68 (0.18) | +9.0% | 14.0% | 45.0% | 8.4 | 53% | 1.10 | 0.03 | 0.59 | 1.29 | 0.80 | -0.36 (p=1.00; -0.59..-0.16) | 0/5 |
| ridge-prop | 0.82 (0.18) | +8.9% | 11.2% | 39.7% | 1.4 | 51% | 1.25 | -0.04 | 1.45 | 1.53 | 0.64 | -0.23 (p=1.00; -0.39..-0.09) | 1/5 |
| gbm | 0.81 (0.18) | +11.8% | 15.0% | 46.0% | 9.6 | 70% | 1.20 | 0.09 | 1.08 | 1.37 | 1.05 | -0.23 (p=0.95; -0.46..+0.00) | 1/5 |
| logit | 0.89 (0.18) | +15.5% | 18.1% | 58.5% | 3.5 | 89% | 1.34 | -0.00 | 1.67 | 1.55 | 0.63 | -0.16 (p=0.95; -0.32..-0.01) | 2/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-prop | -36% | -1% | -6% | -10% | +3% | -26% | -13% |
| logit-prop | -46% | -7% | -8% | -17% | -3% | -19% | -20% |
| gbm-low | -53% | +1% | -6% | -15% | +2% | -37% | -23% |
| logit-low | -36% | -6% | -8% | -19% | -3% | -22% | -25% |
| gbm-reg-prop | -43% | +4% | -6% | -7% | -8% | -34% | -13% |
| ridge-prop | -40% | -8% | -11% | -18% | -3% | -21% | -21% |
| gbm | -45% | -0% | -8% | -13% | +1% | -38% | -19% |
| logit | -59% | -14% | -16% | -31% | -7% | -33% | -36% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: gbm-prop +8.1%, logit-prop +8.1%, gbm-low +11.4%, logit-low +11.4%, gbm-reg-prop +8.6%, ridge-prop +8.5%, gbm +11.1%, logit +14.4%, tsmom12 +16.4%, equal-weight +16.7%

## Out of universe: etf, from 2007-01-05

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-prop@etf | 0.19 (0.23) | +1.2% | 7.8% | 24.1% | 9.8 | 47% | 0.03 | 0.13 | 0.64 | 0.12 | -0.28 (p=0.94; -0.57..+0.02) | 1/4 |
| tsmom12@etf | 0.47 (0.23) | +3.7% | 8.5% | 16.5% | 3.0 | 64% | 0.45 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.47 (0.23) | +6.0% | 14.8% | 43.1% | 0.3 | 100% | 0.27 | 0.46 | 0.76 | 0.52 | +0.00 (p=0.49; -0.27..+0.27) | 2/4 |

## Out of universe: coin, from 2023-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-prop@coin | 0.76 (0.55) | +23.7% | 36.5% | 32.8% | 11.4 | 43% | 0.76 | +0.21 (p=0.32; -0.55..+0.87) | 1/1 |
| tsmom12@coin | 0.55 (0.59) | +15.9% | 47.5% | 46.1% | 5.3 | 56% | 0.55 | - | - |
| equal-weight@coin | 0.98 (0.58) | +53.8% | 66.4% | 53.5% | 2.8 | 100% | 0.98 | +0.43 (p=0.02; +0.08..+0.78) | 1/1 |

## Out of universe: idx, from 1974-01-04

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-prop@idx | 0.61 (0.14) | +4.3% | 7.3% | 26.9% | 9.3 | 49% | 0.21 | 0.87 | 1.00 | 0.47 | 0.45 | 0.50 | 0.60 | -0.10 (p=0.82; -0.27..+0.08) | 2/7 |
| tsmom12@idx | 0.71 (0.14) | +6.2% | 9.1% | 25.7% | 2.3 | 70% | 0.69 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| equal-weight@idx | 0.59 (0.14) | +7.5% | 13.7% | 57.6% | 0.2 | 100% | 0.56 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | -0.11 (p=0.84; -0.30..+0.07) | 5/7 |

## Pass bar (primary variant `gbm-prop`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.30, p = 0.98)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (1 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (36.6% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.28, coin +0.21, idx -0.10)
- FAIL: 5. Beats equal weight on Sharpe (0.75 vs 0.88)

**FAILS train.**
## Verdict (2026-11-12)

Dead. Letting the position follow the forecast made every model worse, not better: 0.68 to
0.82 Sharpe for the six variants, against 0.81 and 0.89 for the same models under the first
rule, 0.88 for equal weight and 1.05 for `tsmom12` (all p >= 0.95 the wrong way).

The check the card set for itself failed too: on the control (`results/ml-control.md`), a
planted signal of correlation 0.10 does not get ahead of `tsmom12` under either new rule
(0.80 to 0.90), and even 0.20 only ties it. So by the card's own terms the Sharpe comparison
had no power and the card is judged on forecast skill, which is nil (AUC 0.49 to 0.51, same
models as before).

Why a sharper rule hurt: the forecasts carry no skill, so following them more closely is
following noise more closely. One systematic thing they do carry works against the book: the
models learnt that volatile assets go up less often, so they hold less Bitcoin and Ether. Those
went up less often but far more when they did, and were the best assets of the period.
Forecasting the chance of a gain ignores the size of the gain.

The held-out year was not looked at.
