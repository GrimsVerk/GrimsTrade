# W36 `grid-load-premium`: result

Card: `research/cards/wide-22.md`. Script: `research/lib/wide22.py`. Data: EIA Monthly Energy Review Table 7.6 (ESICPUS, industrial retail sales of electricity; ESRCPUS residential), Ken French's monthly `Mkt-RF`. Only statistics are committed.

**Gate (usage months 1974-01 .. 2025-07, 619 rows; outcome Mkt-RF of month m+3):** b = -0.0978% a month per point of year-on-year growth (-0.421% per sd of g, sd 4.30 points), Newey-West t -2.31; rank 1 of 41 (lowest = 1); post-sample b -0.2252 (t -2.53, 175 rows). **PASS (kill-only).**

Conditions: b < 0 yes; t <= -2 yes; rank <= 2 yes; post-sample b < 0 yes.

## Placebo null: earlier doses, k = 25..103 months (odd)

40 placebo t: standard deviation 0.91, share with |t| >= 2 2%; quantiles 5% -1.38, 50% -0.44, 95% +1.40; smallest -1.54, largest +2.06.

| placebo | t |
|---|---:|
| k = 25 | -0.49 |
| k = 27 | -0.70 |
| k = 29 | +0.03 |
| k = 31 | -0.39 |
| k = 33 | -0.52 |
| k = 35 | -0.27 |
| k = 37 | +0.38 |
| k = 39 | -0.10 |
| k = 41 | -0.89 |
| k = 43 | -1.23 |
| k = 45 | -0.45 |
| k = 47 | -1.11 |
| k = 49 | -1.54 |
| k = 51 | -0.80 |
| k = 53 | -1.38 |
| k = 55 | -0.72 |
| k = 57 | -1.38 |
| k = 59 | -0.43 |
| k = 61 | +0.18 |
| k = 63 | -0.93 |
| k = 65 | -0.45 |
| k = 67 | +1.21 |
| k = 69 | +0.95 |
| k = 71 | -0.18 |
| k = 73 | -0.39 |
| k = 75 | +1.14 |
| k = 77 | +2.06 |
| k = 79 | +1.17 |
| k = 81 | +1.42 |
| k = 83 | +1.28 |
| k = 85 | +1.40 |
| k = 87 | +0.64 |
| k = 89 | -0.66 |
| k = 91 | -0.64 |
| k = 93 | -0.27 |
| k = 95 | -0.69 |
| k = 97 | -1.00 |
| k = 99 | -0.91 |
| k = 101 | -1.30 |
| k = 103 | +0.05 |

## Shown (not gating)

| Cell | b (% a month per point) | t | rows |
|---|---:|---:|---:|
| (a) with controls: Mkt-RF of m+2, of m-9..m+2 | -0.0985 | -2.46 | 619 |
| (b) paper's horizon: Mkt-RF m+3..m+14, NW 18 | -0.4984 | -1.29 | 608 |
| (c) inside the paper's sample, 1974-01 .. 2010-12 | -0.0743 | -1.52 | 444 |
| (c) after it, 2011-01 .. 2025-07 (gate condition 4) | -0.2252 | -2.53 | 175 |
| (d) common rows 1982-08 .. 2025-07 | -0.0946 | -1.93 | 516 |
| (e) negative control: residential sales growth | -0.0286 | -1.04 | 619 |
| (h) SPY log return, month m+3 | -0.0463 | -0.67 | 393 |
| (h) TLT log return, month m+3 | +0.0278 | +0.49 | 279 |
| (h) GLD log return, month m+3 | +0.0023 | +0.04 | 251 |
| (h) BTC log return, month m+3 | -1.3666 | -1.82 | 165 |

(d) on the common rows the true t ranks 1 of 41 against the same 40 shifts.

(f) feedback, g(m) on the market's 12- and 24-month excess returns ending at m (619 rows, NW 12): 12-month +0.0292 (t +0.98), 24-month +0.0531 (t +2.28).

(g) phase-randomised surrogates of g (seed 22): the true t ranks 3 of 41.

40 placebo t: standard deviation 1.10, share with |t| >= 2 10%; quantiles 5% -1.64, 50% -0.00, 95% +1.85; smallest -2.62, largest +2.17.

| placebo | t |
|---|---:|
| surrogate 1 | +0.49 |
| surrogate 2 | +0.44 |
| surrogate 3 | +0.39 |
| surrogate 4 | -0.41 |
| surrogate 5 | -0.94 |
| surrogate 6 | +2.17 |
| surrogate 7 | -1.59 |
| surrogate 8 | +1.73 |
| surrogate 9 | +0.32 |
| surrogate 10 | +0.10 |
| surrogate 11 | -0.24 |
| surrogate 12 | -0.55 |
| surrogate 13 | -0.43 |
| surrogate 14 | -1.41 |
| surrogate 15 | +1.31 |
| surrogate 16 | +0.35 |
| surrogate 17 | -1.04 |
| surrogate 18 | -0.04 |
| surrogate 19 | -2.62 |
| surrogate 20 | +0.03 |
| surrogate 21 | -2.57 |
| surrogate 22 | -0.22 |
| surrogate 23 | -0.39 |
| surrogate 24 | +1.04 |
| surrogate 25 | +1.34 |
| surrogate 26 | -0.01 |
| surrogate 27 | +1.84 |
| surrogate 28 | +0.71 |
| surrogate 29 | -0.27 |
| surrogate 30 | -0.22 |
| surrogate 31 | +0.21 |
| surrogate 32 | -0.63 |
| surrogate 33 | -0.13 |
| surrogate 34 | +0.81 |
| surrogate 35 | -0.17 |
| surrogate 36 | +2.13 |
| surrogate 37 | -0.93 |
| surrogate 38 | +0.51 |
| surrogate 39 | +0.01 |
| surrogate 40 | +1.67 |
