# ml-payoff: train the model on what a position earns, not on which way the price goes

Card: `cards/ml-payoff.md`. Protocol: `protocol.md`.

## The six live assets, train period, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pay | 0.68 (0.18) | +10.6% | 17.0% | 55.0% | 6.5 | 78% | 1.06 | -0.00 | 0.78 | 1.46 | 0.49 | -0.37 (p=1.00; -0.59..-0.15) | 0/5 |
| logit-pay | 0.77 (0.18) | +13.8% | 19.0% | 52.7% | 2.3 | 91% | 1.38 | 0.00 | 1.16 | 1.41 | 0.52 | -0.27 (p=0.99; -0.48..-0.08) | 1/5 |
| tree-pay | 0.67 (0.18) | +11.2% | 18.4% | 58.7% | 3.2 | 82% | 1.32 | -0.11 | 0.80 | 1.53 | 0.38 | -0.38 (p=1.00; -0.61..-0.16) | 1/5 |
| gbm-raw | 0.74 (0.18) | +11.8% | 16.9% | 55.7% | 5.7 | 78% | 1.12 | 0.06 | 0.82 | 1.45 | 0.67 | -0.30 (p=1.00; -0.51..-0.10) | 0/5 |
| gbm | 0.81 (0.18) | +11.8% | 15.0% | 46.0% | 9.6 | 70% | 1.20 | 0.09 | 1.08 | 1.37 | 1.05 | -0.23 (p=0.95; -0.46..+0.00) | 1/5 |
| logit | 0.89 (0.18) | +15.5% | 18.1% | 58.5% | 3.5 | 89% | 1.34 | -0.00 | 1.67 | 1.55 | 0.63 | -0.16 (p=0.95; -0.32..-0.01) | 2/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-pay | -54% | -3% | -6% | -32% | -14% | -38% | -38% |
| logit-pay | -48% | -15% | -24% | -39% | -3% | -39% | -42% |
| tree-pay | -57% | -5% | -9% | -37% | -8% | -21% | -42% |
| gbm-raw | -56% | -5% | -14% | -24% | -13% | -37% | -30% |
| gbm | -45% | -0% | -8% | -13% | +1% | -38% | -19% |
| logit | -59% | -14% | -16% | -31% | -7% | -33% | -36% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: gbm-pay +10.1%, logit-pay +12.9%, tree-pay +10.6%, gbm-raw +11.1%, gbm +11.1%, logit +14.4%, tsmom12 +16.4%, equal-weight +16.7%

## Forecast skill on the six assets (walk-forward forecasts, 28 days ahead)

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone | Size-weighted hit rate | ...of always up | ...of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pay | 6214 | 59.3% | 0.488 | 55.0% | 79.7% | 0.522 | 56.6% | 52.1% | 59.9% | 58.2% |
| logit-pay | 6214 | 59.3% | 0.489 | 57.6% | 92.3% | 0.522 | 56.6% | 53.6% | 59.9% | 58.2% |
| tree-pay | 6214 | 59.3% | 0.480 | 54.6% | 81.7% | 0.522 | 56.6% | 51.7% | 59.9% | 58.2% |
| gbm-raw | 6214 | 59.3% | 0.478 | 55.9% | 81.1% | 0.522 | 56.6% | 53.1% | 59.9% | 58.2% |
| gbm | 6214 | 59.3% | 0.509 | 56.2% | 85.4% | 0.522 | 56.6% | 52.9% | 59.9% | 58.2% |
| logit | 6214 | 59.3% | 0.494 | 59.3% | 99.8% | 0.522 | 56.6% | 59.6% | 59.9% | 58.2% |

## The two-question rule `tree-pay` found

At three of its yearly fits (left branch = condition true; class 1.0 = hold):

Fit of 2000 (1922 rows):

```
|--- log_vol <= -2.46
|   |--- class: 0.0
|--- log_vol >  -2.46
|   |--- sma_gap <= -0.10
|   |   |--- class: 1.0
|   |--- sma_gap >  -0.10
|   |   |--- class: 1.0
```

Fit of 2012 (3913 rows):

```
|--- log_vol <= -0.91
|   |--- breadth <= 0.88
|   |   |--- class: 1.0
|   |--- breadth >  0.88
|   |   |--- class: 1.0
|--- log_vol >  -0.91
|   |--- class: 0.0
```

Fit of 2025 (7640 rows):

```
|--- dd_1y <= -0.20
|   |--- univ_vol_shock <= -0.19
|   |   |--- class: 1.0
|   |--- univ_vol_shock >  -0.19
|   |   |--- class: 1.0
|--- dd_1y >  -0.20
|   |--- log_vol <= -1.47
|   |   |--- class: 1.0
|   |--- log_vol >  -1.47
|   |   |--- class: 1.0
```

## Settings chosen by purged CV (six assets)

- `logit-pay`: 32 yearly fits, 1617 rows at the first, 7640 at the last. Chosen: C=0.001: 32 fits.

## Out of universe: etf, from 2007-01-05

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pay@etf | 0.21 (0.23) | +1.8% | 11.8% | 38.9% | 11.7 | 74% | -0.01 | -0.02 | 1.20 | 0.07 | -0.26 (p=0.91; -0.56..+0.08) | 1/4 |
| tsmom12@etf | 0.47 (0.23) | +3.7% | 8.5% | 16.5% | 3.0 | 64% | 0.45 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.47 (0.23) | +6.0% | 14.8% | 43.1% | 0.3 | 100% | 0.27 | 0.46 | 0.76 | 0.52 | +0.00 (p=0.49; -0.27..+0.27) | 2/4 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone | Size-weighted hit rate | ...of always up | ...of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pay | 7555 | 57.3% | 0.488 | 52.4% | 73.8% | 0.514 | 53.5% | 49.6% | 54.5% | 51.5% |

## Out of universe: coin, from 2023-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pay@coin | 0.77 (0.57) | +28.2% | 45.7% | 41.6% | 10.1 | 63% | 0.77 | +0.22 (p=0.28; -0.42..+0.81) | 1/1 |
| tsmom12@coin | 0.55 (0.59) | +15.9% | 47.5% | 46.1% | 5.3 | 56% | 0.55 | - | - |
| equal-weight@coin | 0.98 (0.58) | +53.8% | 66.4% | 53.5% | 2.8 | 100% | 0.98 | +0.43 (p=0.02; +0.08..+0.78) | 1/1 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone | Size-weighted hit rate | ...of always up | ...of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pay | 870 | 48.0% | 0.550 | 52.1% | 64.0% | 0.473 | 47.1% | 57.9% | 56.6% | 42.0% |

## Out of universe: idx, from 1974-01-04

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pay@idx | 0.61 (0.14) | +6.2% | 10.9% | 43.8% | 7.1 | 79% | 0.32 | 1.02 | 0.96 | 0.30 | 0.24 | 0.77 | 0.58 | -0.10 (p=0.81; -0.28..+0.08) | 2/7 |
| tsmom12@idx | 0.71 (0.14) | +6.2% | 9.1% | 25.7% | 2.3 | 70% | 0.69 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| equal-weight@idx | 0.59 (0.14) | +7.5% | 13.7% | 57.6% | 0.2 | 100% | 0.56 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | -0.11 (p=0.84; -0.30..+0.07) | 5/7 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone | Size-weighted hit rate | ...of always up | ...of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pay | 9427 | 59.3% | 0.524 | 56.6% | 79.6% | 0.530 | 56.5% | 55.0% | 56.7% | 54.8% |

## Pass bar (primary variant `gbm-pay`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.37, p = 1.00)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (55.0% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.26, coin +0.22, idx -0.10)
- FAIL: 5. Beats equal weight on Sharpe (0.68 vs 0.88)

**FAILS train.**

## Verdict (2026-11-12)

Dead. Training on payoff instead of direction made the models worse, not better: 0.67 to 0.77
Sharpe for the four variants, against 0.81 and 0.89 for the same models trained on direction,
0.88 for equal weight and 1.05 for `tsmom12` (all p >= 0.99 the wrong way). Worst loss 53% to
59% against 37% for `tsmom12`. Out of universe the primary is behind on the other ETFs and the
indexes and ahead on the other coins, where the test is three years long and says nothing
(standard error 0.57).

The claim was that a model aimed at payoff would rediscover the trend rule and improve on it.
It did not rediscover it:

- Counting each month by the size of its move, the payoff models call 52% to 54% right.
  "Always up" calls 60% and the 12-month flag alone 58%. They are worse than no model at the
  thing they were trained for.
- The two-question tree, the readable variant, never asks about trend. Its first question is
  volatility in 2000 and 2012 (in opposite directions) and the one-year drawdown in 2025, when
  all four of its leaves say "hold". A rule that changes its mind about what matters at each
  fit is fitted to the few large moves in its sample, as the card feared.
- Purged CV chose the strongest shrinkage for the logistic model at all 32 fits: its own
  validation says there is nothing to fit.

Same reading as the other four ML cards: nothing in these 15 features forecasts the next month
on six assets, whichever target the model is given. The held-out year was not looked at.
