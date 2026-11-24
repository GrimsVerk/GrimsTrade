# Wide 13: data-wide-1's eleven ideas scored, the top two gated

Research run wide-13, 2026-11-19. Branch `wide-13` (from `data-wide-1`), draft PR into
`data-wide-1`. Research only: fake money, public keyless data already in the shared cache, no
change to the gym, the daily runner or the live strategies.

**Count carried in:** wide-12 (draft PR on branch `wide-12`): union of the wide and survey
lines **81 mechanisms, 18 tested by a strategy, none passed; 16 gates, all failed**. weather-1
(branch `weather-1`) added one gated mechanism (`hdd-gas`, UNG on heating-degree-day
surprise, gate failed, logged as a `screen` row) without a W number: **82 mechanisms, 17
gates**. Project-wide bar (`git show origin/register-5:research/register/BAR.md`, rows through
2026-11-19 00:30): **3,130 tries, N 1,032 for a new pick; measured rho 0.53 gives N_eff 486: a
new rule needs z >= 4.69, an edge over `tsmom12` of +0.30 (close rule) to +0.56 (far rule) in
annual Sharpe on the primary test, Bonferroni p <= 1.0e-4.** Published effects after their
publication in this book: 0 for 10 (wide-12's count).

Method: every gate follows `research/gate-null.md` (placebo family fixed in the rule, 40
placebos, one code path for true and placebo, the rank decides, t >= 2 also required; rule,
script and tests pushed before any number; one dry run that prints counts only, then one real
run). Train only: no bar after 2025-11-10 is loaded; the held-out year is never read. As
weather-1 did, each gate gets one `screen` row in `tries.md` (descriptive, not selectable, not a
strategy try).

## Step 1. The eleven ideas scored (2026-11-19, before any price was read)

Scoring: wide-11's filters F1 (not announced: an unscheduled flow, or a premium) and F2 (not
price-driven; passing only with controls costs 1 point), then wide-10's six points (cause 1,
dose 2, post-sample 1, power 1, unseen 1, not killed in other words 1). Ideas numbered as in
`data-wide-1.md`, "For wide-13". "Loaded" = the four sources with loaders in
`lib/datawide1.py` (GPR, FDIC, MOF, USGS); the brief limits the gates to those.

**Post-sample, read literally.** wide-10's point needs 8 train years after the source
literature's latest sample, "or after the idea was first formed if it has no literature". These
ideas were formed tonight (data-wide-1), so an idea with no literature has no train years after
its formation: post-sample 0. That is the conservative reading, applied to every row.

| # | Idea (source, assets) | F1 | F2 | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Note |
|---:|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---|
| 1 | GPR acts: safe-haven premium (GPR, GLD/TLT) | pass (b) premium | pass | 0 | 2 | 0 | 1 | 1 | 1 | 0 | **5** | loaded |
| 2 | GPR and the oil premium (GPR, DBC/XLE) | pass (b) | with controls: war coverage and oil spikes feed each other the same weeks | 0 | 2 | 0 | 1 | 1 | 1 | -1 | 4 | loaded; DBC holds oil only in part |
| 3 | Bank-failure Fridays, Monday flight to quality (FDIC, TLT/IEF) | **fail** as written: the failure is public Friday evening, before Monday's window; a flight to quality is a repricing on public news, neither an unannounced flow nor a premium | - | - | - | - | - | - | - | - | - | filtered |
| 3' | Same dose as a **bank-distress premium** (FDIC, XLF) | pass (b): holders of bank equity are paid for contagion risk over the weeks after a failure | with controls: failures follow bank stock falls with lags (XLF's own 4/13/26/52-week returns) | 0 | 2 | 0 | 1 | 1 | 1 | -1 | **4** | loaded; 594 closures since 2000 but two clusters |
| 4 | MOF dollar buying, Treasury purchases (MOF, TLT/IEF) | pass (a) on the **monthly** total only (below) | with controls (leans against USDJPY; no USDJPY in the project's data) | 0 | 2 | 1 | 0 | 1 | 0 | -1 | 3 | W23 `custody-selling` (foreign official Treasury flow carry-over, dead at t -1.20) is the same channel |
| 5 | Japan quakes, yen repatriation (USGS, TLT/SPY) | pass (a) | pass | 1 (claims are contractual) | 2 | 0 | 0 | 1 | 0 | 0 | 4 | W15 `cat-claims` (insurers liquidate to pay catastrophe claims, dead) is the same story; M >= 7 near Japan since 2002: a few dozen events |
| 6 | Quakes in copper/oil regions (USGS, DBC) | **fail**: a supply shock is public within minutes and priced on the day; no flow or premium follows | - | - | - | - | - | - | - | - | - | filtered |
| 7 | Nuclear outages above the seasonal norm (EIA, DBC/XLU) | **fail**: outages are published daily before any window; extra gas burn is news, priced on publication | - | - | - | - | - | - | - | - | - | filtered (not loaded) |
| 8 | Flu above the seasonal norm (FluView, XLV/SPY) | **fail**: weekly public report; news, not a flow or premium | - | - | - | - | - | - | - | - | - | filtered (not loaded) |
| 9 | Stolen coins, laundering sales (DefiLlama, ETH vs BTC) | pass (a): the date of the sales is not public | with controls (sums stolen scale with prices) | 0 | 2 | 0 | 1 | 1 | 1 | -1 | 4 | not loaded; no publication date per event (curated, back-filled), so no honest "available on" rule |
| 10 | Chokepoint closures (PortWatch, DBC) | pass (a)/(b) | pass | 0 | 2 | 0 | 0 | 1 | 1 | 0 | 4 | under 7 years: a lead at most, no gate before 2027 (data-wide-1) |
| 11 | Central-bank gold buying (IMF, GLD) | pass (a) | with controls (buyers paused on price spikes) | 0 | 2 | 0 | 1 | 1 | 1 | -1 | 4 | not loaded (IMF SDMX never queried) |

Points that decide the ranking:
- **1 power 1:** the dose is a continuous weekly index, about 1,080 weeks with both GLD and
  TLT in 2005-2025 (270 non-overlapping 4-week blocks per asset, 540 for the two).
- **1 post-sample 0:** Caldara and Iacoviello, "Measuring geopolitical risk", American Economic
  Review 112(4), 2022, pp. 1194-1225, use the index to 2019 or 2020 `[memory]`; the
  precious-metals hedging paper (Baur and Smales, Journal of Banking & Finance 117, 2020) ends
  about 2018 `[memory]`. 2020-01 .. 2025-10 is 5.8 train years: under 8. The safe-haven premium
  cut (next 4 weeks after acts, from the date the index is public) is not the papers' claim (they
  report same-period effects on activity and stock returns), so this is not a post-publication
  test of a published effect; it is shown on the post-paper years anyway (step 2).
- **1 unseen and not killed:** no run in this repo has read GPR against a price. wide-12's D3
  `geopolitical-premium` (threats index, stocks, parked at 4, never computed) is the nearest;
  idea 1 uses the acts sub-index and safe-haven assets, and SPY appears here only as a shown
  cell, so D3 is not run in disguise.
- **3' power 1:** at least 200 dosed events (594 closures since 2000, about 250 failure weeks);
  the two clusters (2008-2012, 2023) are what the placebo null measures.

**Idea 4 and the MOF lag, stated as the brief asks.** The daily detail of interventions is
published once a quarter (data-wide-1's default: quarter end + 45 days, unchecked). A trading
rule cannot use a daily operation 45-135 days after it happened: an event study on daily
operation dates would read a flow nobody could see in time, so **it is not a tradable gate and is
not run**. What is usable in real time is the monthly total, public on the month's last business
day. Since TLT exists (2002-07) yen-selling months number about two dozen, nearly all in
2002-2004 and 2010-2011, and the channel is W23's: idea 4 scores 3 and is not picked.

**Picked: idea 1 as W25 `act-haven` (5), and idea 3' as W26 `failure-premium` (4).** Idea 3'
ties at 4 with 2, 5, 9, 10, 11; tie-break by wide-10's rule (fewest fetches: loaded first), then
the higher prior: 2 needs an oil control that is not in the data, 5 is W15 in other words with
a few dozen events, 9-11 are not loaded. 3' is gated knowing it scores under wide-12's
threshold of 5; it is the strongest second candidate on loaded data, and the lead asked for up to
two.

Priors: W25 1% (a safe asset is insurance, so theory leans to a *lower* expected return when risk
is high; the premium story needs slow-moving hedging demand after acts; and the dose arrives 9-15
days late). W26 1% (bank-equity distress premia are plausible, but failure weeks sit inside two
crises where the 4-week path was dominated by the crisis itself).

## Step 2. W25 `act-haven` gate (rule fixed and pushed before any number)

**Data.** The daily GPR file in the cache (`data-wide-1/gpr/<latest snapshot>/`, read with
`lib/datawide1.read_gpr_xls`, `uv run --with xlrd python -I`), columns `GPRD_ACT` (acts) and
`GPRD_THREAT` (threats). Values before 2022-02 exist only in today's revised form (median
revision 2.7% of the level against the 2022-02-24 vintage): the z below is on log levels, so a
2.7% revision moves it by about 0.03 log points, small against a weekly spread of tenths. No
vintage is read: only six were fetched, and a mixed as-of reading would change the dose
definition mid-sample.

**Dose.** For each Monday M: A(M) = mean of `GPRD_ACT` over the seven days M - 6 .. M;
d(M) = ln(1 + A(M)); z(M) = (d(M) - mean) / sd (ddof 1) over d of the Mondays M - 1092 .. M - 7
days (156 weeks), needing at least 104. Past-only. Predicted sign: positive (after adverse acts
GLD and TLT earn more over the next 4 weeks).

**Available on (no look-ahead).** `datawide1.gpr_available_on(M)`: the first Wednesday at least 9
days after M, i.e. M + 9 (covers one slipped weekly update). Entry at the close of the asset's
first bar dated >= M + 9, exit at the close of the first bar dated >= M + 37. y(M) = ln(exit /
entry), dividend-adjusted closes (`harness.load_history("train")`). The row is dropped if either
bar is missing, the exit bar is dated after M + 44, or after 2025-11-10.

**Panel and statistic.** Gate assets GLD and TLT (the gym's two safe havens). Pooled OLS
y = a_asset + b z (F2 passes outright: no controls in the gate). t of b with Driscoll-Kraay
standard errors: scores summed over the rows of each Monday, Newey-West (Bartlett) 4 lags over
the week index (weeks counted by date).

**Placebo null (the decider).** The same function with the dose calendar moved by k weeks:
z_k(M) = z(M - 7k days), outcomes stay put, rows with a missing z_k dropped from that placebo
only. k in +-{27, 31, ..., 103} (odd, step 4): **40 placebos** (wide-11/12's family: war episodes
keep the index high for months; odd weeks are never a whole year).

**Gate. Pass only if both hold** (Mondays 2005-01-03 .. 2025-10-06; GLD trades from 2004-11):
1. b > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41 (empirical one-sided p = rank / 41 <= 0.049).

**Shown, not gating** (b, t, rows): threats sub-index z instead (priced on the day by the
story: predicted near 0); the total index `GPRD`; GLD alone; TLT alone; SPY alone (D3's
neighbour, not a gate); the post-paper years, Mondays 2020-01-06 .. 2025-10-06; with the
asset's own past 4/13/26/52-week returns as controls (at the last bar <= M); the 1-week horizon
(exit at the first bar >= M + 16, 1 lag); the F2 feedback check, z(M) on each past return alone
(GLD and TLT pooled, asset intercepts, Driscoll-Kraay 4 lags); the placebo null's width.

**Power, written before any number.** 4-week sd: GLD about 5%, TLT about 4%. About 1,080
Mondays, two weakly correlated assets (about 1.8 effective), returns overlapping by 3 weeks:
standard error of b about 4.5% / sqrt(1,080 x 1.8 / 4), near 0.2% per unit of z. A premium of
0.2-0.4% per 4 weeks per sd of acts gives t 1-2: only an effect at the top of that range passes.

**My guess before any number.** b near zero, t between -1 and +1.5, rank in the middle; placebo
t sd 1.0-1.4. Threats cell near zero too. Feedback weak (|t| < 1.5). Chance of a pass: 1%.

## Step 3. W26 `failure-premium` gate (rule fixed and pushed before any number)

**Data.** FDIC failures in the cache (`data-wide-1/fdic/<latest snapshot>/`, read with
`lib/datawide1.parse_fdic_failures`, `python -I`), kinds FAILURE and ASSISTANCE.

**Dose.** Weeks end on Fridays F and run Saturday F - 6 .. Friday F. S(F) = sum of total assets
at failure (`QBFASSET`, thousands of USD, nominal; a missing value counts 0) of the closures in
the week, in millions of USD. x(F) = ln(1 + S(F)): 0 in weeks without a failure. Predicted sign:
positive (a distress premium on bank equity after failures).

**Available on (no look-ahead).** `datawide1.failure_available_on(day)` = the next calendar day
(closures are announced after the close). Every closure in the week ending F is public by
Saturday F + 1. Entry at the close of XLF's first bar dated >= F + 3 (Monday; the Monday reaction
is left out on purpose: the premium is earned after the news is priced), exit at the close of the
first bar dated >= F + 31. y(F) = ln(exit / entry), dividend-adjusted. The row is dropped if
either bar is missing, the exit bar is dated after F + 38, or after 2025-11-10.

**Controls (F2), every horizon up to a year.** r_h(F) = ln(close of XLF's last bar <= F / close
of the last bar <= F - h days) for h = 28, 91, 182, 364.

**Statistic.** One asset, OLS y = a + b x + g4 r4 + g13 r13 + g26 r26 + g52 r52; t of b with
Newey-West (Bartlett) 4 lags over the week index (weeks counted by date). The same Driscoll-Kraay
function as W25 with one row per week, so it is the same code path.

**Placebo null (the decider).** x_k(F) = x(F - 7k days), outcome and controls stay put, rows with a
missing x_k dropped from that placebo only; k in +-{27, 31, ..., 103}: **40 placebos**. Failures
cluster in 2008-2012, so many shifted calendars still land inside the crisis: that is the null
this design has, and the rank is read against it.

**Gate. Pass only if both hold** (Fridays 2000-01-07 .. 2025-10-03; XLF from 1998-12, its 52-week
control from 1999-12):
1. b > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41.

**Shown, not gating:** without the controls; a failure-week dummy instead of x; the year 2023
dropped (SVB, Signature, First Republic: three of the largest failures in one spring); SPY, TLT and
IEF instead of XLF (TLT/IEF: idea 3's flight to quality, whose F1 fails, shown only); the Monday
reaction alone (XLF, close of the last bar <= F to the close of the first bar >= F + 3, no
controls, 1 lag); the 1-week horizon (exit at the first bar >= F + 10, 1 lag); the F2 feedback
check: x(F) on each of XLF's past returns alone (positive story: failures follow falls, so the
slope should be negative); the placebo null's width.

**Power, written before any number.** XLF 4-week sd about 6-7% (far more in 2008-09). About 250
failure weeks in about 1,340 weeks, in two clusters. If a failure week of median size (x about 5,
an assets sum near 150 million) earns 1% more over the next 4 weeks, b is 0.2% per unit of x; with
x sd near 2.5 over all weeks and overlap of 3 weeks, the standard error is about 6.5% / (2.5 x
sqrt(1,340 / 4)), near 0.14% per unit: t about 1.4 before the clustering, less after.

**My guess before any number.** The 2008 failures came before the worst months and the 2009-10
failures during the rally: b of either sign, t between -1.5 and +1.5, rank in the middle; placebo
t sd 1.2-1.8 (clustered dose). Feedback strongly negative at 26-52 weeks (failures follow a fall),
t below -3. Chance of a pass: 1%.

**On a pass (either gate):** no card in this run. A proposed card for the next window, read at the
family bar p < 0.10 / 84 = 0.00119 and the register's bar above, with z = (t - placebo median) /
placebo sd. **On a fail:** dead by the gate, no card, no strategy; one `screen` row each.

## What came out (one dry run, then one real run, 2026-11-19)

Dry run first (`DRY=1`, counts only): GPR 14,924 days 1985-01-01 .. 2025-11-10 (nothing later
read), 2,028 weekly acts z; 1,084 gate Mondays, every one with a z; 1,083 rows each for GLD, TLT
and SPY (the last Monday's exit falls after 2025-11-10); the 40 placebos keep 986 to 1,084 dose
weeks. FDIC: 4,113 failures read (none after 2025-11-10), 1,871 dose weeks from 1990; 1,344 gate
Fridays, **268 with a failure**; 1,344 XLF and SPY rows with outcome and all four controls, 1,158
for TLT and IEF (from 2002-07); placebos keep 1,246 to 1,344 dose weeks. Then one real run each,
as carded. Tables: `results/act-haven.md`, `results/failure-premium.md`.

### W25 `act-haven`: fails

**One unit of acts z goes with -0.137% on GLD and TLT over the next 4 weeks (t -1.02, 2,166
rows, 2005-01 .. 2025-10): the wrong sign; the true t ranks 21 of 41 (empirical one-sided p
0.51). Dead by the gate: no card, no strategy.** Held-out year untouched.

| Cut (4-week return, GLD+TLT unless named) | b, % per unit of z | t | Rows |
|---|---:|---:|---:|
| **Gate: acts z, no controls** | **-0.137** | **-1.02** | 2,166 |
| Threats z instead | -0.229 | -1.69 | 2,166 |
| Total index z instead | -0.225 | -1.69 | 2,166 |
| GLD / TLT alone | -0.118 / -0.156 | -0.70 / -0.95 | 1,083 each |
| SPY alone (shown only) | -0.115 | -0.64 | 1,083 |
| Post-paper years 2020-01 .. 2025-10 | -0.163 | -0.55 | 600 |
| With past 4/13/26/52-week returns | -0.135 | -1.00 | 2,120 |
| 1-week horizon | +0.001 | +0.01 | 2,168 |

- **No safe-haven premium after geopolitical acts**, not in the full span, not after the paper,
  not for either asset alone. Every 4-week cut is negative; the theory point in the prior (a
  safe asset is insurance and should earn *less* when risk is high) fits the sign, but nothing
  reaches |t| 1.7, and the threats cell (the story said "priced on the day", so near zero) is
  no different from the acts cell.
- **The placebo null is centred below zero:** median placebo t -0.96, so the true t is exactly
  ordinary (z against the placebo scale -0.05). Shifted GPR calendars "predict" lower safe-haven
  returns about as well as the true one: what the index shares with GLD/TLT is slow regimes, not
  a weekly dose.
- **F2 on paper, a slow link in the data:** acts z is lower after GLD/TLT have rallied over 26
  and 52 weeks (slopes -1.32 and -0.94 z per unit of log return, t -2.96 and -2.81; at 4 weeks
  0.00). Newspapers do not read gold prices; the link is coincident regimes (the 2022 war
  started in the year bonds fell most). The controls cell shows it does not move b.
- **Null width: SD of placebo t 1.11, 12% with |t| >= 2**, quantiles 5/50/95% -2.37 / -0.96 /
  +0.99, extremes -2.74 / +1.68.
- My guess (t -1 to +1.5, middle rank, placebo sd 1.0-1.4, feedback weak, pass 1%) held on t,
  rank and width; the feedback guess was wrong (|t| near 3 at 26-52 weeks).

### W26 `failure-premium`: fails

**One unit of ln(1 + failed assets) goes with -0.059% on XLF over the next 4 weeks, controls
for XLF's past 4/13/26/52-week returns (t -0.48, 1,344 weeks, 2000-01 .. 2025-10): the wrong
sign; the true t ranks 21 of 41 (empirical one-sided p 0.51). Dead by the gate: no card, no
strategy.** Held-out year untouched.

| Cut (4-week return from the Monday close after the failure week) | b, % per unit of x | t | Rows |
|---|---:|---:|---:|
| **Gate: XLF, four controls** | **-0.059** | **-0.48** | 1,344 |
| Without the controls | -0.061 | -0.45 | 1,344 |
| Failure-week dummy instead of x (% per failure week) | -0.201 | -0.30 | 1,344 |
| Year 2023 dropped | -0.073 | -0.57 | 1,292 |
| SPY instead | -0.023 | -0.25 | 1,344 |
| TLT / IEF instead (idea 3, F1 fails; shown only) | +0.122 / +0.056 | +1.72 / +1.68 | 1,158 each |
| Monday reaction, XLF (Friday close to Monday close) | -0.071 | -1.59 | 1,344 |
| 1-week horizon | +0.037 | +0.61 | 1,344 |

- **No distress premium in bank equity after failures.** A failure week of median size changes
  XLF's next 4 weeks by about -0.3%, t -0.5; neither the dummy nor the cut without SVB's spring
  changes that.
- **F2 confirmed, and it shapes the null:** failures follow bank-stock falls (x on XLF's past
  52-week return: slope -2.37, t -3.87; 4-26 weeks t -1.2 to -1.5), so the *future-dose* placebos
  (negative k: next year's failures against this month's XLF return) are strongly negative
  (down to t -4.37 at k = -91) while past-dose shifts sit near +0.6. The null is wide and skewed:
  **SD of placebo t 1.63, 25% with |t| >= 2**, quantiles 5/50/95% -3.26 / -0.71 / +1.21,
  extremes -4.37 / +1.56; the true t is ordinary (z +0.14).
- **The TLT and IEF cells (t +1.72 / +1.68) are noted only, not a lead:** idea 3's flight to
  quality fails F1 (the failure is public before the window), the cells are 2 of 8 shown in a
  design whose null has SD 1.63, and by `gate-null.md` step 6 they would need their own placebo
  before anyone writes "lead". wide-13 does not run it (a second look after a fail is a
  forking-paths pick).
- My guess (t -1.5 to +1.5, middle rank, placebo sd 1.2-1.8, feedback below -3 at long horizons,
  pass 1%) held on all four counts; the feedback was below -3 only at 52 weeks.

### Card note, 2026-11-19 03:15 UTC, written AFTER both gates had run: review-2's flaw in the null

While this write-up was being finished, the night lead relayed review-2 (draft PR #119,
`research/reviews/review-2.md` on branch `review-2`) on `gate-null.md`: (1) placebos that move
the dose *later* than the true one can overlap the outcome window and lean one way (W22's showed
it), so placebos should use only earlier doses (or year shifts / a swap design); (2) step 7,
stretching a 40-placebo rank into a z read at p 1e-4, is invalid; (3) a gate with about ten
independent episodes or fewer can only kill an idea, never pass it. Both gates had already run
as carded; the card is not changed. Both readings are reported:

| Gate | True t | Carded null: rank of 41 (p) | Earlier-dose placebos only (k = +27 .. +103, 20): rank of 21 (p) | Earlier-only null: SD, median, 5%-share with \|t\| >= 2, range |
|---|---:|---|---|---|
| W25 `act-haven` | -1.02 | 21 (0.51) | 16 (0.76) | 0.97, -0.26, 5%, -2.36 .. +0.98 |
| W26 `failure-premium` | -0.48 | 21 (0.51) | 21 (1.00): every earlier-dose placebo is above it | 0.48, +0.61, 0%, -0.18 .. +1.56 |

(Read from the stored placebo tables in `results/act-haven.md` and `results/failure-premium.md`;
no rerun.) **Neither verdict changes: both t are of the wrong sign, so no null can make them
pass.** What changes is the null's shape: for W26 the later-dose placebos (next year's failures
against this month's XLF) carried all the wide negative tail (to -4.37), exactly review-2's
point; the earlier-dose null alone is narrow (SD 0.48) and centred at +0.61. For W25 the
earlier-dose null is near normal.

Labels under point (3): **W26 is a kill-only gate** (its 268 failure weeks sit in about two
episodes, 2008-2012 and 2023, plus scattered single failures); **W25 is kill-only too** to be
safe (the acts index is dominated by perhaps 10-15 war and terror episodes since 2005). Both
results are kills, which is what such gates can deliver. Point (2): the card's "on a pass"
reading (z = (t - placebo median) / placebo sd at p < 0.00119 and 1.0e-4) was step 7 and is
withdrawn; it was never used, since neither gate passed. The z values printed in the result
files are descriptive only.

## Family count and status

Two mechanisms added and closed by their gates (W25 `act-haven`, W26 `failure-premium`; W numbers
follow wide-12's W24; if a parallel lane used them, the names decide).

**Count, reconciled with the branches visible on 2026-11-19 03:05 UTC:** wide-12 (branch
`wide-12`) 81 mechanisms, 18 tested by a strategy, 16 gates; weather-1 (branch `weather-1`)
gated one more without a W number (`hdd-gas`, failed, one `screen` row): 82 and 17 gates;
weather-2 (branch `weather-2`) has carded a CPC outlook-revision gate but posted no result yet,
so it is not counted here. **Union count: 84 mechanisms (82 + W25 + W26), 18 tested by a
strategy, none passed; 19 gates, all failed.** (The lead's "~80 / 19 tested" reads as gates, not
strategy tests: no branch has a 19th strategy test.) The next strategy test is read at
**p < 0.10 / 84 = 0.00119** (family) and the register's bar (N_eff 486: z >= 4.69, +0.30 to
+0.56 Sharpe over `tsmom12`, Bonferroni p <= 1.0e-4). Published effects after publication: still
0 for 10 (neither gate tested a published claim: the GPR index is published, the forward
safe-haven cut is not; the failure premium has no literature found).

Rows logged in `tries.md`: 2 (`act-haven`, `failure-premium`, kind `screen`, as weather-1 did).

## Next

1. **data-wide-1's sources are spent for now.** After this run no idea on the four loaded sources
   scores 5 (2: 4, 3 and 6: filtered, 4: 3 and W23 in other words, 5: 4 and W15 in other words);
   the unloaded ones (9-11) score 4 and carry data limits (no publication dates for hacks,
   under 7 years for chokepoints, IMF gold never queried). None is worth a gate by wide-12's
   threshold.
2. **The MOF daily detail is not a tradable dose** (quarterly publication); only the monthly
   total is, and its channel died as W23. Its exact quarterly publication dates are still
   unchecked; nobody should build on `mof_daily_available_on` without checking them.
3. Both nulls again show the pattern of W21-W23: a dose that shares slow regimes with the asset
   (GPR) or follows its price at 6-12 months (failures) makes future-dose placebos lean one way.
   A gate whose dose has a known 52-week feedback should expect a skewed null and say so in the
   card (W26's did).
