# gate-null-2: the shifted-calendar null is too liberal for persistent doses; t >= 2 hides it

Lane `gate-null-2` (night run 2026-11-25/26, UTC), branch `gate-null-2-b`. Methodology study:
no strategy, no backtest, no new gate, no new verdict. Card: `cards/gate-null-2.md` (pushed
before any number, commit `09d665d`). Numbers: `results/gate-null-2.md`. Code:
`lib/gatenull2.py` (pure functions, `tests/test_gatenull2.py`), `lib/gatenull2_sim.py`
(Parts 1-2), `lib/gatenull2_rescore_{a,b,c}.py` (Part 3), `lib/gatenull2_report.py`.

## Answer in four lines

1. **Yes, the rank part of the gate is mis-sized for persistent doses.** Under a true null, the
   true t ranks among the top 2 of 41 earlier-dose calendars (F1) in 7.5-8% of samples at
   dose autocorrelation phi 0.8-0.9, and in 13-19% at phi 0.98-0.99 (nominal 4.9%). Rank 1
   alone: 11-16% at phi 0.98-0.99 against 2.4%.
2. **The gate's t >= 2 condition hides almost all of it.** With realistic returns (GARCH-t or
   real French market months) the full gate rule (t >= 2 and rank <= 2) passes a null 0.9-3.1%
   of the time in every family (AR doses; the skewed dose up to 4.0%). Here the rank adds little to "t >= 2 with Newey-West 3". The
   shifted family's error matters when the t itself is inflated. That happens when returns carry
   a slow premium a persistent dose can line up with (R3): there F1's false passes reach
   5.4-5.5% at phi 0.98-0.99, T = 300.
3. **Phase-randomised surrogates (F2) are close to nominal everywhere:** P(rank <= 2) is
   4.0-6.0% over all AR doses, R1 and R2, both sample sizes, and 4.5-6.5% in R3. They also fix
   the cyclic dose (W35's problem: F1 14%, F2 5%). IAAFT (F3) is as good and better for a skewed
   dose (F2 4.9-7.2%, F3 4.5-5.7%). Block bootstrap with 24-month blocks is fine in R1/R2 but
   too liberal in R3. Random rotations are mildly liberal.
4. **"Both" (F1 and F2) costs 2-3 points of power at phi 0.9-0.95 and 5-8 points at 0.98-0.99**
   (R^2 1%, T = 600). It changes no verdict on main: W32 ranks 1 in all three families, and every
   other gate fails its own t.

**Recommendation (by the card's rule): adopt "both" for future gates whose dose has lag-1
autocorrelation >= 0.8 at the gate's own step.** A pass then needs t >= 2 with the predicted
sign and rank <= 2 of 41 in the shifted calendars and in 40 phase-randomised surrogates (IAAFT
when the dose is skewed or mostly zeros). Do not expect it to stop passes dying in replication:
W32 passes it, and two passes among about 32 gates is what chance gives at this per-gate size.

## Part 1: size under a known null

Synthetic Gaussian AR(1) doses, phi from 0 to 0.99, plus a cyclic dose and a skewed one, all
independent of the returns. Three return models: R1 `garch-t` (AR 0.05, GARCH(1,1), t5 shocks),
R2 `real` (French Mkt-RF 1926-07..2025-10, randomly rotated) and R3 `slow-premium` (R1 plus an
AR(0.98) expected return carrying 2% of the variance). The statistic is OLS of the next month's
return on x_t, Newey-West t with 3 lags. T = 300 and 600 months, 2,000 simulations per cell,
40 placebos per family.

P(rank <= 2 of 41) under the null, %, nominal 4.9 (R1 / R2; full tables in the results file):

| Dose phi | T | F1 shift-earlier | F1b shift-both | F2 phase | F3 IAAFT | F4 block 24 | F5 rotation |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 600 | 4.6 / 5.3 | 4.7 / 5.0 | 4.0 / 5.0 | 4.9 / 5.1 | 4.4 / 4.7 | 3.6 / 4.4 |
| 0.8 | 600 | 7.5 / 5.4 | 5.8 / 5.2 | 5.1 / 4.5 | 5.0 / 4.8 | 5.3 / 4.5 | 5.3 / 5.3 |
| 0.9 | 600 | 10.7 / 8.3 | 6.7 / 6.6 | 6.0 / 6.0 | 5.7 / 5.3 | 5.5 / 5.9 | 6.3 / 5.7 |
| 0.95 | 600 | 12.8 / 10.4 | 7.1 / 6.5 | 5.2 / 4.9 | 4.9 / 5.2 | 5.0 / 5.0 | 6.6 / 5.9 |
| 0.98 | 600 | 16.7 / 13.4 | 6.8 / 5.9 | 4.3 / 4.2 | 4.7 / 4.4 | 4.9 / 3.4 | 6.8 / 5.2 |
| 0.99 | 600 | 18.9 / 16.2 | 6.2 / 5.9 | 4.9 / 5.1 | 4.7 / 5.0 | 5.3 / 3.1 | 6.4 / 6.7 |
| cycle (132 m) | 600 | 13.2 / 13.1 | 8.2 / 9.2 | 4.7 / 4.7 | 4.5 / 4.2 | 4.7 / 4.0 | 5.8 / 4.8 |
| skewed, phi 0.95 | 600 | 10.6 / 8.8 | 5.7 / 7.0 | 4.9 / 7.2 | 4.5 / 5.7 | 4.5 / 5.0 | 5.0 / 5.7 |

T = 300 looks the same: F1 is at 9.2 / 7.5 at phi 0.9 and 15.4 / 14.9 at phi 0.99. Newey-West
with 12 lags and a 3-month overlapping outcome (the W32 shape) change nothing material.

**Why F1 fails.** Neighbouring shifts (k and k + 2 months) of a persistent dose are near-copies.
Across simulations the mean correlation among the 40 F1 placebo t is +0.17 at phi 0.9, +0.28
at 0.95, +0.51 at 0.98 and +0.64 at 0.99. So the 40 calendars act like a handful of draws, and
"higher than all of them" is much likelier than 1/41. Surrogate placebos are uncorrelated with
each other and with the true t (|r| <= 0.01). F1b (both ways, 4-month spacing, spread over
-89..+89) is less affected but still 6-7% from phi 0.9. For the cycle it is 8-9% (true-placebo
correlation -0.18: W35's anti-phase).

**The gate rule (t >= 2 and rank <= 2), false passes, %:**

- R1 and R2: 0.9-3.1 in every family, every AR phi and both T (skewed dose: up to 4.0, F2). P(t >= 2) alone is 1.4-3.4%
  (one-sided nominal 2.3%), so the t condition decides almost every pass and the rank rarely
  removes one.
- R3 (slow premium): P(t >= 2) rises to 5-8% at phi >= 0.95, the spurious-regression case.
  F1's gate rule passes 5.4-5.5% at phi 0.98-0.99 (T = 300) and 4.8-5.1% at T = 600, F2's
  3.6-4.4%, F3's 3.1-4.0%, both F1+F2 2.8-3.4%. Here the surrogates widen with the true t (they
  share the dose's low frequencies), and the shifted calendars only half do.

## Part 2: power

The effect is planted in R1 and R2 so the dose explains R^2 of next month's variance. At R^2 1%
(about W36's size) and T = 600, the gate-rule pass rate, %, is (R1 / R2):

| Dose phi | t >= 2 alone | F1 | F2 | F3 | both F1+F2 | both F1+F3 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 69.9 / 67.1 | 68.0 / 65.1 | 66.7 / 65.2 | 67.5 / 65.1 | 65.2 / 63.4 | 66.0 / 63.3 |
| 0.9 | 66.9 / 66.0 | 63.2 / 62.9 | 63.9 / 61.9 | 63.3 / 62.4 | 61.0 / 59.5 | 60.5 / 60.0 |
| 0.95 | 65.4 / 65.5 | 60.5 / 61.4 | 59.9 / 60.5 | 59.1 / 60.6 | 56.4 / 57.4 | 55.6 / 57.2 |
| 0.98 | 67.2 / 65.2 | 58.3 / 56.5 | 57.8 / 56.8 | 58.0 / 57.4 | 52.6 / 50.5 | 52.5 / 51.2 |
| 0.99 | 66.3 / 66.1 | 53.2 / 52.8 | 52.8 / 55.3 | 53.0 / 55.1 | 45.6 / 47.5 | 45.2 / 46.7 |

- F1 and F2 have the same power. Both lose some at high phi, because a planted persistent effect
  also lifts the near shifts (F1) and the persistent surrogates (F2).
- "Both" costs 2-3 points up to phi 0.95 and 5-8 points at 0.98-0.99.
- F1b (both ways) loses the most at high phi: 39% at phi 0.99, because its near shifts (k = +-13)
  carry the effect.
- Power at R^2 0.25% is 8-26% in every family, so a gate of this shape cannot see a
  post-publication-sized monthly effect in 300-600 months (as `gate-power.md` found).

## Decision rule applied (fixed in the card)

- **Mis-sized** (P(rank <= 2) > 7.3% or gate false pass > 4.9%, R1 or R2, either T):
  - F1 from **phi = 0.8**: 7.5% at R1, T = 600. This is borderline (0.3 SE above the line, within noise), and
    every cell is above the line from phi 0.9.
  - That threshold gives N_eff = T (1 - phi) / (1 + phi) = 33 at T = 300 and 67 at T = 600.
  - F1b is not mis-sized on the AR doses: its maximum is 7.3%, at the line. It is mis-sized on the
    cycle (8-9.5%, shown).
- **Fixes it** (P(rank <= 2) within 3.4-6.4% for all AR doses, R1/R2, both T; false pass <= 4.9%):
  - F2 phase: yes, range 4.0-6.0%.
  - F3 IAAFT: just misses, range 4.2-6.7%. The 6.7% is the phi = 0 cell of R1 at T = 300, where
    F1 and F2 are also high (5.8% and 5.3%) on the same simulated returns, so it is noise in a
    shared draw rather than a fault of IAAFT. By the rule as written, F2 is the fixing family.
  - F4 block bootstrap: no, 3.1-5.9%, too strict at phi 0.98-0.99 in R2, and 6.5-6.6% false
    passes in R3.
  - F5 rotation: no, up to 8.7%.
- **Choice**, for phi >= 0.8, R^2 1%, T = 600, averaged over phi 0.9-0.99 and R1/R2:
  - Every option has gate false passes <= 4.9% in R1/R2.
  - Power: F1 alone 58.6%, F2 alone 58.6%, both 53.8%.
  - "Both" is within 5 points of F2 alone (4.8), so the card's rule says **"both"**. The margin
    is thin: at phi 0.98-0.99 alone the cost is 5-8 points.

## Part 3: re-score of the gates on main (descriptive, no new verdict)

All 19 gates with code on main and cached inputs reproduced their stored true t (to the stored two
decimals) and their stored rank exactly. Each was then ranked among 40 phase and 40 IAAFT surrogates of
its own dose, through its own fit:

| Gate | t | Shift rank | Phase / IAAFT rank | Dose acf1 | Note |
|---|---:|---:|---:|---:|---|
| W32 `drought-inflation` | -3.71 | 1 | 1 / 1 | 0.94 | the only pass; **stays a pass under "both"** (killed by R32 regardless) |
| R32 | -0.19 | 21 | 26 / 22 | 0.94 | fails its t |
| W33 `margin-susceptibles` | +0.05 | 41 | 19 / 20 | 0.86 (quarterly) | the off-centre shifted null (median +1.70, all 40 positive) is centred under surrogates (+0.02 / -0.08) |
| W35 `solar-max-recession` | -0.87 | 3 | 9 / 8 | 0.998 | the anti-phase shifted null (median +1.25) is centred (-0.14 / -0.09), as wide-21 asked |
| W29 `temperature-premium` | +1.63 | 9 | 7 / 6 | 0.99 | fails its t |
| W22 `hedging-pressure` | +0.49 | 14 | 19 / 14 | 0.95 | surrogate null wider (SD 1.45 vs 1.13) |
| W28 `refund-runoff` | +1.44 | 7 | 4 / 5 | 0.60 | shifted null was the widest (SD 1.92); surrogates 1.10-1.13 |
| W30 `outbreak-premium` | +1.68 | 9 | 4 / 5 | 0.35 | shifted SD 1.64, surrogates 1.20-1.27 |
| W21 `stablecoin` | +1.06 | 17 | 2 / 10 | 0.31 | phase rank 2, fails its t |
| W20, W23-W27, W31, W34, weather-1, weather-2 | \|t\| <= 1.20 or wrong sign | 10-37 | 9-40 | 0.14-0.80 | nothing near a pass |

**Verdicts that would change: none**, under F2 alone, F3 alone or "both". Every gate except W32
fails its own t condition (wrong sign or |t| < 2), which no placebo family can change. W32 ranks
1 of 41 in all three families. Not re-scored: W1-W19 and ann-1 (code not on main),
`seasonal-20y` (no single dose series). W36 (#202, unmerged) is left out. Its own write-up
reports phase rank 3, so W36 would have failed "both". That is one of the two passes so far.

## What this does and does not explain

- The two passes (W32, W36) do not need a mis-sized rank to explain them. In R1/R2 the gate
  rule's false-pass rate is about 2-3% per gate in every family. Over about 32 gates the
  chance of two or more false passes is 13-25% (Poisson, lambda 0.6-1.0). Replication, which the
  procedure already requires, is the guard that worked twice.
- The shifted rank matters more as the t condition weakens: a slow premium in returns (R3),
  overlapping outcomes, or any future relaxation of t >= 2. The rank-only error (up to 19%)
  is large, so the rank must never be read alone as "p = rank / 41" for a persistent dose.
- Cycles and off-centre families (W33, W35) are where F1 is plainly wrong, and surrogates centre
  them.

## Limits

- The simulated dose is a single regressor, Gaussian AR(1) (plus one cycle and one skewed
  shape), with no controls.
- Placebo rows are complete: the gates truncate instead, which adds noise to F1 only.
- Newey-West 3 (12 shown). Monthly step only; weekly gates use a 4-week shift spacing, so the
  threshold carries over as "acf at the shift spacing >= about 0.64" `[inferred]`, not tested.
- Surrogates assume a stationary linear dose. They break any dose-on-past-price feedback, which
  is the right null for "dose independent of returns". But a dose that follows prices also
  carries a small-sample (Stambaugh-type) bias that surrogates do not share.
- Doses with level shifts or spikes (W30's re-dating week) are a poor fit for phase surrogates;
  IAAFT is safer there.
- R3's slow premium is an assumed world and did not set the threshold.
- Deviation from the card: power used the same 2,000 simulations as size (the card said 1,000).
- Part 3 read price bars from the lanes' own gitignored `research/data/` folders, through an
  environment variable (`lib/gatenull2_rescore_a.py` docstring).

## Proposed rule (for the lead; not adopted by this lane)

For a gate whose dose has lag-1 autocorrelation >= 0.8 at its own step (monthly, weekly), or a
dose with its own cycle:

- Add a second placebo family to the rule before any number: 40 phase-randomised surrogates of
  the dose's full series (IAAFT when the dose is skewed or mostly zeros), seed fixed.
- A pass needs t >= 2 with the predicted sign and rank <= 2 of 41 in both the shifted family and
  the surrogate family.
- Report both nulls' widths.
- Below 0.8 the surrogate family is optional (shown).
- Expected cost: 2-3 points of power at phi 0.9-0.95, 5-8 at 0.98-0.99.
- Keep the replication step.
