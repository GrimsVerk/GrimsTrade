# R36: replication of W36 `grid-load-premium` on 1926-1955

Card: `research/cards/wide-22b.md` (pushed after the W36 number, before this one). Script: `research/lib/wide22.py r36`. Data: NBER Macrohistory electric power production (FRED `M01128USM247NNBR` to 1938, `M0128AUSM247NNBR` from 1939, spliced on year-on-year growth); French monthly `Mkt-RF`.

**R36 (usage months 1926-04 .. 1955-12, 357 rows; outcome Mkt-RF of month m+3):** b = -0.0271% a month per point (-0.203% per sd of g, sd 7.47), Newey-West t -0.32; rank 13 of 41 (lowest = 1). **FAIL: W36 is killed.**

## Placebo null: earlier doses, k = 25..103 months (odd)

40 placebo t: standard deviation 0.55, share with |t| >= 2 0%; quantiles 5% -1.36, 50% -0.14, 95% +0.60; smallest -1.78, largest +0.66.

| placebo | t |
|---|---:|
| k = 25 | -0.41 |
| k = 27 | -0.25 |
| k = 29 | -0.37 |
| k = 31 | -0.28 |
| k = 33 | +0.14 |
| k = 35 | -0.19 |
| k = 37 | +0.21 |
| k = 39 | -0.30 |
| k = 41 | -0.10 |
| k = 43 | -0.04 |
| k = 45 | +0.03 |
| k = 47 | -0.97 |
| k = 49 | -1.78 |
| k = 51 | -1.00 |
| k = 53 | -1.14 |
| k = 55 | -1.36 |
| k = 57 | -1.38 |
| k = 59 | -0.74 |
| k = 61 | -0.22 |
| k = 63 | -0.48 |
| k = 65 | -0.18 |
| k = 67 | +0.04 |
| k = 69 | -0.00 |
| k = 71 | -0.07 |
| k = 73 | +0.24 |
| k = 75 | +0.34 |
| k = 77 | +0.36 |
| k = 79 | +0.66 |
| k = 81 | +0.64 |
| k = 83 | +0.60 |
| k = 85 | -0.09 |
| k = 87 | -0.53 |
| k = 89 | -0.29 |
| k = 91 | +0.10 |
| k = 93 | +0.04 |
| k = 95 | -0.53 |
| k = 97 | -0.05 |
| k = 99 | +0.18 |
| k = 101 | +0.05 |
| k = 103 | -0.28 |

## Shown (not deciding)

| Cell | b (% a month per point) | t | rows |
|---|---:|---:|---:|
| without the Depression, 1934-01 .. 1955-12 | -0.0398 | -0.68 | 264 |
| P1 alone, 1926-04 .. 1938-12 | -0.0812 | -0.57 | 153 |
| P2 alone, 1939-01 .. 1955-12 | -0.0059 | -0.10 | 204 |

Phase-randomised surrogates of g (seed 22): the true t ranks 14 of 41.

40 placebo t: standard deviation 1.10, share with |t| >= 2 8%; quantiles 5% -1.86, 50% +0.04, 95% +1.49; smallest -2.84, largest +2.32.

| placebo | t |
|---|---:|
| surrogate 1 | +2.32 |
| surrogate 2 | -0.08 |
| surrogate 3 | +0.03 |
| surrogate 4 | -1.68 |
| surrogate 5 | +1.00 |
| surrogate 6 | +0.76 |
| surrogate 7 | +0.56 |
| surrogate 8 | -0.12 |
| surrogate 9 | -1.83 |
| surrogate 10 | -2.84 |
| surrogate 11 | +0.28 |
| surrogate 12 | -1.19 |
| surrogate 13 | -0.05 |
| surrogate 14 | -2.43 |
| surrogate 15 | -0.95 |
| surrogate 16 | -1.39 |
| surrogate 17 | -0.57 |
| surrogate 18 | -0.39 |
| surrogate 19 | -0.41 |
| surrogate 20 | +0.05 |
| surrogate 21 | +0.67 |
| surrogate 22 | +0.41 |
| surrogate 23 | +1.47 |
| surrogate 24 | +0.47 |
| surrogate 25 | +0.32 |
| surrogate 26 | -1.78 |
| surrogate 27 | +0.11 |
| surrogate 28 | +0.17 |
| surrogate 29 | -0.21 |
| surrogate 30 | +0.47 |
| surrogate 31 | -0.59 |
| surrogate 32 | -0.89 |
| surrogate 33 | +1.72 |
| surrogate 34 | -0.30 |
| surrogate 35 | +0.94 |
| surrogate 36 | -0.23 |
| surrogate 37 | +1.47 |
| surrogate 38 | +0.43 |
| surrogate 39 | +0.20 |
| surrogate 40 | +1.15 |
