# Hedging pressure and the next 4 weeks: event-study gate (wide-11, W22)

Rule: `research/wide-11.md` step 2 (pushed before this ran). Script
`research/lib/wide11_hp.py`. Positions: CFTC legacy COT, futures only (keyless).
HP = (commercial short - long) / (short + long); z = HP against its previous 156 weeks.
y = log return from the close of the first bar >= T + 7 to the first bar >= T + 35
(T = Tuesday position date). Pooled over GLD, TLT, SPY, QQQ with market intercepts and
the asset's past 4- and 52-week returns as controls. b = 4-week return per unit of z;
Driscoll-Kraay t (scores summed by report week, Newey-West 4 lags).

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Reports 2018-06-05..2025-10-06, b (t), 1484 rows | +0.075% (+0.49) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 14 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 14/41 = 0.341. z against the placebo scale: (t - median) / sd = +0.49.

## Placebo null (each market's dose calendar moved k weeks)

40 placebo t: standard deviation 1.13, share with |t| >= 2 8%; quantiles 5% -1.35, 50% -0.06, 95% +2.22; smallest -1.66, largest +3.41.

| k (weeks) | t |
|---:|---:|
| +27 | -0.49 |
| -27 | +2.52 |
| +31 | -0.61 |
| -31 | +3.41 |
| +35 | -0.39 |
| -35 | +1.79 |
| +39 | -0.61 |
| -39 | +1.63 |
| +43 | +0.22 |
| -43 | +1.38 |
| +47 | +0.54 |
| -47 | +1.17 |
| +51 | +0.65 |
| -51 | +0.83 |
| +55 | -0.05 |
| -55 | +2.20 |
| +59 | +0.18 |
| -59 | +1.39 |
| +63 | -0.16 |
| -63 | +1.04 |
| +67 | -0.11 |
| -67 | +0.08 |
| +71 | -0.25 |
| -71 | +0.39 |
| +75 | -1.18 |
| -75 | -0.10 |
| +79 | -0.74 |
| -79 | +0.38 |
| +83 | -1.66 |
| -83 | +0.64 |
| +87 | -0.70 |
| -87 | -0.51 |
| +91 | -1.34 |
| -91 | -0.57 |
| +95 | -1.44 |
| -95 | -0.60 |
| +99 | -0.06 |
| -99 | -1.17 |
| +103 | +0.34 |
| -103 | -1.09 |

## Shown (not gating)

| Cut | b, % per unit (t) | Rows |
|---|---:|---:|
| Without the controls | +0.088 (+0.53) | 1484 |
| 1-week horizon (exit >= T + 14, 1 lag) | -0.006 (-0.11) | 1484 |
| Raw HP level instead of z (same rows) | +1.131 (+0.57) | 1484 |
| GLD alone | -0.005 (-0.02) | 371 |
| TLT alone | +0.086 (+0.27) | 371 |
| SPY alone | -0.345 (-0.80) | 371 |
| QQQ alone | +0.150 (+0.41) | 371 |
| IEF alone | +0.517 (+3.18) | 371 |
| SLV alone | -0.220 (-0.30) | 371 |
| BTC alone | -2.872 (-1.21) | 222 |
| Pre-gate years 2008-01-01..2018-05-29 (inside Fan et al.) | -0.184 (-1.19) | 2152 |

Feedback check (F2): 4-week change in z on the past 4-week return, pooled: slope +0.90 z per unit of log return (t +1.13, 1452 rows). Positive = hedgers add to their net short after a rally.
