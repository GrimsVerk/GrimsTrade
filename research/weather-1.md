# weather-1: heating-degree-day surprises and natural gas (card, pre-registered)

Lane weather-1, 2026-11-19, branch `weather-1` (from `wide-11`). Written and pushed **before any
return data was loaded**. The weather files were downloaded and their layout checked (header
and first columns only) before this card; no statistic was computed from them.

## Not a repeat

Searched every remote research branch (wide-1..12, survey-2..7, info-1, register-*, macro-1,
data-*) for weather, degree-day, temperature, HDD, hurricane, El Nino, ENSO:

- W19 `enso-commodity` (wide-9): ONI and DBC six-month return. Dead (rank 32 of 41).
- W15 `cat-claims` (wide-8): hurricane landfalls and bond funds (LQD - 0.5 TLT). Dead (rank 8 of 23).

No lane has tested temperature or degree days against an energy asset. This card does.

## Mechanism

Natural gas demand in winter is mostly space heating, and heating demand scales with heating
degree days (HDD). A colder-than-normal week draws more gas out of storage than expected. The
draw is confirmed only in the EIA's weekly storage report the following Thursday, and storage
that ends the winter low has to be refilled at higher prices. **Hypothesis: the gas price
under-reacts to a realised HDD surprise, so last week's surprise predicts next week's return
with a positive sign.** The rival story is over-reaction to forecasts (negative sign, or zero
if the forecast already priced it all, which is the main reason this may fail: weather is
forecast days ahead and the realised anomaly is largely known before it happens).

Literature anchor: Mu (2007), "Weather, storage, and natural gas price dynamics:
fundamentals and volatility", Energy Economics 29(1), 46-63 `[memory]`: weather shocks
(HDD deviations from normal) and storage surprises move natural gas futures returns and
volatility; sample about 1997-2005 `[memory]`. Everything here (2007-2025) is after it.

## Filters (wide-11) and score (wide-10)

- **F1 not announced: pass.** Nobody schedules a cold snap; no date or size is public before
  it happens. Caveat written in advance: the realised anomaly is public at entry (by design,
  lagged) and was partly forecast, so this tests under-reaction to public information, not a
  hidden flow. The physical flow (storage withdrawal) is not public until the EIA report.
- **F2 not price-driven: pass outright.** Gas prices do not cause the temperature.
- wide-10 score: cause 1 (physical heating demand), dose 2 (degree days, continuous, signed),
  post-sample 1 (18 winters after Mu's sample), power 1 (about 390 weekly points), unseen 1
  (no lane has looked), not killed 1. **7 of 7**, no F2 cost. Prior: **3%** (weather is
  the most forecast fundamental in commodities; a weekly lag is long).

## Data

- **Dose source:** NOAA Climate Prediction Center, daily heating degree days weighted by homes
  heated with utility gas, CONUS row, files
  `https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_data/<year>/UtilityGas.Heating.txt`
  (keyless, public domain), years 1981-2025. Stored outside git under the cache root of
  `research/macro.local.json` in `weather-1/cpc-dd/`, read with `python -I`. **Days after
  2025-11-09 are discarded by the parser** (2026 files never downloaded).
- **Asset:** UNG (United States Natural Gas Fund, front-month futures, tradable ETF), daily
  adjusted close from the Yahoo chart API (as `research/lib/fetch.py`), requested with
  `period2` = 2025-11-11 00:00 UTC so **no held-out bar is ever fetched**; stored in
  `weather-1/yahoo/` under the cache root. First bar 2007-04-18.

## Rule (fixed now)

**Dose.** For each Friday F: x(F) = sum over the 7 days Saturday F-6 .. Friday F of
(HDD_d - normal_d), CONUS utility-gas-weighted, in degree days. normal_d = mean HDD over the
same calendar day +-7 days (15 days) in each of the 20 previous calendar years (300 values;
Feb 29 mapped to Feb 28). Rolling, uses no data after day d.

**Season.** Fridays F in November .. March (months 11, 12, 1, 2, 3). Winter label = the year
of its November. Winters 2007-08 .. 2024-25 (18 winters). A week enters only if its exit bar
is dated <= 2025-11-10.

**Outcome (no look-ahead, publication lag 4 days).** Entry = close of the first UNG session
dated on or after F + 4 days (Tuesday; CPC posts each day's file the next day). Exit = close
5 sessions later. y(F) = ln(exit close / entry close). Non-overlapping weeks.

**Statistic.** OLS of y on (1, x), slope b in percentage points per 10 degree days, HC1 t.
Predicted sign: **positive**.

**Null (`research/gate-null.md`).** 40 placebo calendars, each a derangement of the 18
winters (no winter keeps its own dose): week F of winter i gets the dose of the Friday in
winter pi(i) at the same offset from November 1 (the one Friday within +-3 days), so the
season is kept and the weather is real but unrelated. Permutations from
`numpy.random.default_rng(20261119)`, drawn until 40 distinct derangements; computed by the
same function as the true statistic (a `perm` argument).

**Gate: pass needs all three.**
1. b > 0 and t >= 2.
2. Rank of the true t among the 41 (true + 40 placebos) is 1 or 2 from the top (empirical
   one-sided p <= 2/41 = 0.049).
3. b > 0 in both halves: winters 2007-08 .. 2015-16 and 2016-17 .. 2024-25 (9 each).

Reported every time (gate-null step 5): placebo t SD, share with |t| >= 2, 5/50/95% quantiles
and extremes.

**Shown, not gating (written now so they cannot be chosen later):**
- Dose check: contemporaneous slope, UNG return from the close before Saturday F-6 to the
  close on or before F, on x(F). Expected strongly positive if the data are right; it is not
  tradable.
- Horizon 10 sessions instead of 5 (same entry).
- XLE (energy equities, already in the cache) with the same rule.
- Mean y in the coldest and warmest quintile of x.

**Power.** UNG's weekly winter SD is about 6-7%; x's SD about 30 degree days. With about 390
weeks, t = 2 needs b near 0.2 points per 10 degree days, i.e. a one-SD cold week worth
+0.6-0.7% the next week.

## The bar, if the gate passes (it is not a card yet)

A gate pass would only earn a strategy card. From `research/register/BAR.md` (branch
`register-4`, rows through 2026-11-19 00:21): **N = 486 effectively independent trials
(measured rho 0.53): z >= 4.69, an edge over `tsmom12` of +0.30 (close rule) to +0.56 (far
rule) on the primary test; Bonferroni p <= 1.0e-04.** A seasonal UNG-only rule over 18 years
is a far rule on other data: it would use its own SE in the z column and read its t against
the placebo scale (gate-null step 7). The held-out year (2025-11-11 .. 2026-11-09) is spent and
is not read here.

## Bookkeeping

- One row in `research/tries.md`, kind `screen` (descriptive gate, not a strategy, not
  selectable), whatever the result.
- Script: `research/lib/weather1_hdd.py`; output `research/results/hdd-gas.md`.

## Result (one run, 2026-11-19; table `results/hdd-gas.md`)

**Gate: fail on all three tests.** Slope -0.036 points per 10 degree days (t -0.29, 389
weeks), the wrong sign; rank 19 of 41 among the winter-derangement placebos; halves +0.165
(t 1.16, winters 2007-15) and -0.248 (t -1.14, 2016-24). The coldest fifth of weeks was
followed by a mean UNG week of -1.24%, the warmest by -0.77% (UNG's mean week -1.05%: the
roll drag). No strategy card. One `screen` row in `research/tries.md`. Held-out year untouched
(weather cut at 2025-11-09, UNG fetched only to 2025-11-10).

Placebo null: SD of t 1.12, 10% with |t| >= 2, 5/50/95% -1.90 / -0.32 / +1.53, extremes
-2.53 / +2.37. Weekly non-overlapping weeks with a whole-winter permutation give a null close
to N(0, 1), slightly wide.

Deviation from the card, found in the dry run (before any statistic): a placebo week gets no
dose when the other winter has no Friday within +-3 days of the same November-1 offset (first
or last week of a season), so placebo samples have 382-389 weeks instead of 389. No effect on
the verdict.

What the shown cells say (noted only, none is a lead):
- **The same-week check is weak**: UNG rose +0.23 points per 10 degree days in the dose week
  itself (t 1.68). Realised weather moves the gas fund much less than its weekly 7.3% SD; the
  market trades the forecast, so by the time the week is measured most of it is in the price.
  That is the main reason a lagged realised anomaly carries nothing: the surprise that matters
  is forecast revision, which keyless sources do not give historically.
- UNG over 10 sessions: -0.08 (t -0.47). XLE next week +0.08 (t 1.44), same week +0.03
  (t 0.51): energy equities do not trade on heating weather.

**Verdict: the realised HDD surprise does not predict next-week natural gas returns in
2007-2025.** The under-reaction story is dead in this form.

## Next weather idea (not tested)

The dose that matters is the forecast surprise, not the realised anomaly. A keyless version:
CPC's 6-10 and 8-14 day outlooks are archived as probability maps (temperature tercile
probabilities, issued daily); the change in the population-weighted cold probability from
one issue to the next is a forecast revision that nobody schedules and that prices cannot
cause (F1/F2 pass). Testing it needs a parser for the archived outlook files and their issue
times, and the same winter-derangement null. Before that, check whether the archive goes back
far enough (at least 2007) in a form that can be weighted by gas-heated homes.
