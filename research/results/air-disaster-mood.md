# W29 `air-disaster-mood`: result

Card: `research/cards/wide-20.md` (pushed before this run). Script: `research/lib/wide20.py`. Train only: bars to 2025-10-31; held-out year unread.
Events: Wikidata aviation accidents with >= 50 deaths, day precision (460 in all years to 2025-10-31; 34 in the gate window).

## Gate (SPY daily return on the dose of days 0-1, HC1)

| Test | Value | Needed | Met |
|---|---:|---|---|
| b, % a day per unit of log2(deaths / 25), 4488 days | -0.0383 | < 0 | True |
| t (HC1) | -0.59 | <= -2 | False |
| Rank of true t among 41 calendars (1 = lowest) | 10 | <= 2 | False |

**Gate: fail.** Empirical one-sided p = 10/41 = 0.244.

## Placebo null (each event moved 23k days, wrapped in the window, k = +-1..20)

40 placebo t: sd 0.91, share with |t| >= 2 2%; quantiles 5% -1.59, 50% +0.11, 95% +1.26; smallest -2.04, largest +1.47.

| k | t |
|---:|---:|
| -20 | +0.19 |
| -19 | +0.02 |
| -18 | +0.32 |
| -17 | +0.56 |
| -16 | -0.36 |
| -15 | +1.47 |
| -14 | -2.04 |
| -13 | -0.36 |
| -12 | +0.39 |
| -11 | +0.28 |
| -10 | -1.16 |
| -9 | +1.31 |
| -8 | -0.66 |
| -7 | -0.09 |
| -6 | -1.23 |
| -5 | +0.74 |
| -4 | -1.58 |
| -3 | +0.25 |
| -2 | +0.36 |
| -1 | -1.84 |
| +1 | -1.49 |
| +2 | -1.47 |
| +3 | +0.94 |
| +4 | +0.59 |
| +5 | -0.25 |
| +6 | +0.02 |
| +7 | +1.18 |
| +8 | -0.14 |
| +9 | +0.61 |
| +10 | +1.26 |
| +11 | +1.06 |
| +12 | +0.49 |
| +13 | -0.51 |
| +14 | +0.71 |
| +15 | +0.87 |
| +16 | -0.44 |
| +17 | -0.73 |
| +18 | -0.39 |
| +19 | +0.52 |
| +20 | -0.08 |

## Shown (not gating)

| Cut | Events | b, % a day per unit (t) | Days |
|---|---:|---:|---:|
| Gate (SPY, dose, days 0-1) | 34 | -0.0383 (-0.59) | 4488 |
| Binary indicator, days 0-1 | 34 | -0.1394 (-1.04) | 4488 |
| Dose, days 0-2 | 34 | -0.0632 (-1.13) | 4488 |
| Reversal: dose on days 2-4 (predicted > 0) | 34 | +0.0004 (+0.01) | 4488 |
| Only >= 100 deaths | 16 | +0.0135 (+0.20) | 4488 |
| Three largest removed | 31 | -0.0662 (-0.93) | 4488 |
| QQQ from 2008-01-02 | 34 | -0.0215 (-0.30) | 4488 |
| IWM from 2008-01-02 | 34 | +0.0357 (+0.40) | 4488 |
| GLD from 2008-01-02 | 34 | +0.1116 (+1.96) | 4488 |
| TLT from 2008-01-02 | 34 | -0.0607 (-0.94) | 4488 |
| BTC from 2012-01-02 | 20 | -0.0715 (-0.25) | 5049 |
| ETH from 2016-05-19 | 10 | -0.2967 (-0.85) | 3451 |
| List completed (+13 items, wide-20.md addendum) | 47 | -0.0274 (-0.57) | 4488 |
| GSPC 1950-2007 (the paper's span, in-sample for it) | 414 | -0.0270 (-1.52) | 14591 |
| GSPC 1950-2007, binary | 414 | -0.0748 (-2.05) | 14591 |
| GSPC 1950-2007, reversal days 2-4 | 414 | -0.0152 (-1.23) | 14591 |
| GSPC 1950-2025 (full span) | 448 | -0.0269 (-1.57) | 19079 |

GSPC 1950-2007 with its own 40 placebos (shown): t -1.52, rank 8 of 41 (1 = lowest). 40 placebo t: sd 1.10, share with |t| >= 2 12%; quantiles 5% -2.39, 50% -0.65, 95% +1.13; smallest -2.57, largest +1.25.

List completed with its own 40 placebos (shown): t -0.57, rank 11 of 41. 40 placebo t: sd 0.79, share with |t| >= 2 0%; quantiles 5% -1.06, 50% +0.16, 95% +1.28; smallest -1.39, largest +1.50. Added events: 2010-01-25 90, 2010-05-22 158, 2010-07-28 152, 2014-03-08 239, 2014-12-28 162, 2018-02-11 71, 2018-02-18 66, 2018-04-11 257, 2018-05-18 112, 2018-10-29 189, 2019-03-10 157, 2020-05-22 98, 2023-01-15 72.

Largest events in the gate window (date, deaths): 2014-07-17 298, 2025-06-12 260, 2009-06-01 228, 2015-10-31 224, 2024-12-29 179.
