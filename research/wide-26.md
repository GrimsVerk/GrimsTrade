# Wide 26: fourteen mechanisms from agronomy, crop physiology, glaciology, hydropower, remote sensing, atmospheric chemistry, plant pathology, fisheries, wind and solar power, limnology, fire science, coastal flooding and livestock physiology, scored before any price, the top one gated

Research run wide-26, 2026-11-25 (night run, WIDER lane). Branch `wide-26` (from `main`
013bedd), PR into `main`. Research only: fake money, keyless public data, no change to the gym,
the daily runner or the live strategies. Train only: no bar or event after 2025-10-31 is used.

Angle of this lane: a slow, physically measured process (not news) that changes a real cost or
quantity for listed firms, with a lag the market may under-weight.

Fields already mined are left out (from the headers of `wide-1` .. `wide-24` and wide-25's
list): physics, signal processing, control, information theory, networks of prices; ecology,
epidemiology, immunology, neuroscience, queueing, reliability; pharmacokinetics, seismology,
actuarial science, materials, metrology, astronomy, chronobiology, hydraulics; demography,
calendars, tax law, catastrophe meteorology, heliophysics, release engineering, sport,
oceanography as climate indices (PDO, AMO, ENSO); procurement, agricultural economics (harvest
cash), securities law, real estate, payments; conflict, bank regulation, FX intervention;
public finance, administrative law, legislative studies, power systems as curtailment and
hash rate, hydrology x mining (wide-15); biology, climate (temperature, outbreaks, monsoon and
gold, drought as inflation, heat and labour, smoke, pollen; wide-17); meteorology, operations
research (wide-19); economic history, psychology, sociology, word counts (wide-20); hydrology
and river freight (Mississippi), volcanology and stratospheric aerosols, solar physics,
chemistry (wide-21); energy systems (grid load, gas storage, blackouts), freight, game theory,
frost on crops (wide-22); cybercrime, courts, news novelty, cloud outages, influenza, soil
moisture as food prices (wide-23); seismology as damage, supply networks, sport, mega-events,
shipping, livestock epidemics, supply-chain pressure, critical minerals, extreme values
(wide-24); and wide-25 (running in parallel, `origin/wide-25` read 2026-11-25 23:04 UTC):
comparative politics, air quality, software engineering, night lights, process safety, rail
traffic, recalls, Beige Book tone, quantum risk. Mechanisms scored there are not scored again.

**Existing weather, drought and grid gates, whose channels are not duplicated:** W32
`drought-inflation` (contiguous-US PDSI on TLT, an inflation-risk premium; kill-only pass,
killed by R32 on 1962-2002 yields; its food-CPI cell had the wrong sign), W36
`grid-load-premium` (industrial electricity sales on the market, killed by R36), weather-1
`hdd-gas` and weather-2 `cpc-revision` (heating-degree surprises on natural gas, dead), W19
`enso-commodity` (ENSO on commodities, dead), W15 `cat-claims` (hurricanes on bonds, dead),
W40 `quake-drift` (disaster damage on country indices, dead). The channel gated here (a crop
input-cost shock to one industry's margins, relative to the market) is none of these.

**Count carried in** (provisional, after #215): **108 mechanisms, 29 tested by a strategy,
none passed; 36 gates, two kill-only passes (W32, W36), each killed by its replication (R32,
R36).** As in wide-12 .. wide-25, only mechanisms that get a gate or a strategy test enter the
count.

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-25 22:31): **4,328 tries,
N_eff 509 (measured rho 0.55): a new rule needs z >= 4.70 against `tsmom12`, Bonferroni p <=
9.8e-5.** Family bar with this run's gate: p < 0.10 / 109 = 0.00092 (0.10 / 110 = 0.00091 if
wide-25's W41 lands first).

Method as wide-21 .. wide-24: wide-11's filters F1 (not announced: an unscheduled flow (a) or
a premium (b)) and F2 (not price-driven; passing only with controls costs 1 point), then
wide-10's points (structural cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1),
plus keyless data, a size check and a duplicate check against the record. Gates follow
`research/gate-null.md` (40 placebos, the rank decides, t >= 2 also required, rule pushed
before any number, one dry run with counts only, then one real run). gate-null-2's proposed
"both families" rule applies when the dose's lag-1 autocorrelation is 0.8 or more; the card
says whether it does. `[memory]` marks a literature fact not checked tonight.

## Step 1. What the record already holds near these fields

Searched `research/` and `docs/` on 2026-11-25 for: Hong, food industry, food stock, Food,
snowpack, SNOTEL, reservoir, hydro, NDVI, curtail, fisher, salmon, pest, wildfire, corn,
Schlenker, cocoa, hail, sea level, wind drought, 49 industries, Agric. Found:

- **Drought**: W32 / R32 (above). wide-23 C12 `soil-moisture` and wide-22 H1 `frost-crop` were
  filtered as "dead channel": both were scored as food-price (CPI) stories, which W32/R32's
  food-CPI cell does not support. No gate or card on food or farm **stocks**; "food industry"
  and "food stock" have no hit, and Hong, Li and Xu (2019) is not cited anywhere.
- **Hydro**: wide-15 X6 `hydro-hash` (Sichuan wet season and bitcoin hash rate, filtered) and
  X7 `curtailment-hash` (Texas miners); wide-17 Y3 `monsoon-gold`. "reservoir" hits are W2
  `tax-drain` (a metaphor). No snowpack, SNOTEL or hydro-generation idea.
- **49 industries**: used by gsy-1 (bubble run-ups), cached under `french-gsy/`. No industry
  gate on a physical dose.
- **Fisheries**: wide-21 S4 `pdo-regime` mentions fisheries as a PDO effect (scored 3).
- Snowpack, NDVI, salmon, wildfire, Schlenker, cocoa, hail, sea level, wind drought: nothing.

## Step 2. Fourteen mechanisms, scored (2026-11-25 23:08 UTC, before any price was read)

**Disclosure.** Before this table, format only (no price, no return, no dose statistic): the
nClimDiv state readme (region codes; NCEI robots.txt read first) and the column names and
first/last months of Ken French's 49-industry file (fetched 2026-11-25 23:06 UTC; robots.txt
read first). Details and hashes in `cards/wide-26.md`.

### The mechanisms (cause story each)

- **H1 `drought-food-margin`** (agronomy x food-processor margins). Corn Belt drought cuts corn
  and soybean yields; feed, sweetener and oil inputs cost more; food processors and meat
  packers, hedged months ahead, see margins fall with a lag. Hong, Li and Xu (Journal of
  Econometrics 2019 `[memory]`): a country's drought trend predicts lower food-industry
  profitability and returns, read as under-reaction. Tradable form: the US food industry's
  beta-adjusted return in the quarter after the drought is posted.
- **H2 `heat-yield`** (crop physiology: Schlenker and Roberts, PNAS 2009 `[memory]`: corn and
  soy yields fall steeply with degree days above 29-30 C). The same input-cost channel with a
  sharper meter (July-August extreme heat in the Corn Belt).
- **H3 `snowpack-hydro`** (glaciology / snow hydrology). The 1 April snow-water equivalent in
  the Pacific Northwest and California sets summer hydro output; a thin snowpack forces
  hydro-heavy utilities to buy replacement power.
- **H4 `reservoir-power`** (hydropower). Low reservoir storage in hydro-heavy systems (Brazil's
  ONS, New Zealand, the Nordic pool) raises power prices and, in the worst years, rationing
  (Brazil 2001).
- **H5 `ndvi-crop`** (remote sensing of vegetation: satellite greenness as a yield nowcast ahead
  of the USDA's crop reports).
- **H6 `ozone-yield`** (atmospheric chemistry: tropospheric ozone cuts soybean and wheat yields
  by several percent in high-ozone summers `[memory]`).
- **H7 `crop-pest`** (plant pathology and entomology: citrus greening, wheat stem rust, fall
  armyworm spread as slow supply shocks).
- **H8 `sst-fishery`** (ocean temperature and fisheries: warm water cuts the Peruvian anchovy
  catch and fishmeal supply; sea temperature and lice set farmed-salmon harvests).
- **H9 `wind-drought`** (wind-resource meteorology: a low-wind year, Europe 2021, cuts wind
  farms' output and the owners' earnings).
- **H10 `solar-curtailment`** (power systems: midday solar curtailment in California as lost
  revenue for renewable owners).
- **H11 `rhine-low-water`** (limnology / river levels: the Kaub gauge below about 80 cm forces
  part-loaded barges; BASF cut output in 2018 `[memory]`).
- **H12 `wildfire-liability`** (fire science: fuel dryness and wind raise the odds of
  utility-ignited fires, whose liability is revealed over months: PG&E 2017-2018, Hawaiian
  Electric 2023 `[memory]`).
- **H13 `sea-level-flooding`** (coastal flooding: rising high-tide flood days as a slow
  discount on coastal property; Bernstein, Gustafson and Lewis, JFE 2019 `[memory]`).
- **H14 `livestock-heat`** (animal physiology: heat stress cuts milk yields and poultry weights
  as a cost shock to meat and dairy processors).

### Score

| # | F1 not announced | F2 not price-driven | Cause | Dose | Post | Power | Unseen | Not killed | F1/F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| H1 `drought-food-margin` | pass weakly, as wide-24 Q1: neither a flow nor a premium; rests on slow revelation of a cost shock through earnings | pass: weather does not follow stock prices | 1 (grain inputs, hedged with a lag) | 2 (PDSI, a graded index) | 1 (Hong-Li-Xu's sample ends about 2015 `[memory]`) | 1 (monthly 1960-2025, about 10-15 drought episodes: kill-only; the 1930s and 1950s give an independent replication) | 1 (no food- or farm-stock gate; W32 used a drought dose for bonds) | 1 (W32/R32 killed the inflation-premium channel; the food-CPI cell's wrong sign speaks against pass-through, not against a margin squeeze) | -1 (weak F1) | **6** | 3% |
| H2 `heat-yield` | pass weakly (as H1) | pass | 1 | 2 | 1 | 1 | 1 | 1 | -1 | 6, but **same channel as H1** | parked: duplicate of H1's channel with a meter that needs daily station data (GHCN-daily, several GB); joins H1's fate |
| H3 `snowpack-hydro` | pass weakly (as H1); the NRCS water-supply forecasts are scheduled monthly releases | pass | 0 (**pass-through**: hydro-heavy utilities recover most replacement-power costs through regulated power-cost adjustment clauses `[memory]`) | 2 | 0 | 0 (one water year a year, about 40; a few firms that move together; firm prices not cached) | 1 | 1 | -1 | 4 | filtered (channel, power) |
| H4 `reservoir-power` | pass (a) | pass | 1 | 2 | 0 | **0** (dry-year crises: Brazil 2001, 2014-15, 2021; New Zealand 2001, 2003, 2008; the Nordic weight in OMX is small) | 1 | 1 | 0 | - | filtered (power) |
| H5 `ndvi-crop` | the yield news it nowcasts is scheduled (USDA Crop Progress weekly, WASDE monthly) | pass | - | - | - | - | - | **duplicate of H1's channel** | - | - | filtered (data: MODIS and VIIRS archives need an Earthdata login) |
| H6 `ozone-yield` | pass (a) | pass | 0 (size: a few percent of two crops, inside H1's noise) | 1 | 0 | 0 (no keyless long national ozone-season series by script `[memory]`) | 1 | 1 | 0 | - | filtered (size, data) |
| H7 `crop-pest` | pass (a) | pass | - | - | - | **0** (a handful of outbreaks, each on one crop) | - | - | - | - | filtered (power, reach) |
| H8 `sst-fishery` | pass (a) | pass | - | - | - | - | - | **duplicate**: the anchovy link is ENSO (W19 dead); salmon farmers trade in Oslo, not cached | - | - | filtered (duplicate, data) |
| H9 `wind-drought` | pass (a) | pass | 1 | 2 | 0 | **0** (about 15 years of large wind fleets, one dose a year; owners' prices not cached) | 1 | 1 | 0 | - | filtered (power, data) |
| H10 `solar-curtailment` | pass (a) | pass | - | - | - | 0 (CAISO data from 2014) | - | **no reach**: curtailment is a small share of owners' revenue and no listed sector tracks it | - | - | filtered (reach) |
| H11 `rhine-low-water` | pass (a) | pass | - | - | - | **0** (five or six low-water seasons since 2000) | - | **duplicate of wide-21 S3** `river-freight` (parked on size); gauge history not keyless by script `[memory]` | - | - | filtered (duplicate, power) |
| H12 `wildfire-liability` | pass (a) | pass | 1 | 1 | 0 | **0** (a handful of utility fires, single firms) | 1 | 1 | 0 | - | filtered (power) |
| H13 `sea-level-flooding` | pass (b) | pass | 1 | 0 (a smooth trend, no dose that swings) | 0 | **0** (a trend is one event) | 1 | 1 | 0 | - | filtered (power, no dose) |
| H14 `livestock-heat` | pass weakly (as H1) | pass | - | - | - | - | - | **same channel as H1** (processor input costs); no national heat-stress series by script | - | - | parked (duplicate of H1) |

**Size check (shown, not part of the rule).** H1: grains and oilseeds are a few percent of US
food processors' sales, meat packers' feed costs more (through their livestock suppliers), and
the 2012 drought lifted corn by about half `[memory]`. A cost rise of 2-3% of sales against
operating margins near 10% is a 20-30% hit to a year's profit for the most exposed firms, much
less for branded food. A quarter's beta-adjusted underperformance of 1-2% after a severe
drought would be at the top of what this allows; near zero after mild ones. H3 fails on
pass-through, H4, H7, H9, H11-H13 on events.

**Picked by the rule.** H1 scores 6, the only candidate at 6 with its own channel, keyless data
and enough episodes (H2 and H14 share its channel). **Gated: H1 as W43 `drought-food-margin`**
(card `cards/wide-26.md`, pushed before any return was read; ids W43 / R43 provisional: wide-25
takes W41/R41 and W42). The replication **R43** is fixed in the same card: the same rule on dose
months 1931-06 .. 1959-09 (the 1930s and 1950s droughts, no overlap with the gate's outcome
months). No second gate (W44 not used).

## Step 3. W43 `drought-food-margin` gate

The rule, data, placebo families, gate, the replication R43 (run only after a pass), shown
cells, power and guess are in [`cards/wide-26.md`](cards/wide-26.md), pushed before any number
(commit 0bf2770, 23:10 UTC). Code: `research/lib/wide26_events.py` (pure functions, tested
offline in `tests/test_wide26.py`) and `research/lib/wide26.py` (load and run). Results:
`research/results/drought-food-margin.md`.

### Dry run (counts only, 2026-11-25 23:12 UTC)

Corn Belt PDSI (nClimDiv 361): 1,570 months, 1895-01 .. 2025-10, no gap. **Gate rows 786 dose
months (1960-01 .. 2025-06**; 2025-07 drops because its outcome would end after 2025-10); R43
rows 340. **Dose lag-1 autocorrelation 0.940**: above 0.8, so gate-null-2's "both families"
rule applies, as the card expected (pass needs rank <= 2 of 41 in the shifted calendars and in
the phase surrogates). Gate-row dose SD 2.48 PDSI units (the card's power guess used 2.5); 77
dose months at PDSI <= -2 and 27 at PDSI <= -4.

## What came out (one real run, 2026-11-25 23:13 UTC)

### W43 `drought-food-margin`: fails (no effect)

**One PDSI unit of Corn Belt drought goes with +0.009% for the US food industry's
beta-adjusted return over the quarter m+2 .. m+4 (Newey-West t +0.07, 786 dose months,
1960-2025), against the predicted negative sign; the true t ranks 22 of 41 shifted calendars
and 23 of 41 phase surrogates. Dead by the gate: no card for a strategy. R43 is not run** (the
card runs it only after a pass). Held-out year untouched.

| Cell (beta-adjusted Food, m+2 .. m+4, NW 3, dose months 1960-01 .. 2025-06, unless named) | b, % per unit | t | Rows |
|---|---:|---:|---:|
| **Gate** | **+0.009** | **+0.07** | **786** |
| Raw Food minus market (no beta) | -0.044 | -0.33 | 786 |
| W32's dose: contiguous-US PDSI (code 110) | +0.053 | +0.41 | 786 |
| Drying: PDSI(m-3) - PDSI(m), Corn Belt | -0.008 | -0.04 | 786 |
| 12-month horizon (m+2 .. m+13), NW 12 | +0.086 | +0.20 | 777 |
| Growing-season dose months only (Jun-Sep) | -0.121 | -0.49 | 261 |
| Restaurants (Meals) | +0.006 | +0.04 | 786 |
| Farms (Agric), no sign predicted | +0.103 | +0.61 | 786 |
| Equal-weighted Food | -0.122 | -1.19 | 786 |
| The market itself (Mkt-RF, m+2 .. m+4) | +0.246 | +1.59 | 786 |
| After Hong-Li-Xu: dose months 2016-01 on | -0.327 | -2.02 | 114 |

- **Nothing in the channel.** Every full-sample cell has |t| under 1.6; the signs split. The
  equal-weighted cell (smaller food firms, less able to hedge) leans the predicted way, t -1.19,
  within the null.
- **The driest months go both ways.** The ten driest gate months (results file) are 1964-01..03
  and 1977-02..07 and 2012-11: the quarter after is -2.8% .. +3.7% in 1964 and 1977, and
  **+14.6%** after November 2012 (the 2012 drought), when food
  stocks beat their beta handily instead of trailing it.
- **The post-sample cell (t -2.02, 114 months) is noted only, not a lead** (gate-null step 6). It
  rests on one episode: all 14 of its months at PDSI <= -2 lie in 2022-10 .. 2024-03. Run
  through the same two families after the main run (descriptive, shown here because its t
  crossed 2): rank 5 of 41 in the shifted calendars (null SD 1.49, 22% past |t| 2, min -3.99)
  and 2 of 41 in the surrogates (SD 1.47, 22%). A one-episode subsample with that null width is
  ordinary.
- **The null.** Shifted calendars: SD 1.10, 8% past |t| 2, 5/50/95% -1.68 / +0.03 / +1.52,
  extremes -2.28 / +2.02. Phase surrogates: SD 1.25, 15%, -2.13 / -0.07 / +2.06, extremes
  -2.97 / +2.65. Both centred; the surrogates are wider, as gate-null-2 found for persistent
  doses.
- **The market cell** (drought then the market rises, t +1.59) is W32's other half seen from
  stocks; noted only.
- **Power, measured.** SE(b) is about 0.13% per unit (b / t of the raw cell; the gate's t is too
  small to divide by), near the card's 0.14. A pass needed about -0.3% per unit, about -1.5% in
  the quarter after a severe drought; the true slope is +0.01 with a 95% interval of about -0.25
  .. +0.27. Effects as large as the size check allowed are unlikely; a 1% quarterly squeeze after
  the worst droughts is not ruled out.
- My guess (b near 0, t between -1.5 and +1, a middle rank, placebo SD 1.0-1.5, pass 3%) was
  right on every count.

Label: **kill-only** by `gate-null.md` step 7 (smallest p 1/41 = 0.024, above the family bar and
the register's 9.8e-5). A kill on its own t (+0.07, wrong sign).
Published effect tested after publication: Hong, Li and Xu (2019) `[memory]` in a US-only,
industry-level form (their test is a cross-country panel of drought trends): not reproduced.
