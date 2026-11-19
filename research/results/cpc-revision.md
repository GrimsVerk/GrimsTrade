# CPC outlook revisions and next-session natural gas: gate (weather-2)

Rule: `research/weather-2.md` (card pushed before any price was loaded). Script
`research/lib/weather2_rev.py`. Dose: change in the gas-weighted cold-outlook index K
(mean of the 6-10 and 8-14 day CPC outlooks, signed tercile probability minus 1/3, at
state population centroids) between the latest issues before session t and before the
previous session. y: UNG open-to-close of session t, in percent. Slope in percentage
points per 0.10 of K, HC1 t. Winters 2012-13 .. 2024-25, train bars only.

Gas weights by Census division (NNLS 1981-2006, sum 1): 1: 0.039, 2: 0.147, 3: 0.229, 4: 0.089, 5: 0.102, 6: 0.045, 7: 0.091, 8: 0.084, 9: 0.173.
Outlook files parsed 4069, Fcst_Date differing from the file name 0, files without polygons 1, points 49. Issues with K: 2032.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Slope (t, n) | -0.076 (-0.68, 1327) | > 0, t >= 2 | False |
| Rank of t among 41 (1 = highest) | 36 | <= 2 | False |
| Slope 2012-17 / 2018-24 winters (t, n) | -0.028 (-0.22, 609) / -0.111 (-0.66, 718) | both > 0 | False |

**Gate: fail.**

## Placebo null (40 winter derangements)

SD of placebo t 0.95; share |t| >= 2 10%; 5/50/95% -0.77 / +0.78 / +2.26; min -0.79, max +2.76.

Placebo t, in draw order: +0.59, +1.09, +0.79, +2.47, -0.79, +1.59, +1.80, +2.19, +0.50, +1.79, -0.64, +1.35, +0.53, +0.84, +0.65, +1.13, +1.76, +0.06, -0.11, +2.76, +0.78, +1.09, +2.24, -0.74, +0.80, -0.79, +0.18, +0.43, +1.75, -0.77, +0.12, +1.12, +1.65, +0.64, +1.38, +1.75, +0.16, +0.41, +0.76, -0.73

## Shown (carded, not gating)

| Cell | Slope per 0.10 (t, n) | Rank of t among 41 |
|---|---:|---:|
| UNG dose check: close before t' to open t (not tradable) | +1.863 (+7.93, 1327) | 1 |
| UNG close t to close t+1 | +0.056 (+0.32, 1327) | 18 |
| UNG open t to close t+4 (overlapping) | -0.286 (-0.75, 1327) | 37 |
| UNG primary, 6-10 day outlook only | -0.057 (-0.65, 1327) | 35 |
| UNG primary, 8-14 day outlook only | -0.054 (-0.50, 1327) | 38 |
| XLE primary | +0.093 (+1.50, 1327) | 2 |

UNG mean y, top quintile of x (colder revisions) -0.020%, bottom +0.064%.
x: mean +0.0009, SD 0.0575 (K units); y: mean -0.070%, SD 2.132%.
