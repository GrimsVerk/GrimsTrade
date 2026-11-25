# W44 `revision-noise`: results

Card: `research/cards/wide-27.md`. Code: `research/lib/wide27.py`. One real run, 2026-11-25 23:32 UTC. Verdict: **dead** (kill-only gate fails
in both placebo families; R44 not run). Write-up: `research/wide-27.md`.

- Vintages 1964-12 .. 2025-10; dose defined 1975-12 .. 2025-07 (596 months); gate rows 427.
- Lag-1 acf of the dose 0.969; |end - start| / SD 0.89; surrogate family `phase`, gating: True.
- **Gate: b +0.473 % per unit of D over 3 months, t +0.24; rank 23 of 41 (shifted), 19 of 41 (surrogates). Pass: False.**

| Cell | b, % | t | Rows |
|---|---:|---:|---:|
| Gate | +0.473 | +0.24 | 427 |
| Horizon 1 month (NW 0) | +0.244 | +0.26 | 427 |
| Horizon 6 months (NW 6) | +1.372 | +0.38 | 424 |
| Horizon 12 months (NW 12) | -0.224 | -0.04 | 418 |
| No controls | +1.531 | +0.95 | 427 |
| Without s12 | +0.873 | +0.61 | 427 |
| First revision only | +0.579 | +0.30 | 427 |
| Dose in levels (ln R12, no trailing mean) | +0.350 | +0.17 | 427 |
| Rows 1990-01 .. 2007-12 | +6.942 | +1.30 | 216 |
| Rows 2008-01 .. 2025-07 | -1.598 | -0.66 | 211 |

| Null | SD | share \|t\|>=2 | 5% | 50% | 95% | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shifted (k 25..103) | 1.03 | 0.05 | -0.93 | +0.53 | +1.89 | -1.17 | +2.20 |
| Surrogates (phase) | 0.96 | 0.03 | -1.26 | +0.09 | +1.50 | -2.65 | +1.87 |

Shifted t by k: 25: +2.04, 27: +1.88, 29: +1.32, 31: +1.29, 33: +1.43, 35: +1.32, 37: +1.24, 39: +1.83, 41: +2.20, 43: +1.43, 45: +1.44, 47: +1.41, 49: +1.22, 51: +1.01, 53: +0.69, 55: +0.80, 57: +0.25, 59: -0.78, 61: -0.93, 63: -0.61, 65: -0.86, 67: -1.01, 69: -1.17, 71: -0.79, 73: -0.61, 75: -0.88, 77: -0.88, 79: -0.60, 81: -0.45, 83: -0.84, 85: -0.80, 87: -0.31, 89: +0.13, 91: +0.15, 93: +0.80, 95: +1.13, 97: +1.11, 99: +0.77, 101: +0.36, 103: +0.13

R44: not run (the gate failed)
