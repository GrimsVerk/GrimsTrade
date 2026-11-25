# forward-se-1: a dependence-robust standard error for the forward registry's verdict

Lane `forward-se-1`, 2026-11-25 (UTC). Engineering, with one simulation check. Card:
[`cards/forward-se-1.md`](cards/forward-se-1.md) (pushed as `27530c8` before any number). Code
`src/grimstrade/forward.py` (`hac_t`, `lag`, `critical`, `t_sf`), tests `tests/test_forward.py`,
check script [`forwardse1.py`](forwardse1.py), tables
[`results/forward-se-1.md`](results/forward-se-1.md) (30 s, numpy, deterministic). Inputs: the
committed weekly returns store through `evalue1.py`'s path generators, train only. No backtest,
no held-out year, no live record, no ledger or paper-trail change.

## Answer (one screen)

- **Done: the verdict's standard error now allows for a year of serial dependence.** Bartlett
  (Newey-West) long-run variance, lags = one year of observations (51 for weekly bars), at
  most n / 4; p from a Student-t approximation to the fixed-b distribution (Kiefer and
  Vogelsang 2005). With no lags it is the ordinary t-test; on iid data it gives the old p
  within 0.01 (tested). `sharpe` uses the same statistic (Lo 2002 at the null). `min_sample`
  uses the new test's critical value and a plan field `lrv` (long-run variance ratio,
  measured on the train record at freeze). Fixed before any live verdict: the registry holds
  no frozen line.
- **The card's bar failed at 10 years for difference books.** Null rejection at nominal 2.5%
  on 52-week block-resampled store paths:

  | Null | Old, 10 y | New, 10 y | Old, 100 y | New, 100 y |
  |---|---:|---:|---:|---:|
  | vs `tsmom12`, rho 0.77 (`mean`) | 0.064 | 0.059 | 0.047 | 0.036 |
  | vs `tsmom12`, rho 0.88 (`mean`) | 0.062 | 0.050 | 0.046 | 0.035 |
  | vs `tsmom12`, rho 0.95 (`mean`) | 0.061 | 0.044 | 0.046 | 0.031 |
  | `tsmom12` vs 0 (`sharpe`) | 0.081 | 0.010 | 0.083 | 0.023 |
  | Gaussian iid, difference | 0.026 | 0.024 | 0.024 | 0.024 |
  | Gaussian iid, vs 0 | 0.026 | 0.027 | 0.026 | 0.027 |

  The bar asked for at most 0.035 everywhere; the 10-year difference cells (0.044-0.059) and
  one 100-year cell (0.0356) miss it. Book against zero: from 8% to 1.0% / 2.3% (now
  conservative). The Gaussian controls keep their level.
- **What is left is skew, not the standard error** (diagnostic added after the result): the
  upper and lower tails of the new statistic are lopsided (difference at rho 0.88, 10 years:
  5.2% above, 2.1% below, mean 3.6%; at 100 years 3.0% / 2.3%). A 10-year read averages about
  10 yearly sums, whose skewness is median -0.3 for the differences (p10 -2.1) and +1.8 for
  `tsmom12`; a one-sided t on 10 skewed values is lopsided whatever its standard error. The
  card's limit also holds: 52-week blocks put all simulated dependence within a year, which a
  one-year window covers by construction, so this checks the implementation, not that real
  dependence stops at a year (104-week blocks: 6.5% at 10 years, 3.3% at 100).
- **Power at the new min_sample:** own Sharpe 1.0 vs 0, Gaussian, lrv 1: 503 weeks, power
  0.83 (target 0.80). On resampled `tsmom12` with lrv 1 the same n gives 0.66; with its
  measured lrv 2.14, 974 weeks (18.7 years) give 0.95. So `lrv` must be measured at freeze,
  not left at 1.

## Recommendation (for the lead)

1. Merge as an improvement, not a fix: every resampled cell's level falls (difference books at
   10 years from 6.1-6.4% to 4.4-5.9%, books against zero from 8% to at most 2.3%), iid data
   keep their answer, and nothing live changes (the daily runner does not import
   `grimstrade.forward`; the scoreboard and registry outputs of the dry run are identical).
   Read a 10-year verdict of a book against `tsmom12` as a 5%-level test, not 2.5%.
2. Measure `lrv` on the train record at every freeze (Bartlett, same lags); with lrv 1 a
   trend-like book is under-powered (0.66 instead of 0.80).
3. If the 2.5% level must hold at 10 years: a longer read (the 100-year level is 3.1-3.6%,
   and the skew term shrinks as 1 / sqrt(years)) or a stricter per-rule alpha. A skew
   correction fitted on the train record's yearly sums (about 30 of them, skew SE about 0.45)
   would pass this simulation by construction and was not tried.

## Daily dry run

See the PR body: `run_daily --root <copy of paper-trail>` and `--intraday <dir>` exit 0; the
scoreboard, backtest and weekly reports the branch writes equal those that `origin/main`'s code
renders from the same copy, byte for byte.

Tries rows: one `note` row (`forward-se`), no selectable try.
