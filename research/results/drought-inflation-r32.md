# Drought and the 10-year yield, 1962-2002 (parked-gates-1, R32: replication of W32)

Rule: `research/cards/parked-gates-1b.md` (pushed after W32's result, before this ran).
Dose D(m) = -PDSI(m), contiguous US. y = DGS10 at the end of month m+4 minus DGS10 at
the end of month m+1 (percentage points). Newey-West t, 3 lags, one row a dose month.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Dose months 1962-01..2002-03, b (t), 483 rows | -0.32 bp per PDSI unit (-0.19) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 21 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 21/41 = 0.512.

## Placebo null (dose calendar moved k months, both ways)

40 placebo t: standard deviation 1.19, share with |t| >= 2 8%; quantiles 5% -1.96, 50% -0.21, 95% +1.59; smallest -2.35, largest +2.55.

| k (months; > 0 an earlier dose) | t |
|---:|---:|
| +13 | -0.12 |
| -13 | +0.41 |
| +17 | +0.05 |
| -17 | +1.56 |
| +21 | +1.21 |
| -21 | +0.61 |
| +25 | +1.58 |
| -25 | -0.28 |
| +29 | +2.55 |
| -29 | +0.35 |
| +33 | +1.72 |
| -33 | -1.48 |
| +37 | +0.82 |
| -37 | -2.10 |
| +41 | +0.39 |
| -41 | -0.98 |
| +45 | -1.43 |
| -45 | -2.35 |
| +49 | -1.63 |
| -49 | -1.53 |
| +53 | -0.82 |
| -53 | -0.14 |
| +57 | -1.13 |
| -57 | -0.62 |
| +61 | -1.50 |
| -61 | -0.58 |
| +65 | -1.18 |
| -65 | -1.95 |
| +69 | +0.04 |
| -69 | -1.90 |
| +73 | +0.47 |
| -73 | -1.37 |
| +77 | +0.15 |
| -77 | -1.54 |
| +81 | +0.74 |
| -81 | -0.58 |
| +85 | +0.25 |
| -85 | +0.16 |
| +89 | -0.93 |
| -89 | +1.00 |

## Shown (not gating)

| Cut | b (t) | Rows |
|---|---:|---:|
| Yield, dose months 2002-07..2025-06 (bp per unit) | +4.360 (+3.01) | 276 |
| Yield, dose months 1962-01..2025-06 (bp per unit) | +0.905 (+0.73) | 762 |
| Yield, growing season May-Sep 1962-2002 (bp) | +1.843 (+0.76) | 200 |
| Reaction: yield over month m+1, 1962-2002 (bp) | +0.105 (+0.18) | 483 |
| Food CPI log change m+1..m+4, 1962-2025 (% per unit) | -0.045 (-1.68) | 761 |
| Food CPI log change m+1..m+4, 1962-2002 (% per unit) | -0.063 (-1.82) | 483 |

## Post hoc on W32's gate sample (TLT, % per unit; descriptive, picked after W32)

| Dose months left out | b (t) | Rows |
|---|---:|---:|
| none (W32's gate) | -0.784 (-3.71) | 276 |
| 2002-07..2003-12 | -0.797 (-3.68) | 258 |
| 2006-01..2008-12 | -0.839 (-3.84) | 240 |
| 2011-01..2013-12 | -0.781 (-3.12) | 240 |
| 2020-01..2023-06 | -0.652 (-3.18) | 234 |
| 2021-08..2022-10 (outcome touches 2022) | -0.662 (-3.34) | 261 |
