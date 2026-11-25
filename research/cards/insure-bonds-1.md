# Card insure-bonds-1: does trend's crash insurance hold on long government-bond histories?

Lane `insure-bonds-1`, written 2026-11-25 22:55-23:10 UTC, **before any number on the tested
series was computed** (no yield, return, level, fall count, autocorrelation, rule position or
episode). Branch `insure-bonds-1`. Research only: fake money, keyless public data, no change to
the gym, the daily runner or the live strategies. Train data only (everything is before 1985).

## Question

The project's central finding (SUMMARY "The insurance is real"; insure-1 #87, insure-2 #90,
insure-1870-1 #186, insure-1709-1 #212): `tsmom12` is crash insurance. It lost less than holding
in nearly all large falls and avoided more of each fall than the same exposure at random dates.
Before 1966 the timing statistic needs a null that keeps the series' autocorrelation (#192,
#204); on UK monthly shares 1709-1866 the insurance held 7 of 7 and the timing beat random dates
and an AR(1) null but not a block bootstrap (#212). Almost all of this is equity. **On long
monthly government-bond histories that no record has scored, does `tsmom12` lose less than
holding in the falls of a bond total-return index, and does it avoid more of each fall than an
autocorrelation-preserving null allows?**

## What had been seen when this was written

- The write-ups and result tables of insure-1709-1 (#212; its consols 1754-1866 price-only and
  coupon-accrual rows, including their fall counts and S), jst-autocorr-2, the SUMMARY bullet,
  data-wide-2's source table and text (not its result table: its fall counts on the Norway and
  consol price series, `results/data-wide-2.md`, were **not** read and are not read before the
  results here are written).
- `tries.md`: no row scores a Norwegian bond before 1985 or a UK government bond 1867-1959. The
  only bond insurance rows are insure-1709-1's consols (1754-1866) and asset-ledger-1's 30-year
  Treasury rebuild (1978-2025, a note). data-wide-2's `SEEN`: bond USA 1871-2025, GBR from 1960,
  NOR from 1985 (data-long-3, OECD 10-year long rate).
- Norges Bank HMS `bond_yields.xlsx` (cached by data-wide-2): sheet names and text cells only.
  - A4 "Yields on most actively traded maturities of long-term government bonds, monthly
    (1822-2007)", Klovland (2004) pp. 177-180. Notes: "Averages of most representative quotations
    abroad through December 1914, thereafter Oslo Stock Exchange"; "Average figures from
    1843-1844 are interpolated". Layout: a row per year, a column per month (+ annual average).
  - A1 "Norwegian long-term government bonds, monthly (1820-1920)": columns Hamburg, London,
    Paris, Copenhagen, Oslo, Berlin, GOV; A1's annual sheet: "Annualized yield computed from
    end-of-month quotations in different markets".
  - A3 "Norwegian bond yields by maturity (average life), monthly (1921-2005)" (ST2..ST10,
    S1015, S1520, S2060, ...); annual note: "computed from end-of-month quotations of domestic
    bonds at Oslo Stock Exchange". A2: Hypotekbank (state mortgage bank) bonds 1851-1920. A5:
    from 1985, monthly averages.
- Norges Bank HMS `shortterm_ir.xlsx` (fetched this lane, 338 KB, robots.txt read: only a crawl
  delay of 5 s, kept): text cells only. Sheet 1A1 "Norges Bank's discount rates, end-of-month"
  (Oct 1818-Dec 1986), column "NB discount rate".
- BoE millennium workbook M10 (cached by insure-1709-1): header text only. Spliced consol yield
  1753-2015 corrected for Goschen's conversion, note "Mixture of end months and averages".
  Sources: Neal (1990) 1753-1823 end month; Odlyzko (2014) 1823-1860; NBER macrohistory
  1840-1852 and 1852-1888 (timing not stated); Klovland (1994) 1870-1914 corrected for Goschen,
  "Last Friday of month"; Capie and Webber 1870-1982 uncorrected, "Mixture of end month and
  averages".
- General knowledge an agent cannot unlearn: bond prices fall when yields rise. Norwegian and
  UK yields rose in and after the First World War (to about 1920) and Norway's in the 1970s
  and early 1980s; Norway regulated interest rates for much of 1946-1980; UK consols drifted
  down from the late 1890s, and the London exchange was shut August-December 1914.
  **Expectation, stated so it can be wrong:** bond falls are slow yield rises, so the rule loses
  less in most of them, but its share avoided is not clearly above random dates (bond trend
  exits have shown no warning skill, #182); the most likely verdict is "Holds only as lower
  exposure" or "In between", then "Holds, timing not separable from autocorrelation".

## Overlap and window (fixed now)

- **Norway (primary): 1822-01 to 1984-12.** No Norwegian bond is scored before 1985
  (data-long-3 from 1985, `SEEN`). Calendar overlap, stated: 1822-1866 overlaps insure-1709-1's
  consols (UK, price-only); 1871-1984 overlaps the US bond calendar (`SEEN` bond USA 1871-).
  1985-2005 is left out (Norway's bond already scored there).
- **UK consols (secondary): scored 1867-01 to 1926-12**, the span after insure-1709-1 and
  before the post-1927 bond tests. The 12 months 1866-01..1866-12 (which insure-1709-1 scored)
  only warm up the signal: the level of 1865-12 is the base for the first return, the first
  decision is at the end of 1866-12. No UK government bond is scored 1867-1959; JST carries
  annual UK bond returns from 1870, which no lane has scored.
- Nothing outside these windows is parsed by the scoring code (Norway after 1984-12, consols
  after 1926-12 or before 1865-12).
- Not used: A2 Hypotekbank bonds (a state mortgage bank, not the government); A3 maturities
  (overlap A4 from 1921); SNB Swiss bond indices 1924-1981 (cached; a yield index to 1943
  spliced to a price index, `SEEN` CHE from 1955: 31 years needing a splice, left for later);
  JST annual bond returns (annual; another lane).

## Data and total-return formula (fixed now)

- **Norway, A4 single column** (yield, % a year, of the most actively traded long government
  bonds), months 1822-01..1984-12 with a value. **Total return: the project's constant-maturity
  par bond rebuild** (data-long-3's method, `combo2_longrun.bond_returns`): at the end of month
  t-1 buy a 10-year par bond with coupon y(t-1) (semiannual), reprice it at the end of month t at
  y(t) with 10 - 1/12 years left (exact annuity formula), add the coupon accrued over the month
  y(t-1)/12. Monthly simple return r(t) = price - 1 + y(t-1)/12. A missing month breaks the
  segment (never filled).
  - Why 10 years: A4's later years are a 10-year benchmark and data-long-3 rebuilt every
    foreign 10-year bond this way. Nineteenth-century Norwegian loans were long amortising
    loans; their duration is not documented here. A longer duration makes falls deeper; check
    2 uses a perpetuity (price 1/y, coupon y/12: the longest duration).
- **Consols, BoE spliced consol yield** (corrected for Goschen's conversion), months
  1865-12..1926-12. **Total return: a perpetuity paying 1 a year**, price 1/y, coupon accrued
  monthly: r(t) = y(t-1)/y(t) - 1 + y(t-1)/1200 (y in %). Consols are perpetual (callable from
  1923 after Goschen; ignored); check 3 is price only (1/y), insure-1709-1's main reading.
- **Signal and holding are on the same total-return index**, the gym's convention for
  bonds (TLT adjusted close). Cash earns 0 when out (primary; the gym's convention). Being out
  therefore forgoes the coupon, a bias against the rule. Check 1: cash at the end-month
  discount rate (Norges Bank discount rate for Norway; BoE spliced discount rate on prime
  short-term paper for consols), `rate/1200` a month earned while out.
- **Source periods** (labels for the before-scoring table and the per-period nulls; fixed now
  from the documentation):
  - Norway: N1 1822-01..1842-12 quotations abroad; N2 1843-01..1844-12 **interpolated**
    (documented); N3 1845-01..1914-12 quotations abroad; N4 1915-01..1939-12 Oslo Stock
    Exchange; N5 1940-01..1945-12 Oslo, occupation; N6 1946-01..1984-12 Oslo, regulated rates.
    Timing documented: end of month (A1/A3 notes); A4's "averages of most representative
    quotations abroad" is read as an average across markets of end-month quotes (if it is a
    time average, the per-period acf below picks it up; the nulls use it either way).
  - Consols: the splice months are identified after this card as insure-1709-1 did: the months
    where the spliced column's monthly change matches the NBER 1852-1888 column, the Klovland
    1870-1914 column, or the Capie-Webber column to 1e-6 (M10 columns 6, 8, 7). Card default if
    ambiguous: NBER to 1869-12 (C1, timing not stated), Klovland 1870-01..1914-12 (C2, last
    Friday of month), Capie-Webber 1915-01..1926-12 (C3, "mixture of end month and averages").
    1914-08..1914-12 (exchange closed) is flagged; it stays in.

## Before scoring (computed after this card is pushed, before any rule position or episode)

- Per series and source period: months, missing months, lag-1 and lag-2 acf of monthly log
  total returns (demeaned per period, pairs inside the period), the noise line 1.645/sqrt(pairs),
  the share of exactly-zero yield changes, "stale-suspect" if acf1 > noise line or zero changes
  above 20% (insure-1709-1's rule). These set the AR null's coefficients; they change nothing
  else.
- **Fall threshold (the only data-dependent choice, fixed now as a rule on the holding level
  alone):** for each series separately, count confirmed falls of the total-return index
  (`insure1.zigzag`, fall d and rise d) for d = 25%, 20%, 15%, 10%, in that order, in the scored
  window (after the 12 warm-up months). The series' threshold is the **largest d with at least
  8 confirmed falls**; if none has 8, d = 10%. These counts are computed and pushed before any
  rule position exists. Robustness (check 4): the next lower and next higher rung.

## Rule (the project's `tsmom12`, monthly form, code unchanged)

`trend_where_long.signals` via `insure1709.build_seg`: at the end of month k, on if the 12
monthly log total returns dated k-11..k sum to more than 0; the position earns month k+1's
return. In 1, out 0 (cash at 0). 2 bps a side per flip. Segments: maximal runs of months with a
value, at least 60 scored months, 12 warm-up months.

## Episodes and statistics (insure-1 / insure-1709-1, code reused)

- Falls: `insure1.zigzag` on the holding level per segment at the threshold above (fall d, rise
  d); only confirmed troughs count. Scored by `insure1.score`: insurance I (rule minus holding,
  log points, peak to trough), rebound B (12 months after the trough, cut at the next peak), net
  N = I + B, calm C; S = I / |holding's log change|; premium P = -(sum B + C) / sum I.
- **Insurance tests (decisive, primary = Norway):** `insure1.sign_test` (ties dropped,
  one-sided) and `insure1.boot` (10,000 draws, seed 0) of I over the falls; the same for N.
  Headline: falls with I > 0 out of all falls, ties against.
- **Timing (as #87 / insure-1709-1):** fixed exposure (the rule's mean position per segment,
  no costs) S_fix; random dates: 1,000 common rotations of the positions (offset uniform on
  [12, L_max - 12], seed 0), p_rot = share with mean S at least the rule's; gap G = rule S minus
  the mean rotation S.
- **AR-preserving nulls for G (decisive for timing):** 1,000 synthetic worlds per null, each
  run through the same rule, zigzag at the series' threshold, scoring and 200 rotations; p =
  share of worlds with G at least the observed G (worlds without a fall dropped and counted).
  - **AR1:** Gaussian AR(1) monthly log returns with each source period's own mean, sd and
    lag-1 acf (`insure1709.ar1_path`), seed 0.
  - **BB:** stationary block bootstrap of each source period's own monthly log returns, mean
    block 3 months (`insure1709.bb_path`), seed 1.
  - **p_AR = the larger of the two.**
  - Reference (description): iid Gaussian (phi 0), seed 2; and **AAFT phase-randomised
    surrogates** per segment (Theiler et al. 1992: Gaussian ranks, FFT phases randomised,
    remapped to the segment's own returns; keeps the marginal distribution and approximately
    the whole autocorrelation function, including any 12-month momentum), seed 3. AAFT is
    description, not decisive: it also removes real momentum, so it asks a different question
    (is the timing more than linear autocorrelation at any lag?).

## Verdict (Norway, the primary; consols get the same table as a secondary verdict)

| Outcome | When |
|---|---|
| **Holds, timing beyond autocorrelation** | I: sign p < 0.05 and bootstrap p < 0.05, **and** p_rot < 0.05 **and** p_AR < 0.05 |
| **Holds, timing not separable from autocorrelation** | I passes, p_rot < 0.05, p_AR >= 0.05 |
| **In between** | I passes, 0.05 <= p_rot < 0.10 |
| **Holds only as lower exposure** | I passes, p_rot >= 0.10 |
| **Does not hold** | I fails (sign or bootstrap p >= 0.05) with at least 5 falls with I != 0 |
| **Too few falls** | fewer than 5 falls with I != 0 |

Qualifiers, always reported: "at the claimed strength" if the headline share is at least 0.80,
else "weaker than claimed"; "kept" if N passes both tests, else "handed back in the rebound";
"cheaper than holding less" if P < P_fix. A pooled Norway-and-consols description uses linked
clusters (`insure1.link`, overlapping [peak, trough]); it does not change either verdict.

**Kill reading for the SUMMARY claim:** "Does not hold" on Norway means the insurance claim does
not extend to this long bond history; "Holds only as lower exposure" means the bond evidence
adds no timing support. No outcome changes the live rule.

## Checks (description, each a `tries.md` row)

1. Cash at the discount rate when out (both series).
2. Norway with a perpetuity total return (price 1/y + y/12) instead of the 10-year par bond.
3. Consols price only (1/y), signal and holding.
4. Thresholds: the next lower and next higher rung of the ladder (where they exist, both series).
5. Norway sub-periods: 1822-1914 (quotations abroad, before the post-1927 calendar) and
   1915-1984 (Oslo).
6. Norway with the interpolated 1843-1844 months removed (the series splits there).
7. Norway A1 "GOV" column 1820-05..1920-12 (another construction of the same market;
   overlapping, not independent), same rebuild.
8. Stale check: signal one month older (both series).

## Bar and rows

Not a pick: no rule is selected, nothing tuned, one configuration decides. The project-wide bar
(`research/register/BAR.md`, rows through 2026-11-25 22:31: 4,328 distinct tries, N 1,123 for
a new pick) is quoted for scale only; no p here can reach it. `tries.md` (kind `insure-check`,
idea `insure-bonds-1`): one row per primary series (`tsmom12m@insure-bonds-norway`,
`tsmom12m@insure-bonds-consols`) and one per check; the before-scoring table gets a `note` row.
Rotations, null worlds and the fixed control are re-scorings: no rows.
