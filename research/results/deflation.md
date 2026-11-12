# How much of the best result could be luck?

Variants that could have been selected, on the six assets: 17. Typical standard error of a Sharpe difference to equal weight over the train period: 0.10.

If none of the 17 had any edge at all, the best of them would still be expected to beat equal weight by about **+0.19** Sharpe (Bailey & Lopez de Prado's expected maximum). The best one actually seen: **+0.22** (`ensemble-tsmom/e4`).

Sharpe difference to equal weight, every selectable variant, best first:

| Variant | dSharpe vs equal weight |
|---|---:|
| ensemble-tsmom/e4 | +0.22 |
| kelly-shrunk/k0.1 | +0.22 |
| drawdown-control/d1.0 | +0.20 |
| drawdown-control/d1.5 | +0.15 |
| trend-vol/tv40 | +0.15 |
| vol-target/t25 | +0.06 |
| hmm-regime/hard | +0.01 |
| hmm-regime/soft | +0.00 |
| vol-target/t40 | -0.01 |
| hawkes-clustering/down2 | -0.01 |
| kelly-shrunk/k0.2 | -0.02 |
| absorption-ratio/six | -0.03 |
| universal-portfolio/up | -0.04 |
| kelly-shrunk/k0.4 | -0.04 |
| fracdiff-momentum/d0.3 | -0.11 |
| fracdiff-momentum/d0.5 | -0.16 |
| fracdiff-momentum/d0.4 | -0.18 |
