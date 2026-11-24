# cost-band: results (card `cards/cost-band.md`)

## Primary test: the six, 1994-2025

| Rule | Sharpe | dSharpe | Paired SE | z | p (one-sided) | Max DD | Turnover/yr | Coin drift fills/yr | Their cost/yr | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `tsmom12` (b = 0.01) | 1.045 | - | - | - | - | 37.4% | 2.81 | 59.4 | 0.279% | - |
| `band05` | 1.093 | +0.0487 | 0.0176 | **+2.76** | 0.001 | 32.5% | 2.06 | 6.2 | 0.158% | TE 1.48%, corr 0.9962; eras: 1994-99 +0.000 2000-09 -0.004 2010-16 +0.079 2017-21 +0.133 2022-25 +0.007 |
| `band05/bills` (above bills) | 0.982 | +0.0511 | 0.0168 | **+3.04** | 0.001 | - | - | - | - | - |
| `band02` | 1.058 | +0.0136 | 0.0058 | **+2.35** | 0.007 | 36.1% | 2.44 | 22.7 | 0.210% | TE 0.56%, corr 0.9995; eras: 1994-99 +0.000 2000-09 -0.000 2010-16 +0.025 2017-21 +0.036 2022-25 -0.002 |
| `band02/bills` (above bills) | 0.943 | +0.0123 | 0.0058 | **+2.13** | 0.013 | - | - | - | - | - |

## Out of universe: 6 other coins

| Rule | Sharpe | dSharpe | Paired SE | z | p (one-sided) | Max DD | Turnover/yr | Coin drift fills/yr | Their cost/yr | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `tsmom12` (b = 0.01) | 0.520 | - | - | - | - | 92.6% | 4.77 | 137.7 | 1.146% | - |
| `band05` | 0.559 | +0.0392 | 0.0159 | **+2.47** | 0.003 | 91.7% | 3.27 | 12.2 | 0.466% | TE 4.05%, corr 0.9987; eras: 2017-21 +0.035 2022-25 +0.060 |
| `band02` | 0.527 | +0.0068 | 0.0063 | **+1.08** | 0.141 | 92.5% | 4.09 | 55.1 | 0.826% | TE 1.36%, corr 0.9998; eras: 2017-21 +0.000 2022-25 +0.027 |

## Pass bar (card)

- `band05`: z +2.76 (cash 0) < 4.69; z +3.04 (above bills) < 4.69; coin dSharpe +0.0392 (> 0); max DD 32.5% vs 37.4% (ok). **FAIL**
- `band02`: z +2.35 (cash 0) < 4.69; z +2.13 (above bills) < 4.69; coin dSharpe +0.0068 (> 0); max DD 36.1% vs 37.4% (ok). **FAIL**
