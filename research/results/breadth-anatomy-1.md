# breadth-anatomy-1 results (2026-11-25 00:05 UTC)

Card `research/cards/breadth-anatomy-1.md`. Window: decisions 2008-01-02 .. 2025-10-31, no bar after 2025-10-31. Sharpe = daily return above the 13-week bill, calendar days, 365-day year. Edges: paired stationary bootstrap (block 20, 2,000 draws), (SE, z). Descriptive: nothing here is a candidate book.

Added sets (the six's added ETFs, round-robin order): A-6: EEM FXE SHY USO EFA FXB; A-14: EEM FXE SHY USO EFA FXB IWM IEF SLV EWJ XLE LQD DBC EWG; A-29: EEM FXE SHY USO EFA FXB IWM IEF SLV EWJ XLE LQD DBC EWG XLF EWA XLU EWP XLB EWU XLI EWQ XLY EWN XLP EWI XLK XLV VNQ

## Step 0: reproduction (breadth-book-1 to 2025-11-09: six 1.19, L-12 0.96, L-20 0.83, L-all 0.65, four 0.82, E-all 0.37)

| Set | N | Sharpe above bills | Cash-0 Sharpe | Edge vs ref |
|---|---:|---:|---:|---|
| `six` | 6 | 1.19 | 1.24 | - |
| `four` | 4 | 0.82 | 0.92 | - |
| `L-12` | 12 | 0.97 | 1.05 | -0.228 (0.085, z -2.68) vs `six` |
| `L-20` | 20 | 0.84 | 0.93 | -0.356 (0.149, z -2.39) vs `six` |
| `L-all` | 35 | 0.65 | 0.75 | -0.544 (0.193, z -2.82) vs `six` |
| `E-all` | 33 | 0.37 | 0.47 | -0.448 (0.163, z -2.75) vs `four` |

## (a) Coin share

| Set | N | Mean coin weight | Coin share of variance | Sharpe |
|---|---:|---:|---:|---:|
| `six` | 6 | 0.147 | 0.83 | 1.19 |
| `L-12` | 12 | 0.072 | 0.64 | 0.97 |
| `L-20` | 20 | 0.043 | 0.36 | 0.84 |
| `L-all` | 35 | 0.024 | 0.13 | 0.65 |
| `K-12` | 12 | 0.147 | 0.88 | 1.03 |
| `K-20` | 20 | 0.147 | 0.87 | 1.03 |
| `K-all` | 35 | 0.147 | 0.83 | 1.02 |

Coins excluded from both (vs `four`):

| Set | N | Sharpe | Edge vs `four` |
|---|---:|---:|---|
| `X-10` | 10 | 0.38 | -0.442 (0.140, z -3.15) |
| `X-18` | 18 | 0.36 | -0.455 (0.168, z -2.70) |
| `X-33` | 33 | 0.37 | -0.448 (0.163, z -2.75) |

Split of the gap (coins held at the six's weight = `K`):

| k | SR(L) - SR(six) | ETF breadth, coins fixed: K - six | Coin dilution: L - K | Coin share of the gap |
|---|---|---|---|---:|
| 12 | -0.228 (0.085, z -2.68) | -0.167 (0.053, z -3.15) | -0.060 (0.065, z -0.92) | 26% |
| 20 | -0.356 (0.149, z -2.39) | -0.165 (0.063, z -2.60) | -0.191 (0.123, z -1.56) | 54% |
| all | -0.544 (0.193, z -2.82) | -0.174 (0.067, z -2.59) | -0.371 (0.166, z -2.23) | 68% |

## (b) Each asset's own tsmom12 sleeve (from its first eligible day in the window)

| Asset | Class | Group | Sleeve Sharpe | Sleeve vol | Exposure | Hold Sharpe |
|---|---|---|---:|---:|---:|---:|
| SPY | us-equity | six | 0.55 | 14.2% | 0.81 | 0.56 |
| QQQ | us-equity | six | 0.72 | 17.9% | 0.85 | 0.72 |
| GLD | commodities | six | 0.36 | 14.5% | 0.66 | 0.49 |
| TLT | bonds | six | 0.16 | 12.5% | 0.59 | 0.17 |
| BTC | crypto | six | 1.28 | 71.3% | 0.55 | 1.28 |
| ETH | crypto | six | 0.81 | 74.3% | 0.30 | 0.84 |
| EEM | intl-equity | A-6 | 0.12 | 15.4% | 0.61 | 0.19 |
| FXE | currencies | A-6 | -0.28 | 5.4% | 0.45 | -0.24 |
| SHY | bonds | A-6 | 0.46 | 1.3% | 0.86 | 0.19 |
| USO | commodities | A-6 | -0.14 | 20.6% | 0.48 | -0.17 |
| EFA | intl-equity | A-6 | -0.04 | 13.5% | 0.62 | 0.23 |
| FXB | currencies | A-6 | -0.33 | 5.0% | 0.45 | -0.27 |
| IWM | us-equity | A-14 | 0.22 | 16.0% | 0.67 | 0.39 |
| IEF | bonds | A-14 | 0.46 | 5.7% | 0.65 | 0.27 |
| SLV | commodities | A-14 | 0.33 | 23.6% | 0.53 | 0.31 |
| EWJ | intl-equity | A-14 | 0.13 | 13.5% | 0.63 | 0.24 |
| XLE | us-equity | A-14 | 0.11 | 19.2% | 0.63 | 0.23 |
| LQD | bonds | A-14 | 0.31 | 6.6% | 0.77 | 0.36 |
| DBC | commodities | A-14 | -0.02 | 13.6% | 0.48 | -0.03 |
| EWG | intl-equity | A-14 | 0.07 | 15.1% | 0.62 | 0.21 |
| XLF | us-equity | A-29 | 0.22 | 15.5% | 0.64 | 0.32 |
| EWA | intl-equity | A-29 | 0.04 | 16.2% | 0.64 | 0.23 |
| XLU | us-equity | A-29 | 0.21 | 15.0% | 0.80 | 0.43 |
| EWP | intl-equity | A-29 | 0.18 | 15.4% | 0.51 | 0.20 |
| XLB | us-equity | A-29 | 0.13 | 16.6% | 0.69 | 0.33 |
| EWU | intl-equity | A-29 | 0.09 | 12.9% | 0.59 | 0.20 |
| XLI | us-equity | A-29 | 0.34 | 15.0% | 0.78 | 0.50 |
| EWQ | intl-equity | A-29 | -0.26 | 15.6% | 0.58 | 0.23 |
| XLY | us-equity | A-29 | 0.68 | 16.9% | 0.82 | 0.61 |
| EWN | intl-equity | A-29 | 0.11 | 16.1% | 0.67 | 0.31 |
| XLP | us-equity | A-29 | 0.47 | 12.7% | 0.86 | 0.54 |
| EWI | intl-equity | A-29 | -0.06 | 16.7% | 0.52 | 0.16 |
| XLK | us-equity | A-29 | 0.57 | 18.8% | 0.84 | 0.70 |
| XLV | us-equity | A-29 | 0.45 | 13.8% | 0.79 | 0.57 |
| VNQ | us-equity | A-29 | 0.26 | 15.8% | 0.69 | 0.31 |

| Group | n | Mean sleeve Sharpe | Median | Mean hold Sharpe |
|---|---:|---:|---:|---:|
| six | 6 | 0.65 | 0.63 | 0.68 |
| four | 4 | 0.45 | 0.45 | 0.49 |
| C (BTC, ETH) | 2 | 1.05 | 1.05 | 1.06 |
| A-6 | 6 | -0.04 | -0.09 | -0.01 |
| A-14 | 14 | 0.10 | 0.11 | 0.14 |
| A-29 | 29 | 0.17 | 0.13 | 0.26 |
| A-29 us-equity | 11 | 0.33 | 0.26 | 0.45 |
| A-29 bonds | 3 | 0.41 | 0.46 | 0.27 |
| A-29 commodities | 3 | 0.06 | -0.02 | 0.04 |
| A-29 intl-equity | 10 | 0.04 | 0.08 | 0.22 |
| A-29 currencies | 2 | -0.31 | -0.31 | -0.26 |

Books on the added ETFs alone: `A-6` -0.10, `A-14` 0.18, `A-29` 0.29

## (c) Correlation of the weekly above-bill sleeve returns

| Weeks | n weeks | Within six | Within A-29 | Six x A-29 | Four x A-29 | rho(A-29 book, six book) | N_eff six | N_eff all 35 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 931 | 0.14 | 0.31 | 0.20 | 0.24 | 0.42 | 4.0 | 5.8 |
| market crises | 110 | 0.39 | 0.28 | 0.29 | 0.26 | 0.66 | 2.7 | 5.2 |
| not market crises | 821 | 0.10 | 0.33 | 0.19 | 0.24 | 0.37 | 4.1 | 5.7 |
| all 7 stress windows | 236 | 0.23 | 0.29 | 0.24 | 0.27 | 0.50 | 3.8 | 5.7 |
| outside them | 695 | 0.09 | 0.32 | 0.18 | 0.23 | 0.37 | 4.1 | 5.7 |

Two-book blend (static daily mix; weight w on the added book; rho = daily correlation; test = SR_A - rho x SR_ref, > 0 means a small weight on A helps):

| Ref | Added | SR_ref | SR_A | rho | rho x SR_ref | Test | w* | SR(w*) | SR at L-weight (actual L) | SR(1) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| `six` | `A-6` | 1.19 | -0.10 | 0.27 | 0.32 | -0.42 | 0.00 | 1.19 | 1.01 at w 0.50 (0.97) | -0.10 |
| `six` | `A-14` | 1.19 | 0.18 | 0.33 | 0.39 | -0.21 | 0.00 | 1.19 | 0.87 at w 0.70 (0.84) | 0.18 |
| `six` | `A-29` | 1.19 | 0.29 | 0.38 | 0.45 | -0.16 | 0.00 | 1.19 | 0.65 at w 0.83 (0.65) | 0.29 |
| `four` | `A-29` | 0.82 | 0.29 | 0.73 | 0.59 | -0.31 | 0.00 | 0.82 | 0.39 at w 0.83 (0.37) | 0.29 |

Per added sleeve, marginal test against the six and the four books (weekly rho):

| Asset | SR_i | rho_i six | SR_i - rho x SR_six | rho_i four | SR_i - rho x SR_four |
|---|---:|---:|---:|---:|---:|
| EEM | 0.12 | 0.26 | -0.19 | 0.48 | -0.28 |
| FXE | -0.28 | 0.20 | -0.52 | 0.28 | -0.51 |
| SHY | 0.46 | 0.00 | +0.45 | 0.06 | +0.40 |
| USO | -0.14 | 0.08 | -0.24 | 0.18 | -0.28 |
| EFA | -0.04 | 0.36 | -0.47 | 0.57 | -0.51 |
| FXB | -0.33 | 0.15 | -0.51 | 0.22 | -0.51 |
| IWM | 0.22 | 0.35 | -0.19 | 0.55 | -0.23 |
| IEF | 0.46 | 0.04 | +0.41 | 0.12 | +0.37 |
| SLV | 0.33 | 0.24 | +0.04 | 0.49 | -0.07 |
| EWJ | 0.13 | 0.30 | -0.22 | 0.49 | -0.27 |
| XLE | 0.11 | 0.15 | -0.07 | 0.32 | -0.15 |
| LQD | 0.31 | 0.16 | +0.12 | 0.38 | -0.00 |
| DBC | -0.02 | 0.12 | -0.16 | 0.24 | -0.22 |
| EWG | 0.07 | 0.28 | -0.26 | 0.45 | -0.30 |
| XLF | 0.22 | 0.28 | -0.11 | 0.48 | -0.17 |
| EWA | 0.04 | 0.28 | -0.29 | 0.50 | -0.36 |
| XLU | 0.21 | 0.23 | -0.06 | 0.45 | -0.15 |
| EWP | 0.18 | 0.17 | -0.03 | 0.34 | -0.10 |
| XLB | 0.13 | 0.33 | -0.26 | 0.52 | -0.29 |
| EWU | 0.09 | 0.25 | -0.21 | 0.48 | -0.30 |
| XLI | 0.34 | 0.31 | -0.03 | 0.56 | -0.12 |
| EWQ | -0.26 | 0.33 | -0.64 | 0.50 | -0.67 |
| XLY | 0.68 | 0.41 | +0.19 | 0.72 | +0.09 |
| EWN | 0.11 | 0.35 | -0.31 | 0.57 | -0.36 |
| XLP | 0.47 | 0.28 | +0.13 | 0.53 | +0.03 |
| EWI | -0.06 | 0.29 | -0.41 | 0.42 | -0.41 |
| XLK | 0.57 | 0.36 | +0.15 | 0.75 | -0.04 |
| XLV | 0.45 | 0.31 | +0.08 | 0.61 | -0.05 |
| VNQ | 0.26 | 0.26 | -0.05 | 0.54 | -0.18 |

Pass the marginal test: 8 of 29 against `six`, 4 of 29 against `four`.

## (d) Equal weight vs inverse-vol weight

| Set | SR equal | SR rw | Coin weight equal | Coin weight rw | Gap equal | Gap rw |
|---|---:|---:|---:|---:|---|---|
| `six` | 1.19 | 1.20 | 0.147 | 0.041 | - | - |
| `four` | 0.82 | 0.86 | 0.000 | 0.000 | - | - |
| `L-12` | 0.97 | 0.51 | 0.072 | 0.008 | -0.228 (0.085, z -2.68) | -0.689 (0.168, z -4.09) |
| `L-20` | 0.84 | 0.48 | 0.043 | 0.005 | -0.356 (0.149, z -2.39) | -0.717 (0.182, z -3.94) |
| `L-all` | 0.65 | 0.39 | 0.024 | 0.004 | -0.544 (0.193, z -2.82) | -0.808 (0.180, z -4.50) |
| `E-all` | 0.37 | 0.36 | 0.000 | 0.000 | -0.448 (0.163, z -2.75) | -0.493 (0.165, z -3.00) |

## (e) Period (one row; the asset-class view is tick-tier-1's)

| Span | six | four | L-all | E-all | A-29 | K-all | L-all - six |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2008-2009 | -0.13 | -0.13 | -0.32 | -0.32 | -0.34 | -0.32 | -0.19 |
| 2010-2025-10 | 1.29 | 0.94 | 0.74 | 0.44 | 0.35 | 1.11 | -0.54 |
