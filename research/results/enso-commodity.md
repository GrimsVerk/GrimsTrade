# ENSO and commodities: event-study gate (wide-9, W19)

Rule: `research/wide-9.md` step 1 (pushed before this ran). Script
`research/lib/wide9_enso.py`. ONI: NOAA CPC (public domain). y = six-month log return
after each month end; x = ONI of the season ending the month before. Slopes in points
of six-month return per degree of ONI; Newey-West t, 6 lags.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| DBC 2014-01..2025-04 b (t), 136 months | -2.47 (-0.92) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 32 | <= 2 | False |
| Mean y, x >= 1.0 (23) vs 0.5 <= x < 1.0 (24) | -0.43 vs -4.61 | strong > weak | True |
| DBC 2006-02..2013-12 b (t) | +1.83 (+0.44) | > 0 | True |

**Gate: fail.** Empirical one-sided p = 32/41 = 0.780.

## Placebo null (ONI moved k = 2..41 years earlier), DBC 2014-2025

40 placebo t: standard deviation 1.74, share with |t| >= 2 20%; quantiles 5% -2.56, 50% +0.30, 95% +2.35; largest +2.84.

| k (years) | t |
|---:|---:|
| 2 | +1.87 |
| 3 | +0.83 |
| 4 | -0.48 |
| 5 | +0.99 |
| 6 | +2.80 |
| 7 | +0.38 |
| 8 | -0.05 |
| 9 | +0.21 |
| 10 | -2.55 |
| 11 | +0.24 |
| 12 | -0.44 |
| 13 | -1.30 |
| 14 | +0.67 |
| 15 | +1.81 |
| 16 | +0.18 |
| 17 | -2.50 |
| 18 | +1.86 |
| 19 | +1.16 |
| 20 | -0.76 |
| 21 | -1.68 |
| 22 | -2.64 |
| 23 | +0.36 |
| 24 | +0.94 |
| 25 | -0.47 |
| 26 | +1.17 |
| 27 | -0.70 |
| 28 | -0.62 |
| 29 | +1.55 |
| 30 | +2.84 |
| 31 | -0.51 |
| 32 | -5.93 |
| 33 | +0.85 |
| 34 | +2.03 |
| 35 | -0.99 |
| 36 | -1.67 |
| 37 | -1.13 |
| 38 | +2.33 |
| 39 | +1.83 |
| 40 | +0.90 |
| 41 | +1.74 |

## Shown

| Series, sample | b (t) |
|---|---:|
| GLD 2014-2025, 6 months | +3.86 (+2.61) |
| SLV 2014-2025, 6 months | +6.68 (+3.25) |
| DBC 2014-2025, 3 months | -1.95 (-1.15) |

| ONI bin (DBC 2014-2025) | Mean six-month y | Months |
|---|---:|---:|
| x <= -1.0 | +21.87 | 3 |
| -1.0 < x <= -0.5 | +2.77 | 28 |
| -0.5 < x < 0.5 | -0.68 | 58 |
| 0.5 <= x < 1.0 | -4.61 | 24 |
| x >= 1.0 | -0.43 | 23 |
