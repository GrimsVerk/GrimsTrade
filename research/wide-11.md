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
