# ml-linear: a regularised linear model on simple features

Card: `cards/ml-linear.md`. Protocol: `protocol.md`.

## The six live assets, train period, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| logit | 0.89 (0.18) | +15.5% | 18.1% | 58.5% | 3.5 | 89% | 1.34 | -0.00 | 1.67 | 1.55 | 0.63 | -0.16 (p=0.95; -0.32..-0.01) | 2/5 |
| logit-hard | 0.88 (0.18) | +18.1% | 21.6% | 68.8% | 1.3 | 100% | 1.38 | 0.02 | 1.67 | 1.53 | 0.67 | -0.17 (p=0.92; -0.36..+0.02) | 3/5 |
| ridge | 0.84 (0.18) | +15.4% | 19.1% | 60.6% | 2.1 | 90% | 1.32 | -0.02 | 1.59 | 1.55 | 0.61 | -0.20 (p=0.99; -0.37..-0.04) | 2/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| sma200 | 1.01 (0.18) | +15.9% | 15.8% | 44.4% | 4.3 | 70% | 1.14 | 0.14 | 1.58 | 1.53 | 0.75 | -0.04 (p=0.69; -0.18..+0.09) | 2/5 |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| logit | -59% | -14% | -16% | -31% | -7% | -33% | -36% |
| logit-hard | -69% | -20% | -24% | -37% | -17% | -46% | -42% |
| ridge | -61% | -14% | -21% | -32% | -6% | -33% | -37% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| sma200 | -33% | +2% | -14% | -12% | -4% | -23% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: logit +14.4%, logit-hard +16.7%, ridge +14.3%, tsmom12 +16.4%, sma200 +14.7%, equal-weight +16.7%

## Forecast skill on the six assets (walk-forward forecasts, 28 days ahead)

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| logit | 6214 | 59.3% | 0.494 | 59.3% | 99.8% | 0.522 | 56.6% |
| ridge | 6214 | 59.3% | 0.488 | 59.4% | 100.0% | 0.522 | 56.6% |

## Settings chosen by purged CV (six assets)

- `logit`: 32 yearly fits, 1617 rows at the first, 7640 at the last. Chosen: C=0.001: 25 fits; C=0.01: 7 fits.
- `ridge`: 32 yearly fits, 1617 rows at the first, 7640 at the last. Chosen: alpha=10000: 31 fits; alpha=1000: 1 fits.

## What the last logistic model weighs (standardised coefficients)

`since_high` -0.04, `breadth` +0.04, `z7` +0.04, `dd_1y` +0.03, `log_vol` -0.03, `z365` -0.02, `vol_shock` -0.02, `z182` +0.02, `z91` -0.01, `up_12m` +0.01, `univ_mom_1m` +0.00, `z30` -0.00, `sma_gap` +0.00, `univ_vol_shock` +0.00, `rank_12m` +0.00

## Out of universe: etf, from 2007-01-05

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| logit@etf | 0.37 (0.23) | +4.2% | 13.3% | 42.5% | 1.5 | 90% | 0.08 | 0.40 | 0.65 | 0.50 | -0.09 (p=0.72; -0.34..+0.15) | 1/4 |
| tsmom12@etf | 0.47 (0.23) | +3.7% | 8.5% | 16.5% | 3.0 | 64% | 0.45 | 0.44 | 0.44 | 0.59 | - | - |
| sma200@etf | 0.49 (0.23) | +3.7% | 8.1% | 16.8% | 3.9 | 64% | 0.69 | 0.36 | 0.66 | 0.31 | +0.02 (p=0.46; -0.18..+0.20) | 2/4 |
| equal-weight@etf | 0.47 (0.23) | +6.0% | 14.8% | 43.1% | 0.3 | 100% | 0.27 | 0.46 | 0.76 | 0.52 | +0.00 (p=0.49; -0.27..+0.27) | 2/4 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| logit | 7555 | 57.3% | 0.472 | 57.3% | 100.0% | 0.514 | 53.5% |

## Out of universe: coin, from 2023-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| logit@coin | -0.06 (0.59) | -0.2% | 3.1% | 4.2% | 0.8 | 2% | -0.06 | -0.61 (p=0.83; -1.57..+0.38) | 0/1 |
| tsmom12@coin | 0.55 (0.59) | +15.9% | 47.5% | 46.1% | 5.3 | 56% | 0.55 | - | - |
| sma200@coin | 0.51 (0.59) | +13.9% | 48.9% | 45.8% | 6.4 | 53% | 0.51 | -0.04 (p=0.58; -0.32..+0.22) | 0/1 |
| equal-weight@coin | 0.98 (0.58) | +53.8% | 66.4% | 53.5% | 2.8 | 100% | 0.98 | +0.43 (p=0.02; +0.08..+0.78) | 1/1 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| logit | 870 | 48.0% | 0.600 | 55.5% | 12.1% | 0.473 | 47.1% |

## Out of universe: idx, from 1974-01-04

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| logit@idx | 0.62 (0.14) | +6.4% | 11.0% | 36.4% | 3.0 | 86% | 0.41 | 0.97 | 1.08 | 0.04 | 0.47 | 0.50 | 0.93 | -0.09 (p=0.86; -0.22..+0.05) | 3/7 |
| tsmom12@idx | 0.71 (0.14) | +6.2% | 9.1% | 25.7% | 2.3 | 70% | 0.69 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| sma200@idx | 0.67 (0.14) | +5.4% | 8.3% | 23.5% | 3.8 | 68% | 0.55 | 1.10 | 1.00 | 0.37 | 0.25 | 0.30 | 0.92 | -0.04 (p=0.67; -0.17..+0.09) | 2/7 |
| equal-weight@idx | 0.59 (0.14) | +7.5% | 13.7% | 57.6% | 0.2 | 100% | 0.56 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | -0.11 (p=0.84; -0.30..+0.07) | 5/7 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| logit | 9427 | 59.3% | 0.509 | 58.4% | 97.3% | 0.530 | 56.5% |

## Pass bar (primary variant `logit`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.16, p = 0.95)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (58.5% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.09, coin -0.61, idx -0.09)
- PASS: 5. Beats equal weight on Sharpe (0.89 vs 0.88)

**FAILS train.**
## Verdict (2026-11-12)

Dead. The linear models found nothing and turned into equal weight, exactly the failure the
card named. At 25 of 32 yearly fits purged CV picked the strongest shrinkage on offer, which is
the data saying "no feature helps": the forecasts sat at the long-run average, the model said
"up" 99.8% of the time, and the portfolio held 89% of everything through every crash (worst
loss 58% against 37% for `tsmom12`; Sharpe 0.89 against 1.05, p = 0.95 the wrong way).

The skill table says why. Ranking which asset-months go up, the model scored an AUC of 0.494
(0.5 is a coin toss), worse than the single flag `up_12m` at 0.522. And the flag itself is a
poor forecaster of direction: it is right 56.6% of the time, less than always saying "up"
(59.3%). So `tsmom12` does not earn its Sharpe by calling the direction of the next month. It
earns it by being out of the market in the months when losses are large. A model trained to
forecast direction, or the average risk-adjusted return, is aimed at the wrong target.

Out of universe the same: behind `tsmom12` on other ETFs (-0.09), on the four indexes since
1974 (-0.09), and on other coins since 2023 it held almost nothing (the coins' training history
was mostly falling) and missed a +54% a year market.

The held-out year was not looked at.
