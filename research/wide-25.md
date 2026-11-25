# Wide 25: fourteen mechanisms from comparative politics, environmental health, software engineering, remote sensing, process safety, transport, food safety, official-document linguistics and cryptography, scored before any price, the top one gated

Research run wide-25, 2026-11-25 (night run, WIDER lane). Branch `wide-25` (from `main`
ee7ba63), PR into `main`. Research only: fake money, keyless public data, no change to the gym,
the daily runner or the live strategies. Train only: no bar or event after 2025-10-31 is used.

Fields already mined are left out (from the headers of `wide-1` .. `wide-24`, wide-15's step-1
table and `ideas.md`): physics, statistical physics, signal processing, control, information
theory, networks of prices (wide-1, wide-18); ecology, epidemiology, immunology, neuroscience,
evolutionary game theory, queueing, reliability (wide-1); pharmacokinetics, seismology,
actuarial science, materials fatigue, metrology, astronomy and chronobiology, hydraulics
(wide-1 .. wide-6); demography (cohorts), anthropology of calendars, tax law, catastrophe
meteorology, heliophysics, software release engineering (scheduled upgrades), sport sociology,
oceanography (wide-7 .. wide-9); procurement, currency boards, agricultural economics,
securities law, real-estate finance, payments engineering (wide-10, wide-11); conflict studies,
bank regulation, FX intervention (wide-12, wide-13); public finance, administrative law
(Federal Register counts), legislative studies (roll calls), power systems, hydrology x mining
(wide-15); biology, epidemiology, climate (wide-17); meteorology, operations research
(wide-19); economic history, psychology, sociology, demography of age structure, word-count
linguistics (wide-20, panic-words-1); hydrology and river freight, oceanography, solar physics,
volcanology, chemistry, materials (wide-21); energy systems, freight, game theory, network
contagion, rational inattention, frost, habituation (wide-22); cybercrime, court rulings, KL
news novelty, cloud outages, influenza, estates, crime counts, bolides, soil moisture, creep
(wide-23); seismology as damage, supply networks, renewal processes, sport, mega-events,
shipping, cable cuts, white-collar crime, livestock disease, migration, supply-chain pressure,
critical minerals, extreme-value theory (wide-24, PR #215, open when this lane started, merged
before this lane's PR; `main` merged into this branch). Mechanisms scored there are
not scored again.

**New fields tonight**: comparative politics (cabinets, coups, leaders, party systems),
environmental health (air quality), software engineering beyond scheduled releases (developer
activity, vulnerability disclosures), remote sensing (night lights), process safety
(industrial accidents), transport networks (rail traffic), food and drug safety (recalls),
linguistics of official documents (the Beige Book) and cryptography (quantum risk). One
legal-docket candidate (sanctions designations) is noted as a data lead for wide-23's parked C2,
not scored again.

**Count carried in** (after #215, merged during this lane; `main` ee7ba63 had 107 / 29 / 35
without it): **108 mechanisms, 29 tested by a
strategy, none passed; 36 gates, two kill-only passes (W32, W36), each killed by its
replication (R32, R36).** As in wide-12 .. wide-24, only mechanisms that get a gate or a
strategy test enter the count.

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-25 22:31): **4,328 tries,
N 1,123 for a new pick; measured rho 0.55 gives N_eff 509: a new rule needs z >= 4.70 against
`tsmom12`, Bonferroni p <= 9.8e-5.** Family bar with this run's gate: p < 0.10 / 109 = 0.00092.

Method as wide-21 .. wide-24: wide-11's filters F1 (not announced: an unscheduled flow (a) or
a premium (b)) and F2 (not price-driven; passing only with controls costs 1 point), then
wide-10's points (structural cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1),
plus keyless data, a size check and a duplicate check against the record. Gates follow
`research/gate-null.md` (40 placebos, the rank decides, t >= 2 also required, rule pushed
before any number, one dry run with counts only, then one real run). `[memory]` marks a
literature fact not checked tonight.

## Step 1. What the record already holds near these fields

Searched `research/` and `docs/` on 2026-11-25 for: election, cabinet, political, coup,
ParlGov, no-confidence, terror, sanction, OFAC, developer, GitHub activity, CVE, vulnerab,
bankrupt, recall, openFDA, strike, protest, riot, night light, VIIRS, river level, Rhine,
barge, PHMSA, derail, wildfire, air quality, smog, PM2.5, Beige Book, docket. Found:

- **Politics**: W27 `congress-workload` (wide-15: weekly roll-call counts as a Pastor-Veronesi
  political-uncertainty premium on SPY; dead, t -0.19, rank 25/41); W25 `act-haven` (GPR acts,
  dead); wide-22 G1 `debt-ceiling-attrition` (filtered). "election" hits are the presidential
  cycle and halving notes of the finance lanes. Nothing on cabinets, coups or leaders.
- **Sanctions and vulnerabilities**: data-wide-1 inventoried OFAC and the CISA KEV list (no
  idea built on them); wide-23 C2 `crackdown-shock` parked for want of a dated list.
- **Recalls, night lights**: data-wide-1 lists openFDA and NASA Black Marble (login) only.
- **Air quality**: wide-17 mentions PM2.5 in passing; no candidate.
- **Rivers**: wide-21 S3 `river-freight` (Mississippi, parked: size); hydrology is mined.
- Strikes: wide-20 P12 `strike-idleness` (parked: BLS asks for a contact e-mail).
- Beige Book, dockets, derailments, wildfires, protests: nothing.

## Step 2. Fourteen mechanisms, scored (2026-11-25 23:00 UTC, before any price was read)

(Time corrected on review: the first pushed version said 23:10 UTC, a slip; the table was
written before the card's commit at 23:01 UTC.)

**Disclosure.** Before this table, format and coverage only (no price, no return, no statistic
involving a price): the ParlGov cabinet table (`view_cabinet.csv`, 1.8 MB; field names, and per
country the first and last cabinet start and the number of distinct starts); the CPDS
government-composition codebook (the xlsx was fetched but not opened); the file names, header
lines and first/last months of the cached Ken French international country returns (UK.Dat
1975-01 .. 2025-12, Malaysia.Dat 1994-01 .. 2001-10).

### The mechanisms (cause story each)

- **P1 `cabinet-collapse`** (comparative politics: cabinet durability). A government that falls
  between elections and is replaced in the same parliament raises policy uncertainty and doubt
  about the next cabinet's life. Pastor and Veronesi (JF 2012, JFE 2013 `[memory]`) price
  political uncertainty: prices fall when it rises, holders earn a premium afterwards. Bernhard
  and Leblang (2006 `[memory]`) find cabinet dissolutions and formations move markets in
  parliamentary democracies, samples to about 2000. Tradable form: the country's index against
  the other developed markets over the six months after a mid-term cabinet start.
- **P2 `coup-shock`** (political science: coups, Powell and Thyne's list, keyless). A coup is
  an unscheduled shock to property rights.
- **P3 `leader-death`** (political science: Jones and Olken, QJE 2005 `[memory]`: leaders who
  die of natural causes in office change growth paths; Archigos list).
- **P4 `fragmentation-premium`** (party systems: the effective number of parliamentary parties
  or minority government as a level of political risk that earns a premium).
- **P5 `smog-cognition`** (environmental health / atmospheric chemistry: Heyes, Neidell and
  Saberian, NBER 2016 `[memory]`: Manhattan PM2.5 lowers same-day S&P 500 returns through
  traders' cognition and mood; EPA daily files are keyless).
- **P6 `dev-activity`** (software engineering: commit activity in Bitcoin Core and go-ethereum,
  from a git clone, as a fundamental that holders under-weight).
- **P7 `cve-disclosure`** (software security: NVD vulnerabilities in Bitcoin Core and Ethereum
  clients as a repricing of the chain's security).
- **P8 `sanctions-designation`** (legal dockets: OFAC SDN additions with digital-currency
  addresses, Tornado Cash 2022 and others, as a crackdown on crypto).
- **P9 `night-lights`** (remote sensing: satellite night lights as true growth against reported
  GDP, Henderson, Storeygard and Weil, AER 2012 `[memory]`).
- **P10 `process-accident`** (process safety: refinery fires, chemical plant explosions,
  pipeline ruptures as supply shocks).
- **P11 `rail-carloads`** (transport networks: weekly rail traffic as a real-time activity gauge
  ahead of official data).
- **P12 `recall-wave`** (food and drug safety: openFDA recall counts as a consumer-trust shock).
- **P13 `beige-book-tone`** (linguistics of official documents: negative tone in the Fed's
  Beige Book text, eight a year since 1970, as a macro-risk premium).
- **P14 `quantum-threat`** (cryptography: papers that lower the qubit cost of breaking
  elliptic-curve signatures as a slowly rising break risk for BTC and ETH).

### Score

| # | F1 not announced | F2 not price-driven | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| P1 `cabinet-collapse` | pass (b): a political state, unplanned | with controls: governments fall after bad economies and market falls | 1 (policy uncertainty, a priced risk in theory) | 1 (an event, no natural size) | 1 (Bernhard-Leblang samples end about 2000 `[memory]`; half the gate's months are later) | 1 (18 markets x 47 years, perhaps 100-200 nearly independent events) | 1 (no cabinet gate in the record) | 0 (the Pastor-Veronesi premium was W27's channel, dead on US roll calls) | -1 | **4** | 3% |
| P2 `coup-shock` | pass (a) | with controls (coups follow crises) | 1 | 1 | 1 | **0** (no coup in a market with cached returns since 1975 apart from a handful; Thailand and Turkey are not cached) | 1 | 1 | -1 | - | filtered (power) |
| P3 `leader-death` | pass (a) | pass | 1 | 1 | 1 | **0** (a handful of natural deaths in office in the 21 French markets since 1975) | 1 | 1 | 0 | - | filtered (power) |
| P4 `fragmentation-premium` | pass (b) | with controls: fragmentation rises after financial crises (Funke, Schularick and Trebesch, EER 2016 `[memory]`) | 1 | 2 | 0 (no return paper known to me) | 1, weakly (a persistent dose that changes at elections: a few swings per country) | 1 | 0 (same premium as W27) | -1 | 4 | 1% |
| P5 `smog-cognition` | pass (a) | pass | - | - | - | - | - | **dead class and horizon**: a same-day mood or cognition dip (W31 `air-disaster-mood`, W16 storms), not a trade at the book's weekly horizon | - | - | filtered |
| P6 `dev-activity` | pass (b) | with controls: developers and funding follow prices | 0 (no link from commits to coin demand at a monthly horizon) | 2 | 0 | 1 (monthly 2011-2025, persistent) | 1 | 1 | -1 | 4 | 0.5% |
| P7 `cve-disclosure` | pass (a) | pass | 0 (most entries are minor; the few critical bugs were fixed before disclosure) | 1 | 0 | 0 (a few dozen, a handful critical) | 1 | 0 (W37: security news does not move ETH at index level) | 0 | - | filtered (power) |
| P8 `sanctions-designation` | - | - | - | - | - | - | - | **duplicate**: a subset of wide-23 C2 `crackdown-shock` (scored there, parked for want of a dated list); not scored again. Noted for C2: the OFAC SDN list is a complete official list of one kind of action, if per-entry dates can be had keyless | - | - | not scored |
| P9 `night-lights` | pass (b) | pass | 1 | 2 | 1 | 1 | 1 | 1 | 0 | - | filtered (data: NASA Earthdata and the EOG archive need a login) |
| P10 `process-accident` | pass (a) | pass | - | - | - | - | - | **no reach**: hits product prices and single firms, no live asset | - | - | filtered (reach) |
| P11 `rail-carloads` | **fail** as a flow: a scheduled weekly release read as news | - | - | - | - | - | - | duplicate of wide-22 T1 (freight as an output gauge, parked); history not keyless by script `[memory]` | - | - | filtered (F1, data) |
| P12 `recall-wave` | pass (a) | pass | - | - | - | - | - | **no reach**: single firms | - | - | filtered (reach) |
| P13 `beige-book-tone` | fails as a flow (scheduled release); passes as a premium (b) | with controls: tone follows the economy and markets | 0 (a noisy macro summary, priced on release) | 2 | 0 | 1 (about 440 reports) | 1 | 0 (narrative-text channel dead in W34; macro text heavily studied) | -1 | 3 | 0.3% |
| P14 `quantum-threat` | pass (b) | pass | 0 (no break within any trading horizon) | 1 | 0 | **0** (a handful of milestone papers) | 1 | 1 | 0 | - | filtered (power) |

**Size check (shown, not part of the rule).** P1: Italian, Belgian or Japanese government
crises move their markets by a few percent around the change `[memory]`; a premium for holding
through the following months of uncertainty of 1-2% would be in line with a reaction of that
size reversing, near zero if the change was expected. P2, P3, P14 fail on events, P5 on horizon
and class, P10 and P12 on reach.

**Picked by the rule.** P1, P4 and P6 tie at 4, the top of the scored set (lower than the 5-6
of recent picks: no candidate tonight combines a published effect, a fresh channel and many
events). P1 is picked: it has a structural cause (as P4, unlike P6), nearly independent events
(P4's dose is persistent, a few swings per country) and keyless data with event dates as the
market saw them (ParlGov's start dates; a complete list of cabinets, not one chosen by market
impact). **Gated: P1 as W41 `cabinet-collapse`** (card `cards/wide-25.md`, pushed before any
return was read; the card calls W41 / R41 provisional because wide-24's PR #215 was open
and held W40; #215 merged before this PR and left W41 unused, so **W41 / R41 are final**). The replication **R41** is fixed in the same card: the same event definition on annual
JST returns, 1921-1959 (years before the gate's), 15 countries. No second gate (W42 not used).

## Step 3. W41 `cabinet-collapse` gate

The rule, data, placebo family, gate, the replication R41 (run only after a pass), shown cells,
power and guess are in [`cards/wide-25.md`](cards/wide-25.md), pushed before any number (commit
6b25042, 23:01 UTC). Code: `research/lib/wide25.py` (pure functions tested offline in
`tests/test_wide25.py`; load and run). Results: `research/results/cabinet-collapse.md`.

### Dry run (counts only, 2026-11-25 23:03 UTC)

ParlGov: 180 mid-term cabinet starts in the 18 countries, 1976-01 .. 2022-12 (17 of them
caretaker cabinets). **Gate rows 9,300 country-months (1976-01 .. 2022-12), 171 event months**
(France 22, Italy 27, Japan 22, Belgium 18, Finland 10, Norway 10, Austria 9, the Netherlands
and Sweden 8, Britain 7, New Zealand 6, Australia, Denmark and Ireland 5, Canada and Spain 3,
Germany 2, Switzerland 1). **Pooled lag-1 autocorrelation of the dose -0.007**: far under 0.8,
so gate-null-2's proposed "both families" rule does not apply (as the card expected). Spot
check of the British events: 1976-04 (Callaghan), 1990-11 (Major), 2007-06 (Brown), 2016-07
(May), 2019-07 (Johnson), 2022-09 (Truss), 2022-10 (Sunak): all right.

**A weakness of the frozen event rule, found in the dry run (before any number), not changed:**
ParlGov codes a caretaker cabinet that starts on election day and carries the new election's
date; the government formed after the negotiation then has the same election date as that
caretaker and counts as a "mid-term" start. 13 of the 180 events are such post-election
formations (Belgium 2007, 2011, 2014; Germany 2018; Spain 2016; the Netherlands 1977, 2017;
Austria 2000, 2003, 2020; Ireland 2020; Sweden 2019; Belgium 1992). The rule runs as written;
one shown cell (added now, before any number, not gating) drops events whose previous cabinet
is a caretaker that started on its own election day. Events after a non-caretaker cabinet that
started on election day (Britain 1976 and 1990, Norway, Sweden 1986 and 1990) are real
mid-term changes and stay in.

## What came out (one real run, 2026-11-25 23:05 UTC)

### W41 `cabinet-collapse`: fails (wrong sign; no premium)

**In the six months after a mid-term cabinet start, the country's market did 1.66% worse than
the other developed markets, not better (DK t -1.74, 9,300 country-months, 171 event months,
18 countries, 1976-2022), against the predicted positive sign; the true t ranks 41 of 41
earlier-dose calendars (the lowest). Dead by the gate: no card for a strategy. R41 is not run**
(the card runs it only after a pass). Held-out year untouched. Table: `results/cabinet-collapse.md`.

| Cell (excess over the other 20 markets, USD, six months from m+1, controls c1 c3 c12, country dummies, unless named) | b, % per event month | t | Rows |
|---|---:|---:|---:|
| **Gate** | **-1.663** | **-1.74** | **9,300** |
| Reaction e(m-1) + e(m), no controls, DK 2 (the channel's first link) | +0.086 | +0.15 | 9,360 |
| Horizon 3 months, DK 3 | -1.119 | -1.86 | 9,300 |
| Horizon 12 months, DK 12 | -3.120 | -2.60 | 9,300 |
| Local-currency returns | -1.197 | -1.44 | 9,300 |
| Without Italy and Japan | -1.323 | -1.13 | 8,172 |
| Rows m >= 2001-01 (after Bernhard and Leblang's samples) | -0.888 | -1.08 | 4,752 |
| Non-caretaker events only | -1.647 | -1.60 | 9,300 |
| Caretaker events only (17) | -1.726 | -0.85 | 9,300 |
| Without the 13 post-election formations (added after the card, before any number) | -1.773 | -1.77 | 9,300 |
| Count dose (equal to the gate: no row month has two events) | -1.663 | -1.74 | 9,300 |
| No controls | -1.683 | -1.74 | 9,300 |

- **No reaction, no premium.** Over the month before and the month of the new cabinet the
  country's market moves +0.09% against the others (t +0.15): by the time a new cabinet takes
  office, a fall at the crisis (if any) is either earlier than the month before or absent at
  this monthly resolution. Nothing positive follows: every shown cell is negative.
- **The negative side is noted only, not a lead.** The gate is one-sided (b > 0). The true t
  is below all 40 placebos and the 12-month cell reaches t -2.60, but the direction was not
  predicted, the null is wide (SD 1.24, below), a two-sided reading of rank 41 of 41 gives p
  about 2/41 = 0.05 before counting the 11 shown cells, and the post-2001 half (t -1.08) and the cell
  without Italy and Japan (t -1.13) are weaker. The 12-month cell is noted only because its
  sign was not predicted, its window overlaps the gate's (it contains the gate's six months),
  and it has no placebo of its own. A card for a negative drift (markets
  under-react to a weakened government) would have to be written before looking at
  independent data: R41's annual JST design on 1921-1959, with the sign b < 0, is the obvious
  candidate (`Next`).
- **The null is somewhat wide on the upper side** (earlier-dose placebos: SD 1.24, 8% past
  |t| 2, 5/50/95% -1.26 / +0.14 / +2.26, extremes -1.66 / +3.39). Shifts of 31-53 months lean
  positive (k 33: +2.84, 41: +2.23, 43: +3.39): a placebo dose 3-4 years before the outcome
  falls near the next regular election of a parliament, so these shifts may pick up a
  pre-election pattern (Pantzalis, Stangeland and Turtle, JBF 2000, report positive returns
  before elections `[memory]`); a guess, not tested. Random-month surrogates (shown) are
  centred and close to normal: SD 1.10, 5% past |t| 2, 5/50/95% -1.50 / +0.16 / +1.96; true
  t rank 39 of 41. The two families agree on the verdict.
- **Power, measured.** SE(b) is about 0.96% (b / t), as the card guessed (1.0%): a pass needed
  about +2% over six months after a mid-term change. The point estimate is -1.7% with its
  upper 95% bound near +0.2%: a premium of the size a pass needed is unlikely in these
  markets and years. A strong kill for the premium form as stated.
- **Event dates.** ParlGov's start dates are the dates the new cabinets took office (public on
  the day). Its one known coding quirk for this rule (caretaker cabinets from election day,
  dry run above) does not move the result (-1.77 without the 13 post-election formations).
- My guess (b near 0, t between -1.5 and +1.5, a middle rank, placebo SD 0.9-1.3, pass 3%) was
  wrong on t and rank (t -1.74, the lowest rank), right on the null's width (1.24) and on the
  verdict.

Label: **kill-only** by `gate-null.md` step 7 (smallest p 1/41 = 0.024, above the family bar and
the register's 9.8e-5). A kill on its own sign (b < 0, every shown cell negative).

## Family count and status

One mechanism added and closed by its gate (W41 `cabinet-collapse`). The thirteen others are
parked, filtered, dead by class or a duplicate and are **not counted**, as in wide-12 ..
wide-24; each has a `note` row in `tries.md` (no number computed) and a line in `ideas.md`.

**Count: 109 mechanisms, 29 tested by a strategy, none passed; 37 gates, two
kill-only passes (W32, W36), each killed by its replication (R32, R36)**: +1 mechanism and +1
gate over the count after #215 (108 / 29 / 36), which merged into `main` during this lane
(and was merged into this branch). Family bar p < 0.10 / 109 = 0.00092. Gate id
W41 / R41 final (W40 is #215's; W42 not used). Published effects tested after publication: 1 more (a
Pastor-Veronesi political-uncertainty premium after mid-term cabinet changes, in the spirit of
Bernhard and Leblang 2006, 18 developed markets 1976-2022, half after their samples): dead.

**Data terms.** ParlGov: Döring, Holger, Alexandra Quaas, Maike Hesse and Philip Manow
(2023), "Parliaments and governments database (ParlGov): Information on parties, elections and
cabinets in established democracies", development version (4 Nov 2023), parlgov.org; release
data: Döring and Manow, Harvard Dataverse, doi 10.7910/dvn/2vz5zc. parlgov.org's data and
about pages (read 2026-11-25 23:15 UTC, generic UA) give the citation but state no licence;
the Dataverse page answered the script with a bot challenge (HTTP 202, no content), so its
licence was not read and is not stated here; check it in a browser before any redistribution. Only statistics
derived from the table are committed. `view_cabinet.csv` sha256
bd39f73335e8bc49c00d5000ab5a68e7a8c41ca0eb17d8c89ff6d05ba93e6063 (1,783,351 bytes; manifest
`wide-25/parlgov/2026-11-25/`). CPDS (not used by the rule): Armingeon, Klaus, Sarah Engler,
Lucas Leemann and David Weisstanner (2025), "Supplement to the Comparative Political Data Set -
Government Composition 1960-2023", University of Zurich, Leuphana University Lueneburg and
University of Lucerne; its codebook asks users to quote the data set and the original sources;
the data page states no other terms.

Rows logged in `tries.md`: 1 `screen` (`cabinet-collapse`), 11 `robustness` rows (the shown
cells), 13 `note` rows (one per candidate scored but not gated). Data downloaded: 4.5 MB (ParlGov
`view_cabinet.csv` 1.8 MB; the CPDS codebook 0.2 MB and xlsx 2.5 MB, not used by the rule);
the French country returns were already cached (data-long-4).

## Next

1. **The political-uncertainty premium is closed at this horizon in two forms** (W27 roll
   calls on SPY, W41 cabinet changes on 18 markets). A third try should not reuse the premium
   story.
2. **The negative drift after cabinet changes is a post-hoc pattern, not a lead.** If a lane
   wants it, the honest test is a new card with b < 0 on independent years: R41's design
   (annual JST, ParlGov events, 1921-1959, 15 countries, 20 earlier-dose calendars), written
   before any number. Expect low power (about 15 countries x 30 usable years, annual returns).
3. **P8 `sanctions-designation`** is a data lead for wide-23's C2 `crackdown-shock`: OFAC's
   SDN list is a complete official list of one kind of action against crypto services, if
   per-entry designation dates can be had keyless (not checked tonight). The index-level size
   is likely small (most designated services are small).
4. **Method**: an event calendar with a known election clock (parliaments of 3-5 years) can
   make earlier-dose placebos near that clock lean one way (k 31-53 months here); a future
   political gate should either skip shifts near the term length or report the random-month
   family next to it, as here.
