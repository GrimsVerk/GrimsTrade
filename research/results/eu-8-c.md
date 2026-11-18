# eu-8 step 2: idea C, trend on the stock and long-bond funds (cards/eu-8.md)

Train only, cash at 0 (eu-7's terms). C = `tsmom12` slots on SXR8, EXSA, IQQE, IBGL; IBGS, 4GLD, EXXY at 1/7 always; band 3.57%. On `usw`: SPY, EFA, EEM, TLT filtered; IEF, GLD, DBC held. Monthly proxy: stocks and 10y Treasuries filtered, gold held.

## Stage 1: US proxies 1994-2011 (judged first)

| Rule | Monthly 1994-2011: Sharpe | CAGR | Max DD | Longest under water | Turnover/yr | `usw` 2007-03..2011-12: Sharpe | Max DD | Orders/yr | 2000-02 | 2008 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| T trend (tsmom12, all seven) | 1.51 | +8.1% | 6.7% | 16 mo | 1.00 | 0.64 | 10.0% | 16.3 | +8.8% | -0.7% |
| B hold7 + 33% cash | 1.27 | +5.4% | 11.8% | 21 mo | 0.17 | 0.53 | 22.1% | 5.8 | -0.7% | -15.7% |
| C trend on stocks + long bonds | 1.46 | +8.2% | 6.7% | 15 mo | 0.52 | 0.77 | 10.8% | 10.5 | +11.4% | -0.8% |
| H hold7 | 1.27 | +8.1% | 17.3% | 21 mo | 0.24 | 0.54 | 32.0% | 5.8 | -1.2% | -23.1% |

| Test (C vs T) | Value | Pass |
|---|---|---|
| Max DD monthly <= T + 2 pts | +0.0% | yes |
| Max DD `usw` <= T + 2 pts | +0.8% | yes |
| 2000-02 >= T - 3 pts | +2.6% | yes |
| 2008 >= T - 3 pts | -0.0% | yes |
| **Keeps the insurance** | | yes |
| Sharpe monthly >= T + 0.05 | -0.05 | **no** |
| Under water monthly >= 3 mo shorter | -1 mo | **no** |
| Orders `usw` >= 25% fewer | -35% | yes |
| **Loses less of the rest** (2 of 3) | 1 | **no** |
| **Stage 1** | | **no** |

## Stage 2: EUR 2012-2025 (eu-7's test)

| Rule | Sharpe (SE) | CAGR | Vol | Worst loss (max DD) | Longest under water | Worst 12 months | Orders/yr | Avg exposure |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T trend (tsmom12, all seven) | 0.62 (0.27) | +3.7% | 6.1% | 13.6% | 58 mo | -11.5% | 21.1 | 67% |
| B hold7 + 33% cash | 0.79 (0.27) | +4.5% | 5.8% | 13.8% | 31 mo | -8.3% | 2.3 | 67% |
| C trend on stocks + long bonds | 0.63 (0.27) | +4.1% | 6.7% | 15.9% | 57 mo | -13.8% | 13.4 | 85% |
| H hold7 | 0.78 (0.27) | +6.3% | 8.3% | 19.8% | 31 mo | -11.4% | 1.9 | 100% |
| A trend on stocks only (eu-7, ref) | 0.60 (0.27) | +4.0% | 6.9% | 16.1% | 56 mo | -13.1% | 10.1 | 89% |

Paired bootstrap (block 20, 2,000 draws, seed 0); real only at p < 0.0077 (eu family 13).

| Pair | dSharpe | SE | 90% range | p (first better) |
|---|---:|---:|---|---:|
| C - T | +0.00 | 0.07 | -0.12 .. +0.13 | 0.492 |
| C - H | -0.15 | 0.11 | -0.33 .. +0.02 | 0.924 |
| C - B | -0.17 | 0.10 | -0.33 .. +0.01 | 0.941 |

| Window | T trend (tsmom12, all seven) | B hold7 + 33% cash | C trend on stocks + long bonds | H hold7 | Best (within 1 pt) |
|---|---:|---:|---:|---:|---|
| 2000-02 (long monthly proxy) | +8.8% | -0.7% | +11.4% | -1.2% | C |
| 2008 (usw proxy, USD) | -0.7% | -15.7% | -0.8% | -23.1% | T, C |
| 2015-16 | -8.2% | -10.0% | -11.2% | -13.8% | T |
| 2018-Q4 | -4.2% | -2.5% | -2.6% | -3.4% | B, C, H |
| 2020 covid | -12.2% | -13.0% | -14.2% | -18.7% | T, B |
| 2022 rate shock | +1.7% | -4.3% | +1.2% | -6.7% | T, C |

Windows best (of 6): T 4, B 2, C 4, H 1. C within 3 pts of T: 5 of 6.

| Test (C vs T) | Value | Pass |
|---|---|---|
| Max DD <= T + 2 pts | +2.2% | **no** |
| Crash windows within 3 pts of T >= 5 of 6 | 5 | yes |
| **Keeps the insurance** | | **no** |
| Sharpe >= T + 0.05 | +0.00 (p=0.492, not real) | **no** |
| Under water >= 3 mo shorter | -1 mo | **no** |
| Orders >= 25% fewer | -37% | yes |
| **Loses less of the rest** (2 of 3) | 1 | **no** |
| **Stage 2** | | **no** |

Worth a held-out-year card: **no** (needs stage 1 and stage 2).

With rate (a) of step 1 (shown): C excess Sharpe 0.57, CAGR +4.1%, worst loss 15.9%; T 0.57, +3.8%, 14.0%.

## Fixed fees by tier and book

| Tier | Book | T Sharpe (loss; orders) | B Sharpe (loss; orders) | C Sharpe (loss; orders) | H Sharpe (loss; orders) | P1 winner |
|---|---:|---|---|---|---|---|
| EUR 1 | 5k | 0.55 (0.070; 21.1) | 0.76 (0.027; 2.2) | 0.58 (0.049; 13.6) | 0.76 (0.017; 1.9) | tie B~H (p=0.48) -> H |
| EUR 1 | 10k | 0.59 (0.039; 21.0) | 0.77 (0.019; 2.2) | 0.60 (0.021; 13.4) | 0.77 (0.007; 1.9) | tie H~B (p=0.44) -> H |
| EUR 1 | 25k | 0.61 (0.016; 21.0) | 0.78 (0.007; 2.2) | 0.62 (0.010; 13.4) | 0.78 (0.002; 1.9) | tie B~H (p=0.38) -> H |
| EUR 2 | 5k | 0.49 (0.130; 21.1) | 0.76 (0.027; 2.2) | 0.54 (0.082; 13.5) | 0.76 (0.017; 1.9) | tie B~H (p=0.48) -> H |
| EUR 2 | 10k | 0.56 (0.062; 21.1) | 0.77 (0.019; 2.2) | 0.58 (0.041; 13.5) | 0.77 (0.007; 1.9) | tie H~B (p=0.45) -> H |
| EUR 2 | 25k | 0.60 (0.028; 21.0) | 0.78 (0.007; 2.2) | 0.61 (0.015; 13.4) | 0.77 (0.009; 1.9) | tie B~H (p=0.23) -> H |
| EUR 3 | 5k | 0.42 (0.209; 21.1) | 0.75 (0.043; 2.2) | 0.48 (0.141; 13.5) | 0.75 (0.031; 1.8) | tie H~B (p=0.45) -> H |
| EUR 3 | 10k | 0.53 (0.098; 21.1) | 0.76 (0.027; 2.2) | 0.56 (0.064; 13.5) | 0.76 (0.017; 1.9) | tie B~H (p=0.49) -> H |
| EUR 3 | 25k | 0.58 (0.044; 21.0) | 0.78 (0.009; 2.3) | 0.60 (0.023; 13.4) | 0.77 (0.005; 1.9) | tie B~H (p=0.36) -> H |

## Which wins under which preference (among T, B, C, H)

| Preference | Winner | Why | Fee loss <= 0.10 in all 9 cells? |
|---|---|---|---|
| P1 Sharpe after fees | H | per cell: EUR 1 5k H, EUR 1 10k H, EUR 1 25k H, EUR 2 5k H, EUR 2 10k H, EUR 2 25k H, EUR 3 5k H, EUR 3 10k H, EUR 3 25k H | - |
| P2 worst loss | **B** | max DD T 13.6%, B 13.8%, C 15.9%, H 19.8% | yes |
| P3 waiting | **H** | under water T 58 mo, B 31 mo, C 57 mo, H 31 mo | yes |
| P4 crash insurance | **C** | windows best T 4, B 2, C 4, H 1 (a tie goes to fewer orders, eu-7's rule) | no: EUR 3 5k |
| P5 cost | **H** | orders/yr T 21.1, B 2.3, C 13.4, H 1.9 | yes |
