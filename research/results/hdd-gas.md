# HDD surprise and next-week natural gas: gate (weather-1)

Rule: `research/weather-1.md` (pushed before any return data was loaded). Script
`research/lib/weather1_hdd.py`. Dose: CPC CONUS utility-gas-weighted HDD, 7 days to
Friday, minus a rolling 20-year +-7-day normal. y: UNG log return, close of the first
session on/after Friday + 4 days to 5 sessions later. Slope in percentage points per
10 degree days, HC1 t. Winters 2007-08 .. 2024-25, train bars only.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Slope (t, n) | -0.036 (-0.29, 389) | > 0, t >= 2 | False |
| Rank of t among 41 (1 = highest) | 19 | <= 2 | False |
| Slope 2007-15 / 2016-24 winters (t, n) | +0.165 (+1.16, 193) / -0.248 (-1.14, 196) | both > 0 | False |

**Gate: fail.**

## Placebo null (40 winter derangements)

SD of placebo t 1.12; share |t| >= 2 10%; 5/50/95% -1.90 / -0.32 / +1.53; min -2.53, max +2.37.

Placebo t, in draw order: +1.49, -0.29, -2.00, -1.00, -0.40, -0.30, -0.70, +1.20, +1.12, -0.35, -0.82, -1.75, -0.07, +1.07, -1.59, -2.53, +1.14, -1.89, +2.37, +0.94, +0.35, -0.68, -0.67, -0.85, -1.35, -0.25, -0.33, -0.10, -0.20, -0.13, -0.80, +0.26, +2.15, -1.20, -0.33, +0.56, -1.21, +0.44, +1.11, -0.62

## Shown (carded, not gating)

| Cell | Slope per 10 DD (t, n) |
|---|---:|
| UNG dose week (same-week check) | +0.228 (+1.68, 389) |
| UNG next 10 sessions | -0.078 (-0.47, 389) |
| XLE next 5 sessions | +0.083 (+1.44, 389) |
| XLE dose week (same-week check) | +0.031 (+0.51, 389) |

UNG next-week mean y, coldest quintile of x -1.24%, warmest -0.77%.
x: mean -3.0 DD, SD 29.9 DD; y: mean -1.05%, SD 7.32%.
