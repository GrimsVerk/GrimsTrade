# Congress workload and SPY over the next 4 weeks (wide-15, W27 `congress-workload`)

Rule: `research/wide-15.md` step 3 (pushed before this ran). Script
`research/lib/wide15.py`. Dose x = 2 sqrt(n + 3/8), n = House + Senate roll calls dated
Saturday..Friday F (Voteview); in-session dummy s = 1 if n > 0 also in the fit.
y = log return of SPY from the close of the first bar >= F + 3 to the first bar
>= F + 31.
Controls: SPY's past 4/13/26/52-week returns. Newey-West t, 4 lags (one row a week).

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Fridays 1994-02-04..2025-10-03, b (t), 1653 rows | -0.009% per unit of x (-0.19) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 25 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 25/41 = 0.610. (t - placebo median) / placebo sd = -0.21 (descriptive only).

## Placebo null (dose calendar moved k weeks: placebo dose = dose at F - 7k days)

40 placebo t: standard deviation 1.08, share with |t| >= 2 5%; quantiles 5% -1.48, 50% +0.03, 95% +1.98; smallest -1.67, largest +2.68.

| k (weeks) | t |
|---:|---:|
| +27 | -0.57 |
| +29 | +0.36 |
| +31 | -0.58 |
| +33 | -1.28 |
| +35 | -0.80 |
| +37 | -0.05 |
| +39 | -0.98 |
| +41 | -0.95 |
| +43 | -0.26 |
| +45 | -1.47 |
| +47 | -0.40 |
| +49 | -0.01 |
| +51 | -0.09 |
| +53 | +0.18 |
| +55 | -0.33 |
| +57 | -1.38 |
| +59 | -1.65 |
| +61 | -1.67 |
| +63 | -0.78 |
| +65 | +0.84 |
| +67 | +0.42 |
| +69 | +0.72 |
| +71 | +1.04 |
| +73 | +1.47 |
| +75 | +1.62 |
| +77 | +0.95 |
| +79 | +1.22 |
| +81 | +2.68 |
| +83 | +0.61 |
| +85 | -0.96 |
| +87 | -0.16 |
| +89 | +0.08 |
| +91 | +1.00 |
| +93 | +2.27 |
| +95 | +1.96 |
| +97 | +0.56 |
| +99 | +0.82 |
| +101 | +0.71 |
| +103 | +0.21 |
| +105 | -0.65 |

## Shown (not gating)

| Cut | b, % per unit (t) | Rows |
|---|---:|---:|
| Without the controls | -0.012 (-0.24) | 1653 |
| QQQ instead of SPY | +0.059 (+0.74) | 1335 |
| IWM instead of SPY | -0.058 (-0.81) | 1272 |
| Close votes only (margin < 10%) | -0.033 (-0.44) | 1653 |
| House only | -0.062 (-0.87) | 1653 |
| Senate only | +0.092 (+1.21) | 1653 |
| Fridays 2011-01-07..2025-10-03 (after Pastor-Veronesi) | -0.071 (-1.07) | 770 |
| 1-week horizon (exit >= F + 10, 1 lag) | +0.013 (+0.55) | 1653 |
| Calendar cell: c, the in-session dummy, % per 4 weeks (gate fit) | +0.337 (+0.69) | 1653 |

F2 feedback check: x on SPY's own past return alone, session weeks only (NW 4 lags;
negative = more votes after falls):

| Past return | Slope, x per unit of log return (t) | Rows |
|---|---:|---:|
| 4 weeks | +0.45 (+0.17) | 1151 |
| 13 weeks | +1.65 (+0.91) | 1151 |
| 26 weeks | +1.08 (+1.01) | 1151 |
| 52 weeks | +0.13 (+0.16) | 1151 |
