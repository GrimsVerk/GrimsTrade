# RL 4, part 2: the gate-passing learner on the perp cross-section (train only)

**Addendum run (`ls-ml-ret`, post-hoc):** here `ls-ml` is trained on the week's return
itself (percent, as a z-score across the venue's coins), not on its rank. Everything
else is as in `results/rl-4-perp.md`.

Script `lib/rl4_perp.py --run`; card part 2 in `research/rl-4.md`. `ls-ml`: lasso on the four
ranked inputs, refitted on the first Friday of each year on every earlier venue-week (7-day
embargo); long the top third of its forecast, short the bottom third, per venue. `ls-funding`:
carry-2's book on the same days. `ls-equal`: the four inputs averaged with fixed signs, no
fitting. 10 bps a side plus every funding event; `@30` the same at 30 bps. `tsmom12 twin`:
long-only, 30 bps, no funding. Sharpe on daily returns, 365 days. p: one-sided stationary
bootstrap. Pooled: equal capital per venue book on each day it exists.

## Verdict (card part 2 bars, `ls-ml`)

- bar 1 pooled Sharpe > 0, p < 0.10: no
- bar 2 beats ls-funding, p < 0.10: no
- bar 3 not behind ls-equal: no
- bar 4 B-out > 0 and Bybit or Hyperliquid > 0: no
- bar 5 pooled blend beats the twin, p < 0.10: no

**does not pass**

## The models

| Fitted on | Penalty | `funding` | `premium` | `mom_12_1` | `vol` |
|---|---:|---:|---:|---:|---:|
| 2022-01-07 | 0.08 | +0.000 | +0.000 | +0.000 | +0.000 |
| 2023-01-06 | 0.08 | +0.000 | +0.000 | +0.000 | +0.000 |
| 2024-01-05 | 0.08 | +0.000 | +0.000 | +0.000 | +0.000 |
| 2025-01-03 | 0.08 | +0.000 | +0.000 | +0.000 | +0.000 |

Weights are on ranked, standardised inputs, for a target with unit spread: a weight is roughly
that input's own IC after the penalty.

### Pooled

First return day 2022-01-08, 3.8 years.

| Book | Sharpe | CAGR | Max DD | Worst week | 2022 | 2023 | 2024 | 2025 | Funding/yr | Turn/yr | Corr twin | p(S>0) | vs ls-funding (p) | vs ls-equal (p) | Blend | Blend - twin (p) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ls-ml | 0.00 | +0.0% | 0% | +0% | +0.00 | +0.00 | +0.00 | +0.00 | - | - | +0.00 | 1.000 | -0.57 (0.88) | -0.06 (0.56) | 0.01 | +0.00 (1.00) |
| ls-ml @30 | 0.00 | +0.0% | 0% | +0% | +0.00 | +0.00 | +0.00 | +0.00 | - | - | +0.00 | 1.000 | +0.27 (0.31) | +0.51 (0.16) | 0.01 | +0.00 (1.00) |
| ls-funding | 0.57 | +5.8% | 19% | -7% | +0.33 | +0.06 | +1.65 | +0.03 | - | - | -0.18 | 0.119 |  |  | 0.18 | +0.17 (0.12) |
| ls-funding @30 | -0.27 | -3.6% | 29% | -7% | -0.40 | -0.72 | +0.77 | -1.02 | - | - | -0.18 | 0.693 |  |  | -0.07 | -0.08 (0.70) |
| ls-equal | 0.06 | -0.1% | 27% | -10% | -0.27 | -1.08 | +0.97 | +0.61 | - | - | -0.32 | 0.444 |  |  | 0.03 | +0.02 (0.44) |
| ls-equal @30 | -0.51 | -7.8% | 39% | -10% | -0.86 | -1.63 | +0.20 | +0.17 | - | - | -0.32 | 0.836 |  |  | -0.19 | -0.20 (0.84) |
| tsmom12 twin | 0.01 | -6.5% | 50% | -28% | -1.23 | +1.48 | +0.45 | -0.95 | - | - | +1.00 | - |  |  | - |  |

### B-out

First return day 2022-01-08, 3.8 years. Weekly decisions 200, coins per week 116. Forecast's weekly IC out of sample - (t -).

| Book | Sharpe | CAGR | Max DD | Worst week | 2022 | 2023 | 2024 | 2025 | Funding/yr | Turn/yr | Corr twin | p(S>0) | vs ls-funding (p) | vs ls-equal (p) | Blend | Blend - twin (p) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ls-ml | 0.00 | +0.0% | 0% | +0% | +0.00 | +0.00 | +0.00 | +0.00 | +0.0% | 0 | +0.00 | 1.000 | -0.37 (0.74) | +0.38 (0.24) | -0.30 | +0.00 (1.00) |
| ls-ml @30 | 0.00 | +0.0% | 0% | +0% | +0.00 | +0.00 | +0.00 | +0.00 | +0.0% | 0 | +0.00 | 1.000 | +0.46 (0.21) | +0.95 (0.04) | -0.30 | +0.00 (1.00) |
| ls-funding | 0.37 | +3.5% | 24% | -8% | +0.30 | +0.13 | +1.55 | -0.47 | +9.1% | 42 | -0.00 | 0.257 |  |  | -0.16 | +0.14 (0.23) |
| ls-funding @30 | -0.46 | -5.5% | 35% | -8% | -0.33 | -0.89 | +0.52 | -1.26 | +9.1% | 42 | -0.00 | 0.790 |  |  | -0.43 | -0.13 (0.77) |
| ls-equal | -0.38 | -5.8% | 36% | -12% | -0.88 | -1.16 | +0.77 | -0.09 | +6.4% | 36 | -0.12 | 0.763 |  |  | -0.44 | -0.14 (0.75) |
| ls-equal @30 | -0.95 | -12.9% | 51% | -12% | -1.36 | -1.88 | -0.11 | -0.51 | +6.4% | 36 | -0.12 | 0.962 |  |  | -0.68 | -0.38 (0.96) |
| tsmom12 twin | -0.30 | -13.7% | 53% | -28% | -1.31 | +1.52 | -0.16 | -1.48 | +0.0% | 4 | +1.00 | - |  |  | - |  |

### Bybit

First return day 2022-05-14, 3.5 years. Weekly decisions 182, coins per week 59. Forecast's weekly IC out of sample - (t -).

| Book | Sharpe | CAGR | Max DD | Worst week | 2022 | 2023 | 2024 | 2025 | Funding/yr | Turn/yr | Corr twin | p(S>0) | vs ls-funding (p) | vs ls-equal (p) | Blend | Blend - twin (p) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ls-ml | 0.00 | +0.0% | 0% | +0% | +0.00 | +0.00 | +0.00 | +0.00 | +0.0% | 0 | +0.00 | 1.000 | -0.31 (0.74) | -0.19 (0.67) | 0.20 | +0.00 (1.00) |
| ls-ml @30 | 0.00 | +0.0% | 0% | +0% | +0.00 | +0.00 | +0.00 | +0.00 | +0.0% | 0 | +0.00 | 1.000 | +0.35 (0.25) | +0.26 (0.28) | 0.20 | +0.00 (1.00) |
| ls-funding | 0.31 | +3.5% | 20% | -8% | -0.49 | +0.32 | +1.58 | -0.49 | +8.6% | 46 | -0.13 | 0.256 |  |  | 0.31 | +0.11 (0.28) |
| ls-funding @30 | -0.35 | -6.0% | 29% | -8% | -0.97 | -0.27 | +0.79 | -1.32 | +8.6% | 46 | -0.13 | 0.749 |  |  | 0.06 | -0.14 (0.76) |
| ls-equal | 0.19 | +1.8% | 26% | -12% | -0.09 | -0.72 | +0.67 | +0.95 | +6.7% | 37 | -0.27 | 0.326 |  |  | 0.30 | +0.09 (0.33) |
| ls-equal @30 | -0.26 | -6.1% | 31% | -12% | -0.52 | -1.12 | +0.05 | +0.57 | +6.7% | 37 | -0.27 | 0.720 |  |  | 0.08 | -0.12 (0.72) |
| tsmom12 twin | 0.20 | +0.4% | 51% | -24% | +0.00 | +1.74 | +0.30 | -1.09 | +0.0% | 6 | +1.00 | - |  |  | - |  |

### Hyperliquid

First return day 2023-06-10, 2.4 years. Weekly decisions 126, coins per week 14. Forecast's weekly IC out of sample - (t -).

| Book | Sharpe | CAGR | Max DD | Worst week | 2023 | 2024 | 2025 | Funding/yr | Turn/yr | Corr twin | p(S>0) | vs ls-funding (p) | vs ls-equal (p) | Blend | Blend - twin (p) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ls-ml | 0.00 | +0.0% | 0% | +0% | +0.00 | +0.00 | +0.00 | +0.0% | 0 | +0.00 | 1.000 | -0.47 (0.79) | -0.43 (0.75) | 0.52 | +0.00 (1.00) |
| ls-ml @30 | 0.00 | +0.0% | 0% | +0% | +0.00 | +0.00 | +0.00 | +0.0% | 0 | +0.00 | 1.000 | -0.10 (0.58) | -0.09 (0.57) | 0.52 | +0.00 (1.00) |
| ls-funding | 0.47 | +9.1% | 27% | -19% | -0.21 | +0.80 | +0.58 | +7.8% | 44 | -0.26 | 0.207 |  |  | 0.74 | +0.23 (0.20) |
| ls-funding @30 | 0.10 | -0.6% | 27% | -19% | -0.43 | +0.41 | +0.08 | +7.8% | 44 | -0.26 | 0.415 |  |  | 0.57 | +0.05 (0.41) |
| ls-equal | 0.43 | +8.0% | 34% | -15% | -0.28 | +0.68 | +0.59 | +6.5% | 40 | -0.36 | 0.254 |  |  | 0.76 | +0.25 (0.22) |
| ls-equal @30 | 0.09 | -0.9% | 37% | -16% | -0.51 | +0.28 | +0.26 | +6.5% | 40 | -0.36 | 0.426 |  |  | 0.60 | +0.08 (0.38) |
| tsmom12 twin | 0.52 | +14.1% | 51% | -24% | +1.44 | +1.03 | -0.64 | +0.0% | 11 | +1.00 | - |  |  | - |  |
