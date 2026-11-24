# eu-8 step 1: idle cash earns a money-market rate (cards/eu-8.md)

Train only. `euw` in EUR, window W (decisions 2012-01-02 .. 2025-11-09), no fixed fee, eu-6/eu-7's runs re-scored. Rate (a): ECB EONIA monthly average before 2019-10-01, EUR STR daily after, ACT/360, negative years included (average 0.48% a year over W); (b): the same floored at 0 (average 0.70%). Interest on the gym's actual end-of-day cash. Excess Sharpe = Sharpe of returns above the rate (primary); Sharpe vs 0 as before.

## 1. `euw`, no fixed fee

| Rule | Cash | Avg cash share | Excess Sharpe (SE) | Sharpe vs 0 | CAGR | Vol | Worst loss | Longest under water | Worst 12 months | Orders/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| T trend (tsmom12, all seven) | 0 (eu-6/7) | 31% | - | 0.62 | +3.7% | 6.1% | 13.6% | 58 mo | -11.5% | 21.1 |
| T trend (tsmom12, all seven) | (a) EONIA/EUR STR | 31% | 0.57 (0.27) | 0.64 | +3.8% | 6.1% | 14.0% | 58 mo | -11.5% | 21.1 |
| T trend (tsmom12, all seven) | (b) floored | 31% | 0.54 (0.27) | 0.66 | +3.9% | 6.1% | 13.6% | 58 mo | -11.5% | 21.1 |
| B hold7 + 33% cash | 0 (eu-6/7) | 33% | - | 0.79 | +4.5% | 5.8% | 13.8% | 31 mo | -8.3% | 2.3 |
| B hold7 + 33% cash | (a) EONIA/EUR STR | 33% | 0.73 (0.27) | 0.82 | +4.6% | 5.8% | 13.8% | 31 mo | -8.4% | 2.3 |
| B hold7 + 33% cash | (b) floored | 33% | 0.71 (0.27) | 0.83 | +4.7% | 5.8% | 13.8% | 31 mo | -8.3% | 2.3 |
| H hold7 | 0 (eu-6/7) | 3% | - | 0.78 | +6.3% | 8.3% | 19.8% | 31 mo | -11.4% | 1.9 |
| H hold7 | (a) EONIA/EUR STR | 3% | 0.72 (0.27) | 0.78 | +6.3% | 8.3% | 19.8% | 31 mo | -11.4% | 1.9 |
| H hold7 | (b) floored | 3% | 0.70 (0.27) | 0.78 | +6.3% | 8.3% | 19.8% | 31 mo | -11.4% | 1.9 |
| M mix60 | 0 (eu-6/7) | 2% | - | 0.75 | +7.0% | 9.6% | 22.3% | 31 mo | -15.7% | 1.2 |
| M mix60 | (a) EONIA/EUR STR | 2% | 0.71 (0.27) | 0.75 | +7.1% | 9.6% | 22.3% | 31 mo | -15.7% | 1.2 |
| M mix60 | (b) floored | 2% | 0.68 (0.27) | 0.76 | +7.1% | 9.6% | 22.3% | 31 mo | -15.7% | 1.2 |

## 2. Excess-Sharpe differences, rate (a)

Paired stationary bootstrap (block 20, 2,000 draws, seed 0); real only at p < 0.0083. Cash at 0 (eu-6/7) for reference.

| Pair | dSharpe, cash 0 | dSharpe, rate (a) | Bootstrap SE | 90% range | p (first better) |
|---|---:|---:|---:|---|---:|
| B - T | +0.17 | +0.17 | 0.13 | -0.04 .. +0.40 | 0.099 |
| H - T | +0.16 | +0.16 | 0.13 | -0.05 .. +0.39 | 0.117 |
| M - T | +0.13 | +0.14 | 0.17 | -0.15 .. +0.42 | 0.208 |
| B - H | +0.01 | +0.01 | 0.02 | -0.01 .. +0.04 | 0.257 |
| H - M | +0.03 | +0.02 | 0.10 | -0.14 .. +0.18 | 0.407 |

## 3. Crash windows, rate (a) (cash at 0 in brackets)

| Window | T trend (tsmom12, all seven) | B hold7 + 33% cash | H hold7 | M mix60 | Best of T/B/H (1 pt) |
|---|---:|---:|---:|---:|---|
| 2000-02 (long monthly proxy) | +13.2% (+8.8%) | +2.5% (-0.7%) | -1.2% (-1.2%) | -14.3% (-14.3%) | T |
| 2008 (usw proxy, USD) | -0.3% (-0.7%) | -15.0% (-15.7%) | -23.0% (-23.1%) | -30.4% (-30.4%) | T |
| 2015-16 | -8.2% (-8.2%) | -10.1% (-10.0%) | -13.9% (-13.8%) | -13.8% (-13.8%) | T |
| 2018-Q4 | -4.2% (-4.2%) | -2.5% (-2.5%) | -3.4% (-3.4%) | -5.5% (-5.5%) | B, H |
| 2020 covid | -12.2% (-12.2%) | -13.0% (-13.0%) | -18.7% (-18.7%) | -22.1% (-22.1%) | T, B |
| 2022 rate shock | +1.5% (+1.7%) | -4.4% (-4.3%) | -6.7% (-6.7%) | -17.4% (-17.4%) | T |

Windows best (of 6): T 5, B 2, H 1 (cash 0: T 5, B 2, H 1).

## 4. Proxies with the US T-bill rate (IRX)

`usw` 2007-03-01 .. 2025-11-09 (USD, daily):

| Rule | Excess Sharpe | Sharpe vs 0 (cash 0) | CAGR (cash 0) | Worst loss (cash 0) | 2008 (cash 0) |
|---|---:|---:|---:|---:|---:|
| T | 0.50 | 0.70 (0.64) | +4.9% (+4.4%) | 10.9% (10.9%) | -0.3% (-0.7%) |
| B | 0.47 | 0.66 (0.60) | +4.8% (+4.3%) | 21.9% (22.1%) | -15.0% (-15.7%) |
| H | 0.51 | 0.63 (0.63) | +6.5% (+6.5%) | 31.9% (32.0%) | -23.0% (-23.1%) |
| M | 0.43 | 0.55 (0.54) | +6.0% (+5.9%) | 32.0% (32.0%) | -30.4% (-30.4%) |

Long monthly proxy (stocks / 10y Treasuries / gold, 1972-2025, cash earns the month's average IRX / 12; Sharpe from monthly returns):

| Rule | Excess Sharpe | Sharpe vs 0 (cash 0) | CAGR (cash 0) | Max DD (cash 0) |
|---|---:|---:|---:|---:|
| T | 0.78 | 1.47 (1.26) | +9.5% (+8.1%) | 11.7% (12.5%) |
| B | 0.62 | 1.48 (1.20) | +7.7% (+6.2%) | 11.6% (14.3%) |
| H | 0.62 | 1.20 (1.20) | +9.2% (+9.2%) | 20.8% (20.8%) |
| M | 0.60 | 1.14 (1.14) | +9.4% (+9.4%) | 27.0% (27.0%) |

## 5. The card's conclusions K1-K8 (rate (a))

| | eu-6/7 (cash 0) | With rate (a) | Verdict |
|---|---|---|---|
| K1 Sharpe order | B > H > M > T (vs 0) | B > H > M > T (excess); flips > 0.05: none; real gaps: none | holds |
| K2 B - T Sharpe | +0.17 | +0.17 (p 0.099) | holds |
| K3 P2 worst loss | B | B (max DD T 14.0%, B 13.8%, H 19.8%) | holds |
| K4 P3 under water | H | H (T 58 mo, B 31 mo, H 31 mo) | holds |
| K5 P4 crash insurance | T | T (windows T 5, B 2, H 1) | holds |
| K6 H - T CAGR | +2.7% | +2.6% | holds |
| K7 2008 proxy worst loss B vs T | 22.1% vs 10.9% | 21.9% vs 10.9% | holds |
| K8 long proxy T vs H Sharpe | 1.26 vs 1.20 | 0.78 vs 0.62 (excess) | holds |

P1 at no fee (excess Sharpe, among T/B/H): B (cash 0: B). Rate (b), floored, shown in table 1 only.
