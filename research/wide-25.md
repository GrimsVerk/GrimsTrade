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
critical minerals, extreme-value theory (wide-24, PR #215, open). Mechanisms scored there are
not scored again.

**New fields tonight**: comparative politics (cabinets, coups, leaders, party systems),
environmental health (air quality), software engineering beyond scheduled releases (developer
activity, vulnerability disclosures), remote sensing (night lights), process safety
(industrial accidents), transport networks (rail traffic), food and drug safety (recalls),
linguistics of official documents (the Beige Book) and cryptography (quantum risk). One
legal-docket candidate (sanctions designations) is noted as a data lead for wide-23's parked C2,
not scored again.

**Count carried in** (provisional, after #215 lands): **108 mechanisms, 29 tested by a
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

## Step 2. Fourteen mechanisms, scored (2026-11-25 23:10 UTC, before any price was read)

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
return was read; id W41 / R41 provisional: wide-24's PR #215, open, takes W40 and leaves W41
unused). The replication **R41** is fixed in the same card: the same event definition on annual
JST returns, 1921-1959 (years before the gate's), 15 countries. No second gate (W42 not used).

## Step 3. W41 `cabinet-collapse` gate

(Filled after the dry run and the real run.)
