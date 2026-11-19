# Inflation disagreement and next quarter's bond return: gate (wide-12, W24)

Rule: `research/wide-12.md` step 3 (pushed before this ran). Script
`research/lib/wide12_spf.py`. Dose: SPF interquartile range of 10-year CPI inflation
forecasts (`CPI10_D1`), z against the previous 40 surveys. y = log return from the first
bar >= the first day of the survey quarter's third month to the first bar three months
later. Pooled over TLT and IEF with asset intercepts. b = quarterly return per unit of z;
Driscoll-Kraay t (scores summed by quarter, Newey-West 1 lag).

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Surveys 2010Q1..2025Q2, b (t), 124 rows | -0.487% (-0.75) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 36 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 36/41 = 0.878. z against the placebo scale: (t - median) / sd = -1.27.

## Placebo null (the dose calendar moved k quarters)

40 placebo t: standard deviation 0.90, share with |t| >= 2 0%; quantiles 5% -1.39, 50% +0.40, 95% +1.45; smallest -1.85, largest +1.65.

| k (quarters) | t | rows |
|---:|---:|---:|
| +7 | +1.12 | 124 |
| -7 | +0.40 | 112 |
| +9 | +1.52 | 124 |
| -9 | +0.68 | 108 |
| +11 | +1.28 | 124 |
| -11 | +1.65 | 104 |
| +13 | +0.71 | 124 |
| -13 | +1.45 | 100 |
| +15 | +0.74 | 124 |
| -15 | -0.41 | 96 |
| +17 | +0.49 | 124 |
| -17 | +1.04 | 92 |
| +19 | +0.78 | 124 |
| -19 | -1.38 | 88 |
| +21 | +0.36 | 124 |
| -21 | -0.44 | 84 |
| +23 | +1.20 | 124 |
| -23 | -0.38 | 80 |
| +25 | +0.34 | 124 |
| -25 | -0.51 | 76 |
| +27 | +0.46 | 124 |
| -27 | +0.69 | 72 |
| +29 | +0.30 | 124 |
| -29 | -0.65 | 68 |
| +31 | +1.00 | 124 |
| -31 | -0.12 | 64 |
| +33 | +1.25 | 124 |
| -33 | +0.41 | 60 |
| +35 | -1.85 | 124 |
| -35 | -0.33 | 56 |
| +37 | -0.18 | 124 |
| -37 | -1.62 | 52 |
| +39 | +0.06 | 124 |
| -39 | -1.35 | 48 |
| +41 | -0.40 | 124 |
| -41 | +0.40 | 44 |
| +43 | -0.30 | 124 |
| -43 | +1.39 | 40 |
| +45 | -1.15 | 124 |
| -45 | +0.64 | 36 |

## Shown (not gating)

| Cut | b, % per unit (t) | Rows |
|---|---:|---:|
| With past 13/26/52-week returns as controls | -0.351 (-0.60) | 124 |
| Next-year dose CPI_D1(T+4) instead | -0.981 (-1.58) | 124 |
| TLT alone | -0.653 (-0.74) | 62 |
| IEF alone | -0.321 (-0.73) | 62 |
| SPY alone | -0.211 (-0.27) | 62 |
| Pre-gate years 1996Q4..2009Q4 | -0.642 (-1.25) | 60 |

Feedback check (F2): z(q) on the asset's own past return, pooled TLT and IEF:

| Past return | Slope, z per unit of log return (t) | Rows |
|---|---:|---:|
| 13 weeks | -2.63 (-1.07) | 124 |
| 52 weeks | -1.40 (-0.97) | 124 |
