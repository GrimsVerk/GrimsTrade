# Same-calendar-month seasonality: event-study gate (survey-7, `seasonal-20y`)

Rule: `research/survey-7.md` (pushed before this ran). Script
`research/lib/survey7_season.py`. Signal = an asset's mean return in the same calendar
month over the past 20 years (at least 5); y = top fifth minus bottom fifth of the
23 assets, held from the last Friday of M - 1 to the last Friday of M.

## Gate (holding months 2017-01 .. 2025-10)

| Test | Value | Needed | Met |
|---|---:|---|---|
| Mean y a month (t), 106 months | +0.12% (+0.19) | > 0, t >= 2 | False |
| Rank of true t among 41 (1 = highest) | 31 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 31/41 = 0.756.

Assets per month: median 22 (min 21, max 23); years
per signal: median 20 (min 5, max 20).

## Placebo null (lags 12j + s, s = 1..10, j = 1 + a .. 20 + a, a = 0..3)

SD of placebo t 0.79; share with |t| >= 2 2%; quantiles
5/50/95% -0.72 / +0.58 / +1.57; extremes
-1.58 / +2.08. Placebos kept: 40 of 40.

| s | a = 0 | a = 1 | a = 2 | a = 3 |
|---:|---:|---:|---:|---:|
| 1 | -0.09 | +0.25 | +0.90 | +0.43 |
| 2 | +2.08 | +1.01 | +0.66 | -0.11 |
| 3 | +0.76 | +1.12 | +1.58 | +1.31 |
| 4 | -0.24 | +0.47 | +0.69 | +1.27 |
| 5 | +0.49 | -0.45 | -0.70 | +0.33 |
| 6 | +1.27 | -0.14 | +0.49 | +0.65 |
| 7 | +1.53 | +1.50 | +1.57 | +1.34 |
| 8 | +1.54 | +1.24 | +1.16 | +0.42 |
| 9 | +0.52 | +0.47 | +0.26 | +1.12 |
| 10 | +0.01 | -0.43 | -1.09 | -1.58 |

## Shown, not gating

| Cell | Mean y a month | t | Months |
|---|---:|---:|---:|
| Calendar months (month end to month end), 2017-2025 | +0.41% | +0.65 | 106 |
| Friday clock, 2004-01 .. 2016-12 | -0.10% | -0.31 | 156 |
| Calendar months, 2004-01 .. 2016-12 | -0.06% | -0.17 | 156 |
| Six live assets only, Friday clock, 2017-2025 | +0.37% | +0.18 | 53 |
| 17 ETFs only, Friday clock, 2017-2025 | -0.12% | -0.33 | 106 |
