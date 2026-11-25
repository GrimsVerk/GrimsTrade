# Solar activity and next-month US stock returns (wide-21, W35 `solar-max-recession`)

Rule: `research/cards/wide-21.md` (pushed before this ran). Script
`research/lib/wide21.py`. Dose x(m) = trailing 12-month mean SILSO total sunspot number
/ 100. y = ln((P(m+2) + D(m+2)/12) / P(m+1)), Shiller's monthly S&P 500 (P = monthly
average of daily closes). Newey-West t, 12 lags, one row a dose month.
Dose over the gate rows: mean 0.82, sd 0.64.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Dose months 1871-01..2023-07, b (t), 1831 rows | -0.162% a month per 100 sunspots (-0.87) | < 0, t <= -2 | False |
| Rank of true t among 41 calendars (1 = lowest) | 3 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 3/41 = 0.073.

## Placebo null (sunspot calendar moved k months, both ways)

40 placebo t: standard deviation 1.16, share with |t| >= 2 25%; quantiles 5% -0.58, 50% +1.25, 95% +2.83; smallest -1.18, largest +3.11.

| k (months; > 0 an earlier dose) | t |
|---:|---:|
| +19 | -1.18 |
| -19 | +0.18 |
| +23 | -0.91 |
| -23 | +0.67 |
| +27 | -0.56 |
| -27 | +1.19 |
| +31 | -0.31 |
| -31 | +1.63 |
| +35 | -0.02 |
| -35 | +1.99 |
| +39 | +0.29 |
| -39 | +2.41 |
| +43 | +0.54 |
| -43 | +2.72 |
| +47 | +0.83 |
| -47 | +3.08 |
| +51 | +1.13 |
| -51 | +3.11 |
| +55 | +1.56 |
| -55 | +2.82 |
| +59 | +1.62 |
| -59 | +2.27 |
| +63 | +1.73 |
| -63 | +1.67 |
| +67 | +1.89 |
| -67 | +0.94 |
| +71 | +2.25 |
| -71 | +0.55 |
| +75 | +2.51 |
| -75 | +0.24 |
| +79 | +2.52 |
| -79 | +0.20 |
| +83 | +2.29 |
| -83 | +0.16 |
| +87 | +1.92 |
| -87 | +0.02 |
| +91 | +1.51 |
| -91 | -0.27 |
| +95 | +1.31 |
| -95 | -0.48 |

## Shown (not gating)

Solar maxima used by the window cell (peaks of the 13-month smoothed series; look-ahead):
1870-08, 1883-12, 1894-01, 1906-02, 1917-08, 1928-04, 1937-04, 1947-05, 1958-03, 1968-11, 1979-12, 1989-11, 2001-11, 2014-04, 2024-10.

| Cut | b per 100 sunspots (t) | Rows |
|---|---:|---:|
| Gorbanev window (max -12..+24 months), indicator, look-ahead | -0.426% (-1.63) | 1831 |
| Phase: x(m) - x(m-12) | +0.135% (+0.47) | 1831 |
| 12-month horizon P(m+1)..P(m+13), NW 18 | -2.209% (-1.24) | 1820 |
| Crash: 20% fall within 12 months (LPM, pp per unit; predicted > 0), NW 18 | +0.968 pp (+0.40) | 1821 |
| GSPC month-end, 1950-01..2025-09 | -0.136% (-0.60) | 909 |
| GSPC month-end, post-Gorbanev dose months 2012-01.. | +0.247% (+0.52) | 165 |
| SPY month-end, from 1993-01 | -0.501% (-0.92) | 393 |
| QQQ month-end, from 1999-03 | -1.094% (-1.00) | 319 |
| TLT month-end, from 2002-07 | -0.054% (-0.15) | 279 |
| GLD month-end, from 2004-11 | -0.083% (-0.10) | 251 |
| BTC month-end, from 2012-01 | -0.669% (-0.18) | 165 |
| ETH month-end, from 2016-05 | -3.495% (-0.75) | 113 |
