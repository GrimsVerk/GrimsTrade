# wide-28 card: `arms-fear`, does the US market earn more after a surge in household gun buying?

Lane wide-28, written 2026-11-26 (about 00:10 UTC), **before any return was read for this
rule** (card pushed first; the commit time is in git). Field: criminology and firearm-policy
research (gun purchases as a measure of household fear) x a fear premium. Candidate P1 of
`research/wide-28.md`, step 2. Gate **W45** (next free number: W44 was wide-27; open PRs #228
and #229 use no W number, #229 uses `W41n`), replication **R45** fixed below. No second gate.

## What was seen before this card (disclosed)

- BuzzFeed News `nics-firearm-background-checks.csv` (FBI NICS monthly checks by state, as
  compiled from the FBI's monthly PDF; repository MIT, last pushed 2023-10-02), downloaded
  2026-11-26 00:04 UTC from raw.githubusercontent.com (robots.txt: 404, no rule), 1,249,714
  bytes, sha256 ae0476f1bfe0df28582c8a3a6aecedda4ce0e9ad779cb875971611344533cfd6, cached under
  `wide-28/nics/2026-11-26/`. Seen: the header (month, state, permit, permit_recheck, handgun,
  long_gun, other, multiple, ..., totals), 16,445 data rows, 299 distinct months, first month
  1998-11, last 2023-09, and one Alabama row's first numbers. No sum, growth or dose was
  computed.
- Ken French `F-F_Research_Data_Factors_CSV.zip` and `..._daily_CSV.zip` (cached 2026-11-12):
  file names only; other lanes read the US market from them many times, never against gun
  purchases.

## Hypothesis

Background checks for gun sales surge when households are afraid: of crime and unrest
(2020), of a pandemic (March 2020), or of new gun laws after elections and mass shootings
(Nov 2008, Dec 2012) (Depetris-Chauvin, J. Public Econ. 2015, "Fear of Obama" `[memory]`).
Gun buying is a costly act by households, not a price and not a survey answer. If household
fear is shared by the marginal investor and priced (time-varying risk aversion), **the US
market's excess return is higher in the months after a surge in gun purchases: b > 0.**

Filters (wide-11 F1/F2): F1 passes as a premium (b): the dose is a state (how fast households
are buying), not a scheduled announcement. F2 passes only with controls: fear also follows
market falls (2008, 2020), when expected returns are high for other reasons; so the gate
carries the market's own past return and its own realised variance, and the placebo
calendars use earlier doses only.

## Data (keyless, cached)

- The NICS CSV above. **Sales proxy** S(m) = sum over every row (states and territories) of
  `handgun + long_gun + multiple` for month m (empty cells are 0): the usual proxy for sales,
  which leaves out permit checks and permit re-checks (Kentucky's monthly re-checks inflate
  `totals`). The FBI posts month m's table in the first days of month m+1 `[memory]` and does
  not revise it `[memory]`; **row m enters at the end of month m+1** (one month of slack), so
  nothing after month m+1 is used for row m.
- Returns: French factors, monthly `Mkt-RF` (% per month) and daily `Mkt-RF` (% per day), up
  to **2025-10** (nothing after 2025-10-31; the outcomes here end 2024-01).

## Rule (frozen)

- **Dose.** D(m) = ln( (S(m) + S(m-1) + S(m-2)) / (S(m-12) + S(m-13) + S(m-14)) ): the
  year-on-year growth of three months of gun sales (y/y removes the strong seasonal pattern
  and the level trend). Defined for m = 2000-01 .. 2023-09.
- **Outcome.** y(m) = Mkt-RF(m+2) + Mkt-RF(m+3) + Mkt-RF(m+4), % (three months after entry at
  the end of month m+1).
- **Controls**, from the market up to month m+1: c12(m) = sum of Mkt-RF over m-10 .. m+1;
  c1(m) = Mkt-RF(m+1); rv(m) = ln of the sum of squared daily Mkt-RF over months m-1 .. m+1
  (the market's own fear). Constant.
- **Rows.** m = **2008-08 .. 2023-09** with D(m), the controls and y(m) defined (182 months if
  all are; 2008-08 is the first month at which every shift below is defined).
- **Statistic.** OLS of y on D, c12, c1, rv and a constant; t of b with Newey-West (Bartlett)
  3 lags (`gatepower.dk_fit` with period = month); b in % over three months per unit of D.
- **Predicted sign: b > 0.**

## Placebo nulls (the decider, `research/gate-null.md` + gate-null-2's proposed rule, adopted here as in wide-27)

- **Shifted family**: D_k(m) = D(m - k), k = 25, 27, ..., 103 months (40 placebos, odd); same
  rows and controls.
- **Surrogate family**: 40 phase-randomised surrogates of the full D series (2000-01 ..
  2023-09), `gatenull2.surrogate_doses(..., "phase", 40, seed 2745)`; IAAFT instead only if
  the dry run shows |end - start| of D larger than one SD of D. The surrogate family gates if
  the dry run's lag-1 acf of D is 0.8 or more (a three-month y/y growth is expected near
  0.85-0.9); under 0.8 it is shown, not gating.

## Gate (pass only if all hold)

1. b > 0.
2. t >= 2.
3. The true t ranks among the 2 highest of 41 in the shifted family **and** among the 2
   highest of 41 in the surrogate family (when acf >= 0.8).

**Kill-only** (gate-null step 7): the smallest p a rank shows is 1/41 = 0.024, above the
family bar (0.10 / 112 = 0.00089 with this card) and the register's 9.8e-5. A fail kills the
idea; a pass says only "not dead yet".

**Replication R45, fixed now, run only if the gate passes** (earlier, non-overlapping years):
the same rule on rows m = 2000-01 .. 2008-05 (outcomes end 2008-09, before the gate's first
outcome month 2008-10); the 40 phase surrogates of the same D series (seed 2745). Pass: b > 0,
t >= 2, true t among the 2 highest of 41 surrogates. (The shifted family cannot be built
there.) R45 has about 100 months: weak, said now.

## Shown, not gating

- Horizons 1 month (NW 0), 6 months (NW 6), 12 months (NW 12).
- No controls; without rv.
- One-month dose ln(S(m) / S(m-12)); dose from `totals` instead of the sales proxy.
- Halves: rows 2008-08 .. 2015-12 and 2016-01 .. 2023-09.
- Without the pandemic surge: rows 2020-02 .. 2021-06 dropped.
- The null's width in both families: SD of placebo t, share with |t| >= 2, 5/50/95%,
  extremes.

## Power and my guess (written before any number)

The three-month US excess return has an SD near 8%; 182 months of a persistent dose are
perhaps 25-35 independent stretches, so only a large premium (2-3% over three months per SD
of the dose) would be seen. The big surges (late 2008, early 2013, spring 2020) sit next to
large market moves both ways (the 2009 fall and rebound, the 2013 rally, the 2020 rebound), so
the estimate rests on a handful of episodes. **Guess: b slightly positive, t between -1 and
+1.5, middle ranks in both families; pass 3%.**
