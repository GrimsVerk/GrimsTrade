# Bank failures and XLF over the next 4 weeks (wide-13, W26 `failure-premium`)

Rule: `research/wide-13.md` step 3 (pushed before this ran). Script
`research/lib/wide13.py`. Dose x = ln(1 + total assets, millions of USD, of FDIC
failures and assistance transactions dated Saturday..Friday F); 0 without one.
y = log return of XLF from the close of the first bar >= F + 3 to the first bar
>= F + 31.
Controls: XLF's past 4/13/26/52-week returns. Newey-West t, 4 lags (one row a week).

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Fridays 2000-01-07..2025-10-03, b (t), 1344 rows | -0.059% per unit of x (-0.48) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 21 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 21/41 = 0.512. z against the placebo scale: (t - median) / sd = +0.14.

## Placebo null (dose calendar moved k weeks)

40 placebo t: standard deviation 1.63, share with |t| >= 2 25%; quantiles 5% -3.26, 50% -0.71, 95% +1.21; smallest -4.37, largest +1.56.

| k (weeks) | t |
|---:|---:|
| +27 | +1.20 |
| -27 | -1.67 |
| +31 | +1.41 |
| -31 | -1.94 |
| +35 | +1.56 |
| -35 | -1.26 |
| +39 | -0.06 |
| -39 | -2.72 |
| +43 | +0.99 |
| -43 | -2.22 |
| +47 | +0.88 |
| -47 | -1.28 |
| +51 | +0.47 |
| -51 | -2.85 |
| +55 | +0.41 |
| -55 | -1.86 |
| +59 | +0.60 |
| -59 | -2.60 |
| +63 | +0.16 |
| -63 | -3.23 |
| +67 | +0.63 |
| -67 | -1.87 |
| +71 | +0.35 |
| -71 | -3.79 |
| +75 | +1.07 |
| -75 | -1.79 |
| +79 | -0.18 |
| -79 | -3.07 |
| +83 | +0.80 |
| -83 | -2.21 |
| +87 | +0.73 |
| -87 | -1.46 |
| +91 | +0.70 |
| -91 | -4.37 |
| +95 | +0.41 |
| -95 | -1.80 |
| +99 | +0.35 |
| -99 | -1.25 |
| +103 | -0.05 |
| -103 | -2.74 |

## Shown (not gating)

| Cut | b, % per unit (t) | Rows |
|---|---:|---:|
| Without the controls | -0.061 (-0.45) | 1344 |
| Failure-week dummy instead of x | -0.201 (-0.30) | 1344 |
| Year 2023 dropped | -0.073 (-0.57) | 1292 |
| SPY instead of XLF | -0.023 (-0.25) | 1344 |
| TLT instead (idea 3, F1 fails) | +0.122 (+1.72) | 1158 |
| IEF instead (idea 3, F1 fails) | +0.056 (+1.68) | 1158 |
| Monday reaction (last close <= F to first close >= F + 3, 1 lag) | -0.071 (-1.59) | 1344 |
| 1-week horizon (exit >= F + 10, 1 lag) | +0.037 (+0.61) | 1344 |

F2 feedback check: x on XLF's own past return alone (NW 4 lags; negative = failures
follow falls):

| Past return | Slope, x per unit of log return (t) | Rows |
|---|---:|---:|
| 4 weeks | -2.62 (-1.15) | 1344 |
| 13 weeks | -2.13 (-1.46) | 1344 |
| 26 weeks | -1.64 (-1.48) | 1344 |
| 52 weeks | -2.37 (-3.87) | 1344 |
