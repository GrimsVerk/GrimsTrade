# register-2: measured record length, shape and trial correlation for the bar

Card written 2026-11-18, before any number below the "Results" heading was computed.
Base: register-1 (PR #79), whose `research/register/BAR.md` (2,904 tries, N 1,012 for a new
pick, Bonferroni p <= 5e-5) assumes one record length, normal returns and a guessed
correlation between trials (rho 0.9 or independent).

## Question

How many effectively independent trials has the project run, measured from the trials' own
return series instead of assumed, and what bar does a new pick face per record length once the
real skew and kurtosis of the returns are used?

## Data (train only, no held-out bar is loaded)

- Return series of tries already in the register, no new configuration (so no new try rows):
  1. Re-simulated with the research harness (`research/lib/harness.py`, `log=False`) at a
     pinned commit of a research branch: every baseline in `research/lib/baselines.py` (the
     plain twins on every test universe). A row counts as backfilled only if the re-simulated
     Sharpe equals its logged Sharpe to 0.01; otherwise it is reported as a mismatch.
  2. The live strategies (`grimstrade.strategies.LIVE`) through `grimstrade.gym` on the six
     assets, train period. They are not register rows; they get their own lines.
  3. Equity curves the harness already saved for logged tries (`research/data/runs/<idea>/
     <variant>.train.csv`, gitignored caches on the machine, listed in a gitignored local
     file). Matched to a register row only if idea, variant and period agree, the curve starts
     within 10 days of the row's From and its Sharpe (the harness's own formula) equals the
     logged one to 0.01. Ambiguous matches are dropped.
- Weekly returns: equity on each Friday (calendar days, equity carried over days without a
  bar), simple returns. T = number of weekly returns; skew and excess kurtosis are population
  moments of those weekly returns (`grimstrade.stats.moments`).

## Outputs (generated, never hand-edited)

- `research/register/moments.jsonl`: one line per backfilled register row (its register id)
  or live strategy: weeks, skew, excess kurtosis, weekly Sharpe, logged Sharpe, source.
- `research/register/trials.json`: the effective-trials estimate and its inputs.
- `BAR.md` gains a measured section: effective N, method, per-record-length bar table.

## Method for the effective number of trials (fixed now)

Correlations of weekly returns over one common window (every series that covers
2012-01-06..2025-11-07; the 1994-2025 window as a check). Three estimates:

1. A.3 of Bailey and Lopez de Prado (2014): N_eff = rho + (1 - rho) N with rho the measured
   average off-diagonal correlation.
2. ONC clustering (Lopez de Prado and Lewis, "Detection of false investment strategies using
   unsupervised learning methods", Quantitative Finance 19(9), 2019; checked against the SSRN
   version 3167017, sections 8.1-8.2): D = sqrt((1 - rho) / 2); k-means on the rows of D
   (Euclidean distance between rows = the paper's D-tilde); quality q = mean / std of the
   silhouette scores; best q over k = 2..k_max and several seeded initialisations; clusters
   with below-average quality re-clustered recursively when more than two of them, kept only
   if their average quality improves. K = number of clusters. Cluster return series by
   minimum-variance weights within the cluster; V[SR_k] is the variance of the clusters'
   annualised Sharpes (section 8.2).
3. Eigenvalues of the correlation matrix (participation ratio (sum l)^2 / sum l^2), as a
   cross-check only.

Seeds fixed; the result must be identical on a re-run.

Scaling to the register: the sample has M series, the register N = 1,012 selectable + live
tries. The ONC count is scaled as K * N / M (clusters found per series tried), which is the
cautious direction when the sample covers the families evenly.

## Decision rule (fixed now)

- BAR.md keeps the independent row (N = 1,012) as the upper bound and replaces the assumed
  rho rows with the measured ones (A.3 with measured rho; ONC K scaled; ONC K on the sample).
- The bar quoted for a new pick becomes the more cautious (larger N) of the two measured
  estimates, A.3 and ONC scaled, never above the raw count.
- The per-record-length table (5, 10, 20, 32 years) uses that N, the cluster Sharpe variance
  where available, and the median and a fat-tail (10th percentile skew, 90th percentile excess
  kurtosis) shape of the backfilled weekly returns.

## Results

(Not yet computed.)
