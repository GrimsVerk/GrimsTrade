# w41-neg-1 card: `cabinet-drift`, does a country's market do worse in the year after a mid-term change of government (annual JST, 1921-1959)?

Lane w41-neg-1, written 2026-11-26, **before any return was read for this rule** (card pushed
first; the commit time is in git). Next-steps lane queue item 7(d). Gate id **provisional
`W41n`** (the lead renumbers on merge). Kill-only. No replication is fixed: a pass says only
"not dead yet" and would need a third, independent sample.

## Why this card

W41 `cabinet-collapse` (wide-25, PR #221) predicted b > 0 (a political-uncertainty premium after
a mid-term cabinet start) on 18 French country markets, 1976-2022, and failed with the wrong
sign: b -1.66% over six months, t -1.74, the lowest of 41 earlier-dose calendars; its 12-month
cell had b -3.12%, t -2.60. That negative side was seen after the fact and is not evidence.
This card fixes the sign it suggests, **b < 0** (markets under-react to a weakened or new
government and drift down afterwards), and tests it on years W41 never touched: R41's annual
JST design, outcomes 1921-1959. Nothing about 1921-1959 returns was looked at by W41 or this
lane.

## What was seen before this card (disclosed)

- ParlGov `view_cabinet.csv` (cached by wide-25, sha256 bd39f733...; same file): per country
  the first cabinet start year, and the number of mid-term events (wide-25's `events`) and of
  event years with a start in 1919-1958: FRA 32 event years, FIN 20, BEL 18, DEU 15, NOR 13,
  SWE 12, GBR 7, ITA 7, NLD 6, JPN 5, AUS 4, DNK 4, CAN 2, CHE 2, IRL 0 (the 15 JST countries;
  8 of the 1919-1958 events are wide-25's post-election type). No market value.
- JST R6 (cached, read by jst-gates-1 and earlier jst lanes): its coverage is known from those
  lanes; no 1921-1959 statistic against a political dose has been computed by anyone.
- W41's result (above), which is why the sign is b < 0.

## Feasibility (step 1)

About 150 event years in 15 countries before the drop list and the 1939-1946 gap: enough for a
pooled annual test, low power (below). France has an event in most years (its dose varies
little; country dummies absorb its level). Testable: the card proceeds.

## Data (keyless, cached)

- Cabinets: ParlGov development version, `~/data/grimstrade/wide-25/parlgov/2026-11-25/
  view_cabinet.csv` via `research/macro.local.json` (untrusted, `python -I`). **Licence not
  read** (wide-25: parlgov.org states none; the Dataverse page was a bot challenge): only
  statistics are committed, **no ParlGov-derived event list or data file**.
- Returns: JST Macrohistory R6 (CC BY-NC-SA 4.0), `eq_tr`, `bill_rate`, `cpi` (for the
  hyperinflation drop), loaded with `jstgates1.load_jst`.

## Rule (frozen)

- **Countries (15):** AUS, BEL, CAN, CHE, DEU, DNK, FIN, FRA, GBR, IRL, ITA, JPN, NLD, NOR, SWE
  (JST countries with ParlGov cabinets before 1959; R41's list).
- **Event:** wide-25's definition unchanged (`wide25.events`): cabinet c whose previous cabinet
  p exists and has the same `election_date`; caretakers included; dated by c's `start_date`
  (public that day).
- **Dose:** D(i, t) = 1 if country i has at least one event with start date in calendar year t,
  else 0; defined for t from the year of i's first ParlGov cabinet start to 1958.
- **Returns:** x(i, t) = ln(1 + eq_tr) - ln(1 + bill_rate); a year is kept unless
  `jstgates1.dropped` (jst-autocorr-2 point 2: wars, closures, hyperinflation, interpolated
  years). d(i, t) = x(i, t) minus the mean of the kept x(j, t) over the 15 countries in year t.
- **Rows:** (i, t+1) with t+1 in 1921..1959 except 1939-1946, d(i, t+1) kept, D(i, t) defined,
  d(i, t-2), d(i, t-1), d(i, t) kept.
- **Statistic:** OLS of 100 d(i, t+1) on D(i, t), controls d(i, t) and d(i, t-2) + d(i, t-1) +
  d(i, t), country dummies; b in % per event year; Driscoll-Kraay t by year, 2 lags
  (`gatepower.dk_fit`).
- **Predicted sign: b < 0.**

## Nulls

1. **Earlier-dose calendars (shift rank):** D(i, t - k), k = 2..21 years (20 placebos); rows
   where D(i, t - k) is undefined are dropped for that placebo; same controls. Rank of the true
   t from the bottom among 21 (1 = lowest).
2. **AR-preserving bootstrap under H0 (pass condition; #204 / jst-autocorr-2 point 1: pooled
   pre-1966 JST tests need one):** `jstgates1.boot_model` / `simulate` on x over 1900-1959
   (AR(1) of the common mean and of each country's deviation, residuals drawn by whole
   historical year so the cross-country structure is kept, burn-in 30), 199 paths, seed 4101.
   The real dose is kept (the simulated returns are independent of it under H0); each path is
   masked to the real kept years and goes through the same statistic. p = (1 + #{t_boot <=
   t}) / 200.

## Gate (kill-only; "not dead yet" only if all hold)

1. b < 0 and t <= -2.
2. Shift rank 1 or 2 of 21.
3. Bootstrap p <= 0.05.
4. Both halves (outcomes 1921-1938, 1947-1959) have b < 0.

Otherwise dead. Kill-only by `gate-null.md` step 7: the smallest p a rank shows is 1/21 = 0.048,
far above the family bar (0.10 / 112 = 0.00089 if this counts as a 112th mechanism) and the
register's 9.8e-5.

## Shown, not gating

- The two halves (also gate condition 4).
- No controls.
- Without France (an event in most years).
- Without the post-election formations (wide-25's `post_election`: previous cabinet a caretaker
  that started on its own election day).
- Count dose (number of events in year t).
- The nulls' width: SD of the shift and bootstrap t, share past |t| 2, 5/50/95%.
- Pooled lag-1 autocorrelation of the dose on the rows.

## Power and my guess (written before any number)

A country's annual excess over the cross-country mean has an sd near 18-22% in these years;
with roughly 100-120 event rows SE(b) is about 2% (DK may add a little), so a pass needs
b near -4% to -5% a year. W41's post-hoc 12-month point estimate (-3.1%) would give power of
about 30% if it were true and transferred, which is unlikely (it was the extreme of a selection
of cells). Guess: b between -3% and +2%, |t| < 1.5, a middle rank; prior of a pass 5%.

## On the outcome

Fail: dead; one `screen` row in `research/tries.md` plus a `robustness` row per shown cell. The
negative-drift reading of W41 is then closed. Pass: "not dead yet"; it would need an
independent third sample (no other cabinet data are cached; CPDS starts 1960 and overlaps W41).
