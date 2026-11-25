# wide-25 card: `cabinet-collapse`, does a country's market earn more in the months after a mid-term change of government?

Lane wide-25, written 2026-11-25, **before any return was read for this rule** (card pushed
first; the commit time is in git). Field: comparative politics (cabinet durability) x a
political-uncertainty premium. Candidate P1 of `research/wide-25.md`, step 2. Gate **W41**
(provisional: wide-24, PR #215, open, takes W40 and leaves W41 unused; the merging lead may
renumber), replication **R41** fixed below. No second gate (W42 not used).

## What was seen before this card (disclosed)

- ParlGov development data, `view_cabinet.csv` (parlgov.org, no robots.txt: 404; fetched once
  2026-11-25, 1.8 MB, 12,640 cabinet-party rows): field names, and per country the first and
  last cabinet start date and the number of distinct start dates. No market value.
- CPDS government-composition supplement (cpds-data.org, robots.txt allows `/wp-content/`):
  codebook read (it has the successor's investiture date and the reason the previous
  government ended, but **no date of the termination itself**); the xlsx was downloaded but
  not opened (no reader installed). Not used by the rule.
- Ken French international country returns (`F-F_International_Countries.zip`, cached by
  data-long-4 on 2026-11-24): file names, the header lines of `UK.Dat`, and the first and last
  month of `UK.Dat` (1975-01, 2025-12) and `Malaysia.Dat` (1994-01, 2001-10). No return value.
  Other lanes (data-long-4, e4 tests) have read these returns, never against a political dose.

## Hypothesis

When a government falls between elections (coalition break-up, lost confidence vote, a prime
minister's resignation) and a new cabinet takes office in the same parliament, investors face
more uncertainty about policy and about how long the new cabinet will last. Pastor and Veronesi
(Journal of Finance 2012; Journal of Financial Economics 2013 `[memory]`) model political
uncertainty as a priced risk: prices fall when it rises, and investors who hold through it earn
a premium afterwards. Bernhard and Leblang (Democratic Processes and Financial Markets, 2006
`[memory]`) report that cabinet dissolutions and formations in parliamentary democracies move
markets, with samples ending about 2000. If the premium is real and lasts beyond the month of
the change, **the country's market beats the other developed markets over the six months after
a mid-term cabinet start: b > 0.**

Filters (wide-11 F1/F2): F1 passes as a premium (b): the dose is a state (an unplanned change
of government), not a scheduled release. F2 passes only with controls: governments fall more
often after bad economies and market falls, so the gate carries the country's own past excess
returns as controls and the placebo calendars use **earlier doses only** (gate-null step 1).

## Data (keyless)

- Cabinets: ParlGov `view_cabinet.csv` (development version, fetched 2026-11-25 into
  `~/data/grimstrade/wide-25/parlgov/2026-11-25/`, read with `python -I` as untrusted data;
  only statistics are committed). One cabinet per `cabinet_id`. Fields used: `country_name_short`,
  `start_date`, `election_date`, `cabinet_id`, `previous_cabinet_id`, `caretaker`.
- Returns: Ken French international country returns, block 1 of each `.Dat` file ("Value-Weight
  Dollar Returns, All 4 Data Items Not Reqd"), column `Mkt`, % per month; -99.99 or less is
  missing. Months 1975-01 .. **2025-10** (train only: nothing after 2025-10-31).
- Markets with a dose (rows): the 18 countries in both sources: AUS, AUT, BEL, CAN, CHE, DEU,
  DNK, ESP, FIN, FRA, GBR, IRL, ITA, JPN, NLD, NOR, NZL, SWE. Hong Kong, Singapore and Malaysia
  enter only the comparison mean (no ParlGov data).

## Rule (frozen)

- **Event.** A cabinet c whose `previous_cabinet_id` p exists in the file and whose
  `election_date` equals p's: a new cabinet in the same parliament (no election in between),
  caretaker cabinets included. Its month is the month of c's `start_date`, public on that day.
- **Dose.** D(i, m) = 1 if country i has at least one event in month m, else 0. Defined for
  months from the month of i's first ParlGov cabinet start to **2022-12** (ParlGov may be
  incomplete after; the dry run prints each country's last start), missing outside.
- **Excess return.** e(i, m) = ln(1 + r(i, m)/100) - mean over the other markets j with a value
  in month m of ln(1 + r(j, m)/100) (all 21 French markets, i excluded).
- **Outcome.** y(i, m) = e(i, m+1) + ... + e(i, m+6): the six months after the event month.
- **Controls.** c1 = e(i, m), c3 = e(i, m-2) + e(i, m-1) + e(i, m), c12 = sum of e(i, m-11..m):
  the country's own recent excess return, the reaction month included. Country dummies.
- **Rows.** Every (i, m) of the 18 countries with D(i, m) defined, m from 1976-01, and every
  e(i, m-11 .. m+6) present.
- **Statistic.** OLS of 100 y on D, c1, c3, c12 and the country dummies; t of b (% over six
  months per event month) with Driscoll-Kraay standard errors: scores summed by month m, then
  Bartlett weights, 6 lags (overlapping six-month outcomes); `gatepower.dk_fit`.
- **Predicted sign: b > 0.**

## Placebo null (the decider, `research/gate-null.md`)

Earlier doses only: D_k(i, m) = D(i, m - k), k = 25, 27, ..., 103 months (40 placebos, odd, so
no shift is a whole number of years and the calendar of formation seasons is broken). Same
rows as the true statistic, except rows where D(i, m - k) is undefined (before the country's
first ParlGov cabinet: Spain before 1977-07) are dropped for that placebo. Same controls, same
function (a `shift` argument). Lag-1 autocorrelation of the dose is expected far under 0.8
(events are months apart), so gate-null-2's proposed "both families" rule does not apply; the
dry run prints it.

## Gate (pass only if all hold)

1. b > 0.
2. t >= 2.
3. The true t ranks among the 2 highest of 41 (empirical one-sided p = rank / 41 <= 0.049).

**Kill-only** (gate-null step 7): the events are nearly independent (the dry run counts them;
expected 100-200 in 18 countries over 47 years), but the smallest p a rank shows is 1/41 =
0.024, above the family bar (0.10 / 109 = 0.00092 after #215) and the register's 9.8e-5. A fail
kills the idea; a pass says only "not dead yet".

**Replication R41, fixed now, run only if the gate passes** (independent years): the same
construction on annual JST data before the gate's years. Outcome years t+1 = 1921 .. 1959,
without 1939-1946 and the `jstgates1.dropped` list; y(i, t+1) = JST ln(1 + eq_tr) -
ln(1 + bill_rate) minus that year's mean over the countries in the rows; dose D(i, t) = 1 if
country i has at least one ParlGov event (same definition) with start date in calendar year t;
controls y(i, t) and y(i, t-2) + y(i, t-1) + y(i, t); country dummies; Driscoll-Kraay by year,
2 lags; JST countries with ParlGov cabinets before 1959 (AUS, BEL, CAN, CHE, DEU, DNK, FIN, FRA,
GBR, IRL, ITA, JPN, NLD, NOR, SWE; dose defined from each country's first ParlGov start). 20
earlier-dose calendars k = 2..21 years. Pass: b > 0, t >= 2, the true t the highest of 21.

## Shown, not gating

- Reaction (the channel's first link): e(i, m-1) + e(i, m) on D, no controls, country dummies,
  DK 2 lags; predicted b < 0 (prices fall as uncertainty rises).
- Horizons 3 months (DK 3) and 12 months (DK 12).
- Local-currency returns (block 2 "Value-Weight Local Returns"), same comparison construction.
- Without Italy and Japan (the most frequent changes).
- Rows with m >= 2001-01 (after Bernhard and Leblang's samples).
- Non-caretaker events only, and caretaker events only.
- Count dose (number of events in the month) and no controls.
- Random-month surrogates (40, seed 2511): each country's events moved to months drawn
  uniformly without replacement from its own row months; rank of the true t.
- The null's width: SD of placebo t, share with |t| >= 2, 5/50/95% quantiles, extremes.

## Power and my guess (written before any number)

A country's monthly excess return over the others has an sd of about 4-5%, so a six-month sum
about 11%. With about 130 event months, SE(b) is about 11 / sqrt(130) = 1.0% (DK may add a
little). A pass needs about +2% over six months after a mid-term change, i.e. a premium of
about 4% a year for half a year: large for a risk premium, plausible only if the reaction
reverses. Guess: b near 0, t between -1.5 and +1.5, a middle rank, placebo SD 0.9-1.3
(independent events, normal-like null). Prior of a pass: 3%.

## On the outcome

Pass: check that the largest-weight events are dated by their start (not a later coding date),
run R41 at once and report both. Fail: dead, one `screen` row in `research/tries.md`
(descriptive, not selectable); R41 is not run.
