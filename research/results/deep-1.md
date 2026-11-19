# deep-1, Part B: three combination rules

Card and pass bar: `deep-1.md`. Twin: `tsmom12`. Train period, total-return prices, gym costs. The sleeves are the 29 pool models of the card; every choice is made by the rule from past returns, refitted each first Friday of January.

## The six live assets, 1994-2025

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| stack | 1.01 (0.18) | +12.4% | 12.4% | 30.9% | 1.2 | 75% | 1.34 | 0.14 | 1.53 | 1.83 | 0.50 | -0.04 (p=0.64; -0.23..+0.14) | 1/5 |
| switch | 1.02 (0.18) | +14.9% | 14.7% | 34.7% | 3.2 | 65% | 1.24 | 0.61 | 1.59 | 1.43 | -0.32 | -0.03 (p=0.61; -0.21..+0.17) | 2/5 |
| meta | 1.08 (0.18) | +14.7% | 13.5% | 32.3% | 2.3 | 74% | 1.39 | 0.16 | 1.70 | 1.63 | 0.74 | +0.03 (p=0.27; -0.06..+0.12) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| stack | -30% | -4% | -17% | -24% | -5% | -4% | -21% |
| switch | -2% | +6% | +1% | -9% | -6% | -26% | -16% |
| meta | -32% | -3% | -15% | -20% | -0% | -24% | -25% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## Since 2003 (the review's window)

| Variant | Sharpe | CAGR | Max DD | vs tsmom12 (p) | vs equal weight (p) |
|---|---:|---:|---:|---:|---:|
| stack | 1.22 | +14.8% | 25.8% | +0.02 (0.42) | +0.03 (0.42) |
| switch | 1.05 | +15.9% | 34.7% | -0.14 (0.86) | -0.14 (0.81) |
| meta | 1.27 | +17.2% | 29.1% | +0.08 (0.11) | +0.08 (0.17) |
| tsmom12 | 1.20 | +20.7% | 36.5% | - | +0.00 (0.49) |
| equal-weight | 1.19 | +24.9% | 47.0% | -0.00 (0.51) | - |

## How far each book is from `tsmom12`

- `stack`: on average 21.2% of the book is held differently from `tsmom12`; average invested 75% (`tsmom12` 76%).
- `switch`: on average 9.6% of the book is held differently from `tsmom12`; average invested 65% (`tsmom12` 76%).
- `meta`: on average 9.2% of the book is held differently from `tsmom12`; average invested 74% (`tsmom12` 76%).

Best single pool model with hindsight: `curve-and`, Sharpe 1.13 over its own span (`tsmom12` 1.05).

## What each refit chose (six assets)

| Refit | `stack`: complement (share of `tsmom12`) | `switch`: off / mixed / on | `meta`: largest shares (lambda) |
|---|---|---|---|
| 1995-01-06 | none | tsmom12 / tsmom12 / tsmom12 | tsmom12 100% (-) |
| 1996-01-05 | none | tsmom12 / tsmom12 / tsmom12 | tsmom12 100% (-) |
| 1997-01-03 | fracdiff (41%) | tsmom12 / tsmom12 / fracdiff | fracdiff 31%, meta-gbm 8%, vol-calm 7%, equal-weight 7% (0.1) |
| 1998-01-02 | vol-calm (33%) | tsmom12 / tsmom12 / fracdiff | fracdiff 13%, vol-calm 12%, kelly 7%, equal-weight 6% (1) |
| 1999-01-01 | vol-calm (18%) | tsmom12 / tsmom12 / hawkes | hawkes 6%, hmm 6%, curve-and 5%, vol-target 5% (10) |
| 2000-01-07 | vol-calm (1%) | tsmom12 / tsmom12 / curve-and | hmm 11%, vol-calm 10%, curve-and 10%, hawkes 7% (1) |
| 2001-01-05 | hike-and (23%) | tsmom12 / tsmom12 / curve-and | curve-and 13%, sixty-forty 13%, inverse-vol 9%, hike-and 9% (0.1) |
| 2002-01-04 | hike-and (11%) | tsmom12 / tsmom12 / curve-and | curve-and 17%, hike-and 13%, fracdiff 9%, spread-and 8% (1) |
| 2003-01-03 | hike-and (0%) | gbm-pool / tsmom12 / curve-and | curve-and 17%, hike-and 12%, fracdiff 10%, trend-vol 9% (1) |
| 2004-01-02 | hike-and (50%) | sma200 / tsmom12 / curve-and | curve-and 16%, hike-and 13%, spread-and 9%, trend-vol 8% (1) |
| 2005-01-07 | hike-and (45%) | sma200 / tsmom12 / curve-and | curve-and 10%, spread-and 7%, hike-and 7%, trend-vol 7% (10) |
| 2006-01-06 | hike-and (39%) | sma200 / tsmom12 / curve-and | sixty-forty 17%, curve-and 14%, hike-and 10%, inverse-vol 9% (0.1) |
| 2007-01-05 | hike-and (33%) | sma200 / tsmom12 / curve-and | sixty-forty 19%, curve-and 14%, meta-gbm 11%, hike-and 10% (0.1) |
| 2008-01-04 | hike-and (38%) | sma200 / tsmom12 / absorption | curve-and 9%, hike-and 7%, spread-and 7%, trend-vol 6% (10) |
| 2009-01-02 | hike-and (46%) | curve-and / tsmom12 / absorption | curve-and 9%, spread-and 7%, hike-and 7%, trend-vol 6% (10) |
| 2010-01-01 | hike-and (50%) | sma200 / tsmom12 / absorption | curve-and 8%, spread-and 7%, hike-and 6%, trend-vol 6% (10) |
| 2011-01-07 | hike-and (50%) | sma200 / tsmom12 / absorption | curve-and 8%, hike-and 6%, spread-and 6%, trend-vol 6% (10) |
| 2012-01-06 | hike-and (50%) | sma200 / tsmom12 / absorption | curve-and 8%, hike-and 6%, spread-and 6%, trend-vol 6% (10) |
| 2013-01-04 | hike-and (50%) | sma200 / tsmom12 / absorption | curve-and 8%, hike-and 6%, spread-and 6%, trend-vol 5% (10) |
| 2014-01-03 | hike-and (50%) | sma200 / tsmom12 / absorption | curve-and 17%, sixty-forty 14%, hike-and 12%, trend-vol 11% (0.1) |
| 2015-01-02 | sixty-forty (8%) | sma200 / real-and / absorption | sixty-forty 15%, curve-and 14%, hike-and 10%, inverse-vol 10% (0.1) |
| 2016-01-01 | sixty-forty (12%) | sma200 / hmm / absorption | curve-and 8%, hike-and 7%, spread-and 6%, tsmom12 5% (10) |
| 2017-01-06 | sixty-forty (34%) | sma200 / hmm / absorption | curve-and 7%, hike-and 6%, spread-and 6%, tsmom12 5% (10) |
| 2018-01-05 | sixty-forty (14%) | sma200 / hmm / absorption | curve-and 7%, spread-and 6%, hike-and 5%, tsmom12 5% (10) |
| 2019-01-04 | sixty-forty (11%) | sma200 / real-and / absorption | curve-and 7%, spread-and 6%, hike-and 6%, tsmom12 5% (10) |
| 2020-01-03 | sixty-forty (10%) | sma200 / hmm / curve-and | curve-and 7%, hike-and 5%, spread-and 5%, ensemble 5% (10) |
| 2021-01-01 | sixty-forty (23%) | sma200 / hmm / curve-and | curve-and 7%, hike-and 5%, ensemble 5%, sma200 4% (10) |
| 2022-01-07 | sixty-forty (17%) | sma200 / hmm / curve-and | curve-and 6%, hike-and 5%, ensemble 5%, trend-safe 4% (10) |
| 2023-01-06 | sixty-forty (25%) | sma200 / hmm / curve-and | curve-and 7%, hike-and 5%, tsmom12 5%, ensemble 5% (10) |
| 2024-01-05 | sixty-forty (28%) | sma200 / hmm / curve-and | curve-and 6%, hike-and 5%, tsmom12 5%, ensemble 5% (10) |
| 2025-01-03 | sixty-forty (45%) | sma200 / hmm / absorption | curve-and 14%, hike-and 10%, sixty-forty 8%, ensemble 7% (1) |

## Out of universe: 8 other ETFs, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| stack@etf | 0.52 (0.20) | +4.3% | 8.8% | 17.3% | 3.9 | 69% | 0.77 | 0.37 | 0.44 | 0.36 | -0.07 (p=0.92; -0.17..+0.02) | 0/4 |
| switch@etf | 0.56 (0.20) | +3.9% | 7.3% | 16.8% | 6.0 | 68% | 0.72 | 0.63 | 0.33 | 0.37 | -0.04 (p=0.66; -0.19..+0.12) | 1/4 |
| meta@etf | 0.59 (0.20) | +4.4% | 7.9% | 16.7% | 2.1 | 68% | 0.74 | 0.40 | 0.67 | 0.50 | -0.01 (p=0.56; -0.11..+0.09) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

Sleeves: 28 complements. Distance from `tsmom12`: `stack` 5.9%, `switch` 16.1%, `meta` 10.0%.

## Out of universe: 6 other coins, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| stack@coin | 0.44 (0.34) | +6.4% | 73.3% | 92.4% | 7.5 | 51% | 0.58 | 0.16 | -0.10 (p=0.94; -0.21..+0.00) | 0/2 |
| switch@coin | 0.54 (0.34) | +13.9% | 76.4% | 92.4% | 5.6 | 52% | 0.64 | 0.42 | +0.00 (p=0.47; -0.06..+0.07) | 1/2 |
| meta@coin | 0.59 (0.34) | +18.7% | 74.3% | 91.9% | 3.9 | 63% | 0.72 | 0.39 | +0.05 (p=0.26; -0.08..+0.18) | 1/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

Sleeves: 28 complements. Distance from `tsmom12`: `stack` 5.2%, `switch` 4.0%, `meta` 12.5%.

## Out of universe: 4 indexes as one portfolio, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| stack@idx | 0.73 (0.13) | +5.0% | 7.0% | 24.0% | 2.2 | 52% | 0.81 | 1.19 | 1.02 | 0.40 | 0.38 | 0.26 | 0.75 | +0.01 (p=0.47; -0.10..+0.12) | 3/7 |
| switch@idx | 0.63 (0.13) | +4.6% | 7.5% | 22.9% | 3.7 | 55% | 0.68 | 1.06 | 0.94 | 0.18 | 0.31 | 0.52 | 0.76 | -0.09 (p=0.82; -0.26..+0.07) | 2/7 |
| meta@idx | 0.75 (0.13) | +5.4% | 7.4% | 23.3% | 3.0 | 65% | 0.82 | 1.14 | 1.14 | 0.30 | 0.37 | 0.46 | 0.81 | +0.03 (p=0.24; -0.04..+0.11) | 6/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.7% | 2.3 | 70% | 0.76 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| equal-weight@idx | 0.62 (0.13) | +7.5% | 13.1% | 57.6% | 0.2 | 100% | 0.71 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | -0.10 (p=0.84; -0.27..+0.07) | 5/7 |

Sleeves: 28 complements. Distance from `tsmom12`: `stack` 9.5%, `switch` 12.8%, `meta` 10.6%.

## After the test: two reference points (not part of the card)

`naive-1n` is the plain twin of `meta`, added after `meta`'s result was seen and logged as a baseline: equal shares in `tsmom12` and every eligible complement, no learning. It tells how much of `meta` is plain averaging.

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| naive-1n | 1.06 (0.18) | +14.5% | 13.7% | 39.7% | 2.5 | 75% | 1.40 | 0.14 | 1.65 | 1.67 | 0.76 | +0.01 (p=0.41; -0.09..+0.12) | 3/5 |
| meta | 1.08 (0.18) | +14.7% | 13.5% | 32.3% | 2.3 | 74% | 1.39 | 0.16 | 1.70 | 1.63 | 0.74 | +0.03 (p=0.27; -0.06..+0.12) | 3/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |

| Variant | Sharpe | CAGR | Max DD | vs tsmom12 (p) | vs equal weight (p) |
|---|---:|---:|---:|---:|---:|
| naive-1n | 1.29 | +17.3% | 30.2% | +0.09 (0.11) | +0.10 (0.08) |
| meta | 1.27 | +17.2% | 29.1% | +0.08 (0.11) | +0.08 (0.17) |
| tsmom12 | 1.20 | +20.7% | 36.5% | - | +0.00 (0.49) |
| equal-weight | 1.19 | +24.9% | 47.0% | -0.00 (0.51) | - |

`meta` against `naive-1n`: +0.02 Sharpe (p = 0.23).

The hindsight ceiling is no strategy: the best constant long-only mix of the sleeves, fitted on the very days it is scored on, sleeve returns mixed as they are. No rule that picks among these sleeves from past data can be expected to do better.

| Days | Best mix with hindsight | `tsmom12` | Shares |
|---|---:|---:|---|
| 1994-2025 | 1.22 | 1.05 | curve-and 52%, hike-and 20%, inverse-vol 20%, trend-vol 4%, ensemble 3% |
| 2003-2025 | 1.49 | 1.20 | kelly 62%, curve-and 22%, dd-control 17% |

## Pass bar

### `stack`

- FAIL: 1. Sharpe beats `tsmom12` with p < 0.033 (difference -0.04, p = 0.64)
- FAIL: 2. Ahead of `tsmom12` in at least 4 of 5 eras (1 of 5)
- PASS: 3. Max drawdown not more than 5 points worse (30.9% vs 36.5%)
- FAIL: 4. Ahead of `tsmom12` out of universe in at least 2 of 3 sets (etf -0.07, coin -0.10, idx +0.01)
- PASS: 5. Beats equal weight on Sharpe (1.01 vs 0.88)
- PASS: 6. Since 2003 not behind `tsmom12` nor equal weight (1.22 vs 1.20 and 1.19)

**`stack` FAILS train.**

### `switch`

- FAIL: 1. Sharpe beats `tsmom12` with p < 0.033 (difference -0.03, p = 0.61)
- FAIL: 2. Ahead of `tsmom12` in at least 4 of 5 eras (2 of 5)
- PASS: 3. Max drawdown not more than 5 points worse (34.7% vs 36.5%)
- FAIL: 4. Ahead of `tsmom12` out of universe in at least 2 of 3 sets (etf -0.04, coin +0.00, idx -0.09)
- PASS: 5. Beats equal weight on Sharpe (1.02 vs 0.88)
- FAIL: 6. Since 2003 not behind `tsmom12` nor equal weight (1.05 vs 1.20 and 1.19)

**`switch` FAILS train.**

### `meta`

- FAIL: 1. Sharpe beats `tsmom12` with p < 0.033 (difference +0.03, p = 0.27)
- FAIL: 2. Ahead of `tsmom12` in at least 4 of 5 eras (3 of 5)
- PASS: 3. Max drawdown not more than 5 points worse (32.3% vs 36.5%)
- PASS: 4. Ahead of `tsmom12` out of universe in at least 2 of 3 sets (etf -0.01, coin +0.05, idx +0.03)
- PASS: 5. Beats equal weight on Sharpe (1.08 vs 0.88)
- PASS: 6. Since 2003 not behind `tsmom12` nor equal weight (1.27 vs 1.20 and 1.19)

**`meta` FAILS train.**
