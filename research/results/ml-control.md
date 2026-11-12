# Positive control: can the ML machinery find an edge that is really there?

Not a strategy and not a try: a 16th feature `peek` is planted that knows the future (correlation rho with the row's own 28-day risk-adjusted return, the rest noise). Everything else is the `ml-linear` and `ml-gbm` primary pipeline, unchanged: same rows, purged walk-forward, purged CV, sizing, gym and costs. `peek0.00` is pure noise.

## Six assets, 1994-2025

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| logit+peek0.00 | 0.88 (0.18) | +15.3% | 18.1% | 58.4% | 3.6 | 89% | -0.17 (p=0.96; -0.33..-0.02) | 2/5 |
| logit+peek0.03 | 0.88 (0.18) | +15.3% | 18.0% | 58.0% | 4.8 | 89% | -0.17 (p=0.96; -0.33..-0.01) | 1/5 |
| logit+peek0.05 | 0.88 (0.18) | +15.1% | 17.9% | 57.4% | 6.3 | 88% | -0.17 (p=0.96; -0.33..-0.01) | 1/5 |
| logit+peek0.10 | 0.90 (0.18) | +15.1% | 17.4% | 55.9% | 11.7 | 83% | -0.15 (p=0.93; -0.32..+0.02) | 2/5 |
| logit+peek0.20 | 1.08 (0.18) | +17.2% | 15.8% | 43.9% | 19.2 | 72% | +0.03 (p=0.40; -0.18..+0.26) | 4/5 |
| gbm+peek0.00 | 0.79 (0.18) | +11.3% | 15.0% | 46.5% | 9.4 | 70% | -0.26 (p=0.96; -0.50..-0.01) | 1/5 |
| gbm+peek0.03 | 0.80 (0.18) | +11.6% | 15.0% | 44.6% | 10.0 | 70% | -0.24 (p=0.95; -0.48..-0.01) | 1/5 |
| gbm+peek0.05 | 0.77 (0.18) | +11.1% | 15.1% | 42.9% | 10.4 | 70% | -0.27 (p=0.97; -0.51..-0.04) | 1/5 |
| gbm+peek0.10 | 0.81 (0.18) | +11.6% | 15.0% | 42.6% | 12.8 | 70% | -0.24 (p=0.96; -0.46..-0.01) | 2/5 |
| gbm+peek0.20 | 0.98 (0.18) | +14.6% | 15.1% | 37.7% | 17.7 | 68% | -0.07 (p=0.69; -0.30..+0.17) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

## Forecast skill

| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | AUC of `up_12m` alone | Hit rate of `up_12m` alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| logit+peek0.00 | 6214 | 59.3% | 0.493 | 59.3% | 99.8% | 0.522 | 56.6% |
| logit+peek0.03 | 6214 | 59.3% | 0.500 | 59.3% | 99.8% | 0.522 | 56.6% |
| logit+peek0.05 | 6214 | 59.3% | 0.504 | 59.1% | 99.5% | 0.522 | 56.6% |
| logit+peek0.10 | 6214 | 59.3% | 0.524 | 58.9% | 97.2% | 0.522 | 56.6% |
| logit+peek0.20 | 6214 | 59.3% | 0.571 | 59.2% | 85.5% | 0.522 | 56.6% |
| gbm+peek0.00 | 6214 | 59.3% | 0.508 | 56.7% | 85.4% | 0.522 | 56.6% |
| gbm+peek0.03 | 6214 | 59.3% | 0.509 | 56.5% | 85.6% | 0.522 | 56.6% |
| gbm+peek0.05 | 6214 | 59.3% | 0.509 | 56.6% | 85.6% | 0.522 | 56.6% |
| gbm+peek0.10 | 6214 | 59.3% | 0.523 | 56.8% | 84.9% | 0.522 | 56.6% |
| gbm+peek0.20 | 6214 | 59.3% | 0.562 | 58.4% | 79.9% | 0.522 | 56.6% |
## Reading (2026-11-12, first pass)

Two things, and the second is a fault in this run's own test design.

1. **The machinery sees a planted signal.** AUC climbs with the planted correlation: 0.50 at
   0.05, 0.52 at 0.10, 0.57 at 0.20, for both model kinds. Against that scale the real models'
   0.49 to 0.51 means: whatever the 15 features know about next month is worth less than a
   signal of correlation 0.05, if anything.
2. **The sizing rule fixed in the protocol wastes most of a signal.** Even with a feature that
   knows the future at correlation 0.20 (far better than anything real), the portfolios only
   reach `tsmom12`'s Sharpe (1.08 and 0.98 against 1.05). The rule gives a full slot at average
   confidence and above, so the position hardly moves unless the model expects an outright
   loss. With that rule no realistic edge could have passed the three cards' Sharpe bars. Their
   skill tables stand (they do not depend on sizing); their Sharpe comparisons say less than
   they seem to.

Follow-up: card `ml-sizing` tests two converters that let the position follow the forecast,
first on this control, then on the real models.
