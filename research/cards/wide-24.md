# wide-24 card: `quake-drift`, does a country's stock index keep falling against the world in the month after a damaging earthquake?

Lane wide-24, written 2026-11-25 (UTC), **before any return, event count or dose value was
read for this rule** (card pushed first; the commit time is in git). Field: seismology as an
economic shock. Candidate Q1 of `research/wide-24.md`, step 2. Gate **W40** and replication
**R40**: provisional ids (W38 / W39 are taken by the open PR #210; the merging lead may
renumber; the card keeps these ids).

## What was seen before this card (disclosed)

- First and last dates, time zone and currency of the 24 cached daily index files
  (`insure-2/raw-2026-11-18/yahoo`: AEX, AORD, ATX, BFX, BSESN, BVSP, FCHI, FTSE, FTSEMIB.MI,
  GDAXI, GSPTSE, HSI, IBEX, JKSE, KLSE, KS11, MXX, N225, NZ50, OMX, SSMI, STI, TA125.TA, TWII;
  first dates 1965 (N225) .. 2008 (OMX), last 2025-10-30/31) and of `yahoo-1d/2026-11-12/^GSPC`
  (1927-12-30 .. 2026-11-12). No price, no return.
- Natural Earth populated places (public domain), fetched 2026-11-25 22:27 UTC from
  `raw.githubusercontent.com/nvkelso/natural-earth-vector` (no robots.txt there: 404), 7,342
  places; field names only. GeoNames was not used (its robots.txt disallows all).
- The USGS ComCat catalogue cached by data-wide-1 (2026-11-19) was not opened; data-wide-1's
  write-up states its coverage (M >= 6 from 1900) and that magnitudes are the reviewed ones.
- The literature as remembered (below).

## Hypothesis

A large shallow earthquake under a country's cities destroys capital and stops production. The
quake is public in minutes, the damage is not: death tolls, damage estimates and supply-chain
stoppages come out over weeks (Carvalho, Nirei, Saito and Tahbaz-Salehi, QJE 2021; Boehm,
Flaaen and Pandalai-Nayar, REStat 2019 `[memory]`). Scholtens and Voorhorst (Earthquake Spectra
2013) report negative abnormal returns of the hit country's index for days to weeks after
large quakes, larger with more deaths `[memory]`. If the market under-reacts to slowly revealed
damage, **the hit country's index keeps falling against the other markets in the month after
the first full session of reaction: b < 0.**

Filters (wide-11 F1/F2): F1 passes weakly (a, b): the quake is unannounced, but public within
minutes (wide-13 filtered the commodity form for that reason); the drift form rests on slow
revelation of damage. F2 passes: earthquakes do not follow prices, so placebo calendars may move
both ways (gate-null step 1).

## Data (keyless)

- **Earthquakes**: the cached ComCat files `data-wide-1/usgs/2026-11-19/*.csv`, read with
  `datawide1.load_quakes` (one row per event id, the latest revision). Used: `type` earthquake,
  magnitude M >= 6.0, depth <= 70 km, origin time 1965-01-01 .. 2025-10-31 UTC. Origin times are
  exact; magnitudes are the reviewed ones (a real-time reader saw a first estimate, often 0.1-0.3
  off; for Tohoku 7.9 at first, 9.0-9.1 later): noise in the dose, not information about prices.
- **Declustering** (aftershocks): an event is dropped if an event of equal or larger magnitude
  lies within 300 km (epicentral, great-circle) in the 30 days before it. Its damage is inside
  the earlier event's outcome window.
- **Disclosure date**: an earthquake of M >= 6 is public at its origin time (global networks and
  newswires report it the same day). The dose uses only origin time, location, depth, magnitude
  and static population, never deaths or damage (known only later). Check before any pass is
  read: the 15 largest-weight events are listed with their dates, and each must be a quake that
  was reported on its date (no back-filled catalogue entry); an event that was not is dropped and
  the gate rerun as a disclosed correction.
- **Population**: Natural Earth populated places, `pop_max` (metro population, a recent value,
  held fixed over time: an anachronism, not price information), country by `adm0_a3`.
- **Markets** (25): the 24 cached indices above plus ^GSPC, daily `close` from the Yahoo JSON,
  null closes dropped, session date = local date of the bar's timestamp in the file's exchange
  time zone, nothing after 2025-10-31. Countries (`adm0_a3`): N225 JPN, TWII TWN, MXX MEX, JKSE
  IDN, NZ50 NZL, FTSEMIB.MI ITA, BSESN IND, ^GSPC USA, KS11 KOR, AORD AUS, GSPTSE CAN, KLSE MYS,
  STI SGP, HSI HKG, TA125.TA ISR, AEX NLD, ATX AUT, BFX BEL, BVSP BRA, FCHI FRA, FTSE GBR, GDAXI
  DEU, IBEX ESP, OMX SWE, SSMI CHE. Price indices in local currency. Markets that have large
  quakes but no cached file (Chile, Turkey, Greece, Peru, the Philippines, China, Iran) are out
  by data, not by outcome.

## Rule (frozen)

- **Exposure.** For event e (magnitude M, depth z) and market country c: S(e, c) = 100 x (sum of
  `pop_max` of the places of c whose hypocentral distance sqrt(d^2 + z^2) <= R(M)) / (sum of
  `pop_max` of all places of c), with R(M) = 40 km x 10^(0.45 (M - 6.5)) (about 24 km at M 6,
  40 km at 6.5, 67 km at 7, 190 km at 8, 530 km at 9: a rough radius of strong shaking, fixed
  here, not fitted). Weight w(e, c) = log2(1 + S): 1 at 1% of the country's place population
  exposed, about 5.4 at 40%.
- **Event session.** For market i in country c: D_i(e) = the local date of the origin time in
  i's time zone; s0 = the first session of i with date >= D_i(e). Dose D(i, s) = sum of w(e, c)
  over events with s0 = s (0 elsewhere).
- **Outcome.** y(i, s) = [ln C_i(s+1+H) - ln C_i(s+1)] - W_i(s), H = 20 sessions. The window
  starts at the close of session s0 + 1, whose date is after the quake's local date, so at least
  one full session of reaction is outside it. W_i(s) = mean over the other markets j of
  [ln C_j(t2) - ln C_j(t1)], where C_j(t) is j's last close on or before the date t, t1 = the
  date of i's session s+1, t2 = the date of i's session s+1+H; j counts only if both closes are
  within 7 calendar days of their dates; at least one j needed.
- **Controls.** r2(i, s) = ln C_i(s+1) - ln C_i(s-1) (the reaction, known when the window
  starts) and r20(i, s) = ln C_i(s-1) - ln C_i(s-21). Market dummies.
- **Rows.** Every session s of every market with s - 21 >= 0, session s+1+H present and dated on
  or before 2025-10-31, and the date of s in the **gate window 1998-01-01 .. 2025-10-31**.
- **Statistic.** Pooled OLS of y on the market dummies, D, r2, r20; t of b (the D slope) with
  Driscoll-Kraay standard errors (`gatepower.dk_fit`: scores summed by the calendar day of
  session s+1, Bartlett weights over day distance, 30 lags: the 20-session windows overlap and
  markets share world shocks).
- Predicted sign: **b < 0**.

## Placebo null (the decider)

Shifted calendars, both ways (quakes do not answer prices): every event's origin time moved by
23k days, k = -20..-1 and 1..20 (40 placebos; 23 is not a multiple of a week, but k = +-7 and
+-14 are whole weeks: noted, used as written). The whole 1965-2025 catalogue is shifted, so
events from before the gate window enter it and later ones leave it; shifted events past
2025-10-31 or before a market's first session drop. Weights stay with their (event, market)
pair. Same rows, same controls, same function (a `shift` argument).

**Dose autocorrelation and gate-null-2's proposed rule.** The dose is a sparse event series; its
pooled lag-1 autocorrelation (within market, session to session) is printed in the dry run and
expected near 0. The "both families" rule applies only at 0.8 or more; if it did, the pass would
also need rank <= 2 in the 40 random-day surrogates below.

## Gate (pass only if all hold)

1. b < 0.
2. t <= -2.
3. The true t ranks among the 2 lowest of 41 (empirical one-sided p = rank / 41 <= 0.049).

**Kill-only** (gate-null step 7): the events are nearly independent (dozens to a few hundred
(event, market) pairs, counted in the dry run), but the smallest p a rank shows is 1/41 = 0.024,
above the family bar (0.10 / 106 = 0.00094 relative to `main`; 0.00093 if #210 lands first) and
the register's 9.9e-5. A fail kills the idea; a pass says only "not dead yet".

**Replication R40, fixed now, run only if W40 passes** (independent events): the same rule,
placebos and pass conditions on rows dated **1965-01-01 .. 1997-12-31** (events before the gate
window: mostly Japan (N225 from 1965), plus Mexico and Indonesia from the early 1990s, the US,
and the other markets as their files begin). With few markets in the early years, W_i uses
whatever other markets exist (at least one).

## Shown, not gating

- Reaction (the channel's first link): r2 on D with market dummies, no other controls, DK 5
  lags; predicted b < 0. If there is no reaction, a drift has nothing to continue.
- 60-session horizon (H = 60, DK 90 lags): a later rebuild could reverse the drift.
- Own return, no world subtraction.
- Binary dose: 1 per event with S >= 1% (w >= 1), 0 otherwise.
- Fixed radius: R = 100 km for every magnitude.
- M >= 6.5 only.
- Japan only (N225).
- Without the Tohoku event (2011-03-11; the Fukushima accident is a second shock in its window).
- After Scholtens and Voorhorst's sample: rows dated 2012-01-01 or later.
- 40 random-day surrogates: each (event, market) weight put on a session drawn uniformly from
  that market's gate rows, seed 24; the rank of the true t.
- The 15 largest-weight events in the gate rows: date, market, M, S, w, y.
- The null's width: SD of placebo t, share with |t| >= 2, 5/50/95% quantiles, extremes.

## Power and my guess (written before any number)

A 20-session excess index return has an SD of about 4-5%. If there are about 150 (event,
market) pairs with a mean weight near 1.5, sum(w^2) is about 450 and SE(b) about 4.5 /
sqrt(450) = 0.21% per unit (more with cross-market correlation). A Tohoku-size event (w about 5)
followed by a 3% drift is b about -0.6, t about -2.8; a pass needs about -0.45% per unit. Most
exposures are small and the index reach of housing damage is weak. Guess: b near 0, t between
-1.5 and +1, a middle rank, placebo SD 0.9-1.2. Prior of a pass: 3%.

## On the outcome

Pass: check the disclosure dates of the 15 largest events (above), run R40 at once and report
both. Fail: dead, one `screen` row in `research/tries.md` (descriptive, not selectable); R40 is
not run. Every shown cell gets a `robustness` row.
