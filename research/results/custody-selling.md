# Foreign official custody flows and the next 4 weeks of Treasuries: gate (wide-12, W23)

Rule: `research/wide-12.md` step 2 (pushed before this ran). Script
`research/lib/wide12_custody.py`. Holdings: Fed H.4.1, custody of marketable Treasuries
for foreign official accounts, Wednesday level (DDP series RESH4FG_N.WW, keyless).
f = 4-week log change; z = f against its previous 156 weeks. y = log return from the
close of the first bar >= W + 5 to the first bar >= W + 33 (W = Wednesday). Pooled over
TLT and IEF with asset intercepts and the asset's past 4-, 13-, 26- and 52-week returns
as controls. b = 4-week return per unit of z; Driscoll-Kraay t (scores summed by week,
Newey-West 4 lags).

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Wednesdays 2010-01-06..2025-10-01, b (t), 1644 rows | -0.154% (-1.20) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 34 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 34/41 = 0.829. z against the placebo scale: (t - median) / sd = -1.11.

## Placebo null (the dose calendar moved k weeks)

40 placebo t: standard deviation 1.19, share with |t| >= 2 10%; quantiles 5% -2.07, 50% +0.12, 95% +1.89; smallest -2.25, largest +2.46.

| k (weeks) | t |
|---:|---:|
| +27 | -0.83 |
| -27 | +0.25 |
| +31 | -2.06 |
| -31 | +0.86 |
| +35 | -0.95 |
| -35 | -1.79 |
| +39 | +1.19 |
| -39 | -0.37 |
| +43 | +1.09 |
| -43 | +1.07 |
| +47 | +1.98 |
| -47 | -0.45 |
| +51 | +0.44 |
| -51 | +0.32 |
| +55 | +0.08 |
| -55 | +1.01 |
| +59 | -1.47 |
| -59 | -2.18 |
| +63 | -1.96 |
| -63 | -0.41 |
| +67 | -0.96 |
| -67 | +0.55 |
| +71 | +0.08 |
| -71 | -1.62 |
| +75 | +0.29 |
| -75 | +0.17 |
| +79 | -0.70 |
| -79 | +1.89 |
| +83 | -0.43 |
| -83 | +0.68 |
| +87 | +0.80 |
| -87 | +0.64 |
| +91 | +0.75 |
| -91 | +0.17 |
| +95 | -0.07 |
| -95 | -0.58 |
| +99 | +2.46 |
| -99 | -2.25 |
| +103 | +1.82 |
| -103 | -0.59 |

## Shown (not gating)

| Cut | b, % per unit (t) | Rows |
|---|---:|---:|
| Without the controls | -0.167 (-1.35) | 1644 |
| 1-week horizon (exit >= W + 12, 1 lag) | -0.019 (-0.40) | 1644 |
| Raw 4-week flow f instead of z (same rows) | -1.885 (-0.15) | 1644 |
| TLT alone | -0.221 (-1.20) | 822 |
| IEF alone | -0.087 (-1.10) | 822 |
| SPY alone | -0.300 (-1.24) | 822 |
| GLD alone | -0.197 (-0.90) | 822 |
| Pre-gate years 2005-01-05..2009-12-30 | +0.475 (+0.83) | 46 |

Feedback check (F2): z(W) on the asset's own past return, pooled TLT and IEF:

| Past return | Slope, z per unit of log return (t) | Rows |
|---|---:|---:|
| 4 weeks | -5.91 (-3.19) | 1644 |
| 13 weeks | -1.90 (-1.44) | 1644 |
| 26 weeks | -1.08 (-1.25) | 1644 |
| 52 weeks | -0.57 (-0.94) | 1644 |

Face-value check: weekly log change of holdings on TLT's same-week log return: slope -0.0169 (t -1.79, 822 weeks). A market-value series would show a slope near the holdings' duration ratio to TLT (about +0.3).
