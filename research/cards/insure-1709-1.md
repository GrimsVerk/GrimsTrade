# Card insure-1709-1: does trend's crash insurance hold on UK monthly data 1709-1866?

Lane `insure-1709-1`, written 2026-11-25 ~22:25 UTC, **before any number on the tested series
was computed** (no return, level, fall count, autocorrelation, rule position or episode).
Branch `insure-1709-1`. Research only: fake money, keyless public data, no change to the gym,
the daily runner or the live strategies. Train data only (everything is before 1867).

## Question

The project's main finding (SUMMARY "The insurance is real"; insure-1 #87, insure-2 #90,
insure-1870-1 #186): `tsmom12` is crash insurance, not an edge. It lost less than holding in
20-21 of 21 US falls of 25%+ since 1927 and in 17 of 18 effective falls in other developed
markets since 1966, avoided about half of each fall against about 0.27-0.34 at random dates, and
held out of sample on annual JST data 1871-1965 (9 of 9 effective falls; share avoided 0.73
against 0.51 fixed and 0.47 random, p_S 0.020). The annual timing statistic is confounded by
the lag-1 autocorrelation of early annual indices (jst-autocorr-1 #192, jst-autocorr-2 #204):
a rotation null assumes none, and an AR(1) of the observed size produces most of the gap.
**On monthly UK share prices 1709-1866 and consol prices 1753-1866, which no scored series
covers: does the rule lose less than holding in the falls, and does it avoid more of each fall
than an autocorrelation-preserving null allows?**

## What had been seen when this was written

- insure-1, insure-2, insure-1870-1 (all numbers above), jst-autocorr-1, jst-autocorr-2 (their
  write-ups; jst-autocorr-2 compared the BoE monthly share index with JST for 1871-2016 only).
- PR #206 (data-wide-2): its PR text ("UK shares 1709-1866, consols 1753-, USD/GBP 1791-") and
  its `SEEN` list in `research/lib/datawide2.py`. Its fall counts on these series
  (`research/results/data-wide-2.md` on that branch) were **not** read by this lane, and are
  not read before the results here are written.
- The BoE cached CSV (`<cache_root>/jst-autocorr-2/boe/monthly.csv`, the datahub mirror of
  "A millennium of macroeconomic data" v3.1, OGL v3): variable names, units and first/last year
  with a value only. Share index: 1709-2017, 3,695 monthly values (so some months are missing;
  where not yet looked at). Consol yield (corrected for Goschen's conversion): 1753-2017.
  Discount rate on prime short-term paper (spliced): 1718-2017. No value was read.
- The BoE workbook's documentation text (fetched this lane from bankofengland.co.uk, robots.txt
  checked: `/-/media/` is allowed; 27.5 MB xlsx, only text cells of the headers read):
  - M13 (share prices): the spliced column is "Spliced monthly index weighted by market
    capitalisation", April 1962=100. Sources listed: Neal (1990), "Unweighted average of Bank
    of England, East India Company and South Sea Company shares, April 1709=100, **end month
    data**"; Acheson et al. (2009), "681 companies, weighted by market capitalisation, March
    1825=100, **end month data**" (also paid-up-capital weighted and unweighted versions);
    Gayer, Rostow and Schwartz (1953) 1811-1850, 63 companies with and without mines (timing
    not stated); Hayek's unweighted index 1820-1868 (timing not stated); Smith and Horne
    (1934) 1867-1914, end month.
  - A31's note on the annual index says the monthly-based index uses "the Neal (1990) and Smith
    and Horne (1934) monthly indices which have less coverage", "weighted by market
    capitalisation 1825-1870, end year observations". So the spliced monthly index is read as
    **Neal 1709-1824 (3 shares, unweighted, end month) and Acheson et al. 1825-1866 (681
    companies, cap-weighted, end month)** in the window used here. The exact splice month is
    checked after this card (below).
  - M10 (long rates): spliced consol yield 1753-2015; sources Neal (1990) "Yield on 3% consols
    1753-1823", note "**End month data**"; Odlyzko (2014) 1823-1860 and NBER Macrohistory
    1852-1888 (timing not stated).
  - M9 (short rates): spliced discount rate on prime short-term paper 1718-2005; East India
    bonds 1718-1797 quarterly (6-month rate), Heim and Mirowski 1780-1825, Overend Gurney /
    Economist 3-month bills from 1824.
- General knowledge an agent cannot unlearn: the South Sea bubble (1720) was a fast, huge fall;
  the wars of 1739-48, 1756-63, 1776-83 and 1793-1815 hit consols; the 1825-26 and 1845-47
  (railway) crises; 1866 (Overend Gurney). **Expectation, stated so it can be wrong:** the
  rule loses less in most slow, war-driven falls, but is fully in at the 1720 peak and loses
  about as much as holding there; the share avoided beats random dates; beating the AR null is
  less clear on so few falls.

## Overlap and window (fixed now)

- UK stocks are scored from 1867 on (e4-indep-1 used NBER GB industrial shares from 1867;
  data-wide-2's `SEEN[("stock", "GBR")]` starts 1867; JST UK from 1870). **Shares: every month
  up to and including 1866-12.** Consols: no scored UK bond series before 1960 (`SEEN`), but
  JST carries UK bond returns from 1870; the same cut **1866-12** is used, which also keeps the
  window before Goschen's 1888 conversion.
- Nothing after 1866-12 of these series is parsed by the scoring code.

## Data (fixed now)

- **Primary series (UK shares):** BoE spliced monthly share price index
  (`spliced-monthly-share-price-index-weighted-by-market`), the cached CSV, months up to
  1866-12. A price index: no dividends. Read with a small loader of this lane (no dependence
  on PR #206).
- **Secondary series (consols):** spliced consol yield `y` (% a year, corrected for Goschen's
  conversion), turned into a perpetuity price level `1/y` (a fall of the level is a loss for a
  holder; as data-wide-2's `Monthly` does). Price only; coupon accrual (`y/12` a month) is a
  check.
- **Cash (check only):** spliced discount rate on prime short-term paper, `rate/1200` a month,
  earned while out (as insure-1's "with T-bill" reading).
- **Segments:** maximal runs of consecutive months with a value. Missing months are never
  filled; a segment with fewer than 60 scored months is dropped. The first 12 months of a
  segment only warm up the signal; the index base (1) is the month of the first decision.
- **Source periods (labels, for per-source description and the thin-market treatment):**
  shares Neal (to the splice month, at the latest 1824-12; **thin**: 3 shares, though the most
  traded of their day), Acheson et al. (from the splice month; **broad**: 681 companies,
  cap-weighted); both documented **end month**. Consols: Neal 1753-1823 (end month), Odlyzko /
  NBER 1823-1866 (timing not stated). The splice month is identified after this card as the
  first month where the spliced column's monthly change matches the Acheson cap-weighted column
  (and no longer Neal's) to 1e-6, read from the BoE workbook's M13 sheet; if that is
  ambiguous, 1825-03 (Acheson's base month) is used.

## Before scoring (computed after this card is pushed, before any rule position or episode)

- Per series and per source period: number of months, missing months, lag-1 (and lag-2)
  autocorrelation of monthly log returns (demeaned per source period, pairs not crossing a gap
  or a source change), its rough one-sided 5% noise line 1.645/sqrt(pairs), and the share of
  months with an exactly zero change (a stale-price marker). Reported as written, before the
  scoring runs. These numbers set `phi` for the AR null; they do **not** change the rule, the
  window or the verdict.
- **Treatment of thin / stale / averaged segments (fixed now):** no source in the window is
  documented as averaged, so none is dropped for averaging. Every timing reading uses the AR
  nulls below for every segment (so a high-acf segment cannot pass on its autocorrelation). In
  addition, any source period whose lag-1 acf is above its noise line or whose share of
  zero-change months is above 20% is flagged "stale-suspect" and reported separately; the
  extra-lag check (check 5) is the stale-price test. The thin Neal period is scored in the
  primary test (it is most of the window) and also reported alone.

## Rule (the project's `tsmom12`, monthly form, code reused unchanged)

- `trend_where_long.signals` (the project's monthly translation of `tsmom12`, data-long-2): at
  the end of month k the signal is on if the 12 monthly log returns dated k-11..k exist and sum
  to more than 0 (price above its level 12 months earlier). The position earns month k+1's
  return (gap 0). In: 1; out: 0 (cash at 0, the gym's convention, as insure-1 and insure-2
  primary). Cost 2 bps a side per flip (`insure2.COST`); no cost on a segment's first month.
- The gym's `tsmom12` decides weekly on Fridays with a 365-day lookback; the monthly form decides
  12 times a year (exits up to a month later): a bias against the rule in fast falls.
- Signal and holding both on the price index (no dividends): the rule forgoes the dividend
  while out and earns 0. With cash at 0 this understates the cost of being out by the dividend
  yield and overstates it by the interest rate; check 1 adds the interest.

## Episodes and statistics (insure-1's definitions, monthly closes; `insure1` code unchanged)

- Falls: `insure1.zigzag` on the holding level per segment, 25% fall and 25% rise. Only
  confirmed troughs count; an unfinished fall at a segment end is listed, not counted.
- Scored through `insure1.score` on an `insure1.Series` of month-end dates (rebound = the 365
  days after the trough, i.e. 12 months, cut at the next peak): insurance `I` over
  (peak, trough], rebound `B`, net `N = I + B`, calm `C`, all rule minus holding in log points;
  share avoided `S = I / |holding's log change|`; premium `P = -(sum B + C) / sum I` pooled;
  calm drag C per calm year. The decomposition identity is checked by `insure1.score`.
- **Effective falls:** for the shares alone, each episode is one effective fall (one series,
  episodes never overlap). For the pooled description of shares and consols: single linkage on
  overlapping [peak, trough] windows (`insure1.link`).
- **Insurance tests (decisive):** on the shares' falls, `insure1.sign_test` (ties dropped,
  one-sided) and `insure1.boot` (10,000 draws, seed 0, one-sided p = share of draws <= 0) of
  `I`; the same for `N`. **Headline count:** falls with `I > 0` out of all falls, ties counted
  against.
- **Controls for the share avoided (as #186 and insure-1 card 2):**
  - Fixed exposure: per segment the rule's mean position x held constant, x times the
    holding's monthly return, no costs: `S_fix`, `P_fix`.
  - Random dates (rotation, the standard null): one common offset k, uniform integer on
    [12, L_max - 12] months (L_max = the longest segment's scored months), seed 0, 1,000 draws;
    each segment's positions rolled by k mod its length; 2 bps per flip. `S_rot` = mean over
    falls; p_rot = share of rotations with mean `S` at least the rule's. p_P likewise (at or
    below the rule's premium).
  - **Timing gap** G = mean S (rule) minus the mean over rotations of mean S.
- **AR-preserving nulls for the timing gap (fixed now; decisive for timing):** synthetic
  worlds built per segment, the same rule, zigzag, scoring and rotations (200 offsets per
  world) applied, the world's gap G recorded; p = share of 1,000 worlds whose G is at least the
  observed G (worlds with no confirmed fall are dropped and counted).
  - **AR1:** Gaussian AR(1) monthly log returns with each source period's own mean, standard
    deviation and lag-1 acf (as `jstautocorr.ar1`, jst-autocorr-1's null), seed 0.
  - **BB:** stationary block bootstrap (Politis-Romano) of each source period's own monthly
    log returns, mean block length 3 months (keeps lag-1 and lag-2 dependence, fat tails and
    some volatility clustering, but not 12-month trends), seed 1.
  - **p_AR = the larger of the two.**
  - Reference (description): the same with phi = 0 (iid Gaussian), the event definition alone.

## Verdict (UK shares, 1709-1866, 25%/25%, cash at 0)

| Outcome | When |
|---|---|
| **Holds, timing beyond autocorrelation** | `I`: sign-test p < 0.05 and bootstrap p < 0.05, **and** p_rot < 0.05 **and** p_AR < 0.05 |
| **Holds, timing not separable from autocorrelation** | `I` passes, p_rot < 0.05, p_AR >= 0.05 |
| **In between** | `I` passes, 0.05 <= p_rot < 0.10 |
| **Holds only as lower exposure** | `I` passes, p_rot >= 0.10 |
| **Does not hold** | `I` fails (sign or bootstrap p >= 0.05) |
| **Too few falls** | fewer than 5 falls with `I != 0` (the sign test cannot reach 0.05) |

Qualifiers, always reported: "at the claimed strength" if the headline count share is at
least 0.80, "weaker than claimed" otherwise; "kept" if `N` passes both tests, else "handed back
in the rebound"; "cheaper than holding less" if `P < P_fix`.

The consols get the same table, reported as a **secondary** verdict; they do not change the
shares' verdict. A pooled shares-and-consols description uses linked clusters.

## Checks (description, each a `tries.md` row)

1. Cash at the discount rate when out.
2. Thresholds 20%/20% and 40%/25%.
3. Per source period: Neal (thin) alone, Acheson (broad) alone.
4. Other indices over the same years, from the workbook's M13 (overlapping, not independent):
   Acheson paid-up-capital weighted and unweighted (1825-1866), Gayer-Rostow-Schwartz with and
   without mines (1811-1850), Hayek (1820-1866).
5. **Stale-price check:** the signal lagged one more month (decision at the end of k trades
   month k+2). Stale prices that make a trend look timely should lose their effect at a month's
   delay; real slow falls should not.
6. Consols with coupon accrual (total return), both signal and holding.

## Bar and rows

- Not a pick: no rule is selected, nothing tuned, one configuration decides. The project-wide
  bar (`register/BAR.md`, rows through 2026-11-25 01:16: 4,126 distinct tries, N 1,116 for a
  new pick, Bonferroni p <= 4.5e-05 independent, 9.9e-05 at the measured N 506) is quoted for
  scale only. With one series and, likely, a dozen or so falls, no p here can reach it.
- `tries.md` (kind `insure-check`, idea `insure-1709-1`): one row per series of the primary run
  (`tsmom12m@insure-1709-shares`, `tsmom12m@insure-1709-consols`: monthly Sharpe x sqrt(12),
  total return, max drawdown of the rule, flips a year) and one row per check; the before-
  scoring autocorrelation table gets a `note` row. Rotations, AR worlds and the fixed control
  are re-scorings: no rows.

## What each answer means

- **Holds, timing beyond autocorrelation:** the insurance and its timing show on 158 years of
  monthly data the claim never saw, and the timing is not what lag-1/lag-2 dependence alone
  would give. The SUMMARY claim can cite independent support for timing.
- **Holds, not separable:** the insurance is there, but its timing is consistent with the
  series' own short-lag autocorrelation (real or stale).
- **Lower exposure only / In between:** the rule lost less, but not clearly more than holding
  less at random dates.
- **Does not hold:** the insurance claim does not extend to 18th- and 19th-century London.
- No outcome changes the live rule.
