# Festival gold: event-study gate (wide-7, W13)

Rule: `research/wide-7.md` (pushed before this ran). Script
`research/lib/wide7_festival.py`.
GLD daily log returns on calendar-month dummies plus a festival-run dummy (the 15
sessions strictly before Dhanteras or the Lunar New Year); b = festival-run day minus
the same month's mean, bps a day; Newey-West t, 10 lags.

## Gate

| Test | b, bps a day (t) | Needed |
|---|---:|---|
| All GLD days 2004-11..2025-11 | -1.87 (-0.30) | b > 0, t >= 2 |
| To 2010 (Baur's years) | -8.61 (-0.64) | b > 0 |
| 2011 on | +1.11 (+0.16) | b > 0 |
| Rank of true dates among 15 weekly shifts | 10 | top 3 |

**Gate: fail.**

Shifts by k weeks (bps a day): -7: -4.9, -6: +1.4, -5: +1.5, -4: +4.8, -3: +0.5, -2: -2.3, -1: -4.0, +0: -1.9, +1: +4.3, +2: -4.3, +3: -2.3, +4: +3.4, +5: +6.9, +6: +4.0, +7: +0.2

## Shown

| Period | Both, 15 | Dhanteras only | Lunar New Year only | Both, no months | Both, 5 sessions |
|---|---:|---:|---:|---:|---:|
| all | -1.87 (-0.30) | +0.91 (+0.09) | -4.37 (-0.58) | +2.86 (+0.57) | +2.73 (+0.30) |
| to 2010 | -8.61 (-0.64) | -8.16 (-0.37) | -8.98 (-0.55) | -3.27 (-0.25) | +15.21 (+0.69) |
| 2011 on | +1.11 (+0.16) | +5.30 (+0.49) | -2.80 (-0.34) | +5.37 (+1.13) | -1.41 (-0.17) |

## Mean GLD return by calendar month, bps a day (Baur's autumn effect)

| Month | To 2010 | 2011 on |
|---|---:|---:|
| 1 | +18.9 | +13.9 |
| 2 | +12.4 | +1.4 |
| 3 | -6.4 | +5.6 |
| 4 | +10.2 | +7.6 |
| 5 | +4.8 | -5.1 |
| 6 | -0.9 | -1.6 |
| 7 | -0.3 | +7.7 |
| 8 | -2.3 | +10.2 |
| 9 | +22.0 | -8.6 |
| 10 | -2.2 | +4.9 |
| 11 | +29.4 | -6.6 |
| 12 | +6.0 | +1.6 |
