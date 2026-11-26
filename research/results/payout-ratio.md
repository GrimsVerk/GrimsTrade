# W47 `payout-ratio`: results

Card: `research/cards/wide-30.md`. Code: `research/lib/wide30.py`. One real run.
Row months below are the card's m (the code's m' minus 3).

- D/E months 1871-01 .. 2023-06; dose SD 0.268; gate rows 390.
- Lag-1 acf 0.990; |end - start| / SD 1.02; surrogates `iaaft`, gating: True.
- **Gate: b +2.437 % per unit of H over 12 months, t +0.80; rank of t 18 of 41 (shifted), 20 of 41 (surrogates). Pass: False.**

| Cell | b, % | t | Rows |
|---|---:|---:|---:|
| Gate | +2.437 | +0.80 | 390 |
| Horizon 3 months (NW 3) | +1.087 | +0.84 | 390 |
| Horizon 6 months (NW 6) | +1.399 | +0.59 | 390 |
| No controls | +2.150 | +0.65 | 390 |
| Without rv | +2.511 | +0.82 | 390 |
| Rows 1991-01 .. 2007-12 | +0.497 | +0.05 | 204 |
| Rows 2008-01 .. 2024-06 | +1.163 | +0.56 | 186 |
| Without rows 2008-07 .. 2010-06 | -3.641 | -0.62 | 366 |

| Null | SD | share \|t\|>=2 | 5% | 50% | 95% | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shifted (k 25..103) | 1.61 | 0.23 | -1.51 | +0.56 | +3.31 | -1.66 | +3.47 |
| Surrogates (iaaft) | 2.00 | 0.25 | -2.90 | +0.63 | +2.77 | -6.67 | +4.12 |

Shifted t by k: 25: +0.60, 27: +1.06, 29: +1.55, 31: +1.95, 33: +2.45, 35: +2.92, 37: +3.27, 39: +3.47, 41: +3.47, 43: +3.30, 45: +3.00, 47: +2.64, 49: +2.25, 51: +1.78, 53: +1.28, 55: +0.74, 57: +0.24, 59: -0.27, 61: -0.78, 63: -1.17, 65: -1.45, 67: -1.51, 69: -1.45, 71: -1.22, 73: -0.86, 75: -0.43, 77: +0.08, 79: +0.52, 81: +0.85, 83: +0.95, 85: +0.89, 87: +0.69, 89: +0.38, 91: +0.08, 93: -0.25, 95: -0.61, 97: -0.93, 99: -1.24, 101: -1.51, 103: -1.66

R47: not run (the gate failed)
