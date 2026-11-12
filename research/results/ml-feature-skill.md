# Forecast skill of each feature on its own (no model)

Not a strategy and not a try: no backtest. The six live assets, every Friday of the train period from 1994-02-01, 28-day labels: 6293 rows, 59.3% went up. AUC of the raw feature as a ranking of which asset-months go up (0.50 = coin toss; below 0.50 = the feature ranks them backwards). Standard error from resampling 13-week blocks. "Within asset" is the average AUC inside each asset: skill at timing, with the differences between assets taken out. The last three columns are the same AUC on the other market sets, over the periods of the model tests (etf: 7818 rows, coin: 870 rows, idx: 9452 rows).

| Feature | AUC | SE | Within asset | Other ETFs | Other coins | Indexes |
|---|---:|---:|---:|---:|---:|---:|
| `dd_1y` | 0.542 | 0.015 | 0.522 | 0.510 | 0.399 | 0.517 |
| `sma_gap` | 0.531 | 0.016 | 0.522 | 0.509 | 0.381 | 0.522 |
| `breadth` | 0.530 | 0.015 | 0.527 | 0.504 | 0.450 | 0.533 |
| `z365` | 0.528 | 0.015 | 0.517 | 0.505 | 0.455 | 0.525 |
| `z182` | 0.524 | 0.015 | 0.517 | 0.510 | 0.391 | 0.519 |
| `z7` | 0.524 | 0.007 | 0.523 | 0.494 | 0.475 | 0.508 |
| `z91` | 0.523 | 0.015 | 0.518 | 0.502 | 0.407 | 0.513 |
| `up_12m` | 0.520 | 0.012 | 0.515 | 0.514 | 0.473 | 0.530 |
| `z30` | 0.519 | 0.013 | 0.516 | 0.489 | 0.426 | 0.496 |
| `univ_mom_1m` | 0.516 | 0.014 | 0.517 | 0.491 | 0.395 | 0.494 |
| `rank_12m` | 0.510 | 0.012 | 0.496 | 0.513 | 0.501 | 0.517 |
| `univ_vol_shock` | 0.489 | 0.015 | 0.487 | 0.500 | 0.387 | 0.524 |
| `vol_shock` | 0.489 | 0.014 | 0.491 | 0.505 | 0.422 | 0.519 |
| `log_vol` | 0.471 | 0.014 | 0.468 | 0.503 | 0.392 | 0.482 |
| `since_high` | 0.461 | 0.015 | 0.479 | 0.478 | 0.544 | 0.473 |

## How strong the planted control signals really were

`lib/control_ml.py` plants `peek` = rho x risk-adjusted return + noise. The noise draw happens to correlate slightly with the outcome by chance (the 0.00 row), so each planted signal is about 0.02 stronger than its label:

| Label (rho) | Correlation with the risk-adjusted return | ...with the 28-day log return | AUC of `peek` alone |
|---:|---:|---:|---:|
| 0.00 | 0.024 | 0.021 | 0.505 |
| 0.03 | 0.053 | 0.042 | 0.518 |
| 0.05 | 0.072 | 0.055 | 0.527 |
| 0.10 | 0.119 | 0.090 | 0.548 |
| 0.20 | 0.214 | 0.158 | 0.590 |
| 0.30 | 0.308 | 0.226 | 0.633 |

## Reading (2026-11-12)

Made after the independent code review pointed out that the result files said "the features
hold no signal" when only the models had been scored. The features were all looked at here
after the fact, so the best of 15 flatters itself; read the pattern, not the top row.

1. **There is a weak signal in the features, and it is the trend effect.** On the six assets
   every trend feature ranks next month slightly better than chance on its own (AUC 0.52 to
   0.54, one and a half to three standard errors above 0.50), and the volatility features
   rank it slightly backwards (calm assets go up more often). That is about what a planted
   correlation of 0.03 to 0.10 scores on its own (0.52 to 0.55, second table).
2. **The fitted models scored below the features they were given:** 0.48 to 0.51 for every
   model of the six cards. Fitting 15 overlapping features on a few thousand overlapping rows
   cost more than it found. The control shows the same loss on a signal known to be there:
   the planted "0.10" feature scores 0.548 alone and 0.524 once a model has combined it with
   the other fifteen; "0.20" scores 0.590 alone and 0.56 to 0.57 through a model.
3. **The signal is not general.** On the other ETFs no feature is distinguishable from 0.50.
   On the indexes the trend features score 0.51 to 0.53. On the other coins (three years, 870
   rows) the trend features rank backwards. `dd_1y`, the best on the six, is not the best
   anywhere else, so its lead is the luck of picking among 15.

What it changes: the wording, not the verdicts. The right sentence is not "the features hold
no signal" but "the features hold the weak trend signal that `tsmom12` already uses with no
fitting, and no fitted model got more out of them than that; most got less". Run 1's
`ensemble-tsmom` (several trend horizons, no fitting, +0.05 over `tsmom12`, not significant)
is the honest size of what combining these features is worth.
