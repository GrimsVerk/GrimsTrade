# parked-gates-1b: W32 `drought-inflation` passed its kill-only gate; a replication on 1962-2002 (R32)

Lane parked-gates-1, written 2026-11-25 about 01:15 UTC, **after** W32's gate result
(`results/drought-inflation.md`: TLT 3-month return on -PDSI, b -0.78% per unit, t -3.71, rank 1
of 41) and **before any number below**. `gate-null.md` step 7: a pass of a kill-only design
only says "not dead yet" and needs a new design with more independent episodes before any card.
This is that design: the same rule on a period the gate never saw, with a yield instead of
TLT (TLT starts 2002-07). The card `parked-gates-1.md` is not edited.

Seen before this card: W32's gate and shown cells (all 2002-2025), W33's result. Nothing of
1962-2002 bond yields or food prices has been read.

## R32: drought and the 10-year yield, 1962-2002

**Data (keyless, FRED graph CSV, one snapshot each into `parked-gates-1/fred/`).** `DGS10`
(10-year Treasury constant-maturity yield, daily from 1962-01-02, percent) and `CPIUFDSL` (CPI
food, seasonally adjusted, monthly from 1947; mechanism cell only). Same PDSI file as W32.

**Dose.** D(m) = -PDSI(m), as W32.

**Outcome.** y(m) = DGS10 on the last day with a value on or before the last day of m+4, minus
DGS10 on the last day with a value on or before the last day of m+1 (percentage points; both
days inside their months, else the row is dropped). Same timing as W32 (PDSI month m is posted
in the first ten days of m+1; the yield at the end of m+1 is after that).

**Statistic.** OLS y = a + b D, Newey-West 3 lags, one row a dose month (`ols_dk`, the W32 code
path with a yield outcome). Predicted **b > 0** (drought, higher yields, lower bond prices: the
sign of W32).

**Window.** Dose months 1962-01 .. 2002-03 (exit month m+4 <= 2002-07, before W32's first entry
at the end of 2002-08): 483 months, no outcome month shared with W32.

**Placebo null (the decider).** As W32: D_k(m) = D(m - k), k in +-{13, 17, ..., 89} (40; both
ways, weather does not answer prices). Placebo doses may come from W32's years; that is allowed
(the dose is weather, not a price).

**Gate. Pass only if both hold:** b > 0 with t >= 2, and the true t among the 2 highest of 41.

**Kill-only.** US droughts of 1962-2002 (1963-64, 1976-77, 1980-81, 1988-89, 1999-2002, smaller
ones): about 6-10 more episodes. Smallest p 1/41 = 0.024 per gate; even both gates together
(about 15 episodes) cannot reach the family bar (0.00103) or the register's (9.9e-5). A fail
here sends W32 back to "dead: one-period result"; a pass says "not dead yet, two periods" and
the next step would be other countries' droughts and bonds (a new card), never a strategy card
from this run.

**Shown (not gating).** The same yield design on W32's dose months 2002-07 .. 2025-06 (does the
yield agree with TLT?) and on 1962-01 .. 2025-06; growing-season dose months only (May-Sep,
1962-2002); the reaction cell (yield change over month m+1); the mechanism cell: food CPI log
change from month m+1 to m+4 on D (1962-01 .. 2025-06; predicted > 0; CPI is published mid-month
after, so this is a mechanism check, not a tradable signal).

**Post hoc on W32's gate sample (descriptive, not gating, picked after seeing W32).** W32's fit
without the dose months of one drought episode at a time: 2002-07 .. 2003-12, 2006-01 ..
2008-12, 2011-01 .. 2013-12, 2020-01 .. 2023-06; and without the dose months whose outcome
window touches 2022 (the bond crash: dose months 2021-08 .. 2022-10).

**My guess before any number.** The 2002-2025 result leans on 2020-2022 (the western drought
and the 2022 bond crash, an inflation regime coincidence like W29's); on 1962-2002, b positive
but t below 2. Chance of a pass: 15%.
