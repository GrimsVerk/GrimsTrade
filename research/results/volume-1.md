# Volume 1: weekly IC screen of own trading volume (six assets, to 2025-11-09)

Script `lib/volume1_ic.py`, card `research/volume-1.md`. IC = Pearson correlation
with the coming week's risk-adjusted return (`rl3_plant.week_z`). Chance = 95th
percentile of |IC| with the feature circularly shifted (500 shifts of >= 52
weeks, the same shifts for all six). **Family chance level (maxT over the six):
0.048**; a candidate is above chance only above that. WF = walk-forward IC
(OLS refitted every two years, a year's gap); `per` = a slope per asset, `pool` = one
slope. Gain = WF IC of trend inputs + feature minus trend inputs alone. Overlap =
largest |corr| with the 7 trend inputs.

| Candidate | From | Weeks | Cells | IC | rank IC | Chance | Family | WF per | WF pool | WF trend | Gain | Overlap | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `vol_chg4` | 2000-01-07 | 1348 | 5861 | +0.011 | +0.020 | 0.036 | 0.048 | -0.020 | -0.010 | +0.024 | -0.022 | 0.13 | no |
| `vol_chg13` | 2000-01-07 | 1348 | 5843 | -0.009 | -0.007 | 0.034 | 0.048 | +0.002 | -0.006 | +0.026 | -0.006 | 0.08 | no |
| `vol_z52` | 2000-01-07 | 1348 | 5842 | +0.012 | +0.022 | 0.037 | 0.048 | +0.001 | +0.001 | +0.026 | -0.007 | 0.14 | no |
| `vw_trend13` | 2000-01-07 | 1348 | 5856 | +0.003 | -0.013 | 0.038 | 0.048 | +0.012 | +0.005 | +0.024 | +0.002 | 0.82 | no |
| `updown13` | 2000-01-07 | 1348 | 5856 | -0.003 | -0.038 | 0.037 | 0.048 | -0.018 | +0.001 | +0.024 | -0.017 | 0.38 | no |
| `pv_div13` | 2000-01-07 | 1348 | 5843 | -0.021 | -0.020 | 0.040 | 0.048 | +0.008 | +0.017 | +0.026 | +0.001 | 0.19 | no |

## IC per asset (in sample; shown, not judged)

| Candidate | BTC | ETH | SPY | QQQ | GLD | TLT |
|---|---:|---:|---:|---:|---:|---:|
| `vol_chg4` | -0.001 | +0.043 | +0.028 | +0.008 | +0.033 | -0.031 |
| `vol_chg13` | +0.010 | +0.001 | -0.004 | -0.026 | -0.022 | +0.006 |
| `vol_z52` | +0.045 | +0.078 | +0.014 | -0.017 | +0.044 | -0.025 |
| `vw_trend13` | +0.071 | +0.056 | -0.036 | -0.032 | -0.013 | +0.009 |
| `updown13` | +0.043 | +0.048 | -0.041 | -0.035 | -0.015 | +0.008 |
| `pv_div13` | -0.019 | -0.032 | -0.032 | -0.014 | -0.028 | -0.029 |
