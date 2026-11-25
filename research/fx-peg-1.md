# fx-peg-1: a real-time peg filter, then trend on floating currencies 1791-1970

Lane `fx-peg-1`, 2026-11-25 (UTC). Branch `fx-peg-1`. Research only: fake money, keyless public
data, no change to the gym, the daily runner or the live strategies. Card:
[`cards/fx-peg-1.md`](cards/fx-peg-1.md), pushed at 22:59 UTC (commit 1046ef7) before any
return, filter state or position was computed. Before-scoring table: commit c45d135 (23:03).
Tables: [`results/fx-peg-1.md`](results/fx-peg-1.md). Code: `lib/fxpeg1.py`, tests
`tests/test_fxpeg1.py`.

Data, read locally (only statistics are committed):
- Bank of England, "A millennium of macroeconomic data" v3.1, sheet M15, $ per GBP from 1791
  (Open Government Licence);
- Norges Bank Historical Monetary Statistics, exchange rates (Klovland 2004): Table A1 (end of
  month, 1819-1914) and Table A2 (monthly averages, from 1914);
- the Ilzetzki-Reinhart-Rogoff de facto classification and anchors, stable versions, used
  for the agreement check only. Cite: Ilzetzki, Reinhart and Rogoff (2019), "Exchange
  Arrangements Entering the Twenty-First Century: Which Anchor Will Hold?", *Quarterly Journal
  of Economics* 134(2), 599-646, and (2021), "Rethinking Exchange Rate Regimes", *Handbook of
  International Economics* vol. 5 (the classification files used here belong to both). The
  band test behind the filter is Reinhart and Rogoff (2004), "The Modern History of Exchange
  Rate Arrangements: A Reinterpretation", *QJE* 119(1), 1-48.

## The answer on one screen

**On the floating spells the filter found in real time, `tsmom12` lost less than holding in
the large currency falls, but only by holding less: no timing beyond its average exposure.
Its long/short trend return is positive (+4.2% a year, t 4.7). It is not shown beyond
short-lag autocorrelation (p 0.057 against the AR(1) null) and is about what drift plus
autocorrelation give. By the card: insurance "Holds only as lower exposure"; premium "Premium
not separable from autocorrelation". The filter matches the regime chronology a little below
the card's line (agreement 0.84 against 0.85), so both verdicts carry that caveat. Post hoc,
the gap is IRR's 1946-1970 codes, which follow parallel-market rates. Against the hand-coded
list before 1946 the agreement is 0.93.**

| Book (15% falls) | Months | Falls / clusters | Clusters lost less | S: rule / fixed / random (p_rot) | Gap G; p AR1 / BB | Long/short % a year (t) |
|---|---:|---|---|---|---|---|
| **Filtered (primary)** | 3,715 | 41 / 11 | **10 of 11** (sign p 0.001, boot 0.000) | 0.63 / 0.63 / 0.61 (0.457) | +0.02; 0.39 / 0.20 | **+4.17 (+4.70)**; p AR1 0.057, BB 0.000, iid 0.000 |
| Unfiltered | 13,909 | 57 / 4 | 4 of 4 (0.062) | 0.64 / 0.59 / 0.57 (0.049) | +0.08; not run | +1.65 (+4.38) |
| Peg-only | 10,031 | 1 / 1 | 1 of 1 | - | - | +0.01 (+0.03) |

(Rule: at each month-end, hold the foreign currency next month if its 12-month log change is
above 0, else cash at 0; 2 bps a side. Holding = the foreign currency as quoted in the home
market (the dollar-sterling rate as quoted, and Oslo's price of each foreign currency), price
only, no interest. S = share of the fall's log loss avoided. Fixed = each segment's average
position held constant. Random = 1,000 common rotations of the positions. The long/short
book is `(2 x signal - 1) x monthly log change`, equal weight over the segments scored that
month. Its p values come from demeaned worlds, i.e. worlds with no drift.)

- **Insurance: real, but just lower exposure.** In 10 of 11 linked clusters of falls (41
  falls of 15% or more) the rule lost less than holding, and the net gain survived the rebound
  ("kept"). But its share avoided (0.63) is exactly what its average exposure gives (fixed
  0.63; random dates 0.61, p_rot 0.46). Inside floating spells that contain falls, the rule
  was out most of the time. These spells are mostly long one-way moves: the krone's rise to
  its old gold parity in 1924-28, the franc, lira, peseta and mark depreciations, and the
  greenback's recovery in 1864-78. So holding less is all it did. The autocorrelation nulls
  agree that there is no timing: p 0.39 (AR(1) sieve) and 0.20 (joint block bootstrap).
- **Premium: positive, but not beyond what the series' own dependence produces.** The
  long/short book earns +0.35% a month over 1,237 months (t 4.70). With no drift and no
  autocorrelation (iid worlds), it would earn about 0 (5-95%: -1.4% to +1.4% a year). AR(1)
  worlds with each segment's own lag-1 coefficient give a median of +2.5% a year (5-95%:
  +0.7% to +4.2%). The observed +4.2% sits at their 94th percentile (p 0.057). The joint block
  bootstrap is narrower (median +0.8% a year, p 0.000). The card takes the larger p, so the
  premium is "not separable from autocorrelation". With each segment's mean kept (drift plus
  dependence) the observed value is at the median (p 0.50). The return is what drift plus
  short-lag dependence produce, and nothing more.
- **Where the autocorrelation comes from.** Most krone markets after 1914 are Table A2's
  monthly averages, whose lag-1 autocorrelation is +0.12 to +0.60 (the mark +0.60, the dollar
  +0.41; Iceland aside, which is never scored). An average of daily quotes adds about +0.25 by
  construction (Working 1960). Check 4 keeps only the sources not documented as averages:
  Table A1 (end of month) and the BoE rate (timing not stated). On those the long/short book
  earns +2.2% a year (t 2.4, no null run) and the timing gap is +0.19 (p_rot 0.057, 8
  clusters). This is a description on 9 falls, not a test, and the BoE rate may not be
  end-of-month data: without the 1857 spike (data note below) its lag-1 autocorrelation is
  +0.32, which looks more like an averaged or smoothed series than end-of-month quotes.
- **What the filter changes (description).** It keeps 3,715 of 13,909 scored months (27%). The
  long/short return a year goes from +1.65 (unfiltered) to +4.17 (floats). The pegged months
  earn nothing (+0.01, t 0.03): a trend rule on a pegged rate scores noise. The pegs hold only
  one confirmed 15% fall (the Belgian franc, 1919-20). Devaluations out of pegs are one-way
  drops that never rebound 15%, so in the peg-only book they are unfinished falls (19, for
  example sterling in dollars 1927-31 and 1942-68, the franc 1946-49). The filtered book never
  scores the devaluation month itself, because the filter still says "peg" then. Unfiltered, single linkage chains 57 falls over long
  segments into 4 clusters, too few for the card's test. Its larger timing gap (+0.08,
  p_rot 0.049) mixes pegged and floating months and was not put through the AR nulls.
- **Unfinished falls (not counted by the card).** 22 more falls were still running when their
  floating spell ended. Most are the big one-way moves that ended in a return to gold in
  1926-28 or in the gold bloc's end in 1935-36. There the rule avoided a median 0.87 of the
  loss to the low (range 0.14-1.00). The card counts only confirmed troughs, and fixed
  exposure in those spells is also low, so this does not change the timing reading.

## Step 1: the filter and its agreement with the chronology

- **Rule** (`fxpeg1.classify`, fixed in the card). At the end of month k, take the 24 monthly
  log changes dated k-23..k. If at least 80% are below 1% in absolute value, the month is a
  peg, otherwise a float. With fewer than 24 changes in the run it is unknown. This is
  Reinhart and Rogoff's (2004) de facto peg band test, moved to a trailing window. The state at
  k-1 decides whether month k is scored, so a devaluation out of a peg is never scored, and a
  new peg after one jump stays a peg. A test checks that rewriting the future does not change
  any past state.
- **Agreement (description only, never an input).** The reference is a hand-coded
  per-currency regime list before 1946 (`fxpeg1.CHRONOLOGY`: metal standards, floats, pegs to
  another currency, controls and wars; month dates approximate, from Eichengreen, Bordo and
  Schwartz, Officer, Friedman and Schwartz, and Klovland). From 1946 it is the IRR fine codes
  with anchors. Fine codes 1-4 count as a peg to the anchor. Codes 9-14 count as float: this
  includes 9-12 (wide crawling bands, moving bands, managed floating) as well as free floats
  and free falls (13-14). Codes 5-8 (narrow crawls) and 15 are ambiguous. Months within 3
  months of a switch, silver against gold, controls and wars are ambiguous and left out. The
  code applies the 3-month buffer to an anchor currency too, which goes slightly beyond the
  card's "either currency": for the krone pegged to sterling in 1933-39, a switch of sterling
  also makes the krone pairs ambiguous.
  - The two agree on **0.841** of 10,862 market-months (kappa +0.65), below the card's 0.85.
  - Most of the disagreement is one-sided: 1,520 months where the filter says peg and the
    reference says float, against 212 the other way.
  - **Post hoc, the gap is almost all in 1946-1970, against IRR** (description, not on the
    card). Against the hand-coded list before 1946 the filter agrees on 0.93 of 6,983 months
    (kappa +0.86; 212 and 273 months the two ways). Against IRR in 1946-1970 it agrees on 0.68
    of 3,879 (kappa +0.05): every one of the 1,247 disagreements is IRR "float" and filter
    "peg". IRR codes the krone 12 (managed floating) in 1946-1954 and 11 in 1955-56, and
    several other currencies similarly in the early 1950s. Its de facto codes use
    parallel-market rates where exchange controls held (Reinhart and Rogoff 2004), while the
    filter reads Oslo's official quotations, which were pegged. So the shortfall below 0.85
    comes from what the two measure in the exchange-control years. It is not the filter
    missing floats, but by the card's rule the caveat stands.
  - Per market agreement runs from 0.65-0.82 (dollar, Danish krone, Finnish markka, Swiss
    franc, Belgian franc, Swedish krona, lira, Canadian dollar, escudo) to 0.86-1.00 (sterling,
    mark, franc, guilder, speciedaler, peseta, schilling). The Iceland krona has 38 comparable
    months, all in disagreement.
  - So the filter errs towards excluding floats, not towards scoring pegs: it says float where
    the reference says peg in only 212 market-months (2% of the comparable ones). For the
    test that is the safer error, but it drops quiet floats, so the floats it keeps are the
    volatile ones.
- **It recognises floats late.** It needs five large monthly moves in 24, so a float that
  starts with a jump out of a peg is scored only once those moves are in the window:
  - sterling's exit from gold in 1931: sterling in dollars is scored from 1932-02;
  - the dollar's 1933 devaluation: the dollar in kroner is scored from 1932-02 because of
    sterling's moves, but its 1933-34 fall is cut short at the end of the spell (unfinished).

  The fast first leg of a break is lost by design: the filter knows the regime only after it
  has seen it.

## How sure

- **Few independent events.** 41 falls, 11 clusters. Cluster 9 alone holds 20 falls of
  1920-07 to 1923-02 in 11 markets: the krone's own swings and the mark, franc and Belgian
  franc depreciations. Almost all floating months are 1793-1879 (sterling in dollars and the
  krone's paper years 1821-1845) and 1915-1940. 1946-1970 adds only the Canadian dollar
  1952-53 and the franc 1949-50.
- **Shared krone leg.** 16 of the 18 markets are prices in kroner, so a krone move shows up in all
  of them. Linked clusters and the joint worlds (draws shared by calendar month) keep that
  dependence. A test checks that two identical markets get identical bootstrap worlds.
- **The premium null is the decisive weakness.** The two autocorrelation nulls disagree (AR(1)
  p 0.057, block bootstrap p 0.000), and the card's max-rule makes the AR(1) sieve decide.
  The AR(1) sieve fits phi per segment; on short spells a strong trend inflates phi, so this
  null may absorb some genuine trend. On end-of-month data alone the premium is smaller (+2.2%
  a year). Either way, nothing here shows a currency trend premium that the monthly
  averages' smoothing could not produce.
- **Filter disagreement caveat** (card): agreement 0.841 < 0.85. The chronology is approximate
  by month, and IRR codes several of these currencies as managed in ways the 1% band calls
  pegs, so part of the gap is the reference, not the filter. The card's rule still applies.
- **Price only, no interest.** Holding a currency earns its interest rate. Interest
  differentials (carry) are missing on both sides: the rule forgoes them while out. Monthly
  decisions, 2 bps a side. Cost 25 bps changes nothing (check 6).
- **Checks** (all description; `results/fx-peg-1.md`):
  - falls of 10%: 13 of 17 clusters lost less; S 0.62 against fixed 0.61. Falls of 25%: 6 of
    6, S 0.79 against fixed 0.67, p_rot 0.027, the one check with timing.
  - filter windows of 12 and 60 months and a 2% band: the same picture (S rule within 0.05 of
    fixed, p_rot 0.45-0.72); long/short +4.2% to +6.0% a year.
  - krone markets only: 6 of 6, no timing, long/short +7.4%. The BoE rate alone: 5 of 6, S
    0.61 / 0.50 (p_rot 0.19), long/short +1.3% (t 1.2).
  - a one-month-older signal: the gap goes from +0.02 to -0.01 and long/short from +4.2% to
    +3.4% a year.
- **Not shown:** that the filter is the best one; nothing was tuned, and the three filter
  variants agree. Interest-inclusive returns. Any period after 1970.
- **Data finding.** data-wide-2's label parser drops Excel serial dates below 10,000, so its
  Norges Bank Table A2 series start in 1927-05, not 1914 (its "NOK in USD 1914-" line has no
  1914-1927 months). `fxpeg1.label_month` reads them. data-wide-2's currency counts (367
  market-years, 5 falls of 25%+) therefore miss 1914-1927 of the A2 series, and the 5 falls
  may include the spurious 1857 BoE fall (data note). The dw2-dates-1 lane is fixing
  data-wide-2's parser; this lane does not edit data-wide-2's files.
- **Data note: a one-month spike in BoE M15.** The $/GBP rate reads 4.876 (1857-09), 8.924
  (1857-10) and 4.843 (1857-11): one month at almost twice its neighbours (log changes +0.604
  and -0.611). It stays below the card's ln 10 break rule, so the card's data rules keep it.
  - It sets the GBP-in-USD lag-1 autocorrelation in the before-scoring table at -0.092; without
    those two changes it is +0.321.
  - It creates a spurious 48% fall, 1857-10 to 1861-01, in the unfiltered book (cluster 3 of
    its episode table) and an unfinished one in the peg-only book.
  - The filtered (primary) book never scores 1857 (the filter calls it a peg), so no verdict
    changes. `results/fx-peg-1.md` has the same note, regenerated by `fxpeg1.py run`.

## Kill rules applied

The premium verdict is "not separable", not "no premium", so the card's kill rule (no more
trend-premium variants on these histories) is not triggered. But the observed premium matches
what drift plus dependence give (p 0.50), and nothing here points to a variant worth trying.
The insurance verdict is "lower exposure only". By the card, the SUMMARY line "holds
everywhere we looked" gets a currency exception. Currencies on floating spells, 1791-1970:
lost less in 10 of 11 clusters, through exposure, not timing.

## Logged

`tries.md`, idea `fx-peg-1`:
- 3 `note` rows: the before-scoring table and the agreement, the post-hoc agreement split,
  and a correction (the first note says "23 FX markets"; it is 18 markets in 23
  market-source rows);
- 13 `insure-check` rows, variants `tsmom12m@fx-peg-1-*`: the filtered, unfiltered and
  peg-only books and 10 checks. Sharpe = mean / sd of monthly long/flat rule returns x
  sqrt(12). The Return column chains all segments end to end, so it is not a portfolio return.

Rotations and synthetic worlds are re-scorings: no rows. Downloads: the two IRR workbooks
(10.5 MB and 12.1 MB) from ilzetzki.com into the local data cache, under `fx-peg-1/irr/`.
robots.txt allows it (a copy is saved there as `robots.txt`); the page asks only for the
citation above. The BoE workbook and the Norges Bank file were
already cached by insure-1709-1 and data-wide-2. No gate id is used.
