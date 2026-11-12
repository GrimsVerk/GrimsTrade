# ml-pooled: the same models trained on 33 markets instead of six

Card: `cards/ml-pooled.md`. Protocol: `protocol.md`.

## The six live assets, train period, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pool | 0.70 (0.18) | +10.0% | 15.3% | 50.0% | 6.9 | 74% | 1.17 | 0.09 | 1.34 | 0.88 | 0.77 | -0.35 (p=0.99; -0.56..-0.12) | 0/5 |
| logit-pool | 0.92 (0.18) | +14.1% | 15.6% | 37.3% | 3.1 | 85% | 1.34 | 0.13 | 1.45 | 1.67 | 0.59 | -0.13 (p=0.89; -0.29..+0.04) | 1/5 |
| gbm-pool-low | 0.68 (0.18) | +10.4% | 16.4% | 45.4% | 7.3 | 77% | 1.16 | 0.16 | 1.27 | 0.49 | 0.87 | -0.37 (p=1.00; -0.59..-0.14) | 0/5 |
| gbm | 0.81 (0.18) | +11.8% | 15.0% | 46.0% | 9.6 | 70% | 1.20 | 0.09 | 1.08 | 1.37 | 1.05 | -0.23 (p=0.95; -0.46..+0.00) | 1/5 |
| logit | 0.89 (0.18) | +15.5% | 18.1% | 58.5% | 3.5 | 89% | 1.34 | -0.00 | 1.67 | 1.55 | 0.63 | -0.16 (p=0.95; -0.32..-0.01) | 2/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-pool | -50% | +3% | -6% | -19% | -5% | -35% | -25% |
| logit-pool | -36% | -12% | -14% | -29% | -4% | -24% | -32% |
| gbm-pool-low | -45% | +4% | -6% | -14% | -6% | -34% | -20% |
| gbm | -45% | -0% | -8% | -13% | +1% | -38% | -19% |
| logit | -59% | -14% | -16% | -31% | -7% | -33% | -36% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: gbm-pool +9.6%, logit-pool +13.2%, gbm-pool-low +9.9%, gbm +11.1%, logit +14.4%, tsmom12 +16.4%, equal-weight +16.7%

## Forecast skill on the six assets (walk-forward forecasts, 28 days ahead)

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-pool | 6214 | 59.3% | 0.499 | 57.3% | 90.8% | 0.522 | 56.6% |
| logit-pool | 6214 | 59.3% | 0.496 | 58.7% | 97.5% | 0.522 | 56.6% |
| gbm | 6214 | 59.3% | 0.509 | 56.2% | 85.4% | 0.522 | 56.6% |
| logit | 6214 | 59.3% | 0.494 | 59.3% | 99.8% | 0.522 | 56.6% |

## Training rows at the last fit, by set

| Set | Assets | Rows | Share that went up |
|---|---:|---:|---:|
| six | 6 | 6023 | 59.0% |
| etf | 8 | 8543 | 57.9% |
| sector | 9 | 11718 | 60.6% |
| coin | 6 | 1794 | 47.8% |
| idx | 4 | 10313 | 59.3% |

38391 rows in all, against 7640 for the six-asset models.

## Settings chosen by purged CV (six assets)

- `logit-pool`: 32 yearly fits, 3845 rows at the first, 38391 at the last. Chosen: C=0.001: 31 fits; C=0.01: 1 fits.

## Out of universe: etf, from 2007-01-05

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pool@etf | 0.48 (0.23) | +4.2% | 9.6% | 18.3% | 6.8 | 73% | 0.45 | 0.32 | 0.86 | 0.42 | +0.01 (p=0.48; -0.20..+0.23) | 2/4 |
| tsmom12@etf | 0.47 (0.23) | +3.7% | 8.5% | 16.5% | 3.0 | 64% | 0.45 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.47 (0.23) | +6.0% | 14.8% | 43.1% | 0.3 | 100% | 0.27 | 0.46 | 0.76 | 0.52 | +0.00 (p=0.49; -0.27..+0.27) | 2/4 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-pool | 7555 | 57.3% | 0.487 | 55.8% | 92.1% | 0.514 | 53.5% |

## Out of universe: coin, from 2023-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pool@coin | 0.50 (0.57) | +11.4% | 30.9% | 32.1% | 11.2 | 38% | 0.50 | -0.05 (p=0.56; -0.75..+0.62) | 0/1 |
| tsmom12@coin | 0.55 (0.59) | +15.9% | 47.5% | 46.1% | 5.3 | 56% | 0.55 | - | - |
| equal-weight@coin | 0.98 (0.58) | +53.8% | 66.4% | 53.5% | 2.8 | 100% | 0.98 | +0.43 (p=0.02; +0.08..+0.78) | 1/1 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-pool | 870 | 48.0% | 0.542 | 52.9% | 69.2% | 0.473 | 47.1% |

## Out of universe: idx, from 1974-01-04

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-pool@idx | 0.62 (0.14) | +5.8% | 10.0% | 47.6% | 7.8 | 71% | 0.34 | 0.93 | 1.02 | 0.27 | 0.59 | 0.43 | 0.80 | -0.09 (p=0.80; -0.28..+0.09) | 3/7 |
| tsmom12@idx | 0.71 (0.14) | +6.2% | 9.1% | 25.7% | 2.3 | 70% | 0.69 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| equal-weight@idx | 0.59 (0.14) | +7.5% | 13.7% | 57.6% | 0.2 | 100% | 0.56 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | -0.11 (p=0.84; -0.30..+0.07) | 5/7 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-pool | 9427 | 59.3% | 0.524 | 57.7% | 86.6% | 0.530 | 56.5% |

## Pass bar (primary variant `gbm-pool`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.35, p = 0.99)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (50.0% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf +0.01, coin -0.05, idx -0.09)
- FAIL: 5. Beats equal weight on Sharpe (0.70 vs 0.88)

**FAILS train.**

## Verdict (2026-11-12)

Dead. Five times the training rows (38,391 against 7,640 at the last fit) bought no forecast
skill on the six assets: AUC 0.499 for the boosted model and 0.496 for the logistic one,
against 0.509 and 0.494 for the same models on six-asset rows, and 0.522 for the 12-month
flag alone. The card's second reading asked for 0.53; it is not close.

As portfolios: `gbm-pool` 0.70 Sharpe and `gbm-pool-low` 0.68 (both worse than the unpooled
`gbm` at 0.81), `logit-pool` 0.92, against 1.05 for `tsmom12` and 0.88 for equal weight.
`logit-pool` is the best ML variant of the run and still 0.13 behind the trend rule (p = 0.89
the wrong way); its worst loss of 37% matches `tsmom12` because, taught by markets that fell
for years, it holds 85% on average instead of everything. Purged CV again chose the strongest
shrinkage at 31 of 32 fits. On the other sets the pooled model ties `tsmom12` on the other
ETFs (+0.01), and is behind on the coins and the indexes.

So "too little data" is answered as far as free daily prices can answer it: the same models
on 33 markets back to 1962 forecast next month no better than on six, and still worse than a
single trend feature left alone (`results/ml-feature-skill.md`). More markets of the
same kind are not the missing ingredient. The held-out year was not looked at.
