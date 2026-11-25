# WHO outbreak reports and SPY over the next 4 weeks (wide-17, W30 `outbreak-premium`)

Rule: `research/cards/wide-17.md` (pushed before this ran). Script
`research/lib/wide17.py`. Dose x(F) = 2 sqrt(n + 3/8) minus its mean over the 52
weeks before, n = WHO Disease Outbreak News items published Saturday..Friday F.
y = log return of SPY from the close of the first bar >= F + 3 to the first bar
>= F + 31. Newey-West t, 4 lags, one row a week. Placebos both ways (allowed: WHO
reporting does not answer prices).

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Fridays 2005-01-07..2025-09-26, b (t), 1082 rows | +0.065% per unit of x (+1.68) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 9 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 9/41 = 0.220. (t - placebo median) / placebo sd = +0.86 (descriptive only).

## Placebo null (dose calendar moved k weeks; k > 0 an earlier dose)

40 placebo t: standard deviation 1.64, share with |t| >= 2 22%; quantiles 5% -3.38, 50% +0.27, 95% +2.17; smallest -3.64, largest +2.58.

| k (weeks) | t |
|---:|---:|
| +27 | +0.71 |
| -27 | -1.39 |
| +31 | +0.32 |
| -31 | +0.23 |
| +35 | -2.05 |
| -35 | -0.97 |
| +39 | +0.79 |
| -39 | +2.26 |
| +43 | -1.87 |
| -43 | +1.17 |
| +47 | -0.94 |
| -47 | +1.04 |
| +51 | -3.40 |
| -51 | +1.87 |
| +55 | +0.31 |
| -55 | -0.64 |
| +59 | -0.15 |
| -59 | +2.16 |
| +63 | -3.64 |
| -63 | +2.58 |
| +67 | -0.17 |
| -67 | -3.38 |
| +71 | +1.94 |
| -71 | +0.47 |
| +75 | +0.15 |
| -75 | +1.00 |
| +79 | +0.19 |
| -79 | -0.51 |
| +83 | +2.06 |
| -83 | -0.37 |
| +87 | -2.39 |
| -87 | +1.94 |
| +91 | +1.90 |
| -91 | -0.16 |
| +95 | +1.06 |
| -95 | -0.92 |
| +99 | +1.64 |
| -99 | -1.90 |
| +103 | +1.10 |
| -103 | +0.56 |

## Shown (not gating)

| Cut | b, % per unit (t) | Rows |
|---|---:|---:|
| QQQ instead of SPY | +0.117 (+2.21) | 1082 |
| GLD instead of SPY | -0.005 (-0.06) | 1082 |
| TLT instead of SPY | +0.002 (+0.04) | 1082 |
| XLV (health care) instead of SPY | +0.020 (+0.40) | 1082 |
| BTC and ETH pooled (DK 4 lags) | -0.186 (-0.74) | 1215 |
| Raw Anscombe count z instead of x | +0.018 (+0.40) | 1082 |
| 1-week horizon (exit >= F + 10, 1 lag) | +0.010 (+0.46) | 1082 |
| Fridays 2015-01-02..2025-09-26 (after Donadelli et al.) | +0.060 (+1.78) | 561 |
| With SPY's past 4/13/26/52-week returns | +0.068 (+1.81) | 1082 |
| Reaction: SPY over the dose week itself (premium story: negative) | +0.017 (+1.05) | 1082 |

Dose: 3162 reports to 2025-10-31; x sd over the gate weeks 2.34; weeks with no report 317 of 1082.
**Erratum after review (2026-11-24).** WHO's API dates are partly website migration dates:
about 812 archive items (1996-2003 reports among them) are dated 2021-06-07/08, with more bulk
dates in 2021-06 and 2024-03, and 2020 has no item. The week 2021-06-11 (814 items, x 54.8)
dominates the fit above. On Fridays 2005-01 .. 2019-12 only: b +0.082%, t +0.48, rank 21 of 41,
placebo SD 1.16. The kill stands; see `research/wide-17.md`, "Erratum after review".
