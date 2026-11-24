# Wide 17: twelve mechanisms from biology, ecology, epidemiology, evolution and agriculture/climate, scored before any price, the top two gated

Research run wide-17, 2026-11-24/25 (night run). Branch `wide-17` (from `main`), PR into
`main`. Research only: fake money, keyless public data, no change to the gym, the daily runner
or the live strategies. A parallel lane (wide-18) takes physics, engineering and information
theory; this lane stays in the life sciences and agriculture/climate.

**Count carried in** (`SUMMARY.md`, 2026-11-24): **88 mechanisms, 19 tested by a strategy, none
passed; 22 gates, all failed.** As in wide-12 .. wide-15, only mechanisms that get a gate or a
strategy test enter the count; the scored-but-parked ones are listed here and in `ideas.md`.

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-24 20:01): **3,855 tries,
N 1,083 for a new pick; measured rho 0.54 gives N_eff 500: a new rule needs z >= 4.70, an edge
over `tsmom12` of +0.31 (close rule) to +0.56 (far rule) in annual Sharpe on the primary test;
Bonferroni p <= 1.0e-4.** Family bar for the next strategy test after this run's gates:
p < 0.10 / 90 = 0.0011 (if both gates below are counted).

Method: every gate follows `research/gate-null.md` (placebo family fixed in the rule, 40
placebos, one code path for true and placebo, the rank decides, t >= 2 also required; rule,
script and tests pushed before any number; one dry run that prints counts only, then one real
run). **Train only, cut at 2025-10-31** (this night's lane rule; stricter than the harness's
2025-11-10): no bar, temperature or report dated after 2025-10-31 is read. Each gate gets one
`screen` row in `tries.md` (descriptive, not selectable), as wide-13 and wide-15 did.

## Step 1. What the record already holds in these fields (skipped here)

Searched `ideas.md`, `wide-1.md` .. `wide-16.md`, `weather-1.md`, `weather-2.md`,
`data-wide-1.md` on 2026-11-24 for: ecolog*, epidem*, evolution*, biolog*, immun*, crop,
harvest, drought, monsoon, temperature, pollen, smoke, sunshine, daylight, influenza, outbreak,
pandemic, margin, speciation, flicker. Already done (not redone):

| Field | Mechanisms already in the record |
|---|---|
| Ecology | `critical-slowing` (rising AC1/variance; gate wide-6, dead), `stablecoin-resource` (consumer-resource), predator-prey leverage (E4, killed), predator satiation (`auction-concession`), `patch-leaving` (marginal value theorem), `token-unlocks` (supply pulse), wide-16's portfolio effect, functional groups, Taylor's law, ideal free distribution |
| Epidemiology | `contagion-catchup` (graph SIR), `attention-peak` / `attention-sir` (SIR on page views), P3 sector SIR, P4 liquidation percolation, FluView flu above norm (wide-13 idea 8, filtered as news) |
| Evolution | `crowded-trend` (frequency-dependent fitness), replicator dynamics (G1), minority game (G3), hawk-dove (G4), wide-16's bet-hedging seed bank and phenotype switching |
| Immunology, neuroscience | negative and clonal selection, tolerance (M1-M3); prediction error, reference dependence (N1-N3) |
| Chronobiology | `lunar` (gate wide-6, dead) |
| Agriculture / climate | `enso-commodity` (ENSO -> crop yields -> DBC; W19, dead), `hdd-gas` (weather-1, dead), `cpc-revision` (weather-2, dead), `cat-claims` (W15, dead), `hedging-pressure` (Keynes-Hicks, W22, dead), `festival-gold` (Indian gold demand on festival dates; W13, dead), wide-15's hydro-hash and curtailment-hash (hash rate and power) |

## Step 2. Twelve mechanisms, scored (2026-11-24, committed 23:31 UTC in 455cb2d, before any price was read; first written as "about 23:45", a slip)

Scoring exactly as wide-13 and wide-15: wide-11's filters F1 (not announced: an unscheduled
flow (a), or a premium (b); mood, cognition and public news are neither, as wide-13 read
FluView) and F2 (not price-driven; passing only with controls costs 1 point), then wide-10's
six points (cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1). Data: keyless and
long enough for the power point. `[memory]` marks a literature fact not checked tonight.

**Disclosure.** Before this table two dose sources were probed for format only (no price, no
return, no statistic): NASA GISTEMP v4 `GLB.Ts+dSST.csv` (header and the 1880-1881 rows) and
the WHO Disease Outbreak News API (`www.who.int/api/news/diseaseoutbreaknews`: the three oldest
titles, first dated 2004-01-05, and the item count, 3,209).

### The mechanisms (real-world cause story each)

- **Y1 `temperature-premium`** (climate science x long-run risk). A warmer-than-recent-climate
  year is news that the climate is shifting faster, which raises expected damage to future
  output. If that risk is priced (Bansal, Kiku and Ochoa, "Price of long-run temperature shifts
  in capital markets", NBER 2016, sample to about 2012 `[memory]`; Balvers, Du and Zhao,
  Journal of Banking and Finance 2017, temperature shocks raise the cost of equity, sample to
  about 2015 `[memory]`), a warm shock lowers stock prices when it lands and raises the equity
  premium after it: SPY should earn more in the months after a warm shock. Dose: the 12-month
  mean of the global land-ocean anomaly minus its mean over the ten years before (NASA
  GISTEMP, monthly from 1880, keyless).
- **Y2 `outbreak-premium`** (epidemiology x rare-disaster risk). Each WHO Disease Outbreak News
  report is a new or growing outbreak somewhere (avian flu, MERS, Ebola, Zika, cholera). A
  burst of reports raises the chance of a pandemic, a rare economic disaster; in rare-disaster
  models (Barro, Quarterly Journal of Economics 2006; Wachter, Journal of Finance 2013
  `[memory]`) a higher disaster probability raises the equity premium, so SPY should earn more
  in the weeks after a burst. Donadelli, Kizys and Riedel ("Dangerous infectious diseases: bad
  news for Main Street, good news for Wall Street?", Journal of Financial Markets 2017, sample
  to about 2014 `[memory]`) found US pharmaceutical stocks rising on WHO alerts (a sector, same
  days); the forward market premium is not their test. Dose: weekly count of reports,
  variance-stabilised, minus its trailing-year mean (WHO's reporting practice drifts).
- **Y3 `monsoon-gold`** (agricultural climate x household income). Most of India's gold is
  bought by rural households out of harvest income; a monsoon above the long-period average
  means larger crops and more gold bought from October to January (World Gold Council demand
  notes `[memory]`). Dose: all-India June-September rainfall departure (IMD); GLD over the
  following winter should rise with it.
- **Y4 `drought-inflation`** (agronomy x inflation risk). Widespread US drought cuts crop
  yields and lifts food prices months later; bondholders demand an inflation-risk premium, so
  TLT should earn less (and GLD more) after drought spreads. Dose: the contiguous-US Palmer
  drought index (NOAA nClimDiv, monthly from 1895) or the Drought Monitor's area in drought
  (weekly from 2000).
- **Y5 `margin-susceptibles`** (epidemiology: an outbreak takes off only when R0 = beta S /
  gamma exceeds 1, so its size depends on the stock of susceptibles S). The susceptibles of a
  crash are leveraged longs: when prices fall, maintenance-margin rules (Regulation T, FINRA
  rule 4210) force sales, which push prices down and trigger more calls. A first fall should be
  followed by a further fall only when S, margin debt over market value (FINRA, monthly from
  1997), is high: crash timing as an interaction of a trigger and the susceptible stock.
- **Y6 `smoke-cognition`** (environmental health). Fine-particle pollution in New York lowers
  same-day S&P 500 returns through traders' cognition and mood (Heyes, Neidell and Saberian,
  NBER 2016, sample 2003-2015 `[memory]`). Dose: daily PM2.5 at Manhattan monitors (EPA
  pre-generated daily files, keyless).
- **Y7 `winter-light`** (photobiology / chronobiology). Seasonal affective disorder raises risk
  aversion as nights lengthen (Kamstra, Kramer and Levi, American Economic Review 2003), the
  clock change costs sleep (same authors, AER 2000), sunny mornings lift returns (Hirshleifer
  and Shumway, Journal of Finance 2003) `[memory]`.
- **Y8 `pollen-mood`** (aerobiology). Heavy pollen days impair allergic traders and lower risk
  appetite.
- **Y9 `adaptive-radiation`** (evolution: after an ecological opportunity a lineage splits into
  many species, which then compete for the same resource and many go extinct). A burst of new
  coins splits a fixed pool of speculative capital; once new tokens multiply, the large coins
  should earn less. Dose: new coins listed per week.
- **Y10 `flickering`** (ecology: before a regime shift a system flickers between two states,
  raising skewness and bimodality of its state variable; Scheffer et al., Nature 2009
  `[memory]`). Rising skewness or bimodality of returns should precede crashes.
- **Y11 `harvest-cash`** (agricultural economics). US farmers sell most of the crop at harvest
  (October-November) and park the cash, a seasonal deposit inflow that should ease funding and
  lift bonds and stocks in those months.
- **Y12 `heat-labour`** (occupational physiology). Hot days cut labour supply and output (Graff
  Zivin and Neidell, Journal of Labor Economics 2014 `[memory]`); unusually hot quarters should
  depress earnings and stock returns after them.

### Score

| # | F1 not announced | F2 not price-driven | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| Y1 `temperature-premium` | pass (b): a premium | pass: global temperature does not follow SPY | 0 | 2 | 1 (samples to about 2012-2015 `[memory]`: 10+ train years after) | 1 (393 non-overlapping months 1993-2025) | 1 (no run read a temperature series as a dose) | 1 (W19's ENSO was a crop-yield channel on DBC; the global anomaly co-moves with ENSO, said in the card) | 0 | **6** | 1% |
| Y2 `outbreak-premium` | pass (b): a premium | pass: WHO reporting does not follow asset prices | 0 | 2 | 1 (Donadelli et al. to about 2014 `[memory]`: 11 train years after) | 1 (about 1,080 weeks and 3,000 reports, 2005-2025) | 1 | 1 (FluView was filtered, never tested; seasonal flu surveillance is not an outbreak notice) | 0 | **6** | 0.5% |
| Y3 `monsoon-gold` | pass (a): rainfall is public, the purchases it funds are not | pass | 0 | 2 | 0 (no paper tests gold returns on rainfall `[memory]`) | **0** (one monsoon a year: 21 GLD seasons) | 1 | **0**: the channel (Indian household demand moves GLD) died as W13 `festival-gold` | 0 | 3 | 0.3% |
| Y4 `drought-inflation` | pass (b): an inflation-risk premium | pass | 0 | 2 | 0 | 1 (monthly) | 1 | **0**: ENSO -> crop yields -> commodity inflation died as W19 | 0 | 4 | 0.5% |
| Y5 `margin-susceptibles` | pass (a): the forced sales are not public (monthly totals come about three weeks late) | with controls: margin borrowing rises in bull markets | 1 (margin rules) | 2 | 0 (formed tonight) | **0** (falls deep enough to trigger calls: about ten episodes since 1997) | 1 | 1 (E4 killed leverage on coins through funding and basis; no run used margin debt) | -1 | 4 | 0.5% |
| Y6 `smoke-cognition` | **fail**: cognition and mood, neither a flow nor a premium (and a same-day effect) | pass | - | - | - | - | - | - | - | filtered |
| Y7 `winter-light` | **fail**: SAD and the clock change are calendars without a dose; sunshine is mood | pass | - | - | - | - | - | - | - | filtered (and `lunar`, the same field, died) |
| Y8 `pollen-mood` | **fail**: mood | pass | - | - | - | - | - | - | - | filtered (and no keyless national pollen series) |
| Y9 `adaptive-radiation` | pass (a) | **fail**: the story is that coin launches follow coin prices (W21 `stablecoin-mint`'s class) | - | - | - | - | - | - | - | filtered (and no keyless listing dates) |
| Y10 `flickering` | - | **fail**: skewness and bimodality are functions of the price path | - | - | - | - | - | - | - | filtered (and `critical-slowing`'s family) |
| Y11 `harvest-cash` | **fail**: a fixed seasonal calendar; crop sizes come in scheduled USDA reports | pass | - | - | - | - | - | - | - | filtered |
| Y12 `heat-labour` | pass (a) | pass | - | - | - | - | - | - | - | dead (literature): Addoum, Ng and Ortiz-Bobea (Review of Financial Studies 2020) find no effect of temperature on establishment sales or earnings `[memory]` |

**No flow-size check** (wide-15 "Next" point 3): Y1 and Y2 are premia, not flows. For the
record, Y3 would fail one: a 10% rainfall surprise moving 10-20% of rural demand is a few USD bn
a year against a gold stock worth about USD 20 tn `[memory]`.

**Picked by the rule.** Two candidates score 6: Y1 and Y2. Both are premia whose dose prices
cannot move, so placebo shifts in both directions are allowed. **Gated: Y1 as W29
`temperature-premium` (one static file), then Y2 as W30 `outbreak-premium` (one keyless API).**
W numbers follow wide-15's W28; if a parallel lane used them, the names decide. Y3-Y5 stay
parked (not counted); Y6-Y12 are filtered or dead in the literature.

## Steps 3 and 4. The two gates

Rules, data, statistics, placebos, gates, power and guesses are in
[`cards/wide-17.md`](cards/wide-17.md), pushed before any number.

## What came out (one dry run, then one real run, 2026-11-24 23:35 UTC)

**Timestamp erratum.** The card says "written 2026-11-24 about 23:55 UTC" and step 2 first said
"about 23:45": both were slips. The card was committed at 23:31:36 UTC (455cb2d), the script
and tests at 23:34:25 (5c4c2f7), and the one real run wrote its results at 23:35. The order the
method needs (card, then script, then numbers) holds; the card itself is left unchanged.

**Dry run first** (`DRY=1`, counts only): GISTEMP 1,750 months read, 1880-01 .. 2025-10 (none
later); 393 gate dose months, all with d; rows with outcome and dose SPY 393, QQQ 319, TLT 279,
GLD 251, BTC 165, ETH 113; placebos keep 306-393 rows. WHO DON 3,162 reports read, 2004-01-05 ..
2025-10-03 (none after the cut); 1,139 weeks, 1,087 with a dose; 1,082 gate Fridays, all with x
and an SPY outcome (QQQ, GLD, TLT, XLV the same; BTC 722, ETH 493); placebos keep 979-1,060
rows. Then one real run, as carded. Tables: `results/temperature-premium.md`,
`results/outbreak-premium.md`.

### W29 `temperature-premium`: fails

**One degree C more warmth in the last year than in the decade before goes with +3.25% on SPY
in the month after next (t +1.63, 393 months, outcome months 1993-02 .. 2025-10): the
predicted sign, but t below 2 and the true t ranks 9 of 41 (empirical one-sided p 0.22). Dead
by the gate: no card, no strategy.** Held-out year untouched. In units: d's sd is 0.112 deg C,
so one sd goes with +0.36% a month.

| Cut (SPY next-but-one month unless named) | b, % per deg C | t | Rows |
|---|---:|---:|---:|
| **Gate: d, no controls** | **+3.25** | **+1.63** | 393 |
| QQQ / TLT / GLD instead | +5.83 / -0.84 / +5.82 | +1.52 / -0.35 / +2.15 | 319 / 279 / 251 |
| BTC and ETH pooled | +14.7 | +0.91 | 278 |
| 12-month horizon | +26.1 | +1.73 | 382 |
| Monthly innovation instead of d | -0.23 | -0.16 | 393 |
| Outcome months 2013-01 .. 2025-10 | +2.34 | +1.16 | 154 |
| Reaction: SPY over month m+1 (premium story: negative) | +3.14 | +1.55 | 392 |

- **Not a premium pattern.** A priced risk lowers prices when the shock lands and pays back
  afterwards. Here the release-month slope has the same positive sign and size as the forward
  one (+3.14, t +1.55, against +3.25), which reads as warm spells coinciding with good stock
  years (which years was not computed). The monthly innovation, the shock itself, has no slope (t -0.16).
- **The null is wide: SD of placebo t 1.47, 22% with |t| >= 2**, quantiles 5/50/95% -2.10 /
  -0.11 / +2.85, extremes -2.39 / +3.11. Eight placebos beat the true t, mostly the far shifts
  (k = -85: +3.11, +89: +2.98, +85: +2.84, -45: +2.30, -81: +2.13, +81: +2.09, -41: +1.70,
  -49: +1.65): a persistent dose with a few ENSO-paced swings lines up with stock regimes at
  many lags.
- GLD's +2.15 is noted only (`gate-null.md` step 6: one of 7 shown cells, inside the placebo
  range of this design).
- My guess (either sign, |t| < 1.5, middle rank, placebo sd 1.2-1.8, pass 1%) held on the width
  (1.47); t (+1.63) and rank (9) came out a little better than guessed.

### W30 `outbreak-premium`: fails

**One unit of outbreak activity above its trailing year (Anscombe count of WHO Disease
Outbreak News reports) goes with +0.065% on SPY over the next 4 weeks (t +1.68, 1,082 weeks,
2005-01 .. 2025-09): the predicted sign, but t below 2 and the true t ranks 9 of 41 (empirical
one-sided p 0.22). Dead by the gate: no card, no strategy.** Held-out year untouched. x's sd is
2.34 units, so one sd goes with +0.15% per 4 weeks (about 2% a year), against the 0.55% per sd
the power note said a pass needed.

| Cut (SPY 4-week return unless named) | b, % per unit of x | t | Rows |
|---|---:|---:|---:|
| **Gate: x, no controls** | **+0.065** | **+1.68** | 1,082 |
| QQQ / GLD / TLT instead | +0.117 / -0.005 / +0.002 | +2.21 / -0.06 / +0.04 | 1,082 each |
| XLV (health care) | +0.020 | +0.40 | 1,082 |
| BTC and ETH pooled | -0.186 | -0.74 | 1,215 |
| Raw Anscombe count z instead of x | +0.018 | +0.40 | 1,082 |
| 1-week horizon | +0.010 | +0.46 | 1,082 |
| Fridays 2015-01 .. 2025-09 | +0.060 | +1.78 | 561 |
| With SPY's past 4/13/26/52-week returns | +0.068 | +1.81 | 1,082 |
| Reaction: SPY over the dose week (premium story: negative) | +0.017 | +1.05 | 1,082 |

- **Not a premium pattern either.** The dose week's own SPY return has the wrong sign for a
  disaster premium (+0.017, t +1.05; a premium needs prices to fall when the news lands), safe
  havens do not move (GLD -0.06, TLT +0.04), and the health-care sector, where Donadelli et
  al. found same-day gains, shows nothing forward (t +0.40). Without the trailing-year
  detrending the slope vanishes (t +0.40): what slope there is comes from short bursts against
  the recent norm, i.e. from a handful of outbreak episodes.
- **The null is wider than guessed: SD of placebo t 1.64, 22% with |t| >= 2**, quantiles 5/50/95%
  -3.38 / +0.27 / +2.17, extremes -3.64 / +2.58. Eight placebos beat the true t, five of them
  later doses (k = -63: +2.58, -39: +2.26, -59: +2.16, -87: +1.94, -51: +1.87) and four earlier
  (+83: +2.06, +71: +1.94, +91: +1.90, +99: +1.64). The detrended count still clusters in
  outbreak episodes, so shifted calendars land on other months' common moves.
- QQQ's +2.21 is noted only (one of 10 shown cells; placebo SD 1.64, 95% quantile +2.17).
- My guess (b near zero, |t| < 1.5, middle rank, placebo sd 1.0-1.3, pass 0.5%) was wrong on
  the width (1.64, not 1.0-1.3): outbreak reports are not independent weekly draws.

Labels: both gates are **kill-only** by `gate-null.md` step 7 (smallest p 1/41 = 0.024 above the
family bar 0.0011 and the register's 1.0e-4; about 8-10 temperature swings, 10-20 outbreak
episodes). Both are kills.

## Family count and status

Two mechanisms added and closed by their gates (W29 `temperature-premium`, W30
`outbreak-premium`). The ten others (Y3-Y12) are parked, filtered or dead in the literature
and are **not counted**, as wide-12 .. wide-15 did.

**Count: 90 mechanisms (88 carried in + W29 + W30), 19 tested by a strategy, none passed; 24
gates, all failed.** The next strategy test is read at **p < 0.10 / 90 = 0.0011** (family) and
the register's bar (N_eff 500: z >= 4.70, +0.31 to +0.56 Sharpe over `tsmom12`, Bonferroni
p <= 1.0e-4). Published effects after publication: still 0 for 10 (neither gate tested a
published claim as stated: the temperature papers price the risk in the cross-section, not as a
time-series forecast of SPY; Donadelli et al. tested pharmaceutical stocks on the day).

Rows logged in `tries.md`: 2 (`temperature-premium`, `outbreak-premium`, kind `screen`).

## Next

1. **Parked, scored 4: Y4 `drought-inflation`, Y5 `margin-susceptibles`.** Y4 reuses W19's dead
   channel with a new dose; Y5 (FINRA margin debt as the susceptible stock of a crash) has about
   ten trigger episodes since 1997 and needs price controls. Neither is more likely than the 24
   that died; a lane that runs them should expect a kill.
2. **A check both gates suggest for any premium story: test the reaction cell first.** A risk
   premium predicts opposite signs at the release and afterwards. Both doses here had the same
   positive sign in both windows, which reads as "the dose shares regimes with good stock
   years", not as a premium. A future premium card could make an opposite-signed reaction a
   necessary condition, fixed before any number (this run did not change the rule).
3. Life-science mechanisms that come with a *flow* (Y3 monsoon gold) fail the flow-size check of
   wide-15 point 3 by orders of magnitude; the ones that come as *mood* (Y6-Y8) fail F1. What is
   left from these fields is premia on rare biological or climate risk, and both premium gates
   here found the pattern of a regime coincidence, not a premium.
