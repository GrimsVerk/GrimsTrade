# Global temperature shocks and SPY's next month (wide-17, W29 `temperature-premium`)

Rule: `research/cards/wide-17.md` (pushed before this ran). Script
`research/lib/wide17.py`. Dose d(m) = 12-month mean of the GISTEMP v4 global
land-ocean anomaly minus its mean over the 10 years before (deg C; 2026-11-24 vintage).
y = log return of SPY over calendar month m + 2 (close of the last bar of m + 1 to the
close of the last bar of m + 2). Newey-West t, 3 lags, one row a month.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Outcome months 1993-02..2025-10, b (t), 393 rows | +3.252% per deg C (+1.63) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 9 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 9/41 = 0.220. (t - placebo median) / placebo sd = +1.18 (descriptive only).

## Placebo null (dose calendar moved k months; k > 0 an earlier dose)

40 placebo t: standard deviation 1.47, share with |t| >= 2 22%; quantiles 5% -2.10, 50% -0.11, 95% +2.85; smallest -2.39, largest +3.11.

| k (months) | t |
|---:|---:|
| +13 | -0.11 |
| -13 | +0.51 |
| +17 | -0.45 |
| -17 | -0.70 |
| +21 | -1.66 |
| -21 | -1.85 |
| +25 | -2.09 |
| -25 | -2.39 |
| +29 | -2.25 |
| -29 | -1.15 |
| +33 | -1.28 |
| -33 | -0.11 |
| +37 | -0.75 |
| -37 | +1.02 |
| +41 | -0.10 |
| -41 | +1.70 |
| +45 | -0.28 |
| -45 | +2.30 |
| +49 | -0.10 |
| -49 | +1.65 |
| +53 | -0.19 |
| -53 | +0.96 |
| +57 | -0.21 |
| -57 | +0.20 |
| +61 | -0.74 |
| -61 | -0.13 |
| +65 | -1.59 |
| -65 | -0.01 |
| +69 | -1.42 |
| -69 | +0.46 |
| +73 | -0.29 |
| -73 | +1.07 |
| +77 | +0.87 |
| -77 | +1.32 |
| +81 | +2.09 |
| -81 | +2.13 |
| +85 | +2.84 |
| -85 | +3.11 |
| +89 | +2.98 |
| -89 | +1.30 |

## Shown (not gating)

| Cut | b, % per unit (t) | Rows |
|---|---:|---:|
| QQQ instead of SPY | +5.832 (+1.52) | 319 |
| TLT instead of SPY | -0.835 (-0.35) | 279 |
| GLD instead of SPY | +5.816 (+2.15) | 251 |
| BTC and ETH pooled (DK 3 lags) | +14.710 (+0.91) | 278 |
| 12-month horizon (months m+2..m+13, NW 12 lags) | +26.138 (+1.73) | 382 |
| Monthly innovation A(m) - mean of the 120 months before | -0.229 (-0.16) | 393 |
| Outcome months 2013-01..2025-10 (after the literature) | +2.339 (+1.16) | 154 |
| Reaction: SPY over month m+1 (release month; premium story: negative) | +3.135 (+1.55) | 392 |

Dose sd over the gate months: 0.112 deg C.
