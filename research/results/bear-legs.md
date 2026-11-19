# bear-legs: multi-leg bear markets, and bear-market rally vs bottom

Card: `cards/bear-legs.md`. Written by `lib/bearlegs.py`. Descriptive, no pick, no `tries.md` rows. Episodes and clusters as insure-1 (US) and insure-2 (non-US); rules as fast-reentry-2's paper series. Rally = 10% / 10% zigzag inside a 25% fall's [peak, trough]; signals on daily closes (3-month = 91 days, 12-month = 365 days).

## Step 1: catalogue of multi-leg bears

### US: market + 10 industries, 1927-2025

Episodes 270 in 50 effective falls. Multi-leg (at least one 10% rally inside the fall): 200 of 270 episodes (74%); at 15%: 118; at 20%: 47. Rallies (10%): 427, mean legs per episode 2.58.

Rally size: median 14% (quartiles 12% - 17%, largest 29%); duration median 26 days (quartiles 9 - 56). Next leg after a rally top: median -28% to the fall's trough.

At the rally tops (all rallies inside falls, every series):

| | Share of rallies |
|---|---:|
| 3-month signal on at the top | 52% |
| 12-month signal on at the top | 32% |
| 3-month turned on during the rally with 12-month off | 33% |
| 12-month turned on during the rally | 17% |
| `tsmom12` out at the low, bought during the rally | 9% |
| `or3-12` out at the low, bought during the rally | 25% |
| `arm3-12` out at the low, bought during the rally | 26% |
| `tsmom12` holding at the top | 31% |
| `or3-12` holding at the top | 56% |
| `arm3-12` holding at the top | 55% |

Effective falls by the representative episode's 10% rallies (the US market's episode where the cluster has one, else the deepest). dI = rule minus `tsmom12`, cluster mean over member episodes, log pts (negative = less insurance):

| Rallies inside the fall | Falls | Mean depth | Mean days | `tsmom12` mean S | dI `or3-12` | dI `arm3-12` |
|---|---:|---:|---:|---:|---:|---:|
| 0 (one leg) | 10 | 30% | 149 | +0.65 | -7.2 | -6.6 |
| 1 | 20 | 32% | 264 | +0.38 | -5.3 | -4.3 |
| 2 or more | 20 | 43% | 496 | +0.54 | -8.4 | -7.1 |

Spearman correlation, representative rallies vs cluster dI `or3-12`: -0.11 (50 falls).

Spearman correlation, representative rallies vs cluster dI `arm3-12`: -0.09 (50 falls).

Episode level (all member episodes; not independent, description): the fall's own rallies against whether it is a follow-on leg (it began within 365 days of the same series' previous 25% trough, i.e. after a 25%+ bear-market rally):

| Episodes | Count | Clusters touched | `tsmom12` mean S | dI `or3-12` | dI `arm3-12` |
|---|---:|---:|---:|---:|---:|
| first leg, no 10% rally inside | 41 | 19 | +0.34 | -0.1 | -0.2 |
| first leg, 10% rallies inside | 112 | 30 | +0.50 | -5.2 | -3.8 |
| follow-on leg, no 10% rally inside | 29 | 12 | +0.81 | -8.1 | -7.7 |
| follow-on leg, 10% rallies inside | 88 | 25 | +0.69 | -12.4 | -11.3 |

Share of the summed episode dI of `or3-12` (-1913 log pts) in follow-on legs: 69%; in falls with 10% rallies inside: 88%.

Legs across episodes: 117 times a series began a new 25% fall within 365 days of a trough (the 25%+ rally that ended the episode was a bear-market rally in the wider sense); in 79 of them the new trough was below the old.

| # | Representative | Peak | Trough | Depth | Days | Rallies 10% / 15% / 20% | Largest rally (days) | Tops with 3m on / 12m on | `or3-12` / `arm3-12` / `tsmom12` bought | Episodes multi-leg | dI or / arm |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|
| 1 | Mkt | 1929-09-03 | 1929-11-13 | 44% | 71 | 1 / 1 / 0 | 18% (2) | 0 / 1 | 0 / 0 / 0 | 10 of 12 | -1 / +0 |
| 2 | Telcm | 1930-04-09 | 1932-07-09 | 67% | 822 | 5 / 4 / 1 | 21% (25) | 2 / 0 | 2 / 2 / 0 | 2 of 2 | -27 / -27 |
| 3 | Mkt | 1930-04-10 | 1930-12-16 | 44% | 250 | 1 / 0 / 0 | 12% (34) | 0 / 0 | 0 / 0 / 0 | 5 of 6 | -15 / -14 |
| 4 | Mkt | 1931-02-24 | 1931-06-02 | 32% | 98 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 4 of 6 | -22 / -20 |
| 5 | Mkt | 1931-06-27 | 1931-10-05 | 42% | 100 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 5 of 10 | -16 / -16 |
| 6 | Mkt | 1931-11-09 | 1932-07-08 | 57% | 242 | 4 / 2 / 0 | 19% (27) | 1 / 0 | 0 / 0 / 0 | 10 of 13 | -8 / -8 |
| 7 | Mkt | 1932-09-07 | 1933-02-27 | 36% | 173 | 4 / 2 / 0 | 17% (9) | 4 / 0 | 1 / 1 / 0 | 12 of 12 | -31 / -31 |
| 8 | Utils | 1933-06-12 | 1933-12-26 | 50% | 197 | 2 / 0 / 0 | 13% (28) | 1 / 1 | 0 / 0 / 0 | 2 of 2 | +1 / -0 |
| 9 | Mkt | 1933-07-18 | 1933-10-21 | 29% | 95 | 1 / 1 / 0 | 17% (35) | 1 / 1 | 0 / 0 / 0 | 6 of 7 | -0 / -0 |
| 10 | Mkt | 1934-02-05 | 1934-07-26 | 25% | 171 | 1 / 0 / 0 | 11% (35) | 0 / 1 | 0 / 0 / 0 | 7 of 7 | -4 / -2 |
| 11 | Mkt | 1937-03-10 | 1938-03-31 | 51% | 386 | 4 / 1 / 0 | 17% (48) | 2 / 1 | 1 / 1 / 0 | 12 of 15 | -8 / -8 |
| 12 | Durbl | 1938-11-09 | 1939-04-08 | 31% | 150 | 1 / 1 / 1 | 23% (43) | 1 / 1 | 0 / 0 / 0 | 5 of 5 | -4 / -4 |
| 13 | Mkt | 1940-04-08 | 1940-06-10 | 26% | 63 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 0 of 7 | -1 / -1 |
| 14 | Mkt | 1940-11-09 | 1942-04-28 | 26% | 535 | 1 / 0 / 0 | 15% (139) | 1 / 1 | 1 / 1 / 1 | 9 of 10 | -6 / -3 |
| 15 | Mkt | 1946-05-29 | 1947-05-17 | 28% | 353 | 1 / 0 / 0 | 14% (78) | 1 / 0 | 1 / 1 / 0 | 6 of 6 | -5 / -5 |
| 16 | Hlth | 1946-05-10 | 1948-03-16 | 38% | 676 | 2 / 1 / 0 | 17% (68) | 2 / 1 | 1 / 1 / 0 | 3 of 3 | -7 / -7 |
| 17 | Enrgy | 1948-06-15 | 1949-06-13 | 27% | 363 | 2 / 0 / 0 | 13% (26) | 2 / 1 | 0 / 0 / 0 | 1 of 1 | -6 / -6 |
| 18 | Hlth | 1951-08-02 | 1953-06-10 | 27% | 678 | 1 / 0 / 0 | 12% (66) | 1 / 1 | 0 / 0 / 0 | 1 of 1 | -7 / -7 |
| 19 | Durbl | 1955-11-14 | 1957-12-30 | 30% | 777 | 3 / 2 / 0 | 20% (140) | 3 / 3 | 1 / 1 / 1 | 3 of 3 | -1 / +1 |
| 20 | Enrgy | 1959-01-23 | 1960-06-01 | 27% | 495 | 1 / 0 / 0 | 10% (75) | 1 / 0 | 1 / 1 / 0 | 2 of 2 | -8 / -8 |
| 21 | Mkt | 1961-12-12 | 1962-06-26 | 28% | 196 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 1 of 4 | +0 / -0 |
| 22 | Hlth | 1961-11-14 | 1962-10-23 | 40% | 343 | 1 / 0 / 0 | 14% (20) | 0 / 0 | 0 / 0 / 0 | 3 of 4 | -3 / -3 |
| 23 | HiTec | 1968-06-11 | 1970-08-13 | 46% | 793 | 3 / 2 / 0 | 21% (90) | 2 / 2 | 1 / 1 / 1 | 3 of 5 | +1 / +1 |
| 24 | Mkt | 1968-11-29 | 1970-05-26 | 37% | 543 | 1 / 0 / 0 | 13% (104) | 1 / 0 | 1 / 1 / 0 | 8 of 9 | -6 / -4 |
| 25 | Mkt | 1973-01-11 | 1974-10-03 | 48% | 630 | 2 / 0 / 0 | 14% (98) | 2 / 1 | 2 / 2 / 1 | 8 of 8 | -10 / -5 |
| 26 | Durbl | 1973-01-05 | 1974-12-23 | 58% | 717 | 5 / 1 / 0 | 17% (95) | 2 / 0 | 2 / 2 / 0 | 2 of 2 | -5 / -5 |
| 27 | Hlth | 1975-06-02 | 1977-05-31 | 28% | 729 | 2 / 1 / 1 | 21% (141) | 2 / 2 | 1 / 1 / 1 | 1 of 1 | +0 / +4 |
| 28 | Durbl | 1979-10-05 | 1980-04-21 | 25% | 199 | 1 / 1 / 0 | 17% (71) | 1 / 1 | 0 / 0 / 0 | 1 of 1 | -0 / -0 |
| 29 | Enrgy | 1981-08-11 | 1982-08-12 | 42% | 366 | 2 / 2 / 2 | 22% (66) | 2 / 0 | 1 / 1 / 0 | 4 of 5 | -13 / -10 |
| 30 | HiTec | 1983-06-24 | 1984-07-24 | 29% | 396 | 1 / 0 / 0 | 10% (46) | 0 / 1 | 0 / 0 / 0 | 1 of 1 | -8 / -8 |
| 31 | Mkt | 1987-08-25 | 1987-12-04 | 33% | 101 | 1 / 0 / 0 | 12% (7) | 0 / 1 | 0 / 0 / 0 | 5 of 10 | -0 / -0 |
| 32 | Other | 1989-10-09 | 1990-10-17 | 37% | 373 | 1 / 0 / 0 | 13% (39) | 1 / 1 | 0 / 0 / 0 | 3 of 6 | -3 / -0 |
| 33 | Hlth | 1992-01-09 | 1993-08-13 | 35% | 582 | 4 / 1 / 0 | 16% (60) | 3 / 1 | 1 / 1 / 1 | 1 of 1 | -19 / -9 |
| 34 | Durbl | 1994-02-03 | 1994-12-12 | 28% | 312 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 0 of 1 | +0 / +0 |
| 35 | Other | 1998-07-14 | 1998-10-08 | 33% | 86 | 1 / 0 / 0 | 12% (13) | 0 / 1 | 1 / 1 / 1 | 2 of 5 | +0 / +0 |
| 36 | NoDur | 1998-11-23 | 2000-03-14 | 29% | 477 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 0 of 1 | -6 / -7 |
| 37 | Mkt | 2000-03-24 | 2002-10-09 | 49% | 929 | 5 / 4 / 2 | 24% (179) | 3 / 2 | 1 / 1 / 1 | 14 of 22 | -4 / -4 |
| 38 | Telcm | 2003-01-06 | 2003-03-11 | 26% | 64 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 0 of 1 | -16 / -16 |
| 39 | Mkt | 2007-10-09 | 2008-11-20 | 51% | 408 | 3 / 1 / 0 | 19% (8) | 1 / 0 | 1 / 1 / 0 | 8 of 8 | -9 / -7 |
| 40 | Mkt | 2009-01-06 | 2009-03-09 | 27% | 62 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 5 of 9 | -8 / -6 |
| 41 | Durbl | 2010-04-26 | 2010-07-06 | 25% | 71 | 1 / 0 / 0 | 10% (5) | 1 / 1 | 0 / 0 / 0 | 1 of 1 | +0 / +0 |
| 42 | Durbl | 2011-01-27 | 2011-10-03 | 40% | 249 | 4 / 0 / 0 | 13% (24) | 1 / 4 | 1 / 1 / 1 | 4 of 4 | +0 / +0 |
| 43 | Enrgy | 2014-06-23 | 2015-08-25 | 43% | 428 | 2 / 0 / 0 | 14% (135) | 1 / 1 | 1 / 1 / 0 | 2 of 3 | -15 / -15 |
| 44 | Enrgy | 2018-10-03 | 2018-12-24 | 32% | 82 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 1 of 2 | -2 / -0 |
| 45 | Mkt | 2020-02-19 | 2020-03-23 | 34% | 33 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 4 of 11 | -1 / -0 |
| 46 | Enrgy | 2020-06-08 | 2020-10-28 | 40% | 142 | 1 / 0 / 0 | 12% (34) | 1 / 0 | 0 / 0 / 0 | 1 of 1 | -28 / -28 |
| 47 | Mkt | 2021-11-08 | 2022-10-14 | 26% | 340 | 2 / 1 / 0 | 19% (61) | 1 / 1 | 1 / 1 / 0 | 9 of 10 | -6 / -5 |
| 48 | Durbl | 2023-07-18 | 2023-10-30 | 29% | 104 | 1 / 1 / 0 | 20% (27) | 1 / 0 | 0 / 0 / 0 | 1 of 1 | -9 / -0 |
| 49 | Durbl | 2023-12-27 | 2024-04-22 | 31% | 117 | 1 / 0 / 0 | 10% (36) | 0 / 1 | 0 / 0 / 0 | 1 of 1 | +0 / +0 |
| 50 | Durbl | 2024-12-17 | 2025-04-08 | 48% | 112 | 2 / 1 / 1 | 21% (15) | 1 / 2 | 0 / 0 / 0 | 1 of 2 | +0 / +0 |

### Non-US: 13 developed price indices

Episodes 109 in 19 effective falls. Multi-leg (at least one 10% rally inside the fall): 79 of 109 episodes (72%); at 15%: 54; at 20%: 28. Rallies (10%): 187, mean legs per episode 2.72.

Rally size: median 15% (quartiles 12% - 18%, largest 26%); duration median 38 days (quartiles 17 - 63). Next leg after a rally top: median -31% to the fall's trough.

At the rally tops (all rallies inside falls, every series):

| | Share of rallies |
|---|---:|
| 3-month signal on at the top | 42% |
| 12-month signal on at the top | 31% |
| 3-month turned on during the rally with 12-month off | 36% |
| 12-month turned on during the rally | 22% |
| `tsmom12` out at the low, bought during the rally | 15% |
| `or3-12` out at the low, bought during the rally | 29% |
| `arm3-12` out at the low, bought during the rally | 30% |
| `tsmom12` holding at the top | 29% |
| `or3-12` holding at the top | 47% |
| `arm3-12` holding at the top | 44% |

Effective falls by the representative episode's 10% rallies (the US market's episode where the cluster has one, else the deepest). dI = rule minus `tsmom12`, cluster mean over member episodes, log pts (negative = less insurance):

| Rallies inside the fall | Falls | Mean depth | Mean days | `tsmom12` mean S | dI `or3-12` | dI `arm3-12` |
|---|---:|---:|---:|---:|---:|---:|
| 0 (one leg) | 4 | 34% | 93 | +0.06 | +0.0 | +0.0 |
| 1 | 2 | 42% | 283 | +0.47 | -4.0 | -3.2 |
| 2 or more | 13 | 51% | 578 | +0.63 | -6.0 | -5.3 |

Spearman correlation, representative rallies vs cluster dI `or3-12`: -0.75 (19 falls).

Spearman correlation, representative rallies vs cluster dI `arm3-12`: -0.62 (19 falls).

Episode level (all member episodes; not independent, description): the fall's own rallies against whether it is a follow-on leg (it began within 365 days of the same series' previous 25% trough, i.e. after a 25%+ bear-market rally):

| Episodes | Count | Clusters touched | `tsmom12` mean S | dI `or3-12` | dI `arm3-12` |
|---|---:|---:|---:|---:|---:|
| first leg, no 10% rally inside | 26 | 9 | +0.31 | -0.1 | -0.1 |
| first leg, 10% rallies inside | 54 | 14 | +0.57 | -6.3 | -5.3 |
| follow-on leg, no 10% rally inside | 4 | 3 | +1.00 | -4.4 | -4.4 |
| follow-on leg, 10% rallies inside | 25 | 10 | +0.80 | -8.9 | -7.9 |

Share of the summed episode dI of `or3-12` (-584 log pts) in follow-on legs: 41%; in falls with 10% rallies inside: 96%.

Legs across episodes: 29 times a series began a new 25% fall within 365 days of a trough (the 25%+ rally that ended the episode was a bear-market rally in the wider sense); in 26 of them the new trough was below the old.

| # | Representative | Peak | Trough | Depth | Days | Rallies 10% / 15% / 20% | Largest rally (days) | Tops with 3m on / 12m on | `or3-12` / `arm3-12` / `tsmom12` bought | Episodes multi-leg | dI or / arm |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|
| 1 | Japan | 1973-01-24 | 1974-10-09 | 37% | 623 | 3 / 2 / 1 | 21% (170) | 3 / 3 | 1 / 1 / 1 | 1 of 1 | -1 / +1 |
| 2 | Canada | 1980-11-28 | 1982-07-08 | 44% | 587 | 2 / 0 / 0 | 11% (146) | 1 / 1 | 0 / 0 / 0 | 1 of 1 | -3 / -3 |
| 3 | Australia | 1987-09-21 | 1987-11-11 | 50% | 51 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 0 of 3 | +0 / +0 |
| 4 | HongKong | 1989-05-15 | 1989-06-05 | 37% | 21 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 0 of 1 | -0 / -0 |
| 5 | Japan | 1989-12-29 | 1990-10-01 | 48% | 276 | 1 / 1 / 0 | 19% (66) | 0 / 0 | 0 / 0 / 0 | 4 of 5 | -4 / -2 |
| 6 | Japan | 1991-03-18 | 1992-08-18 | 47% | 519 | 3 / 1 / 0 | 18% (73) | 1 / 1 | 1 / 1 / 1 | 1 of 1 | -9 / -6 |
| 7 | HongKong | 1994-01-04 | 1995-01-23 | 43% | 384 | 4 / 2 / 1 | 21% (58) | 2 / 4 | 0 / 0 / 0 | 4 of 4 | -5 / -4 |
| 8 | Singapore | 1996-02-06 | 1998-01-12 | 57% | 706 | 2 / 1 / 0 | 17% (41) | 1 / 0 | 1 / 1 / 1 | 5 of 14 | -3 / -3 |
| 9 | UK | 1999-12-30 | 2003-03-12 | 53% | 1168 | 6 / 2 / 1 | 21% (76) | 2 / 2 | 2 / 2 / 1 | 3 of 4 | -10 / -10 |
| 10 | Netherlands | 2002-03-28 | 2003-03-12 | 59% | 349 | 3 / 2 / 2 | 24% (51) | 0 / 0 | 1 / 1 / 0 | 18 of 20 | -8 / -6 |
| 11 | Belgium | 2007-05-23 | 2009-03-06 | 68% | 653 | 5 / 1 / 1 | 20% (8) | 1 / 1 | 1 / 1 / 0 | 12 of 12 | -13 / -13 |
| 12 | HongKong | 2007-10-30 | 2008-10-27 | 65% | 363 | 5 / 2 / 1 | 25% (50) | 2 / 3 | 0 / 0 / 0 | 5 of 6 | -5 / -5 |
| 13 | Spain | 2011-02-17 | 2012-07-24 | 46% | 523 | 3 / 3 / 1 | 21% (45) | 1 / 0 | 0 / 0 / 0 | 7 of 10 | -2 / -1 |
| 14 | Austria | 2014-01-15 | 2014-10-16 | 26% | 274 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 0 of 1 | +0 / +0 |
| 15 | HongKong | 2015-04-28 | 2016-02-12 | 36% | 290 | 1 / 0 / 0 | 13% (24) | 0 / 0 | 1 / 1 / 1 | 7 of 7 | -4 / -4 |
| 16 | Austria | 2018-01-23 | 2020-03-18 | 56% | 785 | 2 / 1 / 1 | 23% (112) | 2 / 1 | 2 / 2 / 1 | 6 of 13 | -0 / +1 |
| 17 | HongKong | 2021-02-17 | 2022-10-31 | 53% | 621 | 2 / 1 / 1 | 22% (20) | 1 / 0 | 1 / 1 / 0 | 3 of 3 | -10 / -8 |
| 18 | Austria | 2022-02-09 | 2022-09-29 | 35% | 232 | 3 / 1 / 0 | 17% (15) | 1 / 1 | 1 / 1 / 1 | 2 of 2 | -10 / -10 |
| 19 | Japan | 2024-07-11 | 2024-08-05 | 25% | 25 | 0 / 0 / 0 |  | 0 / 0 | 0 / 0 / 0 | 0 of 1 | +0 / +0 |
