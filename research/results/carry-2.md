# Carry 2: raw tables (train, decisions to 2025-11-09)

Script `lib/carry2.py`; card and reading in `research/carry-2.md`. `ls-` books and perp baselines at 10 bps a side plus every funding event; `@30`: the same at 30 bps. `tsmom12 twin`: long-only on the venue's perp closes (standing in for spot), 30 bps, no funding. Sharpe on daily returns, 365 days; per-era and per-year Sharpe need 180 days. `p(S>0)`: one-sided stationary-bootstrap p that the book's Sharpe is above 0. Blend: 50% twin + 50% the book, re-split daily; p one-sided. Pooled: equal capital per venue book on each day it exists (funding and turnover not pooled).

## Verdict (card bars)

**`ls-premium`: does not replicate**
- bar 1 pooled Sharpe > 0, p < 0.10: no
- bar 2 B-out > 0 and Bybit or Hyperliquid > 0: yes
- bar 3 pooled blend beats twin, p < 0.10: no
- bar 4 pooled > 0 in both eras: yes
- bar (5) at 30 bps: pooled > 0 and blend p < 0.20: no

**`ls-funding`: REPLICATES**
- bar 1 pooled Sharpe > 0, p < 0.10: yes
- bar 2 B-out > 0 and Bybit or Hyperliquid > 0: yes
- bar 3 pooled blend beats twin, p < 0.10: yes
- bar 4 pooled > 0 in both eras: yes
- bar (5) at 30 bps: pooled > 0 and blend p < 0.20: no

### pooled (B-out, Bybit, Hyperliquid)

First return day 2021-02-20, 4.7 years.

| Shape | Sharpe | CAGR | Max DD | Worst week | 2020-21 | 2022-25 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | Funding/yr | Turn/yr | Corr twin | p(S>0) | Blend | Blend - twin (p) | Blend DD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| EW perp | -0.02 | -34.6% | 94% | -52% | +0.52 | -0.20 | - | +0.52 | -1.26 | +0.99 | +0.38 | -0.48 | - | - | +0.82 |  |  |  |  |
| EW perp @30 | -0.04 | -35.8% | 94% | -52% | +0.51 | -0.22 | - | +0.51 | -1.27 | +0.96 | +0.35 | -0.50 | - | - | +0.82 |  |  |  |  |
| ls-funding | 0.69 | +9.8% | 19% | -10% | +1.03 | +0.60 | - | +1.03 | +0.45 | +0.06 | +1.65 | +0.03 | - | - | -0.16 | 0.041 | 0.37 | +0.17 (0.038) | 41% |
| ls-funding @30 | 0.09 | +0.2% | 29% | -10% | +0.70 | -0.23 | - | +0.70 | -0.27 | -0.72 | +0.77 | -1.02 | - | - | -0.16 | 0.401 | 0.22 | +0.02 (0.397) | 42% |
| ls-premium | 0.44 | +5.9% | 27% | -14% | +0.29 | +0.56 | - | +0.29 | +0.72 | -0.58 | +1.13 | +1.01 | - | - | -0.17 | 0.149 | 0.31 | +0.12 (0.146) | 43% |
| ls-premium @30 | -0.12 | -3.2% | 33% | -14% | -0.04 | -0.18 | - | -0.04 | +0.14 | -1.31 | +0.31 | +0.11 | - | - | -0.17 | 0.608 | 0.17 | -0.03 (0.608) | 44% |
| tsmom12 perp | 0.09 | -13.3% | 75% | -52% | +0.42 | -0.13 | - | +0.42 | -1.35 | +1.47 | +0.24 | -0.97 | - | - | +1.00 |  |  |  |  |
| tsmom12 perp @30 | 0.06 | -14.5% | 76% | -52% | +0.40 | -0.16 | - | +0.40 | -1.37 | +1.42 | +0.20 | -1.00 | - | - | +1.00 |  |  |  |  |
| tsmom12 twin | 0.20 | -7.2% | 72% | -52% | +0.61 | -0.04 | - | +0.61 | -1.39 | +1.48 | +0.45 | -0.95 | - | - | +1.00 |  |  |  |  |


### B-out

First return day 2021-02-20, 4.7 years. Coins with data: 558 (26 without a price in train's last month, i.e. delisted); tradable per day median 106; weekly decisions 246.

| Shape | Sharpe | CAGR | Max DD | Worst week | 2020-21 | 2022-25 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | Funding/yr | Turn/yr | Corr twin | p(S>0) | Blend | Blend - twin (p) | Blend DD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 twin | 0.07 | -13.0% | 76% | -52% | +0.61 | -0.35 | - | +0.61 | -1.46 | +1.52 | -0.16 | -1.48 | +0.0% | 4 | +1.00 |  |  |  |  |
| tsmom12 perp | -0.02 | -17.3% | 78% | -52% | +0.42 | -0.38 | - | +0.42 | -1.42 | +1.58 | -0.28 | -1.43 | -6.3% | 4 | +1.00 |  |  |  |  |
| tsmom12 perp @30 | -0.03 | -18.2% | 79% | -52% | +0.40 | -0.41 | - | +0.40 | -1.44 | +1.53 | -0.31 | -1.47 | -6.3% | 4 | +1.00 |  |  |  |  |
| EW perp | 0.04 | -32.7% | 93% | -52% | +0.52 | -0.12 | - | +0.52 | -1.13 | +1.39 | +0.32 | -0.62 | -6.0% | 4 | +0.77 |  |  |  |  |
| EW perp @30 | 0.02 | -33.5% | 93% | -52% | +0.51 | -0.14 | - | +0.51 | -1.14 | +1.38 | +0.30 | -0.64 | -6.0% | 4 | +0.77 |  |  |  |  |
| ls-premium | 0.17 | +1.4% | 29% | -14% | +0.29 | +0.13 | - | +0.29 | +0.50 | -0.55 | +0.89 | -0.60 | +8.7% | 42 | -0.09 | 0.347 | 0.12 | +0.05 (0.352) | 43% |
| ls-premium @30 | -0.36 | -7.3% | 47% | -14% | -0.04 | -0.52 | - | -0.04 | +0.09 | -1.43 | -0.06 | -1.30 | +8.7% | 42 | -0.09 | 0.800 | -0.03 | -0.10 (0.803) | 50% |
| ls-funding | 0.57 | +7.9% | 24% | -10% | +1.03 | +0.40 | - | +1.03 | +0.40 | +0.13 | +1.55 | -0.47 | +9.4% | 42 | -0.10 | 0.072 | 0.22 | +0.15 (0.076) | 41% |
| ls-funding @30 | -0.02 | -1.4% | 35% | -10% | +0.70 | -0.42 | - | +0.70 | -0.22 | -0.89 | +0.52 | -1.26 | +9.4% | 42 | -0.10 | 0.520 | 0.07 | -0.01 (0.526) | 45% |

- `ls-premium`: 273 coins ever held, 16 of them delisted later in train; long leg alone Sharpe -0.01 (CAGR -10.3%, funding +2.2%/yr), short leg alone 0.12 (CAGR -4.5%, funding +6.8%/yr).
- `ls-funding`: 272 coins ever held, 16 of them delisted later in train; long leg alone Sharpe 0.08 (CAGR -6.4%, funding +2.6%/yr), short leg alone 0.16 (CAGR -2.8%, funding +7.0%/yr).

### Bybit

First return day 2022-05-14, 3.5 years. Coins with data: 392 (0 without a price in train's last month, i.e. delisted); tradable per day median 61; weekly decisions 182.

| Shape | Sharpe | CAGR | Max DD | Worst week | 2020-21 | 2022-25 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | Funding/yr | Turn/yr | Corr twin | p(S>0) | Blend | Blend - twin (p) | Blend DD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 twin | 0.20 | +0.4% | 51% | -24% | - | +0.20 | - | - | +0.00 | +1.74 | +0.30 | -1.09 | +0.0% | 6 | +1.00 |  |  |  |  |
| tsmom12 perp | 0.16 | -1.4% | 53% | -24% | - | +0.16 | - | - | +0.00 | +1.79 | +0.15 | -1.03 | -3.0% | 6 | +1.00 |  |  |  |  |
| tsmom12 perp @30 | 0.12 | -2.6% | 53% | -24% | - | +0.12 | - | - | +0.00 | +1.74 | +0.12 | -1.07 | -3.0% | 6 | +1.00 |  |  |  |  |
| EW perp | 0.13 | -18.7% | 73% | -32% | - | +0.13 | - | - | -0.79 | +1.42 | +0.33 | -0.51 | -4.5% | 8 | +0.75 |  |  |  |  |
| EW perp @30 | 0.10 | -20.2% | 74% | -32% | - | +0.10 | - | - | -0.81 | +1.39 | +0.31 | -0.52 | -4.5% | 8 | +0.75 |  |  |  |  |
| ls-premium | 0.73 | +10.4% | 20% | -9% | - | +0.73 | - | - | +0.06 | +0.14 | +1.53 | +1.21 | +8.6% | 43 | -0.18 | 0.075 | 0.49 | +0.29 (0.085) | 24% |
| ls-premium @30 | 0.13 | +0.9% | 24% | -9% | - | +0.13 | - | - | -0.39 | -0.45 | +0.85 | +0.55 | +8.6% | 43 | -0.18 | 0.386 | 0.25 | +0.05 (0.403) | 26% |
| ls-funding | 0.31 | +3.5% | 20% | -8% | - | +0.31 | - | - | -0.49 | +0.32 | +1.58 | -0.49 | +8.6% | 46 | -0.13 | 0.256 | 0.31 | +0.11 (0.275) | 27% |
| ls-funding @30 | -0.35 | -6.0% | 29% | -8% | - | -0.35 | - | - | -0.97 | -0.27 | +0.79 | -1.32 | +8.6% | 46 | -0.13 | 0.749 | 0.06 | -0.14 (0.764) | 31% |

- `ls-premium`: 215 coins ever held, 0 of them delisted later in train; long leg alone Sharpe 0.18 (CAGR -0.3%, funding +2.8%/yr), short leg alone 0.14 (CAGR -2.3%, funding +6.0%/yr).
- `ls-funding`: 212 coins ever held, 0 of them delisted later in train; long leg alone Sharpe 0.11 (CAGR -3.1%, funding +2.9%/yr), short leg alone 0.04 (CAGR -5.9%, funding +5.9%/yr).

### Hyperliquid

First return day 2023-06-10, 2.4 years. Coins with data: 58 (4 without a price in train's last month, i.e. delisted); tradable per day median 13; weekly decisions 126.

| Shape | Sharpe | CAGR | Max DD | Worst week | 2020-21 | 2022-25 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | Funding/yr | Turn/yr | Corr twin | p(S>0) | Blend | Blend - twin (p) | Blend DD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 twin | 0.52 | +14.1% | 51% | -24% | - | +0.52 | - | - | - | +1.44 | +1.03 | -0.64 | +0.0% | 11 | +1.00 |  |  |  |  |
| tsmom12 perp | 0.30 | +1.4% | 54% | -24% | - | +0.30 | - | - | - | +1.31 | +0.71 | -0.73 | -14.2% | 11 | +1.00 |  |  |  |  |
| tsmom12 perp @30 | 0.26 | -1.0% | 54% | -24% | - | +0.26 | - | - | - | +1.25 | +0.66 | -0.76 | -14.2% | 11 | +1.00 |  |  |  |  |
| EW perp | -0.07 | -28.9% | 67% | -30% | - | -0.07 | - | - | - | -0.87 | +0.48 | -0.30 | -9.7% | 13 | +0.93 |  |  |  |  |
| EW perp @30 | -0.11 | -30.9% | 69% | -30% | - | -0.11 | - | - | - | -0.94 | +0.44 | -0.32 | -9.7% | 13 | +0.93 |  |  |  |  |
| ls-premium | 0.28 | +4.0% | 32% | -15% | - | +0.28 | - | - | - | -0.78 | +0.37 | +1.25 | +7.7% | 44 | -0.22 | 0.321 | 0.64 | +0.13 (0.317) | 31% |
| ls-premium @30 | -0.09 | -5.2% | 37% | -16% | - | -0.09 | - | - | - | -1.01 | -0.01 | +0.70 | +7.7% | 44 | -0.22 | 0.545 | 0.47 | -0.04 (0.550) | 32% |
| ls-funding | 0.47 | +9.1% | 27% | -19% | - | +0.47 | - | - | - | -0.21 | +0.80 | +0.58 | +7.8% | 44 | -0.26 | 0.207 | 0.74 | +0.23 (0.199) | 26% |
| ls-funding @30 | 0.10 | -0.6% | 27% | -19% | - | +0.10 | - | - | - | -0.43 | +0.41 | +0.08 | +7.8% | 44 | -0.26 | 0.415 | 0.57 | +0.05 (0.409) | 28% |

- `ls-premium`: 58 coins ever held, 4 of them delisted later in train; long leg alone Sharpe 0.43 (CAGR +9.6%, funding -2.5%/yr), short leg alone -0.18 (CAGR -15.3%, funding +10.5%/yr).
- `ls-funding`: 58 coins ever held, 4 of them delisted later in train; long leg alone Sharpe 0.59 (CAGR +16.1%, funding -2.5%/yr), short leg alone -0.21 (CAGR -16.6%, funding +10.6%/yr).

## Robustness sets (not part of the bars)

### B-all

First return day 2021-01-23, 4.8 years. Coins with data: 588 (26 without a price in train's last month, i.e. delisted); tradable per day median 129; weekly decisions 250.

| Shape | Sharpe | CAGR | Max DD | Worst week | 2020-21 | 2022-25 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | Funding/yr | Turn/yr | Corr twin | p(S>0) | Blend | Blend - twin (p) | Blend DD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 twin | 0.42 | +7.5% | 68% | -49% | +1.34 | -0.18 | - | +1.34 | -1.41 | +1.79 | +0.06 | -1.15 | +0.0% | 4 | +1.00 |  |  |  |  |
| tsmom12 perp | 0.30 | +0.4% | 71% | -49% | +1.07 | -0.22 | - | +1.07 | -1.37 | +1.81 | -0.07 | -1.11 | -8.3% | 4 | +1.00 |  |  |  |  |
| tsmom12 perp @30 | 0.28 | -0.7% | 72% | -49% | +1.05 | -0.25 | - | +1.05 | -1.39 | +1.76 | -0.10 | -1.15 | -8.3% | 4 | +1.00 |  |  |  |  |
| EW perp | 0.26 | -15.2% | 90% | -49% | +1.22 | -0.07 | - | +1.22 | -1.14 | +1.49 | +0.41 | -0.54 | -8.4% | 3 | +0.79 |  |  |  |  |
| EW perp @30 | 0.25 | -16.2% | 90% | -49% | +1.21 | -0.08 | - | +1.21 | -1.15 | +1.48 | +0.40 | -0.56 | -8.4% | 3 | +0.79 |  |  |  |  |
| ls-premium | 0.81 | +13.4% | 22% | -13% | +1.68 | +0.44 | - | +1.68 | +0.67 | -0.53 | +1.35 | +0.19 | +8.5% | 40 | -0.04 | 0.028 | 0.65 | +0.22 (0.033) | 40% |
| ls-premium @30 | 0.32 | +4.1% | 36% | -13% | +1.38 | -0.23 | - | +1.38 | +0.22 | -1.38 | +0.36 | -0.50 | +8.5% | 40 | -0.04 | 0.245 | 0.50 | +0.08 (0.265) | 42% |
| ls-funding | 1.17 | +20.3% | 20% | -14% | +1.89 | +0.92 | - | +1.89 | +1.06 | +0.17 | +2.30 | +0.20 | +9.1% | 41 | -0.04 | 0.004 | 0.75 | +0.32 (0.004) | 39% |
| ls-funding @30 | 0.64 | +10.1% | 26% | -14% | +1.58 | +0.17 | - | +1.58 | +0.57 | -0.82 | +1.23 | -0.71 | +9.1% | 41 | -0.04 | 0.085 | 0.60 | +0.17 (0.097) | 40% |

- `ls-premium`: 303 coins ever held, 16 of them delisted later in train.
- `ls-funding`: 302 coins ever held, 16 of them delisted later in train.

### B-P30 (perp closes)

First return day 2021-02-06, 4.8 years. Coins with data: 30 (0 without a price in train's last month, i.e. delisted); tradable per day median 24; weekly decisions 248.

| Shape | Sharpe | CAGR | Max DD | Worst week | 2020-21 | 2022-25 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | Funding/yr | Turn/yr | Corr twin | p(S>0) | Blend | Blend - twin (p) | Blend DD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 twin | 0.71 | +26.9% | 63% | -47% | +1.36 | +0.43 | - | +1.36 | -1.18 | +2.35 | +0.93 | -0.28 | +0.0% | 3 | +1.00 |  |  |  |  |
| tsmom12 perp | 0.57 | +17.2% | 63% | -46% | +1.08 | +0.36 | - | +1.08 | -1.15 | +2.27 | +0.78 | -0.30 | -9.2% | 3 | +1.00 |  |  |  |  |
| tsmom12 perp @30 | 0.55 | +16.1% | 63% | -46% | +1.07 | +0.34 | - | +1.07 | -1.17 | +2.23 | +0.76 | -0.32 | -9.2% | 3 | +1.00 |  |  |  |  |
| EW perp | 0.47 | +5.8% | 84% | -46% | +1.13 | +0.26 | - | +1.13 | -1.15 | +1.96 | +0.91 | -0.05 | -9.7% | 1 | +0.86 |  |  |  |  |
| EW perp @30 | 0.46 | +5.1% | 84% | -46% | +1.12 | +0.25 | - | +1.12 | -1.16 | +1.95 | +0.90 | -0.05 | -9.7% | 1 | +0.86 |  |  |  |  |
| ls-premium | 1.38 | +32.6% | 15% | -10% | +2.41 | +1.00 | - | +2.41 | +0.40 | -0.12 | +2.09 | +1.47 | +5.8% | 38 | -0.03 | 0.001 | 1.16 | +0.46 (0.002) | 35% |
| ls-premium @30 | 1.00 | +22.0% | 29% | -10% | +2.19 | +0.48 | - | +2.19 | -0.11 | -0.63 | +1.63 | +0.83 | +5.8% | 38 | -0.03 | 0.019 | 1.03 | +0.32 (0.024) | 35% |
| ls-funding | 1.10 | +23.8% | 16% | -11% | +1.72 | +0.91 | - | +1.72 | +0.37 | -0.25 | +1.82 | +1.74 | +6.4% | 38 | -0.08 | 0.006 | 1.07 | +0.37 (0.007) | 35% |
| ls-funding @30 | 0.71 | +13.9% | 30% | -11% | +1.47 | +0.38 | - | +1.47 | -0.10 | -0.80 | +1.31 | +1.12 | +6.4% | 38 | -0.08 | 0.060 | 0.93 | +0.23 (0.069) | 35% |

- `ls-premium`: 30 coins ever held, 0 of them delisted later in train.
- `ls-funding`: 30 coins ever held, 0 of them delisted later in train.
