# How much of the best result could be luck?

Variants that could have been selected, on the six assets: 49. Typical standard error of a Sharpe difference to equal weight over the train period: 0.11.

If none of the 49 had any edge at all, the best of them would still be expected to beat equal weight by about **+0.24** Sharpe (Bailey & Lopez de Prado's expected maximum). The best one actually seen: **+0.22** (`ensemble-tsmom/e4`).

Sharpe difference to equal weight, every selectable variant, best first:

| Variant | dSharpe vs equal weight |
|---|---:|
| ensemble-tsmom/e4 | +0.22 |
| kelly-shrunk/k0.1 | +0.22 |
| drawdown-control/d1.0 | +0.20 |
| drawdown-control/d1.5 | +0.15 |
| trend-vol/tv40 | +0.15 |
| trend-to-safe/safe | +0.14 |
| ml-filter/meta-logit | +0.06 |
| vol-target/t25 | +0.06 |
| crypto-slot-size/c10 | +0.05 |
| ml-pooled/logit-pool | +0.04 |
| crypto-slot-size/c05 | +0.02 |
| hmm-regime/hard | +0.01 |
| ml-linear/logit | +0.01 |
| hmm-regime/soft | +0.00 |
| ml-linear/logit-hard | -0.00 |
| vol-target/t40 | -0.01 |
| hawkes-clustering/down2 | -0.01 |
| ml-gbm/gbm-leaf20 | -0.02 |
| ml-filter/and-gbm | -0.02 |
| kelly-shrunk/k0.2 | -0.02 |
| absorption-ratio/six | -0.03 |
| universal-portfolio/up | -0.04 |
| ml-linear/ridge | -0.04 |
| kelly-shrunk/k0.4 | -0.04 |
| ml-sizing/logit-low | -0.06 |
| ml-sizing/ridge-prop | -0.07 |
| ml-gbm/gbm | -0.07 |
| ml-sizing/gbm-low | -0.08 |
| ml-gbm/gbm-cv | -0.09 |
| ml-gbm/gbm-reg | -0.10 |
| ml-gbm/gbm-d6 | -0.11 |
| ml-payoff/logit-pay | -0.11 |
| fracdiff-momentum/d0.3 | -0.11 |
| ml-gbm/gbm-n400 | -0.12 |
| ml-gbm/gbm-n25 | -0.13 |
| ml-sizing/gbm-prop | -0.13 |
| ml-sizing/logit-prop | -0.13 |
| ml-payoff/gbm-raw | -0.14 |
| ml-filter/meta-gbm | -0.15 |
| ml-gbm/gbm-d1 | -0.16 |
| ml-gbm/gbm-hard | -0.16 |
| fracdiff-momentum/d0.5 | -0.16 |
| fracdiff-momentum/d0.4 | -0.18 |
| ml-pooled/gbm-pool | -0.18 |
| ml-sizing/gbm-reg-prop | -0.20 |
| ml-pooled/gbm-pool-low | -0.20 |
| ml-payoff/gbm-pay | -0.20 |
| ml-payoff/tree-pay | -0.22 |
| crypto-slot-size/c00 | -0.29 |
