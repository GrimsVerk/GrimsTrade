# Wide 10: two mechanisms from unused fields, picked by a written score, gated

Research run wide-10, 2026-11-19. Branch `wide-10` (from `survey-7`), draft PR into `survey-7`.
Research only: fake money, public keyless data, no change to the gym, the daily runner or the
live strategies.

**Count carried in (survey-7):** the union of the wide and survey lines, **76 mechanisms, 18
tested by a strategy, none passed**; 11 gates, all failed. Project-wide
(`git show origin/register-1:research/register/BAR.md`, read 2026-11-19): **2,904 tries, N 1,012
for a new pick, Bonferroni p <= 4.9e-5.** With the two entries below the family is **78**, so a
later strategy test is read at **p < 0.10 / 78 = 0.00128**.

Method: every gate follows `research/gate-null.md` (placebo family fixed in the rule, 40
placebos, the same code path for true and placebo, the rank decides, t >= 2 also required; rule,
script and tests pushed before any number; one dry run that prints counts only, then one real
run). A gate is descriptive: no `tries.md` row, no card, and it does not raise the tested count.

Lesson carried in from the night: published calendar effects and forced-flow stories all died.
So this run favours mechanisms with a structural cause and a dose that is measured event by
event (a dose-response slope is a much harder test than a calendar mean), judged on years after
the source literature's samples.

## Step 1. Candidates and a scoring rule (written 2026-11-19, before any data look)

### Fields already in the list (so excluded)

From `wide-1.md` and its additions: ecology, epidemiology, signal processing, control,
information theory, evolutionary game theory, statistical physics, queueing/inventory and
reliability, neuroscience, immunology (wide-1); physics of pinning, hydraulics, astronomy and
chronobiology (W1-W3); pharmacokinetics, seismology, actuarial science, materials fatigue,
metrology (W4-W8); queueing of dealers and index control (W9, W10); demography, anthropology of
calendars, tax law, catastrophe meteorology (W12-W15); heliophysics, software release
engineering (W16, W17); sport sociology, oceanography (W18, W19). The finance-literature entries
of survey-4 (`ts-carry`, `halloween`, `seasonal-20y`, `ts-value`) and `ideas.md`'s macro
families (`fed-hiking`, `liquidity`: monthly regimes of policy rate, M2 and the Fed's balance
sheet) are also taken.

### Six candidates from fields not in the list

| # | Field x tool | Mechanism | Dose that should scale | Data (keyless) |
|---|---|---|---|---|
| C1 `fed-purchase-flow` | procurement (reverse-auction) theory: a buyer with a published shopping list | On days the Fed buys Treasuries in an operation (QE, Operation Twist, reinvestment), dealers sell it the purchased sector; the sector's price rises that day ("flow effect"). The monthly schedule (dates, maturity buckets, size ranges) is published ahead | Par accepted in bonds of 20+ years remaining maturity (TLT's sector) on the day | NY Fed Markets API, Treasury operations with per-CUSIP results, 2009 on (one endpoint) |
| C2 `stablecoin-mint` | monetary history of currency boards / narrow banks: money issued only against a deposit, 1:1 | A stablecoin is minted only when someone wires dollars to the issuer, so net issuance is fresh cash on its way to buy coins; it should lift coin prices over the following week | Weekly log change of total USD stablecoin supply | DefiLlama stablecoin totals (one endpoint) |
| C3 `hedging-pressure` | agricultural economics: Keynes-Hicks normal backwardation | Producers hedge by selling futures and pay speculators a premium; the larger the hedgers' net short, the higher the expected futures return | Commercials' net short / open interest (CFTC Commitments of Traders), weekly | CFTC yearly zip files (about 30 files) |
| C4 `buyback-blackout` | securities law: Rule 10b-18 safe harbour and insider blackout windows | Companies stop buying back their stock in the weeks before earnings; index returns are lower in blackout weeks than in open-window weeks | Yearly buyback total (zero before Rule 10b-18, 1982) | Prices cached; yearly buybacks from a spreadsheet |
| C5 `mortgage-convexity` | real-estate finance: the prepayment option | When few mortgages can refinance, MBS duration is long and the bond term premium rises; bonds earn more over the next months | Mortgage rate minus its trailing 5-year mean | FRED mortgage rate (one file) |
| C6 `settlement-shift` | payments engineering: the settlement cycle T+n | If the turn-of-month effect is month-end cash settling into stocks, its peak must move by exactly the legal change of the settlement lag (T+5, T+3 1995, T+2 2017, T+1 2024) | The lag in days (a timing shift, not a size) | Prices cached |

### Scoring rule (fixed before any number)

Each candidate gets:

1. **Structural cause** (1 point): the flow or constraint is fixed by a law, regulation, contract,
   index rule or obligation, not by a habit, mood or business choice.
2. **Dose** (2 points): the event's size varies, is public at (or announced before) the
   decision, and the mechanism says the effect scales with it. A timing shift is not a dose.
3. **Post-sample** (1 point): at least 8 train years after the latest sample end of the source
   literature, or after the idea was first formed if it has no literature.
4. **Power** (1 point): at least 200 dosed events, or at least 300 non-overlapping
   observations, in the judging years.
5. **Unseen cut** (1 point): no run in this repo has computed the deciding statistic.
6. **Not killed in other words** (1 point): not a killed idea renamed, and not a plain calendar
   mean (the class that died tonight).

Filter: the field is not in the list and the data are keyless. The two highest scores are
picked; ties go to the candidate with the fewest data fetches (cached, then one keyless
endpoint, then several files), then to the higher prior.

| # | 1 cause | 2 dose | 3 post-sample | 4 power | 5 unseen | 6 not killed | Score | Prior |
|---|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| C1 `fed-purchase-flow` | 1 | 2 | 1 (2014-2025; see below) | 1 (to be checked by the dry run) | 1 | 1 | **7** | 3% |
| C2 `stablecoin-mint` | 1 | 2 | 0 (2018-04 .. 2025-11 is 7.6 years) | 1 (about 395 weeks) | 1 | 1 | **6** | 2% |
| C3 `hedging-pressure` | 0 (hedging is a business choice) | 2 | 1 | 1 | 1 | 1 | 6 | 2% |
| C4 `buyback-blackout` | 1 | 2 | 1 | 0 (about 32 quarters) | 1 | 0 (a quarterly calendar) | 5 | 1% |
| C5 `mortgage-convexity` | 1 | 2 | 1 | 0 (monthly, overlapping, few rate cycles) | 1 | 0 (long-horizon bond reversal: the `ts-value` / yield-level family) | 5 | 1% |
| C6 `settlement-shift` | 1 | 0 | 1 | 1 | 1 | 0 (the turn of month, `month-end-liquidity`, faded) | 4 | 1% |

Source samples (checked on the web 2026-11-19 unless marked):
- C1: D'Amico and King, "Flow and stock effects of large-scale treasury purchases: Evidence on
  the importance of local supply", Journal of Financial Economics 108(2), 2013, pp. 425-448:
  the 2009 purchase programme; flow effect about 3.5 bps lower yield in the purchased sector on
  purchase days. Song and Zhu, "QE auctions of Treasury bonds", Journal of Financial Economics
  128(1), 2018, pp. 103-124: operations November 2010 .. September 2011. Kandrac and Schlusche,
  "Flow effects of large-scale asset purchases", Economics Letters 121(2), 2013, pp. 330-335:
  four programmes over about four years (2009 to about 2012-13; exact end `[search summary]`,
  not read), flow effects "of little economic significance" after the early programmes. Latest
  sample end taken as 2013-12, so **judging years = 2014-01 .. 2025-11** (12 train years); the
  Fed bought Treasuries in operations in 2014 (QE3 taper, to October), 2019-08 .. 2020-02
  (reinvestment and bill purchases) and 2020-03 .. 2022-03 (QE and taper).
- C2: Griffin and Shams, "Is Bitcoin Really Untethered?", Journal of Finance 75(4), 2020,
  pp. 1913-1964: Tether flows March 2017 .. March 2018.
- C3: Basu and Miffre (2013), hedging pressure in commodity futures, sample to about 2011
  `[memory]`. C4: the buyback-blackout story spread in sell-side notes around 2017-18
  `[memory]`. C5: Hanson, "Mortgage convexity", Journal of Financial Economics 2014, sample to
  about 2011 `[memory]`. C6: Ogden (1990), turn of the month and the payment system `[memory]`.

**Picked: C1 `fed-purchase-flow` (7) and C2 `stablecoin-mint` (6; tied with C3, which needs about
30 file fetches against C2's one).** They enter the list as **W20** and **W21**. If the dry run
shows fewer than 200 dosed days for C1 in the judging years its score drops to 6; it would still
lead C2 on the prior, so the order holds either way.

Overlaps, stated so nobody counts them as unseen twice: `liquidity` (dead) used the Fed's
balance sheet as a monthly regime (shrinking or not); C1's statistic is the same-day price of
the purchased sector against the day's purchase size, which no run has computed. E1
`stablecoin-resource` (parked, never computed) used stablecoin supply as a level in a
predator-prey fit; C2 is a weekly flow dose.

Disclosure: before this table was written, the NY Fed endpoint was probed for format and
history (two small files: one quarter of 2011 operations and the list of 1999-2009 operations,
fields only). No price was cut by anything here.
