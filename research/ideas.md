# Ideas

One line per idea. Status: `new` (written down), `testing` (has a card, being tested),
`live` (forward paper), `dead` (and why), `parked` (not testable here yet, and why). Dead ideas
stay: they count as tries. "Dead (literature)" means the survey killed it and we did not spend a
backtest on it; "dead (tested)" means our own test killed it (see `results/`).

## Cards tested in run 1 (all nine failed their pre-set bar; none used the held-out year)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| kelly-shrunk | Kelly / information theory | dead (tested) | [card](cards/kelly-shrunk.md) | Equals inverse-vol (+0.01 Sharpe): the no-leverage cap removes the Kelly scale. On high-volatility coins the scale halves drawdown at equal growth: see `vol-target`. [result](results/kelly-shrunk.md) |
| hmm-regime | Regime models | dead (tested) | [card](cards/hmm-regime.md) | Beats a volatility threshold (+0.14, p = 0.03) but equals equal weight (0.89 vs 0.88) and loses to the 200-day average (1.01); sat through the dot-com bust. [result](results/hmm-regime.md) |
| fracdiff-momentum | Fractional differentiation | dead (tested) | [card](cards/fracdiff-momentum.md) | Worse than 12-month momentum everywhere (-0.25 Sharpe, 3x turnover): it is a fast trend rule. [result](results/fracdiff-momentum.md) |
| drawdown-control | Optimal stopping / control | dead (tested) | [card](cards/drawdown-control.md) | Same as the 200-day switch (+0.07, p = 0.14; mixed out of universe). A smoother trend rule, not a better one. [result](results/drawdown-control.md) |
| universal-portfolio | Information theory | dead (tested) | [card](cards/universal-portfolio.md) | Indistinguishable from the constant mix it starts from; 30 years is too short for its guarantee. [result](results/universal-portfolio.md) |
| absorption-ratio | Random matrix theory / PCA | dead (tested) | [card](cards/absorption-ratio.md) | Worked inside the paper's sample (0.97 vs 0.56 to 2010), behind its plain twin ever since (1.13 vs 1.44); missed 2022. [result](results/absorption-ratio.md) |
| hawkes-clustering | Hawkes processes | dead (tested) | [card](cards/hawkes-clustering.md) | Self-excitation at daily bars is weak; the rule is equal weight minus a few days (0.87 vs 0.88), 7x the turnover. [result](results/hawkes-clustering.md) |
| month-end-liquidity | Calendar / microstructure | dead (tested) | [card](cards/month-end-liquidity.md) | Real in old data (S&P 1962-93 t = 4.0, FTSE 4.2, Nikkei 3.1), faded since 2014, never in TLT; in-or-out loses to a constant one-third holding on Sharpe. [result](results/month-end-liquidity.md) |
| dip-rsi2 | Short-term reversal | dead (tested) | [card](cards/dip-rsi2.md) | Bounce is real on SPY (21.6 vs 3.9 bps a day, t = 2.5), halved since publication, weak on 7 other markets, and only 5% exposure: +2.3% a year. [result](results/dip-rsi2.md) |

## Cards for run 2 (written after run 1; each card says what had been seen)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| vol-target | Volatility targeting | dead (tested) | [card](cards/vol-target.md) | Same Sharpe as equal weight (0.87 vs 0.88); cuts volatility, and on coins halves it at equal growth. A risk dial, not an edge. No help in slow bear markets. [result](results/vol-target.md) |
| ensemble-tsmom | Trend | dead (tested) | [card](cards/ensemble-tsmom.md) | +0.05 over tsmom12 (p = 0.21), right sign in all three other sets, 2x turnover. Indistinguishable from 12-month momentum. [result](results/ensemble-tsmom.md) |
| trend-vol | Trend + volatility | failed bar; paper candidate on drawdown only | [card](cards/trend-vol.md) | Same Sharpe as tsmom12 (1.03 vs 1.05) but worst loss 26% vs 37% (equal weight 69%), growth 13.3% vs 17.8% a year. A risk choice, not an edge. [result](results/trend-vol.md) |

## Cards for run 3

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| trend-to-safe | Trend / regime allocation | dead (tested) | [card](cards/trend-to-safe.md) | Equals tsmom12 on the six assets (1.02 vs 1.05), behind in 2022. Helped on other ETFs with mid-term bonds as the safe asset (0.68 vs 0.60, p = 0.06): a hint for a universe with IEF. [result](results/trend-to-safe.md) |
| crypto-slot-size | Allocation | described (no pass bar) | [card](cards/crypto-slot-size.md) | Sharpe is flat from 5% to 1/6 per coin (1.34-1.39); size sets growth and worst loss (5%: +18%/yr, -31%; 1/6: +35%/yr, -47%). The owner's biggest risk setting. [result](results/crypto-slot-size.md) |

## Card for research run 3: the risk map (a description, not an idea; held-out year unused)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| risk-map | Allocation | described (no pass bar) | [card](cards/risk-map.md) | 20 settings of the run 1-2 rules: hold, trend, trend with a 60/40/20% volatility cap; crypto at 0%, 5%, 10% or a sixth per coin. Since 2003 growth runs from 8% to 25% a year and the worst drop from 12% to 47%, in one rising band. Presets for the owner in [risk-map.md](risk-map.md). [result](results/risk-map.md) |

## Cards for research run 2: machine learning (all seven failed; none used the held-out year)

The first three were written before any model was fitted; each later card says what had been
seen. Sharpe on the six assets, 1994-2025: `tsmom12` 1.05, equal weight 0.88.

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| ml-linear | Machine learning | dead (tested) | [card](cards/ml-linear.md) | Logistic / ridge regression on 15 features. Found nothing and became equal weight (0.84-0.89); AUC 0.494. [result](results/ml-linear.md) |
| ml-gbm | Machine learning | dead (tested) | [card](cards/ml-gbm.md) | Gradient boosting, 9 settings: 0.72-0.86, 3.5x the turnover of the trend rule, AUC 0.50-0.51. Did not beat the linear model. [result](results/ml-gbm.md) |
| ml-filter | Machine learning | dead (tested) | [card](cards/ml-filter.md) | A model grading `tsmom12`'s trades (meta-labelling): 0.73-0.94, worse than the rule alone in all three forms. [result](results/ml-filter.md) |
| ml-sizing | Machine learning | dead (tested) | [card](cards/ml-sizing.md) | Position follows the forecast (two sharper rules): 0.68-0.82. Following a forecast with no skill more closely is worse. [result](results/ml-sizing.md) |
| ml-payoff | Machine learning | dead (tested) | [card](cards/ml-payoff.md) | Trained on payoff (months weighted by size) instead of direction: 0.67-0.77; size-weighted hit rate 52-54% against 60% for "always up". [result](results/ml-payoff.md) |
| ml-pooled | Machine learning | dead (tested) | [card](cards/ml-pooled.md) | Same models trained on 33 markets (5x the rows): AUC 0.50, 0.68-0.92. "Too little data" is not the reason. [result](results/ml-pooled.md) |
| ml-weekly | Machine learning | dead (tested) | [card](cards/ml-weekly.md) | Same models, 7-day labels instead of 28 (four times the bets): AUC 0.50-0.51, 0.82-0.89. [result](results/ml-weekly.md) |

## Plain twins and benchmarks (baselines, see `results/baselines.md`)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| sma200 | Trend | baseline | protocol.md | 1994-2025 Sharpe 1.01 vs 0.88 equal weight (p = 0.17); halves drawdowns. M1 lane owns the live version |
| tsmom12 | Trend | baseline | protocol.md | 1.05 vs 0.88 (p = 0.08); the strongest plain rule on the six assets, weaker out of universe |
| inverse-vol | Risk parity, unlevered | baseline | protocol.md | 0.85: no better than equal weight on Sharpe; lower volatility |
| vol-calm | Volatility switch | baseline | protocol.md | 0.74: worse than equal weight. Stepping aside when volatility is high misses the rebounds |

## Not tested: killed or parked by the survey

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| tda-landscape | Topological data analysis | dead (literature) | - | Landscape norm is proportional to variance; the one controlled comparison finds nothing beyond mean correlation (survey part 6, C) |
| transfer-entropy | Information theory | dead (literature) | - | Descriptive only; crypto and ETF bars close at different times, so a daily lead is not tradable at next open (part 6, D) |
| critical-slowing | Ecology (early warning) | dead (literature) | - | Careful tests reject rising autocorrelation before crashes; the surviving part is rising variance = volatility targeting (part 6, F) |
| changepoint-momentum | Change-point detection | dead (literature) | - | Wood, Roberts, Zohren: edge over plain trend gone above about 2 bps a trade (part 4) |
| crypto-daily-reversal | Short-term reversal | dead (literature) | - | Not real in large coins even before our 60 bps round trip (part 3, A) |
| pre-fomc-drift | Calendar | dead (literature) | - | Gone after 2015; window does not fit next-open fills (part 3, E4) |
| ou-optimal-entry | Optimal stopping | dead (literature) | - | Needs a mean-reverting spread; long-only we cannot trade one (part 4) |
| return-forecast-foundation-model | Deep learning | dead (literature) | - | Chronos/TimesFM: negative R-squared against a zero forecast on daily returns (part 5). Do not spend the GPU on raw-return forecasting in M3 |
| llm-trading-agent | LLM | parked | - | Backtests before the model's training cutoff are contaminated; only forward paper scoring counts (part 5). Fits the M3 "research desk" as designed |
| lppls-bubble | Econophysics | parked | - | Three or four crypto bubbles cannot validate a warning signal (part 6, E) |
| hurst-entropy-gate | Econophysics / information theory | parked | - | Time-varying efficiency is documented, exploiting it is not; about five independent readings in ten years (part 6, D-E) |
| signature-leadlag | Path signatures | parked | - | No daily out-of-sample evidence; level 2 is lead-lag areas, which hit the non-synchronous-close problem; level 3+ overfits (part 6, B) |
| halloween | Calendar | parked | - | One observation a year: cannot be confirmed or rejected in our lifetime (part 3, E5) |
| crypto-carry | Carry | parked | - | Real, but needs perpetual futures; the gym has spot only (part 3, C3) |

## New (not yet carded; candidates for the next run)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| ensemble-tsmom | Trend | new | - | Weight = share of 1/3/6/12-month returns that are positive (part 1) |
| turbulence | Statistics | new | - | Mahalanobis distance of the six returns; test only against a volatility trigger (part 4) |
| vol-shift | Volatility | new | - | Risk assets to cash when SPY's 20-day volatility jumps 1 sd above its 1-year norm. Was the plain twin of absorption-ratio and beat equal weight there (1.17 vs 1.04, not significant). Needs its own card |

## Cards for run macro-1: macro phases (all six failed their bar; none used the held-out year)

Written before any test (`protocol.md` "Macro tests"). Sharpe on the six assets, 1994-2025 /
2003-2025: `tsmom12` 1.05 / 1.20. Summary: [macro-1.md](macro-1.md).

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| fed-hiking | Macro / monetary policy | dead (tested) | [card](cards/fed-hiking.md) | Out while the Fed hikes: 1.03 / 1.09. Helped on the S&P 500 1962-1993 (+0.27, p = 0.06), the inflation decades; not since. [result](results/fed-hiking.md) |
| real-rate | Macro / monetary policy | dead (tested) | [card](cards/real-rate.md) | Out while the real policy rate rises a point a year: 0.87 / 1.05. Too late. [result](results/real-rate.md) |
| yield-curve | Macro / term structure | dead (tested) | [card](cards/yield-curve.md) | A year out after an inversion: 1.13 / 1.17; the gain is the dot-com bust and a lucky covid call; wrong sign out of universe. [result](results/yield-curve.md) |
| liquidity | Macro / money supply | dead (tested) | [card](cards/liquidity.md) | Real M2 below zero: 0.95 / 1.11. Fed balance sheet shrinking: 0.95 / 1.09. [result](results/liquidity.md) |
| credit-spread | Macro / credit | dead (tested) | [card](cards/credit-spread.md) | Baa spread half a point above its yearly low: 0.99 / 1.06. No earlier than the price trend. [result](results/credit-spread.md) |
| halving | Crypto cycle | failed bar; not believed | [card](cards/halving.md) | Coins out 18-30 months after a halving: 1.20 / 1.42, but three winters, a window taken from folklore that saw them, and gone when moved six months. [result](results/halving.md), [shifted](results/halving-shift.md) |

## Run rl-1: reinforcement learning (all five failed their bar; none used the held-out year)

Plan and bar in [rl-1.md](rl-1.md), fixed before training. Sharpe on the six assets, out of
sample 2000-01-07 to 2025-11-09 / since 2003: `tsmom12` 0.99 / 1.19. Ensemble of ten seeds.
Tables: [results/rl-1.md](results/rl-1.md).

| Idea | Family | Status | Plan | Result |
|---|---|---|---|---|
| ppo-lin | RL, linear policy | dead | [rl-1.md](rl-1.md) | 0.63 / 0.75, worst loss 77%; holds a third in coins, overtrades. |
| ppo-mlp | RL, small network | dead | [rl-1.md](rl-1.md) | 0.66 / 0.80, worst loss 80%; 1.15 in sample, 0.63 out. |
| ppo-mlp-dd | RL, drawdown penalty | dead | [rl-1.md](rl-1.md) | 0.57 / 0.76, worst loss 60%; sits in cash, no smarter. |
| ppo-mlp-px | RL, prices only | dead | [rl-1.md](rl-1.md) | 0.71 / 0.81, worst loss 82%; macro inputs did not help. |
| es-lin | Evolution strategy (sanity check) | dead | [rl-1.md](rl-1.md) | 0.57 / 0.72, worst loss 87%; a different optimiser, the same place. |

### Short side on perpetuals (short-1, 2026-11-13)

Sharpe on Binance USDT perps, 2020-2025, 10 bps a side plus funding. Twin: `tsmom12` long-only spot, 30 bps.

| Idea | Kind | Status | Card | Reason |
|---|---|---|---|---|
| tsmom12-ls | Trend, short in downtrends | dead | [short-1.md](short-1.md) | 0.73 vs 1.03 (30 coins), 0.76 vs 1.19 (BTC/ETH); shorts sit through rallies. |
| ls-low_vol, ls-size, ls-turnover, ls-combo | Dollar-neutral relative | dead | [short-1.md](short-1.md) | Sharpe -0.3 to -0.6: short legs of wild coins lose 43-48% a year. |
| ls-trend | Cross-sectional 12-1 | dead | [short-1.md](short-1.md) | 0.24, negative 2022-25. |
| ls-rev_1 | Daily reversal | dead | [short-1.md](short-1.md) | -1.97; 483x turnover. |
| ls-premium, ls-funding | Carry: short the dearest perps | parked | [short-1.md](short-1.md) | 0.83 / 0.78; blend 1.25 vs 1.03 at 10 bps, gone at 30 bps. Held-out year unspent. |

### Run wide-1: hypotheses from other fields (2026-11-17)

Ideation, field by field, in [wide-1.md](wide-1.md) (46 mechanisms; the 33 killed there collapse
into ideas already in this file and are not repeated here). Four got a card; all four failed
their pre-set bar; none used the held-out year. Sharpe on the six assets: `tsmom12` 1.05.

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| auction-concession | Queueing / inventory theory | failed bar; faint lead on TLT alone | [card](cards/auction-concession.md) | TLT out for the five sessions ending with a 20/30-year Treasury auction: book +0.01 (p = 0.14); TLT alone 0.50 vs 0.33 (p = 0.05), mostly 2020-25; IEF with 7/10-year auctions 0.26 vs 0.55 (7-year auctions sit in the month-end bond rally). [result](results/auction-concession.md) |
| rebalance-pressure | Control theory | dead (tested) | [card](cards/rebalance-pressure.md) | Halve the month's stock/bond leader in the last five sessions: book -0.005 (p = 0.67). The raw spread has the predicted sign (+38 bps a month, t = 1.7; +56 before 2014, +21 since): it is the loser rising, which a long-only trend book mostly cannot hold. [result](results/rebalance-pressure.md) |
| contagion-catchup | Epidemiology / graph diffusion | dead (tested) | [card](cards/contagion-catchup.md) | 21 ETFs, hold those whose relatives moved and which did not: 0.50 vs 0.60 for the trend rule (coins 0.38 vs 0.74). Relatives' moves do not spill over (IC -0.015); what remains is plain one-week reversal (IC +0.03, t = 2.9), which does not pay. [result](results/contagion-catchup.md) |
| vol-echo | Signal processing / control theory | dead (tested) | [card](cards/vol-echo.md) | Hold stocks when a shock leaves the 21-day volatility window: SPY 0.25 vs 0.63 at equal exposure; the 1962-1993 placebo shows the same small excess return. [result](results/vol-echo.md) |
| trend-age | Queueing / reliability theory (hazard rate) | dead (tested) | [card](cards/trend-age.md) | Hold a `tsmom12` slot only once the signal has been on for four Fridays (wide-1's Q5, picked from its 42 uncarded mechanisms): 0.99 vs 1.05 (difference -0.06, 90% range -0.11 to -0.01), behind in 5 of 5 eras; coins -0.17. The hazard is front-loaded as claimed (21% of on-spells end in week one, 1.5% a week after week four), but the skipped whipsaws cost less than the three missed weeks of the trends that last. [result](results/trend-age.md), [write-up](wide-2.md) |
| patch-leaving | Behavioural ecology (marginal value theorem) | dead (tested) | [card](cards/patch-leaving.md) | Keep `tsmom12`'s exposure but hold only the in-trend assets whose risk-scaled 12-month return is at least the average (wide-1's E6, second pick of its 42): 0.85 vs 1.05 (difference -0.19, 90% range -0.36 to -0.02), fails all five bars; drawdown 53% vs 37%, turnover 9.7 vs 2.7, two assets held instead of three. ETFs -0.06, coins -0.39, indexes -0.06. [result](results/patch-leaving.md), [write-up](wide-2.md) |
| crowded-trend | Evolutionary game theory (frequency-dependent fitness) | dead (tested) | [card](cards/crowded-trend.md) | Halve `tsmom12`'s book when at least three assets are eligible and all are in trend (wide-1's G2, third pick of its 42; acts on 27% of Fridays): 0.98 vs 1.05 (difference -0.07, 90% range -0.16 to +0.03), ahead in 1 of 5 eras. Drawdown 29% vs 37% and the covid crash -8% vs -22%, but 3 points less return a year. ETFs -0.12, coins +0.05, indexes -0.01. [result](results/crowded-trend.md), [write-up](wide-2.md) |
| hedge-regime | Statistical physics (order parameter) | dead (tested) | [card](cards/hedge-regime.md) | Hold TLT out of trend while its one-year correlation with stocks is below zero (wide-1's F2, wide-3's first pick): 1.05 vs 1.05 (difference +0.003, p 0.39); other ETFs (IEF, LQD) -0.006. The sign was below zero on 81% of Fridays and turned positive only in 2023; the 267 added TLT weeks earned +1.2 bps a week (t 0.1); the slow window kept TLT in the 2022 crash (-17% vs -13%). [result](results/hedge-regime.md), [write-up](wide-3.md) |
| attention-peak | Epidemiology (SIR on attention) | dead (tested) | [card](cards/attention-peak.md) | Drop a coin's slot once its English-Wikipedia views have surged (28-day mean >= 3x the yearly median) and turned down from their peak (wide-1's P2, wide-3's second pick): 1.02 vs 1.05 (difference -0.03, p 0.74), behind in both eras it acts in; other coins 0.33 vs 0.54. It caught the 2017-12 BTC top (-47% while out) but left ETH in Jan-Apr 2021 (+109%) and missed the 2021-11 top. [result](results/attention-peak.md), [write-up](wide-3.md) |
| opex-pin | Physics (pinning) x control (a damper removed on a known date) | dead (tested) | [card](cards/opex-pin.md) | Idle cash into stocks for the option-expiry week (wide-3's new W1): 1.01 vs 1.05 (difference -0.04), fails 4 of 6 bars, behind its own placebo week (1.03). Event study: SPY expiry week minus the average week -0.3 bps (t -0.02, 381 weeks), negative since 2017; S&P 500 index 1983-93 +19 bps (t 1.0) against 0 before listed index options. [result](results/opex-pin.md), [write-up](wide-3.md) |
| stablecoin-resource | Ecology (consumer-resource) | parked | - | Two cycles, two coins: cannot be validated (wide-1, E1) |
| attention-sir | Epidemiology | tested as `attention-peak` | - | Three manias; Wikipedia page views are free from 2015-07 (wide-1, P2). Tested by wide-3 as `attention-peak`: dead |
| validator-queue | Queueing theory | parked | - | Ethereum exit queue; data from 2023-04, one coin (wide-1, Q4) |
| token-unlocks | Ecology (supply pulse) | parked | - | Needs paid data (price not checked, nothing bought); small coins only (wide-1, Q6) |
| month-end-bonds | Calendar / index flows | new | - | Found post hoc in wide-1, not tested: TLT +39 bps and IEF +24 bps in the last four sessions of the month, 2003-2025 (t 4.3, 5.4; +32 and +21 at next-open fills), both halves alike; yields before 2003: nothing to 1989, +13 to +23 bps in 1990-2003 (t ~2). Needs its own card; clean data left: LQD, TLT's first year, the held-out year. [tables](results/wide-1-yields.md) |
| month-end-stock-bounce | Calendar / rebalancing | new | - | Found post hoc in wide-1: stocks rose in the last five sessions after trailing bonds by 2% in the month (+182 bps, t 4.0, 2003-2025; unseen 1962-2003 +43 bps, t 1.7). Not confirmed on unseen data; needs a mid-month placebo before a card (it may be plain dip buying). [tables](results/wide-1-yields.md) |
| volume-screen | Inputs | new | - | The six assets' own volume has never been screened (all 15 ML features are from closes, info-1's 23 inputs are outside data). One IC table by info-1's method |
| tax-drain | Hydraulics (reserve drain on tax dates) | dead (tested); faint trace | [card](cards/tax-drain.md) | wide-3's W2, tested by wide-4. Fact checked first (NY Fed, Santoro 2012): tax receipts stayed in bank TT&L accounts until late 2008, then went to the Fed's TGA. Rule: SPY, QQQ, TLT out for sessions D-1 .. D+3 of each tax date from 2008-12-16: 1.03 vs 1.05 (difference -0.016, p 0.88), fails 4 of 6 bars. The drain is real (TGA +88 $bn over D-2 .. D+1 since 2008, t 13.7; +1.3 $bn before). Prices: every asset's excess is negative in the TGA era and largest while the Fed shrank reserves (SPY -62 bps, t -1.3, 27 dates; IEF -16 bps, t -2.1, 83 dates), about zero before 2008; not supported by the card's reading (SPY t <= -2). [result](results/tax-drain.md), [write-up](wide-4.md) |
| lunar | Astronomy x chronobiology | new | - | wide-3's W3: returns around new moons beat those around full moons (Dichev and Janes 2003). Every phase shift is a placebo. Lowest prior of the three; plan in `wide-1.md`, last section |
