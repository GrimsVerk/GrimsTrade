# eu-6 results: trend vs holding vs 60/40 on `euw` (cards/eu-6.md)

Train only. `euw` in EUR, window W (decisions 2012-01-02 .. 2025-11-09), total-return prices, ETF slippage 0.05% a side, cash at 0. T = `tsmom12` + 5/25 band (eu-5's D2, re-scored); H = equal weight of the seven + 5/25 band (3.57%); M = SXR8, EXSA, IQQE, IBGS, IBGL 20% each + 5% band. Sharpe on calendar days, zero risk-free rate.

## 1. The human criteria at no fixed fee

| Rule | Sharpe (SE) | CAGR | Vol | Worst loss (max DD) | Longest under water | Worst 12 months | Orders/yr | Avg exposure |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T trend (tsmom12 + 5/25) | 0.62 (0.27) | +3.7% | 6.1% | 13.6% | 58 mo | -11.5% | 21.1 | 67% |
| H hold7 (EW + 5/25) | 0.78 (0.27) | +6.3% | 8.3% | 19.8% | 31 mo | -11.4% | 1.9 | 100% |
| M mix60 (60/40 + 5%) | 0.75 (0.27) | +7.0% | 9.6% | 22.3% | 31 mo | -15.7% | 1.2 | 100% |
| R tsmom12 (1% band, ref) | 0.62 (0.27) | +3.5% | 5.8% | 13.0% | 78 mo | -11.0% | 30.1 | 67% |
| EW (1% band, ref) | 0.77 (0.27) | +6.3% | 8.4% | 19.8% | 24 mo | -11.9% | 15.6 | 100% |

Descriptive (no row, hindsight constant): H scaled to T's vol (73% invested, rest cash at 0): Sharpe 0.78, CAGR +4.6%, worst loss 14.8%, longest under water 31 mo, worst 12 months -8.3%.

## 2. Sharpe differences and their uncertainty (no fixed fee)

Paired stationary bootstrap (block 20 days, 2,000 draws). A lead is real only at p < 0.033 (three comparisons).

| Pair | dSharpe | Bootstrap SE | 90% range | p (first better) | p (second better) |
|---|---:|---:|---|---:|---:|
| T - H | -0.16 | 0.14 | -0.39 .. +0.06 | 0.88 | 0.12 |
| T - M | -0.13 | 0.17 | -0.41 .. +0.16 | 0.77 | 0.23 |
| H - M | +0.03 | 0.10 | -0.13 .. +0.19 | 0.38 | 0.62 |

## 3. Crash windows (total return inside each)

| Window | T trend (tsmom12 + 5/25) | H hold7 (EW + 5/25) | M mix60 (60/40 + 5%) | Best (within 1 pt) |
|---|---:|---:|---:|---|
| 2000-02 (long monthly proxy) | +8.8% | -1.2% | -14.3% | T |
| 2008 (usw proxy, USD) | -0.7% | -23.1% | -30.4% | T |
| 2015-16 | -8.2% | -13.8% | -13.8% | T |
| 2018-Q4 | -4.2% | -3.4% | -5.5% | T, H |
| 2020 covid | -12.2% | -18.7% | -22.1% | T |
| 2022 rate shock | +1.7% | -6.7% | -17.4% | T |
| 2008, second view (long monthly proxy; not counted) | +9.3% | -7.2% | -27.0% | - |

Windows won (of 6): T 6, H 1, M 0.

Proxy books in full (shown, not judged):

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs T @usw 2007- (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| T @usw 2007- | 0.64 (0.23) | +4.4% | 7.2% | 10.9% | 2.7 | 65% | 0.71 | 0.35 | 0.85 | 0.85 | - | - |
| H @usw 2007- | 0.63 (0.23) | +6.5% | 10.9% | 32.0% | 0.1 | 100% | 0.44 | 0.47 | 1.12 | 0.71 | -0.01 (p=0.50; -0.27..+0.28) | 2/4 |
| M @usw 2007- | 0.54 (0.23) | +5.9% | 11.9% | 32.0% | 0.1 | 100% | 0.29 | 0.64 | 1.02 | 0.35 | -0.09 (p=0.68; -0.38..+0.21) | 2/4 |

Long monthly proxy (stocks / 10y Treasuries / gold, 1972-2025, monthly averages, cash at 0, no fees; Sharpe from monthly returns):

| Rule | Sharpe | CAGR | Max DD | Turnover/yr |
|---|---:|---:|---:|---:|
| T proxy | 1.26 | +8.1% | 12.5% | 1.12 |
| H proxy | 1.20 | +9.2% | 20.8% | 0.27 |
| M proxy | 1.14 | +9.4% | 27.0% | 0.19 |

## 4. Fixed fees by tier and book

Loss = own Sharpe at no fee minus Sharpe at the tier. Winner (P1) = highest Sharpe at the cell; 'real' only if the bootstrap p of the leader vs the runner-up < 0.033, else a tie, decided by fewer orders a year (at no fee).

| Tier | Book | T Sharpe (loss; orders; fees/yr) | H Sharpe (loss; orders; fees/yr) | M Sharpe (loss; orders; fees/yr) | P1 winner | T fee loss <= 0.10 |
|---|---:|---|---|---|---|---|
| EUR 1 | 5k | 0.55 (0.070; 21.1; 0.49%) | 0.76 (0.017; 1.9; 0.10%) | 0.75 (0.008; 1.2; 0.09%) | tie H~M (p=0.41) -> M | yes |
| EUR 1 | 10k | 0.59 (0.039; 21.0; 0.24%) | 0.77 (0.007; 1.9; 0.05%) | 0.75 (0.004; 1.2; 0.04%) | tie H~M (p=0.39) -> M | yes |
| EUR 1 | 25k | 0.61 (0.016; 21.0; 0.10%) | 0.78 (0.002; 1.9; 0.02%) | 0.75 (0.002; 1.2; 0.02%) | tie H~M (p=0.38) -> M | yes |
| EUR 2 | 5k | 0.49 (0.130; 21.1; 0.85%) | 0.76 (0.017; 1.9; 0.08%) | 0.75 (0.006; 1.2; 0.05%) | tie H~M (p=0.42) -> M | no |
| EUR 2 | 10k | 0.56 (0.062; 21.1; 0.42%) | 0.77 (0.007; 1.9; 0.04%) | 0.75 (0.003; 1.2; 0.02%) | tie H~M (p=0.39) -> M | yes |
| EUR 2 | 25k | 0.60 (0.028; 21.0; 0.17%) | 0.77 (0.009; 1.9; 0.02%) | 0.75 (0.001; 1.2; 0.01%) | tie H~M (p=0.41) -> M | yes |
| EUR 3 | 5k | 0.42 (0.209; 21.1; 1.33%) | 0.75 (0.031; 1.8; 0.17%) | 0.74 (0.014; 1.2; 0.14%) | tie H~M (p=0.45) -> M | no |
| EUR 3 | 10k | 0.53 (0.098; 21.1; 0.67%) | 0.76 (0.017; 1.9; 0.09%) | 0.75 (0.007; 1.2; 0.07%) | tie H~M (p=0.41) -> M | yes |
| EUR 3 | 25k | 0.58 (0.044; 21.0; 0.26%) | 0.77 (0.005; 1.9; 0.04%) | 0.75 (0.003; 1.2; 0.03%) | tie H~M (p=0.39) -> M | yes |

## 5. Which wins under which preference

| Preference | Winner | Why |
|---|---|---|
| P1 Sharpe after fees | per cell, table 4 | EUR 1 5k: M, EUR 1 10k: M, EUR 1 25k: M, EUR 2 5k: M, EUR 2 10k: M, EUR 2 25k: M, EUR 3 5k: M, EUR 3 10k: M, EUR 3 25k: M |
| P2 worst loss | **T** | max DD T 13.6%, H 19.8%, M 22.3%; tie band 2% (candidates T; then worst 12 months) |
| P3 waiting | **M** | longest under water T 58 mo, H 31 mo, M 31 mo (tie band 3 mo: H, M; then fewer orders) |
| P4 crash insurance | **T** | windows won of 6: T 6, H 1, M 0 |
| P5 cost | **M** | orders/yr T 21.1, H 1.9, M 1.2 |

## 6. Is trend worth it? (T wins the preference and T's fee loss <= 0.10)

| Preference | EUR 1 5k | EUR 1 10k | EUR 1 25k | EUR 2 5k | EUR 2 10k | EUR 2 25k | EUR 3 5k | EUR 3 10k | EUR 3 25k |
|---|---|---|---|---|---|---|---|---|---|
| P1 Sharpe | no | no | no | no | no | no | no | no | no |
| P2 worst loss | **yes** | **yes** | **yes** | no | **yes** | **yes** | no | **yes** | **yes** |
| P3 waiting | no | no | no | no | no | no | no | no | no |
| P4 crash insurance | **yes** | **yes** | **yes** | no | **yes** | **yes** | no | **yes** | **yes** |
| P5 cost | no | no | no | no | no | no | no | no | no |

Window W is 13.9 years.
