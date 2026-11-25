# wide-22 card: `grid-load-premium`, does high industrial electricity use foretell low US stock returns?

Lane wide-22, written 2026-11-25, **before any return was read for this rule** (card pushed
first; the commit time is in git). Field: energy systems (grid load as a physical gauge of the
output gap) x the counter-cyclical risk premium. Candidate E1 of `research/wide-22.md`, step 2.
Gate **W36**, replication **R36** (the next free ids after W35 on `main`'s `gate-null.md`;
provisional: a parallel lane may take the same number, the lead renumbers).

## What was seen before this card (disclosed)

- EIA Monthly Energy Review Table 7.6 (electricity end use), format probe: 5,768 data rows, eight
  series (MSN codes ELDUPUS, ELTCPUS, ESACPUS, ESCCPUS, ESICPUS, ESRCPUS, ESTCPUS, ESVHPUS);
  ESICPUS (industrial retail sales, million kWh) has 644 monthly rows 1973-01 .. 2026-08 plus
  annual rows (YYYY13) from 1949. Printed values: the first three annual rows of ESRCPUS and
  ESICPUS (1949-1951). No monthly value was read.
- Ken French's monthly factor file (cache 2026-11-12, from earlier lanes), format probe only:
  months 1926-07 .. 2026-09 (1,203 rows). No value was read. Months after 2025-10 are never used.
- The literature only as a search summary (below).

## Hypothesis

Da, Huang and Yun ("Industrial Electricity Usage and Stock Returns", JFQA 52(1), 2017, 37-69;
2017 Sharpe award) report that the year-on-year growth of US industrial electricity use
predicts stock market returns up to a year ahead with the negative sign (R-squared about 9% at
one year; about -0.9% excess return in the next year per 1 point of growth; sample about
1956-2010; also Japan and the UK) `[search summary]`. Their story is a counter-cyclical risk
premium: industrial power use is a physical, hard-to-fake measure of how hot the economy runs
(the output gap); in a boom the premium investors ask is low, so later returns are low.
**Prediction: b < 0.** The test here is mostly after their sample (2011-2025 is fully
post-sample; 1974-2010 overlaps it), on the EIA monthly series from 1973.

Filters (wide-11 F1/F2, #109): F1 passes (b), a risk premium: the dose is a public statistic,
but a premium is earned on public information and is not front-run away. (A nowcast reading,
"good news not yet priced", would predict b > 0; the sign separates the two.) F2 passes
outright: factories do not set their power use by the stock price within months. Prices do
lead output, though, so a dose from the future is partly a function of today's returns: the
placebo family uses earlier doses only (gate-null step 1), and the shown cells include a
feedback check and price controls.

## Data (keyless)

- Electricity: EIA MER Table 7.6 CSV, `https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T07.06`
  (US public domain), fetched once 2026-11-25 into the shared cache
  `wide-22/2026-11-25/eia/T07.06.csv`, read as untrusted data with `python -I`. Monthly rows
  only (YYYYMM, month 01-12); annual rows ignored. Months after 2025-10 are never read.
  Vintage: the current file (revisions to old months are small; real-time vintages are not
  keyless here; caveat fixed now).
- Publication lag: EIA's Electric Power Monthly publishes month m's sales around the 24th-26th
  of month m+2, the MER at about the same time. **The dose of usage month m is paired with the
  market return of month m+3**, which starts after month m+2 ends.
- Market, gate: French monthly `Mkt-RF` (value-weighted US market minus the one-month T-bill),
  in percent, from `F-F_Research_Data_Factors_CSV.zip` (cache 2026-11-12), months through
  2025-10 only.
- Shown: `harness.load_history("train")` month-end closes of SPY, TLT, GLD, BTC (no bar after
  2025-10-31).

## Rule (frozen)

- U(m) = ESICPUS, industrial retail sales of electricity in month m (million kWh).
- Dose g(m) = 100 x ln(U(m) / U(m - 12)): year-on-year growth in percent (same calendar month,
  so the seasonal cycle drops out). NaN unless both months exist.
- Outcome y(m) = Mkt-RF of month m + 3 (percent).
- Rows: usage months m with g(m) and y(m) defined: 1974-01 .. 2025-07 (outcomes 1974-04 ..
  2025-10).
- Statistic: OLS y(m) = a + b g(m); t of b with Newey-West standard errors, 3 lags (as W33/W34;
  the dose is persistent, the outcome is not overlapping).
- Predicted sign: **b < 0** (b in percent a month per point of growth).

## Placebo null (the decider, `research/gate-null.md`)

Earlier doses only (prices lead output; step 1): g_k(m) = g(m - k), k in {25, 27, 29, ..., 103}
(odd, **40 placebos**, as W33/W34). Each placebo uses the rows where g(m - k) and y(m) exist (its
first rows start k months after 1974-01). Same function, same code path, a shift argument.
Business cycles are irregular (about 5-10 years), not a fixed clock, so the W35 anti-phase
problem is not built in; as a diagnostic (shown, not gating) the run also ranks the true t among
40 phase-randomised surrogates of g (same spectrum, random phases, seed fixed at 22).

## Gate (pass only if all hold)

1. b < 0.
2. t <= -2.
3. The true t ranks among the 2 lowest of 41 (empirical one-sided p = rank / 41 <= 0.049).
4. Post-sample sign: on usage months 2011-01 .. 2025-07 (after the paper's sample), b < 0
   (sign only, same regression).

**Kill-only** (gate-null step 7): 1974-2025 holds about 7 recessions and 3-4 industrial
slowdowns without a recession (1985-86, 1998, 2015-16, 2019), so about 10 independent swings of
the dose; the smallest p a rank can show is 1/41 = 0.024, far above the family bar
(p < 0.10 / 104 = 0.00096, with this gate) and the register's Bonferroni 9.9e-5. A fail kills
the idea; a pass says only "not dead yet".

**Replication fixed now, run only if the gate passes (R36):** an independent earlier period,
before the paper's sample. NBER Macrohistory "Electric Power Production for United States"
(FRED `M01128USM247NNBR`, keyless `fredgraph.csv`, monthly from 1919), dose 100 x ln(P(m) /
P(m - 12)), outcome French `Mkt-RF` of month m + 3, usage months from 1926-04 (first outcome
1926-07) to the earlier of the series' end and 1955-12; NW 3 lags; earlier-only placebos k =
25..103 odd; pass needs b < 0, t <= -2 and rank <= 2 of 41. Total (not industrial) production
is the only monthly series of that age; that weakens the replication and is fixed now. If the
series cannot be fetched keylessly or has fewer than 240 usable months, R36 is reported as
not runnable and W36 stays "not dead yet, unreplicated".

## Shown, not gating

- (a) Controls: the same regression plus the market's own return of month m + 2 and its
  12-month return m - 9 .. m + 2 (the last data known when the dose is), NW 3.
- (b) Paper's horizon: y12(m) = sum of Mkt-RF over months m + 3 .. m + 14, NW 18 (overlapping:
  noted only).
- (c) Sub-periods: usage months 1974-01 .. 2010-12 (inside the paper's sample) and 2011-01 ..
  2025-07 (after it) with t.
- (d) Common rows (the rows every placebo has) with the true t and its rank there.
- (e) Negative control: residential sales (ESRCPUS) growth instead of industrial (weather
  driven, a small business-cycle part): expected near zero.
- (f) Feedback: g(m) on the market's 12-month and 24-month returns ending at month m (prices
  lead output; expected positive).
- (g) Phase-randomised surrogates (above): rank of the true t among 40.
- (h) Live assets: next-month (month m + 3) log return of SPY, TLT, GLD, BTC month-end closes on
  g(m), NW 3, from their first cached month.
- The null's width: SD of placebo t, share with |t| >= 2, 5/50/95% quantiles, extremes.

## Power and my guess (written before any number)

g has a sd of about 4-5 points (from memory of the series, not looked up); monthly Mkt-RF has a
sd of about 4.5%; with about 615 rows SE(b) is about 4.5 / (4.5 x 24.8) = 0.040 (about 0.045
with NW). At the published size (-0.9% a year per point, so about -0.077 a month) t is about
-1.7: **power for t <= -2 is only about 35-40% even if the effect is real at full size**, and
less if it halved after publication (as most published predictors did, McLean and Pontiff 2016
`[memory]`). So a fail is a weak kill of the published size and a strong kill of anything
larger. Guess: b negative but small, t between -1.5 and 0, a middle-to-low rank, placebo SD
1.0-1.4 (a persistent business-cycle dose), post-sample b of either sign. Prior of a pass: 5%.

## On the outcome

Pass: "not dead yet"; run R36 at once (fixed above) and report both. Fail: dead, one `screen`
row in `research/tries.md` (descriptive, not selectable); the output-gap premium class
(capacity utilisation, freight volumes as gauges) is then parked with it.
