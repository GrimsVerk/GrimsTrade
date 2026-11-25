# fast-reentry-2: `or3-12` against exposure controls; `arm3-12` against `tsmom12`

Card: `cards/fast-reentry-2.md`. Written by `lib/fastreentry2.py`. Log points = 100 x natural log; I, B, N are rule minus holding; differences in (b) are `arm3-12` minus `tsmom12`. Paper series (Friday decisions, 2 bps a side, cash at 0), same 25% episodes and clusters as fast-reentry.

## (a) Timing or exposure? insure-1's card 2 controls, US 11 series

Card 1's 25% episodes and market-anchored clusters, cash at 0, each rule's paper series. Rotations: median (5th to 95th percentile) of 1,000, insure-1's seed; p = share of rotations at least as good. Description only.

| | Mean cluster S (share avoided) | Mean cluster N, log pts | Pooled premium P |
|---|---:|---:|---:|
| `tsmom12` | +0.50 | -0.3 | 1.07 |
| Fixed exposure (x = its average position, mean 73%) | +0.29 | +2.5 | 1.63 |
| Random timing (its positions rotated) | +0.27 (+0.21 to +0.34) | +1.3 (-1.4 to +4.2) | +1.82 (+1.44 to +2.57) |
| p: rotations at least as good | 0.000 | 0.817 | 0.000 |
| **Reading: Timing, not just exposure** | | | |
| `or3-12` | +0.35 | +1.2 | 0.97 |
| Fixed exposure (x = its average position, mean 83%) | +0.18 | +1.6 | 1.61 |
| Random timing (its positions rotated) | +0.17 (+0.12 to +0.22) | +0.8 (-1.6 to +3.1) | +1.85 (+1.33 to +2.82) |
| p: rotations at least as good | 0.000 | 0.408 | 0.000 |
| **Reading: Timing, not just exposure** | | | |
| `arm3-12` | +0.37 | +1.6 | 0.98 |
| Fixed exposure (x = its average position, mean 81%) | +0.20 | +1.8 | 1.61 |
| Random timing (its positions rotated) | +0.19 (+0.14 to +0.25) | +0.8 (-1.6 to +3.3) | +1.85 (+1.36 to +2.73) |
| p: rotations at least as good | 0.000 | 0.329 | 0.000 |
| **Reading: Timing, not just exposure** | | | |

## (b) `arm3-12`: exit as `tsmom12`, re-enter when the 3-month return turns positive

**Verdict by the card (family bar p < 0.025): In between.** US mean dN +1.8 (sign test 26 of 45, p 0.19; bootstrap p 0.114); non-US mean dN +5.3; premium US 1.07 -> 0.98, non-US 1.11 -> 0.97; share avoided US 0.50 -> 0.37 (guard: drop at most 0.10).

### US: market + 10 industries, 1927-2025 (decides)

Effective falls (clusters): 50; episodes: 270.

| Mean over effective falls | `tsmom12` | `arm3-12` | Difference | Falls where `arm3-12` is higher |
|---|---:|---:|---:|---:|
| I, loss avoided peak -> trough | +25.1 | +19.3 | -5.9 | 3 of 36 |
| B, the year after the low | -25.4 | -17.7 | +7.7 | 39 of 44 |
| **N = I + B** | -0.3 | +1.6 | +1.8 | 26 of 45 |
| S, share of the fall avoided | +0.50 | +0.37 | -0.13 | 3 of 36 |
| N > 0 (falls) | 16 of 50 | 22 of 50 | | |

Test of the difference in N (H1: `arm3-12` higher): sign test 26 of 45, p 0.19; cluster bootstrap mean +1.8, p 0.114, 90% range -0.6 to +4.3.

| Full period | `tsmom12` | `arm3-12` |
|---|---:|---:|
| Sum I / sum B / C, log pts | +8385 / -7613 / -1387 | +6729 / -5452 / -1111 |
| **Premium P** | **1.07** | **0.98** |
| Rule minus holding, log pts per series-year | -0.57 | +0.15 |
| Mean position | 73% | 81% |
| Position flips a year (mean over series) | 1.90 | 2.92 |
| Worst loss, first series (Mkt) | 38% | 51% |

`tsmom12` exits: 1030; at 369 of them the 3-month return was still positive (`or3-12` stays in; `arm3-12` leaves and waits for a dip and recovery).

| Era (episodes by peak, calm by date) | Premium `tsmom12` | Premium `arm3-12` | Rule minus holding per series-year: `tsmom12` / `arm3-12` |
|---|---:|---:|---|
| 1927-1961 | 0.85 | 0.78 | +1.82 / +2.08 |
| 1962-2001 | 1.38 | 1.10 | -1.67 / -0.39 |
| 2002-2025 | 1.34 | 1.31 | -2.19 / -1.72 |

| Peak to trough (episode level) | Episodes | Mean dI | Mean dB | Mean dN | dN > 0 | `tsmom12` N | `arm3-12` N |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast, <= 92 days | 63 | -4.9 | +5.1 | +0.3 | 20 | -6.5 | -6.3 |
| medium, 93-365 | 127 | -6.2 | +7.5 | +1.3 | 60 | +2.7 | +4.0 |
| slow, > 365 | 80 | -7.0 | +11.1 | +4.1 | 47 | +10.5 | +14.6 |

Effective falls, largest |dN| first (10):

| First peak | Last trough | Episodes | Mean depth | `tsmom12` N | `arm3-12` N | dI | dB | dN |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1932-09-07 | 1933-04-04 | 12 | 37% | +23 | -6 | -31 | +2 | -29 |
| 1972-12-11 | 1974-12-23 | 2 | 56% | +27 | +56 | -5 | +34 | +29 |
| 1929-12-07 | 1932-07-09 | 2 | 56% | +43 | +19 | -27 | +3 | -24 |
| 1931-10-20 | 1932-07-08 | 13 | 52% | +12 | +35 | -8 | +31 | +23 |
| 1930-04-05 | 1931-06-02 | 6 | 44% | +32 | +13 | -20 | +1 | -19 |
| 1955-11-14 | 1958-02-25 | 3 | 28% | -12 | +7 | +1 | +18 | +19 |
| 1930-04-23 | 1931-10-05 | 10 | 45% | +31 | +15 | -16 | +0 | -16 |
| 1964-07-07 | 1970-08-13 | 5 | 31% | -14 | +2 | +1 | +15 | +16 |
| 1968-11-12 | 1970-05-26 | 9 | 37% | +1 | +16 | -4 | +18 | +14 |
| 1961-11-14 | 1962-10-23 | 4 | 35% | -6 | +7 | -3 | +16 | +14 |

`arm3-12` minus `or3-12` (description): mean cluster dN +0.4, higher in 24 of 38 falls (two rules' N, same episodes).

### Non-US: 13 developed indices, price (decides, direction)

Effective falls (clusters): 19; episodes: 109.

| Mean over effective falls | `tsmom12` | `arm3-12` | Difference | Falls where `arm3-12` is higher |
|---|---:|---:|---:|---:|
| I, loss avoided peak -> trough | +27.0 | +23.1 | -3.9 | 2 of 15 |
| B, the year after the low | -27.9 | -18.6 | +9.2 | 19 of 19 |
| **N = I + B** | -0.9 | +4.4 | +5.3 | 13 of 19 |
| S, share of the fall avoided | +0.49 | +0.42 | -0.07 | 2 of 15 |
| N > 0 (falls) | 7 of 19 | 10 of 19 | | |

Test of the difference in N (H1: `arm3-12` higher): sign test 13 of 19, p 0.084; cluster bootstrap mean +5.3, p 0.000, 90% range +2.6 to +8.2.

| Full period | `tsmom12` | `arm3-12` |
|---|---:|---:|
| Sum I / sum B / C, log pts | +3613 / -3384 / -638 | +3111 / -2427 / -604 |
| **Premium P** | **1.11** | **0.97** |
| Rule minus holding, log pts per series-year | -0.83 | +0.16 |
| Mean position | 66% | 77% |
| Position flips a year (mean over series) | 2.35 | 3.83 |
| Worst loss, first series (Japan) | 41% | 41% |

`tsmom12` exits: 574; at 203 of them the 3-month return was still positive (`or3-12` stays in; `arm3-12` leaves and waits for a dip and recovery).

| Era (episodes by peak, calm by date) | Premium `tsmom12` | Premium `arm3-12` | Rule minus holding per series-year: `tsmom12` / `arm3-12` |
|---|---:|---:|---|
| before 2002 | 1.12 | 0.96 | -0.82 / +0.21 |
| 2002-2025 | 1.11 | 0.98 | -0.83 / +0.13 |

| Peak to trough (episode level) | Episodes | Mean dI | Mean dB | Mean dN | dN > 0 | `tsmom12` N | `arm3-12` N |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast, <= 92 days | 23 | -0.2 | +7.5 | +7.2 | 16 | -15.0 | -7.7 |
| medium, 93-365 | 40 | -4.9 | +7.9 | +2.9 | 23 | +3.1 | +6.1 |
| slow, > 365 | 46 | -6.5 | +10.2 | +3.7 | 27 | +9.7 | +13.5 |

Effective falls, largest |dN| first (10):

| First peak | Last trough | Episodes | Mean depth | `tsmom12` N | `arm3-12` N | dI | dB | dN |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1980-11-28 | 1982-07-08 | 1 | 44% | +14 | +36 | -3 | +25 | +22 |
| 1973-01-24 | 1974-10-09 | 1 | 37% | -0 | +20 | +1 | +20 | +20 |
| 2007-05-23 | 2009-03-09 | 12 | 52% | +16 | +28 | -13 | +25 | +13 |
| 1989-08-29 | 1991-01-16 | 5 | 34% | -3 | +9 | -2 | +14 | +12 |
| 2014-01-15 | 2014-10-16 | 1 | 26% | -19 | -9 | +0 | +10 | +10 |
| 1987-07-16 | 1987-11-11 | 3 | 39% | -16 | -9 | +0 | +7 | +7 |
| 1994-01-04 | 1995-10-23 | 4 | 33% | -7 | -0 | -4 | +10 | +7 |
| 2017-05-05 | 2020-03-23 | 13 | 38% | -14 | -8 | +1 | +5 | +6 |
| 2024-07-11 | 2024-08-05 | 1 | 25% | -8 | -2 | +0 | +6 | +6 |
| 1991-03-18 | 1992-08-18 | 1 | 47% | +29 | +24 | -6 | +1 | -5 |

`arm3-12` minus `or3-12` (description): mean cluster dN +0.6, higher in 11 of 16 falls (two rules' N, same episodes).

### French regions, total return, USD (description)

Effective falls (clusters): 13; episodes: 25.

| Mean over effective falls | `tsmom12` | `arm3-12` | Difference | Falls where `arm3-12` is higher |
|---|---:|---:|---:|---:|
| I, loss avoided peak -> trough | +30.1 | +24.8 | -5.3 | 2 of 10 |
| B, the year after the low | -29.7 | -18.4 | +11.3 | 12 of 12 |
| **N = I + B** | +0.4 | +6.5 | +6.0 | 9 of 12 |
| S, share of the fall avoided | +0.53 | +0.42 | -0.11 | 2 of 10 |
| N > 0 (falls) | 8 of 13 | 7 of 13 | | |

Test of the difference in N (H1: `arm3-12` higher): sign test 9 of 12, p 0.073; cluster bootstrap mean +6.0, p 0.025, 90% range +0.8 to +12.1.

| Full period | `tsmom12` | `arm3-12` |
|---|---:|---:|
| Sum I / sum B / C, log pts | +689 / -714 / -137 | +561 / -487 / -104 |
| **Premium P** | **1.23** | **1.05** |
| Rule minus holding, log pts per series-year | -1.57 | -0.28 |
| Mean position | 66% | 76% |
| Position flips a year (mean over series) | 2.68 | 4.20 |
| Worst loss, first series (FF-Europe) | 39% | 38% |

`tsmom12` exits: 137; at 55 of them the 3-month return was still positive (`or3-12` stays in; `arm3-12` leaves and waits for a dip and recovery).

| Era (episodes by peak, calm by date) | Premium `tsmom12` | Premium `arm3-12` | Rule minus holding per series-year: `tsmom12` / `arm3-12` |
|---|---:|---:|---|
| before 2002 | 0.91 | 0.87 | +0.90 / +0.98 |
| 2002-2025 | 1.49 | 1.19 | -2.66 / -0.84 |

| Peak to trough (episode level) | Episodes | Mean dI | Mean dB | Mean dN | dN > 0 | `tsmom12` N | `arm3-12` N |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast, <= 92 days | 2 | +0.0 | +1.2 | +1.2 | 1 | -19.7 | -18.5 |
| medium, 93-365 | 10 | -4.2 | +9.8 | +5.6 | 6 | -1.1 | +4.5 |
| slow, > 365 | 13 | -6.6 | +9.7 | +3.1 | 9 | +2.0 | +5.1 |

Effective falls, largest |dN| first (10):

| First peak | Last trough | Episodes | Mean depth | `tsmom12` N | `arm3-12` N | dI | dB | dN |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2007-10-31 | 2008-10-27 | 1 | 61% | +11 | +47 | -0 | +36 | +36 |
| 2007-10-31 | 2009-03-09 | 1 | 62% | +17 | +44 | -8 | +36 | +27 |
| 1994-02-04 | 1997-04-14 | 2 | 32% | -18 | -3 | +4 | +11 | +15 |
| 1991-11-04 | 1992-08-18 | 1 | 41% | +12 | +5 | -10 | +3 | -7 |
| 2018-01-24 | 2020-03-23 | 3 | 34% | -29 | -23 | +3 | +2 | +5 |
| 2014-09-03 | 2016-01-21 | 1 | 29% | +1 | -4 | -10 | +5 | -5 |
| 1997-06-26 | 1998-10-08 | 4 | 36% | +8 | +3 | -12 | +8 | -4 |
| 2021-06-10 | 2022-10-24 | 1 | 26% | +0 | +4 | -9 | +13 | +4 |
| 2021-09-06 | 2022-10-13 | 2 | 33% | -3 | -1 | -6 | +8 | +2 |
| 2011-04-28 | 2011-10-04 | 2 | 30% | -16 | -14 | -0 | +2 | +2 |

`arm3-12` minus `or3-12` (description): mean cluster dN +2.0, higher in 7 of 11 falls (two rules' N, same episodes).
