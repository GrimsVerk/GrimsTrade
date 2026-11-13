# RL 1: results (train period, out of sample 2000-01-07 to 2025-11-09)

Script `lib/rl_eval.py` (tables by `lib/rl_report.py`). Walk-forward: a model retrained
every two years on data before it trades. Every row is a replay through `gym.simulate`.
Ensemble = the average of the ten seeds' weights each Friday (the selectable strategy).
dSharpe and p against `tsmom12`: paired stationary bootstrap, one-sided. Baselines are
re-scored from 2000-01-07.

## Six assets

| Strategy | Sharpe | Since 2003 | dSharpe vs tsmom12 (p) | Since 2003 d (p) | Worst loss | Growth/yr | Turnover/yr | Seeds: median Sharpe [min..max] | Seeds ahead | Bars passed |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| `tsmom12` | 0.99 | 1.19 | | | 36.5% | +16.8% | 2.8 | | | |
| `sma200` | 0.99 | 1.20 | | | 39.5% | +15.6% | 4.4 | | | |
| `inverse-vol` | 0.73 | 1.32 | | | 61.1% | +10.2% | 0.8 | | | |
| `equal-weight` | 0.81 | 1.19 | | | 68.8% | +17.2% | 1.3 | | | |
| `ppo-lin` | 0.63 | 0.75 | -0.36 (1.00) | -0.44 (1.00) | 77.3% | +18.2% | 7.0 | 0.61 [0.52..0.69] | 0/10 | 6 |
| `ppo-mlp` | 0.66 | 0.80 | -0.33 (0.98) | -0.39 (0.99) | 79.6% | +20.2% | 6.9 | 0.64 [0.55..0.75] | 0/10 | 6 |
| `ppo-mlp-dd` | 0.57 | 0.76 | -0.42 (0.99) | -0.43 (0.98) | 60.4% | +10.5% | 7.1 | 0.50 [0.37..0.70] | 0/10 | 6 |
| `ppo-mlp-px` | 0.71 | 0.81 | -0.28 (0.96) | -0.38 (0.99) | 82.3% | +22.7% | 6.7 | 0.68 [0.64..0.78] | 0/10 | 6 |
| `es-lin` | 0.57 | 0.72 | -0.42 (1.00) | -0.47 (1.00) | 86.5% | +17.1% | 9.9 | 0.56 [0.51..0.64] | 0/10 | 6 |

Eras (Sharpe):

| Strategy | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|
| `tsmom12` | 0.19 | 1.55 | 1.50 | 0.88 |
| `sma200` | 0.14 | 1.58 | 1.53 | 0.75 |
| `inverse-vol` | 0.10 | 1.70 | 1.87 | 0.87 |
| `equal-weight` | 0.02 | 1.67 | 1.55 | 0.67 |
| `ppo-lin` | 0.00 | 0.56 | 1.28 | 0.44 |
| `ppo-mlp` | 0.13 | 0.35 | 1.43 | 0.55 |
| `ppo-mlp-dd` | -0.09 | 0.26 | 1.66 | 0.48 |
| `ppo-mlp-px` | 0.27 | 0.39 | 1.47 | 0.47 |
| `es-lin` | -0.04 | 0.39 | 1.31 | 0.41 |

## Out of universe (fold models unchanged, ensemble)

| Strategy | Other ETFs | Other coins | Four indexes |
|---|---:|---:|---:|
| `tsmom12` | 0.60 (from 2001-06-01) | 0.54 (from 2017-08-18) | 0.49 (from 2000-01-07) |
| `ppo-lin` | 0.51 (-0.09) | 0.60 (+0.07) | 0.37 (-0.12) |
| `ppo-mlp` | 0.49 (-0.11) | 0.64 (+0.11) | 0.31 (-0.19) |
| `ppo-mlp-dd` | 0.39 (-0.21) | 0.56 (+0.02) | 0.14 (-0.35) |
| `ppo-mlp-px` | 0.52 (-0.08) | 0.64 (+0.10) | 0.38 (-0.12) |
| `es-lin` | 0.41 (-0.19) | 0.61 (+0.08) | 0.26 (-0.23) |

## Overfitting: each fold model in sample against the two years it traded

Weekly Sharpe, fresh account, batched simulator (same rules as the gym). In = the
fold's own six-asset training window (1994 to the fold); out = its two traded years.

| Fold | tsmom12 in / out | `ppo-lin` in / out | `ppo-mlp` in / out | `ppo-mlp-dd` in / out | `ppo-mlp-px` in / out | `es-lin` in / out |
|---|---:|---:|---:|---:|---:|---:|
| 2000 | 1.40 / -0.57 | 1.43 / -0.89 | 1.68 / -0.71 | 2.30 / -0.82 | 1.59 / -0.75 | 1.43 / -1.02 |
| 2002 | 0.68 / 0.99 | 0.95 / 0.13 | 1.40 / -0.14 | 1.61 / 0.24 | 1.27 / 0.70 | 1.14 / -0.28 |
| 2004 | 0.66 / 1.04 | 0.89 / 1.29 | 1.26 / 2.04 | 1.84 / 1.41 | 1.19 / 1.93 | 1.10 / 1.65 |
| 2006 | 0.67 / 1.04 | 0.82 / 1.32 | 1.32 / 1.46 | 1.70 / 1.82 | 1.12 / 1.59 | 1.17 / 1.46 |
| 2008 | 0.71 / -0.04 | 0.86 / 0.03 | 1.36 / -0.05 | 1.90 / -0.38 | 1.14 / 0.11 | 1.22 / 0.03 |
| 2010 | 0.65 / 1.26 | 0.71 / 1.17 | 1.32 / 0.95 | 1.79 / 0.66 | 1.07 / 1.03 | 1.16 / 0.75 |
| 2012 | 0.69 / 2.90 | 0.68 / 3.22 | 1.19 / 0.74 | 1.76 / -0.12 | 1.04 / 0.98 | 1.02 / 1.14 |
| 2014 | 0.98 / -0.20 | 0.78 / -0.41 | 0.92 / -0.31 | 0.89 / -0.23 | 0.88 / -0.32 | 1.06 / -0.42 |
| 2016 | 0.91 / 2.72 | 0.69 / 2.22 | 0.86 / 2.50 | 0.80 / 2.45 | 0.84 / 2.52 | 0.80 / 2.45 |
| 2018 | 1.10 / -0.69 | 0.86 / -0.84 | 0.98 / -0.83 | 1.07 / -0.48 | 0.95 / -0.84 | 0.93 / -1.04 |
| 2020 | 0.93 / 1.59 | 0.71 / 1.45 | 0.85 / 1.63 | 0.99 / 1.62 | 0.81 / 1.74 | 0.73 / 1.32 |
| 2022 | 1.00 / 0.59 | 0.80 / -0.17 | 0.91 / 0.01 | 1.06 / -0.61 | 0.90 / -0.13 | 0.85 / -0.23 |
| 2024 | 0.96 / 1.29 | 0.75 / 0.97 | 0.83 / 0.91 | 1.02 / 1.10 | 0.80 / 0.87 | 0.82 / 0.72 |
| mean | 0.87 / 0.92 | 0.84 / 0.73 | 1.15 / 0.63 | 1.44 / 0.51 | 1.05 / 0.72 | 1.03 / 0.50 |

## What the ensembles do (six assets, out of sample)

Slot = weight as a multiple of an equal slot (1/number of eligible assets).

| Strategy | Avg cash | Avg coins | Slot when 12m trend up | Slot when down | Corr(risk held, VIX) | Avg weekly change |
|---|---:|---:|---:|---:|---:|---:|
| `tsmom12` | 30% | 10% | 1.00 | 0.00 | -0.37 | 1.8% |
| `ppo-lin` | 15% | 32% | 0.97 | 0.64 | -0.48 | 7.6% |
| `ppo-mlp` | 10% | 32% | 0.94 | 0.82 | -0.24 | 16.6% |
| `ppo-mlp-dd` | 54% | 13% | 0.48 | 0.46 | -0.12 | 10.4% |
| `ppo-mlp-px` | 11% | 34% | 0.97 | 0.79 | -0.28 | 18.1% |
| `es-lin` | 6% | 41% | 1.01 | 0.78 | -0.30 | 14.0% |

## Pass bar

- `ppo-lin`: fails (1 beats tsmom12 p<0.10: no; 2 ahead in >=3 of 4 eras: no; 3 worst loss <= tsmom12 + 5 pts: no; 4 not behind tsmom12 since 2003, ahead of sma200/inverse-vol/equal weight: no; 5 >= 7 of 10 seeds ahead of tsmom12: no; 6 out-of-universe sign in >= 2 of 3: yes)
- `ppo-mlp`: fails (1 beats tsmom12 p<0.10: no; 2 ahead in >=3 of 4 eras: no; 3 worst loss <= tsmom12 + 5 pts: no; 4 not behind tsmom12 since 2003, ahead of sma200/inverse-vol/equal weight: no; 5 >= 7 of 10 seeds ahead of tsmom12: no; 6 out-of-universe sign in >= 2 of 3: yes)
- `ppo-mlp-dd`: fails (1 beats tsmom12 p<0.10: no; 2 ahead in >=3 of 4 eras: no; 3 worst loss <= tsmom12 + 5 pts: no; 4 not behind tsmom12 since 2003, ahead of sma200/inverse-vol/equal weight: no; 5 >= 7 of 10 seeds ahead of tsmom12: no; 6 out-of-universe sign in >= 2 of 3: yes)
- `ppo-mlp-px`: fails (1 beats tsmom12 p<0.10: no; 2 ahead in >=3 of 4 eras: no; 3 worst loss <= tsmom12 + 5 pts: no; 4 not behind tsmom12 since 2003, ahead of sma200/inverse-vol/equal weight: no; 5 >= 7 of 10 seeds ahead of tsmom12: no; 6 out-of-universe sign in >= 2 of 3: yes)
- `es-lin`: fails (1 beats tsmom12 p<0.10: no; 2 ahead in >=3 of 4 eras: no; 3 worst loss <= tsmom12 + 5 pts: no; 4 not behind tsmom12 since 2003, ahead of sma200/inverse-vol/equal weight: no; 5 >= 7 of 10 seeds ahead of tsmom12: no; 6 out-of-universe sign in >= 2 of 3: yes)

## Verdict (2026-11-13)

All five agents dead: behind `tsmom12` by 0.28 to 0.42 Sharpe out of sample (p 0.96-1.00), behind
equal weight, worst losses 60-87%, 0 of 50 seeds ahead. They learned to hold coins and to
half-follow the trend flag, and they overfit their training windows (MLP 1.15 in sample, 0.63
out). Held-out year not used. Reading and next steps: `rl-1.md`.
