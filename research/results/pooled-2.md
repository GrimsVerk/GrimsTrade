# pooled-2: e4 and vt-own-70-x vs tsmom12 outside equities

Card: `cards/pooled-2.md`. Code: `lib/pooled2.py`, `lib/pooled2_core.py` (rules from `lib/pooled1_core.py`). d = Sharpe(variant) - Sharpe(`tsmom12`) on the same series and periods (weekly Sharpe x sqrt 52 for daily series, monthly x sqrt 12 otherwise), excess over the US bill (commodities: spot); D = equal-weight mean over markets; SE from a joint circular block bootstrap of calendar months (12-month blocks, 2000 draws, seed 0). Costs a side: bonds 2 bps, currencies 3, commodities 10. Bars: z >= 2.5 (real small edge, with D > 0 in 2 of 3 judged groups and before 1994); project z >= 4.7; killed if the 95% upper end < +0.03 or z <= -2.5.

## Judged pool: bonds and currencies (21 markets)

| Variant | D | SE | z | 95% (normal) | 95% (percentile) | d > 0 | USB3 | GOV9 | FX9 | Before 1994 (markets) | SE 3 / 24-month blocks | Edge seen 80% (z 2.50 / 4.70) | Mean corr of d | Verdict |
|---|---:|---:|---:|---|---|---:|---|---|---|---|---|---|---:|---|
| `e4` | +0.010 | 0.030 | +0.33 | -0.050..+0.070 | -0.051..+0.065 | 12 of 21 | -0.001 (0.042, z -0.03) | +0.014 (0.045, z +0.31) | +0.010 (0.045, z +0.22) | +0.042 (0.042, z +1.01); 20 | 0.029 / 0.033 | +0.10 / +0.17 | +0.13 | **still open** |
| `vt-own-70-x` | -0.010 | 0.017 | -0.57 | -0.043..+0.024 | -0.044..+0.022 | 11 of 21 | +0.023 (0.036, z +0.63) | +0.022 (0.024, z +0.90) | -0.052 (0.032, z -1.60) | +0.004 (0.023, z +0.18); 20 | 0.017 / 0.018 | +0.06 / +0.09 | +0.07 | **killed** |

## Commodities, spot (8 markets; shown, not judged)

| Variant | D (SE, z) | 95% | d > 0 | Verdict by the same bars |
|---|---|---|---:|---|
| `e4` | -0.019 (0.022, z -0.86) | -0.064..+0.025 | 4 of 8 | killed |
| `vt-own-70-x` | +0.056 (0.026, z +2.15) | +0.005..+0.108 | 6 of 8 | still open |

All 29 non-equity: `e4` +0.002 (0.024, z +0.08); `vt-own-70-x` +0.009 (0.015, z +0.58)

## Combined with pooled-1's 41 equity markets (re-run with pooled-1's code)

| Variant | Equity (41) | Non-equity judged (21) | Combined (62) | Combined 95% | Combined before 1994 (markets) | Class-balanced (D, SE) | Edge seen 80% (z 2.50) | Everything (70) | Reading |
|---|---|---|---|---|---|---|---|---|---|
| `e4` | +0.063 (0.040, z +1.57) | +0.010 (0.030, z +0.33) | +0.045 (0.032, z +1.43) | -0.017..+0.107 | +0.062 (0.032, z +1.95); 37 | +0.036 (0.029, z +1.26) | +0.11 | +0.038 (0.029, z +1.30) | **unsettled, leaning positive** |
| `vt-own-70-x` | +0.022 (0.015, z +1.40) | -0.010 (0.017, z -0.57) | +0.011 (0.012, z +0.89) | -0.013..+0.035 | +0.025 (0.017, z +1.48); 37 | +0.006 (0.012, z +0.49) | +0.04 | +0.016 (0.012, z +1.41) | **equity-only at best** |

## Checks (reported, not deciding; point D)

| Check | Set | `e4` | `vt-own-70-x` |
|---|---|---:|---:|
| costs x2 | judged | -0.002 | -0.014 |
| costs x2 (COM8) | COM8 | -0.033 | +0.052 |
| FX signal on spot only | judged | +0.019 | -0.006 |
| FX signal on spot only (FX9) | FX9 | +0.030 | -0.044 |
| GOV10 gap 3 (strict OECD publication) | judged | +0.001 | -0.013 |
| GOV10 gap 3 (strict OECD publication) (GOV9) | GOV9 | -0.007 | +0.014 |

## Drift-matched null (100 i.i.d. walks with each series' own mean and sd)

| Variant | Set | D | Null mean | Null 5% / 95% | D beyond drift | Reading |
|---|---|---:|---:|---|---:|---|
| `e4` | judged | +0.010 | +0.001 | -0.027 / +0.024 | +0.009 | - |
| `e4` | COM8 | -0.019 | +0.005 | -0.025 / +0.032 | -0.024 | no timing effect either way |
| `vt-own-70-x` | judged | -0.010 | -0.005 | -0.019 / +0.009 | -0.005 | no timing effect either way |
| `vt-own-70-x` | COM8 | +0.056 | -0.008 | -0.026 / +0.007 | +0.065 | - |

## Per market

| Market | Group | Freq | Scored from | Periods | `tsmom12` Sharpe | `e4` | `vt-own-70-x` | d `e4` | d `vt-own-70-x` | `tsmom12` max DD | Turnover `tsmom12` / `e4` |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| UST2 | USB3 | w | 1977-06-10 | 2526 | 0.61 | 0.63 | 0.60 | +0.012 | -0.010 | 6% | 2.5 / 4.8 |
| UST10 | USB3 | w | 1963-01-18 | 3277 | 0.41 | 0.36 | 0.39 | -0.053 | -0.020 | 16% | 2.2 / 5.3 |
| UST30 | USB3 | w | 1978-03-03 | 2488 | 0.31 | 0.34 | 0.40 | +0.036 | +0.098 | 37% | 2.3 / 5.5 |
| GOV10-JP | GOV9 | m | 1990-03-01 | 427 | 0.45 | 0.32 | 0.43 | -0.131 | -0.020 | 11% | 1.2 / 2.3 |
| GOV10-GB | GOV9 | m | 1961-03-01 | 775 | 0.16 | 0.11 | 0.23 | -0.049 | +0.069 | 29% | 1.1 / 2.3 |
| GOV10-CH | GOV9 | m | 1973-03-01 | 630 | 0.53 | 0.56 | 0.53 | +0.030 | +0.006 | 12% | 1.0 / 2.5 |
| GOV10-CA | GOV9 | m | 1956-03-01 | 835 | 0.30 | 0.20 | 0.27 | -0.098 | -0.028 | 18% | 0.9 / 2.3 |
| GOV10-DE | GOV9 | m | 1957-07-01 | 819 | 0.58 | 0.63 | 0.62 | +0.049 | +0.040 | 15% | 0.8 / 2.0 |
| GOV10-AU | GOV9 | m | 1970-09-01 | 661 | 0.21 | 0.22 | 0.27 | +0.012 | +0.055 | 23% | 1.2 / 2.3 |
| GOV10-NZ | GOV9 | m | 1980-12-01 | 538 | 0.06 | 0.11 | 0.10 | +0.044 | +0.038 | 41% | 1.2 / 2.5 |
| GOV10-SE | GOV9 | m | 1988-02-01 | 452 | 0.36 | 0.56 | 0.40 | +0.193 | +0.031 | 22% | 1.0 / 2.0 |
| GOV10-NO | GOV9 | m | 1986-03-01 | 475 | 0.31 | 0.38 | 0.31 | +0.075 | +0.002 | 16% | 1.1 / 2.4 |
| FX-JPY | FX9 | w | 1974-03-22 | 2694 | 0.24 | 0.19 | 0.21 | -0.052 | -0.037 | 35% | 2.2 / 5.0 |
| FX-GBP | FX9 | w | 1974-03-22 | 2694 | 0.18 | 0.24 | 0.15 | +0.065 | -0.028 | 39% | 2.5 / 5.2 |
| FX-CHF | FX9 | w | 1974-03-22 | 2694 | 0.21 | 0.21 | 0.27 | -0.005 | +0.054 | 37% | 2.3 / 5.4 |
| FX-CAD | FX9 | w | 1974-03-22 | 2694 | 0.08 | 0.08 | -0.11 | -0.001 | -0.193 | 31% | 3.0 / 5.7 |
| FX-AUD | FX9 | w | 1974-03-22 | 2694 | 0.20 | 0.19 | 0.09 | -0.009 | -0.113 | 38% | 2.1 / 5.0 |
| FX-NZD | FX9 | w | 1975-01-17 | 2651 | 0.42 | 0.41 | 0.31 | -0.011 | -0.109 | 28% | 2.3 / 5.3 |
| FX-SEK | FX9 | w | 1974-03-22 | 2694 | 0.13 | 0.16 | 0.14 | +0.026 | +0.014 | 35% | 2.4 / 5.3 |
| FX-NOK | FX9 | w | 1980-02-15 | 2386 | 0.21 | 0.23 | 0.13 | +0.021 | -0.078 | 31% | 3.1 / 5.7 |
| FX-EUR | FX9 | m | 1974-05-01 | 618 | 0.07 | 0.12 | 0.10 | +0.054 | +0.026 | 50% | 1.2 / 2.3 |
| PPI-grains | COM8 | m | 1927-04-01 | 1181 | 0.16 | 0.12 | 0.18 | -0.043 | +0.018 | 59% | 1.3 / 2.6 |
| PPI-livestock | COM8 | m | 1947-03-01 | 942 | 0.16 | -0.05 | 0.14 | -0.215 | -0.021 | 57% | 1.2 / 2.6 |
| PPI-coal | COM8 | m | 1927-04-01 | 1181 | 0.62 | 0.53 | 0.62 | -0.086 | -0.002 | 16% | 1.2 / 2.4 |
| PPI-natgas | COM8 | m | 1968-04-01 | 689 | 0.19 | 0.28 | 0.20 | +0.089 | +0.012 | 94% | 1.3 / 2.4 |
| PPI-crude | COM8 | m | 1948-04-01 | 929 | 0.10 | 0.17 | 0.14 | +0.069 | +0.036 | 91% | 1.0 / 1.9 |
| PPI-steel | COM8 | m | 1927-04-01 | 1181 | 0.64 | 0.66 | 0.88 | +0.018 | +0.238 | 37% | 0.7 / 1.8 |
| PPI-prim-nonferrous | COM8 | m | 1948-04-01 | 929 | 0.40 | 0.47 | 0.56 | +0.071 | +0.154 | 46% | 0.9 / 2.0 |
| GOLD | COM8 | m | 1972-03-01 | 644 | 0.63 | 0.57 | 0.65 | -0.059 | +0.016 | 44% | 1.3 / 2.3 |
