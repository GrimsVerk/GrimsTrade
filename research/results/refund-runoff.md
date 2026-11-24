# Tax-refund runoff and retail-heavy assets over the next 4 weeks (wide-15, W28
`refund-runoff`)

Rule: `research/wide-15.md` step 4 (pushed before this ran). Script
`research/lib/wide15.py`. Dose u = Nash-cascade runoff (gamma 2, mean 2 weeks) of the
weekly individual-refund surprise d (Daily Treasury Statement, same-ISO-week median of
three earlier years as baseline, % of last year's refunds).
y = log return from the close of the first bar >= F + 5 to the first bar >= F + 33;
QQQ, IWM, BTC, ETH pooled with asset intercepts, Driscoll-Kraay t, 4 lags.
Placebo k > 0 uses an earlier dose, k < 0 a later one (allowed: refunds do not answer
prices).

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Fridays 2008-01-04..2025-10-03, b (t), 2999 rows | +0.281% per unit of u (+1.44) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 7 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 7/41 = 0.171. (t - placebo median) / placebo sd = +1.10 (descriptive only).

## Placebo null (dose calendar moved k weeks: placebo dose = dose at F - 7k days)

40 placebo t: standard deviation 1.92, share with |t| >= 2 32%; quantiles 5% -3.51, 50% -0.67, 95% +2.80; smallest -4.61, largest +3.47.

| k (weeks) | t |
|---:|---:|
| +27 | +3.47 |
| -27 | -0.67 |
| +31 | +1.73 |
| -31 | +0.06 |
| +35 | +0.69 |
| -35 | -0.59 |
| +39 | +0.48 |
| -39 | -2.82 |
| +43 | -0.91 |
| -43 | -2.78 |
| +47 | +0.26 |
| -47 | +0.63 |
| +51 | -0.82 |
| -51 | +2.76 |
| +55 | -0.67 |
| -55 | +1.79 |
| +59 | -0.51 |
| -59 | +3.45 |
| +63 | +1.46 |
| -63 | +0.69 |
| +67 | -0.21 |
| -67 | +1.00 |
| +71 | -0.94 |
| -71 | +0.84 |
| +75 | +0.17 |
| -75 | -1.41 |
| +79 | -1.21 |
| -79 | -2.44 |
| +83 | -2.21 |
| -83 | -2.17 |
| +87 | -4.61 |
| -87 | -3.50 |
| +91 | +0.39 |
| -91 | -3.72 |
| +95 | -0.82 |
| -95 | -1.11 |
| +99 | -1.49 |
| -99 | -3.50 |
| +103 | -3.03 |
| -103 | -1.87 |

## Shown (not gating)

| Cut | b, % per unit (t) | Rows |
|---|---:|---:|
| SPY alone | +0.182 (+1.58) | 903 |
| QQQ and IWM | +0.309 (+2.67) | 1806 |
| BTC and ETH | +0.247 (+0.72) | 1193 |
| Raw weekly surprise d instead of u | +0.208 (+1.25) | 3062 |
| Seasons from 2017 (PATH Act hold) | +0.403 (+2.05) | 1796 |
| With past 4/13/26/52-week returns | +0.318 (+1.64) | 2886 |
| 1-week horizon (exit >= F + 12, 1 lag) | +0.051 (+0.46) | 2993 |

F2 feedback check: u on each asset's own past return alone (pooled, DK 4 lags):

| Past return | Slope, u per unit of log return (t) | Rows |
|---|---:|---:|
| 4 weeks | +0.763 (+1.08) | 2982 |
| 13 weeks | -0.267 (-1.20) | 2964 |
| 26 weeks | -0.087 (-0.74) | 2938 |
| 52 weeks | -0.059 (-0.72) | 2886 |
