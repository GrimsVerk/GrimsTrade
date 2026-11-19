# RL 3: weekly IC of the real inputs (six assets, 2000-01-07 to 2025-11-09)

Script `lib/rl3_input_ic.py` (descriptive, no backtest). IC = correlation with the coming
week's risk-adjusted return, the target the planted input copies. Macro inputs repeat
across assets, so their real standard error is larger than 1/sqrt(cells).

## all eligible cells: 6002 cells (1/sqrt = 0.013)

| Input | IC |
|---|---:|
| `cpi_yoy` | -0.047 |
| `since_high` | -0.041 |
| `real_ff` | +0.040 |
| `breadth` | +0.033 |
| `z365` | +0.031 |
| `univ_mom_1m` | +0.028 |
| `sma_gap` | +0.028 |
| `dd_1y` | +0.027 |
| `up_12m` | +0.026 |
| `z182` | +0.024 |
| `z7` | -0.020 |
| `z91` | +0.020 |
| `dgs10` | -0.018 |
| `coin` | +0.017 |
| `unrate_rise` | +0.016 |
| `z30` | +0.016 |
| `vol_shock` | +0.012 |
| `dff_chg182` | +0.012 |
| `real_m2` | +0.009 |
| `curve` | +0.008 |
| `rank_12m` | +0.007 |
| `log_vol` | -0.005 |
| `vix` | -0.003 |
| `univ_vol_shock` | -0.003 |
| `baa20` | -0.002 |
| `dff30` | +0.001 |
| `halving` | +0.000 |

## cells `tsmom12` holds: 4341 cells (1/sqrt = 0.015)

| Input | IC |
|---|---:|
| `cpi_yoy` | -0.036 |
| `since_high` | -0.033 |
| `z7` | -0.028 |
| `coin` | +0.027 |
| `real_ff` | +0.023 |
| `z365` | +0.022 |
| `unrate_rise` | +0.019 |
| `vol_shock` | +0.018 |
| `breadth` | +0.017 |
| `dd_1y` | +0.016 |
| `curve` | +0.014 |
| `univ_mom_1m` | +0.013 |
| `sma_gap` | +0.012 |
| `log_vol` | +0.009 |
| `dgs10` | -0.009 |
| `z30` | +0.009 |
| `dff_chg182` | +0.008 |
| `z182` | +0.006 |
| `z91` | +0.006 |
| `real_m2` | +0.006 |
| `rank_12m` | +0.005 |
| `halving` | +0.004 |
| `dff30` | -0.002 |
| `univ_vol_shock` | +0.002 |
| `baa20` | +0.001 |
| `vix` | +0.001 |

## All 27 inputs together

- In-sample least squares (overfit upper bound): correlation +0.114; pure chance
  with this many inputs gives about 0.067.
- Walk-forward least squares (refitted every two years, a year's gap): IC -0.018.
