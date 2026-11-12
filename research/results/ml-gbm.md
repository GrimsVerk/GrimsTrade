# ml-gbm: gradient boosting on simple features

Card: `cards/ml-gbm.md`. Protocol: `protocol.md`.

## The six live assets, train period, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm | 0.81 (0.18) | +11.8% | 15.0% | 46.0% | 9.6 | 70% | 1.20 | 0.09 | 1.08 | 1.37 | 1.05 | -0.23 (p=0.95; -0.46..+0.00) | 1/5 |
| gbm-hard | 0.72 (0.18) | +11.8% | 17.6% | 53.1% | 6.8 | 83% | 1.12 | 0.00 | 0.92 | 1.39 | 0.88 | -0.32 (p=0.99; -0.56..-0.10) | 0/5 |
| gbm-reg | 0.78 (0.18) | +12.2% | 16.6% | 46.9% | 8.0 | 68% | 1.19 | 0.08 | 0.66 | 1.51 | 0.82 | -0.27 (p=0.99; -0.47..-0.07) | 1/5 |
| gbm-cv | 0.79 (0.18) | +13.1% | 17.6% | 58.2% | 4.2 | 84% | 1.24 | -0.02 | 1.42 | 1.55 | 0.43 | -0.26 (p=0.99; -0.45..-0.07) | 1/5 |
| gbm-d1 | 0.72 (0.18) | +11.0% | 16.2% | 53.3% | 4.7 | 80% | 1.11 | -0.03 | 1.10 | 1.37 | 0.81 | -0.32 (p=1.00; -0.53..-0.12) | 0/5 |
| gbm-d6 | 0.78 (0.18) | +11.1% | 15.0% | 45.6% | 11.8 | 66% | 1.26 | 0.04 | 1.02 | 1.28 | 1.11 | -0.27 (p=0.97; -0.52..-0.03) | 1/5 |
| gbm-n25 | 0.75 (0.18) | +11.6% | 16.3% | 49.4% | 6.4 | 78% | 1.17 | 0.02 | 1.02 | 1.43 | 0.66 | -0.29 (p=0.99; -0.51..-0.09) | 0/5 |
| gbm-n400 | 0.76 (0.18) | +10.7% | 14.9% | 52.8% | 12.8 | 63% | 1.35 | 0.05 | 0.84 | 1.25 | 1.09 | -0.29 (p=0.98; -0.54..-0.04) | 2/5 |
| gbm-leaf20 | 0.86 (0.18) | +12.5% | 14.9% | 47.3% | 9.4 | 70% | 1.21 | 0.13 | 1.19 | 1.38 | 1.06 | -0.18 (p=0.92; -0.40..+0.04) | 1/5 |
| logit | 0.89 (0.18) | +15.5% | 18.1% | 58.5% | 3.5 | 89% | 1.34 | -0.00 | 1.67 | 1.55 | 0.63 | -0.16 (p=0.95; -0.32..-0.01) | 2/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| sma200 | 1.01 (0.18) | +15.9% | 15.8% | 44.4% | 4.3 | 70% | 1.14 | 0.14 | 1.58 | 1.53 | 0.75 | -0.04 (p=0.69; -0.18..+0.09) | 2/5 |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm | -45% | -0% | -8% | -13% | +1% | -38% | -19% |
| gbm-hard | -52% | -8% | -15% | -16% | -6% | -44% | -19% |
| gbm-reg | -46% | +4% | -9% | -12% | -10% | -38% | -20% |
| gbm-cv | -58% | -3% | -17% | -33% | +4% | -40% | -39% |
| gbm-d1 | -51% | -5% | -15% | -24% | -2% | -43% | -29% |
| gbm-d6 | -44% | -2% | -8% | -9% | -2% | -33% | -15% |
| gbm-n25 | -49% | -4% | -14% | -24% | -3% | -40% | -31% |
| gbm-n400 | -53% | +6% | -10% | -17% | -5% | -30% | -20% |
| gbm-leaf20 | -44% | +1% | -7% | -15% | +6% | -33% | -19% |
| logit | -59% | -14% | -16% | -31% | -7% | -33% | -36% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| sma200 | -33% | +2% | -14% | -12% | -4% | -23% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: gbm +11.1%, gbm-hard +11.2%, gbm-reg +11.5%, gbm-cv +12.4%, gbm-d1 +10.4%, gbm-d6 +10.5%, gbm-n25 +11.0%, gbm-n400 +10.2%, gbm-leaf20 +11.8%, logit +14.4%, tsmom12 +16.4%, sma200 +14.7%, equal-weight +16.7%

## Forecast skill on the six assets (walk-forward forecasts, 28 days ahead)

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm | 6214 | 59.3% | 0.509 | 56.2% | 85.4% | 0.522 | 56.6% |
| gbm-reg | 6214 | 59.3% | 0.490 | 55.6% | 81.7% | 0.522 | 56.6% |
| gbm-cv | 6214 | 59.3% | 0.502 | 59.1% | 98.4% | 0.522 | 56.6% |
| gbm-d1 | 6214 | 59.3% | 0.503 | 58.2% | 96.1% | 0.522 | 56.6% |
| gbm-d6 | 6214 | 59.3% | 0.506 | 55.5% | 78.9% | 0.522 | 56.6% |
| gbm-n25 | 6214 | 59.3% | 0.508 | 58.1% | 95.0% | 0.522 | 56.6% |
| gbm-n400 | 6214 | 59.3% | 0.503 | 54.3% | 74.9% | 0.522 | 56.6% |
| gbm-leaf20 | 6214 | 59.3% | 0.509 | 57.0% | 84.1% | 0.522 | 56.6% |
| logit | 6214 | 59.3% | 0.494 | 59.3% | 99.8% | 0.522 | 56.6% |

## Settings chosen by purged CV (six assets)

- `gbm-cv`: 32 yearly fits, 1617 rows at the first, 7640 at the last. Chosen: max_depth=1, max_iter=25: 18 fits; max_depth=3, max_iter=25: 12 fits; max_depth=1, max_iter=100: 2 fits.

## What the last `gbm` model leans on

Drop in AUC on its own training rows when one feature is shuffled (in-sample: it shows what the model uses, not what is true):

`log_vol` +0.047, `since_high` +0.026, `vol_shock` +0.023, `univ_vol_shock` +0.019, `z30` +0.016, `z365` +0.016, `z7` +0.015, `breadth` +0.013, `univ_mom_1m` +0.013, `sma_gap` +0.012, `z91` +0.011, `z182` +0.011, `rank_12m` +0.009, `dd_1y` +0.005, `up_12m` +0.000

## Out of universe: etf, from 2007-01-05

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm@etf | 0.23 (0.23) | +2.0% | 11.1% | 34.0% | 10.4 | 69% | 0.06 | 0.16 | 0.72 | 0.16 | -0.23 (p=0.91; -0.51..+0.06) | 1/4 |
| tsmom12@etf | 0.47 (0.23) | +3.7% | 8.5% | 16.5% | 3.0 | 64% | 0.45 | 0.44 | 0.44 | 0.59 | - | - |
| sma200@etf | 0.49 (0.23) | +3.7% | 8.1% | 16.8% | 3.9 | 64% | 0.69 | 0.36 | 0.66 | 0.31 | +0.02 (p=0.46; -0.18..+0.20) | 2/4 |
| equal-weight@etf | 0.47 (0.23) | +6.0% | 14.8% | 43.1% | 0.3 | 100% | 0.27 | 0.46 | 0.76 | 0.52 | +0.00 (p=0.49; -0.27..+0.27) | 2/4 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm | 7555 | 57.3% | 0.481 | 54.5% | 84.9% | 0.514 | 53.5% |

## Out of universe: coin, from 2023-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm@coin | 0.78 (0.56) | +26.7% | 40.3% | 35.1% | 11.5 | 51% | 0.78 | +0.24 (p=0.29; -0.49..+0.89) | 1/1 |
| tsmom12@coin | 0.55 (0.59) | +15.9% | 47.5% | 46.1% | 5.3 | 56% | 0.55 | - | - |
| sma200@coin | 0.51 (0.59) | +13.9% | 48.9% | 45.8% | 6.4 | 53% | 0.51 | -0.04 (p=0.58; -0.32..+0.22) | 0/1 |
| equal-weight@coin | 0.98 (0.58) | +53.8% | 66.4% | 53.5% | 2.8 | 100% | 0.98 | +0.43 (p=0.02; +0.08..+0.78) | 1/1 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm | 870 | 48.0% | 0.548 | 52.8% | 57.8% | 0.473 | 47.1% |

## Out of universe: idx, from 1974-01-04

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gbm@idx | 0.59 (0.14) | +5.4% | 9.7% | 41.1% | 9.2 | 69% | 0.34 | 0.93 | 1.03 | 0.26 | 0.31 | 0.58 | 0.65 | -0.12 (p=0.89; -0.28..+0.05) | 1/7 |
| tsmom12@idx | 0.71 (0.14) | +6.2% | 9.1% | 25.7% | 2.3 | 70% | 0.69 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| sma200@idx | 0.67 (0.14) | +5.4% | 8.3% | 23.5% | 3.8 | 68% | 0.55 | 1.10 | 1.00 | 0.37 | 0.25 | 0.30 | 0.92 | -0.04 (p=0.67; -0.17..+0.09) | 2/7 |
| equal-weight@idx | 0.59 (0.14) | +7.5% | 13.7% | 57.6% | 0.2 | 100% | 0.56 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | -0.11 (p=0.84; -0.30..+0.07) | 5/7 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| gbm | 9427 | 59.3% | 0.529 | 57.6% | 85.3% | 0.530 | 56.5% |

## Pass bar (primary variant `gbm`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.23, p = 0.95)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (1 of 5)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (46.0% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.23, coin +0.24, idx -0.12)
- FAIL: 5. Beats equal weight on Sharpe (0.81 vs 0.88)
- FAIL: 6. Not behind `ml-linear/logit` on Sharpe (0.81 vs 0.89)
- FAIL: 7. Median Sharpe of the five sweep settings ahead of `tsmom12` (0.76 vs 1.05; sweep 0.72, 0.78, 0.75, 0.76, 0.86)

**FAILS train.**
## Verdict (2026-11-12)

Dead, on every count of its bar. All nine settings landed between 0.72 and 0.86 Sharpe: below
`tsmom12` (1.05), below the linear model (0.89) and below simply holding everything (0.88). No
setting was close, so this is not a matter of tuning: the spread across settings (0.14) is
smaller than the gap to the trend rule.

- **Boosting did not beat the linear baseline.** The linear model found nothing and held
  everything. Boosting also found nothing, but acted on it: its forecasts wobble around the
  average, so it traded 10 times its equity a year (the trend rule: 2.7) in and out of
  positions for no gain. More trees, deeper trees and smaller leaves all made that worse.
- **Forecast skill is nil.** AUC 0.50-0.51 on 6,214 walk-forward forecasts, against 0.522 for
  the single flag `up_12m`. The fitted models are worse at ranking months than the one feature
  they were given as a starting point.
- **Purged CV saw it coming.** Asked to choose, it picked the smallest model on offer at 30 of
  32 fits (25 trees). When honest validation keeps choosing "as little model as possible", the
  features hold no signal the model can use.
- **It did protect a little.** The models leaned on volatility (`log_vol`, `vol_shock`) and cut
  positions when it was high: worst loss 46% against 69% for equal weight, small losses in 2008
  and 2020. That is volatility targeting found the expensive way; run 1's `trend-vol` does it
  with two lines (worst loss 26%).
- **Out of universe:** behind `tsmom12` on other ETFs (-0.23) and the indexes (-0.12); ahead on
  other coins over three years (+0.24, p = 0.29), where plain holding beat both.

The held-out year was not looked at.
