# Card gate-null-2: is the shifted-calendar placebo null mis-sized for persistent doses?

Lane `gate-null-2` (night run 2026-11-25/26, UTC), branch `gate-null-2-b` (the name
`gate-null-2` was taken by the 2026-11-19 method-change lane). Methodology study: no strategy,
no backtest, no new gate, no new verdict. **Card written and pushed before any number was
computed** (no simulation run, no gate re-scored).

## Question

The kill-only gates (`gate-null.md` step 4) pass when the true dose slope t has the predicted
sign, |t| >= 2, and ranks among the 2 most extreme of 41 (true + 40 shifted-calendar
placebos). Both passes so far died in their replications: W32 `drought-inflation` (R32,
`parked-gates-1.md`) and W36 `grid-load-premium` (open PR #202, not on main; a 40-member
phase-surrogate family, shown there, ranked W36's t 3rd of 41). wide-21 found the shifted family
off-centre for a cyclic dose (W35), and W33's earlier-only family was off-centre (all 40 placebo
t positive).

Hypothesis (from the design, before any number): the 40 shifted calendars of a persistent dose
are not 40 independent nulls. Neighbouring shifts (k and k + 2 months) are near-copies of each
other when the dose's autocorrelation is close to 1, so the family behaves like a few draws, and
the true t outranks "all 40" more often than 2 / 41. If so the shifted rank is too liberal for
persistent doses, and a family whose members are (nearly) independent copies of the dose with
the same persistence (phase-randomised or IAAFT surrogates; a block bootstrap) should be closer
to nominal.

Asked: (1) the false-pass rate of each placebo family under a known null, by dose persistence;
(2) the power of each family and of a "both" rule at plausible effect sizes; (3) a descriptive
re-score of every gate on main whose code is in `research/lib/`, with no new verdicts; (4) a
recommendation, with the dose-persistence threshold if any.

## Counts quoted (unchanged by this lane)

From `research/gate-null.md` (count after W35): **103 mechanisms, 29 tested by a strategy, 30
gates, family bar p < 0.10 / 103 = 0.00097**; one kill-only pass (W32), killed by R32. From
`research/register/BAR.md` (rows through 2026-11-25 01:16): 4,126 distinct tries, N for a new
pick 1,116, the bar's N_eff 506, Bonferroni p <= 9.9e-05. This lane adds `note` rows only
(methodology / descriptive, not selectable, not counted as tries of any idea or as gates).

## Part 1: size under a known null (synthetic)

**Dose.** Gaussian AR(1), x_t = phi x_{t-1} + e_t, phi in {0, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99},
simulated with burn-in and with 103 months of history before and 89 after the sample, so every
shifted placebo has all T rows (the gates truncate instead; noted as a limit). Shown, not in the
threshold: a cyclic dose (sine of period 132 months with random phase, plus AR(1) phi 0.9 noise
of equal variance; the W35 case) and a skewed dose (exp of the phi = 0.95 AR(1), standardised).

**Returns** (independent of the dose by construction, so the null is true):

- R1 `garch-t`: r_t = 0.05 r_{t-1} + s_t z_t, z_t Student-t with 5 df scaled to unit variance,
  GARCH(1, 1) with alpha 0.10, beta 0.85 (monthly).
- R2 `real`: French `Mkt-RF` monthly 1926-07..2025-10 (cached `F-F_Research_Data_Factors_CSV.zip`
  of 2026-11-12), rotated by a uniform random circular offset per simulation, first T months.
  Real fat tails, vol clustering and serial dependence; the synthetic dose knows nothing of it.
- R3 `slow-premium`: R1 plus a slow expected return mu_t, AR(1) phi 0.98, scaled so mu carries
  2% of the return variance (the spurious-regression case: a persistent dose can line up with a
  persistent premium in one sample; Ferson, Sarkissian and Simin 2003 `[memory]`).

**Sample sizes.** T = 300 and T = 600 months (the gates on main use 276-729).

**Statistic.** OLS of r_{t+1} on x_t with an intercept, Newey-West t with Bartlett weights and
3 lags (the monthly gates' usual choice), the same function for the true dose and every placebo
(vectorised; a unit test checks it equals `wide11_events.ols_dk` to 1e-8). Shown: 12 lags; a
3-month overlapping outcome (sum of r_{t+1..t+3}, NW 3, the W32 shape) at T = 300.

**Placebo families (40 members each, same statistic):**

- F1 `shift-earlier`: x_{t-k}, k = 25, 27, ..., 103 (earlier doses only, W33/W34/W36).
- F1b `shift-both`: x_{t-k}, k = +-13, 17, ..., 89 (both ways, W29/W32).
- F2 `phase`: Fourier phase-randomised surrogates of the dose's T sample values (same amplitude
  spectrum, independent uniform phases, Hermitian; Theiler et al. 1992 `[memory]`).
- F3 `iaaft`: iterated amplitude-adjusted Fourier transform surrogates (Schreiber and Schmitz
  1996 `[memory]`): same values as the dose, spectrum matched iteratively (up to 100
  iterations or no change in rank order).
- F4 `block`: circular block bootstrap of the dose's sample values, block length 24 months.
- F5 `rotation`: the dose's sample values rotated circularly by 40 distinct random offsets, each
  at least 24 months from 0 and from T.

**Pass rules scored** (predicted sign +, by symmetry): P(rank = 1 of 41), P(rank <= 2), the gate
rule P(t >= 2 and rank <= 2), and P(t >= 2) alone. Nominal: 1/41 = 2.4%, 2/41 = 4.9%. "Both":
the gate rule in F1 and in F2 (and F1 with F3), at once. 2,000 simulations per cell (binomial SE
0.34 points at 2.4%, 0.48 at 4.9%); seeds fixed per cell. Diagnostics: mean correlation of the
true t with the placebo t and among placebo t, across simulations.

## Part 2: power (synthetic)

Plant r_{t+1} = c x_t / sd(x) + noise in R1 and R2 (noise = the null return series), with c set
so the dose explains a share R^2 of the next month's return variance: R^2 in {0.25%, 0.5%, 1%,
2%} (monthly macro predictors report about 0.5-1% in sample; W36's t -2.31 on 619 months is
about 0.9%). phi in {0, 0.5, 0.9, 0.95, 0.98, 0.99}, T = 300 and 600, 1,000 simulations per
cell. Report the gate rule's pass rate per family and for "both". Power is read next to size: a
family that is oversized buys its power with false passes.

## Part 3: descriptive re-score of the gates on main (no new verdicts)

Gates whose code and cached inputs are on main and on this machine: W20, W21 (`wide10*`), W22
(`wide11*`), W23, W24 (`wide12*`), W25, W26 (`wide13*`), W27, W28 (`wide15*`), W29, W30
(`wide17*`), W31 (`wide20*`), W32, R32, W33 (`parkedgates1*`), W34 (`panicwords1*`), W35
(`wide21*`), weather-1 (`weather1*`), weather-2 (`weather2*`). For each: rebuild the true t with
the gate's own fit (check: within 0.02 of the stored value, else reported as not reproduced and
not re-scored), then rank it among 40 F2 and 40 F3 surrogates of the gate's dose (the dose's full
cached series in time order, surrogate built once per family, seed 2; the true fit's code path
with the surrogate dose in place of the dose, k = 0). Multi-regressor gates replace only the dose
(W33: s, the interaction recomputed from the surrogate s). Reported per gate: true t, stored
rank, F2 and F3 rank, null width (SD, share |t| >= 2, 5/50/95%), lag-1 autocorrelation and N_eff
of the dose, and whether the verdict would change under F2 alone, F3 alone, or "both". Not
re-scored, listed with the reason: W1-W19 and ann-1 (code not on main), `seasonal-20y` (survey-7:
the "dose" is a cross-section of 20-year same-month averages, no single dose series), any gate
whose cached input is missing (no new download for the re-score). W36 (#202) is left out.

## Decision rule for the recommendation (fixed now)

- **Mis-sized**: a family is called mis-sized at a phi if its P(rank <= 2) under the null is
  above 1.5 x 2/41 = 7.3% or its gate-rule false-pass rate is above 4.9%, in R1 or R2, at
  T = 300 or 600. The **persistence threshold** is the smallest phi at which F1 is mis-sized
  (and its N_eff = T (1 - phi) / (1 + phi) at T = 300 and 600).
- **Fixes it**: a second family fixes it if its P(rank <= 2) stays within 3.4-6.4% (nominal +-
  3 SE) for all phi in R1 and R2, and its gate-rule false-pass rate is at most 4.9%.
- **Recommendation**: among {F1 only; F1 and the fixing family ("both"); the fixing family
  alone} for doses above the threshold, the rule with false-pass rate at most 4.9% and the
  highest power at R^2 1%, T = 600; if "both" and the second family alone are within 5 points of
  power, recommend "both" (it never passes more than either). If no family fixes it: recommend
  no new rule, and say so.
- R3 is reported and discussed but does not set the threshold (its slow premium is an assumed
  world, not measured).

## Expected cost and risk

numpy only, one process, under 1 GB. Part 1 is about 2 x 3 x 9 x 2,000 cells x 240 fits, Part 2
about half that, vectorised. No download (French file is cached; re-score reads existing
caches with `python -I`). Code: `research/lib/gatenull2.py` (pure functions, tested in
`tests/test_gatenull2.py`), `research/lib/gatenull2_sim.py`, `research/lib/gatenull2_rescore.py`;
numbers in `research/results/gate-null-2.md`; write-up `research/gate-null-2.md`.

## My guess (before any number)

F1 is roughly nominal up to phi 0.9 and oversized from about 0.95 (rank <= 2 near 8-12% at
0.99), worse with overlapping outcomes; F2 and F3 near nominal for the Gaussian dose but F2
slightly oversized for the skewed one; F4 (24-month blocks) oversized at phi >= 0.98 because
the blocks are shorter than the dose's memory; F5 near nominal. The t >= 2 condition hides much
of F1's excess in the gate rule. "Both" costs 10-25% of power. W32 keeps rank 1-3 under F2/F3.
