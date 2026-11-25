# forward-se-1: a dependence-robust standard error for the forward registry's verdict

Lane `forward-se-1`, 2026-11-25 (UTC). Engineering, with one simulation check. Card:
[`cards/forward-se-1.md`](cards/forward-se-1.md) (pushed as `27530c8` before any number). Code
`src/grimstrade/forward.py` (`hac_t`, `lag`, `critical`, `t_sf`), tests `tests/test_forward.py`,
check script [`forwardse1.py`](forwardse1.py), tables
[`results/forward-se-1.md`](results/forward-se-1.md) (30 s, numpy, deterministic). Inputs: the
committed weekly returns store through `evalue1.py`'s path generators, train only. No backtest,
no held-out year, no live record, no ledger or paper-trail change.

## Answer (one screen)

- **Built: the verdict's standard error now allows for a year of serial dependence.** Bartlett
  (Newey-West) long-run variance, lags L = one year of observations (51 for weekly bars), at
  most n / 4; p from a Student-t approximation to the fixed-b distribution (Kiefer and
  Vogelsang 2005, bandwidth M = L + 1, b = M / n). With no lags it is the ordinary t-test; on
  iid data it gives the old p within 0.01 (tested). `sharpe` uses the same statistic (Lo 2002
  at the null). `min_sample` uses the new test's critical value and a plan field `lrv`
  (long-run variance ratio, measured on the train record at freeze). Fixed before any live
  verdict: the registry holds no frozen line.
- **Card kill condition met (3 cells > 0.040); adopted anyway by the night lead as an
  improvement over the old iid test (every resampled cell falls, iid controls keep their
  level); a deviation from the card, reversible by the owner.** Null rejection at nominal 2.5%
  on 52-week block-resampled store paths (10,000 per cell):

  | Null | Old, 10 y | New, 10 y | Old, 100 y | New, 100 y |
  |---|---:|---:|---:|---:|
  | vs `tsmom12`, rho 0.77 (`mean`) | 0.064 | 0.058 | 0.047 | 0.036 |
  | vs `tsmom12`, rho 0.88 (`mean`) | 0.062 | 0.050 | 0.046 | 0.035 |
  | vs `tsmom12`, rho 0.95 (`mean`) | 0.061 | 0.043 | 0.046 | 0.031 |
  | `tsmom12` vs 0 (`sharpe`) | 0.081 | 0.010 | 0.083 | 0.023 |
  | Gaussian iid, difference | 0.026 | 0.024 | 0.024 | 0.024 |
  | Gaussian iid, vs 0 | 0.026 | 0.027 | 0.026 | 0.027 |

  The pass bar asked for at most 0.035 everywhere and the kill bar fired above 0.040: the three
  10-year difference cells (0.0584, 0.0498, 0.0430) are above 0.040, and one 100-year cell
  (0.0356) misses the pass bar. A 10-year verdict on a book against `tsmom12` is therefore
  read as about a 5%-level test, not 2.5%. Against zero the one-sided upper test is now very
  conservative (0.9% above +cv against 11.7% below -cv at 10 years).
- **What is left is skew, not the standard error** (diagnostic added after the result): the
  upper and lower tails of the new statistic are lopsided (difference at rho 0.88, 10 years:
  5.2% above, 2.0% below, mean 3.6%; at 100 years 3.0% / 2.3%). A 10-year read averages about
  10 yearly sums, whose skewness is median -0.3 for the differences (p10 -2.1) and +1.8 for
  `tsmom12`; a one-sided t on 10 skewed values is lopsided whatever its standard error. The
  card's limit also holds: 52-week blocks put all simulated dependence within a year, which a
  one-year window covers by construction, so this checks the implementation, not that real
  dependence stops at a year (104-week blocks: 6.5% at 10 years, 3.3% at 100).
- **Power at the new min_sample:** own Sharpe 1.0 vs 0, Gaussian, lrv 1: 504 weeks, power
  0.83 (target 0.80). On resampled `tsmom12` with lrv 1 the same n gives 0.65; with its
  measured lrv 2.14, 975 weeks (18.8 years) give 0.95. So `lrv` must be measured at each
  freeze, not left at 1.

## Recommendation (for the lead)

1. Adopted by the night lead as an improvement, not a fix (card kill condition met, 3 cells
   > 0.040; a deviation from the card, reversible by the owner): every resampled cell's level
   falls (difference books at 10 years from 6.1-6.4% to 4.3-5.8%, books against zero from 8%
   to at most 2.3%), iid controls keep their level, and nothing live changes (the daily runner
   does not import `grimstrade.forward`; the scoreboard renders byte-identical). Read a
   10-year verdict of a book against `tsmom12` as about a 5%-level test, not 2.5%.
2. Measure `lrv` on the train record at every freeze (Bartlett, same lags); with lrv 1 a
   trend-like book is under-powered (0.65 instead of 0.80), and against zero the upper test is
   very conservative (0.9% at 10 years).
3. If the 2.5% level must hold at 10 years: a longer read (the 100-year level is 3.1-3.6%,
   and the skew term shrinks as 1 / sqrt(years)) or a stricter per-rule alpha. A skew
   correction fitted on the train record's yearly sums (about 30 of them, skew SE about 0.45)
   would pass this simulation by construction and was not tried.

Correction made after review: the first run used b = L / n; Kiefer and Vogelsang's bandwidth
is M = L + 1, so the code now uses b = (L + 1) / n. The numbers above are from the corrected
run (they moved by at most 0.0005 in rejection rate; `carry-3-band@1` 750 -> 752 weeks).

Timestamps: the card header time 01:20 UTC is wrong; commit `27530c8` at 2026-11-25
01:00:42Z is authoritative (it precedes every result commit).

## Daily dry run

See the PR body: `run_daily --root <copy of paper-trail>` and `--intraday <dir>` exit 0; the
scoreboard, backtest and weekly reports the branch writes equal those that `origin/main`'s code
renders from the same copy, byte for byte.

Tries rows: one `note` row (`forward-se`), no selectable try.
