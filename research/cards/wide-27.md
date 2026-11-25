# wide-27 card: `revision-noise`, does the US market earn more after a spell of noisy payroll data?

Lane wide-27, written 2026-11-25 (about 23:29 UTC), **before any return was read for this
rule** (card pushed first; the commit time is in git). Field: statistical-agency revision
patterns (data quality as an organisational process) x a data-uncertainty premium. Candidate
O6 of `research/wide-27.md`, step 2. Gate **W44** (provisional: W42 unused by wide-25, W43
taken by wide-26, PR #223; the merging lead may renumber), replication **R44** fixed below. No
second gate (W45 not used).

## What was seen before this card (disclosed)

- Philadelphia Fed Real-Time Data Set, `employmvmd.xlsx` (nonfarm payroll employment, monthly
  vintages; cached 2026-11-12 under `philly-rtdsm/2026-11-12/`): sheet name `employ`, 1,055
  rows, 744 columns, first column `DATE`, vintage columns `EMPLOY64M12` .. `EMPLOY26M10`. No
  value and no revision was computed.
- Ken French `F-F_Research_Data_Factors_CSV.zip` (cached 2026-11-12): file name only; other
  lanes have read the US market from it many times, never against a revision dose.
- No probe of any patent series returned data (USPTO pages 404, ALFRED reset the connection;
  step 2, O1).

## Hypothesis

Payroll employment is first published from an incomplete sample and revised in the next two
monthly releases and at the annual benchmark. When revisions run large for a spell, the data
investors use to read the state of the economy are noisier. In learning models of
uncertainty (Pastor and Veronesi; Veronesi 1999 `[memory]`) noisier signals about the state
raise the uncertainty investors bear; if that uncertainty is priced, **the US market's excess
return is higher in the months after a spell of large payroll revisions: b > 0.** The noise
comes from the statistical agency's survey process (response rates, birth-death model,
benchmark), not from prices.

Filters (wide-11 F1/F2): F1 fails as a flow (each revision arrives in a scheduled release) and
passes as a premium (b): the dose is a state (how noisy the data have been), not the content
of one release. F2 passes only with controls: revisions are larger in recessions and at
turning points, when the market has fallen and expected returns are high for other reasons;
so the gate carries the real-time payroll growth, the real-time volatility of monthly payroll
changes and the market's own past return as controls, and the placebo calendars use earlier
doses only.

## Data (keyless, cached)

- `employmvmd.xlsx` as above, read with the stdlib xlsx reader (`long_x.xlsx_rows`, sheet
  `employ`). Vintage column `EMPLOYyyMm` is the series as the Philadelphia Fed recorded it in
  the middle of month m (after that month's first-Friday Employment Situation release): its
  last observation is month m-1. **Vintage m is known by mid-month m; nothing after it is
  used for row m.** Vintages 1964-12 .. 2025-10 only (train). Missing cells (`#N/A`, empty)
  are missing.
- Returns: French `F-F_Research_Data_Factors_CSV.zip`, monthly block, `Mkt-RF` (% per month),
  months up to **2025-10** (nothing after 2025-10-31).

## Rule (frozen)

- **Level.** E_v(j): employment for reference month j in vintage v. Delta_v(j) =
  100 ln(E_v(j) / E_v(j-1)).
- **Revision at vintage v.** rev(v) = |Delta_v(v-2) - Delta_{v-1}(v-2)| +
  |Delta_v(v-3) - Delta_{v-1}(v-3)| (the first and the second revision of a month's change,
  benchmark months included). Undefined if any of the four values is missing.
- **Noise state.** R12(v) = mean of rev over v-11 .. v (all 12 defined, else undefined).
  **Dose** D(v) = ln R12(v) - mean of ln R12(u) over u = v-120 .. v-1 (all 120 defined, else
  undefined): the noise relative to the last ten years (revisions shrank as the survey grew;
  the trailing mean removes that slow drift).
- **Outcome.** y(v) = Mkt-RF(v+1) + Mkt-RF(v+2) + Mkt-RF(v+3), % (three months after the
  vintage month; entry at the end of month v, after the vintage is known).
- **Controls**, all from vintage v or the market up to month v: g12(v) = 100 ln(E_v(v-1) /
  E_v(v-13)) (real-time payroll growth over a year); s12(v) = ln of the mean of
  |Delta_v(j) - mean over the same window| for j = v-12 .. v-1 (real-time volatility of
  monthly changes, so the dose is noise beyond the size of the moves); c12(v) = sum of
  Mkt-RF over v-11 .. v; c1(v) = Mkt-RF(v). Constant.
- **Rows.** v = **1990-01 .. 2025-07** with D(v), the controls and y(v) defined (427 months
  if all are).
- **Statistic.** OLS of y on D, g12, s12, c12, c1 and a constant; t of b with Newey-West
  (Bartlett) 3 lags (`gatepower.dk_fit` with period = month); b in % over three months per
  unit of D.
- **Predicted sign: b > 0.**

## Placebo nulls (the decider, `research/gate-null.md` + gate-null-2's proposed rule, adopted here)

- **Shifted family**: D_k(v) = D(v - k), k = 25, 27, ..., 103 months (40 placebos, odd); same
  rows and controls (D is defined from about 1975-11, so every shift is defined for every
  row).
- **Surrogate family**: the dose is persistent by construction (a 12-month rolling mean;
  expected lag-1 acf about 0.9-0.95, the dry run prints it). **This card adopts gate-null-2's
  proposed "both families" rule** (stricter than gate-null.md alone): 40 phase-randomised
  surrogates of the full D series (all months where D is defined, 1975-11 .. 2025-07),
  `gatenull2.surrogate_doses(..., "phase", 40, seed 2744)`; IAAFT is used instead only if the
  dry run shows |end - start| of D larger than one SD of D (gate-null-2's end-mismatch
  caveat), which the dry run prints before any return is read. If the dry run's acf is under
  0.8, the surrogate family is shown, not gating, as gate-null-2 says.

## Gate (pass only if all hold)

1. b > 0.
2. t >= 2.
3. The true t ranks among the 2 highest of 41 in the shifted family **and** among the 2
   highest of 41 in the surrogate family (when acf >= 0.8).

**Kill-only** (gate-null step 7): the smallest p a rank shows is 1/41 = 0.024, above the
family bar (0.10 / 111 = 0.00090 after #221, #223 if merged, and this card) and the register's 9.8e-5. A
fail kills the idea; a pass says only "not dead yet".

**Replication R44, fixed now, run only if the gate passes** (earlier, non-overlapping years):
the same rule on rows v = 1976-01 .. 1989-09 (outcomes end 1989-12, before the gate's first
outcome month 1990-02); the 40 phase surrogates of the same D series (seed 2744). Pass: b > 0,
t >= 2, true t among the 2 highest of 41 surrogates. (The shifted family cannot be built
there: D starts about 1975-11.)

## Shown, not gating

- Horizons 1 month (NW 0), 6 months (NW 6), 12 months (NW 12).
- No controls; without s12; first revision only (|Delta_v(v-2) - Delta_{v-1}(v-2)|).
- Dose in levels: ln R12(v) without the trailing-mean step (rows as the gate).
- Halves: rows 1990-01 .. 2007-12 and 2008-01 .. 2025-07.
- The null's width in both families: SD of placebo t, share with |t| >= 2, 5/50/95%,
  extremes.

## Power and my guess (written before any number)

The three-month market excess return has an SD near 8%. With a persistent dose the effective
sample is small (a 12-month rolling mean over 427 months is perhaps 30-40 independent
stretches), so the test only sees a large premium: roughly 2-3% over three months per SD of
the dose. I know of no paper that finds a payroll-revision premium in stock returns; my prior
is low. **Guess: b near 0, t between -1.5 and +1.5, middle ranks in both families, shifted
null somewhat wider than surrogates; pass 3%.**
