# US drought and TLT over the next quarter (parked-gates-1, W32 `drought-inflation`)

Rule: `research/cards/parked-gates-1.md` (pushed before this ran). Script
`research/lib/parkedgates1.py`. Dose D(m) = -PDSI(m), contiguous US (NOAA nClimDiv,
2026-11-05 vintage). y = log return of TLT from the last bar of month m+1 to the last
bar of month m+4. Newey-West t, 3 lags, one row a dose month.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Dose months 2002-07..2025-06, b (t), 276 rows | -0.784% per PDSI unit (-3.71) | < 0, t <= -2 | True |
| Rank of true t among 41 calendars (1 = lowest) | 1 | <= 2 | True |

**Gate: PASS (kill-only design: not dead yet).** Empirical one-sided p = 1/41 = 0.024.

## Placebo null (dose calendar moved k months, both ways)

40 placebo t: standard deviation 0.94, share with |t| >= 2 0%; quantiles 5% -1.37, 50% +0.08, 95% +1.71; smallest -1.76, largest +1.95.

| k (months; > 0 an earlier dose) | t |
|---:|---:|
| +13 | -0.51 |
| -13 | +0.18 |
| +17 | -0.40 |
| -17 | +0.26 |
| +21 | +0.86 |
| -21 | -0.41 |
| +25 | +1.37 |
| -25 | -1.27 |
| +29 | +1.39 |
| -29 | -0.44 |
| +33 | +1.47 |
| -33 | +0.00 |
| +37 | +1.95 |
| -37 | -0.78 |
| +41 | +0.54 |
| -41 | -1.36 |
| +45 | -0.63 |
| -45 | -0.76 |
| +49 | -0.07 |
| -49 | +0.38 |
| +53 | +0.45 |
| -53 | -0.02 |
| +57 | +0.29 |
| -57 | -0.33 |
| +61 | +0.06 |
| -61 | +0.10 |
| +65 | -1.76 |
| -65 | -0.19 |
| +69 | +0.36 |
| -69 | +0.06 |
| +73 | +1.70 |
| -73 | -0.39 |
| +77 | +0.75 |
| -77 | +1.25 |
| +81 | +0.74 |
| -81 | +1.92 |
| +85 | +1.44 |
| -85 | -0.35 |
| +89 | +1.32 |
| -89 | -1.46 |

## Shown (not gating)

| Cut | b, % per unit (t) | Rows |
|---|---:|---:|
| GLD instead of TLT (predicted > 0) | -0.390 (-1.32) | 249 |
| DBC instead of TLT (predicted > 0) | +0.688 (+1.72) | 234 |
| IEF instead of TLT | -0.325 (-3.02) | 276 |
| SPY instead of TLT | +0.220 (+0.96) | 276 |
| 1-month horizon (month m+2 only) | -0.268 (-2.98) | 276 |
| 6-month horizon (m+2..m+7, NW 6 lags) | -1.525 (-4.84) | 273 |
| Growing-season dose months only (May-Sep) | -0.462 (-1.35) | 115 |
| 3-month change PDSI(m-3) - PDSI(m) as dose | -0.155 (-0.60) | 276 |
| Reaction: TLT over month m+1 (release month) | -0.208 (-2.15) | 276 |

Dose sd over the gate months: 2.40 PDSI units.
