# wide-26 card: `drought-food-margin`, do US food stocks trail the market in the quarter after Corn Belt drought?

Lane wide-26, written 2026-11-25 (UTC), **before any return was read for this rule and before
any dose statistic was computed** (card pushed first; the commit time is in git). Field:
agronomy x food-processor margins (crop drought as an input-cost shock to listed firms).
Candidate H1 of `research/wide-26.md`, step 2. Gate **W43** and replication **R43**:
provisional ids (wide-25, running in parallel, takes W41/R41 and W42; the merging lead may
renumber; the card keeps these ids).

## What was seen before this card (disclosed)

- The nClimDiv state readme (`state-readme.txt`, fetched 2026-11-25 23:05 UTC from
  `www.ncei.noaa.gov/monitoring-content/...`; robots.txt read first: it disallows `/data*` and
  `/orders*`, not this path): the list of region codes (361 = Corn Belt, productivity
  weighted; 110 = contiguous US). No PDSI value was printed tonight; W32's write-up
  (parked-gates-1) published statistics of the contiguous-US series (code 110) on bonds and food
  CPI, which I have read (TLT t -3.71, R32 t -0.19, food CPI cell t -1.68).
- Ken French's 49 industry portfolios (`49_Industry_Portfolios_CSV.zip`, fetched 2026-11-25
  23:06 UTC from `mba.tuck.dartmouth.edu`; robots.txt read first: `/pages/faculty/ken.french/`
  is not disallowed; SHA-256 `d1a3b0b9896e1e633ed2aa85e24ca144d7998f8ab2ff344e2379383ebeb7b836`,
  CRSP vintage 202609): section titles, column names and the first and last month of the
  value-weighted monthly block (1926-07 .. 2026-09). No return.
- The literature as remembered (below).

## Hypothesis

Drought in the Corn Belt cuts corn and soybean yields over the growing season; feed grain,
corn sweetener, starch and vegetable-oil prices rise. Food processors and meat packers buy
these inputs, mostly hedged 3-12 months ahead, so the cost rise reaches their margins with a
lag, and W32/R32's food-CPI cell (wrong sign, t -1.68) suggests retail prices do not pass it on
quickly. The drought is public (the Palmer index and the Drought Monitor), but its effect on
profits is revealed in quarterly earnings. Hong, Li and Xu ("Climate risks and market
efficiency", Journal of Econometrics 2019 `[memory]`) find that a country's drought trend
predicts lower profitability and lower returns of its food stocks, which they read as the
market under-reacting to drought. If so, **the US food industry earns less than its market
beta implies in the quarter after Corn Belt drought: b < 0.**

Filters (wide-11 F1/F2): F1 passes weakly, as wide-24's Q1: drought is not a flow or a
premium; the form rests on slow revelation of a cost shock through earnings (-1 point). F2
passes: weather does not follow stock prices, so placebo calendars may move both ways
(gate-null step 1). Channel: not W32's. W32/R32 tested drought as an inflation-risk premium
on Treasuries (dead); this tests drought as a cost shock to one industry's cash flows, relative
to the market.

## Data (keyless)

- **Dose**: NOAA nClimDiv `climdiv-pdsist-v1.0.0-20261105` (cached by parked-gates-1,
  `parked-gates-1/climdiv/2026-11-25/`), element 05 (PDSI), code **361 = Corn Belt
  (productivity weighted)**, monthly from 1895, -99.99 missing, nothing after 2025-10. Today's
  vintage (recent months are revised; real-time vintages are not used, as in W32): noise in the
  dose, not price information.
- **Returns**: French 49 industries, value-weighted monthly block, column `Food` (SIC food
  products); market excess `Mkt-RF` and `RF` from the cached
  `french/2026-11-12/F-F_Research_Data_Factors_CSV.zip` (monthly block). Percent, simple
  monthly returns; -99.99 / -999 missing; nothing after 2025-10.

## Rule (frozen)

- **Dose.** D(m) = -PDSI_361(m) (positive = drier).
- **Available on (no look-ahead).** Month m is posted in the first ten days of m+1 (as W32).
  The outcome for dose month m covers months m+2, m+3, m+4.
- **Beta.** beta(m) = OLS slope (with intercept) of (Food - RF) on (Mkt-RF) over the 60 months
  m-58 .. m+1 (all known when the outcome window opens); all 60 needed, else the row drops.
- **Outcome.** y(m) = sum over j = m+2 .. m+4 of [(Food_j - RF_j) - beta(m) (Mkt-RF)_j], percent.
- **Rows.** Gate: dose months **1960-01 .. 2025-07** with all three outcome months on or before
  2025-10 and a beta.
- **Statistic.** OLS y = a + b D, one row per dose month, t of b with Newey-West (Bartlett) 3
  lags over the month index (`wide11_events.ols_dk` with one row per period, as W32; the same
  function for every cell and placebo).
- Predicted sign: **b < 0**.

## Placebo null (the decider)

- **Shifted calendars**, both ways (drought does not answer stock prices): D_k(m) = D(m - k),
  k in +-{13, 17, ..., 89} months (`wide17_events.SHIFTS_W29`, never a multiple of 12): 40
  placebos. The dose series runs 1895-2025, so every k has a dose for the gate months except
  the later shifts past 2025-10; a row with a missing D_k drops from that placebo only.
- **Dose autocorrelation and gate-null-2's proposed rule.** The PDSI is persistent; its lag-1
  autocorrelation over 1895-2025 is printed in the dry run and expected above 0.8. If it is
  0.8 or more, the "both families" rule applies: **40 phase-randomised surrogates** of the full
  1895-01 .. 2025-10 dose series (`gatenull2.phase_surrogates`, seed 26; the PDSI is a bounded
  index, about -6 .. +6, not a near-unit root, so no end-matching), each put on the same months,
  same rows, same function; the pass also needs rank <= 2 of 41 there.

## Gate (pass only if all hold)

1. b < 0.
2. t <= -2.
3. The true t ranks among the 2 lowest of 41 in the shifted calendars.
4. If the dose acf1 >= 0.8: also among the 2 lowest of 41 in the surrogates.

**Kill-only** (gate-null step 7): Corn Belt droughts come in about 10-15 episodes in 1960-2025
(1974, 1976-77, 1980, 1983, 1988-89, 2002, 2005-06, 2012, 2021-23 and smaller ones
`[memory]`). The smallest p a rank shows is 1/41 = 0.024, above the family bar (0.10 / 109 =
0.00092 after #215; 0.10 / 110 if wide-25's gate lands first) and the register's 9.8e-5. A fail
kills the idea; a pass says only "not dead yet".

**Replication R43, fixed now, run only if W43 passes** (independent episodes): the same rule,
placebos and pass conditions on dose months **1931-06 .. 1959-09** (the first month with a
60-month beta, to the last month whose outcome ends before the gate's first outcome month; the
1930s and 1950s droughts). Food stocks were then a different industry (fewer, older firms;
wartime price controls 1942-46), noted, not excluded.

## Shown, not gating

- Raw Food minus market (no beta): sum of (Food - RF) - (Mkt-RF) over m+2 .. m+4.
- W32's dose: contiguous-US PDSI (code 110) instead of the Corn Belt.
- Drying: PDSI_361(m-3) - PDSI_361(m) instead of the level.
- 12-month horizon: months m+2 .. m+13, Newey-West 12 lags.
- Growing-season dose months only (June .. September).
- Restaurants (`Meals`) instead of Food (food is about a third of their costs `[memory]`;
  predicted b < 0); farms (`Agric`, no sign predicted: drought cuts output and raises prices).
- Equal-weighted Food.
- The market itself: (Mkt-RF) over m+2 .. m+4 on D (W32-like; does drought predict the market?).
- After Hong, Li and Xu's sample (`[memory]`: it ends about 2015): dose months 2016-01 on.
- The null's width for both families: SD of placebo t, share with |t| >= 2, 5/50/95%
  quantiles, extremes.
- The five driest dose months of each episode are not listed; the ten largest D months in the
  gate rows are, with y.

## Power and my guess (written before any number)

A quarter's beta-adjusted Food excess has an SD of about 5-6% (food is a low-beta, mostly
idiosyncratic industry against the market). With about 260 non-overlapping quarters and a dose
SD near 2.5 PDSI units, SE(b) is about 5.5 / (2.5 x 16) = 0.14% per unit, more if the
persistent dose gives few effective episodes (likely 0.2). A pass needs about -0.4% per unit:
about -2% in the quarter after a severe drought (PDSI -4 to -5, as 1988 or 2012). The input-cost
share of grains in food processors' sales is a few percent and largely hedged, so a true effect
of that size would be at the top of what the size check allows. Guess: b near 0 or slightly
negative, t between -1.5 and +1, a middle rank, placebo SD 1.0-1.5 (persistent dose). Prior of
a pass: 3%.

## On the outcome

Pass: run R43 at once and report both. Fail: dead, one `screen` row in `research/tries.md`
(descriptive, not selectable); R43 is not run. Every shown cell gets a `robustness` row.
