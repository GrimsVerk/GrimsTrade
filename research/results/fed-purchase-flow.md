# Fed purchase operations and TLT: event-study gate (wide-10, W20)

Rule: `research/wide-10.md` step 2 (pushed before this ran). Script
`research/lib/wide10_fedflow.py`. Operations: NY Fed Markets API (keyless). y = TLT
open-to-close log return of day d; x = ln(1 + $bn par of 20+ year coupons the Fed bought
on d). Slopes in bps of return per unit of x; White (HC1) t.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| TLT 2014-01-02..2025-11-10 b (t), 2983 days | +3.3 (+0.37) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 11 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 11/41 = 0.268. Dosed days in the gate sample: 224, mean L $2.14bn, median $1.73bn, largest $10.95bn.

## Placebo null (dose calendar moved k trading days), TLT 2014-2025

40 placebo t: standard deviation 0.99, share with |t| >= 2 2%; quantiles 5% -1.67, 50% -0.62, 95% +1.06; smallest -2.27, largest +1.57.

| k (days) | t |
|---:|---:|
| +3 | +0.87 |
| -3 | -1.03 |
| +4 | +0.66 |
| -4 | -0.83 |
| +6 | +0.54 |
| -6 | -1.11 |
| +7 | -0.06 |
| -7 | -1.36 |
| +8 | -0.17 |
| -8 | -1.26 |
| +9 | +1.05 |
| -9 | -1.40 |
| +11 | -0.39 |
| -11 | -1.34 |
| +12 | -0.27 |
| -12 | -1.16 |
| +13 | +1.24 |
| -13 | -1.93 |
| +14 | +0.83 |
| -14 | -1.20 |
| +16 | +0.86 |
| -16 | -1.30 |
| +17 | +1.01 |
| -17 | -1.37 |
| +18 | +1.57 |
| -18 | -1.47 |
| +19 | -1.22 |
| -19 | -1.65 |
| +21 | -0.36 |
| -21 | -1.28 |
| +22 | -0.36 |
| -22 | -0.75 |
| +23 | +0.20 |
| -23 | -1.17 |
| +24 | -0.18 |
| -24 | -2.27 |
| +26 | -0.16 |
| -26 | -0.98 |
| +27 | +0.96 |
| -27 | -0.49 |

## Shown (not gating)

| Cut | b (t) | Days |
|---|---:|---:|
| TLT, papers' years 2009-03..2013-12 | -8.5 (-1.55) | 1219 |
| TLT gate sample, indicator dose (L > 0) | +2.8 (+0.46) | 2983 |
| TLT gate sample without 2020-03..2020-04 | +1.3 (+0.30) | 2940 |
| TLT close-to-close of d, gate sample | +10.7 (+0.91) | 2983 |
| TLT next day's open-to-close on today's x, gate sample | +4.5 (+0.51) | 2983 |
| IEF on its 7-10 year dose, gate sample | +1.0 (+0.44) | 2983 |
| IEF on its 7-10 year dose, papers' years | +0.4 (+0.22) | 1219 |
| SPY on all coupon par bought, gate sample | +0.4 (+0.10) | 2983 |
| SPY on all coupon par bought, papers' years | -0.5 (-0.15) | 1219 |
