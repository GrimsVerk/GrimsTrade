# RL 5: perp inputs screened by weekly net return spread (train only)

Script `lib/rl5_screen.py --screen`, run once (card `research/rl-5.md`). Per input and
venue-week: +0.5 of equity in the top third of coins by the input, -0.5 in the bottom third;
week = total return (price change minus funding), cost 10 bps on every change of weight.
Pooled = mean over the venues with a book that Friday. Sign = the side that earned gross
over all train weeks (picked in sample, so p is two-sided). Holm = adjusted p over the nine
inputs. Pass = Holm p < 0.10 and net above 0 on at least two venues. Sharpe = pooled net
weeks, annualised with sqrt(52). Turnover = sum of absolute weight changes a year.

| Input | Long side | Weeks | Gross per week (t) | **Net per week (t)** | p | **Holm p** | Net Sharpe | Turnover | B-out | Bybit | Hyperliquid | Venues > 0 | Pass |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `funding` | low | 246 | +0.27% (+2.3) | **+0.18% (+1.6)** | 0.113 | **0.905** | 0.73 | 39x | +0.17% (+1.4) | +0.09% (+0.6) | -0.02% (-0.0) | 2 | no |
| `premium` | low | 245 | +0.22% (+1.7) | **+0.14% (+1.1)** | 0.287 | **1.000** | 0.49 | 38x | +0.06% (+0.4) | +0.22% (+1.5) | +0.07% (+0.2) | 3 | no |
| `mom_12_1` | low | 246 | +0.07% (+0.4) | **+0.04% (+0.2)** | 0.835 | **1.000** | 0.10 | 15x | +0.14% (+0.8) | -0.09% (-0.5) | -0.17% (-0.4) | 1 | no |
| `vol` | low | 246 | +0.04% (+0.2) | **-0.00% (-0.0)** | 1.000 | **1.000** | -0.01 | 21x | -0.14% (-0.8) | -0.07% (-0.3) | +0.50% (+1.2) | 1 | no |
| `rev_1w` | high | 246 | +0.09% (+0.6) | **-0.05% (-0.4)** | 1.000 | **1.000** | -0.17 | 62x | -0.16% (-1.1) | +0.04% (+0.2) | +0.46% (+1.2) | 2 | no |
| `mom_1m` | high | 246 | +0.00% (+0.0) | **-0.07% (-0.4)** | 1.000 | **1.000** | -0.20 | 32x | -0.17% (-1.0) | -0.11% (-0.6) | +0.50% (+1.4) | 1 | no |
| `fund_30` | low | 246 | +0.21% (+1.8) | **+0.16% (+1.4)** | 0.161 | **1.000** | 0.64 | 21x | +0.14% (+1.1) | +0.23% (+1.4) | -0.02% (-0.1) | 2 | no |
| `max_30` | low | 246 | +0.11% (+0.8) | **+0.06% (+0.4)** | 0.688 | **1.000** | 0.18 | 25x | +0.02% (+0.1) | -0.15% (-0.9) | +0.43% (+1.2) | 2 | no |
| `log_qv` | low | 246 | +0.25% (+2.0) | **+0.22% (+1.7)** | 0.087 | **0.780** | 0.79 | 16x | +0.41% (+3.1) | -0.04% (-0.3) | -0.51% (-1.4) | 1 | no |

Passed: **none**. Bar for a book on survivors: pooled Sharpe above `ls-funding`'s 0.57 (rl-4's days).
