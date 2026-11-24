# Geopolitical acts and safe havens over the next 4 weeks (wide-13, W25 `act-haven`)

Rule: `research/wide-13.md` step 2 (pushed before this ran). Script
`research/lib/wide13.py`. Dose: z of ln(1 + weekly mean of the Caldara-Iacoviello daily
acts sub-index), week ending Monday M, against the previous 156 weeks. y = log return
from the close of the first bar >= M + 9 (the index's available-on date) to the first bar
>= M + 37. GLD and TLT pooled with asset intercepts, no controls. Driscoll-Kraay t
(scores summed by Monday, Newey-West 4 lags). Values are today's revised index.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Mondays 2005-01-03..2025-10-06, b (t), 2166 rows | -0.137% per unit of z (-1.02) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 21 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 21/41 = 0.512. z against the placebo scale: (t - median) / sd = -0.05.

## Placebo null (dose calendar moved k weeks)

40 placebo t: standard deviation 1.11, share with |t| >= 2 12%; quantiles 5% -2.37, 50% -0.96, 95% +0.99; smallest -2.74, largest +1.68.

| k (weeks) | t |
|---:|---:|
| +27 | -0.34 |
| -27 | -1.80 |
| +31 | -1.42 |
| -31 | -1.54 |
| +35 | -0.71 |
| -35 | -1.61 |
| +39 | -1.86 |
| -39 | -1.37 |
| +43 | -2.36 |
| -43 | -1.59 |
| +47 | -1.41 |
| -47 | -0.24 |
| +51 | -0.12 |
| -51 | +1.68 |
| +55 | -0.75 |
| -55 | +1.10 |
| +59 | -0.17 |
| -59 | -1.21 |
| +63 | +0.51 |
| -63 | -1.66 |
| +67 | +0.67 |
| -67 | -2.28 |
| +71 | +0.17 |
| -71 | -2.14 |
| +75 | +0.90 |
| -75 | -1.40 |
| +79 | +0.98 |
| -79 | -2.74 |
| +83 | +0.11 |
| -83 | -1.42 |
| +87 | +0.44 |
| -87 | -2.58 |
| +91 | -1.72 |
| -91 | -1.59 |
| +95 | -0.82 |
| -95 | -1.11 |
| +99 | +0.38 |
| -99 | -0.54 |
| +103 | -0.50 |
| -103 | -0.25 |

## Shown (not gating)

| Cut | b, % per unit (t) | Rows |
|---|---:|---:|
| Threats sub-index z instead | -0.229 (-1.69) | 2166 |
| Total index GPRD z instead | -0.225 (-1.69) | 2166 |
| GLD alone | -0.118 (-0.70) | 1083 |
| TLT alone | -0.156 (-0.95) | 1083 |
| SPY alone (D3's neighbour) | -0.115 (-0.64) | 1083 |
| Post-paper years 2020-01-06..2025-10-06 | -0.163 (-0.55) | 600 |
| With past 4/13/26/52-week returns | -0.135 (-1.00) | 2120 |
| 1-week horizon (exit >= M + 16, 1 lag) | +0.001 (+0.01) | 2168 |

F2 feedback check: acts z on GLD/TLT's own past return alone (pooled, DK 4 lags):

| Past return | Slope, z per unit of log return (t) | Rows |
|---|---:|---:|
| 4 weeks | -0.01 (-0.01) | 2168 |
| 13 weeks | -1.03 (-1.66) | 2161 |
| 26 weeks | -1.32 (-2.96) | 2148 |
| 52 weeks | -0.94 (-2.81) | 2122 |
