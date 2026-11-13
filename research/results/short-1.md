# Short 1: raw tables (train, decisions to 2025-11-09)

Script `lib/short1.py`; card and reading in `research/short-1.md`. Perp shapes at 10 bps a side plus every funding event; `@30` rows: the same at 30 bps (robustness). `tsmom12 spot`: long-only on spot at 30 bps, no funding (the twin). Sharpe on daily returns, 365 days. `Funding/yr`: funding received (+) or paid (-) per year, share of equity. `Corr ts`: daily correlation with `tsmom12 spot`. `vs tsmom12 (p)`: Sharpe difference to the spot twin, bootstrap one-sided p, and to the perp long-only twin. Blend: 50% `tsmom12 spot` + 50% the long-short book, re-split daily. Verdict: the card's bars that failed, by number.

### Book P30

From 2020-02-15 (first return day) to 2025-11-10. Coins: 30, tradable per day median 22. Weekly decisions: 299. Short spells of `tsmom12-ls` (365-day return < 0, gaps < 30 days merged, >= 30 days): 90 over all coins, 2 for BTC.

| Shape | Sharpe | CAGR | Max DD | Worst week | 2020-21 | 2022-25 | Funding/yr | Turn/yr | Corr ts | vs tsmom12 (p) | Blend Sharpe | Blend - ts (p) | Blend DD | DD>10% spells | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| tsmom12 spot | 1.03 | +56.3% | 62% | -45% | +1.72 | +0.45 | +0.0% | 3 | +1.00 |  |  |  |  |  |  |
| tsmom12 perp | 0.88 | +42.5% | 62% | -45% | +1.47 | +0.38 | -10.8% | 3 | +1.00 |  |  |  |  |  |  |
| tsmom12 perp @30 | 0.86 | +41.0% | 62% | -45% | +1.46 | +0.36 | -10.8% | 3 | +1.00 |  |  |  |  |  |  |
| EW perp | 0.80 | +36.5% | 82% | -52% | +1.61 | +0.25 | -11.8% | 1 | +0.88 |  |  |  |  |  |  |
| EW perp @30 | 0.79 | +35.4% | 82% | -52% | +1.60 | +0.24 | -11.8% | 1 | +0.88 |  |  |  |  |  |  |
| tsmom12-ls | 0.73 | +29.6% | 62% | -45% | +1.24 | +0.31 | -9.6% | 7 | +0.81 | -0.30 (0.88); perp -0.16 |  |  |  |  | fails 1,2 |
| tsmom12-ls @30 | 0.69 | +26.7% | 63% | -45% | +1.22 | +0.26 | -9.6% | 7 | +0.81 | -0.34 (0.91); perp -0.19 |  |  |  |  |  |
| ls-low_vol | -0.43 | -20.0% | 81% | -58% | -1.04 | +0.21 | +1.0% | 10 | -0.39 |  | 0.84 | -0.19 (0.75) | 33% | 2 | fails 1,2,4,5 |
| ls-low_vol @30 | -0.52 | -22.5% | 83% | -58% | -1.10 | +0.08 | +1.0% | 10 | -0.39 |  | 0.79 | -0.24 (0.81) | 34% | 2 |  |
| ls-size | -0.62 | -27.8% | 90% | -57% | -1.17 | -0.06 | +0.4% | 5 | -0.34 |  | 0.67 | -0.36 (0.91) | 40% | 3 | fails 1,2,4,5 |
| ls-size @30 | -0.68 | -29.4% | 91% | -58% | -1.21 | -0.15 | +0.4% | 5 | -0.34 |  | 0.63 | -0.40 (0.93) | 40% | 3 |  |
| ls-turnover | -0.54 | -20.5% | 87% | -54% | -0.87 | -0.26 | -0.8% | 10 | -0.34 |  | 0.79 | -0.24 (0.85) | 37% | 2 | fails 1,2,4,5 |
| ls-turnover @30 | -0.63 | -22.9% | 88% | -54% | -0.95 | -0.40 | -0.8% | 10 | -0.34 |  | 0.74 | -0.29 (0.90) | 39% | 2 |  |
| ls-funding | 0.78 | +20.7% | 48% | -21% | +0.85 | +0.95 | +7.5% | 39 | +0.10 |  | 1.22 | +0.19 (0.12) | 33% | 4 | fails 1,5 |
| ls-funding @30 | 0.49 | +11.0% | 52% | -21% | +0.64 | +0.44 | +7.5% | 39 | +0.10 |  | 1.10 | +0.07 (0.35) | 35% | 2 |  |
| ls-premium | 0.83 | +23.1% | 49% | -30% | +0.77 | +1.21 | +6.8% | 40 | +0.08 |  | 1.25 | +0.22 (0.10) | 34% | 5 | fails 5 |
| ls-premium @30 | 0.54 | +12.9% | 54% | -30% | +0.58 | +0.69 | +6.8% | 40 | +0.08 |  | 1.13 | +0.10 (0.28) | 35% | 4 |  |
| ls-trend | 0.24 | +2.7% | 51% | -27% | +0.96 | -0.41 | +0.4% | 11 | -0.03 |  | 1.04 | +0.02 (0.47) | 38% | 4 | fails 1,2,5 |
| ls-trend @30 | 0.13 | -0.6% | 55% | -27% | +0.87 | -0.54 | +0.4% | 11 | -0.03 |  | 1.00 | -0.03 (0.56) | 39% | 4 |  |
| ls-combo | -0.34 | -16.5% | 79% | -55% | -0.82 | +0.16 | +2.6% | 17 | -0.38 |  | 0.90 | -0.12 (0.69) | 32% | 2 | fails 1,2,4,5 |
| ls-combo @30 | -0.47 | -20.2% | 82% | -56% | -0.92 | -0.03 | +2.6% | 17 | -0.38 |  | 0.83 | -0.20 (0.78) | 33% | 2 |  |
| ls-rev_1 (daily) | -1.97 | -50.4% | 98% | -21% | -1.81 | -2.81 | +0.3% | 483 | +0.12 |  | -0.00 | -1.03 (1.00) | 68% | 1 | fails 1,2,3,4,5 |
| ls-rev_1 (daily) @30 | -5.04 | -81.4% | 100% | -23% | -3.77 | -8.51 | +0.3% | 483 | +0.11 |  | -1.33 | -2.35 (1.00) | 96% | 1 |  |

### Book BTC-ETH

From 2020-01-04 (first return day) to 2025-11-10. Coins: 2, tradable per day median 2. Weekly decisions: 305. Short spells of `tsmom12-ls` (365-day return < 0, gaps < 30 days merged, >= 30 days): 6 over all coins, 2 for BTC.

| Shape | Sharpe | CAGR | Max DD | Worst week | 2020-21 | 2022-25 | Funding/yr | Turn/yr | Corr ts | vs tsmom12 (p) | Blend Sharpe | Blend - ts (p) | Blend DD | DD>10% spells | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| tsmom12 spot | 1.19 | +67.6% | 58% | -50% | +1.79 | +0.72 | +0.0% | 2 | +1.00 |  |  |  |  |  |  |
| tsmom12 perp | 0.98 | +48.3% | 59% | -50% | +1.48 | +0.58 | -12.9% | 2 | +1.00 |  |  |  |  |  |  |
| tsmom12 perp @30 | 0.97 | +47.5% | 59% | -50% | +1.47 | +0.58 | -12.9% | 2 | +1.00 |  |  |  |  |  |  |
| EW perp | 0.92 | +48.2% | 77% | -50% | +1.68 | +0.38 | -14.4% | 0 | +0.88 |  |  |  |  |  |  |
| EW perp @30 | 0.92 | +47.8% | 77% | -50% | +1.67 | +0.37 | -14.4% | 0 | +0.88 |  |  |  |  |  |  |
| tsmom12-ls | 0.76 | +31.8% | 63% | -50% | +1.22 | +0.42 | -11.3% | 3 | +0.86 | -0.43 (0.96); perp -0.22 |  |  |  |  | fails 1,2 |
| tsmom12-ls @30 | 0.74 | +30.2% | 63% | -50% | +1.20 | +0.40 | -11.3% | 3 | +0.86 | -0.45 (0.97); perp -0.24 |  |  |  |  |  |
