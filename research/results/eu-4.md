# eu-4 results: whipsaw reducers on `euw` (cards/eu-4.md)

Train period only, window W (decisions 2012-01-02 .. 2025-11-09). Total-return prices; `euw` and `eu6` in EUR, `usw` in USD. Sharpe on calendar days, zero risk-free rate. `euw`/`eu6`: ETF slippage 0.05% a side (eu-2's costs; coins at the gym's); `usw`: the gym's costs (as eu-1). 1% band. `R` = the house rule `tsmom12`; C1 `confirm2` = switch only after two Fridays in a row with the new sign; C2 `dz25` = dead zone, enter above z = +0.25, leave below z = -0.25 (z = 12-month log return / one-year EWMA vol). Fee tiers: EUR 1, 2, 3 per ETF order on a constant book (eu-2's schedules; the EUR 1 and EUR 3 tiers also carry a EUR 2.50 yearly fee). `R`, V0 and equal weight on `euw` are eu-3's saved runs, re-scored.

## 1. Character on `euw` at no fixed fee

| Rule | Orders/yr | Entries | Exits | Drift | Signal flips/yr | Sharpe | Max DD | 1. Position corr (agree; exposure corr) | 2. dSharpe | 3. dMax DD | 4. Crash signs match / worst window gap | Keeps character (euw) |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| R `tsmom12` | 30.1 | 10.2 | 9.8 | 10.0 | 19.8 | 0.617 | 13.0% | - | - | - | - | (reference) |
| V0 (eu-3) | 27.9 | 10.2 | 9.8 | 7.9 | 19.8 | 0.630 | 13.2% | 1.00 | +0.014 | - | - | yes (eu-3) |
| C1-confirm2 | 20.0 | 5.3 | 4.8 | 10.0 | 9.8 | 0.616 | 16.3% | 0.91 (96%; 0.92) yes | -0.000 yes | +3.3 pts **no** | 3/4, 3.0 pts yes | **no** |
| C2-dz25 | 16.6 | 3.8 | 3.4 | 9.4 | 6.9 | 0.642 | 15.4% | 0.89 (95%; 0.90) yes | +0.026 yes | +2.4 pts **no** | 4/4, 2.6 pts yes | **no** |

Family bar: 8 selectable variants (eu-3's V0-V5, C1, C2); a no-fee Sharpe difference counts as real only at p < 0.0125.

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@euw/slip (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@euw/slip | 0.62 (0.27) | +3.5% | 5.8% | 13.0% | 2.9 | 67% | 0.70 | 0.40 | 0.79 | - | - |
| V0-w-fri@euw/slip | 0.63 (0.27) | +3.6% | 5.8% | 13.2% | 4.1 | 67% | 0.68 | 0.41 | 0.84 | +0.01 (p=0.13; -0.00..+0.04) | 2/3 |
| C1-confirm2@euw/slip | 0.62 (0.28) | +3.6% | 6.0% | 16.3% | 1.5 | 67% | 0.64 | 0.33 | 0.96 | -0.00 (p=0.48; -0.12..+0.12) | 1/3 |
| C2-dz25@euw/slip | 0.64 (0.28) | +3.8% | 6.1% | 15.4% | 1.1 | 67% | 0.63 | 0.38 | 1.00 | +0.03 (p=0.36; -0.10..+0.17) | 1/3 |
| equal-weight@euw/slip | 0.77 (0.27) | +6.3% | 8.4% | 19.8% | 0.2 | 100% | 0.67 | 0.82 | 0.82 | +0.15 (p=0.14; -0.07..+0.39) | 2/3 |

Crash windows (total return inside each, no fixed fee):

| Run | 2011 euro crisis | 2015-16 | 2018-Q4 | 2020 covid | 2022 rate shock |
|---|---:|---:|---:|---:|---:|
| tsmom12@euw/slip | - | -7.8% | -3.9% | -11.6% | +2.2% |
| C1-confirm2@euw/slip | - | -9.7% | -3.1% | -14.6% | +2.0% |
| C2-dz25@euw/slip | - | -9.5% | -3.6% | -14.3% | +1.9% |
| equal-weight@euw/slip | - | -14.6% | -3.2% | -18.7% | -7.6% |

## 2. Robustness: the same reducers on `eu6` (EUR, coins) and `usw` (USD)

Tests 1 and 2 against `R` on the same book (a reducer must pass both on at least one of the two books, else it is 'fragile').

| Book | Rule | Signal flips/yr | Orders/yr | Sharpe | dSharpe vs R | Max DD | dMax DD | Position corr (agree) | Tests 1+2 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| eu6 | R `tsmom12` | 11.8 | - | 1.449 | - | 31.0% | - | - | (reference) |
| eu6 | C1-confirm2 | 6.7 | 38.3 | 1.405 | -0.044 | 32.6% | +1.7 pts | 0.91 (97%) | yes |
| eu6 | C2-dz25 | 4.4 | 35.5 | 1.445 | -0.004 | 31.7% | +0.8 pts | 0.87 (96%) | yes |
| usw | R `tsmom12` | 20.9 | - | 0.629 | - | 11.1% | - | - | (reference) |
| usw | C1-confirm2 | 12.3 | 23.1 | 0.611 | -0.018 | 12.2% | +1.1 pts | 0.90 (95%) | yes |
| usw | C2-dz25 | 7.7 | 18.2 | 0.561 | -0.069 | 14.3% | +3.2 pts | 0.87 (94%) | **no** |

`eu6`:

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@eu6/slip-b1 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@eu6/slip-b1 | 1.45 (0.28) | +31.8% | 20.5% | 31.0% | 3.1 | 78% | 1.90 | 1.49 | 0.86 | - | - |
| C1-confirm2@eu6/slip | 1.40 (0.28) | +30.8% | 20.7% | 32.6% | 2.4 | 79% | 1.92 | 1.44 | 0.74 | -0.04 (p=0.89; -0.11..+0.01) | 1/3 |
| C2-dz25@eu6/slip | 1.45 (0.28) | +32.0% | 20.7% | 31.7% | 1.8 | 79% | 1.92 | 1.53 | 0.75 | -0.00 (p=0.53; -0.08..+0.07) | 2/3 |

`usw`:

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@usw (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@usw | 0.63 (0.27) | +3.6% | 5.9% | 11.1% | 3.0 | 61% | 0.20 | 0.82 | 0.81 | - | - |
| C1-confirm2@usw/slip | 0.61 (0.27) | +3.6% | 6.0% | 12.2% | 1.9 | 61% | 0.32 | 0.60 | 0.91 | -0.02 (p=0.61; -0.12..+0.09) | 2/3 |
| C2-dz25@usw/slip | 0.56 (0.28) | +3.3% | 6.2% | 14.3% | 1.2 | 60% | 0.34 | 0.51 | 0.85 | -0.07 (p=0.77; -0.19..+0.07) | 2/3 |

Keeps the character (euw tests 1-4 and robust on >= 1 other book): C1-confirm2 **no**, C2-dz25 **no**.

## 3. Fixed fees by book size on `euw`

R's Sharpe at no fee 0.617; R's gap to equal weight at no fee -0.15. Loss = max(own Sharpe at no fee, R's) minus Sharpe under the tier (eu-3's strict reading). Predicted = fixed fees per year / the rule's vol at no fee. Worth it = keeps the character, loss <= 0.10, gap to equal weight (same tier and book) within 0.15 of R's.

| Rule | Tier | Book | Sharpe | Loss | Predicted | Gap (EW Sharpe) | Max DD | Orders/yr | Fixed fees/yr | Worth it |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| R | EUR 1 | 5k | 0.505 | 0.112 | 0.113 | -0.23 (0.73) | 15.9% | 29.8 | 0.66% | **no** |
| R | EUR 1 | 10k | 0.558 | 0.058 | 0.057 | -0.19 (0.75) | 14.4% | 29.9 | 0.33% | yes |
| R | EUR 1 | 25k | 0.593 | 0.023 | 0.023 | -0.17 (0.76) | 13.4% | 29.9 | 0.13% | yes |
| R | EUR 2 | 5k | 0.411 | 0.206 | 0.205 | -0.29 (0.70) | 18.5% | 29.9 | 1.20% | **no** |
| R | EUR 2 | 10k | 0.512 | 0.104 | 0.102 | -0.22 (0.73) | 15.7% | 29.9 | 0.60% | **no** |
| R | EUR 2 | 25k | 0.574 | 0.043 | 0.041 | -0.18 (0.75) | 14.0% | 30.1 | 0.24% | yes |
| R | EUR 3 | 5k | 0.293 | 0.323 | 0.325 | -0.36 (0.66) | 21.5% | 30.5 | 1.90% | **no** |
| R | EUR 3 | 10k | 0.457 | 0.159 | 0.160 | -0.26 (0.71) | 17.2% | 30.1 | 0.94% | **no** |
| R | EUR 3 | 25k | 0.550 | 0.067 | 0.063 | -0.20 (0.75) | 14.6% | 29.7 | 0.37% | yes |
| V0 | EUR 1 | 5k | 0.525 | 0.105 | 0.106 | -0.21 (0.73) | 15.7% | 27.8 | 0.62% | **no** |
| V0 | EUR 1 | 10k | 0.576 | 0.054 | 0.053 | -0.17 (0.75) | 14.3% | 27.6 | 0.31% | yes |
| V0 | EUR 1 | 25k | 0.610 | 0.020 | 0.021 | -0.15 (0.76) | 13.6% | 27.8 | 0.12% | yes |
| V0 | EUR 2 | 5k | 0.438 | 0.192 | 0.193 | -0.26 (0.70) | 18.2% | 28.2 | 1.13% | **no** |
| V0 | EUR 2 | 10k | 0.532 | 0.098 | 0.095 | -0.20 (0.73) | 15.5% | 27.8 | 0.56% | yes |
| V0 | EUR 2 | 25k | 0.588 | 0.042 | 0.038 | -0.17 (0.75) | 14.0% | 27.8 | 0.22% | yes |
| V0 | EUR 3 | 5k | 0.330 | 0.301 | 0.304 | -0.33 (0.66) | 21.1% | 28.5 | 1.77% | **no** |
| V0 | EUR 3 | 10k | 0.483 | 0.147 | 0.149 | -0.23 (0.71) | 16.9% | 28.0 | 0.87% | **no** |
| V0 | EUR 3 | 25k | 0.569 | 0.061 | 0.059 | -0.18 (0.75) | 14.5% | 27.6 | 0.34% | yes |
| C1-confirm2 | EUR 1 | 5k | 0.537 | 0.080 | 0.077 | -0.19 (0.73) | 18.3% | 20.0 | 0.46% | **no** |
| C1-confirm2 | EUR 1 | 10k | 0.579 | 0.037 | 0.039 | -0.17 (0.75) | 17.2% | 20.3 | 0.24% | **no** |
| C1-confirm2 | EUR 1 | 25k | 0.602 | 0.015 | 0.016 | -0.16 (0.76) | 16.6% | 20.1 | 0.09% | **no** |
| C1-confirm2 | EUR 2 | 5k | 0.477 | 0.140 | 0.134 | -0.22 (0.70) | 19.8% | 20.1 | 0.80% | **no** |
| C1-confirm2 | EUR 2 | 10k | 0.544 | 0.072 | 0.067 | -0.19 (0.73) | 18.1% | 20.0 | 0.40% | **no** |
| C1-confirm2 | EUR 2 | 25k | 0.590 | 0.026 | 0.027 | -0.16 (0.75) | 16.9% | 20.2 | 0.16% | **no** |
| C1-confirm2 | EUR 3 | 5k | 0.407 | 0.210 | 0.210 | -0.25 (0.66) | 21.6% | 19.9 | 1.26% | **no** |
| C1-confirm2 | EUR 3 | 10k | 0.507 | 0.110 | 0.106 | -0.21 (0.71) | 19.0% | 20.2 | 0.64% | **no** |
| C1-confirm2 | EUR 3 | 25k | 0.572 | 0.044 | 0.043 | -0.18 (0.75) | 17.4% | 20.2 | 0.26% | **no** |
| C2-dz25 | EUR 1 | 5k | 0.581 | 0.061 | 0.065 | -0.15 (0.73) | 16.5% | 16.5 | 0.40% | **no** |
| C2-dz25 | EUR 1 | 10k | 0.612 | 0.030 | 0.032 | -0.14 (0.75) | 15.9% | 16.3 | 0.20% | **no** |
| C2-dz25 | EUR 1 | 25k | 0.628 | 0.014 | 0.013 | -0.13 (0.76) | 15.5% | 16.4 | 0.08% | **no** |
| C2-dz25 | EUR 2 | 5k | 0.532 | 0.110 | 0.109 | -0.17 (0.70) | 17.7% | 16.5 | 0.66% | **no** |
| C2-dz25 | EUR 2 | 10k | 0.586 | 0.056 | 0.054 | -0.15 (0.73) | 16.5% | 16.4 | 0.33% | **no** |
| C2-dz25 | EUR 2 | 25k | 0.620 | 0.022 | 0.022 | -0.13 (0.75) | 15.6% | 16.3 | 0.13% | **no** |
| C2-dz25 | EUR 3 | 5k | 0.470 | 0.172 | 0.178 | -0.19 (0.66) | 19.5% | 16.9 | 1.08% | **no** |
| C2-dz25 | EUR 3 | 10k | 0.557 | 0.086 | 0.086 | -0.16 (0.71) | 17.1% | 16.4 | 0.52% | **no** |
| C2-dz25 | EUR 3 | 25k | 0.609 | 0.034 | 0.035 | -0.14 (0.75) | 16.0% | 16.4 | 0.21% | **no** |

## 4. Minimum book (fee loss <= 0.10)

Interpolated linearly in 1/size between the tested books (eu-2's method); mechanical = (orders a year x fee per order + yearly fee) / (0.10 x the rule's vol at no fee).

| Rule | Tier | Minimum book (tested) | Mechanical | Loss 5k | 10k | 25k | Keeps character |
|---|---|---|---|---:|---:|---:|---|
| R | EUR 1 | ~6k | ~5.6k | 0.112 | 0.058 | 0.023 | yes |
| R | EUR 2 | ~10k | ~10.3k | 0.206 | 0.104 | 0.043 | yes |
| R | EUR 3 | ~16k | ~15.9k | 0.323 | 0.159 | 0.067 | yes |
| V0 | EUR 1 | ~5k | ~5.2k | 0.105 | 0.054 | 0.020 | yes |
| V0 | EUR 2 | ~10k | ~9.6k | 0.192 | 0.098 | 0.042 | yes |
| V0 | EUR 3 | ~15k | ~14.8k | 0.301 | 0.147 | 0.061 | yes |
| C1-confirm2 | EUR 1 | <= 5k | ~3.8k | 0.080 | 0.037 | 0.015 | no |
| C1-confirm2 | EUR 2 | ~7k | ~6.7k | 0.140 | 0.072 | 0.026 | no |
| C1-confirm2 | EUR 3 | ~11k | ~10.4k | 0.210 | 0.110 | 0.044 | no |
| C2-dz25 | EUR 1 | <= 5k | ~3.2k | 0.061 | 0.030 | 0.014 | no |
| C2-dz25 | EUR 2 | ~6k | ~5.5k | 0.110 | 0.056 | 0.022 | no |
| C2-dz25 | EUR 3 | ~9k | ~8.6k | 0.172 | 0.086 | 0.034 | no |

## 5. Verdict grid: is `euw` worth running?

| Tier | EUR 5k | EUR 10k | EUR 25k |
|---|---|---|---|
| EUR 1 | **no** | yes (R, V0) | yes (R, V0) |
| EUR 2 | **no** | yes (V0) | yes (R, V0) |
| EUR 3 | **no** | **no** | yes (R, V0) |

Rescued at EUR 5-10k where neither R nor V0 is worth it: **no**.
