# jst-gates-1 card: two kill-only gates on the JST panel, `consumption-cycle` (W38) and `bank-capital-premium` (W39)

Lane `jst-gates-1`, written 2026-11-25 (UTC), **before any value of the tested data was read**
(card pushed first; the commit time is in git). From survey-8's two card sketches
(`research/survey-8.md`, "Top 2 for a future lane", with its review fixes) and the null rule of
`research/jst-autocorr-2.md` (pooled timing tests on JST equity before 1966 need an
autocorrelation-preserving null; its drop list and suspect periods).

Gate ids **W38** and **W39**, replications **R38** and **R39**: provisional. Main's
`gate-null.md` ends at W36/R36; the open PR #205 (wide-23) holds W37. If #205 or another lane
lands first, the merging lead may renumber; the card keeps these ids.

## What was seen before this card (disclosed)

- The JST R6 file (`JSTdatasetR6.xlsx`, cached by data-long-4, CC BY-NC-SA 4.0; Jorda,
  Schularick and Taylor 2017) is the same file survey-8 opened (header only) and that
  insure-1870-1, jst-autocorr-1 and jst-autocorr-2 read for `eq_tr`, `bill_rate`, `cpi`
  (equity returns 1870-1965 were seen by those lanes as autocorrelation and crash statistics,
  never against consumption or bank capital).
- For this card: **presence counts only** (which country-years have a non-missing value) of
  `rconsbarro`, `lev`, `eq_tr`, `bill_rate`, `eq_dp`, `crisisJST`. No value was printed.
  Consumption starts in 1870 in 13 countries, 1874 (JPN), 1910 (PRT), 1913 (BEL). `lev` starts
  in 1870 in 8 countries, later elsewhere (ESP 1874, FIN 1873, GBR 1880, FRA 1890, JPN 1893, NLD
  1900, BEL and PRT 1920), with gaps (AUS 1946-50, BEL 1934, DEU 1921-23 and 1941-49, ESP
  1936-41).
- PR #207 (gate-null-2, open): phase-randomised surrogates are nominal-size for persistent
  doses; it proposes "pass in both the shift and the phase family" for doses with lag-1 acf >=
  0.8. **Not adopted as a deciding rule here** (not merged); computed and reported as a
  diagnostic, with what its rule would say.

## Shared design (both gates)

- **Outcome** y(i, t+1) = ln(1 + eq_tr) - ln(1 + bill_rate) of country i in year t+1: the log
  equity total return over bills (the real excess return; inflation cancels).
- **Dose** known at the end of year t (an annual figure for year t). The JST series are
  historical reconstructions, not real-time vintages; a shown cell uses the dose of year t-1
  (Melone's second lag).
- **Statistic.** Pooled OLS of y(i, t+1) on the dose z(i, t), country dummies and controls; t of
  the dose slope b with **Driscoll-Kraay** standard errors (scores summed by outcome year, then
  Bartlett weights over year distance, 2 lags; `gatepower.dk_fit`). Controls (wealth feedback,
  F2): the trailing 1-year and 3-year log excess returns ending in year t (y(i, t), and y(i,
  t-2) + y(i, t-1) + y(i, t)), and `eq_dp` of year t. W39 adds `crisisJST` of year t.
- **Rows dropped (jst-autocorr-2 point 2), by outcome year:** 1914-1918 and 1939-1945
  everywhere; ESP 1936-1940, PRT 1974-1977, JPN 1946-1948, DEU 1943-1948, NLD 1944-1946, AUS
  1941-1947; any year with CPI up more than 50%; the interpolated years CHE 1914-1916, NLD
  1944-1946, ESP 1937-1940, PRT 1975-1977 (the constants of `lib/jstautocorr2.py`). A row also
  needs every control and the dose.
- **Suspect periods (jst-autocorr-2 point 3)**, kept in the main test because the null keeps the
  returns' own autocorrelation (below), flagged, and a pass condition checks the sign without
  them: NOR 1881-1920, BEL 1870-1914, DEU 1890-1913, PRT 1870-1987, ESP 1941-2017 (outcome year).
- **Standardising.** The dose is z-scored per country over all its dose years in the gate's
  span (W38: 1880-1946; W39: 1880-2019): a scale choice only, the same series feeds the true
  statistic and every placebo (shifts and surrogates move the same z).
- **Predicted sign: b < 0 in both gates** (low consumption against trend, thin bank capital
  against trend: high marginal value of wealth, high expected excess return).

## The nulls

1. **Deciding family, earlier shifts (gate-null step 1).** Both doses can answer prices
   (consumption follows wealth; book capital falls with loan losses after falls), so placebos are
   earlier doses only: placebo k pairs y(i, t+1) with z(i, t-k), same rows as far as the shifted
   dose exists, same controls, same function (a `shift` argument). Each placebo uses the rows
   where its dose exists; a shown cell repeats the rank on the rows every placebo has.
2. **Returns-side AR-preserving null (a pass condition, bootstrap).** Why the shift family is
   *not* enough alone: it keeps the real returns (all their own and cross-country lag-1
   structure, which jst-autocorr-2 measured at +0.14 per country and +0.38 for the common mean)
   and the dose's own autocorrelation, but a shifted dose loses the dose's *same-year* link to
   returns. That link plus return autocorrelation is a lagged-return channel, and with a
   persistent dose it is Stambaugh's small-sample bias. Both doses rise with good returns
   (feedback, F2), so the bias pushes b **toward the predicted negative sign**: a shift null is
   then too lenient for a pass (a kill stays a kill, since the bias favours the hypothesis). The
   controls absorb the linear lag-1 part; the bootstrap covers the rest. Under H0 (no
   predictability), with seed 38 (W38) / 39 (W39), B = 199:
   - common component m(t) = equal-weight mean of y(i, t) over the gate's countries that year,
     idiosyncratic d(i, t) = y(i, t) - m(t); AR(1) by OLS for m, per country for d, per country
     for z, each on consecutive kept years over the whole span of the gate's data
     (W38 1871-1947, W39 1871-2020);
   - simulated paths: each year draws one historical year tau (with replacement) and uses that
     year's joint residuals (m, every country's d and z), so the cross-country correlation, the
     common lag-1 structure and the same-year dose-return link stay in; a country without a pair
     in year tau draws its own (d, z) pair from a random year of its own; 30 burn-in years;
   - the statistic is recomputed by the same function on the simulated y and z (controls from the
     simulated y; `eq_dp` and `crisisJST` held at their real values) on the same rows;
   - bootstrap p = (1 + #{b* t at or below the true t}) / 200.
3. **Phase-randomised surrogates (shown, a diagnostic; PR #207's family).** 40 surrogates of the
   z panel (seed 381 / 391): per country the Fourier amplitudes of its own dose, **the same
   random phases for every country** (Prichard-Theiler 1994 `[memory]`, so the doses' co-movement
   across countries stays), on the gate's full dose-year grid; gaps are linearly filled for the
   transform only and stay missing in the regression. Rank of the true t among 41. Reported with
   the dose's pooled lag-1 acf and what #207's "both families when acf >= 0.8" would say.

## W38 `consumption-cycle` (Atanasov-Moller-Priestley JF 2020; Melone WP 2022)

- **Question.** Does consumption below its own trend at the end of year t predict a higher
  equity excess return in year t+1, pooled across the JST countries, in 1904-1947 (data every
  source paper left unseen: all four are post-war)?
- **Dose.** c(t) = ln `rconsbarro` (real consumption per capita). cc(t) = c(t) minus the fitted
  value of an OLS of c(s) on a constant, c(s-2) and c(s-3) over s <= t in the same country
  (Hamilton filter, h = 2 years, two lags), expanding window, first value once 8 regression
  pairs exist (from 1880 for a series starting 1870). z = per-country z of cc over 1880-1946.
- **Outcome years** t+1 in 1904-1913, 1920-1938 and 1947 (30 years), minus the drop list.
- **Countries:** those with the dose and the outcome in at least 25 of the 30 years (presence:
  AUS, CHE, DEU, DNK, ESP, FIN, FRA, GBR, ITA, JPN, NLD, NOR, SWE, USA; BEL and PRT start too
  late). Rows also need the controls (FIN's `eq_dp` starts 1912).
- **Placebos:** 20, k = 4..23 years (k >= 4 so a placebo is not a one-cycle lag); ranks among 21.
- **Episodes and smallest honest p (stated before any number):** about 30 outcome years with
  8-10 business cycles that the countries largely share (1907, 1920-21, 1929-33, 1937-38).
  Smallest p = 1/21 = **0.048**; the episode count supports nothing smaller. Family bar p < 0.10 /
  106 = 0.00094 (below): **KILL-ONLY.**
- **Rules (fixed).**
  - **Kill:** b >= 0, or shift rank worse than 5 of 21.
  - **Not dead yet** (all): shift rank 1 or 2 of 21; t <= -2; b < 0 in both halves (outcomes
    1904-1913, and 1920-1938 plus 1947); b < 0 without the suspect periods; bootstrap p <= 0.05.
  - Anything else: a fail that is not a clean kill, read as not supported. Every fail counts as a
    failed gate.
- **Power, for the record (survey-8):** about 14 countries x 30 years; with cross-country
  correlation near 0.4, roughly 60-70 effective years: t about sqrt(R2 x 68), so R2 4% -> 1.6,
  6% -> 2.0, 12% (Melone's in-sample ceiling) -> 2.9. A fully surviving effect would mostly pass
  the t condition only at the high end; a fail kills sizes near the published ones weakly.
- **Shown, not gating:** (a) no controls; (b) dose of year t-1; (c) second form: c(t) minus the
  mean of c(t-10..t-1), z-scored, with its own shift rank; (d) without the suspect periods; (e)
  halves; (f) feedback: z(i, t) on y(i, t) and y(i, t-1) with country dummies, DK 2 (expected
  positive); (g) phase-surrogate rank and #207's reading; (h) bootstrap quantiles; (i) common
  rows; (j) number of countries with a negative own slope (no controls); the null's width (SD of
  placebo t, share with |t| >= 2, 5/50/95%, extremes).
- **Guess (before any number):** b slightly negative, t between -1.5 and +0.5, a middle rank;
  prior of "not dead yet" 5%.

## W39 `bank-capital-premium` (He-Krishnamurthy; He-Kelly-Manela 2017; Haddad-Muir JF 2021)

- **Question.** Does a banking-sector book capital ratio below its own trailing trend at the end
  of year t predict a higher equity excess return in year t+1, pooled, 1925-2020?
- **Dose.** lev(t) = JST `lev` (bank capital to assets). x(t) = lev(t) minus the mean of lev
  over t-10..t-1, needing at least 8 of those 10 values. z = per-country z of x over 1880-2019.
- **Outcome years** t+1 in 1925-2020 without 1939-1946 (88 years), minus the drop list.
- **Countries:** all 16 JST countries with `lev` and equity returns; rows where the dose,
  outcome and controls exist.
- **Placebos:** 40, k = 5..44 years; ranks among 41. Controls as W38 plus `crisisJST` of year t
  (the dose is not a crisis flag in disguise).
- **Episodes and smallest honest p:** perhaps 10-15 independent swings of the detrended ratio
  per country in 88 years, partly shared. Smallest p = 1/41 = **0.024**: **KILL-ONLY.**
- **Rules (fixed).**
  - **Kill:** b >= 0, or shift rank worse than 10 of 41.
  - **Not dead yet** (all): shift rank 1 or 2 of 41; t <= -2; b < 0 in both halves (outcomes
    1925-1938 plus 1947-1970, and 1971-2020); b < 0 without the suspect periods; bootstrap p <=
    0.05.
  - Anything else: a fail that is not a clean kill.
- **Shown, not gating:** (a)-(b), (d)-(j) as W38; (k) the same regression with the government
  bond excess return ln(1 + bond_tr) - ln(1 + bill_rate) as outcome (sign reported only); (l)
  without the crisis control.
- **Guess:** slow, trending dose and Haddad-Muir's prior that equities are where intermediaries
  matter least: t between -1 and +1; prior of "not dead yet" 3%.

## Replications (fixed now; each runs only if its gate passes)

The gates use the only years with earlier doses for placebos; the independent data left on the
same panel are the years *before* each gate window, which no source paper used. No earlier dose
exists there, so the null is the phase-surrogate family (40, as above, seeds 382 / 392) plus the
same bootstrap (B 199, seeds 383 / 393).

- **R38:** the W38 rule on outcome years 1881-1903, countries with the dose and outcome in at
  least 15 of those 23 years. Pass: b < 0, t <= -2, phase rank <= 2 of 41, bootstrap p <= 0.05,
  b < 0 without the suspect periods. The early doses rest on short expanding Hamilton windows (8-30
  pairs), and NOR, BEL and DEU are suspect then: a weak replication, stated now.
- **R39:** the W39 rule on outcome years 1881-1913 and 1920-1924. Same pass conditions.
- If R fails, the gate's idea is dead (as R32, R36). If both pass, the idea is still only "not
  dead yet": every design on this panel is kill-only, and nothing reaches the book.

## Counts quoted (main, 2026-11-25)

- `research/register/BAR.md`: N for a new pick 1,116, measured N_eff 506, z >= 4.70, Bonferroni p
  <= 9.9e-05. These gates are `screen` rows (not selectable): N does not move.
- `research/gate-null.md` (main): 104 mechanisms, 29 tested by a strategy, 32 gates, bar 0.10 /
  104 = 0.00096. This lane adds 2 mechanisms and 2 gates: **106 / 29 / 34, bar 0.10 / 106 =
  0.00094** (each replication that runs adds one gate). If #205 (W37) lands first: 107 / 29 /
  35, bar 0.00093.

## Outcome handling

Each gate gets one `screen` row in `research/tries.md`; shown cells as `robustness` rows. A fail
kills (or leaves unsupported) the idea, recorded in `research/ideas.md` and `gate-null.md`. A
pass runs its replication at once and reports both.
