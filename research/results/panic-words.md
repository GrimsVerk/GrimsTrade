# W34 `panic-words`: result

Card: `research/cards/panic-words-1.md`. Script: `research/lib/panicwords1.py`. Data: American Stories (Dell et al. 2023, CC-BY 4.0) monthly article counts (`panic-words-counts.csv`); US market from Ken French's daily file.

**Gate (dose months 1927-07 .. 1963-12, 438 rows):** b = +1.383% next-month log return per unit of d (+0.354% per sd of d, sd 0.256), Newey-West t +1.19; rank 37 of 41 (lowest = 1). **FAIL.**

40 placebo t: standard deviation 1.18, share with |t| >= 2 10%; quantiles 5% -2.03, 50% -0.10, 95% +1.47; smallest -2.80, largest +3.08.

| k (months; earlier dose) | t |
|---:|---:|
| 25 | -2.80 |
| 27 | -0.39 |
| 29 | -2.28 |
| 31 | +0.34 |
| 33 | -1.15 |
| 35 | -0.09 |
| 37 | +0.31 |
| 39 | +3.08 |
| 41 | +0.22 |
| 43 | +0.57 |
| 45 | -0.40 |
| 47 | -0.17 |
| 49 | +0.06 |
| 51 | +0.79 |
| 53 | -0.89 |
| 55 | -1.71 |
| 57 | +0.34 |
| 59 | +0.41 |
| 61 | -1.80 |
| 63 | -0.96 |
| 65 | +0.43 |
| 67 | -1.18 |
| 69 | -2.02 |
| 71 | -0.84 |
| 73 | -0.13 |
| 75 | +1.43 |
| 77 | -0.13 |
| 79 | +0.42 |
| 81 | +0.13 |
| 83 | -0.10 |
| 85 | -1.94 |
| 87 | +1.46 |
| 89 | -1.02 |
| 91 | +1.68 |
| 93 | +0.68 |
| 95 | +0.41 |
| 97 | -1.08 |
| 99 | +0.33 |
| 101 | -1.66 |
| 103 | +0.16 |

## Shown (not gating)

| Cell | b (% per unit d) | t | rows |
|---|---:|---:|---:|
| (a) no controls | +1.281 | +1.04 | 438 |
| (b) "crash" dose, controls | +1.935 | +1.45 | 438 |
| (c) months m+1..m+3 | +0.142 | +0.06 | 438 |
| (e) 1927-07 .. 1945-12 | +2.987 | +1.21 | 222 |
| (e) 1946-01 .. 1963-12 | +0.187 | +0.21 | 216 |
| (d) common rows 1934-08 .. 1963-12 | +1.096 | +1.06 | 353 |

(d) on the common rows: rank 34 of 41. 40 placebo t: standard deviation 1.18, share with |t| >= 2 2%; quantiles 5% -1.70, 50% -0.12, 95% +1.77; smallest -1.88, largest +3.40.

(f) feedback, d(m) on the dose month's return c1 and the past year's c12 (438 rows): c1 -0.047 (t -0.25), c12 -0.100 (t -1.98).
