# ml-weekly: the same models forecasting one week ahead instead of four

Card: `cards/ml-weekly.md`. Protocol: `protocol.md`.

## The six live assets, train period, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-wk | 0.82 (0.18) | +12.4% | 15.8% | 45.7% | 11.8 | 69% | 0.95 | 0.06 | 0.91 | 1.75 | 0.96 | -0.23 (p=0.96; -0.44..-0.02) | 2/5 |
| logit-wk | 0.89 (0.18) | +15.5% | 18.1% | 57.1% | 2.1 | 90% | 1.34 | -0.03 | 1.55 | 1.57 | 0.74 | -0.16 (p=0.96; -0.31..-0.01) | 1/5 |
| gbm-wk-low | 0.83 (0.18) | +14.0% | 17.6% | 54.7% | 9.1 | 77% | 1.12 | 0.02 | 1.03 | 1.77 | 0.78 | -0.21 (p=0.95; -0.44..-0.00) | 1/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-wk | -46% | +0% | -9% | -12% | -17% | -25% | -18% |
| logit-wk | -57% | -12% | -19% | -27% | -8% | -36% | -33% |
| gbm-wk-low | -55% | +4% | -13% | -15% | -14% | -24% | -23% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: gbm-wk +11.7%, logit-wk +14.4%, gbm-wk-low +13.1%, tsmom12 +16.4%, equal-weight +16.7%

## Forecast skill on the six assets (walk-forward forecasts, 7 days ahead)

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-wk | 6232 | 55.5% | 0.510 | 54.0% | 85.8% | 0.513 | 53.9% |
| logit-wk | 6232 | 55.5% | 0.496 | 55.5% | 100.0% | 0.513 | 53.9% |

## Settings chosen by purged CV (six assets)

- `logit-wk`: 32 yearly fits, 1620 rows at the first, 7661 at the last. Chosen: C=0.001: 31 fits; C=0.01: 1 fits.

## Out of universe: etf, from 2007-01-05

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-wk@etf | 0.24 (0.23) | +2.0% | 10.5% | 37.4% | 14.6 | 68% | -0.02 | 0.33 | 0.56 | 0.14 | -0.22 (p=0.88; -0.52..+0.07) | 1/4 |
| tsmom12@etf | 0.47 (0.23) | +3.7% | 8.5% | 16.5% | 3.0 | 64% | 0.45 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.47 (0.23) | +6.0% | 14.8% | 43.1% | 0.3 | 100% | 0.27 | 0.46 | 0.76 | 0.52 | +0.00 (p=0.49; -0.27..+0.27) | 2/4 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-wk | 7579 | 54.5% | 0.497 | 52.9% | 82.6% | 0.515 | 52.8% |

## Out of universe: coin, from 2023-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-wk@coin | 1.01 (0.55) | +30.1% | 30.6% | 23.1% | 18.3 | 27% | 1.01 | +0.46 (p=0.16; -0.31..+1.31) | 1/1 |
| tsmom12@coin | 0.55 (0.59) | +15.9% | 47.5% | 46.1% | 5.3 | 56% | 0.55 | - | - |
| equal-weight@coin | 0.98 (0.58) | +53.8% | 66.4% | 53.5% | 2.8 | 100% | 0.98 | +0.43 (p=0.02; +0.08..+0.78) | 1/1 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-wk | 888 | 49.7% | 0.566 | 53.8% | 34.3% | 0.469 | 46.8% |

## Out of universe: idx, from 1974-01-04

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm-wk@idx | 0.67 (0.14) | +6.0% | 9.4% | 31.5% | 12.4 | 65% | 0.58 | 0.89 | 1.08 | 0.43 | 0.48 | 0.41 | 0.87 | -0.04 (p=0.64; -0.21..+0.12) | 3/7 |
| tsmom12@idx | 0.71 (0.14) | +6.2% | 9.1% | 25.7% | 2.3 | 70% | 0.69 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| equal-weight@idx | 0.59 (0.14) | +7.5% | 13.7% | 57.6% | 0.2 | 100% | 0.56 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | -0.11 (p=0.84; -0.30..+0.07) | 5/7 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm-wk | 9436 | 55.4% | 0.518 | 54.5% | 80.8% | 0.522 | 54.3% |

## Pass bar (primary variant `gbm-wk`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.23, p = 0.96)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (45.7% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.22, coin +0.46, idx -0.04)
- FAIL: 5. Beats equal weight on Sharpe (0.82 vs 0.88)

**FAILS train.**

## Verdict (2026-11-12)

Dead. Forecasting one week ahead instead of four found no more: AUC 0.510 for the boosted
model and 0.496 for the logistic one on 6,232 forecasts, under the 0.52 the card asked for
and under the 12-month flag alone (0.513 at this horizon). Purged CV chose the strongest
shrinkage for the logistic model at 31 of 32 fits, as at four weeks.

As portfolios: 0.82 (`gbm-wk`), 0.89 (`logit-wk`, which said "up" every single week and so is
equal weight) and 0.83 (`gbm-wk-low`), against 1.05 for `tsmom12` and 0.88 for equal weight,
each with p >= 0.95 the wrong way. The boosted model traded 12 times its equity a year for
that. Out of universe it is behind `tsmom12` on the other ETFs and the indexes; ahead on the
other coins over three years (+0.46, p = 0.16, AUC 0.57 on 888 forecasts), the same
short-sample flicker the monthly models showed there, and still only level with holding the
coins (1.01 against 0.98).

More bets do not help when there is nothing to bet on: four times the decisions at a quarter
of the signal each. The held-out year was not looked at.
