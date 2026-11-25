# Margin credit as the susceptible stock of a crash (parked-gates-1, W33 `margin-susceptibles`)

Rule: `research/cards/parked-gates-1.md` (pushed before this ran). Script
`research/lib/parkedgates1.py`. s = ln(broker receivables from customers / equities
market value) minus its 40-quarter mean (Z.1 via FRED, today's vintage), known from
3 months after the quarter end. y = GSPC log return over month m+1 on F = min(r(m), 0),
s, F s, c = GSPC return over months m-12..m-1, F c. Newey-West t, 3 lags. b3 = F s.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Months 1965-01..2025-09, b3 (t), 729 rows | +0.017 (+0.05) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 41 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 41/41 = 1.000.

## Placebo null (s calendar moved k months back only)

40 placebo t: standard deviation 0.58, share with |t| >= 2 30%; quantiles 5% +1.11, 50% +1.70, 95% +3.06; smallest +0.66, largest +3.27.

| k (months; > 0 an earlier dose) | t |
|---:|---:|
| +25 | +1.32 |
| +27 | +0.66 |
| +29 | +1.55 |
| +31 | +2.12 |
| +33 | +1.57 |
| +35 | +3.27 |
| +37 | +3.06 |
| +39 | +2.33 |
| +41 | +3.07 |
| +43 | +2.89 |
| +45 | +1.91 |
| +47 | +1.61 |
| +49 | +2.29 |
| +51 | +1.79 |
| +53 | +1.25 |
| +55 | +1.69 |
| +57 | +2.33 |
| +59 | +2.51 |
| +61 | +1.70 |
| +63 | +1.48 |
| +65 | +0.77 |
| +67 | +1.27 |
| +69 | +1.77 |
| +71 | +1.13 |
| +73 | +1.34 |
| +75 | +1.69 |
| +77 | +1.68 |
| +79 | +1.65 |
| +81 | +1.60 |
| +83 | +1.69 |
| +85 | +1.48 |
| +87 | +2.12 |
| +89 | +1.58 |
| +91 | +1.45 |
| +93 | +1.82 |
| +95 | +1.81 |
| +97 | +2.00 |
| +99 | +1.92 |
| +101 | +2.49 |
| +103 | +2.10 |

## Shown (not gating)

| Cut | b3 (t) | Rows |
|---|---:|---:|
| Without controls | +0.074 (+0.23) | 729 |
| Binary trigger 1[r(m) < -5%] x s | +0.021 (+0.83) | 729 |
| Stricter release lag (quarter end <= m - 6) | +0.134 (+0.35) | 729 |
| SPY instead of GSPC | -0.130 (-0.17) | 380 |
| Months 1965-01..1994-12 | -0.308 (-0.71) | 360 |
| Months 1995-01..2025-09 | -0.159 (-0.21) | 369 |
| Main effect b1 (F) | +0.014 (+0.16) | 729 |
| Main effect b2 (s) | -0.009 (-1.23) | 729 |

Same rows for all 41 fits (months 1970-10..2025-09, added after the dry run): b3 +0.001 (t +0.00), 660 rows, rank 41 of 41; placebo SD 0.59, share |t| >= 2 30%.

s sd over the gate months: 0.220; months with a fall below -5%: 70.
