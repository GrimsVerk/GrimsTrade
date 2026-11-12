# Positive control: can the ML machinery find an edge that is really there?

Not a strategy and not a try: a 16th feature `peek` is planted that knows the future (correlation rho with the row's own 28-day risk-adjusted return, the rest noise). Everything else is the `ml-linear` and `ml-gbm` primary pipeline, unchanged: same rows, purged walk-forward, purged CV, gym and costs. `peek0.00` is pure noise. One table per position rule (`protocol.md`).

## Six assets, 1994-2025, first rule: full slot at average confidence

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

## Six assets, 1994-2025, `-prop`: position in proportion to confidence

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| logit+peek0.00-prop | 0.75 (0.18) | +8.2% | 11.3% | 46.2% | 2.7 | 52% | -0.30 (p=1.00; -0.46..-0.13) | 2/5 |
| logit+peek0.03-prop | 0.76 (0.18) | +8.5% | 11.6% | 46.1% | 4.2 | 53% | -0.29 (p=1.00; -0.46..-0.12) | 1/5 |
| logit+peek0.05-prop | 0.77 (0.18) | +8.6% | 11.6% | 45.6% | 5.6 | 53% | -0.28 (p=1.00; -0.45..-0.11) | 1/5 |
| logit+peek0.10-prop | 0.84 (0.18) | +9.6% | 11.8% | 43.5% | 10.9 | 53% | -0.21 (p=0.97; -0.39..-0.02) | 2/5 |
| logit+peek0.20-prop | 1.08 (0.18) | +13.2% | 12.2% | 38.4% | 19.0 | 53% | +0.03 (p=0.43; -0.20..+0.26) | 4/5 |
| gbm+peek0.00-prop | 0.74 (0.18) | +8.2% | 11.6% | 37.1% | 9.2 | 51% | -0.31 (p=0.99; -0.55..-0.06) | 1/5 |
| gbm+peek0.03-prop | 0.73 (0.18) | +8.1% | 11.7% | 36.6% | 9.7 | 51% | -0.32 (p=0.99; -0.56..-0.07) | 1/5 |
| gbm+peek0.05-prop | 0.73 (0.18) | +8.2% | 11.7% | 35.3% | 10.3 | 51% | -0.32 (p=0.99; -0.56..-0.08) | 1/5 |
| gbm+peek0.10-prop | 0.80 (0.18) | +9.2% | 11.8% | 31.2% | 12.9 | 51% | -0.24 (p=0.95; -0.48..-0.00) | 2/5 |
| gbm+peek0.20-prop | 0.99 (0.18) | +11.8% | 12.0% | 27.0% | 17.6 | 52% | -0.06 (p=0.65; -0.30..+0.18) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

## Six assets, 1994-2025, `-low`: out on the weakest quarter of forecasts

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| logit+peek0.00-low | 0.82 (0.18) | +12.0% | 15.3% | 37.7% | 6.7 | 73% | -0.23 (p=0.99; -0.41..-0.05) | 1/5 |
| logit+peek0.03-low | 0.83 (0.18) | +12.2% | 15.3% | 39.7% | 8.5 | 73% | -0.22 (p=0.98; -0.39..-0.05) | 0/5 |
| logit+peek0.05-low | 0.84 (0.18) | +12.6% | 15.6% | 41.1% | 10.6 | 73% | -0.21 (p=0.98; -0.38..-0.04) | 0/5 |
| logit+peek0.10-low | 0.90 (0.18) | +13.9% | 15.8% | 42.6% | 15.7 | 72% | -0.14 (p=0.90; -0.32..+0.03) | 1/5 |
| logit+peek0.20-low | 1.07 (0.18) | +17.8% | 16.7% | 41.5% | 18.6 | 74% | +0.02 (p=0.44; -0.20..+0.23) | 4/5 |
| gbm+peek0.00-low | 0.76 (0.18) | +11.3% | 15.7% | 52.3% | 9.2 | 73% | -0.29 (p=0.98; -0.54..-0.04) | 1/5 |
| gbm+peek0.03-low | 0.83 (0.18) | +12.6% | 15.7% | 45.0% | 10.1 | 73% | -0.21 (p=0.93; -0.45..+0.03) | 1/5 |
| gbm+peek0.05-low | 0.80 (0.18) | +12.1% | 15.8% | 42.5% | 10.6 | 73% | -0.24 (p=0.95; -0.49..-0.00) | 0/5 |
| gbm+peek0.10-low | 0.81 (0.18) | +12.4% | 16.0% | 46.6% | 12.3 | 74% | -0.24 (p=0.96; -0.47..-0.01) | 1/5 |
| gbm+peek0.20-low | 0.96 (0.18) | +15.6% | 16.5% | 46.5% | 15.8 | 74% | -0.09 (p=0.73; -0.32..+0.15) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

## Forecast skill (the same for every position rule)

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
## Reading (2026-11-12)

1. **The machinery works.** A planted signal comes through: AUC 0.50 at correlation 0.05,
   0.52 at 0.10, 0.57 at 0.20, for both model kinds, and Sharpe rises with it under every
   position rule. The null results of the cards are not a plumbing fault.
2. **The real features hold less than a 0.05 signal.** The real models score AUC 0.49 to 0.51,
   which is where planted correlations of 0 to 0.05 land. With 6,214 overlapping forecasts
   (about 1,500 independent asset-months) nothing below roughly 0.10 can be told from zero.
3. **Even a forecaster far better than any real one only ties the trend rule.** At planted
   correlation 0.20 the portfolios reach 0.96 to 1.08 Sharpe against 1.05 for `tsmom12`,
   whichever of the three position rules is used; at 0.10 they are at 0.80 to 0.90, no better
   than holding everything. The first reading of this control blamed the position rule; the
   two sharper rules show it was not the rule.

Why point 3 is not a surprise in hindsight: a forecast's worth grows with the number of
independent bets it is used on (Grinold's rule: skill x square root of breadth). Six assets
that mostly move together, decided monthly, long only, are very few bets. A correlation of
0.20 on 13 months a year adds about 0.7 of Sharpe to a free long-short book and much less to
one that can only hold or not hold; added to what holding everything already earns (0.88) that
gives about 1.0 to 1.1, which is what the table shows. Return forecasting pays where there
are hundreds of assets to rank. On this book it would need a correlation above 0.3, which
nobody has.

What it means for the cards: their Sharpe bars against `tsmom12` could not have been passed by
any plausible direction forecast. They are judged on forecast skill, and there is none.
