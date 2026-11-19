# weather-2: CPC 6-10 / 8-14 day outlook revisions and natural gas

Lane weather-2, 2026-11-19, branch `weather-2` (from `weather-1`). Follow-up suggested by
weather-1 (`research/weather-1.md`): the realised heating-degree-day surprise is dead
because the market trades the forecast, so test the forecast revision itself.

## 1. Feasibility (no prices loaded)

Question: is there a keyless archive of NOAA CPC 6-10 and 8-14 day temperature outlooks,
numeric (probabilities or gridded anomalies) and with issue dates, covering at least 10
winters before the held-out cut (2025-11-09)?

**Answer: yes, from September 2012. 13 train winters (2012-13 .. 2024-25). Feasible.**

- **Source:** `https://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/`, files
  `610temp_YYYYMMDD.zip` and `814temp_YYYYMMDD.zip` (ESRI shapefiles, keyless, public
  domain). Each holds the official outlook as nested polygons in lon/lat (NAD83) with
  attributes `Fcst_Date` (issue date), `Start_Date`, `End_Date`, `Prob` (33, 40, 50, 60,
  70, 80, 90) and `Cat` (Above / Below; equal-chances areas have no polygon).
- **Coverage (directory listing, 2026-11-19):** 610temp 4,969 issues, 814temp 4,971, both
  first 2012-09-11, last 2026-11-18 (only issues <= 2025-11-09 will be read). Per year:
  2012 77, 2013 252, 2014 ~310, 2015 onward 362-366. So weekdays only in the first winter
  and a half (2012-13 and most of 2013-14), daily including weekends from 2014-15 on. Only
  two gaps longer than four days, both in September 2013 (5 days each), outside the season.
- **Issue time:** CPC issues the 6-10 and 8-14 day outlooks once a day around 3 pm US
  Eastern. File modification times on the server agree: of 4,969 6-10 files, 4,931 were
  written on the issue date, 3,032 in the 19:00 hour and 1,745 in the 20:00 hour (server
  clock, consistent with UTC: 3 pm EDT / 3 pm EST), a few later; 38 were written 1-4 days
  late (re-uploads; the attribute `Fcst_Date` is the issue date). So an outlook dated D is
  public at about 3 pm ET on D, before the 4 pm equity close but after the 2:30 pm NYMEX
  gas settlement. The test below therefore never enters before the next session's open.
- **Earlier data:** the same directory has `610tempabv_/bel_` files for 2011-01 and
  2012-01 .. 2012-10 only (189 issues, a different two-file layout); the CPC web archive of
  map images (`/products/archives/short_range/`) refuses scripted access (HTTP 403) and is
  images, not numbers. Nothing numeric and keyless reaches 2007. Not used.
- **Weighting by gas-heated homes:** CPC's utility-gas-weighted degree-day files already
  used by weather-1 give daily HDD for the 9 Census divisions and a CONUS row that is their
  gas-household-weighted mean. The 9 division weights can be recovered from those files
  (constrained least squares, CONUS on divisions, years before the sample) and the
  outlook evaluated at Census state population centroids grouped by division.

Verdict: feasible with 13 winters (fewer than weather-1's 18). Next: the card, written and
pushed before any price is loaded.

## 2. Card (pre-registered; written and pushed before any price is loaded)

No UNG or XLE number has been loaded in this lane. The outlook files and the Census
centroid file are downloaded after this card is pushed; only the layout of one outlook file
(attributes above) was inspected.

### Not a repeat

weather-1 tested the realised HDD anomaly (dead). W19 `enso-commodity` (ONI, dead) and W15
`cat-claims` (hurricanes, dead) are the only other weather rows. No lane has used a weather
forecast or its revision.

### Mechanism and the honest objection

Natural gas demand in winter follows heating demand, and the market prices the expected
weather of the next two weeks. CPC's 6-10 and 8-14 day outlooks are the public,
human-blended summary of that expectation. **Hypothesis: when CPC revises the outlook
colder, UNG rises after the revision is public (under-reaction), so the revision predicts
the next session's return with a positive sign.**

The objection, stated before the run: the CPC outlook is a forecaster blend of numerical
models (GEFS, ECMWF and others) whose runs traders see hours earlier, and the outlook is
posted around 3 pm ET, after the 2:30 pm NYMEX settlement. By the next open the futures have
traded on the same model runs overnight. So a revision is unscheduled (F1) and not
price-driven (F2), but it is public the moment it is issued and largely known before that;
any effect must be short and must survive the publication lag. Prior: **2%**.

### Filters (wide-11) and score (wide-10)

- **F1 not announced: pass, with the caveat above.** The issue time is routine (daily), the
  content is not known in advance; the inputs (model runs) are public hours before.
- **F2 not price-driven: pass outright.** Prices do not change the weather forecast.
- wide-10 score: cause 1 (heating demand), dose 2 (continuous, signed revision), post-sample
  1 (no anchor paper is relied on), power 1 (about 1,300 sessions), unseen 1, not killed 1
  (weather-1 killed the realised anomaly, not the forecast). **7 of 7**, no F2 cost.

### Dose (fixed now)

1. **Point signal.** For each outlook file (6-10 or 8-14, issue date D <= 2025-11-09; the
   parser drops later issues and later files are never downloaded) and each of the 48
   contiguous states plus DC: take the state's 2010 Census population centroid
   (`CenPop2010_Mean_ST.txt`, keyless). Among the polygons containing the point, take the
   one with the highest `Prob`; signal = (Prob - 100/3) / 100 if `Cat` is Above,
   -(Prob - 100/3) / 100 if Below, 0 if no polygon contains the point or `Cat` is anything
   else (equal chances, near normal). Point in polygon by ray casting on the shapefile
   rings (outer rings and holes by the even-odd rule), a parser written for this lane, run
   with `python -I`.
2. **Gas weighting.** Division value = 2010-population-weighted mean of its states' signals
   (Census divisions 1-9, the CPC numbering). CONUS value = sum of w_k x division value,
   where w (9 weights, >= 0, sum 1) is fitted once by non-negative least squares of CPC's
   utility-gas-weighted daily CONUS HDD on the 9 division HDD rows over 1981-2006 (the
   files weather-1 cached), then normalised to sum 1. Reported with the result.
3. **Outlook index.** K(D) = -(CONUS value of the 6-10 file + CONUS value of the 8-14
   file) / 2. Positive K = a colder outlook. If either file of D is missing, D has no K.
4. **Revision dose per session.** For trading session t (UNG bar dated t): I(t) = the
   latest issue date D < t with a K (public about 3 pm ET on D, so before t's open).
   x(t) = K(I(t)) - K(I(t')) where t' is the previous UNG session. If I(t) = I(t') (no new
   outlook since the last session) x(t) is missing and t is dropped. Reported in units of
   0.10 (ten probability points).

### Asset, entry, horizon (fixed now)

- **Asset:** UNG, from weather-1's cache (`<cache_root>/weather-1/yahoo/UNG.json`, fetched
  only to 2025-11-10). Every bar dated after `harness.TRAIN_LAST_BAR` (2025-11-10) is
  dropped. Context: XLE (research cache, train bars) with the same rule.
- **Entry strictly after publication:** open of session t (the first session whose open is
  after the 3 pm ET issue of I(t)). **Primary outcome:** y(t) = 100 x ln(close_t / open_t),
  UNG open-to-close of session t (raw open and close of the same bar, unaffected by the
  adjustment). One-session horizon, non-overlapping.
- **Season:** sessions t in November .. March of winters 2012-13 .. 2024-25 (13; winter
  label = year of its November).

### Statistic, null, gate (fixed now)

- **Statistic:** OLS of y on (1, x), slope b in percentage points per 0.10 of K, HC1 t.
  Predicted sign **positive**.
- **Null (`research/gate-null.md`):** 40 winter derangements of the 13 winters (no winter
  keeps its own doses), `weather1_events.derangements(13, 40)` (seed 20261119). In a placebo,
  session t of winter i gets the dose x of the session of winter pi(i) whose offset from
  November 1 is closest to t's (within +-3 days; ties to the earlier; none: t dropped). Same
  function computes true and placebo t (a `perm` argument). The season and the real dose
  distribution are kept; the timing link is broken.
- **Gate, pass needs all three:**
  1. b > 0 and t >= 2;
  2. rank of the true t among the 41 (true + 40 placebos) is 1 or 2 from the top
     (empirical one-sided p <= 2/41 = 0.049);
  3. b > 0 in both halves: winters 2012-13 .. 2017-18 and 2018-19 .. 2024-25.
- Reported every time (gate-null step 5): placebo t SD, share |t| >= 2, 5/50/95% quantiles,
  extremes.

### Shown, not gating (fixed now so none can be picked later)

Each with b, HC1 t and its rank among the same 40 placebos:
- **Dose check (not tradable):** y = 100 x ln(open_t / close of the session before t'),
  the window from the close before the issue day's session to the open after the issue,
  i.e. when the revision's model runs reach the market. Expected strongly positive if the
  dose means anything.
- Next-session close entry: close_t to close of the next session (adjusted closes).
- Five sessions: open of t to close of session t+4 (overlapping; HC1 t overstates, read the
  rank).
- 6-10 file alone and 8-14 file alone (K from one file).
- XLE, primary rule.
- Mean y in the top and bottom quintile of x.

### Power

UNG's daily SD is about 3%; about 13 x 105 = 1,350 sessions (fewer in the weekday-only first
winters is irrelevant: the dose is per session). If x's SD is about 0.5 (five probability
points), t = 2 needs b near 0.33 points per 0.10, i.e. a one-SD colder revision worth
+0.16% in the next session.

### The bar, if the gate passes (it is not a card yet)

A gate pass would earn a strategy card only. From `research/register/BAR.md` (branch
`register-4`, rows through 2026-11-19 00:21): **N = 486 effectively independent trials
(measured rho 0.53): z >= 4.69, an edge over `tsmom12` of +0.30 (close rule) to +0.56 (far
rule) on the primary test; Bonferroni p <= 1.0e-04.** A seasonal UNG-only rule is a far rule
on other data: its own SE in the z column, its t read against the placebo scale (gate-null
step 7). The held-out year (2025-11-11 .. 2026-11-09) is spent and is not read.

### Bookkeeping

- One row in `research/tries.md`, kind `screen` (descriptive gate, not selectable), whatever
  the result. Shown cells are part of the same row.
- Scripts: `research/lib/weather2_events.py` (pure functions), `research/lib/weather2_rev.py`
  (runner), `scripts/fetch_weather2.py` (downloads); output `research/results/cpc-revision.md`.

## 3. Result (one run, 2026-11-19; table `results/cpc-revision.md`)

Data as run: 4,069 outlook files (2,032 issue dates with both leads, 2012-10-22 ..
2025-11-09; 215 dates answered 404, almost all weekends of 2012-13 and 2013-14; the two
files of 2022-10-31 answer 403 and are absent, so that day's sessions use the latest issue
before it, as the rule says). Gas weights by Census division (NNLS 1981-2006): 1 0.039,
2 0.147, 3 0.229, 4 0.089, 5 0.102, 6 0.045, 7 0.091, 8 0.084, 9 0.173. K has SD 0.115;
the session dose x has SD 0.058 (5.8 probability points). 1,327 sessions with a dose,
2012-11-01 .. 2025-03-31, 97-105 per winter.

**Gate: fail on all three tests.** Slope -0.076 points per 0.10 (t -0.68, 1,327
sessions), the wrong sign; rank 36 of 41 among the winter-derangement placebos; halves
-0.028 (t -0.22, winters 2012-17) and -0.111 (t -0.66, 2018-24). Colder-revision quintile
followed by a mean UNG session of -0.02%, warmer quintile +0.06%. No strategy card. One
`screen` row in `research/tries.md`. Held-out year untouched (issues cut at 2025-11-09, UNG
bars only to 2025-11-10).

Placebo null: SD of t 0.95, 10% with |t| >= 2, 5/50/95% -0.77 / +0.78 / +2.26, extremes
-0.79 / +2.76. The null is centred above zero (median +0.78): moving a winter's revisions
onto another winter's calendar leaves a small positive alignment with UNG's open-to-close
returns (likely calendar structure shared across winters: holiday and weekday positions of
large multi-day revisions). Read against that centre the true t is lower still
(z = (-0.68 - 0.78) / 0.95 = -1.5). Width close to N(0, 1), as expected for daily,
nearly independent sessions.

What the shown cells say (noted only, none is a lead):
- **The dose check is very strong: +1.86 points per 0.10 (t 7.93, rank 1 of 41)** from the
  close before the issue day to the next open. The revision index is right about the gas
  market: a colder CPC revision comes with a large UNG rise. But that rise is complete by
  the next open; nothing follows it.
- Close t to close t+1: +0.06 (t 0.32, rank 18). Five sessions: -0.29 (t -0.75, rank 37).
  6-10 alone -0.06 (t -0.65), 8-14 alone -0.05 (t -0.50).
- XLE open-to-close +0.09 (t 1.50, rank 2 of 41): t below 2 and one of six shown cells;
  energy equities did not react to heating weather in weather-1 either. Noted only.
- The 33% contour polygons give a signal of (33 - 33.3)/100 = -0.003 for Above (and +0.003
  for Below) under the card's formula, a sign slip of a third of a probability point, far
  below the 6.7-point step to the next contour. Kept as carded; it cannot move the verdict.

**Verdict: CPC 6-10/8-14 day outlook revisions are priced before the next session opens.**
The forecast moves gas exactly as the mechanism says (t 7.9 in the window where the model
runs reach the market) and carries nothing afterwards, at one session, one day from close or
one week. With weather-1 this closes the public-weather route to natural gas at daily and
weekly horizons: realised weather is priced through the forecast, and the forecast is priced
when the models run, hours before CPC publishes it.

## Next weather idea (not tested)

Only an input that is not public before the price moves could still work: the raw model
runs themselves are public at their run times (not tradable for an ETF at daily bars), so
the remaining keyless angle would be intraday timing, which this project's daily bars cannot
test. No further weather lane is suggested.
