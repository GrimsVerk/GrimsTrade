# eu-5 results: drift-only order cutters on `euw` (cards/eu-5.md)

Train period only, window W (decisions 2012-01-02 .. 2025-11-09). Total-return prices; `euw` and `eu6` in EUR, `usw` in USD. Sharpe on calendar days, zero risk-free rate. `euw`/`eu6`: ETF slippage 0.05% a side (eu-2's costs; coins at the gym's); `usw`: the gym's costs. `R` = the house rule `tsmom12` (weights sent daily, 1% band). Both rules keep R's held set on every Friday. D1 `flipreb` = R's target sent only on days the held set changes (drift traded only then, 1% band); D2 `band25r` = R's daily target with a band of min(5%, 25% of the 1/n target) of the book (3.57% on `euw`/`usw`, 4.17% on `eu6`). Fee tiers: EUR 1, 2, 3 per ETF order on a constant book (eu-2's schedules; the EUR 1 and EUR 3 tiers also carry a EUR 2.50 yearly fee). `R`, V0 and equal weight on `euw` are eu-3's saved runs, re-scored.

## 1. Character on `euw` at no fixed fee

| Rule | Orders/yr | Entries | Exits | Drift | Sharpe | Max DD | 1. Realised-weight corr (mean gap; held-state corr) | 2. dSharpe | 3. dMax DD | 4. Crash signs match / worst window gap | Keeps character (euw) |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| R `tsmom12` | 30.1 | 10.2 | 9.8 | 10.0 | 0.617 | 13.0% | - | - | - | - | (reference) |
| V0 (eu-3) | 27.9 | 10.2 | 9.8 | 7.9 | 0.630 | 13.2% | - | +0.014 | - | - | yes (eu-3) |
| D1-flipreb | 25.3 | 10.2 | 9.8 | 5.3 | 0.609 | 13.7% | 1.00 (0.20%; 1.00) yes | -0.008 yes | +0.7 pts yes | 4/4, 0.4 pts yes | yes |
| D2-band25r | 21.1 | 10.2 | 9.8 | 1.1 | 0.624 | 13.6% | 0.99 (0.51%; 1.00) yes | +0.008 yes | +0.6 pts yes | 4/4, 0.5 pts yes | yes |

D1 event days (decisions sent): 16.7 a year. Entries/exits differ slightly from R's only through count rules (a fill is an entry when the slot was empty).

Family bar: 10 selectable variants (eu-3's V0-V5, eu-4's C1, C2, D1, D2); a no-fee Sharpe difference counts as real only at p < 0.010.

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@euw/slip (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@euw/slip | 0.62 (0.27) | +3.5% | 5.8% | 13.0% | 2.9 | 67% | 0.70 | 0.40 | 0.79 | - | - |
| V0-w-fri@euw/slip | 0.63 (0.27) | +3.6% | 5.8% | 13.2% | 4.1 | 67% | 0.68 | 0.41 | 0.84 | +0.01 (p=0.13; -0.00..+0.04) | 2/3 |
| D1-flipreb@euw/slip | 0.61 (0.27) | +3.5% | 5.9% | 13.7% | 4.1 | 65% | 0.68 | 0.40 | 0.78 | -0.01 (p=0.80; -0.02..+0.01) | 1/3 |
| D2-band25r@euw/slip | 0.62 (0.27) | +3.7% | 6.1% | 13.6% | 2.8 | 67% | 0.70 | 0.44 | 0.76 | +0.01 (p=0.29; -0.02..+0.03) | 1/3 |
| equal-weight@euw/slip | 0.77 (0.27) | +6.3% | 8.4% | 19.8% | 0.2 | 100% | 0.67 | 0.82 | 0.82 | +0.15 (p=0.14; -0.07..+0.39) | 2/3 |

Crash windows (total return inside each, no fixed fee):

| Run | 2011 euro crisis | 2015-16 | 2018-Q4 | 2020 covid | 2022 rate shock |
|---|---:|---:|---:|---:|---:|
| tsmom12@euw/slip | - | -7.8% | -3.9% | -11.6% | +2.2% |
| D1-flipreb@euw/slip | - | -8.2% | -3.9% | -11.7% | +2.1% |
| D2-band25r@euw/slip | - | -8.2% | -4.2% | -12.2% | +1.7% |
| equal-weight@euw/slip | - | -14.6% | -3.2% | -18.7% | -7.6% |

## 2. Robustness: the same rules on `eu6` (EUR, coins) and `usw` (USD)

Tests 1 and 2 against `R` on the same book (a rule must pass both on at least one of the two books, else it is 'fragile'). Max DD and orders shown, not judged.

| Book | Rule | Orders/yr (drift) | Sharpe | dSharpe vs R | Max DD | dMax DD | Realised-weight corr (mean gap) | Tests 1+2 |
|---|---|---:|---:|---:|---:|---:|---|---|
| eu6 | R `tsmom12` | 42.3 (32.7) | 1.449 | - | 31.0% | - | - | (reference) |
| eu6 | D1-flipreb | 16.9 (7.3) | 1.179 | -0.270 | 64.7% | +33.8 pts | 0.73 (2.30%) | **no** |
| eu6 | D2-band25r | 12.1 (2.5) | 1.484 | +0.035 | 30.5% | -0.5 pts | 0.99 (0.91%) | yes |
| usw | R `tsmom12` | 30.4 (9.3) | 0.629 | - | 11.1% | - | - | (reference) |
| usw | D1-flipreb | 26.8 (5.7) | 0.644 | +0.014 | 10.7% | -0.4 pts | 1.00 (0.16%) | yes |
| usw | D2-band25r | 22.3 (1.2) | 0.657 | +0.028 | 10.9% | -0.2 pts | 0.99 (0.49%) | yes |

`eu6`:

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@eu6 (R) (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@eu6 (R) | 1.45 (0.28) | +31.8% | 20.5% | 31.0% | 3.1 | 78% | 1.90 | 1.49 | 0.86 | - | - |
| D1-flipreb@eu6/slip | 1.18 (0.28) | +46.4% | 38.9% | 64.7% | 2.5 | 72% | 1.24 | 1.64 | 0.82 | -0.27 (p=0.91; -0.57..+0.06) | 1/3 |
| D2-band25r@eu6/slip | 1.48 (0.28) | +32.6% | 20.4% | 30.5% | 2.4 | 78% | 1.91 | 1.55 | 0.87 | +0.04 (p=0.08; -0.01..+0.07) | 3/3 |

`usw`:

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@usw (R) (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@usw (R) | 0.63 (0.27) | +3.6% | 5.9% | 11.1% | 3.0 | 61% | 0.20 | 0.82 | 0.81 | - | - |
| D1-flipreb@usw/slip | 0.64 (0.27) | +3.7% | 5.8% | 10.7% | 4.3 | 61% | 0.20 | 0.85 | 0.81 | +0.01 (p=0.10; -0.00..+0.03) | 3/3 |
| D2-band25r@usw/slip | 0.66 (0.27) | +3.9% | 6.1% | 10.9% | 2.9 | 61% | 0.21 | 0.85 | 0.85 | +0.03 (p=0.05; +0.00..+0.06) | 3/3 |

Keeps the character (euw tests 1-4 and robust on >= 1 other book): D1-flipreb **yes**, D2-band25r **yes**.

Pick (fewest orders at no fee among those keeping the character): **D2-band25r**.

## 3. Fixed fees by book size on `euw`

R's Sharpe at no fee 0.617; R's gap to equal weight at no fee -0.15. Loss = max(own Sharpe at no fee, R's) minus Sharpe under the tier. Predicted = fixed fees per year / the rule's vol at no fee. Worth it = keeps the character, loss <= 0.10, gap to equal weight (same tier and book) within 0.15 of R's.

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
| D1-flipreb | EUR 1 | 5k | 0.513 | 0.103 | 0.096 | -0.22 (0.73) | 16.3% | 25.2 | 0.57% | **no** |
| D1-flipreb | EUR 1 | 10k | 0.560 | 0.056 | 0.048 | -0.19 (0.75) | 14.9% | 25.2 | 0.28% | yes |
| D1-flipreb | EUR 1 | 25k | 0.590 | 0.027 | 0.019 | -0.17 (0.76) | 14.1% | 25.3 | 0.11% | yes |
| D1-flipreb | EUR 2 | 5k | 0.441 | 0.176 | 0.170 | -0.26 (0.70) | 18.6% | 25.2 | 1.01% | **no** |
| D1-flipreb | EUR 2 | 10k | 0.521 | 0.096 | 0.085 | -0.21 (0.73) | 16.1% | 25.2 | 0.50% | yes |
| D1-flipreb | EUR 2 | 25k | 0.573 | 0.043 | 0.034 | -0.18 (0.75) | 14.6% | 25.2 | 0.20% | yes |
| D1-flipreb | EUR 3 | 5k | 0.347 | 0.269 | 0.269 | -0.31 (0.66) | 21.4% | 25.5 | 1.60% | **no** |
| D1-flipreb | EUR 3 | 10k | 0.477 | 0.139 | 0.133 | -0.24 (0.71) | 17.4% | 25.1 | 0.79% | **no** |
| D1-flipreb | EUR 3 | 25k | 0.554 | 0.063 | 0.053 | -0.19 (0.75) | 15.1% | 25.2 | 0.32% | yes |
| D2-band25r | EUR 1 | 5k | 0.554 | 0.070 | 0.080 | -0.18 (0.73) | 15.3% | 21.1 | 0.49% | yes |
| D2-band25r | EUR 1 | 10k | 0.585 | 0.039 | 0.040 | -0.16 (0.75) | 14.5% | 21.0 | 0.24% | yes |
| D2-band25r | EUR 1 | 25k | 0.608 | 0.016 | 0.016 | -0.15 (0.76) | 14.0% | 21.0 | 0.10% | yes |
| D2-band25r | EUR 2 | 5k | 0.495 | 0.130 | 0.140 | -0.20 (0.70) | 17.3% | 21.1 | 0.85% | **no** |
| D2-band25r | EUR 2 | 10k | 0.562 | 0.062 | 0.070 | -0.17 (0.73) | 15.1% | 21.1 | 0.42% | yes |
| D2-band25r | EUR 2 | 25k | 0.596 | 0.028 | 0.028 | -0.16 (0.75) | 14.2% | 21.0 | 0.17% | yes |
| D2-band25r | EUR 3 | 5k | 0.416 | 0.209 | 0.220 | -0.24 (0.66) | 19.5% | 21.1 | 1.33% | **no** |
| D2-band25r | EUR 3 | 10k | 0.526 | 0.098 | 0.110 | -0.19 (0.71) | 16.4% | 21.1 | 0.67% | yes |
| D2-band25r | EUR 3 | 25k | 0.581 | 0.044 | 0.044 | -0.17 (0.75) | 14.6% | 21.0 | 0.26% | yes |

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
| D1-flipreb | EUR 1 | ~5k | ~4.7k | 0.103 | 0.056 | 0.027 | yes |
| D1-flipreb | EUR 2 | ~9k | ~8.5k | 0.176 | 0.096 | 0.043 | yes |
| D1-flipreb | EUR 3 | ~14k | ~13.2k | 0.269 | 0.139 | 0.063 | yes |
| D2-band25r | EUR 1 | <= 5k | ~3.9k | 0.070 | 0.039 | 0.016 | yes |
| D2-band25r | EUR 2 | ~6k | ~7.0k | 0.130 | 0.062 | 0.028 | yes |
| D2-band25r | EUR 3 | ~10k | ~10.9k | 0.209 | 0.098 | 0.044 | yes |

## 5. Verdict grid: is `euw` worth running?

| Tier | EUR 5k | EUR 10k | EUR 25k |
|---|---|---|---|
| EUR 1 | yes (D2-band25r) | yes (R, V0, D1-flipreb, D2-band25r) | yes (R, V0, D1-flipreb, D2-band25r) |
| EUR 2 | **no** | yes (V0, D1-flipreb, D2-band25r) | yes (R, V0, D1-flipreb, D2-band25r) |
| EUR 3 | **no** | yes (D2-band25r) | yes (R, V0, D1-flipreb, D2-band25r) |

Rescued at EUR 5-10k where neither R nor V0 is worth it: **yes (EUR 1 5k, EUR 3 10k)**.
