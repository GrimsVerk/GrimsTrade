# Wide 24: thirteen mechanisms from seismology, supply networks, renewal processes, sport, mega-events, shipping, telecommunications, white-collar crime, livestock disease, migration, supply chains, materials and extreme-value theory, scored before any price, the top one gated

Research run wide-24, 2026-11-25 (night run, WIDER lane). Branch `wide-24` (from `main`
94bbbd0), PR into `main`. Research only: fake money, keyless public data, no change to the gym,
the daily runner or the live strategies. Train only: no bar or event after 2025-10-31 is used.

Fields already mined are left out: physics, signal processing, control, networks of prices
(wide-18), meteorology, actuarial science, operations research (wide-19), biology, ecology,
epidemiology, climate (wide-17), economic history, psychology, sociology, demography of age
structure (wide-20), hydrology, oceanography, solar physics, chemistry, materials (wide-21),
energy systems, queueing, reliability, game theory, freight (wide-22), cybercrime, Supreme
Court and crypto court rulings, KL news novelty, cloud outages, influenza, estates, crime
counts, bolides, soil moisture, creep (wide-23), and the open PR #210 (jst-gates-1: W38
`consumption-cycle`, W39 `bank-capital-premium`). Mechanisms scored there are not scored
again. Lunar and tidal clocks are not scored again either: they are scheduled (F1), W3 `lunar`
is dead and `tidal-trigger` (wide-4) is listed.

**Count carried in** (`gate-null.md` on `main` 94bbbd0, count after W37): **105 mechanisms, 29
tested by a strategy, none passed; 33 gates, two kill-only passes (W32, W36), each killed by
its replication (R32, R36).** PR #210 (open when this lane started) adds W38 and W39: 107 / 29
/ 35 if it lands first. As in wide-12 .. wide-23, only mechanisms that get a gate or a strategy
test enter the count.

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-25 01:16): **4,126 tries,
N 1,116 for a new pick; measured rho 0.55 gives N_eff 506: a new rule needs z >= 4.70 against
`tsmom12`, Bonferroni p <= 9.9e-5.** Family bar with this run's gate: p < 0.10 / 106 = 0.00094
relative to `main` (0.10 / 108 = 0.00093 if #210 lands first; it did, at 22:38 UTC, see the
count below).

Method as wide-21 .. wide-23: wide-11's filters F1 (not announced: an unscheduled flow (a) or
a premium (b)) and F2 (not price-driven; passing only with controls costs 1 point), then
wide-10's points (structural cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1),
plus keyless data, a size check and a duplicate check against the record. Gates follow
`research/gate-null.md` (40 placebos, the rank decides, t >= 2 also required, rule pushed
before any number, one dry run with counts only, then one real run). gate-null-2's proposed
"both families" rule applies when the dose's lag-1 autocorrelation is 0.8 or more; the card
says whether it does. `[memory]` marks a literature fact not checked tonight.

## Step 1. What the record already holds near these fields (skipped here)

Searched `research/` and `docs/` on 2026-11-25 for: earthquake, quake, USGS, seism, Suez,
chokepoint, shipping, supply chain, GSCPI, World Cup, football, Olympic, sports, fraud, Ponzi,
scandal, migration, strike, percolation, renewal, extreme value. Found:

- **Earthquakes**: data-wide-1 cached the USGS ComCat catalogue (M >= 6 from 1900, M >= 5 from
  1973; 2026-11-19) and listed two ideas: Japan quakes and yen repatriation (wide-13 row 5,
  scored 4: the insurer-liquidation story of the dead W15 `cat-claims`) and quakes in copper and
  oil regions on DBC (wide-13 row 6, **filtered F1**: a supply shock is public within minutes and
  priced on the day). `omori-1` killed the Omori aftershock law as a market-clock idea (overlap).
  No gate on earthquake damage to the hit country's own market.
- **Shipping**: PortWatch chokepoints (data-wide-1 row 20, wide-13 row 10, scored 4: under 7
  years of data). Freight as an output gauge: wide-22 T1 (parked, duplicate of W36).
- **Sport**: W18 `elimination-mood` (wide-8; listed, never gated: "no keyless match list";
  wide-20 called its channel the same as the mood shock that W31 `air-disaster-mood` then
  killed).
- **Strikes**: wide-20 P12 `strike-idleness` (parked: the BLS server asks for a contact e-mail).
- Fraud, Ponzi, scandal, Olympic, migration, percolation, renewal, extreme value: nothing.

## Step 2. Thirteen mechanisms, scored (2026-11-25 22:30 UTC, before any price was read)

**Disclosure.** Before this table: the first and last dates, time zone and currency of the 24
cached daily index files (`insure-2/raw-2026-11-18/yahoo`, 1965-2025) were printed, no price.
The Natural Earth populated-places file (public domain, 7,342 places, fields `pop_max`,
`adm0_a3`, `latitude`, `longitude`) was fetched from `raw.githubusercontent.com` (no robots.txt:
404; GeoNames was checked first and its robots.txt disallows everything, so it was not used)
and its field names printed (file `geojson/ne_10m_populated_places_simple.geojson` of the
`nvkelso/natural-earth-vector` repository, default branch on 2026-11-25; SHA-256 of the copy
used: `fd3fa867a320cbd5c5b6bb5bc550afeec2939fb2cef688e508007282a55ac42f`; `pop_max` changes
between Natural Earth releases, so a rerun should check the hash). The cached USGS catalogue was
not opened.

### The mechanisms (cause story each)

- **Q1 `quake-drift`** (seismology as an economic shock). A large shallow earthquake under a
  country's cities destroys capital and stops production: Kobe 1995 about 2% of Japan's GDP,
  Tohoku 2011 about 3-4%, Christchurch 2011 about 10% of New Zealand's `[memory]`. The quake is
  public in minutes, but the damage is not: death tolls, damage estimates and supply-chain
  stoppages are revealed over weeks (Carvalho, Nirei, Saito and Tahbaz-Salehi, QJE 2021;
  Boehm, Flaaen and Pandalai-Nayar, REStat 2019 `[memory]`). Scholtens and Voorhorst (Earthquake
  Spectra 2013) report negative abnormal returns of the hit country's index for days after
  large quakes, larger with more deaths; Ferreira and Karali (PLOS ONE 2015) find little effect
  beyond the volatility `[memory]`. Tradable form: does the hit country's index keep falling
  against the world over the month **after** the first full session of reaction?
- **Q2 `quake-supply-spillover`** (network propagation through supply chains; percolation of a
  node failure). A quake in a hub (Japan, Taiwan) cuts inputs to its trading partners'
  factories; the partners' indices fall later as the stoppage spreads (Carvalho et al. 2021
  `[memory]`).
- **Q3 `aftershock-renewal`** (renewal processes, Omori-Utsu decay). After a mainshock the
  aftershock rate decays as 1 / (t + c)^p: a known, falling hazard that should keep a risk
  premium on the hit market until the rate has decayed.
- **Q4 `elimination-mood`** (sport; wide-8's W18, never gated). A national team's knockout
  loss lowers the next day's index (Edmans, Garcia and Norli, JF 2007, 1973-2004). The missing
  keyless match list now exists (an open international-results dataset on GitHub `[memory]`).
- **Q5 `olympic-host`** (mega-events). The award of the Olympic Games raises the winner's index
  (Veraros, Kasimati and Dawson 2004; Dick and Wang 2010 `[memory]`).
- **Q6 `canal-closure`** (shipping). Closures of Suez (1956, 1967-1975), the Ever Given week
  (2021-03) and the Red Sea attacks (2023-) raise freight costs and delay inputs.
- **Q7 `cable-cut`** (telecommunications). Submarine cable faults (the 2006 Hengchun quake cut
  Taiwan's links, the 2008 Mediterranean cuts) slow a region's traffic and trade.
- **Q8 `fraud-revelation`** (white-collar criminology: Galbraith's "bezzle" grows in booms and
  is revealed in busts; Povel, Singh and Winton, RFS 2007). Revealed corporate frauds lower
  trust in the market and household participation (Giannetti and Wang, JF 2016; Guiso,
  Sapienza and Zingales, JF 2008 `[memory]`): a trust shock that raises the equity premium.
- **Q9 `livestock-epidemic`** (agriculture beyond drought: foot-and-mouth in the UK 2001,
  African swine fever in China 2018-2019, avian influenza culls).
- **Q10 `refugee-wave`** (demography of migration: large inflows as labour-supply shocks).
- **Q11 `supply-pressure`** (supply-chain bottlenecks: the New York Fed's Global Supply Chain
  Pressure Index, monthly from 1997) as an inflation-risk premium on bonds.
- **Q12 `export-ban`** (materials and critical minerals: China's rare-earth quota cut 2010,
  gallium and germanium controls 2023) as an input shock to importers.
- **Q13 `disaster-evt`** (extreme-value theory: the rate of exceedances of a high threshold of
  world disaster losses as a time-varying Barro-Wachter disaster probability, a premium).

### Score

| # | F1 not announced | F2 not price-driven | Cause | Dose | Post | Power | Unseen | Not killed | F1/F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| Q1 `quake-drift` | pass (a, b), weakly: the quake is public in minutes (wide-13 filtered the commodity form for that); the damage is revealed over weeks, so the drift form rests on slow revelation | pass: quakes do not follow prices | 1 (capital destroyed, production stopped, 1-10% of GDP in the large cases) | 2 (exposed share of the population spans orders of magnitude) | 1 (Scholtens-Voorhorst's sample ends 2011 `[memory]`; about half the gate's events are later) | 1 (to be counted in the dry run; dozens of damaging shallow quakes in the cached markets, nearly independent) | 1 (no quake gate in the record) | 1 (damage channel; W15's insurer flow and W31's mood are other channels) | -1 (weak F1) | **6** | 3% |
| Q2 `quake-supply-spillover` | pass (a) | pass | 1 | 2 | 1 | 0 (a handful of hub quakes: Kobe, Chi-Chi, Tohoku, Kumamoto, Hualien 2024) | 1 | 1 | 0 | 6 but power 0 | parked: power, and input-output weights are not keyless by script `[memory]`; its first link is Q1 |
| Q3 `aftershock-renewal` | **fail**: once the mainshock is known the Omori decay is a public, deterministic clock (scheduled in effect) | - | - | - | - | - | - | omori-1 killed the market form (overlap) | - | - | filtered (F1) |
| Q4 `elimination-mood` | partly: match dates are scheduled and the odds are priced; the loss is the surprise | pass | 0 (mood) | 1 (round x weight) | 1 (2005-2025) | 1 (with 24 cached indices, perhaps 60-100 eliminations) | 1 (never gated) | 0 (the mood-shock class died in W31 `air-disaster-mood`, the same authors' sibling claim) | 0 | 4 | 0.5% |
| Q5 `olympic-host` | pass (b) | pass | 0 (host spending is small against GDP) | 1 | 1 | **0** (about 15 awards in markets with data) | 1 | 1 | 0 | - | filtered (power) |
| Q6 `canal-closure` | pass (a) | pass | 1 | 1 | 1 | **0** (four or five closures) | 1 | 1 | 0 | - | filtered (power) |
| Q7 `cable-cut` | pass (a) | pass | - | - | - | 0 | - | **no channel**: trading and payments reroute within hours; no index-level size | - | - | filtered (size) |
| Q8 `fraud-revelation` | pass (a): revelations are unannounced | with controls: frauds are revealed in busts (after falls) | 1 | 1 (counts) | 1 | 0-1 (the keyless DOJ press list starts 2009: one bust) | 1 | 1 | -1 | 5 | 0.5%; parked (data: the SEC's servers ask for a contact e-mail in the user agent, which this project does not send) |
| Q9 `livestock-epidemic` | pass (a) | pass | - | - | - | 0 (a few large outbreaks) | - | **dead channel**: the food-price link was absent in W32/R32 | - | - | filtered |
| Q10 `refugee-wave` | **fail**: inflows are counted with lags and published as news; arrivals are slow | - | 0 (Card 1990: no wage effect of the Mariel inflow `[memory]`) | - | - | - | - | - | - | - | filtered (F1, size) |
| Q11 `supply-pressure` | fails as a flow (a monthly scheduled release); passes as a premium (b) | with controls: supply pressure peaks in demand booms | 1 | 2 | 1 | **0** (three episodes since 1997: 2000, 2011, 2021) | 1 | 0 (inflation-risk channel dead in W32/R32) | -1 | - | filtered (power) |
| Q12 `export-ban` | pass (a) | with controls (bans follow price spikes) | - | - | - | **0** (a few events, single sectors) | - | - | - | - | filtered (power, reach) |
| Q13 `disaster-evt` | pass (b) | pass | - | - | - | - | - | **duplicate**: the disaster-probability premium died in W30 `outbreak-premium`; the disaster list (EM-DAT) needs a registration | - | - | filtered (duplicate, data) |

**Size check (shown, not part of the rule).** Q1: the large cases destroy 1-10% of the hit
country's capital or a year's GDP share `[memory]`, against index moves of 5-15% in the weeks
after Kobe and Tohoku. Most of the damage is to housing and public assets, not listed firms,
and listed firms earn abroad, so the index reach is a fraction of the GDP loss; a drift of 1-3%
after the large events would be plausible, of near zero after the small ones. Q2, Q5, Q6 fail
on events, not size.

**Picked by the rule.** Q1 scores 6, the only candidate at 6 with keyless data and more than a
handful of independent events. **Gated: Q1 as W40 `quake-drift`** (card `cards/wide-24.md`,
pushed before any return or event count was read; ids W40 / R40 provisional: W38 / W39 are
taken by the open PR #210). The replication **R40** is fixed in the same card before any
number: the same rule on the events before the gate window (1965-1997), mostly Japan, so it
adds independent events. Q2 has power 0; Q4 and Q8 score 4-5 and are parked; no second gate
(W41 is not used).

Q4's note for the record: the data gap that kept W18 from running is closed (keyless match
results on GitHub `[memory]`, and 24 cached daily indices), but its channel is the mood shock
that W31 killed post-publication, and a one-day dip is not a trade at the book's weekly horizon.

## Step 3. W40 `quake-drift` gate

The rule, data, placebo family, gate, the replication R40 (run only after a pass), shown cells,
power and guess are in [`cards/wide-24.md`](cards/wide-24.md), pushed before any number (commit
f9e4b65, 22:30 UTC). Code: `research/lib/wide24_events.py` (pure functions, tested offline in
`tests/test_wide24.py`) and `research/lib/wide24.py` (load and run). Results:
`research/results/quake-drift.md`.

### Dry run (counts only, 2026-11-25 22:33 UTC)

Cached ComCat (data-wide-1, 2026-11-19): **6,698 events of M >= 6.0 and depth <= 70 km,
1965-01-01 .. 2025-10-31; 5,245 after declustering; 157 (event, market) pairs with exposure
above 0** over the whole span. Gate rows (1998-01-01 .. 2025-10-31): **168,901 rows in 25
markets, 79 (event, market) pairs, sum of weights 70.8** (N225 17 pairs / 18.0, JKSE 18 / 15.7,
TWII 9 / 13.5, NZ50 5 / 9.9, MXX 14 / 6.7, KLSE 1 / 5.2, the US 11 / 0.4, India 2 / 0.9, Italy
1 / 0.4, Canada 1 / 0.0; 15 markets none). **Pooled lag-1 autocorrelation of the dose +0.008**: far under 0.8,
so gate-null-2's proposed "both families" rule does not apply (as the card expected). Fewer
pairs than the card's guess (79 against about 150): the power is lower than written (below).

## What came out (one real run, 2026-11-25 22:34 UTC)

### W40 `quake-drift`: fails (no drift)

**One unit of dose (a doubling of 1 + the exposed share in percent) goes with +0.09% for the
hit country's index against the other markets over the 20 sessions after the first full
reaction session (DK t +0.38, 168,901 rows, 79 pairs, 1998-2025), against the predicted
negative sign; the true t ranks 24 of 41 shifted calendars. Dead by the gate: no card for a
strategy. R40 is not run** (the card runs it only after a pass). Held-out year untouched.

| Cell (excess over the other markets, 20 sessions from the close of s0+1, controls r2 r20, market dummies, unless named) | b, % per unit | t | Rows |
|---|---:|---:|---:|
| **Gate** | **+0.093** | **+0.38** | **168,901** |
| Reaction r2 (close of s0-1 to close of s0+1), no controls, DK 5 (the channel's first link) | -0.380 | -1.39 | 168,901 |
| 60-session horizon, DK 90 | -0.137 | -0.36 | 167,901 |
| Own return, no world subtraction | +0.144 | +0.53 | 168,901 |
| Binary dose (1 per event with S >= 1%) | +0.444 | +0.61 | 168,901 |
| Fixed radius 100 km | -0.005 | -0.03 | 168,901 |
| M >= 6.5 only | -0.088 | -0.33 | 168,901 |
| Japan only (N225) | -0.290 | -0.77 | 6,800 |
| Without Tohoku (2011-03-11) | +0.282 | +1.19 | 168,901 |
| Rows from 2012-01-01 (after Scholtens and Voorhorst's sample) | +0.131 | +0.22 | 85,219 |

- **The reaction is small and the drift is absent.** Over the event session and the next one
  the hit index moves -0.38% per unit (t -1.39): for Tohoku (w 6.0) that is about -2.3% by the
  line; the 64 pairs outside the top 15 average w 0.4, about -0.15%. After that window
  nothing follows: every shown drift cell has |t| under 1.2, the signs split
  (four negative, four positive), and the 60-session cell (a later rebuild could reverse a
  drift) is flat too.
- **The large events go both ways.** Of the 15 largest-weight pairs (results file), the excess
  over the next 20 sessions was negative for 6 (Tohoku -3.5%, Kaikoura -3.0%, Fukuoka 2005
  -3.0%, Darfield -2.5%, Chiapas 2017 -2.3%, Nias 2005 -1.4%) and positive for 9 (Chi-Chi
  +1.3%, Sumatra 2004 on Jakarta +4.0% and Kuala Lumpur +1.7%, Christchurch 2011 +1.3%,
  Miyagi 2003 +1.9%, Fukushima-oki 2022 +0.8%, Hualien 2024 +0.2%, Hualien 2018 +4.7% /
  +4.1%). Without Tohoku the slope is +0.28 (t +1.19).
- **Post-sample** (rows from 2012, after Scholtens and Voorhorst's 1973-2011 sample `[memory]`):
  t +0.22. Their negative abnormal returns are not reproduced as a drift after the first two
  sessions on these markets.
- **The null is close to normal.** Shifted calendars: SD 1.09, 5% past |t| 2, 5/50/95% -1.95 /
  +0.15 / +1.30, extremes -2.29 / +1.80. Random-day surrogates (shown): SD 1.28, 5%, rank 28 of
  41, one draw at +4.77 (a random day that put a large weight on a big move). The two families
  agree on the verdict, as in W37 (both event doses).
- **Disclosure dates.** The 15 largest-weight events are all well-known quakes reported the day
  they struck `[memory]`: Tohoku 2011, Sumatra-Andaman 2004 (on JKSE and KLSE), Chi-Chi 1999 (the
  Taiwan exchange stayed shut until 1999-09-27, which is the event session the rule found),
  Kaikoura 2016, Darfield 2010, Christchurch 2011, Nias 2005, Fukuoka 2005, Miyagi 2003,
  Fukushima-oki 2022, Hualien 2024 and 2018 (two), Chiapas 2017. No back-filled entry, so no
  correction is needed (the hindsight-dating fault found in W37 does not arise: the dose uses
  origin time, place and magnitude only).
- **A weakness of the frozen dose, seen in the list (not changed):** the radius rule gives an
  offshore M 9.1 a 592 km radius, so the 2004 Sumatra-Andaman quake counts 35% of Malaysia's
  place population as exposed (Penang and the north-west coast), while the damage there was
  small. The fixed-radius cell (100 km for every magnitude) avoids that and is flat as well
  (t -0.03).
- **Power, measured.** SE(b) is about 0.245% per unit (b / t), so a pass needed about -0.5% per
  unit, e.g. -3% over a month after a Tohoku-size event and about -1.6% after a Christchurch-size one.
  The card's guess of SE 0.21 assumed about 150 pairs; with 79 the gate detects a published-size
  drift on the large events with roughly even odds: a moderate kill, not a strong one.
- My guess (b near 0, t between -1.5 and +1, a middle rank, placebo SD 0.9-1.2, pass 3%) was
  right on every count.

Label: **kill-only** by `gate-null.md` step 7 (smallest p 1/41 = 0.024, above the family bar and
the register's 9.9e-5). A kill on its own t (t +0.38, wrong sign; no shown cell past |t| 1.4).

## Family count and status

One mechanism added and closed by its gate (W40 `quake-drift`). The twelve others are parked,
filtered or dead by size, power or channel and are **not counted**, as in wide-12 .. wide-23;
each has a `note` row in `tries.md` (no number computed) and a line in `ideas.md`.

**Count: 108 mechanisms, 29 tested by a strategy, none passed; 36 gates, two kill-only passes
(W32, W36), each killed by its replication (R32, R36).** Family bar p < 0.10 / 108 = 0.00093.
This is after #210 (W38, W39), which merged into `main` at 22:38 UTC during this lane (`main`
then 6533d7b, merged into this branch): 107 / 29 / 35 there, plus W40. Relative to the `main`
this lane started from (94bbbd0) it would have been 106 / 29 / 34. W40 is the next free id, so
the card's provisional id stands. Published effects tested after publication: 1 more (the
earthquake abnormal returns of Scholtens and Voorhorst 2013, as a drift after the first two
sessions, 2012-2025): dead.

Rows logged in `tries.md`: 1 `screen` (`quake-drift`), 9 `robustness` rows (the shown cells),
12 `note` rows (one per candidate scored but not gated). Data downloaded: 4.9 MB (the Natural
Earth populated-places file, one call); the earthquake catalogue and index closes were already
cached (data-wide-1, insure-2, yahoo-1d).

## Next

1. **The natural-disaster damage channel is closed at index level for the markets held.** With
   unscheduled events, a dose built only from what was public at the time, and a near-normal
   null, the hit index shows a small two-session reaction and nothing after it. Together with
   W15 (catastrophe claims), W31 (air disasters) and W37 (thefts), the record now has four
   unscheduled-shock gates, all dead (wide-22 E3 `blackout-cascade` was filtered, not gated): one-off shocks of this size are priced
   within a day or two, or not at all.
2. **What a rerun would need:** the cached index set misses the markets with the most damaging
   quakes per unit of market value (Chile, Turkey, Greece, Peru, the Philippines). A keyless
   source of their daily indices, fetched with an honest user agent, would roughly double the
   large events; the fixed-radius dose would avoid the offshore-megathrust artefact.
3. **Q4 `elimination-mood`** (wide-8's W18): its data gap is closed (keyless match results on
   GitHub `[memory]`, 24 cached indices). It is parked here because its channel is the mood
   shock W31 killed and a one-day dip is not a trade at the book's horizon; a lane that wants to
   close W18 for the record can now do so cheaply.
4. **Method:** event doses (W37, W40) give placebo and random-day nulls near N(0, 1) (SD
   1.0-1.3) with a dose acf near 0; gate-null-2's "both families" rule is a matter for
   persistent doses only.
