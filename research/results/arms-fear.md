# W45 `arms-fear`: results

Card: `research/cards/wide-28.md`. Code: `research/lib/wide28.py`. One real run.

- NICS months 1998-11 .. 2023-09; dose defined 2000-01 .. 2023-09 (285 months), SD 0.179; gate rows 182.
- Lag-1 acf of the dose 0.935; |end - start| / SD 4.46; surrogate family `iaaft`, gating: True.
- **Gate: b +10.177 % per unit of D over 3 months, t +3.50; rank 2 of 41 (shifted), 2 of 41 (surrogates). Pass: True.**

| Cell | b, % | t | Rows |
|---|---:|---:|---:|
| Gate | +10.177 | +3.50 | 182 |
| Horizon 1 month (NW 0) | +3.403 | +1.86 | 182 |
| Horizon 6 months (NW 6) | +19.487 | +4.03 | 182 |
| Horizon 12 months (NW 12) | +29.877 | +3.90 | 182 |
| No controls | +10.659 | +4.13 | 182 |
| Without rv | +10.753 | +4.16 | 182 |
| One-month dose ln(S(m)/S(m-12)) | +7.457 | +3.05 | 182 |
| Dose from `totals` | +13.096 | +3.76 | 182 |
| Rows 2008-08 .. 2015-12 | +6.121 | +1.16 | 89 |
| Rows 2016-01 .. 2023-09 | +13.111 | +3.21 | 93 |
| Without rows 2020-02 .. 2021-06 | +7.919 | +1.95 | 165 |

| Null | SD | share \|t\|>=2 | 5% | 50% | 95% | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shifted (k 25..103) | 1.95 | 0.40 | -2.34 | +0.30 | +3.19 | -3.35 | +3.71 |
| Surrogates (iaaft) | 1.52 | 0.23 | -2.05 | +0.53 | +2.79 | -2.40 | +3.50 |

Shifted t by k: 25: -2.23, 27: -2.07, 29: -2.45, 31: -1.71, 33: -0.64, 35: -0.50, 37: -0.71, 39: -0.11, 41: +0.39, 43: +0.05, 45: +0.36, 47: +1.87, 49: +2.65, 51: +2.87, 53: +3.71, 55: +3.19, 57: +1.66, 59: +1.58, 61: +1.53, 63: +0.76, 65: +0.01, 67: -0.32, 69: +0.78, 71: -0.34, 73: -2.34, 75: -1.86, 77: -2.06, 79: -2.33, 81: -3.35, 83: -1.76, 85: +0.23, 87: +0.87, 89: +1.67, 91: +2.73, 93: +2.95, 95: +3.11, 97: +3.19, 99: +2.72, 101: +1.95, 103: -0.15

R45: (4.946933375783261, 0.538794977616967, 101, 13, False)

R45 tuple: (b, t, rows, rank among the gate's 40 IAAFT surrogates, pass). The card's R45 text
names phase surrogates; with 40 phase surrogates (seed 2745, run once after the above,
2026-11-26 00:10 UTC): b +4.947, t +0.54, 101 rows, rank 17 of 41. R45 fails either way (t < 2).
