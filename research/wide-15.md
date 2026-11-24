# Wide 15: twelve mechanisms from unused fields, scored before any price, the top two gated

Research run wide-15, 2026-11-24. Branch `wide-15` (from `main`), draft PR into `main`.
Research only: fake money, keyless public data, no change to the gym, the daily runner or the
live strategies.

**Count carried in.** wide-13 (`wide-13.md`, "Family count"): **84 mechanisms, 18 tested by a
strategy, none passed; 19 gates, all failed**. weather-2 (`weather-2.md`, branch merged into
`main` via the research archive) posted its gate after wide-13 counted: `cpc-revision` (UNG on
CPC outlook revisions, t -0.68, rank 36 of 41, dead; `tries.md` row of 2026-11-19 03:15). Count
carried into this run: **85 mechanisms, 18 tested by a strategy, none passed; 20 gates, all
failed.** As in wide-12 and wide-13, only mechanisms that get a gate or a strategy test enter
the count; the scored-but-parked ones are listed here and in `ideas.md`, not counted.

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-19 00:30): **3,130 tries,
N 1,032 for a new pick; measured rho 0.53 gives N_eff 486: a new rule needs z >= 4.69, an edge
over `tsmom12` of +0.30 (close rule) to +0.56 (far rule) in annual Sharpe on the primary test,
Bonferroni p <= 1.0e-4.** Family bar for the next strategy test after this run's gates:
p < 0.10 / 87 = 0.00115 (if both gates below are counted).

Method: every gate follows `research/gate-null.md` (placebo family fixed in the rule, 40
placebos, one code path for true and placebo, the rank decides, t >= 2 also required; rule,
script and tests pushed before any number; one dry run that prints counts only, then one real
run). Train only: no bar after 2025-11-10 is loaded; the held-out year is never read. Each gate
gets one `screen` row in `tries.md` (descriptive, not selectable), as weather-1 and wide-13 did.

## Step 1. Fields already used (from wide-1 .. wide-13, weather-1/2, data-wide-1, the surveys, `ideas.md`)

| Source | Fields (tool) |
|---|---|
| run 1, `ideas.md` first tables | Kelly / information theory, regime models (HMM), fractional differentiation, optimal stopping / control, universal portfolios, random-matrix theory / PCA, Hawkes processes, calendar / microstructure, short-term reversal, volatility targeting, trend, machine learning (7 designs), RL and evolution strategies, pretrained time-series models, TDA, transfer entropy, change-point detection, econophysics (LPPLS, Hurst), path signatures, LLM agents |
| macro and carry lanes | monetary policy (Fed hiking, real rate), term structure, money supply / Fed balance sheet (`liquidity`), credit spreads, crypto cycle (halving), futures and funding carry, valuation (CAPE, ECY) |
| wide-1 (46 mechanisms) | ecology (incl. early-warning signals), epidemiology / graph diffusion, signal processing, control theory (incl. Kalman innovation, observers), information theory, evolutionary game theory, statistical physics (Ising, percolation, order parameters), queueing / inventory / reliability (hazard rates), neuroscience, immunology, behavioural ecology |
| wide-2 .. wide-9 (W1-W19) | physics of pinning, hydraulics (reserve drain), astronomy x chronobiology, pharmacokinetics, seismology (tidal triggering), actuarial science, materials fatigue, metrology, dealer queueing, index control (feedforward), demography (cohort flows), anthropology of calendars, tax law (wash-sale), catastrophe meteorology, heliophysics, software release engineering, sport sociology, oceanography (ENSO) |
| wide-10, wide-11 | procurement / reverse auctions (Fed purchases), currency boards / narrow banking (stablecoins), agricultural economics (hedging pressure), securities law (buyback blackout), real-estate finance (mortgage convexity), payments engineering (settlement cycle) |
| wide-12 | international reserve management (custody flows), survey methodology (forecaster dispersion), conflict studies (GPR threats), public debt management (maturity supply) |
| data-wide-1, wide-13 | geopolitics (GPR acts), bank regulation (FDIC failures), FX intervention (MOF), seismology (Japan quakes), nuclear energy outages, epidemiology (FluView), cyber (hacks, KEV), maritime chokepoints, central-bank gold |
| weather-1, weather-2 | meteorology (heating degree days, outlook revisions) |
| surveys 2-7, ann-1, gsy-1 | published finance effects: FOMC cycle, cross-asset trend, announcement premium, time-series carry and value, Halloween, same-month seasonality, bubbles (Greenwood-Shleifer-You), live fund records |
| feature screens (info-1, slow-1, micro-1, multi-signal) | COT positioning (speculators, leveraged funds, asset managers), put/call, VIX term structure, oil 13-week return, dollar, hash-rate growth, transaction growth, Fear & Greed, macro levels |

**Fields picked, not in the table** (searched in `research/` on 2026-11-24 for each field's
words: hydrolog*, hydrograph, refund, congress, roll-call, linguist*, petro*, sovereign wealth,
dissent, PATH Act, Sichuan, curtail; no hit outside unrelated broker notes, and `refund` only as
Treasury *refunding auctions*):

1. **Public / household finance** (tax refunds and transfers to households).
2. **Hydrology** (the unit hydrograph: rainfall turned into river flow through a fixed lag
   kernel; seasonal hydropower). Not the same as wide-4's *hydraulics* (a reservoir drained on
   tax dates).
3. **Legislative studies** (roll-call votes as a count of law-making activity).
4. **Administrative law and computational text** (Federal Register rule counts; text-based
   uncertainty). data-wide-1 inventoried the Federal Register source but no idea used it.
5. **Resource economics** (petro-state fiscal rules).
6. **Power systems / mining engineering** (where and when Bitcoin is mined). The hash rate
   itself is not new: info-1 screened `hash_growth`.
7. **Social choice** (committee voting at the FOMC).
8. Borderline: **securities settlement logistics** (fails to deliver as backorders). Close to
   wide-1's queueing / inventory field; listed, marked as such.

Computational maths brought to each (the cross-pollination): the Nash-cascade unit hydrograph
(a gamma lag kernel) and robust same-week baselines (X1), a difference-in-differences timing
test (X3), a Kalman nowcast (X4), variance-stabilised counts (Anscombe) with an in-session
indicator (X8), peaks over a threshold from flood-frequency analysis (X11).

## Step 2. Twelve mechanisms, scored (2026-11-24 19:40 UTC, before any price was read)

Scoring exactly as wide-13: wide-11's filters F1 (not announced: an unscheduled flow (a), or a
premium (b)) and F2 (not price-driven; passing only with controls costs 1 point), then wide-10's
six points (cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1). Post-sample read
literally as wide-13 did: an idea formed tonight with no literature gets 0. `[memory]` marks a
literature fact not checked tonight.

**Disclosure.** Before this table, two dose sources were probed for format only (no price, no
return, no statistic): the Voteview roll-call file (`HSall_rollcalls.csv`, 30 MB, columns
`congress, chamber, rollnumber, date, ...`) and the Treasury Daily Statement table
`income_tax_refunds_issued` (two days, 2006-03-01 and 2024-03-01, to read the category names).

### The mechanisms (cause story each)

- **X1 `refund-runoff`** (public finance x hydrology). IRS individual refunds land in household
  accounts, mostly February to May (`income_tax_refunds_issued`, daily since 2005-10). A share
  is moved to brokerage and coin accounts over the following days and weeks. Like rain becoming
  river flow, the cash should reach retail-heavy assets through a lag kernel (a Nash cascade:
  gamma, shape 2, mean 2 weeks, fixed here). A week with more refunds than the same week of
  earlier years means more retail cash arriving, so retail-heavy assets (QQQ, IWM, BTC, ETH)
  earn more over the next 4 weeks. Dose: the week's refunds minus the median of the same ISO
  week in the three prior years, scaled by the prior year's refund total.
- **X2 `stimulus-runoff`** (public finance). The three Economic Impact Payment waves (2020-04,
  2021-01, 2021-03) put about USD 800 bn in households' hands; retail buying rose after them
  (Greenwood, Laarman and Thaler on stimulus and retail trading `[memory]`).
- **X3 `path-act-shift`** (public finance x difference-in-differences). The PATH Act (2015)
  holds refunds with the earned-income credit until mid-February from the 2017 season. If
  refund cash moves retail-heavy assets, their seasonal return profile should shift later by
  the same weeks after 2017.
- **X4 `withheld-nowcast`** (public finance x a Kalman observer). Withheld income and payroll
  taxes in the daily statement measure wages in real time, weeks before payroll data. A state
  estimate of wage growth from them should lead bond and stock returns.
- **X5 `petro-recycling`** (resource economics). Oil exporters' budgets depend on oil revenue;
  when oil falls they draw down sovereign funds and reserves, selling foreign stocks and bonds
  without notice. A 13-week oil fall should be followed by weaker SPY, EFA and TLT returns
  (positive slope of next 4-week return on the past 13-week oil return).
- **X6 `hydro-hash`** (hydrology x mining). Before the 2021 ban, Sichuan's wet season moved
  hash rate in and out of China; miners' costs and forced coin sales should follow the season.
- **X7 `curtailment-hash`** (power systems). Texas miners switch off in grid peaks and are paid
  to curtail; fewer blocks and less selling pressure in heat waves.
- **X8 `congress-workload`** (legislative studies x a count process). Roll-call votes measure
  how much law is moving through the floor: taxes, spending, regulation. Holding stocks through
  busy legislative weeks carries policy risk, for which a premium should be paid over the
  following weeks (political-uncertainty premium: Pastor and Veronesi, Journal of Financial
  Economics 2013 `[memory]`). Dose: variance-stabilised count of House and Senate roll calls in
  the week, with an in-session indicator so that only the variation *within* session weeks
  counts (the session calendar itself is public and is the calendar-mean effect of Ferguson and
  Witte, "Congress and the stock market", 2006, sample 1897-2004 `[memory]`: lower returns
  while in session). Predicted sign of the premium: positive.
- **X9 `rule-intensity`** (administrative law x text counts). Weekly count of final rules in the
  Federal Register; heavy rule-making raises regulatory risk for sector equity (XLF, XLV, XLE),
  which should earn a premium afterwards.
- **X10 `news-text-vol`** (computational linguistics). News-implied volatility from front-page
  text (Manela and Moreira, Journal of Financial Economics 2017 `[memory]`): disaster-risk
  premium after high text uncertainty.
- **X11 `settlement-fails`** (settlement logistics x peaks over threshold). Primary dealers'
  fails to deliver Treasuries spike when collateral is scarce; scarce safe collateral carries a
  convenience premium (Treasuries rich), so TLT should earn less in the 4 weeks after a fails
  peak above a flood-frequency threshold.
- **X12 `fomc-dissent`** (social choice). Dissenting votes at an FOMC meeting signal a split
  committee and more uncertain policy; long bonds should earn a larger term premium until the
  next meeting.

### Score

| # | F1 not announced | F2 not price-driven | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| X1 `refund-runoff` | pass (a): daily refunds are published the next business day; the purchases they fund are never public (the filing-season start date is announced in January, so part of the timing is known; the same-week baseline keeps that part in the dose) | pass: IRS processing does not follow asset prices | 0 (the refund is owed by law, investing it is a household choice) | 2 | 0 (formed tonight) | 1 (about 18 seasons x 15 weeks = 270 dosed weeks per ETF) | 1 (no run read the refund lines) | 1 (`tax-drain` was the reverse flow on calendar dates; `payday-inflow` is a scheduled payroll calendar, never tested) | 0 | **5** | 0.3% |
| X2 `stimulus-runoff` | **fail**: amounts set by statute, payment dates announced | - | - | - | - | - | - | - | - | - | filtered (and 3 episodes) |
| X3 `path-act-shift` | **fail**: a timing shift set by a public law; no dose (wide-10's C6 `settlement-shift` class) | pass | - | - | - | - | - | - | - | - | filtered |
| X4 `withheld-nowcast` | **fail**: public data read as news; neither an unscheduled flow nor a premium | pass | - | - | - | - | - | - | - | - | filtered |
| X5 `petro-recycling` | pass (a): sovereign drawdowns are not announced | with controls: oil and stocks move together in demand shocks | 0 | 2 | 1 (Driesprong, Jacobsen and Maat, Journal of Financial Economics 2008, oil predicting stocks, sample to 2003 `[memory]`) | 1 | **0**: info-1 and slow-1 screened `oil_13w` on 1-, 4- and 13-week returns (IC -0.008, -0.005, -0.045) | **0**: the `oil` rule (yt-1) died | -1 | 3 | 0.5% |
| X6 `hydro-hash` | pass (a) | with controls: hash rate follows price over months | 0 | **0**: difficulty adjustment holds issuance near 144 blocks a day within two weeks, so a seasonal hash-rate swing barely changes the coins miners must sell | 0 | 0 (about six wet seasons before 2021) | 0 (`hash_growth`, info-1) | 1 | -1 | 0 | - |
| X7 `curtailment-hash` | pass (a) | with controls: miners also curtail when the coin price is low | 0 | 0 (same issuance argument) | 0 (2021 on) | 0 | 1 | 1 | -1 | 1 | - |
| X8 `congress-workload` | pass (b): a premium | with controls: Congress votes more in crises (2008 rescue, 2020 relief), i.e. after market falls; controls for SPY's past 4/13/26/52-week returns | 0 | 2 | 1 (Ferguson-Witte to 2004, Pastor-Veronesi to about 2010 `[memory]`: 15 train years after) | 1 (about 1,100 session weeks 1994-2025) | 1 | 1 (not a calendar mean: the in-session indicator absorbs the calendar; only the within-session dose is tested) | -1 | **5** | 1% |
| X9 `rule-intensity` | pass (b) | with controls: rule waves follow crises at multi-year lags (2010-14 bank rules) | 0 | 2 | 0 (regulatory-intensity literature to about 2018 `[memory]`: under 8 years) | 1 | 1 | 1 | -1 | 4 | 0.5% |
| X10 `news-text-vol` | pass (b) | **fail**: the index is a text regression fitted to VIX, a transform of option prices | - | - | - | - | - | - | - | - | filtered |
| X11 `settlement-fails` | pass (b): a convenience premium | with controls: fails surge in flights to quality, when TLT rallies | 0 | 2 | 1 (fails studies of Fleming and Garbade to about 2004 `[memory]`) | 1 (weekly since 1990) | 1 | 1 | -1 | **5** | 0.5% |
| X12 `fomc-dissent` | pass (b) | with controls: dissents rise with inflation, i.e. while bonds fall | 0 | 2 | 0 | 0 (about 255 meetings 1994-2025) | 1 | 1 | -1 | 3 | 0.5% |

**Size check behind the priors (written now, before any number).** X1 is a flow story, so its
prior rests on the flow's size. Refunds run about USD 250-300 bn a season `[memory]`; a weekly
surprise of USD 10 bn with 2% reaching retail-heavy assets is USD 200 m. With a price multiplier
of about 5 per unit of flow over market value (Gabaix and Koijen's inelastic-markets estimate
`[memory]`), USD 200 m moves a USD 1 tn coin market about 0.1% and a USD 20 tn tech index about
0.005%, against 4-week standard deviations of about 20% and 6%: an expected t near 0.1. X1 is
gated because the rule ranks it, not because it is likely; prior 0.3%. X8 is a premium, so no
flow-size check applies; its prior of 1% reflects a sign the literature does not settle (the
calendar finding is *lower* returns while Congress sits, the premium theory says *higher*
returns after policy risk).

**Picked by the rule.** Three candidates score 5: X1, X8, X11. Tie-break (wide-10): fewest data
fetches, then the higher prior. X8 needs one static CSV (already fetched for the format probe);
X1 one keyless endpoint, a few pages; X11 several primary-dealer files with format breaks.
**Gated: X8 as W27 `congress-workload`, then X1 as W28 `refund-runoff`.** X11 and X9 stay parked
(not counted). X2-X4, X6, X7, X10 are filtered or score under 3.

## Step 3. W27 `congress-workload` gate (rule fixed and pushed before any number)

**Data.** Voteview's roll-call file `HSall_rollcalls.csv` (keyless static file, every recorded
roll call of the House and Senate with its date; fetched 2026-11-24 into the shared cache
`wide-15/voteview/2026-11-24/`, read as untrusted data with `python -I`). Roll calls dated after
2025-11-10 are never read. One row is one roll call; `chamber` is House or Senate.

**Dose.** Weeks run Saturday F - 6 .. Friday F. n(F) = number of roll calls in both chambers
dated in the week. x(F) = 2 sqrt(n(F) + 3/8) (Anscombe's variance-stabilising transform of a
count); s(F) = 1 if n(F) > 0 (in session), else 0. The regression carries both, so b, the slope
on x, is identified only by the variation **within** session weeks; the calendar effect of
sitting or not (Ferguson and Witte) sits in s's coefficient and is shown, not gated. Predicted
sign of b: positive (policy-risk premium).

**Available on (no look-ahead).** Roll calls are public the day they are taken (clerks' tallies).
Entry at the close of SPY's first bar dated >= F + 3 (the Monday after the week; a Friday vote
after the close is then public), exit at the close of the first bar dated >= F + 31. y(F) =
ln(exit / entry), dividend-adjusted closes (`harness.load_history("train")`, adjusted where the
cache has it). The row is dropped if either bar is missing, the exit bar is dated after F + 38,
or after 2025-11-10.

**Controls (F2), every horizon up to a year.** r_h(F) = ln(close of SPY's last bar <= F / close
of the last bar <= F - h days), h = 28, 91, 182, 364 (Congress legislates in crises, which follow
market falls).

**Statistic.** One asset, OLS y = a + b x + c s + g4 r4 + g13 r13 + g26 r26 + g52 r52; t of b
with Newey-West (Bartlett) 4 lags over the week index (the Driscoll-Kraay function of wide-11/13
with one row a week: same code path for every cell).

**Placebo null (the decider).** The dose can answer prices (crisis legislation), so by
`gate-null.md` step 1 only **earlier** doses are used: (x_k, s_k)(F) = (x, s)(F - 7k days), the
outcome and controls stay put, k in {27, 29, 31, ..., 105} (every odd week: **40 placebos**,
never a whole year). Every placebo dose ends at least 26 weeks before its outcome starts.

**Gate. Pass only if both hold** (Fridays 1994-02-04 .. 2025-10-03; SPY from 1993-01, its
52-week control from 1994-01):
1. b > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41 (empirical one-sided p = rank / 41 <= 0.049).

**Kill-only (gate-null step 7).** The smallest p this design can show is 1/41 = 0.024, above
the family bar (0.00115) and the register's (1.0e-4). About 64 sessions in 32 years. A fail
kills the idea; a pass only says "not dead yet".

**Shown, not gating:** without the controls; QQQ and IWM instead of SPY; close votes only (roll
calls with |yea - nay| / (yea + nay) < 0.10) as n; House only; Senate only; the years after
Pastor-Veronesi, Fridays 2011-01-07 .. 2025-10-03; the 1-week horizon (exit at the first bar
>= F + 10, 1 lag); the calendar cell (c, the in-session coefficient, from the gate fit); the F2
feedback check (x on SPY's past 4/13/26/52-week return alone, session weeks only, NW 4 lags);
the placebo null's width.

**Power, written before any number.** SPY's 4-week sd is about 4.5%. About 1,100 session weeks,
overlapping by 3 weeks (about 275 effective); if x's sd within session weeks is about 3 units,
the standard error of b is about 4.5% / (3 x sqrt(275)), near 0.09% per unit. A premium of
0.2% per unit (about 0.6% per 4 weeks per sd of workload, 7% a year) is needed for t 2: only a
large premium passes.

**My guess before any number.** b near zero, t between -1.5 and +1.5, rank in the middle;
placebo t sd 1.0-1.4. The calendar cell c negative (Ferguson-Witte) but |t| < 2 after 2004.
Feedback weak. Chance of a pass: 1%.

**On a pass:** no card in this run; "not dead yet", a new design with more independent episodes
(other countries' parliaments) would be needed. **On a fail:** dead, one `screen` row.

## Step 4. W28 `refund-runoff` gate (rule fixed and pushed before any number)

**Data.** Treasury Daily Statement table `income_tax_refunds_issued`
(`api.fiscaldata.treasury.gov`, keyless, daily from 2005-10-03; fetched 2026-11-24 into the
shared cache `wide-15/dts-refunds/2026-11-24/`, rows dated after 2025-11-10 never read). Daily
individual refunds D(day) = sum of `tax_refund_today_amt` (millions of USD) over the rows whose
type names individual refunds (checks and EFT; one combined "Individual" row before the format
change, two rows after).

**Dose.** Weeks run Saturday F - 6 .. Friday F. R(F) = sum of D over the week. Baseline B(F) =
median of R at the same ISO week number in the three previous ISO years (at least two present;
ISO week 53 has no baseline). T(y) = sum of D over calendar year y. Surprise d(F) = 100 (R(F) -
B(F)) / T(year(F) - 1), in percent of last year's refunds (NaN without a full prior year).
Runoff (the hydrology): a Nash cascade unit hydrograph h(tau) = tau exp(-tau), tau in weeks
(gamma, shape 2, mean 2 weeks), carries refund cash into retail purchases. The share of week
F - i's refunds that the kernel delivers inside the outcome window (days F + 5 .. F + 33 =
weeks i + 5/7 .. i + 33/7 after that week) is w_i = integral of h over that span; the dose is
u(F) = sum over i = 0..7 of w_i d(F - 7i) (NaN if any term is missing). Predicted sign: positive.

**Available on (no look-ahead).** The statement for a day is published at 4 pm Eastern the next
business day, so Friday's figure is public on Monday afternoon (Tuesday after a Monday holiday).
Entry at the close of the asset's first bar dated >= F + 5 (Wednesday), exit at the close of the
first bar dated >= F + 33. y(F) = ln(exit / entry), dividend-adjusted where cached. Row dropped
if a bar is missing, the exit bar is dated after F + 40, or after 2025-11-10.

**Panel and statistic.** Gate assets QQQ, IWM, BTC, ETH (the retail-heavy ones in the cache;
coins from their first cached day). Pooled OLS y = a_asset + b u, no controls (F2 passes
outright). t of b with Driscoll-Kraay standard errors (scores summed per Friday, Newey-West 4
lags over the week index).

**Placebo null (the decider).** IRS processing does not answer asset prices, so shifts both ways
are allowed (`gate-null.md` step 1): u_k(F) = u(F - 7k days), k in +-{27, 31, ..., 103} (odd,
step 4, the wide-11/12/13 family): **40 placebos**, rows with a missing u_k dropped from that
placebo only.

**Gate. Pass only if both hold** (Fridays 2008-01-04 .. 2025-10-03):
1. b > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41.

**Kill-only.** About 18 refund seasons; smallest p 1/41 = 0.024 > 0.00115.

**Shown, not gating:** SPY alone; QQQ and IWM alone; BTC and ETH alone; the raw weekly surprise
d(F) instead of the runoff u(F); seasons from 2017 (after the PATH Act hold); with each asset's
past 4/13/26/52-week returns as controls; the 1-week horizon (exit at the first bar >= F + 12,
1 lag); the F2 feedback check (u on each asset's past return, pooled, DK 4 lags); the null's
width.

**Power, written before any number.** Step 2's size check: an expected t near 0.1 if 2% of the
surprise reaches these assets. Only a flow share far above what the household-finance
literature reports could pass.

**My guess before any number.** b of either sign, |t| < 1.5, middle rank, placebo t sd 1.0-1.3
(the dose is seasonal and the kernel smooths it, so neighbouring weeks are correlated). Chance
of a pass: 0.3%.

**On a pass:** "not dead yet" only; a design with more seasons or other countries' refunds
would be needed. **On a fail:** dead, one `screen` row.

## What came out (one dry run, then one real run, 2026-11-24)

**Dry run first** (`DRY=1`, counts only): Voteview 112,878 roll calls read (none after
2025-11-10); 1,653 gate Fridays, 1,151 of them in session; 1,653 SPY rows with outcome and all
four controls (QQQ 1,335, IWM 1,272); every one of the 40 earlier-dose placebos keeps all 1,653
dose weeks. Daily statement: 5,051 refund days 2005-10-03 .. 2025-11-10, full-year totals for
2006-2024; 942 surprise weeks, 914 runoff weeks; 903 of the 927 gate Fridays have a dose (the 24
missing are the eight Fridays after each ISO week 53 of 2009, 2015 and 2020, which has no
baseline); rows with outcome and dose: QQQ 903, IWM 903, BTC 707, ETH 486, SPY 903; placebos keep
805 to 882 dose weeks. Refund rows matched: "IRS Tax Refunds Individual" (2005-2019 format),
"Individual" (to 2022) and "Taxes - Individual Tax Refunds (Checks / EFT)" (from 2023); Economic
Impact Payments and advance child tax credits are separate rows and are **not** counted (X2 is
filtered). Then one real run each, as carded. Tables: `results/congress-workload.md`,
`results/refund-runoff.md`.

### W27 `congress-workload`: fails

**One more unit of Anscombe-transformed roll calls in a session week goes with -0.009% on SPY
over the next 4 weeks, with SPY's past 4/13/26/52-week returns as controls (t -0.19, 1,653
weeks, 1994-02 .. 2025-10): the wrong sign; the true t ranks 25 of 41 (empirical one-sided p
0.61). Dead by the gate: no card, no strategy.** Held-out year untouched.

| Cut (SPY 4-week return unless named) | b, % per unit of x | t | Rows |
|---|---:|---:|---:|
| **Gate: x with session dummy, four controls** | **-0.009** | **-0.19** | 1,653 |
| Without the controls | -0.012 | -0.24 | 1,653 |
| QQQ / IWM instead | +0.059 / -0.058 | +0.74 / -0.81 | 1,335 / 1,272 |
| Close votes only (margin < 10%) | -0.033 | -0.44 | 1,653 |
| House only / Senate only | -0.062 / +0.092 | -0.87 / +1.21 | 1,653 |
| After Pastor-Veronesi, 2011-01 .. 2025-10 | -0.071 | -1.07 | 770 |
| 1-week horizon | +0.013 | +0.55 | 1,653 |
| Calendar cell: in-session dummy c, % per 4 weeks | +0.337 | +0.69 | 1,653 |

- **No policy-risk premium after busy legislative weeks**, in either chamber, for close votes
  or after the premium paper's sample. The workload premium a pass needed (about 0.2% per unit)
  is ruled out at about two standard errors: the estimate is -0.01 with a standard error near
  0.05.
- **Ferguson and Witte's calendar effect does not show forward either**: the in-session dummy
  is +0.34% per 4 weeks (t +0.69), the opposite sign to their "lower returns while Congress
  sits" (their finding is contemporaneous and to 2004; this cell is the next 4 weeks from 1994,
  so it is not a replication, only a look).
- **F2 feedback is weak**: workload on SPY's past returns, t +0.16 to +1.01 at 4-52 weeks (crisis
  legislation is real but rare enough not to show in weekly counts).
- **Null width: SD of placebo t 1.08, 5% with |t| >= 2**, quantiles 5/50/95% -1.48 / +0.03 /
  +1.98, extremes -1.67 / +2.68 (k = 81). Earlier-dose placebos only, as the card fixed; a
  near-normal null, as for an unclustered weekly dose.
- My guess (t -1.5 to +1.5, middle rank, placebo sd 1.0-1.4, calendar cell negative, feedback
  weak, pass 1%) held on t, rank, width and feedback; the calendar cell came out positive.

### W28 `refund-runoff`: fails

**One unit of refund runoff (about one percent of last year's refunds arriving in the window
beyond the usual) goes with +0.281% on QQQ, IWM, BTC and ETH over the next 4 weeks (t +1.44,
2,999 rows, 2008-01 .. 2025-10): the predicted sign, but t below 2 and the true t ranks 7 of 41
(empirical one-sided p 0.17). Dead by the gate: no card, no strategy.** Held-out year untouched.

| Cut (4-week return, QQQ+IWM+BTC+ETH unless named) | b, % per unit of u | t | Rows |
|---|---:|---:|---:|
| **Gate: runoff u, no controls** | **+0.281** | **+1.44** | 2,999 |
| SPY alone | +0.182 | +1.58 | 903 |
| QQQ and IWM | +0.309 | +2.67 | 1,806 |
| BTC and ETH | +0.247 | +0.72 | 1,193 |
| Raw weekly surprise d instead of u | +0.208 | +1.25 | 3,062 |
| Seasons from 2017 (PATH Act hold) | +0.403 | +2.05 | 1,796 |
| With past 4/13/26/52-week returns | +0.318 | +1.64 | 2,886 |
| 1-week horizon | +0.051 | +0.46 | 2,993 |

- **The null is wide, so a t of 1.44 is ordinary: SD of placebo t 1.92, 32% with |t| >= 2**,
  quantiles 5/50/95% -3.51 / -0.67 / +2.80, extremes -4.61 / +3.47. Six placebos beat the true
  t (k = +27: +3.47, -59: +3.45, -51: +2.76, -55: +1.79, +31: +1.73, +63: +1.46), three earlier
  doses and three later, so the width is not the one-sided lean of review-2's point (1)
  (earlier-dose mean -0.44, sd 1.73; later-dose mean -0.77, sd 2.12). The width comes from the
  design: a dose that is large only in about 15 weeks a year, in a panel of four assets that
  move together, has about 18 seasons of independent information. Shifted refund seasons land
  on other months' common moves and "predict" them as well as the true one.
- **The shown cells with t above 2 are noted only, not a lead** (`gate-null.md` step 6): QQQ
  and IWM together (+2.67) and the post-2017 seasons (+2.05) are 2 of 7 shown cells in a design
  whose placebo SD is 1.92; both sit inside the placebo range (95% quantile +2.80, largest
  +3.47). Coins, where the retail story is strongest, show the weakest cell (t +0.72).
- **The size check of step 2 still stands**: a slope of 0.28% per percent of last year's refunds
  would mean that USD 2-3 bn of surprise refund cash moves four markets worth trillions by a
  quarter of a percent, a price multiplier hundreds of times the inelastic-markets estimate. An
  effect of that size is more likely a seasonal coincidence of the refund calendar with returns
  than a flow, which is what the placebo null says.
- **F2 holds**: the runoff dose does not follow past returns (t -1.20 to +1.08).
- My guess (either sign, |t| < 1.5, middle rank, placebo sd 1.0-1.3, pass 0.3%) held on t; the
  rank (7) was better than the middle and the null was much wider than guessed (1.92, not
  1.0-1.3): the seasonal concentration of the dose matters more than the kernel's smoothing.

Labels: both gates are **kill-only** by `gate-null.md` step 7 (smallest p 1/41 = 0.024 above the
family bar 0.00115 and the register's 1.0e-4); W28 also by its episode count (about 18 seasons).
Both are kills.

## Family count and status

Two mechanisms added and closed by their gates (W27 `congress-workload`, W28 `refund-runoff`; W
numbers follow wide-13's W26; weather-1 and weather-2 had none). The ten others (X2-X7, X9-X12)
are parked or filtered and are **not counted**, as wide-12 and wide-13 did.

**Count: 87 mechanisms (85 carried in + W27 + W28), 18 tested by a strategy, none passed; 22
gates, all failed.** The next strategy test is read at **p < 0.10 / 87 = 0.00115** (family) and
the register's bar (N_eff 486: z >= 4.69, +0.30 to +0.56 Sharpe over `tsmom12`, Bonferroni p <=
1.0e-4). Published effects after publication: still 0 for 10 (neither gate tested a published
claim as stated: W27's dose is not Ferguson-Witte's session calendar and its forward premium cut
is not Pastor-Veronesi's test; W28 has no literature).

Rows logged in `tries.md`: 2 (`congress-workload`, `refund-runoff`, kind `screen`).

## Next

1. **Parked, scored 5 and 4: X11 `settlement-fails`, X9 `rule-intensity`.** X11 needs the NY Fed
   primary-dealer fails files (several formats); X9 the Federal Register API's weekly counts. Both
   are premia with slow price feedback (controls needed). Neither is more likely than the 22 that
   died; a lane that runs them should expect a kill.
2. **Seasonal doses give wide nulls.** W28's placebo SD (1.92) is the widest of a design with an
   exogenous dose so far: a dose concentrated in one season of the year, read in a panel of
   correlated assets, has about one independent draw per season. A future card with a seasonal
   dose should say so before any number and plan for kill-only (as W28's did).
3. **The flow-size check belongs in the score.** Every flow story that died (W15, W20, W21, W23,
   W26, W28) moved a sum far below what a detectable price move needs at any published price
   multiplier. A lane that wants to change the rule could add a sixth filter, "flow at least
   0.1% of the asset's market value per window", fixed before scoring; this run did not change
   the rule.
