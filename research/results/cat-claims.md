# Hurricane landfalls and bonds: event-study gate (wide-8, W15)

Rule: `research/wide-8.md` step 3 (pushed before this ran). Script
`research/lib/wide8_catclaims.py`. Events: US mainland landfalls in NOAA HURDAT2.
Y = log LQD - 0.5 log TLT over 20 sessions after the event day; slope on the
Saffir-Simpson category (0 = tropical storm), percentage points per category, t
clustered by season.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| Slope, all events 2002-2025 (t, n) | +0.01 (+0.09, 104) | < 0, t <= -2 | False |
| Slope 2002-2013 / 2014-2025 (t) | -0.44 (-0.63, 53) / +0.13 (+1.84, 51) | both < 0 | False |
| Rank among 23 calendars (1 = most negative) | 8 | <= 2 | False |

**Gate: fail.**

## Shown

| Outcome | Slope per category, 20 sessions (t) | 60 sessions (t) |
|---|---:|---:|
| LQD - 0.5 TLT | +0.01 (+0.09) | +0.03 (+0.18) |
| LQD | -0.38 (-1.97) | -0.25 (-1.02) |
| TLT | -0.78 (-2.96) | -0.56 (-1.31) |
| LQD - IEF | +0.01 (+0.11) | +0.13 (+0.77) |

Mean Y, major landfalls (category >= 3, n 17) minus tropical-storm landfalls (n 58): +0.91 points.

Events by category: 0: 58, 1: 20, 2: 9, 3: 9, 4: 7, 5: 1

## Events (category >= 3)

| Storm | Event day | Category | Y, 20 sessions |
|---|---|---:|---:|
| Charley (AL032004) | 2004-08-13 | 4 | +0.84 |
| Ivan (AL092004) | 2004-09-16 | 3 | +0.39 |
| Jeanne (AL112004) | 2004-09-26 | 3 | +0.26 |
| Dennis (AL042005) | 2005-07-10 | 3 | +0.73 |
| Katrina (AL122005) | 2005-08-25 | 3 | +0.38 |
| Rita (AL182005) | 2005-09-24 | 3 | -0.42 |
| Wilma (AL252005) | 2005-10-24 | 3 | -0.05 |
| Harvey (AL092017) | 2017-08-26 | 4 | +0.47 |
| Irma (AL112017) | 2017-09-10 | 4 | +2.07 |
| Michael (AL142018) | 2018-10-10 | 5 | +0.28 |
| Laura (AL132020) | 2020-08-27 | 4 | -1.30 |
| Zeta (AL282020) | 2020-10-28 | 3 | +2.80 |
| Ida (AL092021) | 2021-08-29 | 4 | +0.76 |
| Ian (AL092022) | 2022-09-28 | 4 | +1.93 |
| Idalia (AL102023) | 2023-08-30 | 3 | +0.69 |
| Helene (AL092024) | 2024-09-27 | 4 | +0.03 |
| Milton (AL142024) | 2024-10-10 | 3 | +0.43 |

## Shifted calendars (slope, points per category)

| k years | Slope |
|---:|---:|
| -11 | -0.07 |
| -10 | +0.67 |
| -9 | -0.73 |
| -8 | +0.19 |
| -7 | +0.33 |
| -6 | -0.29 |
| -5 | +0.33 |
| -4 | +0.04 |
| -3 | +0.03 |
| -2 | +0.13 |
| -1 | -0.07 |
| +1 | +0.12 |
| +2 | +0.11 |
| +3 | -0.15 |
| +4 | +0.01 |
| +5 | +0.06 |
| +6 | +0.15 |
| +7 | +0.02 |
| +8 | +0.23 |
| +9 | +0.08 |
| +10 | -0.18 |
| +11 | +0.08 |
