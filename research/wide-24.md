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
relative to `main` (0.10 / 108 = 0.00093 if #210 lands first).

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
`iso_a2`, `latitude`, `longitude`) was fetched from `raw.githubusercontent.com` (no robots.txt:
404; GeoNames was checked first and its robots.txt disallows everything, so it was not used)
and its field names printed. The cached USGS catalogue was not opened.

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
