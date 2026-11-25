# Card insure-jstbonds-1: does trend's crash insurance hold on JST annual government-bond returns?

Lane `insure-jstbonds-1`, written 2026-11-25 ~23:15 UTC, **before any bond return, drawdown,
fall count, episode or rule position of this lane was computed**. Branch `insure-jstbonds-1`.
Research only: fake money, keyless public data already in the cache, no change to the gym, the
daily runner or the live strategies. Train data only (JST R6 ends in 2020).

## Question

The project's main finding (SUMMARY; insure-1 #87, insure-2 #90, insure-1870-1 #186): `tsmom12`
is crash insurance, not an edge: it loses less than holding in falls, and avoids more of each
fall than the same exposure at random dates. On bonds the record is thin and mixed: as a crash
warning the exit has no skill on bonds (#182); per asset the timing is not paid on bonds (#214);
on long monthly bond histories (insure-bonds-1, PR #219) falls of 10%+ are too rare, and at 5%
Norway 1823-1984 does not hold (4 of 11) while UK consols 1867-1926 lose less in 9 of 10 with
timing only "in between" random dates. **Does the insurance, and its timing beyond random dates
and beyond what autocorrelation alone gives, show on the JST Macrohistory annual government-bond
total returns, which no record has scored for insurance?**

## What had been seen when this was written

- The write-ups and code of insure-1870-1, jst-autocorr-1/2, jst-gates-1, stale-checks-1
  (PR #220) and insure-bonds-1 (PR #219), with all their numbers.
- The JST file's layout only (this lane): `bond_tr` exists for 16 countries (no Canada or
  Ireland in R6's bond returns): AUS from 1900, CHE 1900 (gap 1915), ESP 1900 (gap 1937-40),
  JPN 1881, PRT and SWE 1871, BEL, DEU, DNK, FIN, FRA, GBR, ITA, NLD, NOR from 1870 (BEL gap
  1914-19, DEU 1944-48, DNK 1915), USA 1871; all to 2020. `bill_rate` gaps as listed in
  insure-1870-1's card. No bond return, level, fall or position.
- jst-gates-1 (#210) used `bond_tr` minus bills as an outcome of the W39 gate (16 countries,
  1925-2020; a regression t, not a trend rule or a fall). Nothing in it bears on falls or timing.
- General knowledge an agent cannot unlearn: nominal bond indices fall when yields rise: the
  inflations after both world wars, the 1970s, 1994 (mostly intra-year), and the long bull market
  1981-2020. Coupons offset much of a yield rise over a year.
- **Expectation, stated so it can be wrong (my guess):** annual bond falls of the chosen size are
  few, mostly one-year yield spikes where a once-a-year rule is fully in (ties), plus some slow
  multi-year falls in the 1950s-1970s where the rule is out. Guess: the insurance sign test
  passes narrowly or not at all; the headline share with ties counted against is well below 0.80;
  the share avoided beats fixed exposure and rotations, but not the AR-preserving nulls (bond
  annual returns are autocorrelated through yield trends); the year-older signal removes most of
  the gap. Most likely verdict "Holds only as lower exposure" (40%), "Does not hold" (35%),
  "In between" (10%), "Holds" (15%).

## Data

Jorda-Schularick-Taylor Macrohistory Database R6 (annual; CC BY-NC-SA 4.0 by the record in
data-long-1 and data-long-4: non-commercial use with citation, fine for fake-money research;
cite Jorda, Schularick and Taylor 2017 and Jorda, Knoll, Kuvshinov, Schularick and Taylor 2019),
the copy cached by data-long-4 (`long_macro_build._jst()`, read-only, never committed; only
statistics are committed):

- `bond_tr`: government bond total return of calendar year t, nominal, local currency
  (holding).
- `bill_rate`: bill return of year t, nominal (cash).
- `cpi`: hyperinflation flags and the real-index check only.

A country-year is **usable** when both `bond_tr` and `bill_rate` exist and the year is not
dropped. **Dropped years (primary):** jst-autocorr-2's rule for timing tests on JST annual data
(`jstautocorr2.disrupted`, reused unchanged): 1914-1918 and 1939-1945 everywhere, CPI inflation
above 50%, and the documented closures / civil war / revolution / price-control spans (ESP
1936-40, PRT 1974-77, JPN 1946-48, DEU 1943-48, NLD 1944-46, AUS 1941-47). These spans were
written for equity sources; they are applied to bonds unchanged so the rule stays one rule.

A **segment** is a maximal run of consecutive usable years; its first year is the signal year
only (index base 1 at its end), the rest are scored years. Segments with fewer than 10 scored
years are dropped (insure-1870-1's `segments`, applied to `bond_tr`).

**Overlap with already-scored bond series** (by the project's register of seen coverage,
`datawide2.SEEN`, plus insure-bonds-1):

- US bonds 1871-2025 (data-long-1 read JST's US `bond_tr`; US 10-year yields since 1871 in
  data-long-3 / Shiller): **all US years overlap.**
- data-long-3 / pooled bond markets: AUS from 1969, CHE 1955, DEU 1956, GBR 1960, JPN 1989,
  NOR 1985, SWE 1986 (CAN, NZL not in JST bonds).
- insure-bonds-1 (PR #219, monthly, rebuilt from yields): Norway 1823-1984 and UK consols
  1867-1926. With the above, **all Norwegian years overlap**, and the UK is new only 1927-1959.
- insure-1709-1's consols (1754-1866) end before JST starts.

**Primary (decisive) sample: the non-overlapping country-years** (usable, undisrupted, not
covered above): BEL, DNK, ESP, FIN, FRA, ITA, NLD, PRT all years; AUS to 1968; CHE to 1954; DEU
to 1955; GBR 1927-1959; JPN to 1988; SWE to 1985. A segment is cut where overlap starts (a new
segment would need its own signal year). **Check 1 keeps the overlapping years** (all 16
countries).

## Rule (fixed now)

- Position in year t: **1 (hold bonds) if `bond_tr`(t-1) > `bill_rate`(t-1), else 0 (bills).**
  The annual analogue of `tsmom12` used by insure-1870-1 (excess over bills; nominal and real
  give the same signal).
- Rule return: pos x `bond_tr` + (1 - pos) x `bill_rate` - 0.0002 x |pos(t) - pos(t-1)| (2 bps a
  side; no cost in a segment's first scored year).

## Fall threshold (the only data-dependent choice; fixed now as a rule on the holding index)

Bond falls are rare at 10%+ (insure-bonds-1), so the threshold is chosen from **holding-index
counts only**, before any rule position is computed:

- Ladder d = 25%, 20%, 15%, 10%, 7.5%, 5% (zigzag fall d, rise d, `insure1.zigzag` on each
  segment's year-end nominal `bond_tr` index), on the primary sample.
- For each d count episodes, anchored clusters and linked clusters (definitions below; both use
  only the holding indices).
- **The threshold is the largest d with at least 10 anchored and at least 10 linked clusters.**
  If no rung reaches that, d = 5%.
- The counts and the chosen d are committed and pushed as an amendment to this card before any
  rule position, insurance or share is computed. Checks use the same d unless they say otherwise.

## Events, decomposition, clusters (insure-1870-1's definitions, unchanged)

- Only confirmed troughs count; an unfinished fall at a segment end is listed, not counted.
- Log points (100 x ln), rule minus holding: **insurance** `I` over (peak, trough]; **share
  avoided** `S = I / |holding's log change|`; **rebound** `B` the first year after the trough
  (bounded by the next peak and the segment end); **net** `N = I + B`; **calm** `C` all other
  scored years; **premium** `P = -(sum B + C) / sum I`.
- **Tie rule (insure-bonds-1's bug):** after scoring, any |I| < 1e-9 is set to exactly 0 and
  counted as a tie (did not lose less; dropped from the sign test).
- **Anchored clusters (primary):** anchors are the US `bond_tr` episodes (all usable undisrupted
  US years 1871-2020, same d; labels only, the US is not in the primary sample). An episode
  joins the anchor whose [peak, trough] holds its trough, else its peak; the rest by single
  linkage. Cluster value = mean over its primary episodes.
- **Linked clusters (strict):** single linkage on overlapping [peak, trough] windows.

## Tests (fixed now)

- **Insurance:** sign test (zeros dropped, one-sided) and cluster bootstrap (10,000 draws, seed
  0), as insure-1, on cluster values of `I`, both clusterings; the same for `N` (anchored).
- **Headline share:** anchored clusters with `I > 0` out of all, ties against; also per episode.
- **Fixed exposure:** per segment the rule's mean position held constant, no costs: `S_fix`,
  `P_fix`.
- **Random dates (rotation, description only):** insure-1870-1's 1,000 common rotations, seed 0:
  `p_rot` = share with mean anchored-cluster S at least the rule's. Not decisive: the sample
  starts before 1966 and is pooled, and #204's rule forbids a rotation null there.
- **AR-preserving nulls (decisive for timing).** Statistic: jst-autocorr-1's per-episode gap
  `G` = mean episode S of the rule minus the mean episode S over rotations (50 rotations per
  world, as jst-autocorr-1). Worlds (1,000 each, seed 0), log excess returns over bills
  x = ln(1 + `bond_tr`) - ln(1 + `bill_rate`), bills kept as observed, the rule's signal
  computed from the world's own x(t-1) > 0, episodes re-detected on the world's index at the
  same d:
  - **AR(1):** Gaussian AR(1) per segment with the segment's mean and sd and the country's own
    pooled lag-1 acf (clipped to [-0.9, 0.9]) (stale-checks-1's `sim_gaps` form);
  - **Block bootstrap:** stationary bootstrap (Politis-Romano) of each segment's own x, mean
    block length 5 years, circular; the signal year's x is the bootstrap draw before the first
    scored year.
  - `p_AR`, `p_BB` = share of worlds with G at least the observed G; **p_null = max(p_AR,
    p_BB)**. Both keep each series' own serial dependence; neither keeps the cross-country
    co-movement, so both are too narrow if falls are common across countries (errs toward
    "timing shown"; stated now).
- **Year-older signal control (stale-checks-1 (b)):** each segment drops its first scored year;
  L1 = the rule (signal year t-1), L2 = position 1 if `bond_tr`(t-2) > `bill_rate`(t-2), scored
  on the same years. Both get the full verdict machinery, with their own AR and BB nulls (the L2
  worlds use a lag-2 signal). Reading: **"timing does not rest on the last year alone"** if L2's
  p_null < 0.05 and L2's insurance passes; **"timing rests on the last year's return"** if L2's
  p_null >= 0.10 and L1's p_null < 0.05; otherwise **"in between / not read"** (including when
  L1 itself shows no timing). Run on the primary and on check 1.
- **Per country (description):** episodes, I > 0 / ties, mean S rule / fixed / rotations, G and
  its AR(1) p with the country's own worlds. Many countries, few falls each: no per-country
  verdict.

## Verdict (primary sample, chosen d, nominal index, cash at bills)

| Outcome | When |
|---|---|
| **Too few falls** | fewer than 8 anchored clusters with I != 0 |
| **Does not hold** | `I` fails (sign-test p < 0.05 and bootstrap p < 0.05) under either clustering |
| **Holds** | `I` passes under both clusterings, **and** p_null < 0.05 |
| **In between** | `I` passes, 0.05 <= p_null < 0.10 |
| **Holds only as lower exposure** | `I` passes, p_null >= 0.10 |

Qualifiers, always reported: "at the claimed strength" if the headline share >= 0.80, else
"weaker than claimed"; "kept" if `N` passes the sign and bootstrap tests (anchored), else
"handed back in the rebound"; "cheaper than holding less" if P < P_fix.

**Kill reading:** "Does not hold" or "Holds only as lower exposure" on the primary means the
JST bond data do not support trend's timing on bonds; together with #182, #214 and
insure-bonds-1 the SUMMARY bond line would read "no timing evidence on bonds". "Holds" would be
the first bond timing evidence beyond autocorrelation, to be read against the year-older
control.

## Checks (description, each a `tries.md` row)

1. All 16 countries, overlapping years kept (with the year-older control).
2. Disrupted years kept (wars, closures, hyperinflation), primary countries and overlap rule.
3. Events on the real index (`bond_tr` deflated by JST `cpi`), same d, same rule.
4. Cash at 0 when out (the gym's convention).
5. Neighbouring rungs: the next larger and next smaller d of the ladder, where they exist.
6. Era split of the primary: scored years up to 1965, and 1966-2020 (a segment is cut at 1965).

## Bar and rows

- Not a pick: no rule selected, nothing tuned; one configuration decides. The project bar
  (`research/register/BAR.md`: N_eff 509, z 4.70) is quoted for scale only.
- `tries.md` (kind `insure-check`, idea `insure-jstbonds-1`): one row per primary country
  (`tsmom12a@insure-jstbonds-<ISO>`; annual Sharpe = mean / sd of rule returns, total return,
  worst year-end drawdown, flips a year), one row per check and one for each year-older run.
  Rotations, null worlds and the fixed control are re-scorings: no rows. No gate id is taken.

## What each answer means

- **Holds:** the timing part of the insurance shows on bonds in 16 countries' annual data,
  beyond fixed exposure and beyond the series' own autocorrelation.
- **In between / lower exposure only:** the rule lost less than holding in bond falls, but not
  clearly more than holding less, once autocorrelation is kept.
- **Does not hold:** the insurance claim should not be extended to bonds on annual data.
- **Too few falls:** the JST annual bond data cannot answer the question at any rung.
- No outcome changes the live rule.

## Amendment A: fall counts and the chosen threshold (2026-11-25 ~23:35 UTC)

Computed by `uv run python -I research/lib/insurejstbonds1.py counts` on the holding indices
only, before any rule position, insurance, share or rule return of this lane was read (the code
builds positions inside `insure1870.segments`, but the counts mode prints none). Primary: 40
segments in 14 countries (no US, no Norway: all their years overlap), 1,352 scored
country-years.

| Sample | d | Episodes | Multi-year | Anchored clusters | Linked clusters | Unfinished falls | Countries with a fall |
|---|---:|---:|---:|---:|---:|---:|---:|
| primary | 25.0% | 2 | 2 | 2 | 2 | 1 | 1 |
| primary | 20.0% | 4 | 4 | 3 | 3 | 0 | 2 |
| primary | 15.0% | 6 | 6 | 4 | 4 | 0 | 3 |
| primary | 10.0% | 23 | 13 | 12 | 12 | 3 | 12 |
| primary | 7.5% | 44 | 19 | 21 | 19 | 4 | 12 |
| primary | 5.0% | 66 | 26 | 24 | 21 | 4 | 13 |
| overlap | 25.0% | 4 | 4 | 4 | 4 | 0 | 2 |
| overlap | 20.0% | 5 | 5 | 4 | 4 | 0 | 2 |
| overlap | 15.0% | 8 | 7 | 5 | 5 | 0 | 4 |
| overlap | 10.0% | 33 | 16 | 15 | 15 | 3 | 14 |
| overlap | 7.5% | 63 | 25 | 22 | 20 | 4 | 15 |
| overlap | 5.0% | 97 | 34 | 24 | 21 | 4 | 16 |

("Multi-year": trough at least two year-ends after the peak.) By the card's rule **d = 10%**
(fall 10%, rise 10%): 12 anchored and 12 linked clusters. Check 5 uses 15% (4 clusters: will
read "Too few falls" by construction) and 7.5%. Ten of the 23 primary episodes are one-year
falls, where a once-a-year rule that was in loses exactly what holding loses (a tie), so the
headline share is biased down as the card says. Nothing else on the card changes.
