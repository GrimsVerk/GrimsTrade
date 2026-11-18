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

## Results (2026-11-19)

Generated files: `research/register/moments.jsonl`, `research/register/trials.json`; BAR.md
regenerated at 3,023 tries, N 1,027 for a new pick (selectable 1,016 + live 11).

- Backfilled: 1,209 register rows (410 of 1,016 selectable; the rest robustness and control
  rows) and the 11 live strategies. The harness re-simulation reproduced 36 of the 39
  baselines exactly (87 rows, logged Sharpe to 0.01); the 3 misses are `equal-weight` on
  N225, FTSE and GDAXI alone (their logged rows were run on an earlier start date).
- Shape of weekly returns (421 selectable or live series): skew median -0.10 (10th percentile
  -1.06), excess kurtosis median 9.0 (90th percentile 17.4). `tsmom12` itself: 1,657 weeks,
  skew +0.05, excess kurtosis 10.8.
- Correlation, 294 series covering every week 2012-01-06..2025-11-07 (722 weeks): average
  pairwise rho 0.58 (median 0.68); 1994-2025 check (213 series): 0.72. One series per family
  (55 families, not on the card): 0.70. The sample over-weights one family (a trend-tuning
  surface, 97 of 294), which lowers the average: the 0.58 is the cautious figure.
- ONC: 2 clusters (crypto-heavy and the rest; silhouette quality 6.5 at k = 2 against 2.5 at
  k = 3), the same in the 1994-2025 window. The implementation finds 6, 10 and 20 planted
  blocks exactly (`onc_check_planted_found`). Eigenvalue participation ratio 2.3: one market
  factor carries most of the variance of every long-only rule.
- Deviation from the card: the per-record-length table uses the larger of the clusters'
  Sharpe variance (0.038, from only two clusters, one degree of freedom) and the selectable
  variants' (0.098), not the clusters' alone.

### How the bar for a new pick changed, and why

Before (register-1): N 1,012, with the correlation between trials assumed, the bar quoted as a
range: +0.27 (rho 0.9 assumed, close rule) to +0.59 (independent, far rule) over `tsmom12`.

Now: the measured average correlation is 0.58, not 0.9, so A.3 counts N 1,027 as 433
independent trials (not 102). By the card's rule (the more cautious of A.3 and ONC scaled)
**the bar is N = 433: z >= 4.65, an edge over `tsmom12` of +0.30 (close rule) to +0.56 (far
rule) on the primary 32-year test, Bonferroni p <= 1.2e-4.** That is near the old independent
end: the generous "rho 0.9" row was wrong by a factor of four in N, though only by 0.03 in
the close-rule edge, because E[max] grows slowly with N.

ONC disagrees sharply (2 clusters; scaled to N, 7 trials, bar +0.20 / +0.36). It measures
how many different bets the project has made (two: with or without crypto), not how many
chances it took to get lucky inside one bet; with every rule long-only on the same markets,
A.3 is the honest count of the latter. The bar keeps the cautious one.

New: the bar depends on record length far more than on the shape of the returns. A rule
judged on 10 years needs +0.54 (close) to +1.00 (far) over `tsmom12`, on 5 years +0.76 to
+1.41; against zero a 10-year record needs an annual Sharpe of 1.48 (normal) to 1.58 (fat
tail), a 32-year one 1.23 to 1.28. Fat tails add 0.02-0.25 Sharpe; halving the record adds
far more.

Caveats: the sample is the 40% of selectable rows whose returns could be rebuilt (saved
curves exist only on one machine; regeneration elsewhere needs those caches or a fresh run of
each lane's scripts). Live strategies' weeks count the whole train period, including years
before an asset existed (held as cash). Tries rows added by this lane: none (only
re-scoring of configurations already counted, `log=False`).
