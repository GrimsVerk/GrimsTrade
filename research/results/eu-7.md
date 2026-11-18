# eu-7 results: trend on stocks only (A), hold-seven with fixed cash (B) (cards/eu-7.md)

Train only. `euw` in EUR, window W (decisions 2012-01-02 .. 2025-11-09), total-return prices, ETF slippage 0.05% a side, cash at 0. T = `tsmom12` + 5/25 band (eu-5's D2); A = `tsmom12` slots on SXR8, EXSA, IQQE, IBGS/IBGL/4GLD/EXXY at 1/7 always, band 3.57%; B = all seven at e/7 with e = T's average exposure = 0.67 (cash 33%), band 2.39%; H = equal weight + 5/25 band; M = 60/40 (eu-6, ref). Sharpe on calendar days, zero risk-free rate.

## 1. The human criteria at no fixed fee

| Rule | Sharpe (SE) | CAGR | Vol | Worst loss (max DD) | Longest under water | Worst 12 months | Orders/yr | Avg exposure |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T trend (tsmom12, all seven) | 0.62 (0.27) | +3.7% | 6.1% | 13.6% | 58 mo | -11.5% | 21.1 | 67% |
| A trend on stocks only | 0.60 (0.27) | +4.0% | 6.9% | 16.1% | 56 mo | -13.1% | 10.1 | 89% |
| B hold7 + fixed cash | 0.79 (0.27) | +4.5% | 5.8% | 13.8% | 31 mo | -8.3% | 2.3 | 67% |
| H hold7 | 0.78 (0.27) | +6.3% | 8.3% | 19.8% | 31 mo | -11.4% | 1.9 | 100% |
| M mix60 (ref) | 0.75 (0.27) | +7.0% | 9.6% | 22.3% | 31 mo | -15.7% | 1.2 | 100% |

## 2. Sharpe differences (no fixed fee)

Paired stationary bootstrap (block 20 days, 2,000 draws, seed 0). A lead of A or B counts as real only at p < 0.0083 (eu family 12).

| Pair | dSharpe | Bootstrap SE | 90% range | p (first better) | p (second better) |
|---|---:|---:|---|---:|---:|
| A - T | -0.02 | 0.08 | -0.15 .. +0.12 | 0.600 | 0.400 |
| A - H | -0.18 | 0.09 | -0.34 .. -0.03 | 0.971 | 0.029 |
| B - T | +0.17 | 0.13 | -0.04 .. +0.40 | 0.101 | 0.899 |
| B - H | +0.01 | 0.02 | -0.01 .. +0.04 | 0.261 | 0.739 |
| A - B | -0.19 | 0.09 | -0.34 .. -0.04 | 0.978 | 0.022 |

## 3. Crash windows (total return inside each)

| Window | T trend (tsmom12, all seven) | A trend on stocks only | B hold7 + fixed cash | H hold7 | M mix60 (ref) | Best of T/A/B/H (within 1 pt) |
|---|---:|---:|---:|---:|---:|---|
| 2000-02 (long monthly proxy) | +8.8% | +12.7% | -0.7% | -1.2% | -14.3% | A |
| 2008 (usw proxy, USD) | -0.7% | -0.8% | -15.7% | -23.1% | -30.4% | T, A |
| 2015-16 | -8.2% | -11.2% | -10.0% | -13.8% | -13.8% | T |
| 2018-Q4 | -4.2% | -1.7% | -2.5% | -3.4% | -5.5% | A, B |
| 2020 covid | -12.2% | -14.5% | -13.0% | -18.7% | -22.1% | T, B |
| 2022 rate shock | +1.7% | -3.8% | -4.3% | -6.7% | -17.4% | T |
| 2008, second view (long monthly proxy; not counted) | +9.3% | +10.5% | -4.7% | -7.2% | -27.0% | - |

Windows best (of 6, within 1 pt): T 4, A 3, B 2, H 0. Windows within 3 pts of T: A 4, B 3.

Proxy books in full (shown, not judged):

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs T @usw 2007- (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| T @usw 2007- | 0.64 (0.23) | +4.4% | 7.2% | 10.9% | 2.7 | 65% | 0.71 | 0.35 | 0.85 | 0.85 | - | - |
| A @usw 2007- | 0.67 (0.23) | +5.1% | 7.8% | 14.1% | 1.2 | 87% | 0.80 | 0.33 | 0.98 | 0.79 | +0.03 (p=0.35; -0.10..+0.17) | 2/4 |
| B @usw 2007- | 0.60 (0.23) | +4.3% | 7.5% | 22.1% | 0.1 | 67% | 0.44 | 0.43 | 1.05 | 0.71 | -0.04 (p=0.59; -0.29..+0.23) | 2/4 |
| H @usw 2007- | 0.63 (0.23) | +6.5% | 10.9% | 32.0% | 0.1 | 100% | 0.44 | 0.47 | 1.12 | 0.71 | -0.01 (p=0.50; -0.27..+0.28) | 2/4 |

Long monthly proxy (stocks / 10y Treasuries / gold, 1972-2025, monthly averages, cash at 0, no fees; Sharpe from monthly returns):

| Rule | Sharpe | CAGR | Max DD | Turnover/yr |
|---|---:|---:|---:|---:|
| T proxy | 1.26 | +8.1% | 12.5% | 1.12 |
| A proxy | 1.24 | +8.7% | 19.4% | 0.44 |
| B proxy | 1.20 | +6.2% | 14.3% | 0.19 |
| H proxy | 1.20 | +9.2% | 20.8% | 0.27 |
| M proxy | 1.14 | +9.4% | 27.0% | 0.19 |

## 4. The card's answer: keep the insurance, lose less of the rest?

| Rule | Max DD vs T (<= +2 pts) | Crash windows within 3 pts of T (>= 5 of 6) | Keeps insurance | Sharpe vs T (>= +0.05; p) | Under water vs T (>= 3 mo shorter) | Orders vs T (>= 25% fewer) | Gains (>= 2 of 3) | Held-out card? |
|---|---|---|---|---|---|---|---|---|
| A trend on stocks only | +2.4% (**no**) | 4 (**no**) | **no** | -0.02 (p=0.600, not real; **no**) | -2 mo (**no**) | -52% (yes) | 1 (**no**) | **no** |
| B hold7 + fixed cash | +0.1% (yes) | 3 (**no**) | **no** | +0.17 (p=0.101, not real; yes) | -28 mo (yes) | -89% (yes) | 3 (yes) | **no** |

Neither rule passes both tests: the held-out year stays unspent.

## 5. Fixed fees by tier and book

Loss = own Sharpe at no fee minus Sharpe at the tier. P1 winner = highest Sharpe at the cell; 'real' only if the bootstrap p of the leader vs the runner-up < 0.0083, else a tie, decided by fewer orders a year at no fee.

| Tier | Book | T Sharpe (loss; orders; fees/yr) | A Sharpe (loss; orders; fees/yr) | B Sharpe (loss; orders; fees/yr) | H Sharpe (loss; orders; fees/yr) | P1 winner |
|---|---:|---|---|---|---|---|
| EUR 1 | 5k | 0.55 (0.070; 21.1; 0.49%) | 0.57 (0.033; 10.2; 0.27%) | 0.76 (0.027; 2.2; 0.11%) | 0.76 (0.017; 1.9; 0.10%) | tie B~H (p=0.48) -> H |
| EUR 1 | 10k | 0.59 (0.039; 21.0; 0.24%) | 0.59 (0.017; 10.2; 0.13%) | 0.77 (0.019; 2.2; 0.05%) | 0.77 (0.007; 1.9; 0.05%) | tie H~B (p=0.44) -> H |
| EUR 1 | 25k | 0.61 (0.016; 21.0; 0.10%) | 0.60 (0.006; 10.1; 0.05%) | 0.78 (0.007; 2.2; 0.02%) | 0.78 (0.002; 1.9; 0.02%) | tie B~H (p=0.38) -> H |
| EUR 2 | 5k | 0.49 (0.130; 21.1; 0.85%) | 0.55 (0.052; 10.2; 0.41%) | 0.76 (0.027; 2.2; 0.09%) | 0.76 (0.017; 1.9; 0.08%) | tie B~H (p=0.48) -> H |
| EUR 2 | 10k | 0.56 (0.062; 21.1; 0.42%) | 0.58 (0.026; 10.2; 0.20%) | 0.77 (0.019; 2.2; 0.04%) | 0.77 (0.007; 1.9; 0.04%) | tie H~B (p=0.45) -> H |
| EUR 2 | 25k | 0.60 (0.028; 21.0; 0.17%) | 0.59 (0.010; 10.2; 0.08%) | 0.78 (0.007; 2.2; 0.02%) | 0.77 (0.009; 1.9; 0.02%) | tie B~H (p=0.23) -> H |
| EUR 3 | 5k | 0.42 (0.209; 21.1; 1.33%) | 0.51 (0.097; 10.3; 0.68%) | 0.75 (0.043; 2.2; 0.19%) | 0.75 (0.031; 1.8; 0.17%) | tie H~B (p=0.45) -> H |
| EUR 3 | 10k | 0.53 (0.098; 21.1; 0.67%) | 0.56 (0.042; 10.2; 0.34%) | 0.76 (0.027; 2.2; 0.10%) | 0.76 (0.017; 1.9; 0.09%) | tie B~H (p=0.49) -> H |
| EUR 3 | 25k | 0.58 (0.044; 21.0; 0.26%) | 0.59 (0.018; 10.2; 0.14%) | 0.78 (0.009; 2.3; 0.04%) | 0.77 (0.005; 1.9; 0.04%) | tie B~H (p=0.36) -> H |

## 6. Which wins under which preference (among T, A, B, H)

| Preference | Winner | Why |
|---|---|---|
| P1 Sharpe after fees | per cell, table 5 | EUR 1 5k: H, EUR 1 10k: H, EUR 1 25k: H, EUR 2 5k: H, EUR 2 10k: H, EUR 2 25k: H, EUR 3 5k: H, EUR 3 10k: H, EUR 3 25k: H |
| P2 worst loss | **B** | max DD T 13.6%, A 16.1%, B 13.8%, H 19.8%; tie band 2 pts (candidates T, B; then worst 12 months T -11.5%, B -8.3%) |
| P3 waiting | **H** | longest under water T 58 mo, A 56 mo, B 31 mo, H 31 mo (tie band 3 mo: B, H; then fewer orders) |
| P4 crash insurance | **T** | windows best of 6: T 4, A 3, B 2, H 0 |
| P5 cost | **H** | orders/yr T 21.1, A 10.1, B 2.3, H 1.9 |

## 7. Worth running? (the winner of the preference, if its fee loss <= 0.10)

| Preference | EUR 1 5k | EUR 1 10k | EUR 1 25k | EUR 2 5k | EUR 2 10k | EUR 2 25k | EUR 3 5k | EUR 3 10k | EUR 3 25k |
|---|---|---|---|---|---|---|---|---|---|
| P1 Sharpe | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) |
| P2 worst loss | B (yes) | B (yes) | B (yes) | B (yes) | B (yes) | B (yes) | B (yes) | B (yes) | B (yes) |
| P3 waiting | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) |
| P4 crash insurance | T (yes) | T (yes) | T (yes) | T (no: fees) | T (yes) | T (yes) | T (no: fees) | T (yes) | T (yes) |
| P5 cost | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) | H (yes) |

Descriptive: vol B 5.8%, T 6.1%; Sharpe B 0.79, H 0.78 (cash at 0: holding less scales return and risk).
