# Wide 23: fourteen mechanisms from criminology, law, information theory, neuroscience, telecommunications, public health, demography, agriculture, materials and astronomy, scored before any price, the top one gated

Research run wide-23, 2026-11-25 (night run, WIDER lane). Branch `wide-23` (from `main`
845f34e), PR into `main`. Research only: fake money, keyless public data, no change to the gym,
the daily runner or the live strategies. Train only: no bar or event after 2025-10-31 is used.

Fields already mined are left out: physics, signal processing, control, networks of prices
(wide-18), meteorology, actuarial science, operations research (wide-19), biology, ecology,
epidemiology, climate (wide-17), economic history, demography of age structure, psychology,
sociology, word-count linguistics (wide-20, panic-words-1), hydrology, oceanography, solar
physics, chemistry, materials (wide-21), public finance and administrative law (wide-15), and
the open PR #202 (wide-22: energy systems, queueing, reliability, network contagion, rational
inattention, game theory, freight, prime-age demography, frost, habituation). Mechanisms that
#202 scored are not scored again here.

**Count carried in** (`gate-null.md` on `main`, count after W35): **103 mechanisms, 29 tested
by a strategy, none passed; 30 gates, one kill-only pass (W32), killed by its replication
R32.** PR #202 (wide-22, open when this lane started, merged before this lane's PR) adds W36
and R36: **104 mechanisms, 29 tested by a strategy, 32 gates, two kill-only passes (W32, W36),
each killed by its replication.** The counts below are final after #202. As in
wide-12 .. wide-22, only mechanisms that get a gate or a strategy test enter the count.

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-25 01:16): **4,126 tries,
N 1,116 for a new pick; measured rho 0.55 gives N_eff 506: a new rule needs z >= 4.70 against
`tsmom12`, Bonferroni p <= 9.9e-5.** Family bar with this run's gate: p < 0.10 / 105 = 0.00095.

Method as wide-21 and wide-22: wide-11's filters F1 (not announced: an unscheduled flow (a) or
a premium (b)) and F2 (not price-driven; passing only with controls costs 1 point), then
wide-10's points (structural cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1),
plus keyless data, a size check and a duplicate check against the record. Gates follow
`research/gate-null.md` (40 placebos, the rank decides, t >= 2 also required, rule pushed
before any number, one dry run with counts only, then one real run), with a phase-randomised
surrogate family reported as a shown diagnostic (wide-21's note; wide-22 found the two
families can disagree). `[memory]` marks a literature fact not checked tonight.

## Step 1. What the record already holds near these fields (skipped here)

Searched `research/` and `docs/` on 2026-11-25 for: hack, exploit, cyber, DefiLlama, ransom,
supreme court, lawsuit, enforcement, influenza, fireball, asteroid, soil, estate, bequest,
outage, crime. Found:

- **Cybercrime**: data-wide-1 (row 19 and idea 9, "stolen coins and forced laundering sales")
  listed the DefiLlama hack list and scored it low (no publication date per event; counts
  follow curation); wide-13 left it unloaded. No card, gate or strategy on hacks.
  survey part 3 quotes Liu and Tsyvinski (RFS 2021): the "Bitcoin hack" Google-search ratio
  predicts -2.75% for BTC the next week (sample 2011-2018).
- **Public health**: FluView (data-wide-1 idea 8, unloaded); W30 `outbreak-premium` (dead).
- **Law**: `rule-intensity` (wide-15 X9, parked), W27 `congress-workload` (dead), wide-22's
  G1 `debt-ceiling-attrition` (filtered). No court-decision idea.
- **Telecommunications / outages**: IODA internet outages (data-wide-1 row 23, score 0.5).
- **Astronomy**: W3 moon, W16 storms, W35 sunspots (all dead); nothing beyond the solar system.
- Crime, soil, estates, asteroids: nothing.

## Step 2. Fourteen mechanisms, scored (2026-11-25 21:30 UTC, before any price was read)

**Disclosure.** Before this table one source was probed for format and counts only (no price,
no return, no statistic involving a price): the DefiLlama hack list (`api.llama.fi/hacks`,
1,377 rows, 2011-06-19 .. 2026-11-24, fields date / amount / targetType / chain / ...; one
row's fields were printed; counts of events of at least USD 10 m by year and by target type
were printed: 2014-2025 to 2025-10-31, 54 on centralised exchanges, 114 on everything else).
The first and last dates of the cached BTC and ETH bar files were read (2012-01-01 and
2016-05-18 on), no price.

### The mechanisms (cause story each)

- **C1 `hack-drift`** (criminology of cybercrime x crypto). Large thefts from DeFi protocols,
  bridges and wallets (Ronin USD 0.6 bn 2022, Wormhole, Poly Network) are unscheduled crimes.
  Three channels: the thief sells or launders the loot over days (a flow), holders of the
  hacked and similar protocols withdraw (a run), and the market reprices the platform's
  security (a premium). Corbet, Cumming, Lucey, Peat and Vigne (Economics Letters 2020)
  report negative returns and higher volatility after hacks `[memory]`; Liu and Tsyvinski
  (RFS 2021) find hack attention predicts lower BTC returns the next week (2011-2018).
  Tradable form: does ETH keep falling in the week **after** the news is out?
- **C2 `crackdown-shock`** (law and regulation, unscheduled enforcement: bans, suits,
  exchange shutdowns). Auer and Claessens (BIS Quarterly Review 2018) find regulatory news
  moves crypto prices strongly `[memory]`.
- **C3 `court-ruling-shock`** (law, unscheduled court decisions on crypto: the Ripple ruling
  2023-07, Grayscale v SEC 2023-08, Tornado Cash 2024-11).
- **C4 `scotus-business`** (law, Supreme Court decisions in economic cases; Supreme Court
  Database, keyless, 1946-): a decision against regulation as a policy-risk shock.
- **C5 `news-novelty`** (information theory / computational linguistics: KL "novelty" and
  "transience" of the day's newspaper text against the recent past, Barron, Huang, Spang and
  DeDeo, PNAS 2018 `[memory]`) on the American Stories corpus that panic-words-1 used: a novel
  news month as an uncertainty shock.
- **C6 `cloud-outage`** (telecommunications / network traffic: large internet and cloud
  outages, AWS 2017 and 2021, Fastly 2021, the 2024-07-19 endpoint-software crash) as a
  productivity shock to tech stocks.
- **C7 `fee-congestion`** (network traffic / queueing on blockchains: mempool congestion and
  fee spikes as unmet demand).
- **C8 `flu-absenteeism`** (public health beyond outbreaks: CDC ILI above its seasonal norm,
  FluView keyless 1997-, as a labour-supply shock).
- **C9 `estate-liquidation`** (demography of mortality: excess deaths among the old force
  estate sales of stocks).
- **C10 `crime-cycle`** (criminology: property crime as a real-time gauge of hardship).
- **C11 `fireball-omen`** (astronomy beyond the sun: CNEOS bolide reports, keyless 1988-, as
  unnoticed or frightening sky events).
- **C12 `soil-moisture`** (agriculture and soil science: corn-belt soil moisture in July
  pollination as a yield shock).
- **C13 `creep-rupture`** (materials beyond wide-21: Larson-Miller creep, time spent at a high
  stress sets the time to rupture; market form: months spent at high valuation as a crash
  hazard).
- **C14 `prediction-error`** (neuroscience: dopamine reward-prediction error; the market reacts
  to the surprise, not the level, and learns at a rate set by surprise variance).

### Score

| # | F1 not announced | F2 not price-driven | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| C1 `hack-drift` | pass (a, b): thefts are not announced | with controls: the loot in USD scales with token prices and value locked, hacks cluster in bull markets | 1 (theft, laundering sales, runs on similar protocols) | 2 (USD stolen spans three orders of magnitude) | 1 (Liu-Tsyvinski's sample ends 2018-05; Corbet et al. use hacks to 2018 `[memory]`; almost all non-exchange hacks are later) | 1 (114 non-exchange events of USD 10 m or more, nearly independent) | 1 (no gate in the record) | 1 | -1 | **6** | 2% |
| C2 `crackdown-shock` | pass (a) | with controls (regulators act after bubbles) | 1 | 1 (events, no natural size) | 1 | 1 | 1 | 1 | -1 | 5 | - | 
| C3 `court-ruling-shock` | pass (a) | pass | - | - | - | **0** (fewer than ten rulings) | - | - | - | - | filtered (power) |
| C4 `scotus-business` | partly: opinion days are announced, the case outcome is priced as a probability | pass | 0 (index-level reach near zero: decisions hit single firms) | 1 | 1 | 1 | 1 | 1 | 0 | 5 (cause 0) | 0.3% |
| C5 `news-novelty` | pass (b) | with controls (news follows prices) | 0 | 2 | 1 | 1 (1927-1963 months) | 1 | 0 (the narrative-news channel died in W34 on the same corpus and years) | -1 | 4 | 0.5% |
| C6 `cloud-outage` | pass (a) | pass | - | - | - | 0 (four or five outages that reached the whole economy) | - | **dead class**: a one-day productivity or mood shock (W31 `air-disaster-mood`, wide-22 E3 `blackout-cascade`) | - | - | filtered |
| C7 `fee-congestion` | pass (a) | **fail**: fees and congestion follow price and volume | - | - | - | - | - | - | - | - | filtered |
| C8 `flu-absenteeism` | fails as a flow (CDC publishes ILI weekly, read as news); passes as a premium (b) | pass | 0 (size: a severe season costs about 0.1% of GDP `[memory]`) | 2 | 1 | 1 (28 seasons) | 1 | 0 (outbreak channel dead in W30) | 0 | 5 (cause 0, size) | 0.3% |
| C9 `estate-liquidation` | pass (a) | pass | - | - | - | 0 (one large episode, 2020-21) | - | size: excess estates of a bad year are tens of USD bn of stock sold over a year or more, against about USD 500 bn traded a day | - | - | filtered (size, power) |
| C10 `crime-cycle` | **fail**: crime statistics are published with a lag and read as news; monthly national counts need a key (FBI API) | - | - | - | - | - | - | - | - | - | filtered (F1, data) |
| C11 `fireball-omen` | pass (a) | pass | - | - | - | - | - | **no channel**: almost nobody notices; the mood class is dead (W31) | - | - | filtered |
| C12 `soil-moisture` | pass (a) | pass | - | - | - | - | - | **dead channel**: the food-price link was absent in W32/R32; grains are not a live asset | - | - | filtered |
| C13 `creep-rupture` | pass (b) | **fail**: time at high valuation is a price statistic (CAPE, `cape-tilt` dead, invest-1) | - | - | - | - | - | - | - | - | filtered |
| C14 `prediction-error` | **fail**: the surprises are scheduled macro releases (finance literature, ann-1's field) | - | - | - | - | - | - | - | - | - | filtered |

**C2 has no keyless event list**: Auer and Claessens' list sits in a paper appendix, and a list
rebuilt from memory tonight would be picked with hindsight (only the crackdowns that moved
prices are remembered). Parked (data), not gated.

**Size check (shown, not part of the rule).** C1's flow channel is small: USD 2-3 bn a year
stolen from non-exchange targets `[memory]`, laundered over days to weeks, against ETH spot
volume of roughly USD 10-20 bn a day; even a USD 600 m theft sold over ten days is well under
1% of volume. A real effect would have to come from the run / repricing channel (the premium
form), which is what the 7-day drift after the news measures. C9 fails the size check (above).

**Picked by the rule.** C1 scores 6, the only candidate at 6 with keyless data and more than
a handful of independent events. **Gated: C1 as W37 `hack-drift`** (card `cards/wide-23.md`,
pushed before any return was read; the card calls W37 provisional because #202 had taken W36
and was still open; no other branch took W37, so the id stands). The replication **R37** is fixed in the same card before any number:
the same design on BTC with the **other** events (thefts from centralised exchanges, 2012-2025),
so it adds independent events, as gate-null's replication step asks. C2 (5) has no event list;
C4 and C8 score 5 only with cause 0 and fail their reach. No second gate (W38 is not used).

## Step 3. W37 `hack-drift` gate

The rule, data, placebo family, gate, the replication R37 (run only after a pass), shown cells,
power and guess are in [`cards/wide-23.md`](cards/wide-23.md), pushed before any number (commit
4277803, 21:32 UTC). Code: `research/lib/wide23_events.py` (pure functions, tested offline in
`tests/test_wide23.py`) and `research/lib/wide23.py` (fetch and run). Results:
`research/results/hack-drift.md`.

**A slip in the card, found while writing the tests (before any number), not edited:** the card
says the placebo step of 23 days "is not a multiple of a week". The step is not, but five of the
40 shifts (k = 7, 14, ..., 35, i.e. 161 .. 805 days) are whole weeks and keep each event's
weekday. The dose has no weekly clock, so this only matters if weekday return patterns line up
with hack days; the shift set is used as written.

### Dry run (counts only, 2026-11-25 21:34 UTC)

Hack list fetched once (`wide-23/defillama/2026-11-25/hacks.json`, 0.8 MB, 1,377 rows): events
of USD 10 m or more dated to 2025-10-31: **114 gate events (G, not `CEX`), 54 replication
events (X, `CEX`)**. ETH closes 3,452 (2016-05-18 .. 2025-10-31); **gate rows 3,412 days,
2016-06-21 .. 2025-10-23, no gaps, 109 event days in the rows.** The 30-day control window
means the first row is 2016-06-21, so the frozen rule leaves out the one G event before it
(the DAO theft, listed 2016-06-17, USD 60 m): a consequence of the card's rows, not changed.
R37 (not run unless W37 passes): BTC 5,050 closes, 4,976 rows 2012-01-30 .. 2025-10-23, one gap,
54 event days.

## What came out (one real run, 2026-11-25 21:35:44 UTC)

### W37 `hack-drift`: fails (no effect; the positive sign comes from one event)

**One doubling of the USD stolen from non-exchange targets goes with +0.28% on ETH over the
week after the listed date (t +0.68, 3,412 days, 109 event days, 2016-06 .. 2025-10), against
the predicted negative sign; the true t ranks 38 of 41 earlier-dose calendars. Dead by the
gate: no card for a strategy. R37 is not run** (the card runs it only after a pass). Held-out
year untouched. Table: `results/hack-drift.md`.

**Reading after the review of this PR (post hoc, below): no effect, t about 0.** The positive
sign comes from one event, LuBian (USD 3.5 bn, weight 9.45, listed 2020-12-28), that was not
public at its listed date; without it b is -0.003 (t -0.01, rank 31).

| Cell (ETH, 7 days from the end of day d+1, controls r7 and r30, unless named) | b, % per unit | t | Rows |
|---|---:|---:|---:|
| **Gate: log2(USD stolen / 5 m), non-exchange thefts of USD 10 m or more** | **+0.278** | **+0.68** | **3,412** |
| Reaction, days d-1 .. d+1, no controls (the channel's first link) | -0.056 | -0.27 | 3,412 |
| BTC, gate design (BTC rows from 2012) | -0.002 | -0.01 | 4,976 |
| ETH minus BTC | +0.175 | +0.89 | 3,412 |
| 30-day horizon, NW 30 | -0.784 | -0.86 | 3,389 |
| Binary dose (1 per event, not per unit; 114 events on 109 days) | -0.816 | -0.59 | 3,412 |
| Events of USD 50 m or more only | +0.590 | +1.30 | 3,412 |
| After Liu and Tsyvinski's sample (d >= 2018-06-01) | +0.403 | +0.98 | 2,702 |

- **There is no reaction to continue.** Over the theft day and the day after, ETH moves
  -0.06% per doubling (t -0.27): even a USD 600 m theft (about 7 units) goes with about -0.4%
  over two days, inside ETH's daily noise of about 4%. The channel's first link (the market
  notices) is absent at index level, so a drift was unlikely. As run, the week after leans
  positive and the USD 50 m+ cell more so (t +1.30), but both come from LuBian: without it
  they are t -0.01 and +0.65 (post hoc, below).
- **Post-sample** (after Liu and Tsyvinski's 2018 sample, nearly all the events): t +0.98 as
  run, +0.32 without LuBian; BTC is flat (t -0.01; -0.49 without LuBian). Their hack-attention
  result is not reproduced by the thefts themselves. (Their measure is Google searches, not
  thefts; this gate tests the thefts.)
- The 30-day horizon and the binary dose have the predicted sign but |t| under 1: noted only.
- **The null is close to normal and slightly left-shifted** (earlier-dose placebos: SD 1.02,
  5% with |t| >= 2; 5/50/95% -1.85 / -0.60 / +1.19; extremes -3.61 at k = 368 days, +1.74).
  The two surrogate families agree with it on width and on the verdict: phase-randomised SD
  1.13, 10% past |t| 2, rank 27 of 41; random-day SD 1.08, 8%, rank 30 of 41 (without
  LuBian: 1.14 / rank 20 and 0.94 / rank 27, against the placebos' 1.02). In this one event
  gate the families agreed, unlike wide-22's persistent macro dose; one gate does not settle
  when they disagree (gate-null-2, PR #207, open, studies exactly this). The phase surrogate
  turns a spike train into a smooth series, so it is the weaker model here. The one far placebo (-3.61) is a single shifted calendar, the kind of
  draw a 40-placebo family shows; it does not bear on the verdict.
- My guess (b < 0, t between -1.5 and +0.5, middle rank, placebo SD 0.9-1.2, pass 2%) was wrong
  on the sign and the rank (t +0.68, rank 38), right on the null's width (1.02).

Label: **kill-only** by `gate-null.md` step 7 (smallest p 1/41 = 0.024 above the family bar and
the register's 9.9e-5). A kill on its own t (|t| < 1 as run and without the late events).

**Correction (review of PR #205):** this write-up first said the card's disclosure-date caveat
"could only have produced a false pass". That holds only for a disclosure a few days late,
whose reaction falls inside the outcome window. A disclosure months or years late (LuBian,
Mirror) and amounts revised after the fact put dose on days when the market knew nothing:
noise in the dose, which pulls b toward zero, the false-kill direction. With the power the
card computed (t about -1.1 at the published size), this is a weak kill: fine for a kill-only
gate, not evidence that thefts have no effect.

### Post hoc: events not public at their listed date (added after the number, on review)

Found by the PR review (2026-11-25, after the real run), checked here with the same code
(`wide23.py posthoc`, 21:57 UTC; tables in `results/hack-drift.md`, section "Post hoc"); not a
rule and not a gate. Two G events were not public at their listed date:

- **LuBian** (USD 3.5 bn, `targetType` Other, listed 2020-12-28, weight log2 700 = 9.45; every
  other G event is at most USD 0.62 bn): the theft of 127,426 BTC from a mining pool was made
  public only in 2025-08 (Arkham, as the review reports). Its listed date opens ETH's best
  week of the sample (ln C(d+8)/C(d+1) = +0.41, 2020-12-29 .. 2021-01-05). One event with
  1.4 times the next weight on a +41% week sets the sign.
- **Mirror** (USD 90 m, listed 2021-10-08): its own description says it ran to 2022-05-17 and
  was discovered then.

| Cell (post hoc, events dropped only) | b, % per unit | t | Rank of 41 | Rows |
|---|---:|---:|---:|---:|
| Gate as run | +0.278 | +0.68 | 38 | 3,412 |
| **Without LuBian** | **-0.003** | **-0.01** | **31** | 3,412 |
| Without LuBian and Mirror (events not public at their listed date) | -0.023 | -0.06 | 31 | 3,412 |
| Without LuBian: reaction days d-1 .. d+1 | -0.110 | -0.51 | - | 3,412 |
| Without LuBian: BTC | -0.145 | -0.49 | - | 4,976 |
| Without LuBian: ETH minus BTC | +0.050 | +0.29 | - | 3,412 |
| Without LuBian: 30-day horizon | -1.240 | -1.37 | - | 3,389 |
| Without LuBian: binary dose (1 per event) | -1.165 | -0.86 | - | 3,412 |
| Without LuBian: USD 50 m or more | +0.234 | +0.65 | - | 3,412 |
| Without LuBian: d >= 2018-06-01 | +0.110 | +0.32 | - | 2,702 |

Without LuBian the earlier-dose placebos have SD 1.02 (12% past |t| 2), the phase surrogates
1.14 (rank 20), the random-day surrogates 0.94 (rank 27). Without both late events: placebo SD
1.00, phase rank 20, random-day rank 16. Every cell has |t| under 1.4; the 30-day and binary
cells lean to the predicted sign, as before, and are noted only.

**A note on the code against the card:** `rows` requires every close from C(d-29) to C(d+8),
while the card names only C(d-29), C(d+1) and C(d+8) (and the controls need C(d-6)). ETH has
no missing day in the span (0 gaps), so the rows are the same either way.

## Family count and status

One mechanism added and closed by its gate (W37 `hack-drift`). The thirteen others are parked,
filtered or dead by size or channel and are **not counted**, as in wide-12 .. wide-22; each has
a `note` row in `tries.md` (no number computed) and a line in `ideas.md`.

**Count: 105 mechanisms (104 after #202 + W37), 29 tested by a strategy, none passed; 33 gates
(32 + W37), two kill-only passes (W32, W36), each killed by its replication (R32, R36).** The
next strategy test is read at p < 0.10 / 105 = 0.00095 (family) and the register's bar.
Published effects tested after publication: 1 more
(the hack channel of Liu and Tsyvinski 2021 / Corbet et al. 2020, in its theft form on ETH and
BTC, 2018-2025): dead.

Rows logged in `tries.md`: 1 `screen` (`hack-drift`), 13 `note` rows (one per candidate
scored but not gated) and 1 `note` row for the post-hoc sensitivity. Data downloaded: 0.8 MB (the hack list; one call, plus one format probe
of the same size).

## Next

1. **The crypto-crime channel is closed at index level, weakly.** The public thefts (at most
   USD 0.62 bn, Ronin) do not move ETH or BTC measurably on the day (t -0.27; -0.51 without
   LuBian) or in the week after, so the flow and run channels are too small, as the size check
   said. The kill is weak: about 110 events, dates without publication times and two events
   listed long before they were public. A rerun would need disclosure dates per event. A test on the hacked protocols' own tokens (where Corbet et al. find their
   effects `[memory]`) needs token prices this project does not hold and is not a live asset.
2. **C2 `crackdown-shock`** (unscheduled regulatory actions against crypto) is the one parked
   candidate with a real channel and published effects; it needs a dated event list built
   without hindsight (a source that lists every action, not the remembered ones).
3. **Method**: in this one event gate the earlier-dose placebos, phase surrogates and
   random-day surrogates gave similar widths (SD 0.94-1.14). wide-22 found them to disagree
   for a persistent dose; when they do is the subject of gate-null-2 (PR #207, open). For
   event doses the random-day family is the natural surrogate, the phase family the weaker one.
4. **Curated event lists need a public-date check** before a gate: DefiLlama's list carries
   no publication date, and its largest entry was back-filled five years after its listed
   date.
