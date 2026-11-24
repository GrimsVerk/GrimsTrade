# Lunar phases: event-study gate (wide-6, W3)

Rule: `research/wide-6.md` (pushed before this ran). Script
`research/lib/wide6_lunar.py`.
Daily close-to-close log returns; new-moon period minus full-moon period, bps a day;
Welch t; 15-day window (N = 7) unless stated. Rank = place of the true phase among 29
phase shifts (1 = largest difference).

## Gate: SPY, 2007-01 to 2025-11-10

| Days new / full | New minus full, bps a day (t) | Rank of 29 | Gate |
|---|---:|---:|---|
| 2342 / 2328 | +1.56 (+0.43) | 12 | **fail** |

Phase shifts 0..28 days (bps a day): +1.6, +2.2, +0.9, -2.0, -3.8, -6.8, -6.1, -5.2, -8.1, -7.0, -7.1, -5.5, -2.7, -0.2, +0.3, -2.4, -1.8, -0.3, +3.1, +4.9, +6.0, +6.4, +5.4, +7.8, +7.3, +7.7, +3.6, +1.9, -0.3

## Shown

| Series | Years | What | Days new / full | 15-day: bps (t), rank | 7-day: bps (t) |
|---|---|---|---|---:|---:|
| GSPC | 1962-01..1972-12 | before the paper's sample | 1360 / 1342 | +0.71 (+0.28), 9 | -0.41 (-0.12) |
| GSPC | 1973-01..2001-07 | paper's sample | 3573 / 3531 | +3.05 (+1.28), 5 | +5.91 (+1.67) |
| GSPC | 2001-08..2006-12 | after sample, before journal | 668 / 671 | -2.43 (-0.43), 22 | -4.31 (-0.54) |
| GSPC | 2007-01..2016-12 | post-publication, first half | 1244 / 1235 | +2.45 (+0.46), 11 | +0.85 (+0.11) |
| GSPC | 2017-01..2025-11 | post-publication, second half | 1098 / 1093 | +0.37 (+0.07), 14 | +5.33 (+0.74) |
| SPY | 1993-02..2001-07 | paper's sample | 1061 / 1049 | +7.33 (+1.54), 3 | +7.90 (+1.21) |
| SPY | 2007-01..2016-12 | gate, first half | 1244 / 1235 | +2.66 (+0.50), 11 | +1.57 (+0.20) |
| SPY | 2017-01..2025-11 | gate, second half | 1098 / 1093 | +0.32 (+0.06), 14 | +5.56 (+0.78) |
| QQQ | 2007-01..2025-11 | gate window | 2342 / 2328 | +0.53 (+0.13), 13 | +1.77 (+0.30) |
| N225 | 2007-01..2025-11 | gate window | 2275 / 2265 | +2.50 (+0.56), 10 | +2.10 (+0.32) |
| FTSE | 2007-01..2025-11 | gate window | 2359 / 2332 | +1.48 (+0.45), 11 | +1.93 (+0.41) |
| GDAXI | 2007-01..2025-11 | gate window | 2372 / 2340 | +0.76 (+0.20), 14 | -2.37 (-0.42) |
| BTC | 2014-01..2025-11 | coin, all days | 2129 / 2131 | +10.28 (+0.92), 1 | +12.21 (+0.75) |
