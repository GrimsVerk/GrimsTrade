# Wide 8: a forward test for the turn-of-year loser rebound, gates for W16 and W15

Research run wide-8, 2026-11-18. Branch `wide-8` (from `wide-7`), draft PR into `wide-7`.
Research only: fake money, public data, no change to the gym, the daily runner or the live
strategies.

**Family count carried in:** 70 mechanisms, 16 tested by a strategy, none passed (wide-7). A
strategy test in this run would be read at **p < 0.10 / 70 = 0.00143** (family), and
project-wide at the register's bar (`git show origin/register-1:research/register/BAR.md`, read
2026-11-18: **2,904 tries, N 1,012 for a new pick, Bonferroni p <= 4.9e-5**).

Method as in ann-1, wide-6 and wide-7: a gate is an event study whose rule, script and tests are
pushed before any number; it is descriptive, gets no `tries.md` row and does not count as a
tested mechanism. One dry run that prints counts only, then one real run.

## Step 1. Pre-register the turn-of-year ETF loser rebound as a forward test

### Where the lead came from, and why it cannot be tested on train

wide-7's W14 gate showed, as a cell that did not gate, that ETFs with a larger loss for the year
to the end of November rose more from the last close of December to 10 January: slope +0.089
per unit of loss in tax years 2012-2024 (t 3.9, clustered by year), +0.043 (t 1.0) in 1994-2011.
The same table's late placebo window (S+46..S+60, which no story predicts) gave t -4.1 and +2.5.
The lead was found by looking at those years, so those years cannot judge it. Tax year 2025 (the
turn of 2025/26) lies in the held-out year, which this lane does not read. **The first turn
nobody has seen is 2026/27.**

### The design issue, and the null distribution

wide-7 read its t against a standard normal. That is the wrong null for this design: 13-18 year
clusters, no small-sample correction, losers concentrated in a few years (2001, 2002, 2008,
2022), and the ETFs' returns inside one window strongly correlated (an equity sell-off makes
the equity funds losers together and their next ten days move together). The late placebo
window hitting |t| 4 is what that looks like.

The fix, for this forward test and for any later pooled reading of it: **the null distribution
is empirical, not N(0, 1).** It is the distribution of the very same statistic computed on
**placebo windows**: the same construction anchored at the end of each other calendar month,
over train years only. Exactly:

- For anchor month m (January to November) of year Y, let E = the last calendar day of month m
  of year Y.
- Dose: YTD-like return over the eleven months ending one month before the window, as in the
  real design: P = log(close on the last bar on or before the last day of month m-1 of Y /
  close on the last bar on or before E minus 12 months, i.e. the last day of month m of Y-1);
  loss L = max(0, -P). (For m = December this is exactly wide-7's YTD to the end of November.)
  The last bar of the dose must fall in month m-1.
- Outcome: R = log return from the last close on or before E to the last close on or before
  E + 10 calendar days (for m = December: 31 December to 10 January, wide-7's window).
- Statistic per window: the OLS slope b of R on L across the eligible ETFs, with an intercept,
  and its **plain OLS t** (residual variance with n - 2 degrees of freedom). One window = one
  number t.
- Eligible window: at least 15 of the 21 ETFs have the dose and the outcome, and at least 3 of
  them have L > 0. Every bar read lies on or before 2025-11-10 (train).
- The null = the list of t over all eligible placebo windows (Y, m), m = January .. November,
  Y = 1994 .. 2025. December anchors are never in the null (they hold the turn of the year the
  lead came from).

What the null absorbs: the cross-sectional correlation of fund returns, the clustering of losers
in crash years, any ordinary reversal or momentum of 11-month losers over ten days in other
months. What it does not absorb: a seasonal that is special to the turn of the year, which is
the hypothesis. So the forward question is: **is the 2026/27 turn-of-year slope's t extreme
against what the same statistic does in ordinary months?**

The null list is computed once from train, written into the proposed registry entry, and frozen
with it. A scorer in January 2027 reads the list; it never recomputes it.

### The forward test (fixed now, before any number of this step)

- **Universe (21 ETFs, as wide-7):** SPY, QQQ, IWM, XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV,
  XLY, EFA, EEM, VNQ, TLT, IEF, LQD, GLD, SLV, DBC. Dividend-adjusted daily closes (total
  return: bond funds go ex-dividend on the first business days of January) from the keyless
  Yahoo chart endpoint as `research/lib/fetch.py` downloads them. A fund that has no bar in the
  dose or the window is left out; the turn is scored if at least 15 remain.
- **Loser definition:** YTD = log(close on the last bar of November 2026 (2026-11-30) / close on
  the last bar on or before 2025-12-31). L = max(0, -YTD). A loser is an ETF with L > 0.
- **Entry / exit:** entry at the close of the last bar on or before 2026-12-31 (Thursday 31
  December 2026), exit at the close of the last bar on or before 2027-01-10 (Friday 8 January
  2027). R = log(exit / entry). Close to close: a descriptive forward test of the price effect,
  not a gym trade (the gym fills at the next open).
- **Metric:** the plain OLS t of the slope b of R on L across the eligible ETFs, with an
  intercept (the same statistic as each null window's).
- **p:** p = (1 + number of null t at or above the 2026/27 t) / (1 + number of null t).
  One-sided: the lead predicts b > 0.
- **Pass rule:** pass if the turn has at least 15 ETFs and at least 3 losers, b > 0 and
  **p <= 0.02**. Fail otherwise.
- **Too few losers:** if fewer than 3 of the ETFs have L > 0 at the end of November 2026, the
  turn gives no verdict (the dose is known a month before the window, so this is not a choice
  made after the outcome); the same rule, unchanged and under the same id, is scored on the next
  turn that has at least 3 losers.
- **When:** scoreable from 2027-01-12 (the first weekday after the window), once the cached
  bars run past 2027-01-10. The scorer reads bars from 2025-12-31 on: the YTD dose uses bars of
  the held-out year 2025-11-11..2026-11-09, as a dose only (no rule is evaluated on that year;
  carry-3 already spent it, per the forward registry's note).
- **Alpha 0.02**, not the registry's 0.025: the four candidates of `forward-1` already share
  0.10 one-sided (0.025 each); with a fifth, an even split is 0.02. If the owner freezes a
  different batch, alpha is the batch's split, fixed at freeze.
- **One turn, one verdict.** The verdict uses the first eligible turn only. Later turns may be
  shown, and could be combined (Fisher's method over the per-turn p, each from the same frozen
  null) only under a new id (`@2`) frozen before its first turn.

Power is computed from the placebo windows only (no turn-of-year window is read): add b* L to
each placebo window's R and count how often its t clears the null's 98th percentile, for b* =
0.089 (the lead's optimistic post-2012 slope) and half of it. Written before the run: **my guess
is power 15-35% at b* = 0.089** (a ten-day cross-section of 21 correlated funds is noisy, and
the effect is about 1.8% for a 20% loser); so a fail in January 2027 says little and a pass
would be the first forward-confirmed lead of the project.

The entry goes to `research/forward/proposed-wide8.jsonl` in the registry's field names, status
"proposed, NOT frozen". This branch does not hold `src/grimstrade/forward.py` (it is on
`forward-1`), so nothing is frozen and no hash is final: freezing needs an owner decision and
the forward-1 code on one branch.

### Gate-like disclosures

Not a strategy and not a gate on train: no `tries.md` row. The null computation reads only
placebo (non-December) windows of train years; no turn-of-year window is computed in this run.

### What came out (one run, 2026-11-18; table `results/turn-of-year-null.md`)

**The empirical null is more than twice as wide as the normal one wide-7 read its t against:
over 153 placebo windows (anchors January-November, 2005-2025, train only) the cross-sectional
t has standard deviation 2.18, and 35% of windows have |t| >= 2 (5% under N(0, 1)). A pass in
January 2027 needs t >= 4.87. At the lead's own (optimistic) slope that happens in 8% of
placebo windows: one turn is almost powerless.**

| Null t | 2% | 5% | 50% | 95% | 98% |
|---|---:|---:|---:|---:|---:|
| 153 placebo windows | -4.26 | -3.34 | -0.06 | +3.33 | +4.55 |

- Power (b* L added to each placebo window's return): 8% at b* = 0.089, 5% at half of it.
  My guess before the run was 15-35%: too high. Ten days of 21 funds that move together give
  a cross-section with only a few independent bets.
- On the design issue: under a null that carries the design's own correlation, t values of
  3 to 4 are common. A one-window cross-sectional t of 3.9 would rank 6th of 154 here (p
  0.039; 9 of 153 placebo windows have |t| >= 3.9, the largest +8.9). wide-7's pooled
  year-clustered t is not the same statistic, so this is an analogy, not a re-test (no
  turn-of-year window was computed); it says the lead's t 3.9 is weaker evidence than it read.
- **Proposed entry:** `research/forward/proposed-wide8.jsonl`, id `turn-of-year-losers@1`,
  status proposed, NOT frozen; code hashed at commit 4dc070a; the null's 153 t values are in
  the entry, so the January scorer only reads them. Metric `placebo_rank` is new to the
  registry (forward.py on `forward-1` knows `sharpe`, `mean`, `win_rate`): freezing needs that
  metric added, or the entry recast.
- **What the registry should take from this:** a single turn is a weak test (8%), so the
  2026/27 verdict will most likely be "fail" whatever the truth. A multi-turn version (Fisher
  over turns, same frozen null) would need to be frozen as `@2` before its first turn; with 8%
  power a turn, it needs on the order of ten or more turns: it falls in the registry's "decide
  on other grounds" bin, like three of forward-1's four candidates.

How a future lane scores it (from 2027-01-12): refresh `research/data/adj` with
`research/lib/fetch.py`, then `SCORE=1 uv run python -I research/lib/wide8_turn.py`. The
scorer refuses tax years before 2026, reads the frozen null from the entry and prints funds,
losers, b, t, p and the verdict. If the 2026 dose has fewer than 3 losers it says so and the
next turn is scored instead.

Disclosures: one dry run (`DRY=1`) printed only the count of eligible placebo windows per
month (153 in 21 years), then one run. Rule pushed at ae4f76c, code and tests at 4dc070a, both
before either run. No `tries.md` row (not a strategy, not a test on train).

## Step 2. W16 `geomagnetic-storm` (heliophysics)

### Data access (checked 2026-11-18, before any price was cut by it)

GFZ Potsdam's file `https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_since_1932.txt` (the old host
kp.gfz-potsdam.de redirects there) downloads without a key or account. Its header: licence
**CC BY 4.0** for Kp, ap and Ap (the sunspot numbers in the same file are CC BY-NC 4.0; not
used), cite Matzka et al. (2021), Space Weather, doi 10.1029/2020SW002641. Daily Ap from
1932-01-01 to the day before download (recent values are nowcasts; all train-year values are
definitive). The file goes to `research/data/kp/` (gitignored, never committed); the script
reads it as text.

### The idea and literature

Severe geomagnetic storms are linked in medical studies to depression and sleep disruption; if
mood moves prices, stock returns should be lower in the days after a storm. A clock set by
the Sun, with no calendar collision.

- **Krivelyova and Robotti (2003)**, "Playing the field: Geomagnetic storms and the stock
  market", Federal Reserve Bank of Atlanta working paper 2003-5 (revised as 2003-5b, October
  2003). `[record]` Abstract (RePEc): "the previous week's unusually high levels of
  geomagnetic activity have a negative, statistically and economically significant impact on
  today's stock returns" for the world index and most country indices; read as misattribution
  of mood. `[memory]` A six-day post-storm window, US indices back to the 1930s, sample ending
  about 2000; storm thresholds on Ap not checked in the paper.

So the paper's years overlap our GSPC years (1950-2002 here); **post-sample = 2003-2025** (SPY,
solar cycles 23's tail, 24 and 25 with the May 2024 G5 storm). No run here has cut returns by
Ap.

### Decision rule (fixed and pushed before any number)

**Series.** SPY dividend-adjusted closes, train bars only (to 2025-11-10); the S&P 500 index
(GSPC, price only, from 1950) for the in-sample check. Daily log close-to-close returns.

**Storm exposure.** Storm on UT day d with daily Ap(d). A session t is in the window of d if it
is one of the first six sessions dated after d (strictly: the session on day d itself is
concurrent and not counted). M(t) = the largest Ap(d) over all d whose window holds t, i.e.
over UT days d with date(t-6) <= d < date(t). **Severe**: M(t) >= 100. **Minor-to-major**:
30 <= M(t) < 100. Everything else is calm.

**Regression.** r(t) = a + b_sev Sev(t) + b_min Min(t) + e, Newey-West t with 5 lags (the
windows overlap). b = extra daily return on post-storm sessions over calm ones.

**Gate.** Pass only if all four hold:
1. SPY 2003-01-01..2025-11-10: b_sev < 0 with t <= -2.
2. Dose: on the same sample, b_sev < b_min (severe storms matter more).
3. GSPC 1950-2002 (in the paper's years): b_sev < 0.
4. Placebo calendar: the true SPY 2003-2025 b_sev ranks among the 2 most negative of 31: the
   true one and the same regression with the whole Ap calendar shifted by k x 61 days, k = -15
   .. -1, 1 .. 15 (61 days is not a multiple of the 27-day solar rotation, so a shift breaks
   the storms' recurrence; Ap values outside the file count as calm). This is the empirical
   null of step 1 applied to time instead of funds.

On a pass: a card for a `tsmom12` overlay (SPY out for the six sessions after a severe storm)
with rows in `tries.md`, read at p < 0.00143 (family) and the register's p <= 4.9e-5. On a
fail: W16 dead by the gate, no card, no row.

**Shown, not gating.** The same regression on GSPC 2003-2025 and SPY 1993-2002; a threshold of
Ap >= 50 in place of 100; a continuous dose log(1 + M(t)); the raw mean six-session return
after severe storm days; the count of severe and minor storm days and flagged sessions per
sample; the 31 shifted b_sev.

**Power, written before any number.** SPY's daily standard deviation is about 1.2%. Severe
days (Ap >= 100) are rare: perhaps 15-25 UT days in 2003-2025, about 100 flagged sessions after
overlaps, so the standard error of b_sev is about 12 bps a day and t <= -2 needs about -25 bps
a day, -1.5% over six sessions. The gate can only see a large mood effect.

**My guess before any number.** b_sev between -15 and +15 bps a day, |t| < 1.5 post-sample;
b_min near zero; GSPC in-sample slightly negative. Chance of a pass: 2%.

### What came out (one run, 2026-11-18; table `results/geomagnetic-storm.md`)

**The gate fails on three of four counts. After 2003, SPY rose more, not less, in the six
sessions after a severe storm: +18.2 bps a day over calm sessions (t +2.46, wrong sign), minor
storms +0.8; the true calendar ranks 29 of 31 shifted ones (shifted values -16 to +23 bps a
day). Only the in-sample sign holds, weakly: GSPC 1950-2002 -4.4 bps a day (t -1.05). W16
`geomagnetic-storm` is dead by the gate: no card, no strategy, no `tries.md` row.**

| Sample, bps a day (NW t) | Severe (Ap >= 100) | Minor (30-99) | Severe days | Raw 6 sessions after a severe day |
|---|---:|---:|---:|---:|
| SPY 2003-2025 (gate) | +18.2 (+2.46) | +0.8 (+0.24) | 19 | +1.34% |
| GSPC 1950-2002 (gate, in-sample) | -4.4 (-1.05) | +2.7 (+1.58) | 108 | -0.11% |
| SPY 1993-2002 (shown) | -28.7 (-1.77) | +6.6 (+1.38) | 11 | -1.62% |

- **Post-sample the sign is wrong, and a t of +2.5 is ordinary here:** 19 severe days (84
  flagged sessions) is about a dozen episodes, 13 of the 19 days in 2003-2005 (the
  2003 Halloween storms, July and November 2004), the rest in 2015, 2017 and 2024 (May,
  August, October); the shifted calendars throw up values from -16 to +23 bps a day, and the true one sits
  third from the top. The step-1 lesson again: with few clustered events, |t| 2.5 is noise.
- **In the paper's years the effect is small:** GSPC 1950-2002 shows -4.4 bps a day after
  severe storms (t -1.05, 108 severe days) and the continuous dose nothing (+0.5, t 0.39).
  The largest negative cell is SPY 1993-2002 (-28.7, t -1.8, 11 days), inside the paper's
  sample: an in-sample effect of a published paper, as for the other published calendar
  effects here.
- **No dose-response anywhere:** minor storms are slightly positive in every sample.
- **Compared with my guess:** b_sev between -15 and +15 with |t| < 1.5 post-sample: no (+18.2,
  t 2.46, the wrong side). b_min near zero: yes. GSPC in-sample slightly negative: yes. 2%
  chance of a pass: no pass. Published calendar or mood effects out of their papers' years:
  now 0 for 6 here.

Disclosures: one dry run (`DRY=1`) printed only storm-day and session counts, then one run.
Rule pushed at 070d5ab, script and tests at 84bde3e, both before either run.

## Step 3. W15 `cat-claims` (catastrophe meteorology)

### Data access (checked 2026-11-18, before any price was cut by it)

NOAA's National Hurricane Center publishes the Atlantic best-track file HURDAT2 at
`https://www.nhc.noaa.gov/data/hurdat/`; the latest, `hurdat2-1851-2025-092326.txt` (seasons
1851-2025), downloads without a key or account. A US government work (public domain). Each
six-hourly record carries a record identifier; `L` marks a landfall, with time (UTC), status,
position and maximum sustained wind (knots). The file goes to `research/data/hurdat/`
(gitignored); the script reads it as text.

### The idea and literature

After a large US hurricane landfall, property and casualty insurers must pay claims within
months and hold mostly bonds; they sell liquid bonds to pay. The selling is forced and sized by
the loss. Corporate bonds (thinner) should show it more than Treasuries.

- **Massa and Zhang (2021)**, "The spillover effects of Hurricane Katrina on corporate bonds
  and the choice between bank and bond financing", Journal of Financial and Quantitative
  Analysis 56(3), pp. 885-913. `[search summary]` Property insurers heavily exposed to Katrina
  cut their corporate bond holdings by 14% (others by 1%); bonds of issuers held by exposed
  insurers had a large drop in risk-adjusted returns, though the issuers were outside the
  region. One event, bond-level, not an index-level test across landfalls.

No run here has cut bond returns by landfalls. The years that can judge it fully are the 2026
season on.

### Decision rule (fixed and pushed before any number)

**Events.** From HURDAT2, every storm with at least one landfall record (`L`) on the US
mainland: latitude >= 24.4 N, longitude between 98 W and 66.9 W, excluding points south of
30 N and east of 80.0 W (Bahamas) and south of 25.85 N and west of 97.0 W (Mexico). Event day
= the UTC date of the storm's first US landfall record; dose = **category** from the largest
maximum wind over its US landfall records (Saffir-Simpson in knots: < 64 = 0, a tropical-storm
landfall; 64-82 = 1; 83-95 = 2; 96-112 = 3; 113-136 = 4; >= 137 = 5). Events whose event day
falls from 2002-08-01 (LQD and TLT start 2002-07-30) and whose window ends by 2025-11-10.

**Outcome.** Y = log return of LQD minus 0.5 x log return of TLT (a fixed duration hedge: LQD's
duration is about half of TLT's), from the last close on or before the event day to the close
of the 20th session dated after it. Dividend-adjusted closes, train bars only.

**Regression.** Y_e = a + b Category_e + e over events, t clustered by season (year).
b < 0 means corporates lag Treasuries more after stronger landfalls.

**Gate.** Pass only if all three hold:
1. b < 0 with t <= -2 over all events 2002-2025.
2. b < 0 in both halves (event days 2002-2013 and 2014-2025).
3. Placebo calendar: the true b ranks among the 2 most negative of 23: the true one and the
   same regression with every event day moved to the same month and day k years away, k = -11
   .. -1, 1 .. 11 (doses kept; same season, no landfall; a moved event outside 2002-08-01 ..
   the train end is dropped for that k; 29 February goes to 28 February).

On a pass: a card (for example an overlay holding TLT in place of LQD-like credit after major
landfalls; the six-asset book holds no LQD, so the card would need its own universe) with rows
in `tries.md`, read at p < 0.00143 (family) and the register's p <= 4.9e-5. On a fail: W15
dead by the gate, no card, no row.

**Shown, not gating.** Slope on category for LQD alone, TLT alone and LQD minus IEF (IEF's
duration is close to LQD's); mean Y for major landfalls (category >= 3) minus tropical-storm
landfalls; a 60-session window; the event count per category; the 22 shifted slopes.

**Power, written before any number.** The LQD - 0.5 TLT spread moves about 0.35% a day, about
1.6% over 20 sessions; with about 80 events and a category spread of about 1.3, the standard
error of b is about 0.15 points per category and t <= -2 needs about -0.3 points per category
(-1.2% over 20 sessions for a category 4). Only a large flow effect can pass.

**My guess before any number.** b between -0.15 and +0.15 points per category, |t| < 1.5; the
largest single cell Katrina-Rita-Wilma 2005 either way. Chance of a pass: 2%.

### What came out (one run, 2026-11-18; table `results/cat-claims.md`)

**The gate fails on all three counts. Over 104 US landfalls 2002-2025, the 20-session return of
LQD minus half of TLT does not fall with the storm's category: +0.01 points per category (t
+0.09); -0.44 (t -0.63) in 2002-2013 and +0.13 (t +1.84) after; rank 8 of 23 year-shifted
calendars. Corporates did not lag Treasuries after major landfalls; if anything they led (major
minus tropical-storm landfalls +0.91 points). W15 `cat-claims` is dead by the gate: no card,
no strategy, no `tries.md` row.**

| 20 sessions after landfall, points per category (t by season) | Slope |
|---|---:|
| LQD - 0.5 TLT (gate), 104 events | +0.01 (+0.09) |
| LQD - IEF (duration-matched) | +0.01 (+0.11) |
| LQD alone | -0.38 (-1.97) |
| TLT alone | -0.78 (-2.96) |

- **No credit leg.** Of the 17 major landfalls, 14 saw the spread rise (Irma +2.1, Ian +1.9,
  Zeta +2.8); only Laura (-1.3) and Rita (-0.4) fell noticeably. Massa and Zhang's Katrina
  selling (a bond-level, cross-issuer effect) does not show at the index level: Katrina's
  window is +0.38.
- **What moves is duration, not credit:** both LQD and TLT fell after stronger landfalls (TLT
  -0.78 points per category, t -3.0), and the duration-matched spread is flat. A shown cell,
  read after the run: with 24 seasons and a t computed against the normal, this is no stronger
  than the cells this night's nulls put at |t| 3 (steps 1 and 2), and the season-clustered
  events sit in late summer, when the bond calendar has its own patterns. Not a lead; noted
  only.
- **The first half's negative slope is crisis timing:** 2008's Gustav and Ike (category 2)
  landed in the September of the Lehman failure. The second half has the sign the other way.
- **Compared with my guess:** b between -0.15 and +0.15 with |t| < 1.5: yes (+0.01, t 0.09).
  Katrina-Rita-Wilma either way: +0.38, -0.42, -0.05. 2% chance of a pass: no pass.

Disclosures: one dry run (`DRY=1`) printed only event counts (104 events in 24 seasons; by
category 58, 20, 9, 9, 7, 1; halves 53 and 51), then one run. Rule pushed at 261b47a, script and
tests at 4ead496, both before either run.
