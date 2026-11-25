# Card insure-1870-1: does trend's crash insurance hold on 1870-1965 annual data?

Lane `insure-1870-1`, written 2026-11-25 ~00:45 UTC, **before any return, drawdown, episode or
rule position of this lane was computed**. Branch `insure-1870-1`. Research only: fake money,
keyless public data already in the cache, no change to the gym, the daily runner or the live
strategies. Train data only (JST R6 ends in 2020; nothing after 2025-10-31 exists in it).

## Question

The project's main finding (SUMMARY, insure-1 #87, insure-2 #90): `tsmom12` is crash insurance,
not an edge. It lost less than holding in 20 of 21 US falls of 25%+ since 1927 and in 17 of 18
effective falls in 13 developed markets since 1966, avoided about half of each fall against
about 0.27-0.34 for the same exposure at random dates, and trailed holding in calm markets by
about 2 log points a year. All of that rests on data from 1927 (US) and 1966 (elsewhere) on.
**Does the insurance show on the years before, which the claim has never seen?**

## What had been seen when this was written

- insure-1, insure-2 (all numbers above), data-long-4's write-up (spans and cross-checks of the
  JST file, no returns).
- The JST file's layout only (this lane, `$CLAUDE_JOB_DIR/tmp` script): per country the first
  and last year of `eq_tr`, `bill_rate`, `cpi`, the missing years, the years with
  |`eq_tr`| > 100% (dates only: BEL 1940, DEU 1921-23, 1926, 1949, 1951, FIN 1945, FRA 1954,
  ITA 1943-46, JPN 1949, NLD 1940, ESP 1986, GBR 1975, PRT 1980s) and the years with CPI
  inflation above 50% (BEL 1916-17, 1941-42; DEU 1917-24; FIN 1917-18, 1946; FRA 1946, 1948; ITA
  1943-47; JPN 1945-48; PRT 1918-23). No return over any window, no drawdown, no rule position.
- `eq_tr` exists for 16 countries (no Ireland, no Canada in R6's equity returns): AUS, BEL, DEU,
  FRA, ITA, USA (from 1870-1872), GBR, PRT, SWE (1871), DNK (1873), NOR (1881), JPN (1886, gap
  1946-47), FIN (1896), CHE, ESP, NLD (1900). `bill_rate` gaps: AUS 1945-47, BEL 1915-18, DEU
  1923 and 1945-49, ESP 1936-38, FRA 1915-21, ITA 1872-84 and 1915-21; DNK from 1875, PRT 1880.
- General knowledge an agent cannot unlearn: the big pre-1927 falls (1873, 1893, 1907, the
  First World War, 1920-21 in the US; wars, revolutions and hyperinflations elsewhere; 1929-32
  and 1937-38 everywhere).
- **Expectation, stated so it can be wrong:** a once-a-year rule catches multi-year falls
  (insurance positive) but sits fully in through single-year falls (insurance exactly 0). So:
  the sign test (ties dropped) passes, the share of falls with insurance above 0 with ties
  counted against is well below insure-2's 0.94 (about 0.5-0.7), the share avoided beats random
  dates but less clearly than on daily data, the rebound year costs a lot (the rule always
  misses the first year after a down trough year), and the premium is near or above 1.

## Data

Jorda-Schularick-Taylor Macrohistory Database R6 (annual, CC BY-NC-SA 4.0; cite Jorda,
Schularick and Taylor 2017), the copy cached by data-long-4 (`long_macro_build._jst()`,
read-only, never committed; only statistics are committed):

- `eq_tr`: equity total return of calendar year t, nominal, local currency (holding).
- `bill_rate`: bill return of year t, nominal (cash).
- `cpi`: for the real-index check only.

A country-year is **usable** when both `eq_tr` and `bill_rate` exist. A **segment** is a maximal
run of consecutive usable years inside the sample window; its first year is the signal year
only (index base 1 at its end), the rest are scored years. Segments with fewer than 10 scored
years are dropped.

**Decisive sample (out of sample for the claim):** US years up to 1926 (insure-1 starts
1927-07); every other country up to 1965 (insure-2's earliest non-US decision is 1966).
Countries insure-2 never had (DNK, FIN, NOR, PRT, SWE, ITA before 1997) use the same 1965
cutoff, so the sample is one fixed rule. **Check (description only):** all usable years
1870-2020 for all 16 countries, which overlaps the data the claim was built on.

## Rule (fixed now)

- Position in year t: **1 (hold equities) if `eq_tr`(t-1) > `bill_rate`(t-1), else 0 (bills).**
  Nominal or real makes no difference to this signal: (1+r)/(1+pi) > (1+b)/(1+pi) exactly when
  r > b, so the card fixes the nominal excess return over bills and notes it is also the real
  one. Neither does it change the insurance `I` below (rule minus holding in log points: the CPI
  cancels). Only the event set depends on nominal vs real (checked below).
- Rule return: pos x `eq_tr` + (1 - pos) x `bill_rate` - 0.0002 x |pos(t) - pos(t-1)| (2 bps a
  side, as insure-2; no cost in a segment's first scored year).
- This is the annual analogue of `tsmom12` (12-month lookback, cash when out), not the gym's
  rule: decided once a year on calendar-year returns, excess over bills instead of price above
  a year ago, cash earning bills instead of 0. The cash-at-0 reading is a check.

## Events (insure-1's definitions on year-end closes)

- On each segment's year-end holding index (nominal total return): zigzag with a 25% fall and a
  25% rise, `insure1.zigzag` unchanged. Only confirmed troughs count; an unfinished fall at the
  segment end is listed, not counted (its years count as calm).
- All in log points (100 x ln), rule minus holding, over years after the start year up to and
  including the end year:
  - **Insurance** `I` over (peak, trough]; **share avoided** `S = I / |holding's log change|`.
  - **Rebound** `B` over (trough, min(trough + 1 year, next peak, segment end)]: the first year
    after the trough.
  - **Net** `N = I + B`. **Calm** `C`: every other scored year. Identity checked in the script:
    total = sum I + sum B + C.
  - **Calm-year drag** = C / number of calm years (log points a year; insure-2: about 2).
  - **Premium** `P = -(sum B + C) / sum I`, pooled over the set.

## Effective falls (clusters, as insure-2)

- **Anchored (primary):** anchors are the US JST episodes on the US index 1872-1965 (same
  zigzag). An episode joins the anchor whose [peak, trough] holds its trough, else its peak;
  the rest form their own clusters by single linkage (`insure1.link`). A cluster's value is the
  mean over its **decisive** episodes (US episodes from 1927-1965 are labels only, as the US was
  in insure-geo); clusters with no decisive episode are dropped.
- **Linked (strict):** single linkage on overlapping [peak, trough] windows across all decisive
  episodes (touching year-ends link, as `insure1.link` does). On 16 countries and two world
  wars this may chain into few long clusters; that is accepted as the conservative count.

## Tests (fixed now)

- **Insurance:** sign test (exact zeros dropped, one-sided binomial) and cluster bootstrap of
  the mean (10,000 draws, seed 0, one-sided p = share of draws at or below 0), as insure-1, on
  the cluster values of `I`; the same for `N`.
- **Headline share:** effective falls with `I > 0` out of **all** effective falls, ties
  (`I = 0`, the rule fully in) counted as "did not lose less". Reported next to insure-2's 17 of
  18 (0.94) and 20 of 21 (0.95). Also per episode (no clustering), description.
- **Random-date placebo (insure-geo's rotation):** one common offset k years, uniform integer
  on [1, L_max - 1] (L_max = the longest decisive segment's scored years), seed 0, 1,000 draws;
  each segment's position vector is rotated circularly by k mod its own length (if that is 0,
  the segment keeps its own timing for that draw, which can only help the placebo); return
  pos x `eq_tr` + (1 - pos) x `bill_rate` - 0.0002 x flips. Statistics: mean anchored-cluster
  `S` (p_S = share of rotations at least as large as the rule's) and pooled `P` (p_P = share at
  or below the rule's).
- **Fixed exposure:** per segment the rule's mean position x held constant, x x `eq_tr` +
  (1 - x) x `bill_rate`, no costs: `S_fix`, `P_fix`.

## Verdict (decisive sample, 25% zigzag, nominal index, cash at bills)

| Outcome | When |
|---|---|
| **Holds** | `I`: sign-test p < 0.05 and bootstrap p < 0.05 under **both** clusterings, **and** p_S < 0.05 |
| **In between** | `I` passes as above, 0.05 <= p_S < 0.10 |
| **Holds only as lower exposure** | `I` passes as above, p_S >= 0.10 |
| **Does not hold** | `I` fails under either clustering |

Qualifiers, fixed now and always reported:

- **Strength:** "at the claimed strength" if the headline share (anchored, ties against) is at
  least 0.80; "weaker than claimed" otherwise.
- **Kept or handed back:** "kept" if `N` passes the sign and bootstrap tests (anchored),
  otherwise "handed back in the rebound" (insure-2's result everywhere).
- **Cheaper than holding less:** insure-geo's card 2 labels: "timing, not just exposure" if
  p_S < 0.05, p_P < 0.05 and P < P_fix; "exposure, not timing" if neither p below 0.10; else "in
  between". Description, not part of the verdict.

## How annual data biases this (stated before the numbers)

1. **Fast falls are invisible.** A fall that recovers inside a calendar year (1987, 2020 type)
   never shows on year-end closes. On daily data those are where trend fails (insure-2: share
   avoided about a third, positive net in 3 of 23). Missing them biases the share of wins **up**.
2. **One decision a year.** A fall that starts after a good year is held in full for its first
   year: `I = 0` in every single-year fall (unless the year before the peak already lost to
   bills) and in the first year of longer falls. This biases `I`, `S` and the headline share
   (ties counted against) **down** against a weekly rule, and the sign test (ties dropped)
   toward fewer, more one-sided counts.
3. **Late buy-back is built in.** After a down trough year the rule is out for the whole first
   rebound year, so `B` is more negative and the premium higher than on weekly decisions.
4. **Year-end points cut depth.** Peaks and troughs between year-ends are missed: fewer and
   shallower events, mostly long ones (the kind trend handles best: bias up).

Net direction against the daily claim: the headline share with ties counted against is biased
down (point 2 dominates for one-year falls), the share avoided among multi-year falls is biased
up (points 1 and 4). So "weaker than claimed" on this data would not by itself contradict the
daily result; "does not hold" (the sign test or the bootstrap fails) would.

## Checks (description, each a `tries.md` row)

1. Full span 1870-2020, all 16 countries (overlaps the claim's data).
2. Events on the real index (`eq_tr` deflated by JST `cpi`), same rule.
3. Thresholds 20%/20% and 40%/25% (insure-1's sensitivity).
4. Cash at 0 when out (the gym's convention), same signal.
5. Years with CPI inflation above 50% treated as missing (segments split there).

## Bar and rows

- Not a pick: no rule is selected, nothing tuned, one configuration decides. The project-wide
  bar (`research/register/BAR.md`, rows through 2026-11-24 23:32: 3,982 tries, N 1,099 for a new
  pick, Bonferroni p <= 4.5e-05 independent, 9.9e-05 at the measured N 504) is quoted for scale.
- `tries.md` (kind `insure-check`, idea `insure-1870-1`): one row per country of the decisive
  sample (variant `tsmom12a@insure-1870-<ISO>`, annual Sharpe of the rule's return above 0 x
  sqrt(1), total return, worst year-end drawdown, flips a year) and one row per check above
  (pooled). The placebo and fixed controls are re-scorings: no rows.

## What each answer means

- **Holds:** the insurance is a property of trend on stock markets that shows on 55-95 years of
  data the claim never saw, at annual resolution. The SUMMARY claim can cite it.
- **In between / lower exposure only:** trend lost less in the old falls, but at annual
  resolution not clearly more than holding less at random dates.
- **Does not hold:** the insurance claim should be stated for 1927 on (US) and 1966 on (other
  markets) only.
- No outcome changes the live rule.
