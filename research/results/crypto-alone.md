# BTC alone and ETH alone

Each asset on its own, in or out (or scaled). Train period, gym costs (60 bps a round trip). `equal-weight` is buy-and-hold. The first three rows are baselines; the last three are the run-2 rules, unchanged (robustness rows).

## BTC, from 2013-01-01

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 | dSharpe vs equal-weight@BTC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| equal-weight@BTC | 1.29 (0.28) | +101.1% | 78.0% | 84.9% | 0.0 | 100% | 1.64 | 1.35 | 0.66 | - | - |
| sma200@BTC | 1.38 (0.28) | +102.5% | 68.1% | 71.0% | 2.2 | 70% | 1.84 | 1.31 | 0.81 | +0.09 (p=0.28; -0.16..+0.34) | 2/3 |
| tsmom12@BTC | 1.30 (0.28) | +95.1% | 71.3% | 80.5% | 0.4 | 76% | 1.58 | 1.26 | 1.04 | +0.01 (p=0.48; -0.21..+0.21) | 1/3 |
| e4@BTC | 1.43 (0.28) | +100.4% | 62.4% | 70.3% | 4.9 | 65% | 1.79 | 1.44 | 0.87 | +0.14 (p=0.14; -0.07..+0.35) | 3/3 |
| t40@BTC | 1.24 (0.28) | +59.1% | 45.8% | 68.5% | 4.6 | 70% | 1.66 | 1.29 | 0.69 | -0.05 (p=0.65; -0.25..+0.17) | 2/3 |
| tv40@BTC | 1.26 (0.28) | +51.8% | 39.5% | 54.3% | 4.0 | 52% | 1.66 | 1.11 | 1.01 | -0.04 (p=0.59; -0.34..+0.26) | 2/3 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| equal-weight@BTC | - | - | -32% | -59% | -85% | -84% | -76% |
| sma200@BTC | - | - | -10% | +0% | -61% | -63% | -35% |
| tsmom12@BTC | - | - | -32% | -11% | -69% | -67% | -36% |
| e4@BTC | - | - | -19% | -21% | -52% | -61% | -40% |
| t40@BTC | - | - | -26% | -51% | -63% | -59% | -66% |
| tv40@BTC | - | - | -26% | -8% | -42% | -37% | -26% |

Annualised log growth: equal-weight@BTC +69.9%, sma200@BTC +70.6%, tsmom12@BTC +66.8%, e4@BTC +69.5%, t40@BTC +46.4%, tv40@BTC +41.7%

## ETH, from 2017-05-19

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs equal-weight@ETH (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| equal-weight@ETH | 0.86 (0.34) | +43.7% | 90.7% | 94.0% | 0.0 | 100% | 1.17 | 0.33 | - | - |
| sma200@ETH | 0.74 (0.34) | +31.1% | 73.2% | 93.4% | 2.6 | 60% | 1.08 | 0.04 | -0.12 (p=0.68; -0.50..+0.28) | 0/2 |
| tsmom12@ETH | 0.83 (0.34) | +40.5% | 74.4% | 91.8% | 1.4 | 63% | 1.11 | 0.32 | -0.02 (p=0.54; -0.36..+0.33) | 0/2 |
| e4@ETH | 0.93 (0.34) | +48.4% | 67.2% | 83.3% | 5.4 | 59% | 1.28 | 0.21 | +0.07 (p=0.35; -0.24..+0.39) | 1/2 |
| t40@ETH | 0.82 (0.34) | +31.3% | 46.1% | 72.0% | 5.8 | 56% | 1.15 | 0.41 | -0.04 (p=0.61; -0.24..+0.18) | 1/2 |
| tv40@ETH | 0.71 (0.34) | +21.5% | 36.7% | 69.4% | 5.0 | 36% | 0.98 | 0.35 | -0.14 (p=0.71; -0.56..+0.29) | 1/2 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| equal-weight@ETH | - | - | -47% | -66% | - | -89% | -76% |
| sma200@ETH | - | - | -48% | -38% | - | -59% | -49% |
| tsmom12@ETH | - | - | -48% | -29% | - | -57% | -42% |
| e4@ETH | - | - | -47% | -29% | - | -27% | -44% |
| t40@ETH | - | - | -20% | -49% | - | -66% | -53% |
| tv40@ETH | - | - | -20% | -22% | - | -36% | -30% |

Annualised log growth: equal-weight@ETH +36.3%, sma200@ETH +27.1%, tsmom12@ETH +34.0%, e4@ETH +39.5%, t40@ETH +27.2%, tv40@ETH +19.4%

## Reading (2026-11-12)

The survey's one positive crypto claim ("slow trend on Bitcoin holds up") is not something our
gym can confirm. On BTC since 2013 the 200-day rule has Sharpe 1.38 against 1.29 for holding
(p = 0.28) and the 12-month rule 1.30; on ETH since 2017 both trend rules are behind holding.
With a standard error of about 0.3 on thirteen years, none of these differences means anything.

What trend did do is shrink the crypto winters, unevenly: BTC -85%, -84%, -76% when held;
-61%, -63%, -35% with the 200-day rule. A worst loss of 71% is still not a protected position.
Only the rule that also caps volatility (`tv40`) brings the winters to -42%, -37%, -26% (worst
loss 54% on BTC, 69% on ETH), and it pays for it with half the growth (+52% a year against +101%
on BTC).

For the paper system: do not expect a trend rule to make crypto safe or to beat holding it. The
size of the crypto slot matters more than the timing rule on it.
