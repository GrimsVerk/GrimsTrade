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
