# RL 6: noise and power of carry-shaped books (train only, no means)

Script `lib/rl6_power.py`, run once (`research/rl-6.md`). Pooled weekly returns of
third-against-third funding books (0.5 a leg, equal capital per venue), gross of costs, mean
removed before every number. MDE = smallest true mean edge detected with 80% power:
(z_alpha + 0.84) x sd_eff / sqrt(weeks); sd_eff = max(weekly sd, sd of 4-week sums / 2).
z_alpha: 1.2816 (one-sided p < 0.10) and 2.2414 (p < 0.10 / 8, an 8th shape on this data).

| Book | Weeks | Weekly sd | ac1 / ac2 / ac3 | 4-week sums (sd) | Turnover/yr | MDE/week at 0.10 | MDE/week at 0.10/8 | MDE/yr at 0.10/8 | MDE Sharpe at 0.10/8 |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| `w1` | 246 | 1.83% | +0.10 / +0.05 / -0.15 | 61 (4.37%) | 39x | 0.30% | 0.43% | 22.3% | 1.42 |
| `m4-f7` | 246 | 1.26% | +0.08 / -0.03 / -0.10 | 61 (2.58%) | 14x | 0.17% | 0.25% | 13.2% | 1.42 |
| `m4-f28` | 246 | 1.50% | -0.01 / +0.01 / +0.07 | 61 (2.80%) | 13x | 0.20% | 0.30% | 15.4% | 1.42 |
| `m4-f56` | 246 | 1.60% | -0.00 / +0.01 / -0.01 | 61 (3.18%) | 10x | 0.22% | 0.32% | 16.4% | 1.42 |

Paired difference to `w1` (same weeks): the sd of slow minus weekly, and the smallest gap
in mean weekly return a paired test detects (80% power). Next to it, the cost a slower book
saves for certain: (turnover of `w1` - turnover of the slow book) x cost a side, per week.

| Slow book | Weeks | sd_eff of difference | Gap MDE/week at 0.10 | at 0.10/8 | Cost saved/week at 8 bps | at 10 bps | at 30 bps |
|---|---:|---:|---:|---:|---:|---:|---:|
| `m4-f7` | 246 | 1.58% | 0.21% | 0.31% | 0.038% | 0.048% | 0.144% |
| `m4-f28` | 246 | 2.46% | 0.33% | 0.48% | 0.041% | 0.051% | 0.153% |
| `m4-f56` | 246 | 2.68% | 0.36% | 0.53% | 0.045% | 0.056% | 0.169% |

Years of data needed to detect a true annual Sharpe (80% power, `years_needed`):

| True Sharpe | at p < 0.10 | at p < 0.10 / 8 |
|---:|---:|---:|
| 0.30 | 50.1 | 105.6 |
| 0.50 | 18.0 | 38.0 |
| 0.79 | 7.2 | 15.2 |
| 1.00 | 4.5 | 9.5 |
