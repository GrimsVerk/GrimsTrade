# forward-se-1: a dependence-robust standard error for the forward registry's verdict (card)

Lane `forward-se-1`, written 2026-11-25 01:20 UTC **before the null check below was run**.
Branch `forward-se-1` from `origin/main` (`d9f369f`, after #184). Engineering with one
simulation check. Inputs: the committed weekly returns store (`research/register/returns/`,
train only, nothing after 2025-11-09), through `research/evalue1.py`'s path generators. No
backtest, no price bar, no held-out year, no live record, no ledger or paper-trail change.

What was seen before this card: evalue-forward-1 (#184): on 52-week block-resampled null paths
the registry's read-once iid t-test rejects 6.1-6.6% at 10 years and 4.2-4.8% at 100 years
(nominal 2.5%), and 8.0% / 8.6% for a book against zero; with 1-week blocks it keeps its level
(2.6-2.8%), so the cause is serial dependence. One calibration was run before this card, on
iid normal synthetic data only (no store data): the Student-t approximation to the fixed-b
distribution named below gives critical values within 1% of the simulated ones and of Kiefer
and Vogelsang's (2005) polynomial for b <= 0.1, and is conservative at b = 0.25 (rejects 2.2%
at nominal 2.5%).

## The rule (fixed now, before any live verdict exists; the registry holds no frozen line)

For the `mean` and `sharpe` metrics (`win_rate` keeps its exact sign test):

- **Long-run variance:** Bartlett (Newey and West 1987) on the values x_1..x_n of the verdict
  window: w = (n / (n - 1)) (g_0 + 2 sum_{j=1..L} (1 - j / (L + 1)) g_j), g_j = (1/n)
  sum_t (x_t - mean)(x_{t-j} - mean). With L = 0 this is the sample variance, so the test is
  the ordinary t-test.
- **Lag rule:** L = min(q - 1, floor(n / 4)), q = max(1, round(per_year)): autocovariances up
  to one year of observations (51 lags for weekly bars, 7 for 8 FOMC meetings a year). Why a
  year: the store's dependence shows at the 52-week horizon (variance ratio median 1.34, p90
  2.73; `tsmom12` 3.3), Bartlett with L + 1 = q is the q-period variance-ratio estimator, and a
  data-driven bandwidth (Andrews 1991, Newey and West 1994) would pick about 5 lags at n = 520
  and miss most of it. The n / 4 cap keeps b = L / n <= 0.25, where the reference distribution
  below is calibrated.
- **Statistic and p-value:** T = mean / sqrt(w / n). One-sided p = P(t_nu > T sqrt(c)), with
  b = L / n, c = 1 - b + b^2 / 3 (the fixed-b mean of the Bartlett estimator, Kiefer and
  Vogelsang 2005) and nu = 1.5 / b (matching the Bartlett estimator's variance 4b/3; Andrews
  1991); nu = n - 1 and c = 1 when L = 0.
- **Sharpe path:** the test of "Sharpe > 0" uses the same T (Lo 2002's dependence-robust
  variance of the Sharpe ratio evaluated at the null Sharpe 0 reduces to the HAC variance of the
  mean over sigma^2). The estimate shown stays the annualised sample Sharpe.
- **min_sample:** smallest n with n >= lrv * base(cv(n)), where cv(n) is the critical value of
  the test above at n, base the old formula with z(1 - alpha) replaced by cv(n) (`sharpe`:
  1 + k ((cv + z_power) / sr)^2, `mean`: ((cv + z_power) sd / effect)^2), and `lrv` a new plan
  field: the long-run variance ratio assumed true (the train record's Bartlett one-year LRV
  over its variance, at least 1; default 1 when not measured).
- **Old registrations:** none is frozen. If one were, it keeps its recorded alpha and
  min_sample; only the SE changes.

## The null check (secondary to the tests; the pass bar for adopting the rule)

`research/forwardse1.py` (new; imports `evalue1.py`'s `donors`, `diff_paths`, `own_paths`,
same seed 20261125 and cells): 10,000 null paths per cell, read once at 10 years (n = 520) and
100 years (n = 5200), alpha 0.025. Cells: resampled (52-week blocks) difference vs `tsmom12` at
rho 0.77 / 0.88 / 0.95 (`mean` path), resampled `tsmom12` against zero (`sharpe` path),
Gaussian iid controls of both. Before = the old statistics (iid t with normal p; PSR), after =
the rule above, on the same paths.

- **Pass:** every resampled cell rejects at most 0.035 (Clopper-Pearson 97.5% upper bound
  under 0.040 allowed), and every Gaussian cell 0.015-0.035 (the rule must not become useless
  on iid data).
- **Kill:** any resampled cell above 0.040, or any Gaussian cell outside 0.010-0.040: the rule
  is not adopted as written; reported as is.
- Reported, not part of the bar: (a) the same with 104-week blocks (dependence beyond a year,
  which the one-year lag rule does not cover by design); (b) simulated power at the new
  min_sample for own Sharpe 1.0 against zero (Gaussian, lrv 1; resampled, lrv = `tsmom12`'s
  measured one-year ratio), target 0.80.

Honest limit stated now: 52-week blocks put all simulated dependence inside one year, which is
exactly what a one-year Bartlett window covers, so the check is a consistency check of the
implementation and its small-sample correction, not evidence that real dependence stops at a
year.
