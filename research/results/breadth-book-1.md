# breadth-book-1 results (2026-11-24 19:35 UTC)

Card `research/cards/breadth-book-1.md`. Train only (no bar after 2025-11-10). Sharpe above bills: cash earns the 13-week bill, Sharpe of the return above it. Gym Sharpe: cash earns 0 (the `tries.md` rows). Edge: paired stationary bootstrap (block 20 days, 2,000 draws), one-sided p. N_eff: participation ratio of the trailing 104-week correlation matrix, mean over month ends.

Eligible ETFs (33), round-robin order: SPY TLT GLD EEM FXE QQQ SHY USO EFA FXB IWM IEF SLV EWJ XLE LQD DBC EWG XLF EWA XLU EWP XLB EWU XLI EWQ XLY EWN XLP EWI XLK XLV VNQ

Coin list (2019-12-31 caps): BTC ETH XRP-CM BCH-CM LTC-CM EOS-CM BNB-CM BSV-CM ADA-CM XTZ-CM

### Candidate books: the six plus ETFs: window 2008-01-02 .. 2025-11-09, compared with `six`

| Set | N | Sharpe above bills | Edge (SE, z, p) | Gym Sharpe | Gym edge | CAGR | Max DD | Worst year | Turnover/yr | Exposure | N_eff (rho) | N_eff held | Eras ahead |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---|---:|---|
| `six` | 6 | 1.19 | - | 1.23 | - | +23.5% | 37.6% | 2018 -20.7% | 2.87 | 0.73 | 3.1 (0.11) | 2.4 | 0/4 |
| `L-12` | 12 | 0.96 | -0.226 (0.086, -2.63, 0.999) | 1.04 | -0.190 | +11.0% | 24.9% | 2018 -12.4% | 2.87 | 0.64 | 4.2 (0.21) | 3.1 | 0/4 |
| `L-20` | 20 | 0.83 | -0.352 (0.156, -2.25, 0.995) | 0.93 | -0.303 | +8.0% | 20.6% | 2018 -10.8% | 2.84 | 0.64 | 4.2 (0.26) | 3.2 | 0/4 |
| `L-all` | 35 | 0.65 | -0.538 (0.204, -2.64, 0.998) | 0.75 | -0.485 | +6.6% | 20.7% | 2018 -8.4% | 2.67 | 0.66 | 3.3 (0.40) | 2.9 | 0/4 |
| `six-live-form` | 6 | 1.32 | +0.133 (0.097, +1.37, 0.079) | 1.39 | +0.156 | +16.2% | 20.0% | 2018 -12.5% | 4.51 | 0.67 | 3.1 (0.11) | 2.4 | 3/4 |
| `L-all-live-form` | 35 | 0.58 | -0.607 (0.238, -2.55, 0.998) | 0.68 | -0.550 | +5.6% | 15.7% | 2008 -8.0% | 5.64 | 0.65 | 3.3 (0.40) | 2.9 | 0/4 |

Return inside the stress windows (gym convention):

| Set | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `six` | - | - | -21.6% | -13.6% | -6.3% | -23.1% | -19.7% |
| `L-12` | - | - | -13.6% | -5.2% | -4.6% | -12.7% | -9.2% |
| `L-20` | - | - | -12.4% | -1.4% | -4.1% | -10.7% | -4.1% |
| `L-all` | - | - | -18.6% | -7.1% | +1.6% | -7.2% | -7.6% |
| `six-live-form` | - | - | -13.9% | -10.7% | +4.1% | -13.1% | -13.9% |
| `L-all-live-form` | - | - | -14.5% | -6.1% | +3.3% | -5.8% | -6.1% |

Sharpe above bills per era:

| Set | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|
| `six` | -0.13 | 1.53 | 1.45 | 0.73 |
| `L-12` | -0.34 | 1.05 | 1.37 | 0.65 |
| `L-20` | -0.27 | 0.85 | 1.24 | 0.67 |
| `L-all` | -0.32 | 0.69 | 1.01 | 0.46 |
| `six-live-form` | -0.17 | 1.86 | 1.57 | 0.86 |
| `L-all-live-form` | -0.36 | 0.58 | 1.03 | 0.43 |

### Clean ETF breadth: ETF-only sets: window 2008-01-02 .. 2025-11-09, compared with `four`

| Set | N | Sharpe above bills | Edge (SE, z, p) | Gym Sharpe | Gym edge | CAGR | Max DD | Worst year | Turnover/yr | Exposure | N_eff (rho) | N_eff held | Eras ahead |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---|---:|---|
| `four` | 4 | 0.82 | - | 0.92 | - | +7.8% | 15.7% | 2022 -10.9% | 2.44 | 0.73 | 2.5 (0.13) | 1.9 | 0/4 |
| `E-6` | 6 | 0.61 | -0.205 (0.086, -2.39, 0.996) | 0.73 | -0.193 | +5.4% | 12.5% | 2022 -7.4% | 2.58 | 0.66 | 3.0 (0.24) | 2.2 | 0/4 |
| `E-12` | 12 | 0.40 | -0.415 (0.143, -2.91, 1.000) | 0.53 | -0.388 | +3.2% | 10.1% | 2018 -4.6% | 2.73 | 0.64 | 3.6 (0.23) | 2.6 | 0/4 |
| `E-20` | 20 | 0.34 | -0.476 (0.174, -2.74, 0.999) | 0.46 | -0.463 | +3.2% | 15.3% | 2018 -6.5% | 2.85 | 0.63 | 3.7 (0.30) | 2.9 | 0/4 |
| `E-all` | 33 | 0.37 | -0.446 (0.168, -2.66, 0.997) | 0.48 | -0.446 | +3.8% | 17.8% | 2008 -7.5% | 2.69 | 0.66 | 3.1 (0.41) | 2.8 | 0/4 |

Return inside the stress windows (gym convention):

| Set | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `four` | - | - | -12.4% | -11.3% | +13.3% | -2.3% | -9.8% |
| `E-6` | - | - | -10.3% | -7.7% | +5.8% | -2.7% | -7.2% |
| `E-12` | - | - | -8.4% | -3.6% | +2.7% | -2.8% | -4.0% |
| `E-20` | - | - | -11.9% | -0.6% | +0.5% | -4.9% | -1.0% |
| `E-all` | - | - | -17.5% | -6.9% | +4.9% | -4.5% | -6.1% |

Sharpe above bills per era:

| Set | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|
| `four` | -0.13 | 1.01 | 1.09 | 0.60 |
| `E-6` | -0.15 | 0.56 | 1.01 | 0.57 |
| `E-12` | -0.23 | 0.37 | 0.72 | 0.35 |
| `E-20` | -0.25 | 0.35 | 0.49 | 0.43 |
| `E-all` | -0.32 | 0.44 | 0.55 | 0.30 |

### ETF-only sets against the six: window 2008-01-02 .. 2025-11-09, compared with `six`

| Set | N | Sharpe above bills | Edge (SE, z, p) | Gym Sharpe | Gym edge | CAGR | Max DD | Worst year | Turnover/yr | Exposure | N_eff (rho) | N_eff held | Eras ahead |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---|---:|---|
| `six` | 6 | 1.19 | - | 1.23 | - | +23.5% | 37.6% | 2018 -20.7% | 2.87 | 0.73 | 3.1 (0.11) | 2.4 | 0/4 |
| `four` | 4 | 0.82 | -0.369 (0.252, -1.46, 0.932) | 0.92 | -0.312 | +7.8% | 15.7% | 2022 -10.9% | 2.44 | 0.73 | 2.5 (0.13) | 1.9 | 0/4 |
| `E-6` | 6 | 0.61 | -0.574 (0.253, -2.27, 0.991) | 0.73 | -0.505 | +5.4% | 12.5% | 2022 -7.4% | 2.58 | 0.66 | 3.0 (0.24) | 2.2 | 0/4 |
| `E-12` | 12 | 0.40 | -0.784 (0.265, -2.96, 0.999) | 0.53 | -0.700 | +3.2% | 10.1% | 2018 -4.6% | 2.73 | 0.64 | 3.6 (0.23) | 2.6 | 0/4 |
| `E-20` | 20 | 0.34 | -0.844 (0.274, -3.08, 1.000) | 0.46 | -0.775 | +3.2% | 15.3% | 2018 -6.5% | 2.85 | 0.63 | 3.7 (0.30) | 2.9 | 0/4 |
| `E-all` | 33 | 0.37 | -0.814 (0.265, -3.07, 1.000) | 0.48 | -0.757 | +3.8% | 17.8% | 2008 -7.5% | 2.69 | 0.66 | 3.1 (0.41) | 2.8 | 0/4 |

Return inside the stress windows (gym convention):

| Set | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `six` | - | - | -21.6% | -13.6% | -6.3% | -23.1% | -19.7% |
| `four` | - | - | -12.4% | -11.3% | +13.3% | -2.3% | -9.8% |
| `E-6` | - | - | -10.3% | -7.7% | +5.8% | -2.7% | -7.2% |
| `E-12` | - | - | -8.4% | -3.6% | +2.7% | -2.8% | -4.0% |
| `E-20` | - | - | -11.9% | -0.6% | +0.5% | -4.9% | -1.0% |
| `E-all` | - | - | -17.5% | -6.9% | +4.9% | -4.5% | -6.1% |

Sharpe above bills per era:

| Set | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|
| `six` | -0.13 | 1.53 | 1.45 | 0.73 |
| `four` | -0.13 | 1.01 | 1.09 | 0.60 |
| `E-6` | -0.15 | 0.56 | 1.01 | 0.57 |
| `E-12` | -0.23 | 0.37 | 0.72 | 0.35 |
| `E-20` | -0.25 | 0.35 | 0.49 | 0.43 |
| `E-all` | -0.32 | 0.44 | 0.55 | 0.30 |

`L-all-vol` holds the same assets as `L-all` (all eligible ETFs are in both orders), so it was not run (card).

### Clean coin breadth: coin-only sets: window 2020-01-01 .. 2025-11-09, compared with `C-2`

| Set | N | Sharpe above bills | Edge (SE, z, p) | Gym Sharpe | Gym edge | CAGR | Max DD | Worst year | Turnover/yr | Exposure | N_eff (rho) | N_eff held | Eras ahead |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---|---:|---|
| `C-2` | 2 | 1.14 | - | 1.17 | - | +65.4% | 57.4% | 2022 -18.1% | 2.29 | 0.71 | 1.2 (0.82) | 1.2 | 0/2 |
| `C-5` | 5 | 0.88 | -0.256 (0.192, -1.33, 0.917) | 0.91 | -0.258 | +43.6% | 62.7% | 2022 -12.4% | 4.44 | 0.64 | 1.7 (0.69) | 1.6 | 0/2 |
| `C-10` | 10 | 0.75 | -0.386 (0.210, -1.84, 0.970) | 0.78 | -0.396 | +31.6% | 60.7% | 2022 -13.6% | 4.42 | 0.56 | 2.0 (0.66) | 1.9 | 0/2 |

Return inside the stress windows (gym convention):

| Set | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `C-2` | - | - | -40.3% | -19.3% | - | - | -38.4% |
| `C-5` | - | - | -32.8% | -13.3% | - | - | -39.9% |
| `C-10` | - | - | -40.9% | -15.4% | - | - | -37.3% |

Sharpe above bills per era:

| Set | 2017-21 | 2022-25 |
|---|---:|---:|
| `C-2` | 1.77 | 0.63 |
| `C-5` | 1.31 | 0.56 |
| `C-10` | 1.28 | 0.27 |

### Candidate books from 2020: window 2020-01-01 .. 2025-11-09, compared with `six`

| Set | N | Sharpe above bills | Edge (SE, z, p) | Gym Sharpe | Gym edge | CAGR | Max DD | Worst year | Turnover/yr | Exposure | N_eff (rho) | N_eff held | Eras ahead |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---|---:|---|
| `six` | 6 | 1.20 | - | 1.28 | - | +29.5% | 28.8% | 2022 -12.9% | 2.76 | 0.69 | 3.4 (0.26) | 2.7 | 0/2 |
| `L-all` | 35 | 0.65 | -0.548 (0.276, -1.99, 0.971) | 0.84 | -0.438 | +8.4% | 18.9% | 2022 -6.2% | 2.77 | 0.69 | 3.3 (0.44) | 3.0 | 0/2 |
| `LC-all` | 43 | 0.73 | -0.474 (0.207, -2.29, 0.990) | 0.84 | -0.445 | +13.2% | 25.8% | 2022 -7.0% | 2.93 | 0.66 | 4.2 (0.38) | 3.5 | 0/2 |
| `six-live-form` | 6 | 1.24 | +0.045 (0.116, +0.39, 0.366) | 1.36 | +0.077 | +20.4% | 20.0% | 2022 -10.6% | 4.20 | 0.61 | 3.4 (0.26) | 2.7 | 2/2 |
| `LC-all-live-form` | 43 | 0.85 | -0.346 (0.255, -1.36, 0.920) | 1.03 | -0.251 | +9.8% | 15.2% | 2022 -5.0% | 5.40 | 0.59 | 4.2 (0.38) | 3.5 | 0/2 |

Return inside the stress windows (gym convention):

| Set | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `six` | - | - | -21.9% | -13.6% | - | - | -19.7% |
| `L-all` | - | - | -18.0% | -7.1% | - | - | -7.6% |
| `LC-all` | - | - | -21.2% | -8.0% | - | - | -12.9% |
| `six-live-form` | - | - | -13.9% | -10.8% | - | - | -14.0% |
| `LC-all-live-form` | - | - | -13.1% | -5.4% | - | - | -6.9% |

Sharpe above bills per era:

| Set | 2017-21 | 2022-25 |
|---|---:|---:|
| `six` | 1.82 | 0.71 |
| `L-all` | 0.93 | 0.46 |
| `LC-all` | 1.20 | 0.33 |
| `six-live-form` | 1.83 | 0.85 |
| `LC-all-live-form` | 1.44 | 0.47 |

Coins whose price stops before the end of the window: none.
