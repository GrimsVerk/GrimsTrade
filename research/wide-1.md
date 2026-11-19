# Wide 1: new hypotheses from other fields

Research run wide-1, started 2026-11-17. Branch `wide-1` (from `carry-2`). Research only: fake
money, public data, no change to the gym, the daily runner or the live strategies.

Question: after 14 runs nothing beats the 12-month trend rule (`tsmom12`) on the six assets. Do
other fields (ecology, epidemiology, signal processing, control, information theory, game
theory, physics, queueing, neuroscience, immunology) suggest a mechanism we have not tested,
whose edge would come from somewhere other than trend?

## In plain words (results, 2026-11-18)

**None of the four new ideas beats the trend rule. All four fail the pass mark that was written
down before testing, so the held-out year was not looked at.** Two are plainly dead. Two leave a
faint trace in the raw prices that is real enough to describe and too small to trade in our book.
**Looking at why they failed turned up one pattern that is stronger than anything carded: long
bonds earned almost all of their return in the last four trading days of each month.** It was
found after the tests, on the same data, so it is a hypothesis for a new card, not a result.

What was done: 46 mechanisms from ten fields were written down and sorted before any number
(step 1 below). Most turned out to be an idea we had already killed, in different words. Four
survived. All four bet on **someone else's mechanical trading**: a bond dealer who must absorb an
auction, a pension fund that must restore its stock/bond mix, a fund that must follow its
volatility formula, and prices that have not yet caught up with their relatives.

| Idea (field) | In one line | Verdict | Key numbers | Why |
|---|---|---|---|---|
| `auction-concession` (queueing / inventory) | Hold no TLT for the five sessions ending with a 20- or 30-year Treasury auction | **fails; faint lead on TLT alone** | Book: +0.01 Sharpe over `tsmom12` (p 0.14). TLT alone: 0.50 against 0.33 (p 0.05). IEF with 7/10-year auctions: 0.26 against 0.55 | TLT did earn less on those days in every period (0 to -8 bps a day against +3 to +4), but about 70% of the gap is 2020-25. On IEF the rule fails because 7-year auctions fall in the last days of the month, when bonds rise |
| `rebalance-pressure` (control theory) | In the last five sessions of a month, halve whichever of stocks or bonds led the month | **fails** | Book: -0.005 (p 0.67). Raw stock-minus-bond return in the window: +38 bps a month in the predicted direction (t 1.7); +56 before 2014, +21 since | The effect is the month's *loser rising*, not the leader falling. Halving the leader gives up its own month-end rise, and the freed money often has nowhere to go (the loser is out of trend) |
| `contagion-catchup` (epidemiology) | Among 21 ETFs, hold those whose close relatives moved last week and which did not | **dead** | 0.50 against 0.60 for the trend rule on the same ETFs (p 0.87); coins 0.38 against 0.74 | Relatives' moves do not spill over: that half of the signal has IC -0.015. All that is left is plain one-week reversal (IC +0.03, t 2.9), and that does not pay either (0.53) |
| `vol-echo` (signal processing x control) | Hold stocks for three days when a shock day leaves the 21-day volatility window | **dead** | SPY 0.25 against 0.63 at the same average exposure (p 0.98); behind on every other market too | The days it holds earn a little more on average (+9.5 against +5.1 bps since 2010) but sit in turbulent weeks and are far riskier. The 1962-1993 placebo, before such funds existed, shows the same small excess: it is not the funds |

(Sharpe = return per unit of risk. IC = correlation between a signal and what happened next. p =
chance of a gap this large by luck; the bar is below 0.10. bps = hundredths of a percent.)

**The pattern worth carrying forward (post hoc; `results/wide-1-yields.md`).**

- 2003-2025, last four sessions of the month: TLT +39 bps (t 4.3), IEF +24 bps (t 5.4), the
  same in both halves of the period. At the gym's next-open fills: +32 and +21 bps (t 3.3 and
  4.5). For TLT that is about 4.7% a year, as much as its whole average return: the other 80%
  of days together earned nothing.
- Before TLT existed (bond yields, data no rule here has used): nothing in 1962-1989; +13 bps
  (10-year) and +23 bps (30-year) in 1990-2003, t about 2. By the reading fixed before looking
  (pooled 1962-2003, |t| >= 2) that is **not confirmed**: pooled t is 0.8 and 1.2. But it is
  what one would expect from the usual explanation, bond index funds that must buy longer
  bonds when their index is rebuilt at month end: such funds hardly existed before 1990.
- Our own `month-end-liquidity` test missed it because its window ran three sessions into the
  next month, where TLT gave part back until 2013 (-39 bps then, -6 since).
- A paper on this exists as far as I remember (Hartley and Schwarz, "Predictable end-of-month
  Treasury returns"; not opened in this run).

**How sure.**

- Sure about the two dead ones: the gaps are large, every era and every other market agree, and
  the built-in controls (plain reversal for contagion, the placebo era for the echo) explain why.
- Sure that neither flow idea helps the six-asset book as carded.
- The auction dip is in the closing prices and half of it is lost to our fills. Close to close,
  TLT fell 34 bps over the five sessions ending with a 30-year auction (t 2.5; both halves),
  near the size the 2013 paper reported. Filled at the next open, as the gym does, it is 15 bps
  (t 1.1). Before 2003 the yield data shows no dip, but with 72 auctions it could not have shown
  one of this size either. Not confirmed, not refuted.
- TLT alone beating its twin ("p 0.05") is one of about ten side comparisons in this run, and its
  out-of-universe check (IEF) went the other way: taken alone it is not evidence.
- The month-end "loser rises" effect is **not confirmed** on unseen data: +13 bps pooled over
  1962-2003 (t 0.9), wrong sign in 1962-1979, right sign after. Since 2003 it is large at closing
  prices (+86 bps, t 3.9), mostly stocks rising after a month in which they trailed bonds.
- 8 variants, 10 variant rows, 39 rows in `tries.md`. The best gain over a twin in the main book
  is +0.01; luck alone gives far more across this many tries. Nothing came near a pass.

**What died, and what it teaches.**

1. **Other fields mostly rename what finance already has.** Of 46 mechanisms, 33 collapsed
   into an idea already tested here (a smoother trend, a volatility gate, a weak weekly forecast,
   a cycle clock with four cycles). The useful output of the exercise is the sorting rule at the
   top of step 1, not the vocabulary.
2. **Forced flows are real but small, and a long-only equal-slot book cannot size them.** Both
   flow effects show up in raw prices at 15-40 bps per event. In our book one event moves half of
   one slot for a week: a few hundredths of a percent. Flows of this size are harvested with
   futures and leverage, which the gym does not have.
3. **"Out of the asset" is an expensive way to trade a relative effect.** Both flow rules lost
   part of their edge by sitting in cash: the month-end rule gives up the leader's own rise,
   the auction rule gives up the bond's drift.
4. **Calendars collide.** The auction calendar and the month-end calendar overlap (7-year notes
   are sold in the last week of the month), so a rule built on one is hit by the other. That
   collision is how the month-end bond pattern was found.
5. **Fills at the next open cost up to half of a short-lived effect.** The auction dip keeps 45%
   of its closing-price size at our fills, the month-end bond rally 83%.
6. **Liquid ETFs do not lag each other by a week.** If anything they overshoot together and come
   back: the network term was negative.

**Next lanes this opens** (each needs its own card; none changes the paper system today).

1. **A `month-end-bonds` card.** Rule from the mechanism, fixed before any run: hold the long
   bond for the last four sessions of each month (bought at the open of T-3, sold at the open of
   T+1), using the cash the trend rule leaves idle. It was found on TLT and IEF 2003-2025, so
   passing there proves nothing. Clean tests left: LQD (not looked at in this run), TLT's first
   year (2002-07 to 2003-07), the held-out year once, then forward paper. If real, it is worth
   roughly +0.5 to +1% a year on the six-asset book (idle cash averages a quarter of it), about
   +0.04 Sharpe, from a source that has nothing to do with trend.
2. **A volume screen.** No test in 15 runs has used the six assets' own trading volume. One cheap
   IC table by info-1's method (abnormal volume, price move per dollar traded, weekly and 4-week
   horizons) either closes that class of input or opens it.
3. **The month-end stock bounce, with a placebo first.** Since 1990 stocks rose in the last five
   sessions after a month in which they trailed bonds (unseen 1990-2003: +71 bps, t 1.5; since:
   +182 bps, t 4.0). Before a card, one table must show whether the same condition measured in
   mid-month does the same; if it does, this is plain dip buying (`dip-rsi2`: real and small),
   not rebalancing.

For the owner rather than a research lane: flow effects of this size only matter with futures
and modest leverage (the broker gap the carry lead ran into), and two of them are worth more at
the close than at the next open. Whether the paper broker should fill at the close is a design
question, not a research one.

**Compared with my guess before any number** (below): I gave the four ideas a 20%, 15%, 10% and
5-10% chance of passing. None did. The sizes came out at the low end of what I expected for the
two flow ideas and below it for the other two. What I did not expect is that the most solid
pattern of the run would be one no card asked about.

### Disclosures

- **Dry runs printed numbers before the logged runs.** Each script was first run with `DRY=1`
  (last 120 days of train, nothing logged) to check the plumbing. The `rebalance-pressure` dry
  run also printed its event study for the whole train period, because that table does not go
  through the harness. All four cards were already pushed (commit a7f90ff) and no rule or
  parameter was changed afterwards (rule code committed in ae289c5, before the logged runs).
- **Seen before the cards:** the Treasury's auction calendar (dates and terms, no prices), to
  write the auction rule. The download holds auction dates up to 2026-10; they are dates, and
  no bar after 2025-11-10 was loaded by any test.
- **Price cache:** copied from the breadth-1 worktree (fetched 2026-11-13). `tsmom12` and equal
  weight reproduce 1.05 and 0.88.
- **Reading of bar 2.** For the two rules that need TLT, eras are counted from 2000-09 (before
  TLT exists the rule *is* its twin), 3 of 4 needed. Written on the cards before testing.
- **`contagion-catchup` has its own pass bar** (card), because its book is 21 ETFs, not the six
  assets; each line is at least as strict as the default.
- **`constant@SPY` and `constant@QQQ` appear twice in `tries.md`**: the twins of `echo21` and of
  `echo63` have different exposures (14% and 7%) and share a name.
- **Post-hoc tables** (`results/wide-1-posthoc.md`, script `lib/wide1_posthoc.py`) were made after
  the verdicts and are not strategies; they have no rows in `tries.md`.
- **Step 4** (`results/wide-1-yields.md`, script `lib/wide1_yields.py`) is descriptive. Its three
  questions and its reading rule were pushed (commit d6582da) before the yield data was read.
  One section, the cross-check on ETF closes, was added after the first output, to explain why
  the yield series and the ETF table disagreed on the auction dip; it says so in its title.
  Carry is booked per calendar day, not per session as the definition said (same average).
- **Not run:** the held-out year, for any of the four.

## Step 1. Ideation (written 2026-11-17/18, before any number of this run)

### What the earlier runs force on any new idea

Three facts from our own tests decide where it is worth looking at all.

1. **A new weak forecast of next week is worth nothing on six assets.** rl-3 measured it: a
   weekly signal needs an IC (correlation between forecast and outcome) of about 0.10 to add
   +0.16 Sharpe, and nothing screened so far reaches 0.05. So "a new predictor that tilts the six
   weights a little" is dead before it starts, whatever field it comes from.
2. **A "step out of risk when X" gate cannot be validated.** Thirty years hold 4-7 bear markets
   and 3-4 crypto winters. Ten such gates were tested (macro phases, absorption ratio, HMM, the
   halving, YouTube tops); each failed or could not be told from luck. `tsmom12` already leaves
   when prices fall, and leaving earlier cost more than it saved.
3. **Costs decide in crypto.** A round trip costs 60 bps there and 4 bps in ETFs. Anything that
   trades often can only live in ETFs.

So this run looks for effects with **hundreds of dated events, in ETFs, whose cause is not the
price trend**. The best candidates are the forced, mechanical trades of other market
participants (someone *must* trade a known amount at a known time) and the spread of a shock
across assets that close at the same moment.

### Field by field

One line per mechanism: what would make money, the maths tool, and the verdict. "Kill" names the
tested idea it collapses into.

**1. Population ecology (predator-prey, carrying capacity)**

| # | Mechanism | Tool | Verdict |
|---|---|---|---|
| E1 | Stablecoin supply is the food coin prices live on; price that outruns it overshoots and falls back | consumer-resource Lotka-Volterra fit | **Park.** Two cycles (2018+), two coins: the halving problem again; info-1's coin inputs restated the trend |
| E2 | ETH and BTC (or QQQ and SPY) compete for the same capital; the fitted sign says coexistence (ratio reverts) or exclusion (ratio trends) | competitive Lotka-Volterra / replicator | **Kill.** Cross-sectional momentum between two assets with a fitted sign; breadth-1: adds nothing on top of trend |
| E3 | Bitcoin adoption follows a logistic curve; price far above the curve is a bubble | logistic fit | **Kill.** A cycle clock on 3-4 cycles (halving, `ath`, LPPLS); on-chain inputs IC ~0 (info-1) |
| E4 | Leverage is the predator of calm prices (Minsky as predator-prey) | Lotka-Volterra phase | **Kill.** The observable is funding/basis: screened in info-1, IC ~0 |
| E5 | A predictable supply pulse bigger than the consumers can eat at once is eaten at a discount (predator satiation) | event study | **Keep** as `auction-concession` (see 8) |
| E6 | Leave a patch when its yield falls below the average of all patches, net of travel cost | marginal value theorem | **Kill.** Relative momentum with a switching band |

**2. Epidemiology (contagion)**

| # | Mechanism | Tool | Verdict |
|---|---|---|---|
| P1 | A shock spreads along the links between assets. An asset whose neighbours moved, and which has not, is "susceptible" and catches up | SIR on the correlation network (graph diffusion) | **Keep** as `contagion-catchup` |
| P2 | Attention is the infection: a mania ends when new infections peak | SIR fit on Wikipedia page views | **Park.** Three manias, all coins at once. Data is free (Wikimedia, from 2015-07) |
| P3 | A downtrend infects sector after sector; leave when it spreads, return when it burns out | SIR on 9 sectors | **Kill.** Leaving early (macro-1); returning early = a faster trend rule (`sma200`, `ensemble-tsmom` tie); ~6 bear markets |
| P4 | Liquidation cascades in perps percolate; buy when the forced sellers are done | percolation / avalanche size | **Kill.** Daily reversal in large coins is dead (literature); open-interest data starts 2021-12; 60 bps |

**3. Signal processing (filtering, spectral methods)**

| # | Mechanism | Tool | Verdict |
|---|---|---|---|
| S1 | A cleaner estimate of the trend | Kalman, wavelets, spectra | **Kill.** A smoother trend rule (`drawdown-control`, `ensemble-tsmom`, `fracdiff-momentum`) |
| S2 | Track the strength of a cycle at a known frequency (month, quarter) | lock-in amplifier | **Kill.** `month-end-liquidity` faded since 2014; the tool only tells us sooner that it is gone |
| S3 | The same coin on two venues: the difference is one side's demand | common-mode rejection | **Kill.** A daily flow signal on two coins cannot pay 60 bps (breadth-1) |
| S4 | Funds that target a fixed volatility measure it over fixed windows (1 and 3 months). When a shock day drops out of the window, measured volatility falls on a date known 21 days ahead, and they must buy | boxcar-filter "ghost"; shadow controller | **Keep** as `vol-echo` (with 4) |
| S5 | Slow lead-lag between asset classes | cross-spectrum | **Kill.** info-1's 13-week cross-asset inputs: IC ~0 |

**4. Control theory (feedback, robust control)**

| # | Mechanism | Tool | Verdict |
|---|---|---|---|
| C1 | Steer our own exposure by feedback on drawdown or volatility | PID, H-infinity | **Kill.** `vol-target`, `drawdown-control`, `kelly-shrunk`, `trend-vol` |
| C2 | Other people's controllers: balanced funds hold a fixed stock/bond mix and correct it at month end. The correction is proportional to the month's gap and known in sign and timing | proportional controller, known setpoint | **Keep** as `rebalance-pressure` |
| C3 | Volatility-control funds keep selling for days after a spike, then stop | rate-limited controller | **Kill.** Dip buying after a spike (`dip-rsi2`: real, small). Its echo (S4) is the untested half |
| C4 | Bitcoin's difficulty adjustment is a sampled controller that squeezes miners | discrete feedback | **Kill.** A function of hash rate; `hash_growth` IC -0.003 (info-1) |
| C5 | Optimal no-trade region | HJB | **Kill.** Saves costs, adds no edge; `tsmom12` trades rarely |

**5. Information theory (compression, coding)**

| # | Mechanism | Tool | Verdict |
|---|---|---|---|
| I1 | Trade only when the series is compressible | Lempel-Ziv, MDL | **Kill.** `hurst-entropy-gate` (parked): ~5 readings in ten years |
| I2 | Let description length pick the look-back | MDL segmentation | **Kill.** `changepoint-momentum` (dead, literature) |
| I3 | Universal coding portfolios | exponential weights | **Kill.** `universal-portfolio` |
| I4 | A never-seen pattern of co-movement is a warning | compression distance | **Kill.** The gate family (`absorption-ratio`, `turbulence`) |
| I5 | The value of side information | Kelly / mutual information | Nothing to trade: it *is* fact 1 above |

**6. Evolutionary game theory**

| # | Mechanism | Tool | Verdict |
|---|---|---|---|
| G1 | Capital flows to the strategy that did well lately | replicator dynamics | **Kill.** Grading the trend rule's trades (`ml-filter`) |
| G2 | When every trend signal agrees, the trade is crowded | frequency-dependent fitness | **Kill.** Leaving early |
| G3 | Once a calendar habit is known, players move a day earlier, then another | minority game | No rule. It is why calendars fade, and why this run prefers flows that are *forced* (the auction must happen, the fund must rebalance) to flows that are habits |
| G4 | Liquidity providers are paid for patience | hawk-dove | **Kill.** Hourly reversal is real but costs ten times the edge (breadth-1) |

**7. Statistical physics (phase transitions, percolation)**

| # | Mechanism | Tool | Verdict |
|---|---|---|---|
| F1 | Assets as spins; alignment and spanning clusters warn of a crash | Ising, percolation | **Kill.** Alignment = breadth (no skill in run 2); spanning cluster = `absorption-ratio` |
| F2 | The sign of the stock-bond correlation is an order parameter that says which hedge works | regime switch | **Kill.** A refinement of `trend-to-safe`; one flip since TLT exists |
| F3 | Bubbles as critical points | LPPLS | Parked already |
| F4 | Time-irreversibility of returns as a regime marker | entropy production | **Kill.** The gate family |
| F5 | Heat flow on a network | graph Laplacian | Same as P1: it is the tool of `contagion-catchup` |

**8. Queueing and inventory theory**

| # | Mechanism | Tool | Verdict |
|---|---|---|---|
| Q1 | Bond dealers are a server with limited capacity. A Treasury auction is a large batch arriving on a published date. Dealers make room by selling beforehand; prices dip into the auction and recover after | scheduled-arrival queue; event study | **Keep** as `auction-concession` |
| Q2 | Dealers' inventory makes yesterday's move reverse | inventory model | **Kill.** `dip-rsi2`, hourly reversal |
| Q3 | Waiting time (price impact per dollar traded) earns a premium | Amihud ratio | **Kill.** Moves with volatility; volatility gates are dead. But see "volume" under next lanes |
| Q4 | Ethereum's validator exit queue is a literal queue of coming supply | queue length | **Park.** Data from 2023-04, one coin |
| Q5 | The chance a trend ends depends on its age | renewal process, hazard rate | **Kill.** Changes *when* the trend rule acts, not where the edge comes from |
| Q6 | Token unlock schedules are supply pulses in small coins | event study | **Park.** Paid data (price not checked, nothing bought); small coins only |

**9. Neuroscience (predictive coding)**

| # | Mechanism | Tool | Verdict |
|---|---|---|---|
| N1 | One asset predicts its sibling; the prediction error gets corrected | Kalman innovation | **Kill on six assets** (two sibling pairs, fact 1). Lives on only as the "own move" half of `contagion-catchup`, where its plain twin is run |
| N2 | The gap between feared and realised volatility is a prediction error that pays over 1-3 months | variance risk premium | **Kill.** `vrp` weekly IC -0.002 on 1,348 weeks (info-1): nothing to add up over a quarter |
| N3 | Anchoring on the yearly high or the average purchase price | reference dependence | **Kill.** `dd_1y`, `high_52w`: no skill; a volume-weighted cost basis is a moving average |

**10. Immunology (anomaly detection)**

| # | Mechanism | Tool | Verdict |
|---|---|---|---|
| M1 | Learn "self", react to "non-self" | negative selection, Mahalanobis distance | **Kill.** The gate family; `turbulence` stays `new` only against a volatility trigger |
| M2 | Detectors that multiply when they were right | clonal selection | **Kill.** Boosting (`ml-gbm`) |
| M3 | The n-th repeat of the same shock matters less | tolerance | **Kill.** Needs news labels, not bars |

### What survives: four ideas, one common thread

All four trade against (or alongside) **someone whose behaviour is mechanical**: a dealer who must
absorb an auction, a fund that must restore its mix, a fund that must follow its volatility
window, and prices that have not yet caught up with their neighbours. None uses the asset's own
long trend, so any edge would be a second source next to `tsmom12`, not a variant of it.

| Idea | Field x tool | Where the money would come from | What has to be true |
|---|---|---|---|
| `auction-concession` | queueing/inventory (and predator satiation) x event study on a published schedule | The Treasury pays dealers a discount to absorb new long bonds; a holder who steps aside for the week before the auction avoids paying it | Long-bond prices still dip before 20/30-year auctions by more than a week of TLT's normal drift (published 1980-2008: about 2-3 bps of yield, ~40 bps of TLT price); the dip is not already traded away; it shows at next-open fills |
| `rebalance-pressure` | control theory x a shadow controller (the 60/40 fund's known correction) | Month-end sellers of whatever rose most pay a small price concession; a holder who leans the other way for the last week collects it | Balanced funds still rebalance on the calendar in size; the month's leader lags the loser in the last days; the effect is larger than 4 bps of cost; front-runners have not moved it out of the window |
| `contagion-catchup` | epidemiology x diffusion on the correlation network | Slow diffusion of news across related ETFs: buy the ones whose neighbours have moved and which have not | Related ETFs still under-react to each other at a one-week horizon; the catch-up is more than plain one-week reversal; it survives being added to the trend rule |
| `vol-echo` | signal processing x control theory (the ghost of a boxcar window in other people's risk controllers) | Mechanical buying by volatility-targeting funds on the day a shock leaves their 1- or 3-month window, a date known three weeks ahead | Enough money uses simple fixed windows; the buying moves the index by a visible amount; the effect is absent before such funds existed (a built-in placebo: 1962-2009) |

### My guess before any number (so the result can be compared with it)

Rough power, from published sizes and our own noise levels:

- `auction-concession`: about 210 auctions of 30-year bonds since 2006 plus 66 of 20-year ones.
  If the dip is still ~40 bps over five days, the test would see it at about t = 3; at half
  that, t = 1.5. Published in 2013 on data to 2008, so decay is likely. Chance it passes: 20%.
- `rebalance-pressure`: about 270 month ends since TLT exists. A 5 bps a day edge on the
  stock-bond spread gives t = 1.3; 10 bps gives 2.6. Chance: 15%. Even if real, the gain on
  the whole book is small (a few tenths of a percent a year), because only half a slot moves.
- `contagion-catchup`: unknown size; our own breadth-1 found one-week momentum slightly negative
  across 33 markets, which is half of this signal. Chance: 10%.
- `vol-echo`: the most novel and the weakest in power. A plausible flow moves the index ~10 bps
  per event; with ~300 events that is t = 1 to 1.5. Chance it passes: 5-10%. It is run because
  it is cheap, has never been tested as far as I know, and has a built-in placebo.

Even the optimistic cases are small: these are possible second sources of return next to the
trend rule, not replacements for it.

### Not carded, but noted for later

- **Volume has never been screened.** All 15 ML features come from closes, and info-1's 23 inputs
  are outside data. The six assets' own volume (abnormal volume, price move per dollar traded)
  deserves one cheap IC table by info-1's method before anyone builds on it.
- **Carry on spot.** Our one outside lead is carry on perps. The same idea exists for the six
  assets without futures (the bond's yield over cash for TLT, the real rate for GLD); macro-1's
  skill table has faint hints (curve slope against TLT rho +0.11, t = 2.0). Not from another
  field, so not carded here.

## Step 2. Cards (written 2026-11-17 23:20 UTC, pushed before any test)

[auction-concession](cards/auction-concession.md),
[rebalance-pressure](cards/rebalance-pressure.md),
[contagion-catchup](cards/contagion-catchup.md), [vol-echo](cards/vol-echo.md). Each fixes the
rule, the variants (two each: eight in all), the twin, the out-of-universe sets and the pass
bar. The only thing looked at before writing them was the Treasury's auction calendar (dates and
terms, no prices).

## Step 3. Tests (run 2026-11-17 23:25 UTC, train only)

- Rules: `lib/wide1_rules.py` (pure logic, tested offline in `tests/test_wide1.py`) and
  `lib/wide1.py` (calendars, the auction file, book universes). One script per card:
  `lib/idea_wide1_auction.py`, `idea_wide1_rebalance.py`, `idea_wide1_contagion.py`,
  `idea_wide1_vol_echo.py`. The auction calendar is parsed by `lib/wide1_auctions.py` (run with
  `python -I`) into `<cache_root>/derived/wide-1/auctions.csv`.
- No look-ahead: `lib/wide1_check.py` proves that every rule gives the same weights as
  `gym.backtest` (which shows a strategy only the bars closed before the decision) on eight
  sample days, including days inside an auction window and a month-end window.
- Results: [auction-concession](results/auction-concession.md),
  [rebalance-pressure](results/rebalance-pressure.md),
  [contagion-catchup](results/contagion-catchup.md), [vol-echo](results/vol-echo.md); post-hoc
  tables in [wide-1-posthoc](results/wide-1-posthoc.md).
- To rerun: `uv run python -I research/lib/wide1_auctions.py`, then
  `uv run python research/lib/idea_wide1_<name>.py` (each appends its rows to `tries.md`).

## Step 4. A descriptive check on data no rule has seen (defined 2026-11-18, before looking)

Not a card and not a strategy: no rule is selected, nothing goes through the harness, no rows in
`tries.md`. The post-hoc tables suggested three patterns on 2003-2025 ETF prices. The same
patterns can be looked for in bond yields before TLT and IEF existed. Fixed here, before any of
this data was read:

- **Data.** FRED `DGS10` (10-year Treasury yield, daily from 1962) and `DGS30` (30-year, from
  1977; not published 2002-02 to 2006-02), the cached snapshot, cut at 2025-11-10. Stocks: the
  S&P 500 index (price only) to 1993-01, SPY (total return) after. The auction calendar (from
  1979-10) as before.
- **Bond return.** A par bond of maturity n (10 or 30 years) earns about `-D x (change in
  yield) + yield / 252` a day, with D its duration at yesterday's yield,
  `D = (1 - (1 + y/2)^(-2n)) / y`. An approximation; close to close, not gym fills.
- **Periods.** Unseen: 1962-1979, 1980-1989, 1990 to 2003-07 (the day before our TLT and IEF
  tests start). Seen: 2003-08 to 2025-11, by the same method, only to check that it agrees with
  the ETF tables.
- **Q1, the dip before auctions.** For every nominal auction of 30-year bonds and of 10-year
  notes: the matching bond's return over sessions A-4 .. A and over A+1 .. A+5. Expected if the
  effect is real: negative before, positive after.
- **Q2, the month-end bond rally.** The 10- and 30-year bond's return over the last four
  sessions of each month, minus four average days of the same period; and the first three
  sessions of the next month. Expected: positive in the last four.
- **Q3, the month-end loser bounce.** g = stocks minus the 10-year bond, month to date at the
  close of T-5. For months with |g| >= 2%: the return of stocks and of the bond over sessions
  T-4 .. T, each leg and the spread signed against g, split by who led. Expected: the signed
  spread is positive, and stocks rise after trailing.
- **Reading.** A pattern "holds on unseen data" if its sign is as expected in the pooled unseen
  period with |t| >= 2. Anything less is "not confirmed". Either way it is evidence for or
  against writing a card, not a result.

### Step 4, what came out (tables in `results/wide-1-yields.md`)

| Question | Unseen data (to 2003-07) | Seen data (2003-08 to 2025) | Reading |
|---|---|---|---|
| Q1, dip before 30-year auctions | +3 bps (t 0.1; 72 auctions): no dip, but too few auctions to tell | -54 bps from yields (t -3.6), -34 bps on TLT's closes (t -2.5), -15 bps at next-open fills (t -1.1) | not confirmed; half of it is lost to our fills |
| Q1, dip before 10-year auctions | +17 bps (t 1.1; 97): none | -11 bps from yields (t -1.6), -5 bps on IEF's closes | not confirmed |
| Q2, month-end bond rally (last four sessions, excess) | 10-year +3 bps (t 0.8; 499 months); 30-year +10 (t 1.2; 318). By era: about zero in 1962-1989, +13 and +23 in 1990-2003 (t 1.9 and 2.2) | 10-year +20 (t 3.9); 30-year +39 (t 3.8); TLT +39 at closes, +32 at fills; IEF +24, +21 | not confirmed by the pooled rule; present since 1990 and strong since 2003 |
| Q3, month-end loser bounce (signed spread) | +13 bps (t 0.9; 261 months); 1962-79 -20, 1980-89 +20, 1990-2003 +46 | +86 bps (t 3.9; 172 months) | not confirmed |

The yield series overstates the auction dip (-54 against -34 bps on TLT itself): at an auction
the newly sold bond replaces the old one in the constant-maturity series, which moves the yield
for a reason no holder earns. The ETF's own closes are the number to trust.

## Status (2026-11-18)

**Done:** ideation, four cards, train tests, post-hoc tables, the step 4 check, write-up,
`ideas.md`, `next-steps.md`. Held-out year unspent. Draft PR #33 (`wide-1` -> `carry-2`), not
merged.

**Doing:** nothing half-finished. No process running.

**Next (not started):** the three lanes listed at the top; `month-end-bonds` first.

## Added by wide-3 (2026-11-18): three new mechanisms, not in the list above

Written after wide-3's two picks (F2 `hedge-regime`, P2 `attention-peak`) had failed, before
any number on these three. Numbered W1-W3 so they extend the list; the multiple-testing
family is now 49 (46 + 3), and any test of one of them is read at p < 0.10 / 49 = 0.0020.
All three follow wide-1's sorting rule (hundreds of dated events, ETFs, a cause that is not
the price trend) and each has a built-in placebo period, because the mechanism did not exist
before a known date.

| # | Field x tool | Mechanism | Where the money would come from | Test plan | Built-in placebo | Prior |
|---|---|---|---|---|---|---|
| W1 `opex-pin` | physics (pinning in a potential well) x control (a damper that is removed on a known date) | Option dealers who are net long options hedge against moves (buy dips, sell rallies) and hold prices near large strikes into expiry; the hedging flow and the expiry itself fall on the third Friday of each month, known years ahead. Published for single stocks (Stivers and Sun 2013, as I remember: high returns in expiry week for stocks with much option activity) | Hold stocks in the expiry week, when the dampened, hedged market drifts up, with cash the trend rule leaves idle | Weekly harness, no new data: on the Friday before the third Friday, idle cash goes to the eligible stock ETFs for one week (Monday open to Monday open). Twin `tsmom12`. Event study of the expiry week's excess return by era. Other ETFs and indexes as out-of-universe sets | S&P 500 index 1962 to 1983-03 (no listed index options before the OEX began in March 1983) and the weak option volume of the 1980s-90s against the 2010s | 2% (the overlay only moves idle cash: even a real 20 bps a week adds about +0.02 Sharpe) |
| W2 `tax-drain` | hydraulics (a reservoir drained into another on known dates) | On federal tax dates (15 April, 15 June, 15 September, 15 December, 15 January) money moves from bank deposits into the Treasury's account at the Fed, draining bank reserves for days. Dealers' balance sheets tighten; repo rates spike (September 2019 is the famous case: a tax date plus coupon settlement) | Avoid stocks and long bonds for the three sessions after a tax date, or use idle cash after the drain has refilled | Dates are fixed by law (shifted for weekends): about 5 a year, ~160 since 1994. Event study on SPY, TLT, IEF, LQD returns over sessions D-1 .. D+3 against all other 5-session windows; the Treasury account level from FRED (`WTREGEN`) to size each drain. A rule only if the event study shows the sign in both halves | Before 2008 the Treasury kept most tax receipts in commercial-bank accounts (TT&L), so a tax date did not drain reserves: 1994-2007 should show nothing, 2008-2025 the effect | 2% |
| W3 `lunar` | astronomy x chronobiology (mood follows the lunar cycle) | Published in finance (Dichev and Janes 2003; Yuan, Zheng and Zhu 2006, 48 countries): returns in the 15 days around new moons beat those around full moons by a few percent a year. The proposed cause is mood and sleep, which is the weakest link | Hold stocks around new moons, with idle cash | Dates are astronomical and fixed. Event study on SPY, QQQ and the four indexes (1962+); the weekly harness with the overlay on Fridays within 7 days of a new moon | Every shift of the phase is a placebo: the new-moon window must beat the 28 other phase shifts, not just zero | 1% (no forced flow; most likely a data-mined anomaly) |

Which first: **W1 `opex-pin`**. It needs no new data, fits the weekly harness exactly (the
overlay starts and ends on Friday decisions), has ~380 events since 1994, and its placebo
(1962-1983) is already in the cache. W2 needs a careful reading of when the Treasury's account
moved to the Fed (2008 is my memory, to be checked) and is an event study first. W3 is written
down for completeness: it is the cleanest test of the "mood" class and the least likely to pay.

## Added by wide-4 (2026-11-18): five mechanisms from fields the list has not used

Written after `tax-drain` (W2) failed, before any number on these five. Numbered W4-W8 so
they extend the list; **the family is now 54 (46 + W1-W3 + W4-W8) and any test of one of them
is read at p < 0.10 / 54 = 0.00185.**

Fields already used, so excluded here: ecology, epidemiology, signal processing, control,
information theory, evolutionary game theory, statistical physics, queueing/inventory and
reliability, neuroscience, immunology (wide-1); physics of pinning, hydraulics, astronomy and
chronobiology (W1-W3); Hawkes self-excitation (the seismologists' ETAS model, run 1's
`hawkes-clustering`); Kelly and universal coding. New fields: **pharmacokinetics, seismology
(tidal triggering, not self-excitation), actuarial science, materials fatigue, metrology of
snapshot reporting.** Each entry passes wide-1's sorting rule (dated events, ETFs, a cause
that is not the price trend) unless it says otherwise.

| # | Field x tool | Mechanism in markets | Why it might survive costs on this book | Test plan and data | Prior |
|---|---|---|---|---|---|
| W4 `coupon-dose` | pharmacokinetics x scheduled dosing (a dose is absorbed into the compartment it came from within days; response rises with dose: dose-response curve) | Treasury coupons and maturing principal are paid on fixed days (the 15th and the month end). Holders of long bonds, index funds above all, must reinvest the cash in the same kind of bond, so a large net payment (coupons + principal minus new issues settling the same day) is a buy order of known size on a known date | ETF-tradable at 4 bps a round trip; ~270 mid-month payment days since TLT began (2002-07) with sizes that vary several-fold (the 10- and 30-year pay in Feb/May/Aug/Nov), so a dose-response slope has power that a pure calendar test lacks; idle cash goes to TLT, whose own drift is positive, not to stocks | Event study on payment days P on the 15th (month-end windows excluded: `month-end-bonds` was found there post hoc): TLT, IEF excess return over P .. P+3 regressed on the net dose. Dose from the Treasury's auction file (issue and maturity dates, amounts, coupon rates: fiscaldata `auctions_query`, keyless). Rule: idle cash into TLT for P .. P+3 when the net dose is positive; placebo the same on non-positive doses | 3% |
| W5 `tidal-trigger` | seismology x tidal triggering (a small periodic stress triggers ruptures only on faults already near failure; Coulomb failure function = background + periodic load) | The small, known calendar flows (tax-date drain, auctions, month-end rebalancing) move prices only when dealers are already near their capacity, i.e. when stress is high; in calm markets the same flow is absorbed | It would concentrate the flow trades into the minority of events that pay: fewer trades, the same edge | Re-cut the seen calendars by a stress state fixed before the event (TLT's 21-day volatility above its trailing one-year median, VIX likewise for stocks): excess return high-stress minus low-stress, per calendar. The calendars are seen, the split is not; data cached. Partial post hoc support from `tax-drain` (regime C), so it must be confirmed on a calendar not used to suggest it | 2% |
| W6 `payday-inflow` | actuarial science x a contribution annuity (defined-contribution plans invest a fixed share of each paycheck on the pay date) | 401(k) and IRA contributions arrive on paydays (semi-monthly: the 15th and the month end; bi-weekly Fridays) and are invested in target-date and index funds within a day or two: a forced buy of stocks mid-month | Hundreds of events, SPY at 4 bps; a placebo before auto-enrolment (the 2006 Pension Protection Act) and on the S&P 500 index 1962-1993 | Event study: SPY excess over sessions after the 15th in months without a tax date (Feb, Mar, May, Jul, Aug, Oct, Nov; the tax months collide with W2), before and after 2007. A rule only if the sign holds in both halves after 2007; idle cash into stocks has failed twice (`opex-pin`), so the prior is low | 1% |
| W7 `fatigue-damage` | materials science x Basquin S-N curve and Palmgren-Miner cumulative damage (each load cycle of amplitude S uses 1/N(S) of a part's life, N ~ S^-b; failure at damage 1) | Leveraged coin longs are worn down by oscillations, not only by one crash: damage = sum of (drawdown cycle amplitude / reference)^b over recent cycles (rainflow counting). When damage passes 1 the leveraged population has been liquidated; the forced sellers are gone and an uptrend resumes | It acts only inside `tsmom12`'s coin slots (adds back a slot after failure): few trades | Rainflow-count BTC and ETH daily cycles, b = 3 fixed (steel's typical exponent, not fitted); event study of returns after damage crosses 1. **Mostly collapses** into dip buying (`dip-rsi2`: real, small) and P4 (liquidation cascades, killed): listed for completeness | 1% |
| W8 `snapshot-shrink` | metrology x snapshot sampling (a quantity measured only at sample dates is managed at those dates: Goodhart's law as a sampling problem) | Non-US banks report Basel III leverage ratios on quarter-end snapshots (public disclosure from 2015), so they shrink repo and dealer balance sheets in the last days of each quarter; US repo rates spike at quarter ends; Treasury intermediation thins | Four dated events a year, a clean placebo (2003-2014, before disclosure, and the eight non-quarter month ends each year) | Event study: TLT's last four sessions of quarter-end months minus those of other months, 2015-2025 against 2003-2014. It sits on top of the month-end bond rally found post hoc on the same data, so it can only be a descriptive split | 1% |

### Choice (written before any number on W4-W8)

**W4 `coupon-dose` is picked.** Reasons, in order:

1. It is the only one of the five with a **dose that varies in size**, known in advance. A
   dose-response slope is a much stronger test than a calendar mean: an effect that rises with
   the dose is hard to get from a seasonal accident, and a placebo (non-positive doses) comes
   free.
2. It is a **forced flow** (index funds must stay at their duration; coupons arrive whether or
   not anyone wants them), which is the one class that left real traces in wide-1 (auction
   dip, month-end bond rally).
3. Its rule puts idle cash into **TLT**, the asset whose drift was positive in our period, not
   into stocks in a downtrend, which is what sank `opex-pin`.
4. It needs only public, keyless data (the Treasury's auction file, already used by wide-1 for
   dates) and it excludes the month-end windows, where the post hoc pattern was found.

Against it: refunding auctions settle on the same 15th (new supply, the opposite of a dose),
which is why the card uses the **net** dose; 30-year bonds were not issued 2001-2006; and the
gain on the book is capped by the idle cash (about a quarter of the book) times four sessions
a month. W5 is the most interesting but is built on calendars this repo has already looked
at; W6, W7, W8 have lower priors as written.

## Added by wide-5 (2026-11-18): two new mechanisms and a written choice rule

Written after `coupon-dose` (W4) failed, before any number on anything below. The W entries
left (W3, W5-W8) all carry priors of 1-2%, so two new ones were invented first, by
cross-pollinating queueing theory and control theory with the dose-response method wide-4
used. Numbered W9-W10 so they extend the list; **the family is now 56 (46 + W1-W10) and any
test of one of them is read at p < 0.10 / 56 = 0.00179.**

A lesson from another lane (ann-1, survey-2/3) shapes the rule: three published calendar
effects (`fomc-cycle`, `xtsmom`, the pre-FOMC drift) held in their papers' years and were zero
after publication. So a new pick should either be judged on years after its idea was formed,
or rest on a structural cause (a law, a contract, an index rule, a regulator's obligation)
rather than a habit or a mood.

Seen before writing this: the field list of the Treasury's auction file (fiscaldata
`auctions_query`, keyless), and for the new download (`<cache_root>/downloads/wide-5/`) only
its row count and, per year, how many rows have `primary_dealer_accepted` filled in (none
before 2008, all from 2009; 39 of 50 in 2008). No dealer share, amount, yield or price.

| # | Field x tool | Mechanism in markets | Why it might survive costs on this book | Test plan and data | Prior |
|---|---|---|---|---|---|
| W9 `dealer-backlog` | queueing theory x a server of last resort with a measured backlog (Grossman-Miller: a liquidity provider who absorbs an order imbalance is paid by the reversal that follows, and more the larger the imbalance) | Primary dealers are obliged by their agreement with the New York Fed to bid in every Treasury auction. When end investors stay away, dealers are left with a large share of the issue (published at 1 pm on auction day). They carry it at a concession and are paid by the price recovery as they distribute it over the next days. The larger the unexpected dealer share, the larger the recovery | The dose (dealer share minus its own recent norm) varies auction to auction and is public before the close, so the rule needs no forecast; ~270 auctions of 20- and 30-year bonds since 2008 for TLT, ~210 of 10-year notes for IEF; ETF fills at 4 bps; idle cash goes to TLT. wide-1 saw the average dip before auctions and the average path after; the dealer-share cut has never been computed | Event study: TLT open-to-open over the 5 sessions after each 20/30-year auction, regressed on the dealer-share surprise; IEF on 10-year auctions as a second calendar. Rule: idle cash into TLT for those 5 sessions when the surprise is positive; placebo on non-positive surprises. Data: the auction file with `primary_dealer_accepted` and `comp_accepted` (2008-07 on) | 3% |
| W10 `extension-dose` | control theory x feedforward on a known setpoint step (an index fund is a tracking controller; at each month end its setpoint, the index's maturity, steps up by an amount fixed by the index rules and known days ahead) | Bond index funds and benchmarked managers must match their index's duration at the month-end rebalance. The step ("index extension") is set by the issues that settled during the month and the bonds that age out of the maturity bucket. If the month-end bond rally (found post hoc by wide-1) is index buying, it must be larger in months with a larger extension | A structural cause written in index rules, with a dose computed from public auction data before the window opens; ~280 month ends since TLT began. The month-end mean was seen (wide-1, `month-end-bonds`); the extension cut has never been computed. The decisive comparison is high-extension months against low-extension months (each other's placebo), which the seen mean does not bias | Event study: TLT open-to-open over the last four sessions of the month (wide-1's window), regressed on the extension of a 20+ year bucket built from the auction file; IEF against a 7-10 year bucket. Rule: idle cash into TLT for those four sessions in months whose extension is above the median of the previous 24 months; placebo the months below | 3% |

### Choice rule (fixed before any number on W3, W5-W10)

Each untested W entry gets one point for each of:

1. **Structural cause**: the flow or constraint is fixed by a law, regulation, contract,
   index rule or obligation, not by a habit or mood.
2. **Unseen cut**: the statistic that decides the test has not been computed by any run in
   this repo.
3. **Dose**: the event's size varies and is known from public data at the decision, so a
   dose-response slope (and a free placebo) can be tested, not only a calendar mean.
4. **Power**: at least 200 events in the train period on ETFs at 4 bps.
5. **Post-sample**: at least 8 train years after the idea was first published or formed.
6. **Not a killed idea in other words** (wide-1's sorting rule).

The two highest scores are picked; ties are broken by the data already cached, then by the
prior.

| # | 1 cause | 2 unseen | 3 dose | 4 power | 5 post-sample | 6 not killed | Score |
|---|:-:|:-:|:-:|:-:|:-:|:-:|---:|
| W3 `lunar` (published 2003, 2006) | 0 | 1 | 0 | 1 | 1 | 1 | 4 |
| W5 `tidal-trigger` | 1 | 1 | 0 | 1 | 0 | 1 | 4 |
| W6 `payday-inflow` | 1 | 1 | 0 | 1 | 0 | 1 | 4 |
| W7 `fatigue-damage` | 0 | 1 | 1 | 0 | 0 | 0 | 2 |
| W8 `snapshot-shrink` | 1 | 1 | 0 | 0 | 0 | 1 | 3 |
| W9 `dealer-backlog` | 1 | 1 | 1 | 1 | 0 | 1 | 5 |
| W10 `extension-dose` | 1 | 1 | 1 | 1 | 0 | 1 | 5 |

**Picked: W9 `dealer-backlog` and W10 `extension-dose`** (5 each). Neither can be judged on
years after the idea was formed (both are formed today); both qualify through a structural
cause, as the lesson allows. W3 is the only entry with post-sample years, but its cause is
mood; it stays the cleanest cheap check of a published calendar effect if one is wanted. The
first test of the two is read at p < 0.00179, and so is the second (Bonferroni over the
family of 56, as wide-4 did).

Against W10, written now: its calendar (the last four sessions) is the one where wide-1 found
the bond rally by looking, so its rule's Sharpe against `tsmom12` is biased upward by a seen
mean. Its card therefore makes the high-against-low comparison (rule against its placebo) and
the dose slope the readings that matter.

## Added by wide-6 (2026-11-18): W11 closed by a gate, four new mechanisms for the queue

**W11 `critical-slowing`** (ecology/physics: rising lag-1 autocorrelation and variance before a
critical transition, Scheffer et al. 2009). Listed in `ideas.md` since run 1 as dead by
literature; wide-6 gave it an event-study gate on our six assets (rule pushed first) and it
fails: a year of rising AC1 adds nothing to the chance of a top-decile drawdown (t 1.4 to
2015, 0.1 after), and rising variance adds nothing once the level of volatility is known
(t -0.5, 1.8). Dead by the gate, no card. W3 `lunar` likewise failed its gate (SPY 2007-2025
+1.6 bps a day, t 0.4, rank 12 of 29 phase shifts). See `wide-6.md`.

**Family count, union of the wide and survey lines:** 63 before wide-6, 64 with W11, **68 with
W12-W15 below; 16 tested by a strategy, none passed. The next strategy test is read at
p < 0.10 / 68 = 0.00147.** (wide-5 said 56 and ann-1 said 61: each missed the other branch.)

The fields the run was pointed at are taken: SIR contagion between assets is P1
(`contagion-catchup`, tested dead) and P2 (`attention-peak`, tested dead); entropy of returns
before breaks is I1/F4 (gate family; `hurst-entropy-gate` parked); Hurst long memory is the
same parked gate, and hydraulics is W2. Four fields this list has not used instead:
**demography, anthropology of calendars, tax law, and catastrophe meteorology.** Each is
written as wide-5's choice rule wants it: a structural cause, a dose that should scale, and
years that could judge it which no run here has seen. None is tested; none has a number.
Each should go through an event-study gate first (ann-1, wide-6), and only a pass gets a
card.

| # | Field x tool | Mechanism in markets | Dose that should scale | Gate (event study first) and the years that can judge it | Prior |
|---|---|---|---|---|---|
| W12 `rmd-december` | demography x cohort flows on a Lexis diagram (a cohort crossing an age line on a known date) | US retirees must take required minimum distributions (RMDs) from IRAs and 401(k)s once past a legal age, and many take them in December. That is a sale of fund shares (stocks and bonds) of roughly the account divided by the life-expectancy divisor (about 4% at the starting age), every year, by law | The year's RMD total: IRA assets held by people past the RMD age (published yearly by the Investment Company Institute) times 1 / divisor. It grows with the baby-boom cohort. **Two zero-dose years by law**: RMDs were waived for 2009 and for 2020 (from memory: WRERA 2008, CARES Act 2020; check). The start age moved from 70.5 to 72 (2020) and 73 (2023) and moves to 75 in 2033, which thins the cohort entering in those years | SPY and TLT excess return over the last ten sessions of December (or the December sessions after the 15th), regressed on the dose with the two waiver years as zero; known collision: the turn-of-year and "Santa" calendar, so the decisive cut is waiver years against the rest, not the December mean. The waiver years are only two (weak); the start-age steps of 2033-2034 are the unseen years that can judge it | 1% |
| W13 `festival-gold` | anthropology of calendars x lunisolar date drift (a festival fixed in the lunar calendar walks through the solar months, about 11 days a year, then jumps back) | Physical gold buying in India peaks before Dhanteras/Diwali (new moon of the month Kartika, mid-October to mid-November) and in China before the Lunar New Year (21 January to 20 February). Jewellers and households buy weeks ahead; the buying is set by the festival, not by the price | Event time against calendar time: because the festival moves by up to a month from year to year, the same calendar window is sometimes 0 and sometimes 4 weeks before it. A festival effect must follow event time; a seasonal or tax effect follows calendar time. A second dose: India's monthly gold imports (Ministry of Commerce; keyless access not checked) | GLD (2004-11 on) and the gold price before it (`datahub-gold` in the cache; check its frequency) over the 15 sessions before each festival, regressed on event-time and calendar-month terms together. Festival dates are computable from the moon code wide-6 wrote (Diwali: the new moon near the October-November boundary; Lunar New Year: the second new moon after the winter solstice, with known exceptions; check against a published table). No run has cut gold by these dates; the unseen years are 2026 on | 2% |
| W14 `wash-sale-echo` | tax law x a refractory period (US wash-sale rule, IRC section 1091: a loss is disallowed if a substantially identical security is bought within 30 days before or after the sale) | Year-end tax-loss sellers of an ETF that is down for the year who want the exposure back must wait 31 days or hold a near-substitute. So the rebound of December's losers should come about a month after the selling peak (mid-January to early February), not on 2 January | The asset's loss for the year at the end of November (bigger loss, more harvesting) times how much of it sits in taxable accounts. **Built-in placebo across assets:** the rule covers securities, not spot coins (the IRS treats crypto as property; the extension proposed for digital assets was not law as of late 2025), so BTC and ETH can be sold and bought back at once and should show no delayed rebound, while spot-bitcoin ETF shares (2024 on) are securities and should | Excess return from the 31st to the 45th day after the third Friday of December, regressed on the November year-to-date loss, for the six assets plus the eight other ETFs of the protocol (about 30 years x 14 ETFs, of which perhaps 80 asset-years with a loss: weak). The unseen years: any year after crypto is brought under the rule (then the coin placebo must turn), and 2026 on for ETFs | 1% |
| W15 `cat-claims` | catastrophe meteorology x a loss-to-liquidation chain (a landfall's insured loss must be paid in cash within months, and property insurers hold mostly bonds) | After a major US hurricane landfall, property and casualty insurers and reinsurers sell liquid bonds to pay claims; the selling is forced and sized by the loss, not by a view on rates | The insured-loss estimate of the event (published by catastrophe modelers within days; the National Hurricane Center's best-track file, HURDAT2, gives date, place and intensity keyless; NOAA's billion-dollar disaster list was discontinued in 2025, check) | TLT and LQD excess return over the 20 sessions after landfall, regressed on the landfall's intensity or loss estimate; the zero-dose placebo is landfalls of weak storms and the same calendar weeks in years without one. About 2-5 major landfalls a year since 2002, so the gate is weak; the unseen years are the 2026 season on. Against it: insurers' bond sales are small next to the Treasury market, so LQD (corporate bonds, thinner) should show it more than TLT | 1% |

Ranking for the next lane, by wide-5's six points (cause, unseen cut, dose, power,
post-sample, not killed): W12, W14, W15 score 4 (law or contract, unseen, dose, not killed;
none has 200 events or post-sample train years); W13 scores 3 (festival buying is custom, not
law). Tie broken by data already cached: **W14 `wash-sale-echo` first**, as a gate: it needs
only the cached ETF and coin prices, and its coin placebo is built in. W13 next if a gold
question is wanted: its event-time against calendar-time cut separates a festival from a
season, which a plain calendar mean cannot.

## Added by wide-7 (2026-11-18): W12-W14 closed by gates, two new mechanisms

Three of wide-6's four queued entries went through event-study gates, rules pushed first (see
`wide-7.md`); all three fail and are dead by the gate, with no card:

- **W14 `wash-sale-echo`**: ETF return over days 31-45 after the third Friday of December on
  the November loss: -0.003 (t -0.07) in tax years 1994-2011, +0.023 (t 0.43) in 2012-2024;
  the coin placebo's slope (+0.049) is above the ETFs' (+0.006).
- **W13 `festival-gold`**: GLD over the 15 sessions before Dhanteras and the Lunar New Year,
  against the same month's mean: -1.9 bps a day (t -0.30), rank 10 of 15 weekly shifts.
  Baur's autumn months (September, November) turned from the best to among the worst after
  2010.
- **W12 `rmd-december`**: SPY's last ten December sessions in the RMD waiver years (2009,
  2020) against the others, excess of the year's drift: -0.06% (permutation p 0.51).

W15 `cat-claims` stays in the queue. Two new entries from fields the list has not used
(heliophysics, software release engineering), each needing a gate first:

| # | Field x tool | Mechanism in markets | Dose that should scale | Gate and the years that can judge it | Prior |
|---|---|---|---|---|---|
| W16 `geomagnetic-storm` | heliophysics x the Kp/Ap geomagnetic index | Lower stock returns in the days after severe geomagnetic storms, through mood (Krivelyova and Robotti 2003, from memory; check) | Daily Ap (G1-G5); severe storms must matter more than minor ones | SPY and the S&P 500 index over the six sessions after storm days on Ap, against calm weeks. Post-sample train years 2003-2025 (solar cycles 24 and 25), so gate-able now; 2026 on after that | 1% |
| W17 `fork-premium` | software release engineering x releases with a fixed activation block | A risk premium into scheduled Ethereum upgrades and a fall after them, larger for upgrades that change supply or consensus | Upgrade scope fixed from its specification before the date (supply/consensus change or not; number of included proposals) | ETH minus BTC over 10 days before and after about 18 upgrades since 2016, on scope; weak. Unseen: Fusaka (2025-12) and 2026 on | 1% |

**Family count: 70 mechanisms (68 + W16, W17), 16 tested by a strategy, none passed. The next
strategy test is read at p < 0.10 / 70 = 0.00143.**

## Added by wide-8 (2026-11-18): W16 and W15 closed by gates, two new mechanisms

Both gates had their rule, script and tests pushed before any number (see `wide-8.md`); both
fail and are dead by the gate, with no card:

- **W16 `geomagnetic-storm`**: SPY 2003-2025, six sessions after a severe storm (daily Ap >=
  100, GFZ Potsdam, keyless, CC BY 4.0): +18.2 bps a day over calm sessions (t +2.46, the wrong
  sign), minor storms +0.8; rank 29 of 31 shifted Ap calendars. In the paper's years (GSPC
  1950-2002) -4.4 bps a day (t -1.05).
- **W15 `cat-claims`**: 104 US landfalls 2002-2025 (NOAA HURDAT2, keyless), LQD minus half of
  TLT over 20 sessions on the Saffir-Simpson category: +0.01 points per category (t 0.09);
  halves -0.44 and +0.13; rank 8 of 23 year-shifted calendars.

Also: the turn-of-year ETF loser rebound (a seen cell of W14's gate) is pre-registered as a
forward test for the 2026/27 turn (`research/forward/proposed-wide8.jsonl`, proposed, not
frozen), with an empirical null from 153 placebo windows (sd of t 2.18).

Two new entries from fields the list has not used (sport sociology, oceanography), each
needing a gate first:

| # | Field x tool | Mechanism in markets | Dose that should scale | Gate and the years that can judge it | Prior |
|---|---|---|---|---|---|
| W18 `elimination-mood` | sport sociology x national mood shocks from knockout matches | Next-day index fall in a country whose team is knocked out of the World Cup (Edmans, Garcia, Norli 2007, from memory) | Round of the elimination x the country's football weight; wins as the placebo | DAX, FTSE 100, Nikkei next day after World Cup and Euro eliminations, against the same weekday without a match; post-sample 2006-2024 (about 25 events, weak); unseen: 2026 World Cup (held-out year) and 2028 on | 2% |
| W19 `enso-commodity` | oceanography x the Oceanic Nino Index | El Nino raises non-fuel commodity prices over the next year through crop yields (Cashin, Mohaddes, Raissi 2017, from memory) | ONI level (strong events more than weak; La Nina the mirror) | DBC and commodity ETFs' 6-month return on lagged ONI, placebo ONI shifted by whole years; post-sample 2014-2025 (three or four episodes, weak); unseen: 2026-27 on | 2% |

**Family count: 72 mechanisms (70 + W18, W19), 16 tested by a strategy, none passed. The next
strategy test is read at p < 0.10 / 72 = 0.00139.**

## Added by wide-9 (2026-11-19): W19 and W17 closed by gates, a gate-null method

Both gates had their rule, script and tests pushed before any number (see `wide-9.md`) and
were judged by rank among 40 placebo calendars (`gate-null.md`); both fail and are dead by the
gate, with no card:

- **W19 `enso-commodity`**: DBC's six-month return on the lagged ONI (NOAA CPC, keyless),
  2014-2025: -2.5 points per degree (t -0.92), rank 32 of 41 year-shifted ONI calendars; in
  the paper's years +1.8 (t 0.44). DBC is mostly energy; the non-fuel channel is untested.
- **W17 `fork-premium`**: ETH minus BTC into and after 15 mainnet upgrades 2016-2025: premium
  +0.70% (t 0.23), rank 19 of 41; no run-up (-0.06%), no sell-off (-0.76%).

No new mechanisms in this run. **Family count: 72 mechanisms, 16 tested by a strategy, none
passed. The next strategy test is read at p < 0.10 / 72 = 0.00139.** Gates so far: 10, all
failed.

## Added by wide-10 (2026-11-19): two mechanisms from unused fields, by a written score

Picked by a scoring rule fixed before any data look (structural cause, a dose scored double,
post-sample years, power, unseen cut, not killed; six candidates scored, see `wide-10.md`
step 1). Each needs a gate first (`gate-null.md`).

| # | Field x tool | Mechanism in markets | Dose that should scale | Gate and the years that can judge it | Prior |
|---|---|---|---|---|---|
| W20 `fed-purchase-flow` | procurement (reverse-auction) theory x a buyer with a published shopping list | On days the Fed buys Treasuries in an operation, dealers sell it the purchased sector and that sector's price rises the same day (flow effect; D'Amico and King 2013, Song and Zhu 2018, Kandrac and Schlusche 2013, the last finding it small after the early programmes) | Par accepted that day in bonds of 20+ years remaining maturity (TLT's sector), from the NY Fed's per-CUSIP results (keyless API) | TLT open-to-close on the day's log dose, placebo = the dose calendar shifted by trading days; judging years 2014-01 .. 2025-11 (after every cited sample); unseen: any future purchase programme | 3% |
| W21 `stablecoin-mint` | monetary history of currency boards / narrow banks x issue only against a deposit | A stablecoin is minted only when dollars are wired to the issuer, so net issuance is fresh cash on its way to buy coins; coin prices should rise over the following week (Griffin and Shams 2020 on Tether, March 2017 .. March 2018) | Weekly log change of total USD stablecoin supply (DefiLlama, keyless) | BTC and ETH next-week return on last week's issuance, own last-week return as control, placebo = issuance shifted by weeks; judging years 2018-04 .. 2025-11 (7.6 years: one short of the post-sample point) | 2% |

**Family count: union of the wide and survey lines 78 mechanisms (survey-7's 76 + W20, W21),
18 tested by a strategy, none passed. The next strategy test is read at p < 0.10 / 78 =
0.00128.** (The survey-4 entries `ts-carry`, `halloween`, `seasonal-20y`, `ts-value` are
counted in the 76 but listed on their own branch.)

**Closed by wide-10's gates (2026-11-19, `wide-10.md`; rules pushed first, 40 placebos each):**
W20 `fed-purchase-flow`: TLT open-to-close +3.3 bps per unit of ln(1 + $bn of 20+ year
purchases), t 0.37, rank 11 of 41 (2014-2025, 224 purchase days); in the papers' years -8.5
(t -1.55). W21 `stablecoin-mint`: next-week BTC/ETH +0.16 per unit of weekly issuance, t 1.06,
rank 17 of 41 (339 weeks); issuance follows prices (same-week t 2.92). Both dead, no card.
Count unchanged: 78 mechanisms, 18 tested, none passed; gates 13, all failed.
