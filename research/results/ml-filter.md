# ml-filter: the 12-month trend rule with a model deciding how much to trust it

Card: `cards/ml-filter.md`. Protocol: `protocol.md`.

## The six live assets, train period, from 1994-02-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| meta-gbm | 0.73 (0.18) | +8.7% | 12.5% | 28.3% | 8.0 | 56% | 1.15 | 0.26 | 0.76 | 0.84 | 1.03 | -0.32 (p=1.00; -0.50..-0.12) | 2/5 |
| meta-logit | 0.94 (0.18) | +13.4% | 14.5% | 29.4% | 3.4 | 69% | 1.28 | 0.21 | 1.21 | 1.49 | 0.85 | -0.11 (p=0.96; -0.22..-0.01) | 1/5 |
| and-gbm | 0.86 (0.18) | +11.0% | 13.1% | 29.6% | 7.0 | 59% | 1.16 | 0.23 | 0.97 | 1.40 | 0.97 | -0.19 (p=0.95; -0.38..+0.01) | 2/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| meta-gbm | -26% | +3% | -6% | -12% | +5% | -23% | -18% |
| meta-logit | -26% | -3% | -13% | -13% | +0% | -20% | -18% |
| and-gbm | -27% | +5% | -7% | -12% | +11% | -20% | -17% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: meta-gbm +8.3%, meta-logit +12.5%, and-gbm +10.4%, tsmom12 +16.4%, equal-weight +16.7%

## Forecast skill on the six assets (walk-forward forecasts, 28 days ahead)

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| meta-gbm | 4573 | 60.8% | 0.503 | 58.2% | 89.0% | - | 60.8% |
| meta-logit | 4573 | 60.8% | 0.482 | 60.7% | 99.8% | - | 60.8% |

## Out of universe: etf, from 2007-01-05

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| meta-gbm@etf | 0.38 (0.23) | +2.4% | 6.9% | 17.2% | 8.2 | 45% | 0.59 | 0.17 | 0.57 | 0.45 | -0.09 (p=0.87; -0.24..+0.05) | 2/4 |
| tsmom12@etf | 0.47 (0.23) | +3.7% | 8.5% | 16.5% | 3.0 | 64% | 0.45 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.47 (0.23) | +6.0% | 14.8% | 43.1% | 0.3 | 100% | 0.27 | 0.46 | 0.76 | 0.52 | +0.00 (p=0.49; -0.27..+0.27) | 2/4 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| meta-gbm | 4859 | 58.4% | 0.506 | 56.0% | 86.5% | - | 58.4% |

## Out of universe: coin, from 2023-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| meta-gbm@coin | 0.17 (0.59) | +1.0% | 27.7% | 39.6% | 10.6 | 28% | 0.17 | -0.37 (p=0.90; -0.86..+0.11) | 0/1 |
| tsmom12@coin | 0.55 (0.59) | +15.9% | 47.5% | 46.1% | 5.3 | 56% | 0.55 | - | - |
| equal-weight@coin | 0.98 (0.58) | +53.8% | 66.4% | 53.5% | 2.8 | 100% | 0.98 | +0.43 (p=0.02; +0.08..+0.78) | 1/1 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| meta-gbm | 484 | 45.7% | 0.453 | 46.5% | 55.8% | - | 45.7% |

## Out of universe: idx, from 1974-01-04

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| meta-gbm@idx | 0.62 (0.14) | +4.5% | 7.5% | 21.7% | 8.1 | 51% | 0.40 | 0.84 | 1.05 | 0.54 | 0.35 | 0.34 | 0.54 | -0.09 (p=0.93; -0.19..+0.01) | 2/7 |
| tsmom12@idx | 0.71 (0.14) | +6.2% | 9.1% | 25.7% | 2.3 | 70% | 0.69 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| equal-weight@idx | 0.59 (0.14) | +7.5% | 13.7% | 57.6% | 0.2 | 100% | 0.56 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | -0.11 (p=0.84; -0.30..+0.07) | 5/7 |

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| meta-gbm | 6568 | 61.3% | 0.520 | 59.5% | 90.3% | - | 61.3% |

## Pass bar (primary variant `meta-gbm`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.32, p = 1.00)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (28.3% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.09, coin -0.37, idx -0.09)
- FAIL: 5. Beats equal weight on Sharpe (0.73 vs 0.88)

**FAILS train.**
## Verdict (2026-11-12)

Dead. A model grading the trend rule's trades made the rule worse in all three forms: 0.73
(`meta-gbm`), 0.94 (`meta-logit`) and 0.86 (`and-gbm`) against 1.05 for `tsmom12` alone, each
with p >= 0.95 the wrong way, and behind in all three out-of-universe sets.

The models could not tell the rule's good trades from its bad ones (AUC 0.50 and 0.48 on 4,573
forecasts made while the rule was holding). What a filter with no skill does is take positions
off at random: exposure fell from 76% to 56%, growth halved (8.7% a year against 17.8%), and
turnover tripled. The worst loss did shrink (28% against 37%), but that is what holding less
does; `trend-vol` from run 1 gets to 26% while keeping 13% a year.

The least bad form is the one where the model does least (`meta-logit`, which said "keep the
trade" 99.8% of the time).

The held-out year was not looked at.
