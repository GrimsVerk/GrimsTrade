# Card fx-peg-1: a real-time peg filter, then trend on floating currencies 1791-1970

Lane `fx-peg-1`, written 2026-11-25 22:55-23:20 UTC, **before any return, fall, filter state,
rule position or episode of the tested series was computed**. Branch `fx-peg-1`. Research
only: fake money, keyless public data, no change to the gym, the daily runner or the live
strategies. Train data only (nothing after 1970-12 is scored).

## Question

The long FX histories cached by data-wide-2 (#206) spend most of their time pegged: gold and
silver standards, wartime pegs, sterling-bloc pegs, Bretton Woods. On a pegged rate a trend
rule scores noise and devaluation jumps, so a currency trend result on these series is not
interpretable until the pegs are taken out, and they must be taken out with what was known at
the time. Two steps:

1. **Tool.** A peg classifier that at each month-end uses only that month's and earlier data,
   with thresholds fixed here, plus an agreement check against a documented regime chronology
   (reported only, never a rule input).
2. **One test.** On the floating spells only, as the filter knew them in real time: does
   monthly `tsmom12` act as **insurance** in large currency falls (smaller losses than holding,
   with timing beyond random dates and beyond an autocorrelation-preserving null), and does it
   earn any **trend premium**? And, descriptively, how much does the filter change the answer
   against the unfiltered series?

## What had been seen when this was written

- SUMMARY (night 6), next-steps.md's lane queue, `gate-null.md`'s headings, the end of
  `tries.md`, data-wide-2's write-up (its currency line: "367 new market-years, 5 falls of
  25%+", USD/GBP 1791-1970 and NOK 1819-1970; the IFS note that pegs must be flagged first),
  insure-1709-1's write-up and card (the model for the statistics here), fx-value-real-1's
  summary (#197: real-rate value, closed, not redone here), pooled-2's FX9 rows in `tries.md`
  (long-only `tsmom12` on 9 currencies against the US dollar, 1974-2025: Sharpe 0.07-0.42) and
  tick-tier-1's summary line on currencies (trend lost Sharpe after 2009). jst-autocorr-2's
  rule (#204): before 1966 a timing test needs a null that keeps the autocorrelation.
- Structure only of the cached files, read with a structure script: sheet names, header rows,
  column spans and gaps to 1970-12.
  - BoE millennium workbook sheet M15 "$/£ exchange rate 1791-2015", units "$'s per £",
    source "Craighead (2010), Federal Reserve Board and ONS", timing not stated; its first six
    values (1791-01..06, about 4.44-4.56) were printed.
  - Norges Bank `fx.xlsx` (Klovland 2004, Norges Bank Occasional Paper 35, ch. 7):
    - Table A1, "end-of-month quotations at Oslo Stock Exchange" (NOK per unit; the speciedaler
      column is "Norwegian speciedaler in Copenhagen"): LONDON 1819-04..1914-12, HAMBURG
      1819-04..1876-12, REICHMARKS 1877-01..1914-12, SPECIEDALER 1820-01..1865-12 (gap
      1841-09..1844-07), PARIS and AMSTERDAM 1881-01..1914-12, ANTWERP 1898-07..1914-12;
    - Table A2, "monthly averages of daily quotations at Oslo Stock Exchange", from 1914:
      GBP 1914-01, USD 1914-09, SEK 1915-10, DEM 1914-01 (gaps 1923-07..1924-11 and
      1945-04..1949-11), FRF 1914-01, DKK 1916-02, NLG 1914-01, CHF 1917-08, BEF_OLD
      1918-12..1926-10, BEF 1926-11, ITL 1920-01, ESP 1920-01 (gap 1939-02..1960-01), FIM
      1919-01, CAD 1946-06, ISK 1946-01, PTE 1946-08, ATS 1955-01, an effective-rate INDEX
      1919-1939; wartime gaps 1940-04..1940-10 and 1945-04..1945-10 in several columns.
    - While reading the header, the first 23 rows of Table A2 (1914-01..1917-02: GBP about
      17.4-19.5, USD about 3.8-4.1, DEM, FRF and NLG levels) were printed. No change or return
      was computed from them.
  - **Found while reading the structure:** data-wide-2's label parser ignores Excel serial
    dates below 10,000, so its Table A2 series start in 1927-05, not 1914 (its "NOK in USD
    1914-" line has no 1914-1927 months). This lane reads serials from 1 up.
- Ilzetzki-Reinhart-Rogoff (IRR) de facto classification, stable version (monthly 1940-2019,
  fine and coarse codes) and anchor currencies (monthly 1946-2019), fetched this lane from
  ilzetzki.com (robots.txt read first: `Allow: /`; the page asks for citation, no other terms).
  Read so far: the code tables and the country column names. No code value was read.
- General knowledge that cannot be unlearned: the dates of the gold standard, the Bank
  Restriction (1797-1821), the US greenback period (1862-1878), the interwar floats and
  stabilisations, the 1931 sterling exit, the 1933 dollar devaluation, the French franc crisis
  of 1924-26, the German hyperinflation, the 1949 and 1967 sterling devaluations.
  **Expectation, stated so it can be wrong:** the filter will mark 1914-1939 (interwar),
  1797-1821 and 1862-1878 on the dollar-sterling rate, and 1819-1842 on the krone as floating,
  and nearly all of 1946-1970 as pegged. On the floats the rule loses less than holding in most
  large falls, mostly because of exposure and drift, with a timing gap that does not clear the
  autocorrelation null (half the data are monthly averages, which add lag-1 autocorrelation by
  construction); a long/short trend premium is positive but not beyond autocorrelation.
  Unfiltered, the devaluation jumps lower the share avoided and dilute the premium.

## Data (fixed now)

Every series is a **price of one unit of a foreign currency in the quoting market's currency,
as quoted** (no inversion): the holder is an investor in that market who holds the foreign
currency. This is pooled-2's convention for FX9 (a US investor holding foreign currencies) and
uses no choice of direction by this lane. Price only: no interest on either currency, cash at 0
when out (the gym's convention).

| Market | Source and timing | Months used (to 1970-12) |
|---|---|---|
| GBP in USD | BoE M15 (timing not stated) | 1791-01.. |
| GBP in NOK | A1 LONDON (end month) to 1914-12, then A2 GBP (monthly average) | 1819-04.. |
| Mark in NOK | A1 HAMBURG (mark banco, end month) to 1876-12; A1 REICHMARKS 1877-01..1914-12; A2 DEM | 1819-04.. |
| FRF in NOK | A1 PARIS to 1914-12, then A2 FRF | 1881-01.. |
| NLG in NOK | A1 AMSTERDAM to 1914-12, then A2 NLG | 1881-01.. |
| BEF in NOK | A1 ANTWERP to 1914-12, then A2 BEF_OLD to 1926-10; A2 BEF (belga) from 1926-11 | 1898-07.. |
| NOK in DKK | A1 SPECIEDALER (Copenhagen, end month) | 1820-01..1865-12 |
| USD, SEK, DKK, CHF, ITL, ESP, FIM, CAD, ISK, PTE, ATS in NOK | A2 (monthly average) | from each start |

- **Joining A1 and A2.** For a currency in both tables, the monthly log changes are A1's up to
  the change dated 1914-12 and A2's from the change dated 1915-01 (A2 1915-01 over A2
  1914-12). No change crosses the two sources, so no timing mix enters one change. A2 levels
  before 1914-12 serve only as the base of that first change.
- **Data runs.** A run is a stretch of consecutive months with a change. It breaks at a missing
  month, at a change of column or unit (HAMBURG to REICHMARKS at 1877-01, BEF_OLD to BEF at
  1926-11), and at any monthly change with |log change| > ln 10 (a redenomination such as the
  1960 new franc or the 1963 new markka, or a data break). The breaking change is never scored
  or used. Signals and the filter use only changes inside the same run.
- The effective-rate INDEX, XEU, ECU and EUR columns are not used. Months after 1970-12 are
  never parsed by the scoring code: the scored FX coverage (`datawide2.SEEN`, pooled-2, data-long-3)
  starts in 1971, so 1791-1970 overlaps no scored currency series.

## Step 1: the peg filter (fixed now)

`research/lib/fxpeg1.py`, `classify(changes, window=24, band=0.01, share=0.80)`:

- At the end of month k, take the 24 monthly log changes of the same run dated k-23..k. If
  fewer than 24 exist: **unknown**. Else **peg** if at least 80% of them have |change| < 1%,
  otherwise **float**.
- Source: the de facto peg test of Reinhart and Rogoff (2004, QJE 119(1)), which calls a regime
  a de facto peg when the monthly change stays within a +/-1% band at least 80% of the time
  over a rolling window. Theirs is a 5-year window read with hindsight; here it is a trailing
  24-month window, so the state at k uses nothing after k, and a float is recognised after at
  most five large monthly moves instead of thirteen.
- Also reported, not used: the trailing 12-month standard deviation of changes.
- The filter state at the end of month k-1 decides whether month k is scored. A devaluation
  out of a peg is therefore excluded (the filter still says peg when it happens), and a new peg
  after a devaluation stays a peg (one large move in 24).
- Monthly averages smooth month-to-month changes (by about a fifth of their standard
  deviation for a random walk), so an averaged float is a little more likely to be called a
  peg. Accepted, not corrected.

**Agreement check (description only; never a rule input):** a monthly bilateral regime label
per market from a documented chronology, compared with the filter state month by month.

- 1946-1970: IRR fine codes (stable version) with IRR anchors. A currency is pegged to its
  anchor when its fine code is 1-4 (no separate legal tender, pre-announced peg or currency
  board, pre-announced band of +/-2% or less, de facto peg). A pair is **peg** when both
  currencies reach the same final anchor through such links (the US dollar is the final anchor
  of the system). It is **float** when either has a fine code of 9-14 and the two are not
  linked as a peg. Codes 5-8 (crawling pegs and narrow crawling bands), 15 and missing are
  **ambiguous**.
- Before 1946: a short hand-coded list per currency in `fxpeg1.CHRONOLOGY` (metal standard,
  float, peg to another currency, or exchange control), from standard secondary sources:
  Eichengreen (1992) *Golden Fetters* and (2008) *Globalizing Capital*; Bordo and Schwartz eds.
  (1984) *A Retrospective on the Classical Gold Standard*; Officer (1996) *Between the
  Dollar-Sterling Gold Points*; Friedman and Schwartz (1963); Klovland (2004) for Norway. Two
  currencies on the same metal, or one pegged to the other, or both pegged to the same third
  currency: **peg**. One on gold and the other on silver (for example 1842-1873 krone against
  sterling, under French bimetallism), exchange control, war and occupation: **ambiguous**.
  Otherwise, when one of them floats: **float**. Month dates are approximate. **Months within 3
  months of a switch in either currency's list are ambiguous.**
- Reported: the share of non-ambiguous market-months where filter and chronology agree,
  Cohen's kappa, and the confusion table (filter float when the chronology says peg, and the
  reverse), for all markets and per market. **Reading fixed now:** agreement of 0.85 or more is
  "the filter matches the chronology"; below 0.85 the verdict carries "filter disagrees with
  the chronology" as a caveat. The chronology never changes the filter, the scored months or
  the verdict.

## Step 2: the test

### Rule (monthly `tsmom12`, as insure-1709-1)

At the end of month k the signal is **on** if the 12 monthly log changes of the run dated
k-11..k exist and sum to more than 0 (`trend_where_long.signals`'s definition). The position
earns month k+1's change: in 1, out 0 (cash at 0). Cost 2 bps a side per flip (`insure2.COST`),
none on a segment's first month.

### Books

- **Filtered (primary):** month k is scored when the filter state at the end of k-1 is float
  and the signal at k-1 is valid. A segment is a maximal stretch of scored months inside one
  run. Segments with fewer than 12 scored months are dropped (counted).
- **Unfiltered (description):** month k is scored when the signal at k-1 is valid; same
  segments rule.
- **Peg-only (description):** months the unfiltered book scores and the filtered book does not.

### Episodes and statistics (insure1 and insure1709 code)

- Falls: `insure1.zigzag` on each segment's holding level, **15% fall and 15% rise**. Only
  confirmed troughs count. 15% instead of the 25% used on stocks because currency moves are
  smaller (about half to two thirds of stock volatility); 10% and 25% are checks.
- Per fall, through `insure1.score` (rebound = 12 months after the trough, cut at the next peak
  or the segment end): insurance `I` over (peak, trough], rebound `B`, net `N = I + B`, all rule
  minus holding in log points; share avoided `S = I / |holding's log change|`; premium
  `P = -(sum B + C) / sum I`.
- **Clusters (effective falls):** `insure1.link` (single linkage on overlapping
  [peak, trough] windows) over all falls of the book. Cluster value = mean over its falls.
- **Insurance tests (decisive):** on the cluster means of `I`, `insure1.sign_test` (ties
  dropped, one-sided) and `insure1.boot` (10,000 draws, seed 0, one-sided p = share of draws
  <= 0); the same for `N` (qualifier). Headline count: clusters with mean `I > 0` out of all.
- **Timing controls (insure1709 code):** mean `S` over falls for the rule; fixed exposure
  (each segment's mean position held constant, no cost) `S_fix`; rotations (1,000 common
  offsets, seed 0, positions rolled mod segment length) `S_rot`; gap `G = S - mean S_rot`;
  `p_rot` = share of rotations with mean S at least the rule's.
- **Autocorrelation-preserving nulls for G (decisive for timing).** 1,000 synthetic worlds,
  each scored with the same rule, falls, rotations (200 a world) and statistics; p = share of
  worlds whose G is at least the observed (worlds without a confirmed fall are dropped and
  counted). The worlds replace the scored months' changes only (earlier months of the run stay
  observed, so the signal at a segment's start keeps its real history) and keep the observed
  filter calendar. To keep the dependence across markets (many pairs share the krone), the
  draws are **joint across segments by calendar month inside each epoch** (an epoch is a
  maximal stretch of calendar months in which at least one segment is scored); a segment that
  has no change at the drawn month takes a random change of its own instead.
  - **AR1:** per segment, x_t - mu = phi (x_{t-1} - mu) + e_t with the segment's own mean mu
    and lag-1 coefficient phi (clipped to +/-0.9); residuals e drawn jointly by calendar month
    (iid months) from the fitted residuals; seed 2.
  - **BB:** stationary block bootstrap (mean block 3 months) of the segments' own changes,
    the block's calendar months shared by all segments; seed 3.
  - **p_AR = the larger of the two.**
- **Trend premium (decisive for the premium question).** The long/short form of the same
  signal, `LS_k = (2 on_{k-1} - 1) x log change_k`, no cost, averaged with equal weights over
  the segments scored in month k; statistic = the mean of that monthly book (reported a year,
  x12). It does not depend on the quoting direction (the long/flat rule equals half holding
  plus half LS). Its nulls are the same joint worlds with **every segment's changes demeaned**
  (no drift: "no trend beyond short-lag dependence"): AR1 (seed 4), BB (seed 5), and an iid
  reference (joint calendar months drawn singly, demeaned, seed 6). p = share of worlds with a
  mean at least the observed. **p_AR_prem = the larger of AR1 and BB.** Also reported, not
  decisive: the same with each segment's own mean kept ("beyond drift").

### Verdicts (filtered book, 15%/15%)

Insurance:

| Outcome | When |
|---|---|
| **Holds, timing beyond autocorrelation** | `I` on clusters: sign p < 0.05 and bootstrap p < 0.05, **and** p_rot < 0.05 **and** p_AR < 0.05 |
| **Holds, timing not separable from autocorrelation** | `I` passes, p_rot < 0.05, p_AR >= 0.05 |
| **In between** | `I` passes, 0.05 <= p_rot < 0.10 |
| **Holds only as lower exposure** | `I` passes, p_rot >= 0.10 |
| **Does not hold** | `I` fails |
| **Too few falls** | fewer than 5 clusters with mean `I` != 0 |

Qualifiers, always reported: "at the claimed strength" if the headline count share is at least
0.80, else "weaker than claimed"; "kept" if `N` passes both tests, else "handed back in the
rebound"; "cheaper than holding less" if `P < P_fix`.

Premium:

| Outcome | When |
|---|---|
| **Trend premium beyond autocorrelation** | mean LS > 0 and p_AR_prem < 0.05 |
| **Premium not separable from autocorrelation** | mean LS > 0, p_iid < 0.05, p_AR_prem >= 0.05 |
| **No trend premium shown** | otherwise |

**Kill rules.** "No trend premium shown": no further currency trend-premium variants on these
1791-1970 histories (other lookbacks, bands, filters). "Does not hold" or "Holds only as lower
exposure": the SUMMARY line "holds everywhere we looked" gets a currency exception. No outcome
changes the live rule; currencies are not traded by the paper books.

### Filter effect (description, no verdict)

The same table for the unfiltered and peg-only books, and the differences filtered minus
unfiltered in: number of falls and clusters, clusters lost less, mean S, S_fix, G, LS mean.
Per market: months scored filtered and unfiltered.

### Checks (description, each a `tries.md` row)

1. Falls 10%/10% and 25%/25%.
2. Filter window 12 and 60 months (band 1%, share 0.80).
3. Filter band 2% (RR's de facto band; window 24).
4. End-of-month sources only (BoE and Table A1; Table A2's monthly averages dropped).
5. Krone markets only (BoE dropped) and the BoE dollar-sterling rate alone.
6. Cost 25 bps a side.
7. Stale check: the signal a month older (decision at the end of k trades month k+2).

## Before scoring (computed after this card is pushed, before any rule position or episode)

Per market and source (end month or average): months, lag-1 acf of monthly log changes and its
rough 5% noise line 1.645/sqrt(pairs), share of |change| < 1%, the filter's share of months
float / peg / unknown, and the chronology agreement. These set nothing: the filter's
thresholds, the books and the verdict rules are fixed above.

## Bar and rows

- Not a pick: nothing is selected or tuned; one configuration decides. The project bar
  (`register/BAR.md`, z 4.70) is out of reach by design with a few dozen falls; quoted for scale.
- `tries.md`, idea `fx-peg-1`: one `note` row for the before-scoring table and the agreement;
  one `insure-check` row per book (`tsmom12m@fx-peg-1-filtered`, `-unfiltered`, `-pegonly`) and
  per check (long/flat rule: Sharpe = mean / sd of monthly returns x sqrt(12), total return,
  max drawdown, flips a year). Rotations and synthetic worlds are re-scorings: no rows.
- No gate id is used.
