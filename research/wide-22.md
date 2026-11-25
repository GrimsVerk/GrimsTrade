# Wide 22: thirteen mechanisms from energy systems, queueing / reliability, network science, information theory, game theory, law, transport, demography and neuroscience, scored before any price, the top one gated

Research run wide-22, 2026-11-25 (night run, WIDER lane). Branch `wide-22` (from `main`
d84fe39), PR into `main`. Research only: fake money, keyless public data, no change to the gym,
the daily runner or the live strategies. Train only: no bar, index value or usage month after
2025-10-31 is used.

Fields already mined by earlier lanes are left out: physics, signal processing, control and
networks of prices (wide-18), meteorology, actuarial science, operations research (wide-19),
biology, ecology, epidemiology, climate (wide-17), economic history, demography of age
structure, psychology, sociology, linguistics of word counts (wide-20, panic-words-1),
hydrology, oceanography, solar physics, chemistry, materials (wide-21), public finance and
administrative law (wide-15). A parallel lane (`survey-8`) reviews finance literature tonight;
this lane stays with mechanisms whose dose comes from a non-finance field.

**Count carried in** (`gate-null.md` count note after W35): **103 mechanisms, 29 tested by a
strategy, none passed; 30 gates, one kill-only pass (W32), killed by its replication R32.** As
in wide-12 .. wide-21, only mechanisms that get a gate or a strategy test enter the count.

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-25 01:16): **4,126 tries,
N 1,116 for a new pick; measured rho 0.55 gives N_eff 506: a new rule needs z >= 4.70 against
`tsmom12` (+0.31 close rule, +0.56 far rule), Bonferroni p <= 9.9e-5.** Family bar with this
run's gate: p < 0.10 / 104 = 0.00096.

Method as wide-21: wide-11's filters F1 (not announced: an unscheduled flow (a) or a premium
(b)) and F2 (not price-driven; passing only with controls costs 1 point), then wide-10's points
(structural cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1), plus keyless long
data, a size check and a duplicate check against the record. Gates follow `research/gate-null.md`
(40 placebos, the rank decides, t >= 2 also required, rule pushed before any number, one dry
run with counts only, then one real run). `[memory]` marks a literature fact not checked
tonight; `[search summary]` one read only as a web-search summary.

## Step 1. What the record already holds near these fields (skipped here)

Searched `research/` and `docs/` on 2026-11-25 for: electric, output gap, capacity util,
Federal Register, regulat, freight, Cass, World Cup, daylight, duration depend, Kingman, queue,
bathtub, hazard, patent, industrial production, vehicle miles, EIA, attention, habituat,
auction, blackout, power outage. Already done (not redone):

- Administrative law: `rule-intensity` (wide-15 X9, Federal Register counts, parked, score 4);
  `congress-workload` (W27, dead).
- Energy: `hydro-hash`, `curtailment-hash` (wide-15, crypto mining, filtered); EIA gas storage
  and HDD surprises (weather-1 `hdd-gas`, dead); nuclear outages inventoried by data-wide-1.
- Activity nowcasts read as news: `withheld-nowcast` (wide-15 X4) and `conception-lead`
  (wide-20 P6), both filtered F1. A nowcast form of any activity gauge is therefore filtered
  here too; only a premium form (b) can pass.
- Reliability / hazard: `trend-age` (wide-2, the hazard of a trend's age: a price transform).
- Networks of prices: absorption ratio (run 1, dead), `mst-length`, `centrality-tilt`,
  `spillover` (wide-16/18, dead or filtered).
- Attention: `attention-peak` (card on main), sports and DST mood (wide-8, wide-20 P7, dead or
  filtered).
- Output gap, capacity utilisation, electricity use: no card, gate or strategy in the record
  (macro-1's ML features included industrial production as one input among many).

## Step 2. Thirteen mechanisms, scored (2026-11-25, before any price was read)

**Disclosure.** Before this table two sources were probed for format only (no price, no return,
no statistic): EIA's Monthly Energy Review Table 7.6 CSV (row count, series codes, date range;
the first three annual rows of two series were printed) and the cached French monthly factor
file (date range only). A web search summary of Da, Huang and Yun (2017) was read.

### The mechanisms (cause story each)

- **E1 `grid-load-premium`** (energy systems x counter-cyclical risk premium). Industrial
  electricity use is a physical measure of how hot the economy runs; Da, Huang and Yun (JFQA
  2017) report that its year-on-year growth predicts US market returns with the negative sign,
  R-squared about 9% at one year, sample about 1956-2010 `[search summary]`. A premium story:
  a hot economy asks a low premium.
- **E2 `storage-premium`** (energy systems x theory of storage). Low natural gas storage
  against its five-year norm raises the futures risk premium (Gorton, Hayashi and Rouwenhorst
  2013 `[memory]`); UNG should earn more after deficits. EIA weekly storage is keyless.
- **E3 `blackout-cascade`** (power-grid networks: cascading failures, DOE OE-417 disturbance
  reports). Large unscheduled outages as a productivity and mood shock for a few days.
- **Q1 `kingman-bottleneck`** (queueing theory). Kingman's formula: waiting time grows like
  u / (1 - u) as utilisation u nears 1; capacity utilisation (Fed G.17) near its ceiling means
  supply delays and inflation pressure explode nonlinearly, so bonds and stocks fall after high
  utilisation.
- **R1 `expansion-hazard`** (reliability engineering, Weibull wear-out). If the hazard of a
  recession rises with the age of the expansion, an old expansion carries a higher crash risk.
- **N1 `epidemic-threshold`** (contagion on graphs). The SIS epidemic threshold is 1 / lambda_max
  of the contact graph; a market correlation network with a large top eigenvalue spreads
  shocks: lower returns after it rises.
- **I1 `rate-distortion-attention`** (information theory: rational inattention, channel
  capacity). When non-financial mega-news (wars abroad, disasters, sports finals) fills
  investors' channel, market news is absorbed late (Peress and Schmidt 2020 on news pressure
  and retail trading `[memory]`): a delayed index reaction.
- **G1 `debt-ceiling-attrition`** (game theory, war of attrition). Standoffs before a debt
  ceiling X-date: a premium for a small default risk that peaks before the deadline.
- **G2 `auction-winners-curse`** (mechanism design). Treasury auction sizes and tails: a
  concession before large auctions.
- **T1 `freight-gauge`** (transport / logistics). Rail carloads or freight shipments as a
  physical output-gap gauge; the same premium story as E1 with another meter.
- **D1 `prime-age-inflow`** (demography). Inflows of prime-age workers raise savings and
  stock demand (Geanakoplos, Magill and Quinzii 2004 `[memory]`).
- **H1 `frost-crop`** (agronomy beyond drought). Hard freezes (Florida citrus, winter wheat)
  as food-price shocks.
- **B1 `habituation`** (neuroscience, stimulus-specific adaptation). The response to a
  repeated stimulus fades; the market's reaction to the k-th shock of a kind (rate hikes, bank
  failures) should shrink with k, so late shocks in a series are underpriced.

### Score

| # | F1 not announced | F2 not price-driven | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| E1 `grid-load-premium` | pass (b): a premium earned on a public statistic (a nowcast form, which would predict b > 0, is the filtered `withheld-nowcast` kind) | pass: factories do not set power use by stock prices; prices lead output, so earlier-only placebos and a feedback cell | 1 (counter-cyclical premium; the physical meter cannot be revised away) | 2 (growth from -15% to +10%) | 1 (2011-2025 after the paper's sample; JFQA 2017) | 1 (about 615 months; about 10 swings: kill-only) | 1 (no output-gap gate in the record) | 1 (not killed in the literature as far as I know) | 0 | **7** | 5% |
| E2 `storage-premium` | pass (b) | with controls: injections answer the futures spread | 1 | 2 | 1 | 0 (UNG 2007-2025: about 5 deficit episodes) | 1 | 1 | -1 | 5 | 2% |
| E3 `blackout-cascade` | pass (a) | pass | - | - | - | - | - | **dead class**: the mood-shock channel died in W31 (`air-disaster-mood`); size: a regional outage of a day is far below an index move | - | - | filtered (dead class) |
| Q1 `kingman-bottleneck` | **fail** as an inflation-flow story (G.17 is a scheduled release read as news); as a premium it is E1 with a survey meter | pass | - | - | - | - | - | **duplicate of E1's channel** (Cooper and Priestley's output gap, which Da et al. compare against) | - | - | filtered (duplicate) |
| R1 `expansion-hazard` | pass (b) | pass | - | - | - | - (about 12 post-war expansions) | - | **dead (literature)**: no positive duration dependence in post-war US expansions (Diebold and Rudebusch 1990; Diebold, Rudebusch and Sichel 1993; Rudebusch 2016 `[memory]`) | - | - | dead (literature) |
| N1 `epidemic-threshold` | pass (b) | **fail**: the graph is built from return correlations | - | - | - | - | - | duplicate of the dead absorption ratio (run 1) | - | - | filtered |
| I1 `rate-distortion-attention` | pass (a) | pass | - | - | - | - | - | data: news pressure (Vanderbilt archive) is not keyless; the documented effect is on retail volume, not index returns (size) | - | - | parked (data, size) |
| G1 `debt-ceiling-attrition` | **fail**: the X-date is published; four standoffs (2011, 2013, 2021, 2023) | pass | - | - | - | - | - | - | - | - | filtered |
| G2 `auction-winners-curse` | **fail**: sizes announced a week ahead (scheduled flow); and finance literature (`survey-8`'s field) | - | - | - | - | - | - | - | - | - | filtered |
| T1 `freight-gauge` | pass (b) | pass | - | - | - | - | - | **duplicate of E1** (same premium, another meter; keyless monthly freight series start about 2000) | - | - | parked (duplicate; joins E1's fate) |
| D1 `prime-age-inflow` | **fail**: the age structure is known decades ahead (as wide-20 P5 `my-ratio`) | pass | - | - | - | - | - | - | - | - | filtered (duplicate of P5) |
| H1 `frost-crop` | pass (a) | pass | - | - | - | - | - | **dead channel**: food-price inflation died in W32/R32; size: citrus and winter wheat are a tiny share of CPI | - | - | filtered (dead channel, size) |
| B1 `habituation` | pass (b) | **fail**: the dose is the market's own reaction to past shocks | - | - | - | - | - | - | - | - | filtered |

**Size check (shown, not part of the rule).** E1 is a premium story, not a flow, so the size
question is how much the premium can vary: the textbook equity premium moves by a few percent a
year over the business cycle (Fama and French 1989 `[memory]`), and Da et al.'s about -0.9% a
year per point of growth times a growth sd of about 4-5 points is about 4% a year per sd: large
but inside what premium-variation stories claim. E2 is also a premium; E3, H1 and I1 fail on
size or channel above.

**Picked by the rule.** E1 scores 7 (highest), with keyless monthly data from 1973 (EIA) and
US market returns from 1926 (French), and a fixed replication on an independent earlier
period (NBER electric power production 1919-, FRED keyless). **Gated: E1 as W36
`grid-load-premium`** (card `cards/wide-22.md`, pushed before any return was read; W36 is the
next free id after W35 on `main`'s `gate-null.md`, provisional since parallel lanes may take
it too; replication R36). E2 (score 5) is the next candidate: power 0 (about five storage-deficit
episodes on UNG) and the F2 cost; parked, not counted. Q1 and T1 are E1's channel with other
meters and share its verdict.

## Step 3. W36 `grid-load-premium` gate

The rule, data, placebo family, gate, the replication R36 (run only after a pass), shown cells,
power and guess are in [`cards/wide-22.md`](cards/wide-22.md), pushed before any number.
Code: `research/lib/wide22_events.py` (pure functions, tested offline in `tests/test_wide22.py`)
and `research/lib/wide22.py` (run, `r36`, `posthoc`). Results:
`research/results/grid-load-premium.md` (W36, with every placebo t),
`research/results/grid-load-premium-r36.md` (R36) and
`research/results/grid-load-premium-posthoc.md` (the post-hoc cells).

**Timing caveat (added at review, 2026-11-25):** the m+3 pairing rests on the Electric Power
Monthly's current release lag (month m out around the 24th-26th of month m+2); the MER's own
timing and the release lags of earlier decades (1970s-1990s) were not verified tonight. If old
releases came later than two months, the early rows hold up to a month or two of look-ahead in
the dose (the data are also today's vintage, not real time; card, "Data").

### Dry run (counts only, 2026-11-25 21:12 UTC)

EIA file fetched once (`wide-22/2026-11-25/eia/T07.06.csv`, 599 kB): industrial and residential
sales 634 months each, 1973-01 .. 2025-10 (none later). French monthly market 1926-07 ..
2025-10. **Gate rows: 619 usage months 1974-01 .. 2025-07** (as the card says); placebo rows
516 .. 594; post-sample rows (2011-01 on) 175; surrogate run 622 months.

## What came out

### W36 `grid-load-premium`: passes the kill-only gate (one real run, 2026-11-25 21:13:15 UTC)

**One point more year-on-year growth in industrial electricity sales goes with -0.098% a month
on the US market's excess return three months later (-0.42% a month per sd of growth, sd 4.30
points; t -2.31, 619 months, 1974-2025); the true t ranks 1 of 41 earlier-dose calendars, and
the post-sample sign holds (2011-2025: b -0.225, t -2.53, 175 months). All four conditions
hold: PASS (kill-only).**

| Cell (French Mkt-RF of month m+3 unless named) | b, % a month per point | t | Rows |
|---|---:|---:|---:|
| **Gate: industrial sales growth, 1974-01 .. 2025-07** | **-0.098** | **-2.31** | **619** |
| (a) with controls (Mkt-RF of m+2, of m-9..m+2) | -0.099 | -2.46 | 619 |
| (b) paper's horizon, Mkt-RF m+3..m+14, NW 18 (% a year) | -0.50 | -1.29 | 608 |
| (c) inside the paper's sample, 1974-2010 | -0.074 | -1.52 | 444 |
| (c) after it, 2011-2025 (gate condition 4) | -0.225 | -2.53 | 175 |
| (d) common rows 1982-08 .. 2025-07 (rank 1 of 41) | -0.095 | -1.93 | 516 |
| (e) negative control: residential sales growth | -0.029 | -1.04 | 619 |
| (h) SPY / TLT / GLD / BTC, log return of month m+3 | -0.046 / +0.028 / +0.002 / -1.37 | -0.67 / +0.49 / +0.04 / -1.82 | 393 / 279 / 251 / 165 |

- The size matches the paper: -0.098% a month is about -1.2% a year per point, against the
  published -0.9% `[search summary]`, and my card's power guess (t about -1.7 at full size) was
  slightly pessimistic.
- **The null is narrow and centred** (SD of placebo t 0.91, 2% with |t| >= 2; 5/50/95%
  -1.38 / -0.44 / +1.40; extremes -1.54 / +2.06). The phase-randomised surrogates (shown) are
  wider (SD 1.10, 10% past |t| 2, smallest -2.62) and rank the true t 3 of 41: by that family
  the rank would have been a near miss.
- **Feedback** (f): growth follows the market's past 24-month return (+0.053 per point of
  return, t +2.28), not its 12-month return (t +0.98): prices lead output, as expected; the
  earlier-only placebo family was the right choice, and the price controls in (a) do not change
  b.
- The negative control (residential, weather-driven growth) has the same sign at a third of
  the size (t -1.04): not zero, which is expected if part of residential use also follows the
  cycle, but a hint that part of the slope is generic.

Label: **kill-only** (gate-null step 7: about 10 independent swings in 1974-2025; smallest
p 1/41 = 0.024, far above the family bar 0.00096 and the register's 9.9e-5). By the gate-null
rule a pass is "not dead yet" and goes to its replication at once.

### Post hoc: where the W36 pass came from (added after both numbers; not a rule)

`wide22.py posthoc`, 2026-11-25 21:15 UTC (written to `results/grid-load-premium-posthoc.md`);
one `robustness` row in `tries.md`.

| Cell (post hoc) | b | t | Rows |
|---|---:|---:|---:|
| 2011-2025 without usage months 2020-2021 | -0.233 | -1.27 | 151 |
| 1974-2025 without usage months 2020-2021 | -0.084 | -1.82 | 595 |
| Usage months 1993-2025 (SPY's span) | -0.073 | -1.02 | 391 |
| Usage months 1993-2010 | -0.009 | -0.08 | 216 |

The slope's sign is stable, but its t leans on two episodes: the 1974-1992 years and the 2020
lockdown (industrial sales fell sharply in spring 2020 and rebounded a year later `[memory]`, while
the market fell and recovered). Over 1993-2010, eighteen years with two recessions, the slope is zero.
The post-sample t of -2.53 falls to -1.27 without 2020-2021. That is what a 10-swing design
gives: one large episode moves t by one unit.

### R36, the replication (card b, one real run, 2026-11-25 21:15:27 UTC): fails, W36 is dead

R36 as first written (`cards/wide-22.md`) was not runnable: FRED `M01128USM247NNBR` ends in
1938-12 (153 usable usage months, under the card's 240). `cards/wide-22b.md`, pushed after the
W36 number and before any R36 number (21:14:54 UTC), splices the NBER indicator's two FRED
variables (`M01128` to 1938, `M0128A` from 1939) on year-on-year growth and keeps the rest of
R36.

**R36: b -0.027% a month per point (-0.20% per sd of growth, sd 7.47 points), t -0.32, rank 13
of 41, usage months 1926-04 .. 1955-12, 357 rows. Fails: W36 is killed.**

| Cell | b, % a month per point | t | Rows |
|---|---:|---:|---:|
| **R36: spliced utility production growth, 1926-04 .. 1955-12** | **-0.027** | **-0.32** | **357** |
| Without the Depression, 1934-01 .. 1955-12 | -0.040 | -0.68 | 264 |
| P1 alone, 1926-04 .. 1938-12 | -0.081 | -0.57 | 153 |
| P2 alone, 1939-01 .. 1955-12 | -0.006 | -0.10 | 204 |

Null: earlier-dose placebos SD 0.55 (0% past |t| 2; 5/50/95% -1.36 / -0.14 / +0.60); phase
surrogates SD 1.10, rank 14 of 41. The sign is negative in every cut. Per point, the full-period
slope is about a quarter of W36's (-0.027 against -0.098), P1 alone about 83% of it (-0.081),
the cut without the Depression about 41% (-0.040) and P2 alone about zero (-0.006); per sd of
growth (7.5 points then, 4.3 since 1974) the full-period slope is about half of W36's.
My guess (b < 0, t between -2.5 and -0.5, rank 1-10, pass 30%) was right on sign and t, too
kind on the rank.

**Caveat on the kill:** the replication's meter is total utility production, not industrial
sales (the card says so), so it is a weaker test of the exact published dose; a pass there
needed about -0.17% a month per point (t -2 at its standard error of 0.085), 1.7 times W36's
slope and six times what it found. **R36 had little power** (computed after the run, not in
its card): at W36's slope per point the expected t was about -1.15 (power for t <= -2 about
20%), and at W36's slope per sd of growth about -0.66, because 1926-1955 monthly returns are
twice as volatile. So the kill follows the rule the card fixed, but it is a weak kill: the
replication neither confirms nor refutes the published size. Read together: the slope has the
predicted sign in 1926-1955, 1974-2010 and 2011-2025, but it is significant only where one
or two large episodes (1974-1992, 2020) carry it. That is the profile W32 / R32 had: a
persistent macro dose that passes one window on a narrow null and fades in the next.

## Family count and status

One mechanism added and closed by its gate and its replication (W36 `grid-load-premium`). The
twelve others are parked, filtered or dead in the literature and are **not counted**, as in
wide-12 .. wide-21; each has a `note` row in `tries.md` (no number computed) and a line in
`ideas.md`.

**Count: 104 mechanisms (103 carried in + W36), 29 tested by a strategy, none passed; 32 gates
(30 + W36 + its replication R36), two kill-only passes (W32, W36), each killed by its
replication (R32, R36).** The next strategy test is read at p < 0.10 / 104 = 0.00096 (family)
and the register's bar. #197 `fx-value-real-1` (merged tonight) is treated as part of #170's style-book mechanism (a
better currency-value definition for the same book), not a new mechanism, so 104 / 29 stands.
Published effects tested after publication: 1 more (Da, Huang and Yun
2017, industrial electricity growth): the post-sample slope keeps its sign but its t rests on
2020; dead by its replication (a low-powered one: see the R36 caveat). Ids W36 / R36 are provisional (parallel lanes tonight may take
W36 too; the lead renumbers).

Rows logged in `tries.md`: 2 `screen` (W36, R36), 1 `robustness` (post hoc), 12 `note` (one per
candidate scored but not gated). Data downloaded: 0.6 MB (EIA) + 8 kB (two FRED files).

## Next

1. **The output-gap premium class is parked with W36** (Q1 `kingman-bottleneck`, T1
   `freight-gauge`): they are the same channel with other meters. A later lane could test the
   class across countries (Da et al. also report Japan and the UK `[search summary]`), which is
   the only way to get more than about 10 independent swings, and the test R36 could not be; keyless monthly electricity data
   for other countries were not looked for tonight.
2. **Second kill-only pass, second replication kill.** Both passes (W32 drought, W36 grid load)
   were persistent monthly macro doses with a narrow earlier-or-shifted placebo null (SD 0.9-0.94)
   and both died on 30-40 earlier years. The phase-randomised surrogate family (used here as a
   diagnostic) was wider (SD 1.10) and would have ranked W36 3rd, a miss. Suggestion for
   `gate-null.md` (not adopted here, for the lead to decide): for a persistent macro dose,
   require the rank in both the shifted family and a phase-surrogate family.
3. **E2 `storage-premium`** (gas storage deficit, UNG) is the best parked candidate (score 5),
   but has about five deficit episodes: kill-only with little power; skip unless a lane can pool
   several storable commodities.
