# risk-menu-3: own-vol targeting without look-ahead; under-water dates (descriptive)

Card: `cards/risk-menu-3.md` (committed before any number). Footing as risk-menu-2: daily calendar returns, gym costs, 5 bps per monthly reset, idle cash at the 13-week T-bill; Sharpe on excess returns (365-day convention), other measures on the total-return curve. W = 1994-02-01..2025-10-31, P = 2007-04-01..2025-10-31 (the W-built series cut to P). Expanding k: on each 1st, k solves mean(min(1, k / sigma_m)) = T over all monthly sigmas known by then; share T for the first 24 sigmas (warm-up). Nothing after 2025-10-31 read.

## 1. Expanding k against the re-fitted k

Re-fitted = risk-menu-2's numbers on W, risk-menu's on P (k solved on that window). This run's re-fitted W row is shown as a check against risk-menu-2.

| Window | Item | Sharpe (SE) | Growth/yr | Vol | Worst loss | Worst 12 months | Longest under water | Mean share |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| W | Own-vol 26%, re-fitted k | 1.03 (0.18) | 6.0% | 3.3% | 5.4% | -2.7% | 1.3 y | 0.26 |
| W | Own-vol 26%, expanding k | 0.97 (0.18) | 5.6% | 3.1% | 5.2% | -2.4% | 1.3 y | 0.24 |
| W | Own-vol 70%, re-fitted k | 1.08 (0.18) | 12.9% | 9.4% | 16.9% | -8.1% | 3.3 y | 0.70 |
| W | Own-vol 70%, expanding k | 1.04 (0.18) | 11.8% | 8.8% | 15.7% | -7.6% | 3.4 y | 0.66 |
| W | `tsmom12`, full size (context) | 0.94 (0.18) | 18.5% | 17.0% | 35.6% | -29.2% | 5.7 y | - |
| W | `tsmom12` 26% + T-bills (context) | 0.94 (0.18) | 6.7% | 4.4% | 8.1% | -6.8% | 2.4 y | - |
| W | `tsmom12` 70% + T-bills (context) | 0.94 (0.18) | 13.8% | 11.9% | 24.6% | -20.6% | 4.7 y | - |
| P | Own-vol 26%, re-fitted k | 1.34 (0.24) | 6.7% | 3.9% | 6.3% | -3.2% | 1.3 y | 0.26 |
| P | Own-vol 26%, expanding k | 1.31 (0.24) | 5.4% | 3.0% | 5.2% | -2.4% | 1.3 y | 0.20 |
| P | Own-vol 70%, re-fitted k | 1.33 (0.24) | 15.9% | 10.5% | 18.2% | -8.4% | 2.2 y | 0.70 |
| P | Own-vol 70%, expanding k | 1.32 (0.24) | 13.8% | 9.1% | 15.7% | -7.6% | 2.1 y | 0.61 |
| P | `tsmom12`, full size (context) | 1.21 (0.24) | 24.4% | 18.3% | 35.6% | -29.2% | 2.6 y | - |
| P | `tsmom12` 26% + T-bills (context) | 1.22 (0.24) | 7.4% | 4.8% | 8.1% | -6.8% | 2.1 y | - |
| P | `tsmom12` 70% + T-bills (context) | 1.22 (0.24) | 17.6% | 12.8% | 24.6% | -20.6% | 2.6 y | - |

| Change, expanding minus re-fitted | Sharpe | Growth/yr | Worst loss | Worst 12 months | Under water |
|---|---:|---:|---:|---:|---:|
| W 26% | -0.06 | -0.4 pt | -0.2 pt | +0.3 pt | +0.0 y |
| W 70% | -0.04 | -1.1 pt | -1.2 pt | +0.5 pt | +0.2 y |
| P 26% | -0.03 | -1.3 pt | -1.1 pt | +0.8 pt | +0.0 y |
| P 70% | -0.01 | -2.1 pt | -2.4 pt | +0.7 pt | -0.1 y |

Check: this run's re-fitted W Sharpe minus risk-menu-2's: 26% +0.000, 70% +0.000.

k (annual vol units; share = min(1, k / sigma52)):

- vt-own 26% x: first solved 1997-02-01, range 0.018...0.038, last 0.026
- vt-own 70% x: first solved 1997-02-01, range 0.068...0.110, last 0.084

## 2. Longest spell under water on W (1994-02-01..2025-10-31)

High = the last day at the old high before the spell; low = the spell's lowest day; back = the first day at or above the old high again. Calendar days: bills accrue on weekends and holidays, so a high can fall on one (2000-03-26 is the Sunday after the Friday 2000-03-24 close).

| Item | Years | High | Low | Back |
|---|---:|---|---|---|
| Hold the six (equal weight) | 11.1 | 2000-03-26 | 2002-10-09 | 2011-04-25 |
| 60/40 (SPY / TLT) | 4.3 | 2000-09-04 | 2002-10-09 | 2004-12-10 |
| `tsmom12`, full size | 5.7 | 2000-03-26 | 2000-11-20 | 2005-12-08 |
| `tsmom12` 70% + T-bills | 4.7 | 2000-03-26 | 2000-11-20 | 2004-12-14 |
| `tsmom12` 26% + T-bills | 2.4 | 2000-09-04 | 2000-10-12 | 2003-01-13 |
| Own-vol target 26%, k re-fitted on W | 1.3 | 2014-07-12 | 2015-08-25 | 2015-10-22 |
| Own-vol target 26%, expanding k (no look-ahead) | 1.3 | 2014-07-12 | 2015-08-25 | 2015-10-22 |
| Own-vol target 70%, k re-fitted on W | 3.3 | 2000-03-26 | 2000-04-14 | 2003-07-08 |
| Own-vol target 70%, expanding k (no look-ahead) | 3.4 | 2000-03-26 | 2000-04-14 | 2003-09-02 |
