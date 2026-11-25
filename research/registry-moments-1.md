# registry-moments-1: noisy lrv and unmeasured moments in the forward registry

Lane `registry-moments-1`, 2026-11-25 (UTC). Engineering, follow-up to #200 (`registry-lrv-1`).
Synthetic records only: no store data, no backtest, no held-out year read. Code
`src/grimstrade/forward.py` (`lrv_upper`, `LRV_LEVEL`, `measure_lrv`, `k_factor`,
`measure_moments`, `check_moments`), tests `tests/test_forward.py`, sizing script
[`registrymoments1.py`](registrymoments1.py), tables
[`results/registry-moments-1.md`](results/registry-moments-1.md) (about 10 s, deterministic).
Decision: `docs/DECISIONS.md`, 2026-11-25; rules: `docs/forward-registry.md`.

## Answer

- **lrv: size with an upper 0.65 value of the measurement, not the estimate.** At five years of
  weekly train values the one-year Bartlett estimate of a true lrv 3 has sd about 1.4 and falls
  below the truth in about 60% of records; a line sized with it has an expected power of
  0.70-0.77 (instead of 0.80) for every dependent AR(1) record tried. The new rule,
  max(1, point nu / chi2_nu(0.35)) with the verdict's fixed-b nu = 1.5 / b, multiplies the
  estimate by 1.35 at five years and 1.21 at ten. Smallest level on a 0.05 grid reaching 0.80
  in all ten weekly sizing cells:

  | Rule | Lowest expected power (weekly AR(1), phi 0-0.6, 5 and 10 y) | No-dependence line: mean sample / needed (5 y / 10 y) |
  |---|---:|---:|
  | point estimate (#200) | 0.703 | 1.20 / 1.14 |
  | upper 0.60 | 0.785 | - |
  | **upper 0.65 (adopted)** | **0.809** | **1.45 / 1.28** |
  | upper 0.70 | 0.833 | - |

  The power approximation used for sizing, Phi(sqrt(U / L) (cv + z) - cv), matches a Monte
  Carlo of the verdict's own HAC test (0.800 vs 0.798 at U = L = 3; 0.496 vs 0.512 at U = 1.5).
- **Not fixed (reported only):** 8 events a year with phi 0.5 reach 0.77 (the 7-lag window
  misses part of it); dependence slower than a year (white noise plus an AR(1) phi 0.98 part,
  lrv 3) reaches only 0.57, because a one-year window cannot see it. For such rules the
  caller must set a larger `lrv` (allowed since #200). t(4) shocks change nothing (0.814).
- **Skew and kurtosis: measured on the train record, `sharpe` only, compared through k.** The
  plan's Mertens k at its own effect may not be below the measured pair's; `entry` takes the
  measured pair if it is, `freeze` refuses otherwise. On a crash-prone weekly record (skew -1,
  kurtosis 6.5) the true k is 1.08 / 1.13 / 1.27 at Sharpe 0.5 / 0.79 / 1.5, against the
  default's 1.00 / 1.01 / 1.02: the default under-sized such lines by 7-24%. The measured k has
  sd 0.02-0.10 and is below the truth in 56-60% of records, a few percent of the sample, so no
  upper value is applied to it.

## Choices and limits

- Criterion: expected power over the measurement noise per true lrv, at plan power 0.80. A
  stricter one (e.g. power >= 0.75 in 85% of records) needed about level 0.8 in an exploratory
  run (not in the results tables), with 1.5-1.8 times the needed sample for independent lines;
  not taken. Plans at power 0.90 are not checked.
- Upper value rather than shrinkage toward a prior: shrinkage lowers the high measurements,
  the direction that under-sizes dependent lines, and no prior for the next rule's lrv is
  known (store variance ratios 1 to 3.3).
- Random numbers: numpy PCG64 seeded from SeedSequence((20261125, cell...)), one stream per
  cell; the review of #200 found the old LCG with consecutive seeds biased. The new tests use
  the same generator; #200's own tests keep their LCG records (their asserts still hold).
- Backward compatibility: lines without `skew`, `kurtosis`, `lrv` or the measurements read and
  score as before; proposals in `candidates.jsonl` (no train values) are unchanged.
