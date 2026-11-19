# Wide 12: four candidates designed against the filters, the top one gated

Research run wide-12, 2026-11-19. Branch `wide-12` (from `wide-11`), draft PR into `wide-11`.
Research only: fake money, public keyless data, no change to the gym, the daily runner or the
live strategies.

**Count carried in (wide-11):** union of the wide and survey lines, **79 mechanisms, 18 tested
by a strategy, none passed**; 14 gates, all failed. Family bar for the next strategy test
p < 0.10 / 79 = 0.00127. Project-wide (`git show origin/register-4:research/register/BAR.md`,
read 2026-11-19): **3,118 tries, N 1,032 for a new pick, Bonferroni p <= 4.8e-5** (effective
N 486 at the measured correlation, p <= 1.0e-4).

Method: every gate follows `research/gate-null.md` (placebo family fixed in the rule, 40
placebos, one code path for true and placebo, the rank decides, t >= 2 also required; rule,
script and tests pushed before any number; one dry run that prints counts only, then one real
run). A gate is descriptive: no `tries.md` row, no card, and it does not raise the tested count.

## Step 1. Candidates written against F1 and F2 (2026-11-19, before any data look)

wide-11 ended with one sentence for the next ideation: a new mechanism needs **an unscheduled
flow that does not answer price, or a premium whose dose does not follow price at any horizon
up to a year**. The four below start from that sentence. Fields checked against the list in
`wide-10.md` step 1 and W20-W22: international reserve management, survey methodology,
conflict studies and public debt management are not in it (W4, W9, W10 used Treasury data,
but as pharmacokinetics, queueing and control).

| # | Field x tool | Mechanism | Dose | Data (keyless) |
|---|---|---|---|---|
| D1 `custody-selling` | international reserve management x a reserve manager defending a currency | Foreign central banks keep most dollar reserves as Treasuries in custody at the New York Fed. To defend their currency they sell dollars, so they must sell Treasuries: a price-insensitive seller, unannounced (interventions are mostly secret), and persistent (a defence lasts weeks to months). Last month's net selling means selling continues, so Treasury prices should be lower over the next 4 weeks; net buying (reserve accumulation) the mirror | 4-week log change of marketable Treasuries held in custody for foreign official accounts (Fed H.4.1 memo item, Wednesday level, released Thursday afternoon), as a z against its previous 156 weeks | FRED series `WMTSECL1` (one CSV) |
| D2 `inflation-disagreement` | survey methodology x forecaster dispersion as a measure of uncertainty | Long bonds pay a term premium for inflation risk; the premium should be larger when inflation is more uncertain (Wright 2011, international panel). Disagreement among professional forecasters measures that uncertainty without using bond prices | Interquartile dispersion of next-year inflation forecasts in the Survey of Professional Forecasters, quarterly | Philadelphia Fed dispersion file (one xlsx) |
| D3 `geopolitical-premium` | conflict studies x a newspaper-count index | Rare-disaster risk premium: when the perceived chance of war is high, stocks are priced to earn more afterwards | Caldara-Iacoviello geopolitical-threats index | One xls file (no reader installed) |
| D4 `debt-maturity-supply` | public debt management x preferred habitat | The more duration the Treasury makes the public hold, the higher the bond risk premium (Greenwood and Vayanos 2014) | Maturity-weighted share of marketable debt, monthly | Fiscal Data monthly statement of the public debt (one endpoint, many pages) |

### Filters (wide-11 step 1, unchanged)

| # | F1 not announced | F2 not price-driven |
|---|---|---|
| D1 | **pass (a)**: the selling is not announced or scheduled; holdings are published only weekly, after the fact | **with controls (-1)**: reserve managers sell when their currencies weaken, which can coincide with rising US yields (falling bond prices) at slow horizons (2022: yen defence while US yields rose). The rule controls for the bond ETF's own past 4-, 13-, 26- and 52-week returns (every horizon up to a year, wide-11's lesson), and shows the feedback at each horizon |
| D2 | **pass (b)**: a premium | **pass**: forecasters answer inflation data, not bond prices (checked by a shown feedback cell in a gate) |
| D3 | **pass (b)**: a premium | **pass**: wars do not follow index prices |
| D4 | **pass (b)**: a premium | **with controls (-1)**: the Treasury lengthened its debt after 2009 when yields were low, a slow reaction to the rate level |

### Score (wide-10 rule, six points: cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1; F2 cost off)

| # | 1 cause | 2 dose | 3 post-sample | 4 power | 5 unseen | 6 not killed | F2 | Score | Prior |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| D1 `custody-selling` | 0 (defence is a policy choice) | 2 | 1 | 1 | 1 | 1 | -1 | **5** | 2% |
| D2 `inflation-disagreement` | 0 | 2 | 1 | 0 (about 64 quarters after the source sample) | 1 | 1 | 0 | **5** | 1.5% |
| D3 `geopolitical-premium` | 0 | 2 | 0 (source data run to about 2021 `[memory]`: under 8 years after) | 0 (judged on 4-week returns, about 60 blocks after the sample) | 1 | 1 | 0 | 4 | 1% |
| D4 `debt-maturity-supply` | 0 (maturity choice is policy) | 2 | 1 | 0 (monthly and very persistent: few swings) | 1 | 1 | -1 | 4 | 1% |

Notes on the points:
- D1 post-sample: the papers that read custody or foreign official flows against Treasury
  yields end before 2010: Bernanke, Reinhart and Sack, Brookings Papers 2004 (custody holdings,
  sample to about 2004 `[memory]`); Warnock and Warnock, Journal of International Money and
  Finance 28(6), 2009 (foreign flows, 1984-2005 `[memory]`); Beltran, Kretchmer, Marquez and
  Thomas, Journal of International Money and Finance 32, 2013 (foreign holdings and yields,
  sample to about 2007 `[memory]`). Judging years 2010-01 .. 2025-10: 15.8 train years.
  All three measure the contemporaneous level effect on yields; none tests whether last
  month's flow predicts next month's bond return. Power: about 820 weekly reports, 205
  non-overlapping 4-week blocks for each of two bond ETFs.
- D1 unseen and not killed: no file in the repo mentions custody holdings (searched
  2026-11-19). The `liquidity` family in `ideas.md` is the Fed's own balance sheet and M2, not
  foreign accounts.
- D2 post-sample: Wright, American Economic Review 101(4), 2011, panel to about 2009
  `[memory]`.
- D4 post-sample: Greenwood and Vayanos, Review of Financial Studies 27(3), 2014, sample to
  about 2005 `[memory]`.

**Pick:** D1 and D2 tie at 5. Tie-break by data fetches: D1 is one CSV from a keyless endpoint;
D2 is one xlsx and the repo has no xlsx reader (it would need a hand-written XML parse), so
**D1 is gated first (as W23), D2 second if time remains (as W24).** D3 and D4 stay parked
here (not in the count).

## Step 2. D1 `custody-selling` gate (enters the list as W23)

### Data access (checked 2026-11-19, before any number was cut by it)

The FRED web endpoints (`fredgraph.csv`, `/data/*.txt`) refuse automated fetches from this
machine (stream reset, timeout), and the FRED API needs a key. The same series comes keyless
from the Federal Reserve Board's Data Download Program as the whole H.4.1 release:
`https://www.federalreserve.gov/datadownload/Output.aspx?rel=H41&filetype=zip` (9.1 MB zip,
one SDMX XML of 127 MB; stored under the cache root of `research/macro.local.json` at
`fed-ddp/h41-2026-11-19/H41.zip`, sha256 in the cache's `manifest.jsonl`). Format probe before
this rule (series names, descriptions, observation counts and dates only, no value printed):
series `RESH4FG_N.WW`, "Memorandum Items: Custody Holdings: Marketable U.S. Treasury
securities: Wednesday level", weekly, 1,248 observations from 2002-12-18. Custody holdings are
reported at face value, not market value `[memory]`; a shown cell checks that the weekly change
does not move with the same week's bond return (a market-value series would, mechanically).

### Decision rule (fixed and pushed before any number)

**Dose.** H(W) = custody holdings of marketable Treasuries on Wednesday W. Flow
f(W) = ln(H(W) / H(W - 28 days)), missing if either level is missing. z(W) = (f(W) - mean) /
sd (ddof 1) over the flows dated W - 1092 .. W - 1 days (156 weeks), needing at least 104;
past-only, so the trend growth of reserves in the 2000s is taken out. Predicted sign: positive
(net buying lifts bond prices over the next weeks; net selling lowers them).

**No look-ahead.** W's H.4.1 is released on Thursday W + 1 at 16:30 New York time (Friday in
some holiday weeks). Entry at the close of the asset's first bar dated >= W + 5 (Monday), exit
at the close of the first bar dated >= W + 33 (four weeks later). y(W) = ln(exit / entry),
dividend-adjusted closes (`harness.load_history("train")`). The row is dropped if either bar is
missing, the exit bar is dated after W + 40, or after 2025-11-10.

**Controls (F2), all horizons up to a year.** r_h(W) = ln(close of the last bar <= W / close of
the last bar <= W - h days) for h = 28, 91, 182, 364: the asset's own past 4-, 13-, 26- and
52-week returns, known at W.

**Panel and statistic.** Gate assets TLT and IEF (the two Treasury ETFs of the gym's data).
Pooled OLS: y = a_asset + b z + g4 r4 + g13 r13 + g26 r26 + g52 r52. t of b with
Driscoll-Kraay standard errors: scores summed over the rows of each Wednesday, then Newey-West
(Bartlett) with 4 lags over the week index (weeks counted by date; the 4-week returns overlap
by 3 weeks, and the two ETFs move together).

**Placebo null (the decider), one family, fixed here.** The same function with the dose
calendar moved by k weeks: z_k(W) = z(W - 7k days), outcome and controls stay put, rows with a
missing z_k dropped from that placebo only. k in +-{27, 31, ..., 103} (odd, step 4): **40
placebos** (wide-11's family: a 4-week flow z is persistent for months, so shifts under half a
year are left out; odd weeks are never a whole year).

**Gate. Pass only if both hold** (gate sample: Wednesdays 2010-01-06 .. 2025-10-01, after every
cited sample):
1. b > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41; empirical one-sided p = rank / 41 <= 0.049.

**Shown, not gating** (b, t, rows): without the controls; the 1-week horizon (exit at the first
bar >= W + 12, 1 lag); the raw flow f instead of z; TLT alone; IEF alone; SPY and GLD alone
(the dollar channel; not in the gate); the pre-gate years, Wednesdays 2005-01-05 .. 2009-12-30;
the F2 feedback check: z(W) on each past return r_h(W) alone (h = 4, 13, 26, 52 weeks), pooled
TLT and IEF with asset intercepts, Driscoll-Kraay 4 lags (positive slope = holdings grow after
bond rallies); the face-value check: the weekly flow ln(H(W) / H(W - 7)) on TLT's return over
the same week, 1 lag; the placebo null's width (gate-null step 5).

**On a pass:** no card in this run. A proposed card for the next window (TLT and IEF held or
scaled by z inside `tsmom12`'s bond slots on the Monday-after clock), read at the family bar
p < 0.10 / 80 = 0.00125 and the register's p <= 4.8e-5 (N 1,032) with z = (t - placebo median)
/ placebo sd. **On a fail:** W23 dead by the gate, no card, no row.

**Power, written before any number.** 4-week returns: TLT sd about 4%, IEF about 1.8%. About
820 weeks, two correlated ETFs (say 1.3 effective), overlapping by 3 weeks: standard error of
b roughly 3% / sqrt(820 x 1.3 / 4), about 0.18% per unit of z. The cited level effects (about
80 bp on the 10-year yield per $100 bn a year, Warnock and Warnock `[memory]`) suggest a
one-sd 4-week flow moves the 10-year yield by several bp in the same month; if a quarter of
that carries into the next month, b is about 0.2-0.3%: t about 1-1.5. Only a carry-over as large
as the same-month effect passes.

**My guess before any number.** b small and positive, t between -1 and +2; rank in the top
half; placebo t sd 1.1-1.5. Feedback: positive at 13-52 weeks (holdings and bond prices both
fall when the dollar is strong and US yields rise), t 1-3. Face-value check: slope near zero.
Chance of a pass: 3%.
