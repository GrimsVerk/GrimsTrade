# jst-gates-1: two kill-only gates on the JST panel (W38 `consumption-cycle`, W39 `bank-capital-premium`)

Lane `jst-gates-1`, 2026-11-25 (UTC). Research only, nothing selectable. Card:
[`cards/jst-gates-1.md`](cards/jst-gates-1.md), pushed at 22:02 UTC (d7c0fa7) before any value
of the tested data was read (only presence counts, listed in the card). Tables:
[`results/jst-gates-1.md`](results/jst-gates-1.md). Code: `lib/jstgates1.py`; tests:
`tests/test_jstgates1.py`. Data: the cached JST R6 file (CC BY-NC-SA 4.0; Jorda, Schularick and
Taylor 2017), nothing downloaded, nothing but statistics committed. Gate ids W38/W39
(replications R38/R39) are provisional: PR #205 holds W37 unmerged, and the merging lead may
renumber.

## The answer on one screen

Both gates fail. Both were labelled **kill-only** before any number (smallest honest p 0.048 for
W38 and 0.024 for W39, far above the family bar of 0.00094), so even a pass would only have said
"not dead yet". No replication was run, because the card runs one only after a pass.

| Gate | b per 1 sd of dose | DK t | Shift rank | Bootstrap p (H0) | Phase rank (shown) | Card verdict |
|---|---:|---:|---:|---:|---:|---|
| W38 `consumption-cycle`, 14 countries, 355 rows, 1904-1947 | -0.024 | -1.88 | 3 of 21 | 0.045 | 4 of 41 | **fail, not a clean kill** (t > -2, rank 3) |
| W39 `bank-capital-premium`, 16 countries, 1,285 rows, 1925-2020 | +0.002 | +0.17 | 19 of 41 | 0.580 | 28 of 41 | **clean kill** (wrong sign) |

- **W38 is a near miss with the predicted sign, and it does not pass.** Consumption below its
  own Hamilton trend is followed by a higher equity excess return the next year, about 2.4 log
  points per standard deviation of the dose. The sign holds:
  - in both halves (1904-1913: -0.030, t -2.33; 1920-1938 plus 1947: -0.027, t -1.78);
  - without the suspect periods (-0.023, t -1.63);
  - in 10 of 14 countries taken one at a time.

  It fails two of the card's pass conditions. The t is -1.88, short of -2. The shift rank is 3
  of 21, outside the top 2: two placebo doses (k = 17 and 23 years) did better. The
  returns-side bootstrap alone would have passed it (p 0.045).
- **What weakens W38 beyond the verdict (shown cells, not gating):**
  - Using the dose of year t-1 (the lag a real-time reader would have; Melone uses the second
    lag) gives t -0.57. Whatever is there sits on the first lag only.
  - The dose follows the previous year's stock return strongly (z(t) on y(t-1): t +3.40), so it
    is partly a lagged wealth effect. The controls cover the trailing 1- and 3-year returns.
  - The alternative dose (log consumption minus its trailing 10-year mean) shows t -2.71 and
    shift rank 1. It is not the card's dose, and choosing it after seeing both would be a forking
    path. It is reported, not used.
- **W39 is dead.** The slope has the wrong sign (+0.002, t +0.17, rank 19 of 41). The halves
  disagree (1925-1970: -0.012, t -1.21; 1971-2020: +0.022, t +0.87), and no variant gets near
  the bar (every shown t is between -0.30 and +0.81). Thin bank capital does not foretell
  equity returns on this panel. That matches Haddad-Muir's prior that equities are where
  intermediaries matter least. The bond outcome shows t +2.38 (shown, sign reported only). The
  predicted sign was negative, the null for this design is wide, and it is one of about 10
  shown cells: noted only.

## The nulls, and whether the shift family is enough for the returns side

jst-autocorr-2 rules that a pooled timing test on JST equity before 1966 needs a null that keeps
the returns' own and common lag-1 autocorrelation. The card used three families.

1. **Earlier shifts (deciding, gate-null step 1).** The placebo pairs the *real* outcome with an
   earlier dose of the same country. All of the returns' autocorrelation (per country and common)
   and the dose's own persistence stay in every placebo. What a shifted dose loses is its
   same-year link to the returns. With a persistent dose and autocorrelated returns, that link
   can create a slope (Stambaugh bias, a lagged-return channel). So the shift family is not
   enough on its own for the returns side.
2. **Returns-side AR bootstrap under H0 (pass condition).** It keeps AR(1) for the common mean,
   per-country AR(1) for the idiosyncratic returns and for the dose, and joint same-year
   residuals (B 199).
   - W38: centred at +0.34 with SD 1.32, wider than the shift null (SD 1.06). Its lower tail is
     not wider (5%: -1.69 against -2.00).
   - The card expected the bias to push toward the predicted negative sign. It did not show up:
     the measured feedback is lagged (y(t-1)), not same-year (z(t) on y(t): t -0.19). So the
     bootstrap does not drive the verdict; W38 fails on t and the shift rank.
   - W39: centred (median -0.01, SD 1.09).
3. **Phase-randomised surrogates (shown; PR #207's family).** The same random phase is added
   to every country's own phases (Prichard-Theiler), so the cross-country co-movement of the
   dose stays.
   - W38: SD 1.49, wider than both other families, true t rank 4 of 41.
   - W39: SD 0.89, rank 28.
   - Dose lag-1 acf: W38 +0.51, below #207's threshold, so its "both families" rule would not
     apply. W39 +0.88, so it would apply, and both families fail W39.
   - Under #207's rule as written, neither verdict changes.

The W39 shift null is off-centre: placebos k = 20-29 years sit near +2 (median +0.23, 95%
+2.16, max +2.37), the W33 pattern of a long earlier-only family. The true t is far from both
tails, so the verdict does not depend on it.

## How sure

- **Power.** As the card wrote, W38 has about 60-70 effective years: t about sqrt(R2 x 68). At
  t -1.88, the data are consistent with an R2 of about 5%. That is inside the published range
  (AMP 2.4% a quarter, Melone 4-12% a year), so the fail is **not** a strong kill of the
  published size. It is a fail by the pre-set rule and leaves the idea unsupported on unseen
  data, not refuted. W39's wrong sign over 88 years is a firmer kill.
- **Rows lost to missing controls.** `eq_dp` is missing for NLD 1919-1937 and CHE 1926-1946,
  so those rows drop by the card's rule (NLD keeps 10 rows in W38, CHE 17). The no-controls
  cell uses the same rows.
- **Drop list.** Applied by outcome year (war, closure, hyperinflation with CPI up more than
  50%, interpolated years). DEU's CPI rule also drops 1917, 1920 and 1922-1924. Controls may use
  returns of dropped years (for example the trailing return into 1925).
- **One fix after the first run, shown diagnostic only.** The phase surrogates first replaced
  every country's phases with one shared random set. That aligns all countries perfectly, which
  is not Prichard-Theiler. Fixed to add the shared phase to each country's own phases. W38's
  phase rank moved from 8 to 4 and W39's from 24 to 28. No deciding number changed (`note` row
  in `tries.md`).
- **The bootstrap is a model.** Its AR(1) fits are OLS without bias correction, and a country
  missing in the drawn year draws its own residual pair from a random year. `eq_dp` and
  `crisisJST` are held at their real values.

## Counts

- Main's `gate-null.md`: 104 mechanisms, 29 tested by a strategy, 32 gates. This lane adds two
  mechanisms and two gates (W38, W39; no replication ran): **106 mechanisms, 29 tested by a
  strategy, 34 gates, still two kill-only passes (W32, W36), each killed by its replication.
  Family bar p < 0.10 / 106 = 0.00094.** If #205 (W37) lands first: 107 / 29 / 35, bar 0.00093,
  and the merging lead may renumber W38/W39.
- `BAR.md` unchanged: these are `screen` rows, not selectable. N for a new pick is 1,116,
  N_eff 506, z >= 4.70.

## Logged

`tries.md`: two `screen` rows (W38, W39), two `robustness` rows (shown cells), one `note` row
(the phase-surrogate fix). `ideas.md`: both survey-8 rows updated. `gate-null.md`: two rows in
each table, and the count.
