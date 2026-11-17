# RL 4, part 2: weekly IC of the four inputs on the perp cross-section (train only)

Script `lib/rl4_perp.py --ic` (descriptive, no backtest, no training). IC = Spearman rank
correlation, across the tradable coins of one venue on one Friday, between the input and the
coming week's total return of a long position (price change minus funding paid); mean over
weeks, t-statistic in brackets. Pooled = all venue-weeks. Walk-forward = the same, but the
input's sign is set at each yearly fit from the weeks before it (7-day embargo), and only
weeks after the first fit count. carry-2's sets, decisions to 2025-11-09.

| Set | First decision | Weeks | Coins per week |
|---|---|---:|---:|
| B-out | 2021-02-19 | 246 | 99 |
| Bybit | 2022-05-13 | 182 | 59 |
| Hyperliquid | 2023-06-09 | 126 | 14 |

| Input | Pooled IC (t) | Pooled, weeks after the first fit | **Walk-forward IC (t)** | Share of weeks > 0 | Sign used | B-out | Bybit | Hyperliquid |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| `funding` | -0.021 (-2.4) | -0.020 (-2.3) | **+0.020 (+2.3)** | 57% | - | -0.008 (-0.8) | -0.026 (-1.7) | -0.050 (-1.6) |
| `premium` | -0.031 (-3.5) | -0.033 (-3.7) | **+0.033 (+3.7)** | 60% | - | -0.014 (-1.3) | -0.055 (-3.8) | -0.029 (-0.9) |
| `mom_12_1` | +0.021 (+2.0) | +0.023 (+2.1) | **+0.023 (+2.1)** | 55% | + | +0.009 (+0.7) | +0.032 (+1.7) | +0.032 (+1.0) |
| `vol` | -0.104 (-8.6) | -0.104 (-8.2) | **+0.104 (+8.2)** | 68% | - | -0.085 (-6.0) | -0.110 (-5.3) | -0.155 (-3.5) |

Screen (card part 2): an input passes with a walk-forward IC of at least 0.04 and t of at least 2. **Passed**: the best walk-forward IC is +0.104.
