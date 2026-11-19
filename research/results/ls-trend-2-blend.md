# ls-trend-2 Part A: `tsmom12` + wide long-short TSMOM at gross <= 1

Card: `cards/ls-trend-2.md` (committed before any number). One blend, equal risk between `tsmom12` and wide-LS rescaled to gross 1, split from trailing 52-week volatility only, reset monthly. Daily calendar excess returns over the 13-week T-bill; Sharpe a year in the repo's convention (daily, 365). P = 2007-04-01..2025-10-31 (decides), L = 2010-02-01..2025-10-31, F = 1995-03-01..2025-10-31. Nothing after 2025-10-31 read.

## 1. The test (a): Sharpe of the blend minus `tsmom12`

| Window | Blend | `tsmom12` | Difference | Bootstrap p (blend better) | 5%..95% |
|---|---:|---:|---:|---:|---:|
| P (decides) | 0.97 | 1.21 | -0.24 | 0.8879 | -0.58..+0.09 |
| L | 1.13 | 1.32 | -0.18 | 0.8048 | -0.55..+0.17 |

Paired stationary bootstrap, mean block 20 days, 20,000 draws, seed 0. Family bar p < 0.00147; project-wide (N 1,012 + this card's rows) p <= 4.9e-05. **(a) fails.**

## 2. Sharpe, risk, split, gross

| Series | Sharpe P | Sharpe L | Sharpe F | Vol P | Max DD P | Worst year P |
|---|---:|---:|---:|---:|---:|---:|
| blend-er | 0.97 | 1.13 | 0.79 | 5.4% | 8.8% | -3.3% (2009) |
| tsmom12 | 1.21 | 1.32 | 0.96 | 18.3% | 38.3% | -20.8% (2018) |
| tsmom12-split-bills (b1) | 1.26 | 1.46 | 0.91 | 3.6% | 5.6% | -1.7% (2018) |
| tsmom12 at the blend's vol, k 0.30 (b2) | 1.21 | 1.32 | 0.96 | 5.4% | 12.2% | -6.0% (2018) |
| wide-LS-g1 | 0.14 | 0.09 | 0.37 | 5.1% | 16.2% | -7.3% (2009) |
| wide-LS raw (ls-trend-1) | 0.21 | 0.15 | 0.58 | 17.1% | 39.7% | -18.5% (2016) |
| blend-er-cost2 | 0.83 | 0.96 | 0.71 | 5.4% | 9.0% | -3.9% (2018) |

Split to `tsmom12` in P: mean 0.26, min 0.05, max 0.85 (the rest in wide-LS-g1). Combined gross: mean 0.93, max 1.000 (card: <= 1); net exposure mean +0.30. wide-LS-g1 alone: net mean +0.17; wide-LS raw gross mean 4.09.

## 3. Costs a year in P

| Item | In the sleeve (own capital) | In the blend (at its weights) |
|---|---:|---:|
| wide-LS-g1 trading (5 bps a side) | 0.14% | 0.11% |
| wide-LS-g1 borrow (1% a year on shorts) | 0.42% | 0.32% |
| `tsmom12` gym costs (with-cost vs no-cost re-score) | 0.26% | 0.06% |
| split reset (5 bps a side) | - | 0.02% |
| **total** | | **0.50%** |

For scale, wide-LS raw (3.7x gross) in P: trading 0.64%, borrow 1.67% a year. Cost stress (10 bps, 3% borrow): blend Sharpe P 0.83.

## 4. Crash windows (compounded monthly excess)

| Series | 2008 | 2020-02..03 | 2022 |
|---|---:|---:|---:|
| blend-er | +8.9% | +2.2% | +2.0% |
| tsmom12 | -1.6% | -14.1% | -12.9% |
| tsmom12-split-bills (b1) | +0.9% | -2.4% | -1.5% |
| tsmom12 at the blend's vol, k 0.30 (b2) | -0.4% | -3.8% | -3.9% |
| wide-LS-g1 | +13.9% | +5.5% | +3.3% |
| wide-LS raw (ls-trend-1) | +34.9% | +24.6% | +12.8% |
| blend-er-cost2 | +8.5% | +2.0% | +0.6% |

How much of the crash help survives at <= 1x: wide-LS-g1 / wide-LS raw = 2008 40%, 2020-02..03 22%, 2022 26%. The blend's gain over the dilution control (b1), in points: 2008 +8.0, 2020-02..03 +4.6, 2022 +3.5.

- (b) blend above `tsmom12` in all three: **yes** (a risk preference, not an edge).
- (b1) blend above the dilution control in all three: yes.
- (b2) blend above `tsmom12` at equal vol: 2008 yes, 2020-02..03 yes, 2022 yes.

## 5. Correlation of monthly excess returns in L

| Series | TC | SPY | tsmom12 | wide-LS-g1 |
|---|---:|---:|---:|---:|
| blend-er | 0.49 (189) | 0.23 (189) | 0.67 (189) | 0.63 (189) |
| tsmom12 | 0.17 (189) | 0.40 (189) | 1.00 (189) | 0.05 (189) |
| wide-LS-g1 | 0.62 (189) | -0.21 (189) | 0.05 (189) | 1.00 (189) |

## Verdict (card's wording): **a risk choice, not an edge**.

Months the split was kept (a sleeve's trailing vol 0): 6.
Rows logged this run: 6.
