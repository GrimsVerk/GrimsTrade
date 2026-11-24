# vol-timing: is ls-trend-2's control just volatility timing of `tsmom12`?

Card: `cards/vol-timing.md` (committed before any number). Descriptive, no pick. Daily calendar excess returns over the 13-week T-bill, bill interest on idle cash, Sharpe a year in the repo's convention (daily, 365). P = 2007-04-01..2025-10-31, L = 2010-02-01..2025-10-31. Nothing after 2025-10-31 read.

## 1. Series

| Series | Mean share P | Sharpe P | Sharpe L | Vol P | Max DD P (excess) | Max DD P (total) | dSharpe P vs `tsmom12` | boot p (better) | 5%..95% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `tsmom12` | 1.00 | 1.21 | 1.32 | 18.3% | 38.3% | 35.6% | - | - | - |
| b1: split vs wide book (ls-trend-2 control) | 0.26 | 1.26 | 1.46 | 3.6% | 5.6% | 5.6% | +0.052 | 0.362 | -0.19..+0.28 |
| const: 0.26 x `tsmom12` + bills | 0.26 | 1.21 | 1.32 | 4.8% | 10.8% | 8.0% | +0.000 | 0.717 | -0.00..+0.00 |
| vt-own: `tsmom12` / own sigma52 + bills | 0.26 | 1.34 | 1.51 | 3.9% | 6.4% | 6.3% | +0.134 | 0.169 | -0.09..+0.36 |
| `trend-vol` tv40 | - | 1.21 | 1.34 | 11.7% | 24.0% | 20.7% | +0.001 | 0.491 | -0.14..+0.15 |

`trend-vol` mean exposure: see `results/trend-vol.md` (72% over 1994-2025); turnover 2.91 a year. b1 and vt-own: no cost on the monthly share reset (as ls-trend-2's control); `tsmom12`'s and tv40's gym costs are inside.

## 2. Decomposition of b1's Sharpe gain over `tsmom12`

| Part | P | L |
|---|---:|---:|
| total: S(b1) - S(`tsmom12`) | +0.052 | +0.142 |
| constant scaling: S(const) - S(`tsmom12`) | +0.000 | +0.000 |
| time-varying: S(b1) - S(const) | +0.052 | +0.142 |
|   of which own-vol timing: S(vt-own) - S(const) | +0.134 | +0.189 |
|   of which the wide book's vol in the split: S(b1) - S(vt-own) | -0.083 | -0.047 |
| `trend-vol` for comparison: S(tv40) - S(`tsmom12`) | +0.001 | +0.018 |

Share of b1's P gain from constant scaling 0%, time-varying 100%.

## 3. Weekly correlation (Monday-Sunday, compounded)

| Pair | P | L |
|---|---:|---:|
| b1 vs `trend-vol` (raw) | 0.88 | 0.88 |
| vt-own vs `trend-vol` (raw) | 0.87 | 0.86 |
| b1 vs `tsmom12` (raw) | 0.83 | 0.85 |
| `trend-vol` vs `tsmom12` (raw) | 0.92 | 0.92 |
| overlays: b1 vs `trend-vol`, residuals on `tsmom12` | 0.54 | 0.49 |
| overlays: vt-own vs `trend-vol`, residuals on `tsmom12` | 0.40 | 0.34 |
| overlays: b1 vs vt-own, residuals on `tsmom12` | 0.88 | 0.88 |

Weeks: P 969, L 821.

## 4. Crash windows (excess over bills, compounded)

| Series | 2008 | 2020-02..03 | 2022 |
|---|---:|---:|---:|
| `tsmom12` | -1.6% | -14.1% | -12.9% |
| b1: split vs wide book (ls-trend-2 control) | +0.9% | -2.4% | -1.5% |
| const: 0.26 x `tsmom12` + bills | -0.3% | -3.4% | -3.4% |
| vt-own: `tsmom12` / own sigma52 + bills | -0.4% | -2.7% | -1.4% |
| `trend-vol` tv40 | -0.5% | -9.6% | -12.1% |
