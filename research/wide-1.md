# Wide 1: new hypotheses from other fields

Research run wide-1, started 2026-11-17. Branch `wide-1` (from `carry-2`). Research only: fake
money, public data, no change to the gym, the daily runner or the live strategies.

Question: after 14 runs nothing beats the 12-month trend rule (`tsmom12`) on the six assets. Do
other fields (ecology, epidemiology, signal processing, control, information theory, game
theory, physics, queueing, neuroscience, immunology) suggest a mechanism we have not tested,
whose edge would come from somewhere other than trend?

## In plain words (results)

Not written yet. Step 1 (below) was written and pushed before any number.

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

## Step 2. Cards

To come: `cards/auction-concession.md`, `cards/rebalance-pressure.md`,
`cards/contagion-catchup.md`, `cards/vol-echo.md`, committed and pushed before any test.
