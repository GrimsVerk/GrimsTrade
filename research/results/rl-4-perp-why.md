# RL 4, part 2: why a good rank forecast made no money (post-hoc, descriptive)

Script `lib/rl4_perp.py --why`, written after `results/rl-4-perp.md` had been seen; no
backtest, no costs. For each input, every venue-week (at least 10 coins with the input): the
coins are split into thirds by the input. Long third = the side the rank IC favours. Return
= the week's total return of a long position in plain percent (price change minus funding),
equal weight inside a third. Spread = long third minus short third: what the book's two
legs earn together per unit of gross exposure x 2. All venue-weeks from 2021-02 to 2025-11.

| Input | Long side | Rank IC | Mean return, long third | Mean return, short third | **Mean spread per week (t)** | Median coin, long third | Median coin, short third | Weeks spread > 0 | Worst week's spread | Best week's spread |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `funding` | low | -0.021 | +0.25% | -0.16% | **+0.40% (+2.1)** | -1.20% | -1.60% | 54% | -22.2% | +16.2% |
| `premium` | low | -0.031 | +0.17% | -0.23% | **+0.40% (+2.0)** | -1.15% | -1.70% | 55% | -19.1% | +18.8% |
| `mom_12_1` | high | +0.021 | -0.05% | +0.04% | **-0.09% (-0.3)** | -1.27% | -1.34% | 53% | -31.7% | +35.2% |
| `vol` | low | -0.104 | +0.05% | +0.00% | **+0.05% (+0.2)** | -0.88% | -1.86% | 52% | -26.7% | +19.3% |
