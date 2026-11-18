# Wide 9: gates for W19 and W17 under a placebo-based null; the gate-null method

Research run wide-9, 2026-11-19. Branch `wide-9` (from `wide-8`), draft PR into `wide-8`.
Research only: fake money, public data, no change to the gym, the daily runner or the live
strategies.

**Family count carried in:** 72 mechanisms, 16 tested by a strategy, none passed (wide-8). A
strategy test in this run would be read at **p < 0.10 / 72 = 0.00139** (family), and
project-wide at the register's bar (`git show origin/register-1:research/register/BAR.md`, read
2026-11-19: **2,904 tries, N 1,012 for a new pick, Bonferroni p <= 4.9e-5**).

Method as in ann-1 and wide-6..8: a gate is an event study whose rule, script and tests are
pushed before any number; it is descriptive, gets no `tries.md` row and does not count as a
tested mechanism. One dry run that prints counts only, then one real run. New in this run,
from wide-8's finding (153 placebo windows: t standard deviation 2.18, 35% with |t| >= 2):
**every gate judges its main statistic by its rank among placebo versions of itself, not
against N(0, 1).** A t >= 2 is still asked for (it costs nothing), but the rank decides.

## Step 1. W19 `enso-commodity` (oceanography)

### Data access (checked 2026-11-19, before any price was cut by it)

NOAA's Climate Prediction Center publishes the Oceanic Nino Index at
`https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt`; it downloads without a key or
account (a US government work, public domain). Columns: season (three-month label, e.g. `DJF`),
year, total Nino 3.4 sea-surface temperature, anomaly (the ONI). Seasons DJF 1950 to the latest
(the file read on 2026-11-19 ends with ASO 2026; its tail was printed to check the format, so
the late-2026 ONI was seen: a dose, not a return, and outside train). The file goes to
`research/data/oni/` (gitignored); the script reads it as text. Caveat: the file holds the
current ERSST version of every value, not the value as first published; revisions are a tenth
of a degree or two, small against the doses used here.

### The idea and literature

El Nino cuts crop yields in exposed regions (Australia, south and south-east Asia, southern
Africa) and raises non-fuel commodity prices over the following year. The ocean's state is
known months ahead and is set by no trader; futures may under-price the yield hit.

- **Cashin, Mohaddes and Raissi (2017)**, "Fair weather or foul? The macroeconomic effects of
  El Nino", Journal of International Economics 106, pp. 37-54. `[memory]` A global VAR on
  1979-2013 quarterly data: an El Nino shock raises non-fuel commodity prices (and inflation in
  most countries) over the following quarters; effects differ by region.

So the paper's years run to about 2013; **post-sample = decisions 2014-2025** (the 2015-16
strong El Nino, the 2020-23 triple La Nina, the 2023-24 El Nino: three or four episodes, weak).
No run here has cut returns by ONI.

### Decision rule (fixed and pushed before any number)

**Series.** DBC dividend-adjusted closes, train bars only (to 2025-11-10). DBC is the only broad
commodity fund in the cache; it is energy-heavy (more than half energy), so it tests the
paper's mechanism (non-fuel) only diluted. An agriculture fund (DBA) is not in the cache and is
not fetched here (assumption: the queue entry named DBC; a later lane may add DBA under its own
rule).

**Dose.** At the decision month M (calendar month, decision at the last bar on or before the
last day of M), x(M) = the ONI of the three-month season ending in month M-1 (e.g. decision at
the end of March uses DJF). CPC publishes a season's value in the first half of the month after
it ends, so x(M) is public by the end of M.

**Outcome.** y(M) = log(close at the last bar on or before the last day of month M+6 / close at
the last bar on or before the last day of month M). Observation kept if both bars exist, are
dated in months M and M+6, and the exit bar is on or before 2025-11-10.

**Regression.** y = a + b x + e over the decision months of a sample, Newey-West t with 6 lags
(the six-month outcomes overlap). b = extra six-month log return per degree of ONI.

**Placebo null (the decider).** The same regression with the ONI calendar moved earlier by k
whole years, k = 2 .. 41: x_k(M) = ONI of the season ending in month M-1 of year (year - k).
Whole years keep ENSO's seasonal cycle (events peak in winter); k = 1 is left out because ENSO
events often span two calendar years, so a one-year shift still shares part of the real episode.
40 placebos, all inside the file (earliest season used: 1972).

**Gate.** Pass only if all four hold:
1. DBC, decisions 2014-01 .. 2025-04: b > 0 with t >= 2.
2. Placebo rank: the true t ranks among the 2 highest of 41 (the true one and the 40 placebos);
   one-sided empirical p = rank / 41 <= 0.049.
3. Dose: on the same sample, the mean y over months with x >= 1.0 (strong El Nino) exceeds the
   mean over months with 0.5 <= x < 1.0 (weak El Nino).
4. In the paper's years (DBC decisions 2006-02 .. 2013-12): b > 0.

On a pass: a card for a commodity overlay (DBC held, or weighted up, for six months after the
ONI crosses +1.0) with rows in `tries.md`, read at p < 0.00139 (family) and the register's
p <= 4.9e-5. On a fail: W19 dead by the gate, no card, no row.

**Shown, not gating.** GLD and SLV with the same regression (2014-2025); DBC with a three-month
horizon; mean y by ONI bin (x <= -1.0, -1.0 < x <= -0.5, -0.5 < x < 0.5, 0.5 <= x < 1.0,
x >= 1.0) with month counts; the 40 placebo t, their standard deviation and the share with
|t| >= 2 (a second measure of how wide this design's null is, for the gate-null note of step
3).

**Power, written before any number.** DBC's six-month log return has a standard deviation of
about 18%; ONI about 0.9 degrees. ENSO episodes last a year or more, so 136 overlapping months
hold perhaps eight independent ONI swings; the standard error of b is then of order 6-8 points
per degree, and t >= 2 needs b of 12-16 points per degree (a strong El Nino of +2 adding 25-30%
over six months). Only a very large effect can pass.

**My guess before any number.** b between -8 and +8 points per degree, |t| < 1.5 post-sample;
the placebo t spread wider than N(0, 1) (standard deviation 1.3-2). Chance of a pass: 2%.
