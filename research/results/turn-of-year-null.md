# Turn-of-year loser rebound: placebo null and power (wide-8, step 1)

Rule: `research/wide-8.md` step 1 (pushed before this ran). Script
`research/lib/wide8_turn.py`. Train bars only; no December anchor is computed.

Eligible placebo windows: 153 (anchors January-November, 21 years).

| Null quantile of t | 2% | 5% | 50% | 95% | 98% |
|---|---:|---:|---:|---:|---:|
| t | -4.26 | -3.34 | -0.06 | +3.33 | +4.55 |

- Standard deviation of the null t: 2.18 (N(0, 1) would give 1).
- Share of placebo windows with |t| >= 2: 35% (N(0, 1) would give 5%).
- t needed for a pass (p <= 0.02): 4.87.
- Power (share of placebo windows passing once b* L is added): 8% at b* = 0.089, 5% at b* = 0.0445.

## Null t by anchor month (mean, sd, count)

| Month | Mean t | Sd | Windows |
|---:|---:|---:|---:|
| 1 | +0.31 | 1.87 | 13 |
| 2 | -0.25 | 1.81 | 13 |
| 3 | +0.58 | 3.10 | 13 |
| 4 | -0.87 | 1.90 | 15 |
| 5 | +0.39 | 1.71 | 15 |
| 6 | -1.93 | 2.43 | 14 |
| 7 | +0.89 | 1.91 | 16 |
| 8 | -0.19 | 1.99 | 15 |
| 9 | -0.22 | 1.56 | 13 |
| 10 | -0.94 | 2.14 | 12 |
| 11 | +0.72 | 2.27 | 14 |
