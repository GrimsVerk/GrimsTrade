# Micro 1: weekly IC screen of minute-bar features (six assets, 2016 to 2025-11-09)

Script `lib/micro1_ic.py`, card `research/micro-1.md`. IC = Pearson correlation
with the coming week's risk-adjusted return (`rl3_plant.week_z`). Chance = 95th
percentile of |IC| with the feature circularly shifted (500 shifts of >= 52
weeks inside the 2016-2025 window, the same shifts for all six). **Family chance
level (maxT over the six): 0.064**; a candidate is above chance only above
that. WF = walk-forward IC (OLS refitted every two years, a year's gap; `Blocks` =
test blocks that had >= 104 training weeks); `per` = a slope per asset, `pool` = one
slope. Gain = WF IC of trend inputs + feature minus trend inputs alone. Overlap =
largest |corr| with the 7 trend inputs.

| Candidate | From | Weeks | Cells | IC | rank IC | Chance | Family | Blocks | WF per | WF pool | WF trend | Gain | Overlap | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `rv_chg` | 2016-01-08 | 513 | 2954 | -0.004 | +0.019 | 0.048 | 0.064 | 3 | -0.053 | -0.023 | +0.003 | -0.036 | 0.11 | no |
| `rv_z52` | 2016-01-29 | 510 | 2895 | -0.000 | +0.020 | 0.048 | 0.064 | 3 | -0.002 | -0.009 | +0.007 | -0.009 | 0.11 | no |
| `jump4` | 2016-01-08 | 513 | 2990 | +0.002 | -0.009 | 0.052 | 0.064 | 3 | -0.005 | -0.010 | +0.001 | -0.010 | 0.15 | no |
| `sjump4` | 2016-01-08 | 513 | 2990 | -0.018 | -0.027 | 0.043 | 0.064 | 3 | -0.001 | -0.010 | +0.001 | -0.004 | 0.18 | no |
| `overnight13` | 2016-01-08 | 513 | 2954 | +0.030 | +0.039 | 0.049 | 0.064 | 3 | -0.006 | +0.007 | +0.003 | -0.009 | 0.75 | no |
| `intraday13` | 2016-01-08 | 513 | 2954 | +0.012 | +0.015 | 0.057 | 0.064 | 3 | +0.048 | +0.021 | +0.003 | +0.021 | 0.62 | no |

## IC per asset (in sample; shown, not judged)

| Candidate | BTC | ETH | SPY | QQQ | GLD | TLT |
|---|---:|---:|---:|---:|---:|---:|
| `rv_chg` | +0.004 | +0.025 | -0.005 | -0.006 | -0.009 | -0.029 |
| `rv_z52` | +0.044 | +0.047 | -0.029 | -0.020 | +0.016 | -0.045 |
| `jump4` | -0.017 | +0.017 | +0.032 | +0.040 | -0.070 | +0.014 |
| `sjump4` | +0.008 | +0.054 | -0.032 | -0.012 | -0.016 | -0.093 |
| `overnight13` | +0.067 | +0.036 | +0.008 | -0.005 | -0.034 | +0.020 |
| `intraday13` | +0.092 | +0.065 | -0.059 | -0.057 | +0.000 | +0.032 |
