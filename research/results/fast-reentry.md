# fast-reentry: `or3-12` against `tsmom12` on insure-1/2's crash episodes

Card: `cards/fast-reentry.md`. Written by `lib/fastreentry.py`. Log points = 100 x natural log; I, B, N are rule minus holding; differences are `or3-12` minus `tsmom12` (dI, dB, dN). Both rules as paper series (Friday decisions, 2 bps a side, cash at 0), scored on the same 25% episodes; clusters as insure-1 (US, market-anchored) and insure-2 (non-US, anchored on the US market's falls).

**Verdict by the card: In between.** US mean dN +1.5 (sign test 30 of 50, p 0.1; bootstrap p 0.186); non-US mean dN +4.7; premium US 1.07 -> 0.97, non-US 1.11 -> 0.97; share avoided US 0.50 -> 0.35.

### US: market + 10 industries, 1927-2025 (decides)

Effective falls (clusters): 50; episodes: 270.

| Mean over effective falls | `tsmom12` | `or3-12` | Difference | Falls where `or3-12` is higher |
|---|---:|---:|---:|---:|
| I, loss avoided peak -> trough | +25.1 | +18.2 | -6.9 | 8 of 48 |
| B, the year after the low | -25.4 | -17.0 | +8.4 | 41 of 49 |
| **N = I + B** | -0.3 | +1.2 | +1.5 | 30 of 50 |
| S, share of the fall avoided | +0.50 | +0.35 | -0.15 | 9 of 49 |
| N > 0 (falls) | 18 of 50 | 21 of 50 | | |

Test of the difference in N (H1: `or3-12` higher): sign test 30 of 50, p 0.1; cluster bootstrap mean +1.5, p 0.186, 90% range -1.3 to +4.2.

| Full period | `tsmom12` | `or3-12` |
|---|---:|---:|
| Sum I / sum B / C, log pts | +8385 / -7613 / -1387 | +6472 / -5293 / -981 |
| **Premium P** | **1.07** | **0.97** |
| Rule minus holding, log pts per series-year | -0.57 | +0.18 |
| Mean position | 73% | 83% |
| Position flips a year (mean over series) | 1.90 | 2.51 |
| Worst loss, first series (Mkt) | 38% | 51% |

`tsmom12` exits: 1030; `or3-12` stayed in at 369 of them (3-month return still positive).

| Era (episodes by peak, calm by date) | Premium `tsmom12` | Premium `or3-12` | Rule minus holding per series-year: `tsmom12` / `or3-12` |
|---|---:|---:|---|
| 1927-1961 | 0.85 | 0.77 | +1.82 / +2.13 |
| 1962-2001 | 1.38 | 1.09 | -1.67 / -0.33 |
| 2002-2025 | 1.34 | 1.33 | -2.19 / -1.76 |

| Peak to trough (episode level) | Episodes | Mean dI | Mean dB | Mean dN | dN > 0 | `tsmom12` N | `or3-12` N |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast, <= 92 days | 63 | -4.9 | +6.5 | +1.7 | 38 | -6.5 | -4.8 |
| medium, 93-365 | 127 | -6.7 | +7.8 | +1.1 | 69 | +2.7 | +3.7 |
| slow, > 365 | 80 | -9.4 | +11.5 | +2.1 | 43 | +10.5 | +12.6 |

Effective falls, largest |dN| first (10):

| First peak | Last trough | Episodes | Mean depth | `tsmom12` N | `or3-12` N | dI | dB | dN |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1972-12-11 | 1974-12-23 | 2 | 56% | +27 | +60 | -5 | +38 | +33 |
| 1932-09-07 | 1933-04-04 | 12 | 37% | +23 | -6 | -31 | +2 | -29 |
| 2023-12-27 | 2024-04-22 | 1 | 31% | -49 | -24 | +0 | +25 | +25 |
| 1929-12-07 | 1932-07-09 | 2 | 56% | +43 | +18 | -27 | +2 | -25 |
| 1931-10-20 | 1932-07-08 | 13 | 52% | +12 | +35 | -8 | +31 | +23 |
| 1930-04-05 | 1931-06-02 | 6 | 44% | +32 | +11 | -22 | +1 | -22 |
| 1992-01-09 | 1993-08-13 | 1 | 35% | +1 | -17 | -19 | +1 | -18 |
| 1955-11-14 | 1958-02-25 | 3 | 28% | -12 | +6 | -1 | +19 | +17 |
| 1964-07-07 | 1970-08-13 | 5 | 31% | -14 | +2 | +1 | +16 | +17 |
| 1930-04-23 | 1931-10-05 | 10 | 45% | +31 | +15 | -16 | +0 | -16 |

### Non-US: 13 developed indices, price (decides, direction)

Effective falls (clusters): 19; episodes: 109.

| Mean over effective falls | `tsmom12` | `or3-12` | Difference | Falls where `or3-12` is higher |
|---|---:|---:|---:|---:|
| I, loss avoided peak -> trough | +27.0 | +22.4 | -4.5 | 2 of 18 |
| B, the year after the low | -27.9 | -18.6 | +9.3 | 18 of 19 |
| **N = I + B** | -0.9 | +3.8 | +4.7 | 12 of 19 |
| S, share of the fall avoided | +0.49 | +0.41 | -0.09 | 2 of 18 |
| N > 0 (falls) | 7 of 19 | 10 of 19 | | |

Test of the difference in N (H1: `or3-12` higher): sign test 12 of 19, p 0.18; cluster bootstrap mean +4.7, p 0.002, 90% range +1.9 to +7.8.

| Full period | `tsmom12` | `or3-12` |
|---|---:|---:|
| Sum I / sum B / C, log pts | +3613 / -3384 / -638 | +3028 / -2371 / -567 |
| **Premium P** | **1.11** | **0.97** |
| Rule minus holding, log pts per series-year | -0.83 | +0.18 |
| Mean position | 66% | 79% |
| Position flips a year (mean over series) | 2.35 | 3.35 |
| Worst loss, first series (Japan) | 41% | 43% |

`tsmom12` exits: 574; `or3-12` stayed in at 203 of them (3-month return still positive).

| Era (episodes by peak, calm by date) | Premium `tsmom12` | Premium `or3-12` | Rule minus holding per series-year: `tsmom12` / `or3-12` |
|---|---:|---:|---|
| before 2002 | 1.12 | 0.95 | -0.82 / +0.27 |
| 2002-2025 | 1.11 | 0.98 | -0.83 / +0.13 |

| Peak to trough (episode level) | Episodes | Mean dI | Mean dB | Mean dN | dN > 0 | `tsmom12` N | `or3-12` N |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast, <= 92 days | 23 | -0.2 | +7.6 | +7.4 | 18 | -15.0 | -7.6 |
| medium, 93-365 | 40 | -5.4 | +9.1 | +3.6 | 21 | +3.1 | +6.8 |
| slow, > 365 | 46 | -7.9 | +10.3 | +2.5 | 25 | +9.7 | +12.2 |

Effective falls, largest |dN| first (10):

| First peak | Last trough | Episodes | Mean depth | `tsmom12` N | `or3-12` N | dI | dB | dN |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1980-11-28 | 1982-07-08 | 1 | 44% | +14 | +36 | -3 | +25 | +22 |
| 1973-01-24 | 1974-10-09 | 1 | 37% | -0 | +18 | -1 | +19 | +18 |
| 2014-01-15 | 2014-10-16 | 1 | 26% | -19 | -6 | +0 | +13 | +13 |
| 2007-05-23 | 2009-03-09 | 12 | 52% | +16 | +28 | -13 | +25 | +12 |
| 1989-08-29 | 1991-01-16 | 5 | 34% | -3 | +8 | -4 | +14 | +11 |
| 1991-03-18 | 1992-08-18 | 1 | 47% | +29 | +22 | -9 | +1 | -7 |
| 1987-07-16 | 1987-11-11 | 3 | 39% | -16 | -9 | +0 | +7 | +7 |
| 1994-01-04 | 1995-10-23 | 4 | 33% | -7 | +0 | -5 | +11 | +7 |
| 2017-05-05 | 2020-03-23 | 13 | 38% | -14 | -8 | -0 | +7 | +7 |
| 1996-02-06 | 1998-10-09 | 14 | 39% | -4 | +2 | -3 | +9 | +6 |

### French regions, total return, USD (description)

Effective falls (clusters): 13; episodes: 25.

| Mean over effective falls | `tsmom12` | `or3-12` | Difference | Falls where `or3-12` is higher |
|---|---:|---:|---:|---:|
| I, loss avoided peak -> trough | +30.1 | +23.0 | -7.1 | 2 of 13 |
| B, the year after the low | -29.7 | -18.6 | +11.1 | 12 of 13 |
| **N = I + B** | +0.4 | +4.5 | +4.0 | 7 of 13 |
| S, share of the fall avoided | +0.53 | +0.38 | -0.14 | 2 of 13 |
| N > 0 (falls) | 8 of 13 | 7 of 13 | | |

Test of the difference in N (H1: `or3-12` higher): sign test 7 of 13, p 0.5; cluster bootstrap mean +4.0, p 0.138, 90% range -1.7 to +10.3.

| Full period | `tsmom12` | `or3-12` |
|---|---:|---:|
| Sum I / sum B / C, log pts | +689 / -714 / -137 | +536 / -481 / -85 |
| **Premium P** | **1.23** | **1.06** |
| Rule minus holding, log pts per series-year | -1.57 | -0.29 |
| Mean position | 66% | 79% |
| Position flips a year (mean over series) | 2.68 | 3.54 |
| Worst loss, first series (FF-Europe) | 39% | 36% |

`tsmom12` exits: 137; `or3-12` stayed in at 55 of them (3-month return still positive).

| Era (episodes by peak, calm by date) | Premium `tsmom12` | Premium `or3-12` | Rule minus holding per series-year: `tsmom12` / `or3-12` |
|---|---:|---:|---|
| before 2002 | 0.91 | 0.88 | +0.90 / +0.92 |
| 2002-2025 | 1.49 | 1.19 | -2.66 / -0.82 |

| Peak to trough (episode level) | Episodes | Mean dI | Mean dB | Mean dN | dN > 0 | `tsmom12` N | `or3-12` N |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast, <= 92 days | 2 | -0.0 | +2.3 | +2.3 | 1 | -19.7 | -17.4 |
| medium, 93-365 | 10 | -5.0 | +10.5 | +5.5 | 6 | -1.1 | +4.4 |
| slow, > 365 | 13 | -7.9 | +9.5 | +1.5 | 7 | +2.0 | +3.5 |

Effective falls, largest |dN| first (10):

| First peak | Last trough | Episodes | Mean depth | `tsmom12` N | `or3-12` N | dI | dB | dN |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2007-10-31 | 2008-10-27 | 1 | 61% | +11 | +47 | -0 | +36 | +36 |
| 1994-02-04 | 1997-04-14 | 2 | 32% | -18 | +2 | +6 | +14 | +20 |
| 2007-10-31 | 2009-03-09 | 1 | 62% | +17 | +33 | -17 | +33 | +16 |
| 1991-11-04 | 1992-08-18 | 1 | 41% | +12 | -0 | -16 | +3 | -13 |
| 2018-01-24 | 2020-03-23 | 3 | 34% | -29 | -19 | +3 | +7 | +10 |
| 1997-06-26 | 1998-10-08 | 4 | 36% | +8 | +1 | -12 | +5 | -7 |
| 2014-09-03 | 2016-01-21 | 1 | 29% | +1 | -5 | -12 | +5 | -7 |
| 2006-05-09 | 2009-03-10 | 1 | 52% | +11 | +5 | -19 | +13 | -7 |
| 2021-09-06 | 2022-10-13 | 2 | 33% | -3 | +3 | -6 | +12 | +6 |
| 2021-06-10 | 2022-10-24 | 1 | 26% | +0 | -5 | -11 | +6 | -5 |
