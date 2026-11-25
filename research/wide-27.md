# Wide 27: thirteen mechanisms from patent administration, research integrity, standard-setting, statistical agencies, open-data operations, central-bank research, spectrum management, aviation networks, postal systems, measurement standards and information science, scored before any price, the top gateable one gated

Research run wide-27, 2026-11-25 (night run, WIDER lane). Branch `wide-27` (from `main`
a4914b8), PR into `main`. Research only: fake money, keyless public data, no change to the gym,
the daily runner or the live strategies. Train only: no bar, vintage or event after 2025-10-31
is used.

Angle of this lane: mechanisms from **organisational and information processes** (how an
office, agency or standards body produces and releases information) rather than physical
ones, where the timing or quality of the information is set by the organisation, not by
prices.

Fields already mined are left out (from the headers of `wide-1` .. `wide-25`, and wide-26,
PR #223, open, `origin/wide-26` read 2026-11-25 23:25 UTC): physics, signal processing,
control, information theory, networks of prices; ecology, epidemiology, immunology,
neuroscience, queueing, reliability; pharmacokinetics, seismology, actuarial science,
materials, metrology, astronomy, chronobiology, hydraulics; demography, calendars, tax law,
catastrophe meteorology, heliophysics, release engineering (scheduled upgrades), sport,
oceanography; procurement, agricultural economics, securities law, real estate, payments;
conflict, bank regulation, FX intervention; public finance, administrative law (Federal
Register), legislative studies (roll calls), power systems, hydrology x mining; biology,
climate; meteorology, operations research; economic history, psychology, sociology, word
counts; hydrology and river freight, volcanology, solar physics, chemistry; energy systems,
freight, game theory, frost; cybercrime, courts, news novelty, cloud outages, influenza, soil
moisture; seismology as damage, supply networks, mega-events, shipping, livestock epidemics,
supply-chain pressure, critical minerals, extreme values (wide-24); comparative politics,
air quality, software engineering, night lights, process safety, rail traffic, recalls,
Beige Book tone, quantum risk (wide-25); agronomy, crop physiology, glaciology, hydropower,
vegetation remote sensing, ozone, plant pathology, fisheries, wind and solar resource,
limnology, fire science, coastal flooding, livestock physiology (wide-26). Mechanisms scored
there are not scored again.

**New fields tonight**: patent administration (grant flows and backlog), research integrity
(retractions), technical standard-setting, statistical-agency revision processes, open-data
operations (release blackouts), central-bank staff research, spectrum management, aviation
route networks, postal systems, measurement standards (statistical methodology changes) and
information science (attention, one duplicate).

**Count carried in** (provisional): `main` after #221 reads **109 mechanisms, 29 tested by a
strategy, none passed; 37 gates, two kill-only passes (W32, W36), each killed by its
replication (R32, R36).** wide-26 (#223, open) adds +1 mechanism and +2 gates if merged first.
As in wide-12 .. wide-26, only mechanisms that get a gate or a strategy test enter the count.

Project-wide bar (`research/register/BAR.md`, as quoted by wide-25 and wide-26: rows through
2026-11-25 22:31): **N_eff 509 (measured rho 0.55): a new rule needs z >= 4.70 against
`tsmom12`, Bonferroni p <= 9.8e-5.** Family bar with this run's gate: p < 0.10 / 111 = 0.00090
(0.10 / 110 = 0.00091 if #223 has not merged).

Method as wide-21 .. wide-26: wide-11's filters F1 (not announced: an unscheduled flow (a) or
a premium (b)) and F2 (not price-driven; passing only with controls costs 1 point), then
wide-10's points (structural cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1),
plus keyless data, a size check and a duplicate check against the record. Gates follow
`research/gate-null.md` (40 placebos, the rank decides, t >= 2 also required, rule pushed
before any number, one dry run with counts only, then one real run). gate-null-2's proposed
"both families" rule applies when the dose's lag-1 autocorrelation is 0.8 or more; **this
lane's card adopts it** (stricter than gate-null.md alone). `[memory]` marks a literature fact
not checked tonight.

## Step 1. What the record already holds near these fields

Searched `research/` and `docs/` on 2026-11-25 for: patent, retraction, peer review, 3GPP,
shutdown, funding lapse / funding gap, real-time / vintage, payroll, spectrum, postal / mail
strike, airline / aviation, Wikipedia / page view, archive, data uncertainty / noisy data /
measurement noise. Found:

- **Patents**: only a search term in wide-22's step 1; no candidate, no gate.
- **Government shutdowns**: only as dropped windows (info-1, wide-11 X1, wide-23): report dates
  inside the 2013 and 2018-19 shutdowns are removed from other tests. No shutdown or
  data-blackout mechanism.
- **Real-time vintages and payrolls**: ALFRED and Philadelphia Fed vintages are used to date
  macro inputs as the market knew them (`lib/macro.py`, macro-1, data-long-3/4, fx-value-real-1);
  `announcement-premium` (Savor-Wilson; scheduled releases, dead by event study) and wide-15
  X4 `withheld-nowcast` (payroll taxes as a nowcast) touch payrolls. **No mechanism uses the
  size of revisions themselves** (data quality) as a dose.
- **Wikipedia attention**: `attention-peak` (coin page views, dead, tested); wide-20 reads
  Wikidata only for event dates.
- "spectrum" hits are spectral analysis (gate-null, wide-1), "aviation" hits are W31
  `air-disaster-mood` (crash mood, dead), "archive" hits are data archives, "peer review" hits
  are the literature surveys. Retractions, standards bodies, postal systems: nothing.

## Step 2. Thirteen mechanisms, scored (2026-11-25, written before the card's commit at 23:29 UTC, before any price was read)

**Disclosure.** Before this table, format and coverage only (no price, no return, no dose
value): the sheet name, size and first/last vintage column of the cached Philadelphia Fed
`employmvmd.xlsx`; search-result titles for USPTO country-of-origin patent tables; HTTP status
codes of four USPTO PTMT pages (all 404 to a script, 2026-11-25 23:27 UTC, robots.txt read
first: only `/cgi-bin/`, `/includes/`, `/cybertraining/`, `/ebc/portal/`, `/images/` are
disallowed) and of two ALFRED patent series (connection reset, no data).

### The mechanisms (cause story each)

- **O1 `patent-surge`** (patent administration: grant flows). A country's US utility-patent
  grants (by the first inventor's residence) rise faster than its peers'; grants are public
  weekly in the Official Gazette, the aggregate is slow-moving and under-weighted. Firm-level
  analogues: Hirshleifer, Hsu and Li (JFE 2013, "innovative efficiency") and Cohen, Diether and
  Malloy (RFS 2013, "misvaluing innovation") `[memory]`. Tradable form: the country's market
  against the other developed markets in the year after the count is public.
- **O2 `grant-backlog`** (patent administration: pendency). The USPTO's backlog and examiner
  staffing set when innovation becomes a property right; a backlog shock delays grants for all
  firms at once.
- **O3 `retraction-wave`** (research integrity: Retraction Watch database). Waves of retracted
  papers in a field (oncology, Alzheimer's 2022) as a shock to firms built on that science.
- **O4 `standard-freeze`** (technical standard-setting: 3GPP release freezes, Wi-Fi and USB
  generations) as a demand cycle for the firms that build to the new standard.
- **O5 `data-blackout`** (open-data operations: appropriation lapses that stop federal
  statistics, 1995-96, 2013, 2018-19) as an information-uncertainty premium.
- **O6 `revision-noise`** (statistical-agency revision processes). Payroll employment is
  first published from an incomplete survey and revised twice more and at the benchmark; when
  revisions run large for a spell, the data investors read the state of the economy from are
  noisier. In learning models (Veronesi 1999; Pastor and Veronesi `[memory]`) noisier signals
  raise the uncertainty investors bear; if priced, the US market earns more afterwards. The
  noise comes from the agency's process (response rates, the birth-death model, benchmark),
  not from prices.
- **O7 `fed-research-tone`** (central-bank staff research: the count or tone of Fed working
  papers on a topic as a lead on policy).
- **O8 `spectrum-auction`** (spectrum management: FCC auction outcomes as a cost shock to
  carriers and a revenue shock to tower firms).
- **O9 `route-network`** (aviation route networks: new direct routes between country pairs as a
  lead on trade and tourism).
- **O10 `postal-disruption`** (postal systems: national mail strikes delaying payments and
  documents).
- **O11 `method-change`** (measurement standards: statistical methodology changes, hedonic CPI
  adjustments, BEA comprehensive revisions) as a shift in measured inflation or growth.
- **O12 `benchmark-revision`** (statistical agencies: the annual payroll benchmark, preliminary
  in August/September, final in February) as a revision of the economy's level.
- **O13 `wiki-attention`** (information science: Wikipedia page views as investor attention;
  Moat et al., Sci. Rep. 2013 `[memory]`).

### Score

| # | F1 not announced | F2 not price-driven | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| O1 `patent-surge` | pass (b): a slow state, public weekly in the Gazette, not a scheduled market event | with controls: patenting follows R&D, which follows booms and market levels | 1 (under-weighted innovation output, firm-level evidence) | 2 | 1 (country-level, after the firm papers' samples) | 1 (about 20 countries x 40 years, annual) | 1 | 1 | -1 | **6** | 2%; **parked: data** (USPTO PTMT country tables 404 to a script tonight; FRED's copies, release 486, unreachable: ALFRED reset the connection, fredgraph did not answer this machine before (data-long-3); PatentsView bulk tables over 1 GB). Data lead for a later lane |
| O2 `grant-backlog` | pass (b) | pass | 0 (no channel from pendency to index returns) | 1 | 0 | **0** (one US series) | 1 | 1 | 0 | - | filtered (cause, power) |
| O3 `retraction-wave` | pass (a) | pass | - | - | - | - | - | **no reach**: single papers, single firms; no index-level exposure | - | - | filtered (reach) |
| O4 `standard-freeze` | **fail**: release freezes are scheduled years ahead by the bodies | - | - | - | - | - | - | duplicate of release engineering (wide-9) | - | - | filtered (F1) |
| O5 `data-blackout` | pass (a) | with controls (shutdowns follow budget fights, not prices) | 1 | 1 | 0 | **0** (three or four data-stopping lapses in the train window) | 1 | 1 | -1 | - | filtered (power) |
| O6 `revision-noise` | fails as a flow (each revision arrives in a scheduled release); **passes as a premium (b)**: a state of data quality | with controls: revisions are larger in recessions and at turning points, when expected returns are high for other reasons | 1 (noisier state signals, priced uncertainty in learning models) | 2 (a graded size) | 0 (no return paper known to me) | 1, weakly (monthly 1990-2025, but a persistent dose: perhaps 30-40 independent stretches; earlier years free for replication) | 1 (no revision-size dose in the record) | 1 (the political-uncertainty premium is dead, W27 and W41; data-quality uncertainty is a different source, not tested) | -1 | **5** | 2% |
| O7 `fed-research-tone` | pass (b) | pass | 0 (staff papers do not set policy; no channel to returns) | 1 | 0 | 1 | 1 | 1 | 0 | 4 | 0.3%; no keyless dated corpus scored by script tonight |
| O8 `spectrum-auction` | the auction calendar is announced; outcomes are a flow | pass | 1 | 1 | 0 | **0** (about ten large auctions since 1994, one sector) | 1 | 1 | 0 | - | filtered (power, reach) |
| O9 `route-network` | timetables are filed months ahead | pass | - | - | - | - | - | - | - | - | filtered (data: OAG and similar route data are paid) |
| O10 `postal-disruption` | pass (a) | pass | - | - | - | **0** (a handful of national strikes in cached markets) | - | **no reach** at index level since electronic payments | - | - | filtered (power, reach) |
| O11 `method-change` | **fail**: methodology changes are announced well ahead | - | - | - | - | - | - | duplicate of metrology (wide-1 .. wide-6) | - | - | filtered (F1, duplicate) |
| O12 `benchmark-revision` | **fail**: the benchmark dates are scheduled; the preliminary estimate is a scheduled release | - | - | - | - | - | - | **same channel as O6** (benchmark months are inside O6's dose) | - | - | folded into O6 |
| O13 `wiki-attention` | pass (a) | **fail**: attention follows prices | - | - | - | - | - | **duplicate**: `attention-peak` (coin page views, dead, tested) | - | - | filtered (F2, duplicate) |

**Size check (shown, not part of the rule).** O6: the three-month US market excess return
has an SD near 8%; a learning-model premium would have to be of the order of 1-3% over three
months per SD of the noise state to be seen with a persistent dose; that is large for a
second-order data property, so the prior is low. O1 would need a few percent a year of
country excess return per SD of patent growth, in line with the firm-level spreads `[memory]`.

**Picked by the rule.** O1 scores highest (6) but is parked on data: no keyless,
script-readable country-by-year patent table answered tonight. O6 is next (5) and has keyless
data already cached, dated as the market saw it (the Philadelphia Fed's monthly vintages, each
as recorded in the middle of its month, after that month's payroll release), and earlier
years free for a replication. **Gated: O6 as W44 `revision-noise`** (card
`cards/wide-27.md`, pushed at 23:29 UTC before any return was read; W44 / R44 provisional: W42
is unused by wide-25, W43 is wide-26's in #223; the merging lead may renumber). The
replication **R44** is fixed in the same card: the same rule on rows 1976-01 .. 1989-09
(outcomes end before the gate's first). No second gate (W45 not used).

## Step 3. W44 `revision-noise` gate

The rule, data, both placebo families, gate, the replication R44 (run only after a pass),
shown cells, power and guess are in [`cards/wide-27.md`](cards/wide-27.md), pushed before any
number (commit f8f266f, 23:29 UTC; code and offline tests 4f6885f; steps 1-2 of this write-up
0f02a1f, 23:32 UTC, all before the real run). Code: `research/lib/wide27.py` (pure functions
tested offline in `tests/test_wide27.py`). Results: `research/results/revision-noise.md`.

### Dry run (counts only, 2026-11-25 23:31 UTC)

Vintages 1964-12 .. 2025-10 (731); the dose is defined 1975-12 .. 2025-07 (596 months; the
12-month mean and the 120-month trailing mean use up the first eleven years). **Gate rows 427
months (1990-01 .. 2025-07)**; every earlier-dose shift k = 25 .. 103 is defined on every row.
**Lag-1 autocorrelation of the dose 0.969** (as the card expected): the surrogate family
gates. |end - start| of the dose is 0.89 SD (under the card's 1 SD switch), so the
surrogates are plain phase-randomised, not IAAFT.

## What came out (one real run, 2026-11-25 23:32 UTC)

### W44 `revision-noise`: fails (no premium)

**In the three months after a spell of large payroll revisions the US market earned no more
than after a quiet spell: b +0.47% per unit of the dose (+0.17% per SD of the dose, SD 0.35),
t +0.24, 427 months 1990-2025. The true t ranks 23 of 41 among earlier-dose calendars and 19
of 41 among phase surrogates. Dead by the gate in both families: no card for a strategy. R44
is not run** (the card runs it only after a pass). Held-out year untouched. Table:
`results/revision-noise.md`.

| Cell (US Mkt-RF, % over three months from v+1, per unit of D; controls g12, s12, c12, c1; NW 3, unless named) | b | t | Rows |
|---|---:|---:|---:|
| **Gate** | **+0.473** | **+0.24** | **427** |
| Horizon 1 month (NW 0) | +0.244 | +0.26 | 427 |
| Horizon 6 months (NW 6) | +1.372 | +0.38 | 424 |
| Horizon 12 months (NW 12) | -0.224 | -0.04 | 418 |
| No controls | +1.531 | +0.95 | 427 |
| Without s12 | +0.873 | +0.61 | 427 |
| First revision only | +0.579 | +0.30 | 427 |
| Dose in levels (ln R12, no trailing mean) | +0.350 | +0.17 | 427 |
| Rows 1990-01 .. 2007-12 | +6.942 | +1.30 | 216 |
| Rows 2008-01 .. 2025-07 | -1.598 | -0.66 | 211 |

- **Nothing near a pass.** Every cell has |t| under 1.3. The controls take out about two
  thirds of the raw slope (no controls +1.53, t +0.95): what there is goes with the business
  cycle (revisions are larger when payroll growth is volatile, s12), as F2 warned.
- **The halves disagree** (1990-2007 +6.9, t +1.30; 2008-2025 -1.6, t -0.66). Not a lead: each
  half has perhaps 15-20 independent stretches of a dose with acf 0.97.
- **The two nulls.** Earlier-dose calendars: SD 1.03, 5% past |t| 2, 5/50/95% -0.93 / +0.53 /
  +1.89, extremes -1.17 / +2.20; short shifts (25-55 months) lean positive (k 25: +2.04, k 41:
  +2.20), long ones (59-87) negative: the persistent dose and the 1990s/2000s cycles give the
  shifted family a wave, as gate-null-2 describes for persistent doses. Phase surrogates are
  centred: SD 0.96, 3% past 2, 5/50/95% -1.26 / +0.09 / +1.50. The true t sits in the middle of
  both; the verdict does not depend on the family.
- **Power, measured.** SE(b) about 1.97% per unit of D, 0.69% per SD of D over three months,
  better than the card's guess (the card expected only a 2-3% premium per SD to be visible).
  One-sided upper 95% bound about +1.3% per SD over three months: a premium of a few percent a
  year per SD of data noise is not excluded, one of the size a pass needed (about 1.4% per SD
  over three months) is unlikely.
- **Event dates.** Vintage v is the Philadelphia Fed's mid-month record, after that month's
  first-Friday payroll release, and the outcome starts in month v+1: no publication-lag
  look-ahead. The 2013 and 2018-19 shutdowns delayed one or two releases; the vintage
  convention keeps the delayed values in the month they were public.
- My guess (b near 0, t between -1.5 and +1.5, middle ranks in both families, the shifted null
  somewhat wider than the surrogates, pass 3%) was right on all four.

Label: **kill-only** by `gate-null.md` step 7 (smallest p 1/41 = 0.024, above the family bar
and the register's 9.8e-5).

## Family count and status

One mechanism added and closed by its gate (W44 `revision-noise`). The twelve others are
parked (O1 on data, O7), filtered or folded and are **not counted**, as in wide-12 ..
wide-26; each has a `note` row in `tries.md` (no number computed) and a line in `ideas.md`.

**Count: +1 mechanism, +1 gate over the count carried in.** Against `main` after #221 (109 /
29 / 37): **110 mechanisms, 29 tested by a strategy, none passed; 38 gates, two kill-only
passes (W32, W36), each killed by its replication (R32, R36)**; if wide-26's #223 (+1
mechanism, +2 gates) merges first: 111 / 29 / 40. Gate id **W44 / R44 provisional** (W42 unused
by wide-25, W43 taken by wide-26; W45 not used); the summary lane reconciles. Family bar p <
0.10 / 111 = 0.00090. Published effects tested after publication: none new (no paper on a
revision-size premium in stock returns is known to me; the learning-model channel is
theory).

**Data terms.** Philadelphia Fed Real-Time Data Set for Macroeconomists, `employmvmd.xlsx`
(nonfarm payroll employment, monthly vintages; cached 2026-11-12 by an earlier lane under
`philly-rtdsm/2026-11-12/`, sha256
49553e6a60fa5e807f2039e4699400cfd407a51104b32ba670b7ba2260ce5437); the Federal Reserve Bank of
Philadelphia asks users to cite the data set (Croushore and Stark, Journal of Econometrics
2001 `[memory]`). Ken French Data Library `F-F_Research_Data_Factors_CSV.zip` (cached
2026-11-12). Only statistics are committed. No new download (the USPTO and ALFRED probes
returned no data).

Rows logged in `tries.md`: 1 `screen` (`revision-noise`), 9 `robustness` rows (the shown
cells), 12 `note` rows (one per candidate scored but not gated).

## Next

1. **O1 `patent-surge` is the best unmet candidate of this lane** (scored 6) and only needs
   data: a script-readable country-by-year table of US utility-patent grants by country of
   first inventor. FRED release 486 ("U.S. Granted Patents by States, Territories, and
   Countries") carries the series; try ALFRED/fredgraph again on another night (both refused
   tonight) and date each annual count by its first vintage. The test would be the country's
   market against the other developed markets in the twelve months after the count is public,
   kill-only, with an earlier-year replication.
2. **Data quality as a priced state is closed at this horizon in its simplest form** (payroll
   revisions, US market, three months). A GDP-revision version (`routputqvqd.xlsx`, also
   cached) would share most of the cycle confound and is not worth a separate gate.
3. **Method**: with a dose of acf 0.97 the shifted family showed a wave across shifts (k 25-55
   positive, 59-87 negative) while the phase surrogates were centred; another case,
   after W33 and W35, where the two families differ in shape but agree on the verdict.
