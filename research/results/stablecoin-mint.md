# Stablecoin issuance and next-week coin returns: event-study gate (wide-10, W21)

Rule: `research/wide-10.md` step 3 (pushed before this ran). Script
`research/lib/wide10_mint.py`. Supply: DefiLlama (keyless). y = mean of BTC and ETH
log return, Friday 00:00 UTC to the next; m = the week's log change of total USD
stablecoin supply to Thursday 00:00 UTC; control = last week's y. b = next-week return
per unit of m (a 1% week of issuance is m = 0.01); White (HC1) t.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Fridays 2018-04-06..2025-10-31 b (t), 339 weeks | +0.16 (+1.06) | > 0, t >= 2 | False |
| Rank of true t among 41 calendars (1 = highest) | 17 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 17/41 = 0.415. Dose guards over 396 Fridays: {'small': 57, 'ok': 339}. Weekly m: mean +1.66%, sd 3.42%.

## Placebo null (dose calendar moved k weeks), 2018-2025

40 placebo t: standard deviation 1.24, share with |t| >= 2 28%; quantiles 5% -0.93, 50% +0.85, 95% +3.29; smallest -1.09, largest +3.34.

| k (weeks) | t |
|---:|---:|
| +3 | +0.88 |
| -3 | +2.33 |
| +4 | +1.25 |
| -4 | +2.88 |
| +5 | -0.73 |
| -5 | -0.38 |
| +6 | -0.53 |
| -6 | +2.04 |
| +7 | +0.67 |
| -7 | +0.58 |
| +8 | -1.09 |
| -8 | +0.31 |
| +9 | +0.23 |
| -9 | +2.57 |
| +10 | -0.27 |
| -10 | +1.63 |
| +11 | +0.61 |
| -11 | +3.29 |
| +12 | -0.05 |
| -12 | +0.92 |
| +13 | +0.85 |
| -13 | +3.31 |
| +14 | +1.21 |
| -14 | +2.15 |
| +15 | +3.34 |
| -15 | +2.23 |
| +16 | +1.41 |
| -16 | +0.92 |
| +17 | -1.01 |
| -17 | +2.07 |
| +18 | -0.93 |
| -18 | +1.80 |
| +19 | +0.15 |
| -19 | +2.35 |
| +20 | +0.86 |
| -20 | +0.26 |
| +21 | -0.15 |
| -21 | +0.29 |
| +22 | +0.16 |
| -22 | +0.04 |

## Shown (not gating)

| Cut | b (t) | Weeks |
|---|---:|---:|
| Without the control | +0.15 (+1.03) | 339 |
| BTC alone (own control) | +0.09 (+0.65) | 339 |
| ETH alone (own control) | +0.21 (+1.26) | 339 |
| Half 2018-04-06..2021-12-31 | +0.10 (+0.52) | 139 |
| Half 2022-01-01..2025-10-31 | -0.15 (-0.56) | 200 |
| Same week: this week's m on this week's return (no control) | +0.08 (+2.92) | 339 |

Next-week y after the top fifth of m (m >= 2.76%): mean +2.18% (68 weeks); after the rest +0.52% (271 weeks). The same-week row's slope is m per unit of return (reversed axes).
