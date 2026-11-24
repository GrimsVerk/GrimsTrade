# turbulence-1: turbulence vs a matched volatility trigger on `tsmom12`

Card: `cards/turbulence.md`. Write-up: `turbulence-1.md`. Fast-crash dates (S&P 500 index close, peak -> trough): 1987 1987-08-25..1987-12-04, 1998 1998-07-17..1998-08-31, 2011 2011-04-29..2011-10-03, 2015 2015-07-20..2015-08-25, 2018-Q4 2018-09-20..2018-12-24, 2020 2020-02-19..2020-03-23.

## six assets (primary), 1994-02-01..2025-11-09

Assets in the signal on the test's days: 1 on 19%, 2-3 on 18%, 4+ on 63% (0 on 0%). Correlation of log T, log M, log C: T-M 0.96, T-C -0.09, M-C -0.38.

| Rule | Signal, percentile | Trigger on (share of days) | Cuts `tsmom12` (share) |
|---|---|---:|---:|
| turb | T, 90 | 10.1% | 8.5% |
| corr | C, 90 | 7.8% | 6.7% |
| mag | M, 90 | 10.4% | 8.5% |
| mag-match | M, 90.141 | 10.1% | 8.3% |
| mag-match-c | M, 92.447 | 7.9% | 6.3% |
| turb-q75 | T, 75 | 24.8% | 21.5% |
| mag-match-q75 | M, 74.916 | 24.8% | 21.1% |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| turb | 0.95 (0.18) | +14.1% | 15.1% | 40.6% | 8.8 | 70% | 1.12 | -0.06 | 1.34 | 1.76 | 0.76 | -0.09 (p=0.86; -0.23..+0.06) | 1/5 |
| corr | 0.97 (0.18) | +15.8% | 16.5% | 31.4% | 11.5 | 72% | 1.34 | 0.15 | 1.37 | 1.34 | 0.90 | -0.07 (p=0.93; -0.16..+0.01) | 1/5 |
| mag | 1.00 (0.18) | +14.9% | 15.1% | 45.0% | 8.5 | 71% | 1.12 | -0.05 | 1.40 | 1.86 | 0.81 | -0.05 (p=0.72; -0.19..+0.10) | 1/5 |
| mag-match | 0.99 (0.18) | +14.9% | 15.1% | 45.0% | 8.4 | 71% | 1.13 | -0.05 | 1.42 | 1.83 | 0.80 | -0.05 (p=0.73; -0.19..+0.10) | 1/5 |
| mag-match-c | 1.05 (0.18) | +16.1% | 15.4% | 38.9% | 6.6 | 72% | 1.20 | 0.02 | 1.50 | 1.76 | 0.98 | +0.00 (p=0.51; -0.12..+0.14) | 2/5 |
| turb-q75 | 0.89 (0.18) | +11.5% | 13.3% | 47.0% | 13.9 | 62% | 1.15 | -0.18 | 1.08 | 1.66 | 0.95 | -0.16 (p=0.90; -0.35..+0.04) | 2/5 |
| mag-match-q75 | 0.90 (0.18) | +11.8% | 13.4% | 48.7% | 15.4 | 62% | 1.15 | -0.17 | 1.15 | 1.58 | 1.02 | -0.14 (p=0.91; -0.33..+0.04) | 2/5 |
| tsmom12 | 1.04 (0.18) | +17.8% | 17.1% | 37.4% | 2.8 | 76% | 1.34 | 0.19 | 1.54 | 1.49 | 0.89 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.5 | 100% | 1.35 | 0.02 | 1.65 | 1.53 | 0.66 | -0.17 (p=0.92; -0.36..+0.02) | 3/5 |

Paired comparisons (stationary bootstrap, block 20, 2,000 draws, seed 0):

| Pair | dSharpe | p (one-sided) | z |
|---|---:|---:|---:|
| turb - mag-match | -0.042 | 0.84 | -1.01 |
| corr - mag-match-c | -0.074 | 0.78 | -0.76 |
| turb - mag | -0.045 | 0.86 | -1.10 |
| turb - tsmom12 | -0.094 | 0.86 | -1.09 |
| corr - tsmom12 | -0.073 | 0.93 | -1.43 |
| mag-match - tsmom12 | -0.052 | 0.73 | -0.58 |
| mag - tsmom12 | -0.049 | 0.72 | -0.55 |
| turb-q75 - mag-match-q75 | -0.012 | 0.59 | -0.25 |
| turb-q75 - tsmom12 | -0.156 | 0.90 | -1.29 |

Slow stress windows (total return inside each):

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| turb | -31% | -6% | -2% | -13% | -17% | -17% | -17% |
| corr | -27% | -3% | -21% | -13% | -6% | -26% | -20% |
| mag | -36% | -1% | +1% | -16% | -17% | -20% | -22% |
| mag-match | -36% | -1% | +1% | -17% | -16% | -20% | -23% |
| mag-match-c | -32% | -2% | +1% | -11% | -13% | -22% | -17% |
| turb-q75 | -39% | +4% | +1% | -13% | -9% | -18% | -16% |
| mag-match-q75 | -41% | +3% | +1% | -8% | -7% | -24% | -14% |
| tsmom12 | -28% | -4% | -22% | -14% | -6% | -23% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -43% | -43% |

Fast crashes (S&P 500 index peak -> trough, then 91 days):

| Rule | 1987 fall / rebound | 1998 fall / rebound | 2011 fall / rebound | 2015 fall / rebound | 2018-Q4 fall / rebound | 2020 fall / rebound |
|---|---:|---:|---:|---:|---:|---:|
| turb | - | -12.2% / +11.6% | -0.4% / +1.0% | -4.9% / +1.1% | -6.7% / +2.2% | -2.1% / +19.3% |
| corr | - | -19.0% / +21.4% | +0.2% / +2.3% | -3.0% / +3.4% | -6.3% / +2.2% | -20.6% / +17.8% |
| mag | - | -12.2% / +11.6% | +0.0% / +0.8% | -1.4% / +2.4% | -7.5% / +2.2% | +0.8% / +19.0% |
| mag-match | - | -12.2% / +11.6% | +0.0% / +0.6% | -1.4% / +2.4% | -7.5% / +2.2% | +0.8% / +19.0% |
| mag-match-c | - | -12.9% / +11.2% | +2.7% / +0.9% | -4.9% / +2.5% | -9.4% / +2.2% | +0.8% / +19.6% |
| turb-q75 | - | -12.0% / +25.4% | +2.9% / -4.7% | -1.4% / +2.4% | -7.3% / +2.2% | +0.6% / +20.0% |
| mag-match-q75 | - | -12.0% / +25.4% | +2.6% / -4.7% | -1.4% / -0.7% | -7.5% / +2.2% | +0.8% / +15.8% |
| tsmom12 | - | -19.0% / +21.4% | +0.1% / +2.1% | -4.1% / +3.4% | -6.0% / +2.2% | -21.5% / +19.6% |
| equal-weight | - | -19.0% / +21.4% | +1.4% / +4.6% | -7.5% / +12.2% | -17.3% / +8.2% | -22.3% / +36.2% |

First day the trigger is on after the peak (business days; share of the fall on):

- turb: 1998 12 (19%), 2011 55 (29%), 2015 24 (11%), 2018-Q4 15 (9%), 2020 4 (83%)
- corr: 1998 - (0%), 2011 0 (7%), 2015 0 (15%), 2018-Q4 5 (2%), 2020 0 (8%)
- mag: 1998 12 (19%), 2011 65 (28%), 2015 23 (15%), 2018-Q4 14 (23%), 2020 3 (88%)
- mag-match: 1998 12 (19%), 2011 65 (28%), 2015 23 (15%), 2018-Q4 14 (23%), 2020 3 (88%)
- mag-match-c: 1998 12 (16%), 2011 65 (19%), 2015 24 (11%), 2018-Q4 15 (18%), 2020 3 (88%)
- turb-q75: 1998 12 (31%), 2011 25 (51%), 2015 2 (19%), 2018-Q4 14 (26%), 2020 3 (88%)
- mag-match-q75: 1998 12 (31%), 2011 24 (51%), 2015 23 (15%), 2018-Q4 14 (41%), 2020 3 (88%)

## out of universe: `idx`, 1962-01-02..2025-11-09

Assets in the signal on the test's days: 1 on 6%, 2-3 on 36%, 4+ on 58% (0 on 0%). Correlation of log T, log M, log C: T-M 0.98, T-C -0.15, M-C -0.36.

| Rule | Signal, percentile | Trigger on (share of days) | Cuts `tsmom12` (share) |
|---|---|---:|---:|
| turb | T, 90 | 10.3% | 8.6% |
| corr | C, 90 | 11.2% | 10.2% |
| mag | M, 90 | 10.4% | 8.5% |
| mag-match | M, 90.063 | 10.4% | 8.5% |
| mag-match-c | M, 89.259 | 11.2% | 9.3% |

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| turb@idx | 0.83 (0.13) | +6.2% | 7.6% | 22.1% | 8.5 | 64% | 0.77 | 1.19 | 0.92 | 0.49 | 0.50 | 0.91 | 1.31 | +0.11 (p=0.08; -0.02..+0.23) | 5/7 |
| corr@idx | 0.62 (0.13) | +5.0% | 8.3% | 25.7% | 17.5 | 62% | 0.68 | 0.81 | 0.86 | 0.64 | 0.08 | 0.31 | 0.88 | -0.10 (p=0.99; -0.17..-0.03) | 2/7 |
| mag@idx | 0.84 (0.13) | +6.2% | 7.6% | 20.8% | 8.1 | 64% | 0.77 | 1.21 | 1.14 | 0.57 | 0.33 | 0.95 | 1.01 | +0.12 (p=0.08; -0.02..+0.26) | 6/7 |
| mag-match@idx | 0.82 (0.13) | +6.1% | 7.6% | 20.8% | 8.1 | 64% | 0.77 | 1.16 | 1.14 | 0.57 | 0.29 | 0.95 | 1.01 | +0.10 (p=0.11; -0.03..+0.24) | 6/7 |
| mag-match-c@idx | 0.86 (0.13) | +6.4% | 7.5% | 20.7% | 8.3 | 63% | 0.77 | 1.23 | 1.16 | 0.58 | 0.39 | 0.90 | 1.22 | +0.14 (p=0.05; +0.00..+0.28) | 7/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.9% | 2.3 | 70% | 0.76 | 0.96 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| equal-weight@idx | 0.62 (0.13) | +7.5% | 13.1% | 57.5% | 0.3 | 100% | 0.71 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.96 | -0.10 (p=0.84; -0.27..+0.07) | 5/7 |

Paired comparisons (stationary bootstrap, block 20, 2,000 draws, seed 0):

| Pair | dSharpe | p (one-sided) | z |
|---|---:|---:|---:|
| turb - mag-match | +0.006 | 0.41 | +0.18 |
| corr - mag-match-c | -0.240 | 0.99 | -2.44 |
| turb - mag | -0.009 | 0.60 | -0.29 |
| turb - tsmom12 | +0.109 | 0.08 | +1.40 |
| corr - tsmom12 | -0.097 | 0.99 | -2.30 |
| mag-match - tsmom12 | +0.103 | 0.11 | +1.26 |
| mag - tsmom12 | +0.119 | 0.08 | +1.43 |

Slow stress windows (total return inside each):

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| turb@idx | -13% | -12% | -4% | -8% | +6% | -6% | -9% |
| corr@idx | -12% | -7% | -22% | -12% | +1% | -8% | -11% |
| mag@idx | -13% | -13% | -4% | -10% | +3% | -4% | -13% |
| mag-match@idx | -13% | -13% | -4% | -10% | +3% | -4% | -13% |
| mag-match-c@idx | -13% | -13% | -4% | -5% | +6% | -5% | -8% |
| tsmom12@idx | -14% | -11% | -22% | -11% | +3% | -8% | -11% |
| equal-weight@idx | -54% | -53% | -33% | -16% | +7% | -8% | -7% |

Fast crashes (S&P 500 index peak -> trough, then 91 days):

| Rule | 1987 fall / rebound | 1998 fall / rebound | 2011 fall / rebound | 2015 fall / rebound | 2018-Q4 fall / rebound | 2020 fall / rebound |
|---|---:|---:|---:|---:|---:|---:|
| turb@idx | -10.7% / +7.5% | -14.0% / -1.8% | -6.0% / -2.8% | -9.4% / +4.1% | -4.6% / +0.0% | -3.8% / -0.6% |
| corr@idx | -22.4% / +3.5% | -13.7% / +0.4% | -13.8% / -2.8% | -10.8% / +6.0% | -5.2% / -0.2% | -21.8% / -0.2% |
| mag@idx | -4.7% / +6.5% | -13.4% / +4.8% | -9.0% / -4.5% | -9.4% / +1.4% | -4.6% / +0.0% | -3.8% / -0.6% |
| mag-match@idx | -6.7% / +6.5% | -13.4% / +4.8% | -9.0% / -4.5% | -9.4% / +1.4% | -4.6% / +0.0% | -3.8% / -0.6% |
| mag-match-c@idx | -4.3% / +6.6% | -10.4% / +4.8% | -8.6% / -4.3% | -9.4% / +1.4% | -4.5% / +0.0% | -3.8% / -0.6% |
| tsmom12@idx | -24.3% / +6.6% | -14.3% / +4.9% | -15.3% / -2.8% | -10.2% / +5.8% | -5.3% / +0.0% | -21.8% / -0.6% |
| equal-weight@idx | -24.8% / +16.4% | -17.6% / +10.5% | -18.8% / +8.2% | -12.4% / +8.7% | -14.4% / +9.1% | -32.5% / +34.4% |

First day the trigger is on after the peak (business days; share of the fall on):

- turb: 1987 37 (28%), 1998 29 (6%), 2011 65 (28%), 2015 24 (11%), 2018-Q4 14 (24%), 2020 3 (88%)
- corr: 1987 0 (21%), 1998 2 (3%), 2011 2 (5%), 2015 11 (4%), 2018-Q4 - (0%), 2020 - (0%)
- mag: 1987 36 (25%), 1998 25 (16%), 2011 66 (26%), 2015 24 (11%), 2018-Q4 14 (24%), 2020 3 (88%)
- mag-match: 1987 36 (24%), 1998 25 (16%), 2011 66 (26%), 2015 24 (11%), 2018-Q4 14 (24%), 2020 3 (88%)
- mag-match-c: 1987 36 (26%), 1998 25 (19%), 2011 65 (28%), 2015 24 (11%), 2018-Q4 14 (27%), 2020 3 (88%)

## Pass bar (card)

### `turb`

- FAIL: 1. Sharpe beats `mag-match` with p < 0.10 (-0.042, p 0.84)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (0 of 5)
- PASS: 3. Max drawdown at most 5 points worse than the twin's (40.6% vs 45.0%)
- FAIL: 4. Same sign on `idx` (idx +0.006)
- PASS: 5. Beats equal weight (0.95 vs 0.88)
- FAIL: 6. Project bar: z >= 4.69 against `tsmom12` (-0.094, z -1.09, p 0.86)

**`turb` FAILS.**

### `corr`

- FAIL: 1. Sharpe beats `mag-match-c` with p < 0.10 (-0.074, p 0.78)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- PASS: 3. Max drawdown at most 5 points worse than the twin's (31.4% vs 38.9%)
- FAIL: 4. Same sign on `idx` (idx -0.240)
- PASS: 5. Beats equal weight (0.97 vs 0.88)
- FAIL: 6. Project bar: z >= 4.69 against `tsmom12` (-0.073, z -1.43, p 0.93)

**`corr` FAILS.**

## Fast crashes: `turb` against `mag-match` (card's descriptive reading)

| Episode | Set | `turb` fall | `mag-match` fall | `tsmom12` fall | `turb` - twin, fall | `turb` - twin, fall + rebound |
|---|---|---:|---:|---:|---:|---:|
| 1987 | idx | -10.7% | -6.7% | -24.3% | -4.0% | -3.4% |
| 1998 | idx | -14.0% | -13.4% | -14.3% | -0.6% | -6.3% |
| 2011 | idx | -6.0% | -9.0% | -15.3% | +3.0% | +4.5% |
| 2015 | idx | -9.4% | -9.4% | -10.2% | +0.0% | +2.5% |
| 2018-Q4 | idx | -4.6% | -4.6% | -5.3% | -0.0% | -0.0% |
| 2020 | idx | -3.8% | -3.8% | -21.8% | +0.0% | +0.0% |

`turb` lost less than `mag-match` in the fall in 2 of 6 episodes; mean (fall + rebound) difference -0.5%. Card's reading (at least 5 of 6 and not worse on average): **does not help**.

## Post hoc, after the run

Computed after the logged run (`lib/turbulence1_posthoc.py`), descriptive only: no backtest, no `tries.md` rows. Forward returns are overlapping windows, so the rows are far from independent.

### `six`, 1994-02-01..2025-11-09

Trigger days: `turb` 811, `mag-match` 811, both 669 (Jaccard 0.70); `turb` only 142, `mag-match` only 142; `corr` 627 (with `turb` 61).

| Days | n | Next 20 grid days, mean log return of the set's assets |
|---|---:|---:|
| all | 7,997 | +1.30% |
| `turb` on | 811 | +1.27% |
| `mag-match` on | 811 | +1.21% |
| `turb` only | 142 | +0.95% |
| `mag-match` only | 142 | +0.62% |
| `corr` on | 627 | +2.13% |

### `idx`, 1962-01-02..2025-11-09

Trigger days: `turb` 1,663, `mag-match` 1,664, both 1,482 (Jaccard 0.80); `turb` only 181, `mag-match` only 182; `corr` 1,800 (with `turb` 91).

| Days | n | Next 20 grid days, mean log return of the set's assets |
|---|---:|---:|
| all | 16,072 | +0.55% |
| `turb` on | 1,663 | +0.71% |
| `mag-match` on | 1,664 | +0.77% |
| `turb` only | 181 | +0.93% |
| `mag-match` only | 182 | +1.43% |
| `corr` on | 1,800 | +0.69% |
