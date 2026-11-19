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

## Step 2. W20 `fed-purchase-flow` gate

### Data access (checked 2026-11-19, before any price was cut by it)

The New York Fed's Markets Data API publishes every Treasury operation with per-CUSIP results
without a key or account: `https://markets.newyorkfed.org/api/tsy/all/results/details/search.json?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD`.
Fields used: `operationDate`, `operationType`, `operationDirection` (`P` purchase, `S` sale),
`auctionStatus`, and per security `securityDescription` (e.g. `T 08.125 05/15/21`: coupon and
maturity) and `parAmountAccepted` (dollars). The script fetches one file per calendar quarter,
2009-Q1 .. 2025-Q4 (end date capped at 2025-11-10), into `research/data/nyfed/` (gitignored),
and reads them as JSON data only.

### Decision rule (fixed and pushed before any number)

**Operations.** Keep operations with `operationDirection` = `P`, `auctionStatus` = `Results`
and an `operationType` that contains `Coupon Purchase` (case-insensitive): nominal coupon
securities bought outright. Out: TIPS, bills, agency debt, sales, and anything else (the dry run
prints the count of every type, kept or not).

**Dose.** For each kept security, maturity = the last token of `securityDescription` (mm/dd/yy;
yy < 70 means 20yy). Long if maturity >= operation date + 20 years (the same day and month, 20
years later; 29 February -> 28 February), TLT's sector (the ICE 20+ year index). L(d) = the sum
of `parAmountAccepted` of long securities over all kept operations dated d, in $bn. **x(d) =
ln(1 + L(d))**, so a day without a long purchase has x = 0 and the very large days of March
2020 do not decide the slope alone.

**Outcome.** y(d) = ln(close / open) of TLT on day d (same-day ratio of the cached daily bar; a
book could buy at the open because the purchase schedule, with dates, maturity buckets and size
ranges, is published before the month or fortnight starts; operations run about 10:15-11:00 New
York time). The actual accepted par stands in for the announced size range: a gate, not a fill
model.

**Statistic.** OLS y = a + b x over every TLT trading day of the sample (days with and without
purchases), t of b with White (HC1) standard errors.

**Placebo null (the decider), one family, fixed here.** The same function with the dose
calendar moved along TLT's trading-day index: x_k(day i) = x(day i - k) for
k in +-{3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 26, 27}: **40
placebos**. Shifts of 1-2 days are left out (the days next to a purchase may carry its effect);
multiples of 5 are left out (they keep the weekday, and buckets may sit on fixed weekdays). Every
shift stays inside the same purchase programme, so the placebo keeps the programme's drift and
volatility and asks only whether the purchase day itself is special. The dose series runs on all
TLT days from 2002-07, so every shifted day has a value.

**Gate. Pass only if both hold** (gate sample: TLT days 2014-01-02 .. 2025-11-10, after every
cited sample):
1. b > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41 (true plus 40 placebos); empirical one-sided p =
   rank / 41 <= 0.049.

**Shown, not gating** (b, t, days): the papers' years 2009-03-01 .. 2013-12-31; the gate sample
with an indicator dose (1 if L > 0); the gate sample without 2020-03-01 .. 2020-04-30 (the
dash for cash); IEF with its own sector's dose (maturity 7 to 10 years after the operation
date, both ends included); SPY open-to-close on ln(1 + all coupon par bought that day); TLT
close-to-close (previous close to close of d) on x; TLT on the next day's open-to-close on
today's x (persistence or reversal); the number of dosed days and the mean L on them; the
placebo t's standard deviation, share with |t| >= 2, 5/50/95% quantiles and extremes
(gate-null step 5).

**On a pass:** no card and no trading test in this run. A *proposed* card (idle cash into TLT
on announced long-bucket purchase days, open to close is not the book's clock, so it would
need a next-open-to-next-open version) for the next window only, read at the family bar
p < 0.00128 and the register's p <= 4.9e-5, with z = (t - placebo median) / placebo sd. And the
mechanism can only trade in a future purchase programme (none runs after 2022-03 in train).
**On a fail:** W20 dead by the gate, no card, no row.

**Power, written before any number.** TLT's open-to-close sd is about 0.8% a day. If about 7% of
about 2,980 gate days carry a long purchase with x near 1.2 (L about $2-3bn), the sd of x is
about 0.3 and the standard error of b about 0.8% / (sqrt(2980) x 0.3), roughly 0.05% per unit
of x. D'Amico and King's 3.5 bps lower yield in the purchased sector is about 0.6% of price at
TLT's duration (about 17): t far above 2 if it held in full. Kandrac and Schlusche's "little
economic significance" after the early programmes would give t below 1.

**My guess before any number.** b > 0 with t between 0 and 2, rank in the top third; placebo t
sd 1.0-1.3 (daily, nearly independent days). Chance of a pass: 8%.

### What came out (one run, 2026-11-19; table `results/fed-purchase-flow.md`)

Dry run first (`DRY=1`, counts only): 1,320 kept coupon purchases out of 1,756 operations
(the rest: TIPS 195, agency 63, bills 57, FRN 10, and 111 sales, chiefly Operation Twist's sales
of short coupons, all left out by the rule); 473 days with a 20+ year purchase, every one a TLT
trading day; **224 dosed days in the gate sample** (2,983 TLT days) and 221 in the papers'
years (1,219 days); 40 placebos, each with at least 2,956 days. So the power point of the score
holds (C1 keeps 7). Then one real run.

**The gate fails on both counts. TLT open-to-close rises +3.3 bps per unit of log dose (t
+0.37, 2,983 days, 224 with a long purchase of $2.1bn on average); the true t ranks 11 of 41
(empirical one-sided p 0.27). W20 `fed-purchase-flow` is dead by the gate: no card, no
strategy, no `tries.md` row.** Held-out year untouched.

| TLT (or other fund) on the day's purchase dose | Slope, bps per unit of ln(1 + $bn) | t | Days |
|---|---:|---:|---:|
| **Gate: TLT open-to-close, 2014-01 .. 2025-11** | **+3.3** | **+0.37** | 2,983 |
| Indicator dose (any 20+ year purchase), gate sample | +2.8 | +0.46 | 2,983 |
| Without March-April 2020 | +1.3 | +0.30 | 2,940 |
| Close-to-close of the purchase day | +10.7 | +0.91 | 2,983 |
| Next day's open-to-close (persistence) | +4.5 | +0.51 | 2,983 |
| Papers' years 2009-03 .. 2013-12 | **-8.5** | **-1.55** | 1,219 |
| IEF on its 7-10 year dose, gate / papers' years | +1.0 / +0.4 | +0.44 / +0.22 | 2,983 / 1,219 |
| SPY on all coupon par bought, gate / papers' years | +0.4 / -0.5 | +0.10 / -0.15 | 2,983 / 1,219 |

- **No flow effect at the fund level, even in the papers' own years.** In 2009-2013, when
  D'Amico and King and Song and Zhu measured purchase-day price gains in the bought CUSIPs, TLT
  fell slightly on long-purchase days (t -1.55). Their flow effect is a cross-sectional one
  (bought bonds against unbought ones, on a day); a sector fund holds both, and the schedule is
  public, so the sector's level prices the purchases in advance. Kandrac and Schlusche's "little
  economic significance" fits the fund-level reading.
- Nothing in the cuts: indicator dose, without the dash for cash, close-to-close, next-day
  persistence, the 7-10 year sector in IEF, and stocks on the total purchase all sit at |t| < 1.
- **Null width: SD of placebo t 0.99, 2% with |t| >= 2**, quantiles 5/50/95% -1.67 / -0.62 /
  +1.06, extremes -2.27 / +1.57. Daily, nearly independent days: the normal null is about right
  (the independent kind in `gate-null.md`'s table). The placebo median sits below zero: TLT's
  open-to-close drift in purchase months was slightly negative on non-purchase days.
- My guess (b > 0, t between 0 and 2, top third, pass 8%) was right on sign and size, a little
  high on rank; placebo sd 0.99 was just under the guessed 1.0-1.3.

## Step 3. W21 `stablecoin-mint` gate

### Data access (checked 2026-11-19, before any price was cut by it)

DefiLlama publishes the total circulating supply of USD-pegged stablecoins, daily, without a key
or account: `https://stablecoins.llama.fi/stablecoincharts/all` (JSON list of
`{"date": unix seconds at 00:00 UTC, "totalCirculatingUSD": {"peggedUSD": dollars}}`). The file
read on 2026-11-19 starts 2017-11-29; its first rows show only about $0.1m, so the early years
miss coins DefiLlama did not yet track (USDT was then about $0.6bn). The rule below guards
against that. The file goes to `research/data/stablecoins/` (gitignored), read as JSON data
only. Only the head of the file was printed (format check); no change or level after 2017-12 was
looked at.

### Decision rule (fixed and pushed before any number)

**Supply.** S(t) = `totalCirculatingUSD.peggedUSD` at the snapshot dated t (00:00 UTC), only
for t <= 2025-11-10 (train; later snapshots are not read even for placebos).

**Dose.** For a Friday F: m(F) = ln S(F - 1 day) - ln S(F - 8 days): the week's net issuance,
as a log change, ending Thursday 00:00 UTC, so it is public a day before the entry close below.
Missing (and the week dropped) if either snapshot is missing, if S(F - 8 days) < $1bn
(incomplete early tracking), or if |m| > ln 1.5 (a jump from DefiLlama adding a coin, not
issuance). The dry run prints how many weeks each guard drops.

**Outcome.** Coin bars are dated by UTC day and close at the next 00:00 UTC
(`grimstrade.data.close_time`). y(F) = the mean of BTC's and ETH's ln(close of the bar dated
F + 6 / close of the bar dated F - 1): Friday 00:00 UTC to the next Friday 00:00 UTC, an event
study on closes, not a fill model. Control c(F) = the same mean over the previous week (bars
dated F - 8 to F - 1), so the dose is not just last week's price move (issuance follows prices).

**Statistic.** OLS y = a + b m + g c over the Fridays of the sample, t of b with White (HC1)
standard errors (weekly returns do not overlap).

**Placebo null (the decider), one family, fixed here.** The same function with the dose
calendar moved by k whole weeks, m_k(F) = m(F - 7k days), for k in +-{3, ..., 22}: **40
placebos**. The control and the outcome stay put. Shifts of 1-2 weeks are left out (issuance
is spent over days, maybe into the next week). Weeks where m_k is missing are dropped from that
placebo only.

**Gate. Pass only if both hold** (gate sample: Fridays 2018-04-06 .. 2025-10-31, after
Griffin and Shams's sample; the last exit bar is dated 2025-11-06):
1. b > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41; empirical one-sided p = rank / 41 <= 0.049.

**Shown, not gating** (b, t, weeks): without the control; BTC alone; ETH alone; the halves
2018-04 .. 2021-12 and 2022-01 .. 2025-10; the same-week regression (this week's m on this
week's return c, to show how much issuance follows prices); mean next-week y in the top fifth
of m against the rest; the placebo null's width (gate-null step 5).

**On a pass:** no card now; a proposed card for the next window (coins on the Friday clock with
issuance as a weight overlay inside `tsmom12`'s coin slots), read at p < 0.00128 and the
register's p <= 4.9e-5 with z = (t - placebo median) / placebo sd. **On a fail:** W21 dead by
the gate, no card, no row.

**Power, written before any number.** Weekly coin returns have an sd near 9-10%; weekly supply
growth an sd near 1-2%. Over about 395 weeks the standard error of b is about 0.10 / (sqrt(395) x
0.015), about 0.34, so t >= 2 needs b near 0.7: a 1% week of issuance followed by +0.7% in
coins the next week. Only a strong effect passes.

**My guess before any number.** b > 0 with t between 0 and 1.5 after the control; rank in the
upper half; placebo t sd 1.2-1.6 (issuance is persistent, so shifted doses share regimes).
Chance of a pass: 4%.
