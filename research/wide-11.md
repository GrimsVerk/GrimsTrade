# Wide 11: two new filters for the score, the parked candidates re-scored, C3 gated

Research run wide-11, 2026-11-19. Branch `wide-11` (from `wide-10`), draft PR into `wide-10`.
Research only: fake money, public keyless data, no change to the gym, the daily runner or the
live strategies.

**Count carried in (wide-10):** union of the wide and survey lines, **78 mechanisms, 18 tested
by a strategy, none passed**; 13 gates, all failed. Family bar for the next strategy test
p < 0.10 / 78 = 0.00128. Project-wide (`git show origin/register-1:research/register/BAR.md`,
read 2026-11-19): **2,904 tries, N 1,012 for a new pick, Bonferroni p <= 4.9e-5.**

Method: every gate follows `research/gate-null.md` (placebo family fixed in the rule, 40
placebos, one code path for true and placebo, the rank decides, t >= 2 also required; rule,
script and tests pushed before any number; one dry run that prints counts only, then one real
run). A gate is descriptive: no `tries.md` row, no card, and it does not raise the tested count.

## Step 1. Two filters added to the scoring rule (written 2026-11-19, before any data look)

### Why

wide-10's two gates died for two different reasons that the score could not see. W20
`fed-purchase-flow` had a structural cause and a large measured dose, but the dose (the Fed's
purchase schedule) was published before the window, so a sector fund priced it before the
day. W21 `stablecoin-mint` had the same, but the dose (issuance) was answering prices: it rose
in the same week as coins (t 2.92) and shifted doses "predicted" just as well. Both are now
filters, applied before the six-point score of `wide-10.md` step 1.

### The filters (fixed now)

**F1, not announced.** The mechanism must not be one the market can price when the dose is
announced. It passes if either
- (a) the dose is a flow (someone must buy or sell) that is **not public before the measured
  window starts**; or
- (b) the mechanism is a **risk premium**: compensation earned over the window for holding a
  risk, which knowing the signal does not remove (a premium is meant to be earned on public
  information; it is not front-run away, only competed down).

It fails if the dose is a flow whose date and size (or size range) are public before the
window (scheduled purchases, index rebalances on a published list, unlock schedules, fixed
calendar dates without a dose).

**F2, not price-driven.** The dose must not be a function of the asset's own recent prices.
- Passes outright if neither the mechanism nor any known behaviour of the dosing agent makes
  the dose follow the asset's price.
- **Passes with controls (costs 1 point)** if the dosing agent is known to react to price, and
  the rule includes, fixed before any number, controls for the asset's own past returns at the
  horizons the reaction is known at; the dose then counts as its part not explained by them.
- Fails if the dose is itself a transform of the asset's price or yield (no control can
  remove that), or if the story is that the dose follows prices.

A candidate that fails F1 or F2 is not picked, whatever its score. The six points of the
wide-10 rule are unchanged; the F2 cost comes off them.

### The parked candidates re-scored

wide-10's unpicked C3-C6, plus the parked mechanisms in `ideas.md` that have a dose (the two
dead picks are scored too, to check the filters would have caught them). Score columns as in
`wide-10.md` (cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1).

| Candidate | F1 not announced | F2 not price-driven | Score (wide-10) | Re-scored | Verdict |
|---|---|---|---:|---:|---|
| W20 `fed-purchase-flow` (dead) | **fail**: schedule with dates, buckets and size ranges published before the month | pass | 7 | - | would have been filtered |
| W21 `stablecoin-mint` (dead) | pass (a): issuance not known ahead | **fail**: issuance follows coin prices (the story allows it; wide-10 measured it) | 6 | - | would have been filtered |
| C3 `hedging-pressure` | pass (b): a premium paid by hedgers to speculators (Keynes-Hicks) | **with controls**: commercial hedgers are known to sell forward into rallies (negative feedback), so the rule must control for the asset's past 4- and 52-week returns | 6 | **3** (see below) | the only candidate that passes both and is testable on assets the gym holds; gated in step 2 |
| C4 `buyback-blackout` | **fail**: blackout windows follow earnings dates, announced weeks ahead | partly (buybacks rise after price falls) | 5 | - | filtered |
| C5 `mortgage-convexity` | pass (b): a term premium | **fail**: the dose (mortgage rate minus its 5-year mean) is a transform of the bond yield, i.e. of TLT's own price | 5 | - | filtered |
| C6 `settlement-shift` | **fail**: settlement-lag changes and month ends are public calendar facts; no dose | pass | 4 | - | filtered |
| `stablecoin-resource` (wide-1 E1) | pass (a) | **fail**: supply level follows prices (W21) | - | - | filtered |
| `validator-queue` (wide-1 Q4) | **fail**: the Ethereum exit queue and its delay are public on chain before the coins can be sold | partly | - | - | filtered |
| `token-unlocks` (wide-1 Q6) | **fail**: unlock schedules are published in advance | pass | - | - | filtered (and paid data) |
| `crypto-carry` (ideas.md) | pass (b): a funding premium | with controls (funding rises in rallies) | - | not scored | passes both, but needs perpetual futures: the gym holds spot only |
| `halloween`, `lppls-bubble`, `hurst-entropy-gate`, `signature-leadlag` | `halloween` fails F1 (calendar, no dose) | the other three fail F2 (the dose is a function of the price path) | - | - | filtered |

**C3 `hedging-pressure` re-scored, honestly, with what this run found in the repo and the
literature before any data look:**

- 1 cause **0**: hedging is a business choice (as wide-10 scored).
- 2 dose **2**: hedgers' net short as a share of their positions varies week by week and is
  public three days after the Tuesday it describes; the premium should scale with it.
- 3 post-sample **0**: the latest source sample covering the futures we can map to our assets
  is Fan, Fernandez-Perez, Fuertes and Miffre, "Speculative pressure", Journal of Futures
  Markets 40(4), 2020, pp. 575-597 (checked on the web 2026-11-19: commodity, currency, equity
  index and fixed-income futures; premium in equity index futures, none in fixed income).
  Its sample is given by a secondary summary as COT data September 1992 .. May 2018
  `[search summary]`, not read in the paper. 2018-06 .. 2025-11 is 7.4 train years, short of
  the 8 the point needs. The other sources end earlier: de Roon, Nijman and Veld, "Hedging
  pressure effects in futures markets", Journal of Finance 55(3), 2000, pp. 1437-1456 (20
  futures markets in four groups, financial among them; checked; sample years not confirmed,
  1986-1994 `[memory]`); Basu and Miffre, "Capturing the risk premium of commodity futures:
  the role of hedging pressure", Journal of Banking & Finance 37(7), 2013, pp. 2652-2664
  (checked; commodities only; sample years not confirmed, to about 2011 `[memory]`).
- 4 power **1**: about 385 non-overlapping 4-week blocks across the four assets in
  2018-06 .. 2025-10 (borderline: the assets move together).
- 5 unseen **1, narrowly**: info-1 (2026-11-13, `info-1.md`) already screened the weekly
  mirror image: non-commercial (speculator) net / open interest as a 3-year z-score, against
  the coming week's risk-adjusted return, six assets pooled, 2000-2025: in-sample IC -0.024
  (chance level 0.028), the wrong sign for the premium (high speculator long = high hedger
  short should mean higher returns). That cut is seen. Not computed anywhere: commercials'
  own hedging pressure, on the 4-week return, with price-path controls, judged on the years
  after Fan et al.
- 6 not killed **0**: info-1's screen found nothing in the weekly COT inputs; a monthly
  horizon is what info-1 itself named as "a new card, not a re-read", but the idea family has
  been looked at and found empty.
- F2 with controls: **-1**.

**Re-scored total 3 of 7.** By the rule C3 would not be picked in a contest; it is gated here
because the lead asked for it and it is the only parked candidate that passes both filters
and can be tested on the assets the gym holds. Prior lowered from 2% to **1%**.

### What the filters leave

Of 15 parked or dead candidates, two pass both filters: C3 (gated below) and `crypto-carry`
(perpetual futures; not in the gym). The filters are strict on purpose: most forced-flow
stories are flows on a public schedule (F1) and most crypto stories are flows that follow
price (F2). A new mechanism worth a gate now needs **an unscheduled flow that does not answer
price, or a premium**, and the list of such ideas is short: the next ideation lane should
start from that sentence, not from a new field.

## Step 2. C3 `hedging-pressure` gate (enters the list as W22)

### Data access (checked 2026-11-19, before any price was cut by it)

The CFTC's legacy Commitments of Traders report, futures only, as yearly zip files without a
key or account: `https://www.cftc.gov/files/dea/history/deacot1986_2016.zip` and
`deacot{YYYY}.zip` for 2017-2025. They sit in the shared research cache (`cftc/legacy/` under
the cache root of `research/macro.local.json`; fetched 2026-11-13 by `scripts/fetch_info1.py`,
sha256 in the cache's `manifest.jsonl`), read as CSV data only. Format probe before this rule
(header and market names only, no position or price value printed): fields `CFTC Contract
Market Code`, `As of Date in Form YYMMDD`, `Commercial Positions-Long (All)`, `Commercial
Positions-Short (All)`; codes 088691 gold (COMEX), 020601 Treasury bonds (CBOT), 13874A E-mini
S&P 500, 209742 E-mini Nasdaq-100, 043602 10-year notes, 084691 silver, 133741 CME bitcoin.

### Decision rule (fixed and pushed before any number)

**Markets.** Gate panel: GLD <- gold 088691, TLT <- Treasury bonds 020601, SPY <- E-mini S&P
500 13874A, QQQ <- E-mini Nasdaq-100 209742 (the four ETFs of the live six with a matching
futures market and history long enough for the placebos). Shown only: IEF <- 10-year notes
043602, SLV <- silver 084691, BTC <- CME bitcoin 133741 (from 2017-12: too short for the
long placebo shifts, so not in the gate).

**Reports.** One report per market per Tuesday position date T (duplicates across files: the
later file wins). Only T <= 2025-11-10. Reports whose release was delayed by a government
shutdown are dropped everywhere (info-1's windows): T in 2013-10-01 .. 2013-10-29,
2018-12-21 .. 2019-03-05, and from 2025-09-30.

**Dose.** Hedging pressure HP(T) = (CS - CL) / (CS + CL), CS and CL = commercial short and long
positions (all). HP > 0: hedgers are net short, speculators are paid to be long (Keynes-Hicks),
so the predicted sign is positive. z(T) = (HP(T) - mean) / sd (ddof 1) over the market's
earlier reports dated T - 1092 days .. T - 1 day (156 weeks), needing at least 104 of them;
past-only, so markets with different hedger mixes are comparable.

**No look-ahead (the release lag).** T's report is released on Friday T + 3 at 15:30 New York
time; in holiday weeks it moves to Monday or later. Entry is therefore at
the close of the asset's first bar dated >= T + 7 (the next Tuesday): a day of slack beyond the
latest regular release. Exit at the close of the first bar dated >= T + 35. y(T) = ln(exit /
entry), dividend-adjusted closes (`harness.load_history("train")`). The row is dropped if
either bar is missing, the exit bar is dated after T + 42, or after 2025-11-10. (ETF total
returns stand in for futures returns: the difference is the cash rate, nearly constant
within 4 weeks and taken up by the market intercepts.)

**Controls (F2).** r4(T) = ln(close of the last bar dated <= T / close of the last bar dated <=
T - 28) and r52(T) the same with T - 364: the asset's own past 4- and 52-week returns, known at
T.

**Statistic.** Pooled OLS over all gate rows of the four markets: y = a_market + b z + g4 r4 +
g52 r52 (one intercept per market). t of b with Driscoll-Kraay standard errors: scores summed
over the rows of each report week, then Newey-West (Bartlett) with 4 lags over the week index
(weeks counted by date, so dropped weeks stay gaps): the four markets' rows in a week are
correlated and the 4-week returns overlap by 3 weeks.

**Placebo null (the decider), one family, fixed here.** The same function with each market's
dose calendar moved by k weeks: z_k(market, T) = z(market, T - 7k days), outcome and controls
stay put, rows with a missing z_k dropped from that placebo only. k in +-{27, 31, 35, ..., 103}
(odd, step 4): **40 placebos**. Shifts under half a year are left out because hedging
pressure is persistent for months (a short shift would be nearly the true dose); odd weeks are
never a multiple of 52, so no placebo is the same date a year away.

**Gate. Pass only if both hold** (gate sample: report dates 2018-06-05 .. 2025-10-06, after the
latest source sample, Fan et al.'s May 2018; the last exit is <= 2025-11-10):
1. b > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41 (true plus 40 placebos); empirical one-sided p =
   rank / 41 <= 0.049.

**Shown, not gating** (b, t, rows): without the controls; the 1-week horizon (exit at the first
bar >= T + 14, 1 lag; the info-1 mirror, with commercials); raw HP level instead of z (market
intercepts kept); each gate market alone; IEF, SLV and BTC alone (own z; BTC's starts about
2020); the pre-gate years, report dates 2008-01-01 .. 2018-05-29 (inside Fan et al.'s
sample); the feedback check for F2: z(T) - z(T - 28 days) on r4(T), pooled (how much hedgers
follow price); the placebo null's width (gate-null step 5).

**On a pass:** no card in this run. A proposed card for the next window (the four ETFs held or
scaled by z inside `tsmom12`'s slots on the Tuesday-plus-7 clock), read at the family bar
p < 0.10 / 79 = 0.00127 and the register's p <= 4.9e-5 with z = (t - placebo median) /
placebo sd. **On a fail:** W22 dead by the gate, no card, no row.

**Power, written before any number.** 4-week returns of the four ETFs have an sd near 4-6%;
z has sd about 1. About 385 report weeks, four correlated markets (say 1.5 effective each),
overlapping by 3 weeks: the standard error of b is roughly 5% / sqrt(385 x 1.5 / 2), about
0.4% per unit of z (the overlap halves the effective count). A premium of 3% a year per sd of
hedging pressure is 0.23% per 4 weeks: t about 0.6. Only an effect several times the size the
literature reports for financial futures passes.

**My guess before any number.** b near zero, t between -1 and +1.5; rank in the middle; placebo
t sd 1.3-1.8 (persistent dose, overlapping returns, four correlated markets). The feedback
check: commercials sell forward into rallies, so HP rises after a rally: slope positive,
t > 3. Chance of a pass: 2%.
