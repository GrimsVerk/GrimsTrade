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
