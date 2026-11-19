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

## What came out

(Filled after the runs.)
