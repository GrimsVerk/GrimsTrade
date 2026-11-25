# insure-2: crash insurance of `tsmom12` per era and outside the US

Written by `lib/insure2.py`. Log points = 100 x natural log; every number is rule minus holding unless said otherwise. Cash earns 0.

## Step 1, insure-era: card 2's controls per era

Card: `cards/insure-era.md`. Same 11 series, insure-1's 25% episodes, market-anchored clusters and calm mask, cash at 0, the rule as its paper series. Episodes by peak, clusters by first peak, calm by date. Fixed exposure: x = the rule's mean position in the window (whole-span x as second reading). Rotations: the 11-series block of the rule's positions rotated within the window, 1,000 per window, median (5-95%). p = share of rotations at least as good as the rule.

| Window | Clusters | Episodes | Rule S | Fixed S | Rotations S | p (S) | Rule P | Fixed P | Fixed P (whole-span x) | Rotations P | p (P) | Mean x | Verdict |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---|
| 1927-1961 | 22 | 138 | 0.55 | 0.32 | +0.29 (+0.20 to +0.43) | 0.000 | 0.85 | 1.38 | 1.38 | +1.63 (+1.09 to +2.88) | 0.000 | 70% | Timing, not just exposure |
| 1962-2001 | 15 | 72 | 0.47 | 0.26 | +0.25 (+0.17 to +0.39) | 0.002 | 1.38 | 2.15 | 2.17 | +2.60 (+1.56 to +4.63) | 0.013 | 75% | Timing, not just exposure |
| 2002-2025 | 13 | 60 | 0.45 | 0.34 | +0.30 (+0.20 to +0.43) | 0.032 | 1.34 | 1.53 | 1.60 | +1.90 (+1.07 to +3.54) | 0.191 | 75% | In between |
| 1962-2025 | 28 | 132 | 0.46 | 0.28 | +0.26 (+0.17 to +0.36) | 0.000 | 1.36 | 1.88 | 1.90 | +2.20 (+1.45 to +3.87) | 0.022 | 75% | Timing, not just exposure |

Detail per window: the rule's sums (log points, paper series), the net N, and a sign test of the rule's cluster I (only with at least 10 clusters).

| Window | Sum I | Sum B | C | Rule N | Fixed N | Rotations N | p (N) | Rule I > 0 (sign test) | Clusters where rule S > fixed S | Rule minus holding per series-year, log pts |
|---|---:|---:|---:|---:|---:|---|---:|---|---|---:|
| 1927-1961 | +4768 | -3872 | -204 | +4.2 | +3.9 | +2.6 (-1.9 to +8.2) | 0.261 | 21 of 22 (p 5.5e-06) | 16 of 22 | +1.82 |
| 1962-2001 | +1915 | -1957 | -692 | -2.3 | +2.8 | +2.0 (-2.7 to +6.4) | 0.934 | 15 of 15 (p 3.1e-05) | 12 of 15 | -1.67 |
| 2002-2025 | +1703 | -1784 | -492 | -5.5 | -0.3 | -1.7 (-7.4 to +2.5) | 0.912 | 12 of 13 (p 0.0017) | 8 of 13 | -2.19 |
| 1962-2025 | +3618 | -3741 | -1184 | -3.8 | +1.5 | +0.4 (-4.3 to +4.4) | 0.919 | 27 of 28 (p 1.1e-07) | 20 of 28 | -1.86 |

Fixed exposure's S is about 1 - x in every episode (it holds x of each fall); the last column counts clusters where the rule's S beats it.

**Headline by the card (1962-2025 window): Timing, not just exposure -> Yes.** Per era: 1927-1961 Timing, not just exposure; 1962-2001 Timing, not just exposure; 2002-2025 In between.


## Step 2, insure-geo: outside the US

Card: `cards/insure-geo.md`. `tsmom12` paper series (Friday decisions, 12-month lookback, 2 bps a side, cash at 0) on each index's closes, from its first decision to 2025-10-31; insure-1's 25% / 25% episodes and metrics. Clusters anchored on the US market's 25% falls (French daily market); a cluster's value is the mean over its non-US episodes. Yahoo indices: price indices in local currency (DAX: total return); French regions: total return in US dollars.

### Primary: 13 developed markets (Yahoo)

| Series | First decision | Sessions | Mean position | Episodes | Open fall (peak) | Sum I | Sum B | C | Premium P | Worst loss rule / hold |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| Japan | 1966-01-24 | 14701 | 65% | 13 | - | +435 | -335 | -57 | 0.90 | 41% / 82% |
| Canada | 1980-07-07 | 11383 | 68% | 7 | - | +210 | -213 | -79 | 1.39 | 34% / 50% |
| UK | 1984-12-31 | 10317 | 71% | 4 | - | +151 | -108 | -96 | 1.35 | 38% / 53% |
| Australia | 1985-08-19 | 10172 | 72% | 4 | - | +125 | -140 | -67 | 1.65 | 54% / 55% |
| HongKong | 1988-01-11 | 9334 | 62% | 15 | - | +459 | -497 | -13 | 1.11 | 47% / 65% |
| Germany | 1989-01-02 | 9319 | 69% | 10 | - | +289 | -349 | -40 | 1.35 | 52% / 73% |
| Singapore | 1989-01-16 | 9202 | 59% | 8 | - | +351 | -338 | -40 | 1.08 | 47% / 68% |
| France | 1991-03-11 | 8806 | 66% | 9 | - | +283 | -221 | -62 | 1.00 | 40% / 65% |
| Switzerland | 1991-11-18 | 8531 | 68% | 6 | - | +189 | -178 | -65 | 1.29 | 38% / 56% |
| Belgium | 1992-04-21 | 8524 | 63% | 7 | - | +207 | -184 | -20 | 0.98 | 38% / 68% |
| Netherlands | 1993-10-11 | 8185 | 71% | 6 | - | +271 | -207 | -54 | 0.96 | 36% / 72% |
| Austria | 1993-11-22 | 7939 | 63% | 12 | - | +367 | -372 | -22 | 1.07 | 50% / 72% |
| Spain | 1994-07-18 | 7932 | 60% | 8 | - | +276 | -242 | -23 | 0.96 | 54% / 63% |
| **pooled** | | | | 109 | | +3613 | -3384 | -638 | **1.11** | |

Premium by era (episodes by peak, calm by date): before 2002 1.12 (44 episodes; rule minus holding -0.82 log pts per series-year); 2002-2025 1.11 (65 episodes; rule minus holding -0.83 log pts per series-year).

| Test | Clusters (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p | 90% range |
|---|---:|---:|---:|---:|---:|---|
| I, anchored on US falls | 18 | 17 | 7.2e-05 | +27.0 | 0.000 | +19.9 to +34.3 |
| I, linked (strict) | 15 | 14 | 0.00049 | +25.1 | 0.000 | +17.7 to +33.1 |
| N = I + B, anchored | 19 | 7 | 0.92 | -0.9 | 0.614 | -6.2 to +4.7 |
| N = I + B, linked | 16 | 4 | 0.99 | -2.2 | 0.736 | -7.6 to +3.7 |
| Share avoided S, anchored | 18 | 17 | 7.2e-05 | +0.5 | 0.000 | +0.4 to +0.6 |

Episodes 109; anchored clusters (effective episodes) 19; linked 16. Verdict by card 1's rule: **Insurance real, handed back in the rebound**.

| Peak to trough | Episodes | Mean depth | Mean I | I > 0 | Mean S | Mean N | N > 0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast, <= 92 days | 23 | 34% | +14.6 | 20 | +0.35 | -15.0 | 3 |
| medium, 93-365 | 40 | 37% | +33.2 | 40 | +0.64 | +3.1 | 16 |
| slow, > 365 | 46 | 45% | +42.4 | 45 | +0.63 | +9.7 | 32 |

Sensitivity (anchored): 20% falls: 36 clusters, I > 0 in 32 of 34 (p 3.5e-08), mean N -2.9, premium 1.09; 40% falls: 11 clusters, I > 0 in 11 of 11 (p 0.00049), mean N +9.2, premium 1.18.

Card 2's controls (rotations by one common calendar offset, 1,000, median and 5-95%):

| | Mean cluster S | Mean cluster N | Pooled premium P |
|---|---:|---:|---:|
| `tsmom12` | +0.49 | -0.9 | 1.11 |
| Fixed exposure (mean x 66%) | +0.36 | +6.3 | 1.33 |
| Random timing | +0.34 (+0.25 to +0.45) | +4.5 (+0.5 to +8.7) | +1.52 (+1.19 to +2.09) |
| p: rotations at least as good | 0.000 | 0.989 | 0.008 |

Verdict by card 2's rule: **Timing, not just exposure**.

Anchored clusters:

| # | First peak | Last trough | Non-US episodes | Mean depth | Mean I | Mean S | Mean N | Series |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | 1973-01-24 | 1974-10-09 | 1 | 37% | +25 | +0.53 | -0 | Japan |
| 2 | 1980-11-28 | 1982-07-08 | 1 | 44% | +51 | +0.88 | +14 | Canada |
| 3 | 1987-07-16 | 1987-11-11 | 3 | 39% | +5 | +0.08 | -16 | Australia, Canada, UK |
| 4 | 1989-05-15 | 1989-06-05 | 1 | 37% | -0 | -0.00 | -23 | HongKong |
| 5 | 1989-08-29 | 1991-01-16 | 5 | 34% | +22 | +0.51 | -3 | Australia, Canada, Germany, Japan, Singapore |
| 6 | 1991-03-18 | 1992-08-18 | 1 | 47% | +60 | +0.93 | +29 | Japan |
| 7 | 1994-01-04 | 1995-10-23 | 4 | 33% | +19 | +0.48 | -7 | Austria, France, HongKong, Japan |
| 8 | 1996-02-06 | 1998-10-09 | 14 | 39% | +26 | +0.46 | -4 | Austria, Belgium, Canada, France, Germany, HongKong, Japan, Netherlands, Singapore, Spain, Switzerland |
| 9 | 1999-01-06 | 2003-03-12 | 4 | 37% | +35 | +0.72 | +3 | Belgium, France, Germany, UK |
| 10 | 2000-01-03 | 2003-04-28 | 20 | 44% | +45 | +0.74 | +18 | Austria, Belgium, Canada, France, Germany, HongKong, Japan, Netherlands, Singapore, Spain, Switzerland |
| 11 | 2007-05-23 | 2009-03-09 | 12 | 52% | +64 | +0.85 | +16 | Australia, Austria, Belgium, Canada, France, Germany, HongKong, Netherlands, Singapore, Spain, Switzerland, UK |
| 12 | 2007-07-09 | 2009-03-10 | 6 | 46% | +53 | +0.82 | +24 | Austria, HongKong, Japan |
| 13 | 2010-01-06 | 2012-07-24 | 10 | 34% | +21 | +0.46 | -6 | Austria, Belgium, France, Germany, HongKong, Japan, Netherlands, Spain, Switzerland |
| 14 | 2014-01-15 | 2014-10-16 | 1 | 26% | +5 | +0.18 | -19 | Austria |
| 15 | 2015-04-10 | 2016-06-27 | 7 | 30% | +16 | +0.44 | -6 | Austria, France, Germany, HongKong, Japan, Singapore, Spain |
| 16 | 2017-05-05 | 2020-03-23 | 13 | 38% | +27 | +0.52 | -14 | Australia, Austria, Belgium, Canada, France, Germany, HongKong, Japan, Netherlands, Singapore, Spain, Switzerland, UK |
| 17 | 2021-02-17 | 2024-01-22 | 3 | 37% | +28 | +0.48 | +3 | Belgium, HongKong |
| 18 | 2022-01-05 | 2022-09-29 | 2 | 31% | +10 | +0.28 | -17 | Austria, Germany |
| 19 | 2024-07-11 | 2024-08-05 | 1 | 25% | +0 | +0.00 | -8 | Japan |

### Total-return check: French regions (USD)

| Series | First decision | Sessions | Mean position | Episodes | Open fall (peak) | Sum I | Sum B | C | Premium P | Worst loss rule / hold |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| FF-Europe | 1991-06-24 | 8966 | 69% | 7 | - | +181 | -215 | -48 | 1.46 | 39% / 62% |
| FF-Japan | 1991-06-24 | 8966 | 59% | 9 | - | +270 | -210 | -52 | 0.97 | 39% / 60% |
| FF-AsiaPacExJapan | 1991-06-24 | 8966 | 69% | 9 | - | +238 | -289 | -36 | 1.36 | 39% / 62% |
| **pooled** | | | | 25 | | +689 | -714 | -137 | **1.23** | |

Premium by era (episodes by peak, calm by date): before 2002 0.91 (11 episodes; rule minus holding +0.90 log pts per series-year); 2002-2025 1.49 (14 episodes; rule minus holding -2.66 log pts per series-year).

| Test | Clusters (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p | 90% range |
|---|---:|---:|---:|---:|---:|---|
| I, anchored on US falls | 13 | 12 | 0.0017 | +30.1 | 0.000 | +20.0 to +40.8 |
| I, linked (strict) | 11 | 10 | 0.0059 | +24.9 | 0.000 | +16.1 to +34.4 |
| N = I + B, anchored | 13 | 8 | 0.29 | +0.4 | 0.433 | -5.8 to +6.2 |
| N = I + B, linked | 11 | 6 | 0.5 | -1.1 | 0.585 | -8.1 to +5.5 |
| Share avoided S, anchored | 13 | 12 | 0.0017 | +0.5 | 0.000 | +0.4 to +0.6 |

Episodes 25; anchored clusters (effective episodes) 13; linked 11. Verdict by card 1's rule: **Insurance real, handed back in the rebound**.

| Peak to trough | Episodes | Mean depth | Mean I | I > 0 | Mean S | Mean N | N > 0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast, <= 92 days | 2 | 30% | +5.2 | 1 | +0.12 | -19.7 | 1 |
| medium, 93-365 | 10 | 34% | +25.9 | 9 | +0.55 | -1.1 | 5 |
| slow, > 365 | 13 | 40% | +32.3 | 12 | +0.55 | +2.0 | 8 |

Sensitivity (anchored): 20% falls: 21 clusters, I > 0 in 20 of 21 (p 1e-05), mean N -2.8, premium 1.18; 40% falls: 5 clusters, I > 0 in 5 of 5 (p 0.031), mean N +17.8, premium 1.39.

Card 2's controls (rotations by one common calendar offset, 1,000, median and 5-95%):

| | Mean cluster S | Mean cluster N | Pooled premium P |
|---|---:|---:|---:|
| `tsmom12` | +0.53 | +0.4 | 1.23 |
| Fixed exposure (mean x 66%) | +0.36 | +5.5 | 1.40 |
| Random timing | +0.33 (+0.18 to +0.51) | +4.0 (-8.8 to +15.4) | +1.60 (+0.95 to +2.82) |
| p: rotations at least as good | 0.034 | 0.691 | 0.239 |

Verdict by card 2's rule: **In between**.

Anchored clusters:

| # | First peak | Last trough | Non-US episodes | Mean depth | Mean I | Mean S | Mean N | Series |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | 1991-11-04 | 1992-08-18 | 1 | 41% | +40 | +0.76 | +12 | FF-Japan |
| 2 | 1993-08-17 | 1993-11-29 | 1 | 26% | -0 | -0.00 | -0 | FF-Japan |
| 3 | 1994-02-04 | 1997-04-14 | 2 | 32% | +5 | +0.15 | -18 | FF-AsiaPacExJapan, FF-Japan |
| 4 | 1997-06-26 | 1998-10-08 | 4 | 36% | +32 | +0.62 | +8 | FF-AsiaPacExJapan, FF-Europe, FF-Japan |
| 5 | 2000-01-03 | 2003-04-28 | 5 | 39% | +37 | +0.74 | +10 | FF-AsiaPacExJapan, FF-Europe, FF-Japan |
| 6 | 2006-05-09 | 2009-03-10 | 1 | 52% | +47 | +0.65 | +11 | FF-Japan |
| 7 | 2007-10-31 | 2008-10-27 | 1 | 61% | +71 | +0.75 | +11 | FF-AsiaPacExJapan |
| 8 | 2007-10-31 | 2009-03-09 | 1 | 62% | +74 | +0.76 | +17 | FF-Europe |
| 9 | 2011-04-28 | 2011-10-04 | 2 | 30% | +7 | +0.19 | -16 | FF-AsiaPacExJapan, FF-Europe |
| 10 | 2014-09-03 | 2016-01-21 | 1 | 29% | +22 | +0.64 | +1 | FF-AsiaPacExJapan |
| 11 | 2018-01-24 | 2020-03-23 | 3 | 34% | +9 | +0.19 | -29 | FF-AsiaPacExJapan, FF-Europe, FF-Japan |
| 12 | 2021-06-10 | 2022-10-24 | 1 | 26% | +24 | +0.78 | +0 | FF-AsiaPacExJapan |
| 13 | 2021-09-06 | 2022-10-13 | 2 | 33% | +24 | +0.60 | -3 | FF-Europe, FF-Japan |

### Wider set: 10 more indices (Yahoo)

| Series | First decision | Sessions | Mean position | Episodes | Open fall (peak) | Sum I | Sum B | C | Premium P | Worst loss rule / hold |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| Italy | 1998-12-21 | 6862 | 61% | 9 | - | +314 | -290 | -28 | 1.01 | 62% / 75% |
| NewZealand | 2004-01-12 | 5378 | 80% | 2 | - | +58 | -43 | -9 | 0.89 | 25% / 44% |
| Israel | 1993-10-04 | 7494 | 69% | 9 | - | +210 | -221 | -26 | 1.17 | 30% / 54% |
| Korea | 1998-01-05 | 6858 | 62% | 10 | - | +320 | -280 | -86 | 1.15 | 42% / 56% |
| Taiwan | 1998-07-20 | 6693 | 66% | 10 | - | +298 | -282 | -23 | 1.03 | 50% / 66% |
| India | 1998-07-20 | 6727 | 74% | 7 | - | +149 | -156 | -53 | 1.40 | 41% / 61% |
| Brazil | 1994-05-09 | 7801 | 66% | 17 | - | +395 | -507 | -10 | 1.31 | 61% / 65% |
| Mexico | 1992-11-30 | 8260 | 70% | 10 | - | +253 | -288 | -100 | 1.54 | 50% / 49% |
| Malaysia | 1994-12-12 | 7586 | 56% | 6 | - | +299 | -247 | -52 | 1.00 | 46% / 79% |
| Indonesia | 1991-04-29 | 8413 | 67% | 12 | - | +392 | -409 | -54 | 1.18 | 53% / 65% |
| **pooled** | | | | 92 | | +2688 | -2724 | -441 | **1.18** | |

Premium by era (episodes by peak, calm by date): before 2002 0.98 (41 episodes; rule minus holding +0.51 log pts per series-year); 2002-2025 1.37 (51 episodes; rule minus holding -2.14 log pts per series-year).

| Test | Clusters (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p | 90% range |
|---|---:|---:|---:|---:|---:|---|
| I, anchored on US falls | 17 | 15 | 0.0012 | +24.7 | 0.000 | +16.9 to +32.8 |
| I, linked (strict) | 15 | 13 | 0.0037 | +22.5 | 0.000 | +14.5 to +31.1 |
| N = I + B, anchored | 17 | 9 | 0.5 | -0.3 | 0.555 | -4.4 to +4.5 |
| N = I + B, linked | 15 | 9 | 0.3 | +0.9 | 0.408 | -3.4 to +5.9 |
| Share avoided S, anchored | 17 | 15 | 0.0012 | +0.5 | 0.000 | +0.3 to +0.6 |

Episodes 92; anchored clusters (effective episodes) 17; linked 15. Verdict by card 1's rule: **Insurance real, handed back in the rebound**.

| Peak to trough | Episodes | Mean depth | Mean I | I > 0 | Mean S | Mean N | N > 0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast, <= 92 days | 19 | 35% | +15.7 | 17 | +0.35 | -12.3 | 6 |
| medium, 93-365 | 49 | 38% | +30.2 | 42 | +0.55 | +1.4 | 24 |
| slow, > 365 | 24 | 43% | +37.9 | 24 | +0.62 | +5.4 | 15 |

Sensitivity (anchored): 20% falls: 33 clusters, I > 0 in 31 of 33 (p 6.5e-08), mean N -0.7, premium 1.15; 40% falls: 10 clusters, I > 0 in 10 of 10 (p 0.00098), mean N +3.4, premium 1.26.

Card 2's controls (rotations by one common calendar offset, 1,000, median and 5-95%):

| | Mean cluster S | Mean cluster N | Pooled premium P |
|---|---:|---:|---:|
| `tsmom12` | +0.47 | -0.3 | 1.18 |
| Fixed exposure (mean x 67%) | +0.35 | +3.1 | 1.34 |
| Random timing | +0.33 (+0.23 to +0.43) | +1.1 (-3.3 to +6.9) | +1.49 (+1.14 to +2.34) |
| p: rotations at least as good | 0.009 | 0.680 | 0.081 |

Verdict by card 2's rule: **In between**.

Anchored clusters:

| # | First peak | Last trough | Non-US episodes | Mean depth | Mean I | Mean S | Mean N | Series |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | 1991-04-26 | 1991-11-11 | 1 | 47% | +64 | +1.00 | +36 | Indonesia |
| 2 | 1994-01-05 | 1995-04-19 | 7 | 39% | +17 | +0.37 | -4 | Brazil, Indonesia, Israel, Mexico |
| 3 | 1997-02-25 | 1999-02-05 | 15 | 42% | +43 | +0.68 | +1 | Brazil, Indonesia, Israel, Korea, Malaysia, Mexico, Taiwan |
| 4 | 1999-06-21 | 1999-09-27 | 1 | 28% | +0 | +0.00 | +0 | Indonesia |
| 5 | 2000-01-04 | 2003-02-13 | 24 | 38% | +27 | +0.51 | +5 | Brazil, India, Indonesia, Israel, Italy, Korea, Malaysia, Mexico, Taiwan |
| 6 | 2002-12-03 | 2003-03-17 | 1 | 30% | +24 | +0.68 | -10 | Korea |
| 7 | 2004-01-14 | 2004-05-17 | 2 | 27% | -0 | -0.00 | +0 | Brazil, India |
| 8 | 2006-05-10 | 2006-06-14 | 1 | 29% | +0 | +0.00 | +0 | India |
| 9 | 2007-05-18 | 2009-03-09 | 4 | 51% | +61 | +0.82 | +8 | India, Italy, Mexico, NewZealand |
| 10 | 2007-10-18 | 2008-12-29 | 7 | 54% | +57 | +0.72 | +5 | Brazil, Indonesia, Israel, Korea, Malaysia, Mexico, Taiwan |
| 11 | 2009-10-19 | 2011-12-20 | 6 | 31% | +14 | +0.36 | -5 | Brazil, India, Israel, Italy, Korea, Taiwan |
| 12 | 2012-03-13 | 2013-07-03 | 2 | 31% | +32 | +0.88 | +10 | Brazil, Italy |
| 13 | 2014-09-02 | 2016-06-27 | 4 | 32% | +18 | +0.51 | -6 | Brazil, Indonesia, Italy, Taiwan |
| 14 | 2017-07-25 | 2020-03-23 | 9 | 37% | +21 | +0.45 | -14 | Brazil, India, Israel, Italy, Korea, Malaysia, Mexico, NewZealand, Taiwan |
| 15 | 2018-02-19 | 2020-03-24 | 2 | 34% | +23 | +0.56 | -13 | Indonesia, Italy |
| 16 | 2021-06-07 | 2023-10-26 | 5 | 29% | +18 | +0.51 | -6 | Brazil, Israel, Italy, Korea, Taiwan |
| 17 | 2024-07-11 | 2025-04-09 | 1 | 29% | -0 | -0.00 | -11 | Taiwan |

### Developed ex US as one series (French, USD)

| Series | First decision | Sessions | Mean position | Episodes | Open fall (peak) | Sum I | Sum B | C | Premium P | Worst loss rule / hold |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| FF-DevExUS | 1991-06-24 | 8966 | 68% | 5 | - | +143 | -177 | -26 | 1.42 | 36% / 59% |
| **pooled** | | | | 5 | | +143 | -177 | -26 | **1.42** | |

Premium by era (episodes by peak, calm by date): before 2002 0.78 (1 episodes; rule minus holding +1.02 log pts per series-year); 2002-2025 1.75 (4 episodes; rule minus holding -2.98 log pts per series-year).

| Test | Clusters (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p | 90% range |
|---|---:|---:|---:|---:|---:|---|
| I, anchored on US falls | 5 | 5 | 0.031 | +28.6 | 0.000 | +12.6 to +46.2 |
| I, linked (strict) | 5 | 5 | 0.031 | +28.6 | 0.000 | +12.6 to +46.2 |
| N = I + B, anchored | 5 | 2 | 0.81 | -6.8 | 0.768 | -22.6 to +9.2 |
| N = I + B, linked | 5 | 2 | 0.81 | -6.8 | 0.768 | -22.6 to +9.2 |
| Share avoided S, anchored | 5 | 5 | 0.031 | +0.5 | 0.000 | +0.3 to +0.7 |

Episodes 5; anchored clusters (effective episodes) 5; linked 5. Verdict by card 1's rule: **Insurance real, handed back in the rebound**.

| Peak to trough | Episodes | Mean depth | Mean I | I > 0 | Mean S | Mean N | N > 0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast, <= 92 days | 1 | 34% | +9.8 | 1 | +0.24 | -37.5 | 0 |
| medium, 93-365 | 1 | 26% | +2.2 | 1 | +0.07 | -19.1 | 0 |
| slow, > 365 | 3 | 46% | +43.7 | 3 | +0.66 | +7.5 | 2 |

Sensitivity (anchored): 20% falls: 11 clusters, I > 0 in 11 of 11 (p 0.00049), mean N -3.3, premium 1.25; 40% falls: 2 clusters, I > 0 in 2 of 2 (p 0.25), mean N +16.3, premium 1.54.

Anchored clusters:

| # | First peak | Last trough | Non-US episodes | Mean depth | Mean I | Mean S | Mean N | Series |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | 2000-03-29 | 2003-03-12 | 1 | 49% | +48 | +0.72 | +23 | FF-DevExUS |
| 2 | 2007-10-31 | 2009-03-09 | 1 | 59% | +62 | +0.70 | +10 | FF-DevExUS |
| 3 | 2011-05-02 | 2011-10-04 | 1 | 26% | +2 | +0.07 | -19 | FF-DevExUS |
| 4 | 2020-01-20 | 2020-03-23 | 1 | 34% | +10 | +0.24 | -38 | FF-DevExUS |
| 5 | 2021-09-06 | 2022-10-12 | 1 | 30% | +21 | +0.57 | -10 | FF-DevExUS |

### Verdicts

| Set | Card 1 rule (insurance) | Card 2 rule (cheaper than holding less) |
|---|---|---|
| Primary, 13 developed (decides) | Insurance real, handed back in the rebound | Timing, not just exposure |
| French regions, total return | Insurance real, handed back in the rebound | In between |
| Wider set, 10 | Insurance real, handed back in the rebound | In between |
| Developed ex US, one series | Insurance real, handed back in the rebound | - |

