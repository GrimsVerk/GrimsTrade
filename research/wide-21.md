# Wide 21: twelve mechanisms from hydrology, oceanography, astronomy / solar physics, chemistry and materials science, scored before any price, the top one gated

Research run wide-21, 2026-11-25 (night run, WIDER lane). Branch `wide-21` (from `main`
a6d66ff), PR into `main`. Research only: fake money, keyless public data, no change to the gym,
the daily runner or the live strategies. Train only: no bar, index value or sunspot month after
2025-10-31 is used.

Other lanes tonight took biology / ecology / epidemiology / climate (wide-17), physics / signal
processing / control / networks (wide-18), meteorology / actuarial science / operations research
(wide-19), economic history / demography / psychology / linguistics (wide-20), seismology
(omori-1) and drought (parked-gates-1). Candidates in those fields are left out here.

**Count carried in** (`gate-null.md` count note after summary-6, #191): **101 mechanisms, 29
tested by a strategy, none passed; 28 gates, one kill-only pass (W32), killed by its
replication R32.** As in wide-12 .. wide-20, only mechanisms that get a gate or a strategy test
enter the count.

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-25 01:16): **4,126 tries,
N 1,116 for a new pick; measured rho 0.55 gives N_eff 506: a new rule needs z >= 4.70 against
`tsmom12` (+0.31 close rule, +0.56 far rule), Bonferroni p <= 9.9e-5.** Family bar after this
run's gate: p < 0.10 / 102 = 0.00098.

Method as wide-20: wide-11's filters F1 (not announced: an unscheduled flow (a) or a premium
(b)) and F2 (not price-driven; passing only with controls costs 1 point), then wide-10's points
(structural cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1), plus keyless long
data. Gates follow `research/gate-null.md` (40 placebos, the rank decides, t >= 2 also
required, rule pushed before any number, one dry run with counts only, then one real run).
`[memory]` marks a literature fact not checked tonight; `[search summary]` one read only as a
web-search summary.

## Step 1. What the record already holds in these fields (skipped here)

Searched `research/` and `docs/` on 2026-11-25 for: sunspot, Jevons, solar, volcan, Pinatubo,
PDO / Pacific decadal, Mississippi, streamflow, river, flood, tide, ocean, eclipse, cosmic,
Kaiser effect, Paris law, rogue wave, fatigue, chemi*, material*. Already done (not redone):

- Astronomy / solar physics: W3 `lunar` (moon phase, wide-6, dead), W16 `geomagnetic-storm`
  (Kp/Ap storm days, wide-8, dead). No gate on the sunspot cycle itself (the only hit,
  `wide-8.md`, notes that GFZ's Kp file carries sunspot numbers under CC BY-NC).
- Oceanography: W19 `enso-commodity` (ONI, wide-9, dead).
- Hydrology: W28 `refund-runoff` (a Nash-cascade unit hydrograph used as a method, wide-15,
  dead); W32 `drought-inflation` (PDSI, parked-gates-1, passed kill-only, killed by R32).
- Materials science: `fatigue-damage` (wide-1 / wide-4's W7: rainflow-counted damage of
  leveraged longs, a price transform, listed `new`); it is not repeated.
- Seismology: `tidal-trigger` (wide-1, listed) and omori-1 (killed in step 1).
- Volcanoes: data-wide-1 row 28 (Smithsonian GVP database answered 403).

## Step 2. Twelve mechanisms, scored (2026-11-25, before any price was read)

**Disclosure.** Before this table one source was probed for format only (no price, no return,
no statistic): SILSO's monthly mean total sunspot number file (3,334 rows, 1749-01 .. 2026-10,
semicolon-separated; the probe printed the first and last three rows, so three monthly sunspot
values of 2026 were seen; they are after the cut and never used). Shiller's `ie_data.xls` was
already in the cache from survey-4 (2026-11-12); no value of it was read for this run before
the card.

### The mechanisms (cause story each)

- **S1 `solar-max-recession`** (solar physics x Jevons' sunspot theory of the trade cycle).
  Jevons (1875-1882) claimed commercial crises recur with the sunspot period; Gorbanev (MPRA
  40271, 2012; Journal of Scientific Exploration 2015) reports that G7 recessions start
  disproportionately in the three years around and after solar maxima (from 1965, nearly
  three fifths of them) `[search summary]`. Proposed channels: solar activity changes weather
  and harvests (Jevons), or human mood and health through geomagnetic activity. If true, US
  stocks should earn less after high solar activity, which nobody prices. Dose: the trailing
  12-month mean sunspot number (its amplitude varies about threefold between cycles).
  Gorbanev himself later (MPRA 102163, 2020) placed the 2008 and 2020 crises near solar
  **minima** `[search summary]`: the claim's own author has wavered on the sign.
- **S2 `volcanic-veil`** (atmospheric chemistry / volcanology). Large eruptions put sulphate
  aerosol into the stratosphere (Krakatoa 1883, Santa Maria 1902, Katmai 1912, Agung 1963,
  El Chichon 1982, Pinatubo 1991), cooling the globe by up to about 0.5 C for one to two years
  `[memory]`: weaker harvests, food inflation, lower real returns and higher yields. Dose:
  stratospheric aerosol optical depth (NASA GISS, keyless, 1850-2012).
- **S3 `river-freight`** (hydrology). Low water on the Mississippi (St. Louis gauge, USGS
  07010000, daily discharge from 1861, keyless) restricts barge loads and raises freight rates
  for grain, coal and chemicals (2012, 2022) `[memory]`; high water closes locks (1927, 1993,
  2019). A transport-cost shock: inflation and industrial output, so TLT down and stocks down
  after extreme stages.
- **S4 `pdo-regime`** (oceanography). The Pacific Decadal Oscillation (NOAA, monthly from
  1854, keyless) shifts North American temperature, rainfall and fisheries for decades
  (regime shifts about 1925, 1947, 1977, 1998 `[memory]`); a slow climate-risk premium on US
  stocks.
- **S5 `amo-hurricane`** (oceanography). Warm phases of the Atlantic Multidecadal Oscillation
  bring more Atlantic hurricanes and more US drought `[memory]`; a catastrophe-risk premium.
- **S6 `cosmic-ray-cloud`** (solar physics, Svensmark). Galactic cosmic rays (neutron monitors,
  Oulu from 1964) seed low clouds; Forbush decreases change cloud cover and mood within days.
- **S7 `eclipse-omen`** (astronomy). Solar eclipses are old omens; investors trade less and
  worse around them (Lepori 2009, "Dark omens in the sky" `[memory]`).
- **S8 `hurst-flood`** (hydrology method). Hurst's rescaled range on Nile floods found long
  memory (the Joseph effect); applied to returns, long memory would make multi-year trends
  predictable.
- **S9 `kaiser-felicity`** (materials science, acoustic emission). A loaded material emits
  acoustic bursts only when the load passes its previous maximum (Kaiser effect); bursts below
  the old maximum (a Felicity ratio under 1) mark accumulated damage before failure. Market
  form: volatility bursts while the index is still below its prior high as a crash precursor.
- **S10 `stress-corrosion-calm`** (materials science, subcritical crack growth). Cracks grow
  slowly under a constant moderate load in a corrosive environment, then fail suddenly; market
  form: long calm periods with credit growth precede crises (Danielsson, Valenzuela and Zer,
  RFS 2018 `[memory]`).
- **S11 `paris-law-credit`** (fracture mechanics). Crack growth per cycle rises as a power of
  the stress intensity (Paris law), so a crack accelerates as it grows; market form: the
  acceleration of private credit to GDP (BIS, quarterly) times the leverage level forecasts
  crises (cf. Greenwood, Hanson, Shleifer and Sorensen, JF 2022 `[memory]`).
- **S12 `chemical-accident-mood`** (chemistry, industrial disasters). Large chemical plant
  explosions and releases (Bhopal 1984, Texas City, Beirut 2020) as salient frightening events
  that depress stocks for a day or two.

### Score

| # | F1 not announced | F2 not price-driven | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| S1 `solar-max-recession` | pass (a): the sunspot number is public but nobody prices it; the recession it is said to trigger is an unscheduled shock | pass: the sun does not answer prices | 0 (no accepted channel; the harvest channel failed in W32/R32, the geomagnetic mood channel in W16) | 2 (cycle amplitudes differ about threefold) | 1 (1871-2025 is post-Jevons; 2012-2025 post-Gorbanev, shown) | 1 (about 1,850 months; but only about 14 cycles: kill-only) | 1 | 1 (no gate on the cycle; the author's 2020 sign change is a warning, not a test) | 0 | **6** | 1% |
| S2 `volcanic-veil` | pass (a) | pass | 1 (the cooling is physics) | 2 (aerosol depth) | 0 (no return paper known to me) | 0 (six eruptions since 1871) | 1 | 0 (the food-price link was absent in W32/R32; disaster studies find volcanoes have limited market impact `[search summary]`) | 0 | 4 | 0.5% |
| S3 `river-freight` | pass (a) | pass | 1 (freight rates do jump) | 2 (stage) | 0 | 1 (daily from 1861) | 1 | 0 (size: barge freight is a tiny cost share of the economy; the inflation channel failed in W32/R32) | 0 | 5 | 0.3% |
| S4 `pdo-regime` | pass (b) | pass | 0 | 2 | 0 | 0 (four or five regimes) | 1 | 0 (ENSO, W19, and drought, W32/R32, its channels, are dead) | 0 | 3 | 0.3% |
| S5 `amo-hurricane` | pass (b) | pass | - | - | - | - (two or three phases since 1856) | - | **dead channel**: catastrophe claims W15 and drought W32 | - | - | filtered (duplicate) |
| S6 `cosmic-ray-cloud` | pass (a) | pass | - | - | - | - | - | **duplicate of W16**: Forbush decreases coincide with geomagnetic storms | - | - | filtered (duplicate) |
| S7 `eclipse-omen` | **fail**: eclipses are scheduled centuries ahead, no dose (a calendar mean, like W3 `lunar`) | pass | - | - | - | - | - | - | - | - | filtered |
| S8 `hurst-flood` | pass (b) | **fail**: a statistic of past returns | - | - | - | - | - | dead in the literature: Lo (1991) modified R/S finds no long memory in US stock returns `[memory]` | - | - | dead (literature) |
| S9 `kaiser-felicity` | pass (a) | **fail**: volatility and prior highs are prices | - | - | - | - | - | - | - | - | filtered |
| S10 `stress-corrosion-calm` | the credit part fails (published statistic read as news) | **fail**: calm is low volatility, a price; near wide-6's `critical-slowing` and the vol-timing work | - | - | - | - | - | - | - | - | filtered |
| S11 `paris-law-credit` | **fail**: quarterly credit statistics are public news | with controls: credit grows after price rises | - | - | - | - (two or three US crises) | - | - | - | - | filtered |
| S12 `chemical-accident-mood` | pass (a) | pass | - | - | - | - | - | **dead class**: the mood-shock channel died post-sample in W31 (`air-disaster-mood`), with more events | - | - | filtered (dead class) |

**Size check (shown, not part of the rule).** S3 is a flow story: US inland barge traffic moves
roughly 500-600 m tons a year at a few tens of dollars a ton `[memory]`, so even a doubling of
freight rates is a cost shock of a few USD bn, against a USD 30 tn economy: invisible in SPY or
TLT. S1 and S2 are macro-shock stories (recessions, harvests), not flows; their size is set by
how often the shock really follows the dose.

**Picked by the rule.** S1 scores 6 (highest), with keyless data covering the whole long
history (sunspots from 1749, Shiller's S&P 500 from 1871). **Gated: S1 as W34
`solar-max-recession`** (card `cards/wide-21.md`, pushed before any return was read; W34 is the
next free id on `main`'s `gate-null.md`; parallel lanes may take it too, the lead renumbers).
The next candidate (S3, score 5) fails its own size check and its channel (inflation) died in
W32/R32; S2 has six events, so even a pass could say nothing. Neither is gated; both are parked,
not counted.
