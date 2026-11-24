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
