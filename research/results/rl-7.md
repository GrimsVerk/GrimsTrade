# rl-7 tables

Card `research/cards/rl-7.md`; code `research/lib/rl7.py`; raw numbers `rl-7-gate.json`,
`rl-7-final.json`. Monthly net returns, Sharpe with sqrt 12, cash 0 (excess series already
excess). D = equal-weight mean over markets of the paired Sharpe difference; SE from the joint
circular 12-month block bootstrap of calendar months (2,000 draws, seed 0).

## Split (seed 707, rule fixed on the card)

| Cell | Markets | Rows (eligible months) | Span |
|---|---:|---:|---|
| Training cell: train markets x before 1990 | 23 | 9,149 | 1870-08..1989-12 |
| Primary holdout: holdout markets x 1990-01.. (judged) | 56 | 20,962 | 1990-01..2025-10 |
| Train markets x 1990-01.. (reported) | 19 | | 1990-01..2025-10 |
| Holdout markets x before 1990 (reported) | 24 | | 1929-04..1989-12 |

Train markets: US-NoDur, US-Manuf, US-Telcm, US-Hlth, US-Other, Canada, UST2, GOV10-GB,
GOV10-CA, GOV10-NZ, FX-GBP, FX-AUD, FX-SEK, FX-NOK, PPI-grains, PPI-coal, PPI-natgas, GOLD,
NO-french, and the four pre-1927 markets (US, GB, DE, FR).

## Planted-signal gate (training cell only, purged 5-fold time CV, out of fold)

Realised IC of `peek` with the target: 0.007 (s = 0.00), 0.057 (0.05), 0.107 (0.10).

| Learner | Lift at 0.05 (z) | Ceiling at 0.05 | Share | Lift at 0.10 (z) | Ceiling at 0.10 | Noise cost (0.00 minus none) | G1 | G2 | G3 | G4 | Gate |
|---|---|---:|---:|---|---:|---:|---|---|---|---|---|
| `lasso-sign` | +0.007 (0.58) | -0.002 | n/a | +0.048 (2.15) | +0.028 | -0.001 | no | no | yes | yes | **fails** |
| `pg-lin` | +0.014 (1.91) | +0.015 | 90% | +0.047 (3.37) | +0.053 | +0.000 | yes | yes | yes | yes | **passes** |

Each run against `tsmom12` on the training cell (out of fold; `tsmom12` mean per-market Sharpe
0.494):

| Run | Mean Sharpe | D vs `tsmom12` | SE | d > 0 |
|---|---:|---:|---:|---:|
| `lasso-sign@none` | 0.455 | -0.038 | 0.039 | 6/23 |
| `lasso-sign@0.05` | 0.461 | -0.032 | 0.036 | 7/23 |
| `lasso-sign@0.10` | 0.502 | +0.009 | 0.031 | 8/23 |
| `pg-lin@none` | 0.465 | -0.028 | 0.024 | 11/23 |
| `pg-lin@0.05` | 0.479 | -0.014 | 0.028 | 11/23 |
| `pg-lin@0.10` | 0.513 | +0.019 | 0.032 | 11/23 |

Lasso penalties chosen per outer fold (no `peek`): 0.01, 0.01, 0.05, 0.01, 0.02. Its mean
position is 0.76-0.90: the forecast is almost always above zero, so its long-or-flat policy is
mostly "long". `pg-lin`'s mean position is 0.11-0.14.

## Final run (once; `pg-lin` only, fitted on the whole training cell, frozen)

Weights (standardised inputs): `up12` +0.31, `up1` +0.20, `m12` +0.19, `m1` +0.14, `up6`
+0.11, `drift` +0.06, `dvol` -0.05, `m3` -0.04, `m6` +0.03, `up3` +0.02, `m24` +0.00;
bias -2.13.

| Cell | D vs `tsmom12` | SE | z | d > 0 | Mean Sharpe `tsmom12` / `pg-lin` | Mean position | Position change a year |
|---|---:|---:|---:|---:|---|---|---|
| **Primary: holdout markets x 1990-2025** | **+0.016** | 0.034 | **+0.46** | 32/56 | 0.405 / 0.420 | 0.64 / 0.13 | 1.18 / 0.50 |
| Train markets x 1990-2025 | +0.006 | 0.026 | +0.24 | 11/19 | 0.379 / 0.386 | 0.63 / 0.13 | 1.29 / 0.52 |
| Holdout markets x before 1990 | -0.024 | 0.031 | -0.77 | 10/24 | 0.520 / 0.496 | 0.65 / 0.13 | 0.97 / 0.48 |

Primary cell by class (the loader labels all 8 ETFs `equity`, so IEF and LQD (bonds) and DBC
and SLV (commodities) sit in the equity row):

| Class | Markets | D | SE | d > 0 |
|---|---:|---:|---:|---:|
| equity | 39 | +0.027 | 0.044 | 24 |
| rates | 8 | -0.018 | 0.048 | 3 |
| fx | 5 | -0.047 | 0.047 | 2 |
| commodity | 4 | +0.054 | 0.045 | 3 |

Verdict by the card: one-sided 95% upper bound +0.072 (not below +0.05, so not killed);
z 0.46 < 1.96 < 4.70: **not shown**. 2 of 4 classes positive.

Per market (primary), lowest to highest: FX-JPY -0.20, GOV10-JP -0.15, Netherlands -0.12,
FX-CAD -0.11 ... Austria +0.15, PPI-crude +0.15, EFA +0.16 (full list in `rl-7-final.json`).
