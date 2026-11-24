# risk-menu: the risk dials side by side (descriptive, no pick)

Card: `cards/risk-menu.md` (committed before any number). P = 2007-04-01..2025-10-31; Sharpe on daily excess returns over the 13-week T-bill (365-day convention); every other measure on the total-return curve (bill interest on idle cash). Costs: gym costs for gym-run rules, 5 bps a side and 1% borrow in the wide book, 5 bps on each monthly share reset. Nothing after 2025-10-31 read.

Equal-risk blend reproduced: Sharpe P 0.97 (ls-trend-2: 0.97).

## 1. Return and risk

| Item | Sharpe P (SE) | Sharpe L | Growth/yr | Vol | Worst loss | Worst 12 months | Longest under water | 2008 | 2020 Q1 | 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Hold the six (equal weight) | 1.15 (0.24) | 1.26 | 27.4% | 21.9% | 47.0% | -44.9% | 2.3 y | -11.7% | +0.4% | -36.5% |
| 60/40 (SPY / TLT) | 0.66 (0.23) | 0.88 | 8.7% | 11.5% | 30.2% | -25.4% | 2.8 y | -12.0% | -3.5% | -23.0% |
| `tsmom12`, full size | 1.21 (0.24) | 1.32 | 24.4% | 18.3% | 35.6% | -29.2% | 2.6 y | -0.2% | -6.8% | -11.2% |
| `tsmom12` 70% + T-bills | 1.22 (0.24) | 1.32 | 17.6% | 12.8% | 24.6% | -20.6% | 2.6 y | +0.3% | -4.4% | -7.3% |
| `tsmom12` 26% + T-bills | 1.22 (0.24) | 1.33 | 7.4% | 4.8% | 8.1% | -6.8% | 2.1 y | +1.0% | -1.3% | -1.5% |
| Own-vol target, mean share 26% | 1.34 (0.24) | 1.50 | 6.7% | 3.9% | 6.3% | -3.2% | 1.3 y | +1.0% | -0.7% | +0.6% |
| Own-vol target, mean share 70% | 1.33 (0.24) | 1.50 | 15.9% | 10.5% | 18.2% | -8.4% | 2.2 y | -0.2% | -2.9% | -2.2% |
| Equal-risk blend with wide-LS (ls-trend-2) | 0.97 (0.23) | 1.13 | 6.7% | 5.4% | 8.7% | -4.2% | 1.8 y | +10.4% | +4.4% | +4.1% |
| `tsmom12` 90% / wide-LS 10% | 1.21 (0.24) | 1.32 | 22.2% | 16.5% | 31.9% | -26.6% | 2.6 y | +1.3% | -5.4% | -9.6% |
| `tsmom12` 70% / wide-LS 30% | 1.21 (0.24) | 1.32 | 17.8% | 13.1% | 24.1% | -21.4% | 2.6 y | +4.4% | -2.6% | -6.3% |
| `tsmom12` 50% / wide-LS 50% | 1.18 (0.24) | 1.30 | 13.3% | 9.9% | 16.2% | -15.9% | 2.5 y | +7.5% | +0.1% | -3.0% |

## 2. How it is held

| Item | Mean `tsmom12` share | Average exposure (gross) | Orders a year | Turnover a year |
|---|---:|---:|---:|---:|
| Hold the six (equal weight) | - | 1.00 | 99 | 1.25 |
| 60/40 (SPY / TLT) | - | 1.00 | 45 | 0.47 |
| `tsmom12`, full size | 1.00 | 0.74 | 81 | 2.74 |
| `tsmom12` 70% + T-bills | 0.70 | 0.52 | 96 (approx.) | 2.00 |
| `tsmom12` 26% + T-bills | 0.26 | 0.19 | 95 (approx.) | 0.79 |
| Own-vol target, mean share 26% | 0.26 | 0.19 | 106 (approx.) | 0.91 |
| Own-vol target, mean share 70% | 0.70 | 0.52 | 108 (approx.) | 2.18 |
| Equal-risk blend with wide-LS (ls-trend-2) | 0.26 | 0.93 | 504 (approx.) | 3.22 |
| `tsmom12` 90% / wide-LS 10% | 0.90 | 0.76 | 464 (approx.) | 2.82 |
| `tsmom12` 70% / wide-LS 30% | 0.70 | 0.82 | 474 (approx.) | 2.94 |
| `tsmom12` 50% / wide-LS 50% | 0.50 | 0.87 | 475 (approx.) | 3.00 |

Orders: exact gym fills in P for gym-run rules. Mixes: `tsmom12`'s fills, plus one order per held `tsmom12` asset at each monthly reset that moves its share by at least 1 point, plus for blends the wide book's held positions once a month (377 a year). Turnover: gym-run rules over their whole run; mixes share-weighted sleeve turnover in P plus resets.

## 3. Sharpe differences (paired stationary bootstrap, block 20 days, 2,000 draws, seed 0; description, not a test)

| Item | vs hold six: d (5%..95%) | vs `tsmom12`: d (5%..95%) | vs best (vt-own 26%): d (5%..95%) |
|---|---:|---:|---:|
| Hold the six (equal weight) | - | -0.06 (-0.28..+0.16) | -0.19 (-0.51..+0.13) |
| 60/40 (SPY / TLT) | -0.49 (-0.87..-0.12) | -0.55 (-1.00..-0.12) | -0.68 (-1.16..-0.23) |
| `tsmom12`, full size | +0.06 (-0.16..+0.28) | - | -0.13 (-0.35..+0.09) |
| `tsmom12` 70% + T-bills | +0.06 (-0.16..+0.28) | +0.01 (-0.00..+0.01) | -0.13 (-0.35..+0.10) |
| `tsmom12` 26% + T-bills | +0.07 (-0.15..+0.29) | +0.01 (-0.01..+0.03) | -0.12 (-0.34..+0.10) |
| Own-vol target, mean share 26% | +0.19 (-0.13..+0.51) | +0.13 (-0.09..+0.35) | - |
| Own-vol target, mean share 70% | +0.18 (-0.12..+0.49) | +0.12 (-0.06..+0.32) | -0.01 (-0.08..+0.07) |
| Equal-risk blend with wide-LS (ls-trend-2) | -0.18 (-0.58..+0.21) | -0.24 (-0.57..+0.08) | -0.37 (-0.66..-0.08) |
| `tsmom12` 90% / wide-LS 10% | +0.06 (-0.16..+0.28) | +0.00 (-0.01..+0.01) | -0.13 (-0.35..+0.09) |
| `tsmom12` 70% / wide-LS 30% | +0.05 (-0.18..+0.28) | -0.00 (-0.05..+0.04) | -0.13 (-0.36..+0.09) |
| `tsmom12` 50% / wide-LS 50% | +0.02 (-0.23..+0.27) | -0.03 (-0.14..+0.06) | -0.16 (-0.40..+0.07) |
