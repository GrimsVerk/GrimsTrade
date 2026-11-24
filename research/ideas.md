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
| ensemble-tsmom | Trend | dead (tested) | [card](cards/ensemble-tsmom.md) | +0.05 over tsmom12 (p = 0.21), right sign in all three other sets, 2x turnover. Indistinguishable from 12-month momentum. [result](results/ensemble-tsmom.md) pooled-1 (#142, 41 markets out of universe): +0.063 per market (z 1.55, 95% -0.02..+0.14), ahead in 4 of 4 groups and before 1994 (+0.09); +0.04 beyond what part positions give on a random walk. Still open, the best near-miss; not shown. [pooled-1](pooled-1.md) pooled-2 (#159, out of sample on 21 bond and currency series): +0.010 (z 0.33, 95% -0.05..+0.07), commodity spot -0.019; combined with the 41 stock markets +0.045 (z 1.43): unsettled, the lean comes from stocks. [pooled-2](pooled-2.md) |
| trend-vol | Trend + volatility | failed bar; paper candidate on drawdown only | [card](cards/trend-vol.md) | Same Sharpe as tsmom12 (1.03 vs 1.05) but worst loss 26% vs 37% (equal weight 69%), growth 13.3% vs 17.8% a year. A risk choice, not an edge. [result](results/trend-vol.md) pooled-1 (#142): killed outside very volatile assets: the 40% cap almost never binds on stocks, bonds, commodities (D +0.002, 95% -0.003..+0.006; corr. with `tsmom12` 1.00). [pooled-1](pooled-1.md) |

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
| critical-slowing | Ecology (early warning) | dead (gate, wide-6) | - | Literature: rising AC1 before crashes rejected (Guttal et al. 2016; Diks, Hommes, Wang 2019); rising variance survives. wide-6's event-study gate on the six assets (rule pushed first): top-decile quarterly drawdown on a year's Kendall trend of AC1 t 1.4 (to 2015) and 0.1 (2016 on); of variance, with the level of volatility controlled, -0.5 and 1.8. Recent volatility is the only predictor (t 3.8). No card. [gate](results/critical-slowing.md), [write-up](wide-6.md) |
| changepoint-momentum | Change-point detection | dead (literature) | - | Wood, Roberts, Zohren: edge over plain trend gone above about 2 bps a trade (part 4) |
| crypto-daily-reversal | Short-term reversal | dead (literature) | - | Not real in large coins even before our 60 bps round trip (part 3, A) |
| pre-fomc-drift | Calendar | dead (literature) | - | Gone after 2015; window does not fit next-open fills (part 3, E4) |
| ou-optimal-entry | Optimal stopping | dead (literature) | - | Needs a mean-reverting spread; long-only we cannot trade one (part 4) |
| return-forecast-foundation-model | Deep learning | dead (literature) | - | Chronos/TimesFM: negative R-squared against a zero forecast on daily returns (part 5). Do not spend the GPU on raw-return forecasting in M3 |
| llm-trading-agent | LLM | parked | - | Backtests before the model's training cutoff are contaminated; only forward paper scoring counts (part 5). Fits the M3 "research desk" as designed |
| lppls-bubble | Econophysics | parked | - | Three or four crypto bubbles cannot validate a warning signal (part 6, E) |
| hurst-entropy-gate | Econophysics / information theory | parked | - | Time-varying efficiency is documented, exploiting it is not; about five independent readings in ten years (part 6, D-E) |
| signature-leadlag | Path signatures | parked | - | No daily out-of-sample evidence; level 2 is lead-lag areas, which hit the non-synchronous-close problem; level 3+ overfits (part 6, B) |
| halloween | Calendar | tested by survey-4: dead | [card](cards/halloween.md) | Parked by the first survey (one observation a year); tested in survey-4, see that section below |
| crypto-carry | Carry | parked | - | Real, but needs perpetual futures; the gym has spot only (part 3, C3) |

## New (not yet carded; candidates for the next run)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| ensemble-tsmom | Trend | new | - | Weight = share of 1/3/6/12-month returns that are positive (part 1) Superseded: carded and tested (row above; pooled-1). |
| turbulence | Statistics | dead (tested) | [card](cards/turbulence.md) | turbulence-1 (2026-11-24, PR #134): as a crash overlay on `tsmom12` it is volatility in disguise. Against a magnitude-only twin out of the market just as often: -0.04 Sharpe on the six assets (p 0.84), +0.01 on the four indexes; trigger days overlap 70-80% (post hoc). The correlation part alone is worse (-0.07, and -0.24 on the indexes) and misses crashes (in a crash assets move the usual way). Both are behind `tsmom12` itself (z -1.1 and -1.4; the project bar needs z >= 4.69). [write-up](turbulence-1.md), [result](results/turbulence-1.md) |
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
| halving | Crypto cycle | failed bar; not believed; transfer test failed (halving-2) | [card](cards/halving.md) | Coins out 18-30 months after a halving: 1.20 / 1.42, but three winters, a window taken from folklore that saw them, and gone when moved six months. On other halving coins' own dates it fails (Litecoin + Zcash: Sharpe 0.45 vs buy-and-hold 0.74, rank 40 of 41 placebos); with BTC's dates it works on every coin (1.23, rank 1 of 41): the market's BTC cycle, the same three winters, no new episodes. Only the forward window (2025-10..2026-10) is left. [result](results/halving.md), [shifted](results/halving-shift.md), [halving-2](halving-2.md) |

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
| cape-tilt, real-tilt | Valuation / real-yield tilt of 60/40 (monthly) | dead | [invest-1.md](invest-1.md) | OOS 1990-2025 Sharpe -0.00 / -0.03 vs 60/40: stocks looked dear for 30 years and kept rising. |
| ecy-tilt | Excess-CAPE-yield tilt of 60/40 | parked | [invest-1.md](invest-1.md) | +0.08 train (p 0.002), +0.06 OOS (p 0.15), -0.01 on ETFs 2003-25: right sign, too small to prove. |
| term-tilt, infl-regime, xmom | Term spread, inflation switch, dual momentum | dead | [invest-1.md](invest-1.md) | No gain over 60/40 in either period; xmom 0.59 vs 0.67 OOS. |
| 6040-sma10 | 60/40 with 10-month average filter | dead | [invest-1.md](invest-1.md) | Matches its twin `tsmom12-m` (0.75 vs 0.77 OOS): the twin is simpler. |
| ecy-trend | ECY tilt inside the trend rule | parked | [invest-1.md](invest-1.md) | Best Sharpe in both periods (0.62 / 0.82) but beats trend only in train (p 0.002; OOS p 0.13; ETF -0.03). |

## FM 1 (time-series foundation models, 2026-11-13)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| fm-chronos-zero-shot | Pretrained time-series models | dead (tested) | [card](fm-1.md) | Chronos-Bolt weekly IC 0.10-0.15 and +0.18 Sharpe in the rl-3 gate, but it is memory: IC ~0 on 2020-25, on the 1964-93 S&P and on inverted prices; Chronos-2 (no memory) IC ~0 everywhere. [results](results/fm-1.md) |
| fm-fine-tune | Pretrained time-series models | parked | [card](fm-1.md) | Not triggered (no clean zero-shot signal); a fine-tune on train years trains on the years the models remember. |
| fm-forward-log | Pretrained time-series models | new | - | Log Chronos forecasts forward on the paper trail (seconds of GPU a week), judge after a year: the only test free of pretraining leakage. Low priority. |

## Cards from YouTube, run ideas-1 (`cards/yt-1.md`, written before any test; summary in `ideas-1.md`)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| bbwp | Volatility (video 1) | dead (tested) | [card](cards/yt-1.md) | Band-width tops: -0.04 vs tsmom12, 0/5 eras; fired once on BTC. [result](results/bbwp.md) |
| srsi | Momentum extremes (video 1) | dead (tested) | [card](cards/yt-1.md) | Monthly stochastic RSI exits: -0.23; out half the time. [result](results/srsi.md) |
| ath | Cycle clock (video 1) | dead (tested), nearest miss | [card](cards/yt-1.md) | +0.08 (p = 0.18), passes bars 2-6; gain all from coins (4 cycles) and the exact window. [result](results/ath.md), [robustness](results/ath-robust.md) |
| gap | Sentiment (video 2, video 3) | dead (tested) | [card](cards/yt-1.md) | Stocks near highs + low UMCSENT: -0.09, 0/5 eras. [result](results/gap.md) |
| oil | Macro (video 3) | dead (tested) | [card](cards/yt-1.md) | Oil-shock gate: +0.05 (p = 0.20), ties since 2003, mixed out of universe. [result](results/oil.md) |
| y10 | Macro (video 3) | dead (tested) | [card](cards/yt-1.md) | Yield change and three levels: -0.07..-0.01. [result](results/y10.md) |
| trend3 | Trend (video 2) | dead (tested): it is `sma200` | [card](cards/yt-1.md) | SPY/GLD/BTC above 200-day: -0.01 vs tsmom12 on the same three. [result](results/trend3.md) |
| fng | Sentiment (video 4, stand-in) | dead (tested) | [card](cards/yt-1.md) | Buy extreme fear -0.10, sell extreme greed -0.08 (coins, from 2018). [result](results/fng.md) |

### Funding carry at real costs (carry-3, 2026-11-18)

Pooled Sharpe on Binance perps outside the 30, Bybit and Hyperliquid, realistic cost for a 10,000 USD account (~8 bps a side) plus funding. Train 2021-2025 / the one held-out year 2025-11-11 .. 2026-11-10.

| Idea | Kind | Status | Card | Reason |
|---|---|---|---|---|
| band (primary) | Funding carry, weekly with a no-trade band | dead (held-out spent) | [carry-3.md](carry-3.md) | Train 0.79 (p 0.025), passed all bars; held-out -0.65, blend behind the twin. 16% funding collected, ~22% lost on price. |
| w1, w2, w4, f30 | Funding carry, other speeds and a 30-day signal | parked (train only) | [carry-3.md](carry-3.md) | Train 0.78 / 1.01 / 0.69 / 0.29; never run on the held-out year, which `band` spent. |

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
| month-end-bonds | Market microstructure / calendar (post hoc, from wide-1) | dead (tested, not replicated) | [card](cards/month-end-bonds.md) | Hold the bond for the last four sessions of the month, on data wide-1 did not use. LQD 2002-2025: +22.5 bps a month gross (t 4.1), +10.5 after cost and ordinary drift (t 1.93, bar 2.0); Sharpe 0.52 vs 0.60 for the constant-weight twin and 0.59 for buy-and-hold. TLT's first year: -1.8 bps, 11 months. Held-out year not spent. [result](results/month-end-bonds.md), [write-up](month-end-bonds.md) |
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
| coupon-dose | Pharmacokinetics (scheduled dosing, dose-response) | dead (tested) | [card](cards/coupon-dose.md) | wide-4's new W4: idle cash into TLT for sessions P .. P+3 when the Treasury's net payment on the 15th (coupons + principal - new issues settling) is positive: 1.04 vs 1.05 (difference -0.011, p 0.71), fails 3 of 6 bars; other ETFs (into IEF) -0.03. Event study: TLT +2 bps on 146 positive-dose days against +18 on 133 others; slope t 1.0; wrong sign since 2014 (IEF -16 bps, t -2.1). Mid-month has no counterpart of the month-end bond rally. [result](results/coupon-dose.md), [write-up](wide-4.md) |
| tidal-trigger | Seismology (tidal triggering near critical stress) | new | - | wide-4's W5: small calendar flows move prices only when dealers are stretched (high stress). Partial post hoc support from `tax-drain` (effect largest while reserves shrank); every calendar it would use is already seen, so it needs a calendar not used to suggest it. Plan in `wide-1.md`, last section |
| payday-inflow | Actuarial science (contribution annuity) | new | - | wide-4's W6: 401(k) contributions buy stocks after mid-month paydays; event study in non-tax months, before and after 2007. Prior 1% (idle cash into stocks has failed). Plan in `wide-1.md`, last section |
| fatigue-damage | Materials science (Basquin, Miner's rule) | new | - | wide-4's W7: rainflow-counted damage of leveraged coin longs; mostly collapses into `dip-rsi2` and P4. Plan in `wide-1.md`, last section |
| snapshot-shrink | Metrology (snapshot sampling, Goodhart) | new | - | wide-4's W8: quarter-end leverage-ratio snapshots thin Treasury intermediation from 2015; sits on top of the post hoc month-end bond rally, so descriptive only. Plan in `wide-1.md`, last section |
| dealer-backlog | Queueing (server of last resort, Grossman-Miller) | dead (tested) | [card](cards/dealer-backlog.md) | wide-5's new W9: idle cash into TLT for five sessions after a 20/30-year auction whose primary-dealer share beat its 12-auction median: 1.02 vs 1.05 (difference -0.026, p 0.95), fails 4 of 6 bars, behind its placebo; other ETFs (into IEF after 10-year auctions) -0.008. Event study (264 long auctions since 2008-07): TLT -13 bps after high-dealer auctions against +6 after the others; slope t -1.0 (the overhang sign, not the recovery). [result](results/dealer-backlog.md), [write-up](wide-5.md) |
| extension-dose | Control theory (feedforward of a known index step) | dead (tested) | [card](cards/extension-dose.md) | wide-5's new W10: the month-end TLT window only in months whose 20+ year index extension (built from the auction file) is above its 24-month median: 1.06 vs 1.05 (difference +0.013, p 0.19), 2 of 4 eras; beats its placebo 1.061 vs 1.054. Event study: high months +32 bps vs low +17; slope t 0.8; the gap is all before 2014 (+46 vs -3 since). The book gain is 2008-09 (+8.1 of +7.9 points). Not supported. [result](results/extension-dose.md), [breakdown](results/wide-5-deeper.md), [write-up](wide-5.md) |
| lunar | Astronomy x chronobiology | dead (gate, wide-6) | - | wide-3's W3. Yuan, Zheng, Zhu (2006, 48 countries 1973-2001): new-moon days beat full-moon days by 3-5% a year (G-7 2.4 bps a day). wide-6 gate, SPY 2007-2025: +1.6 bps a day (t 0.43), rank 12 of 29 phase shifts; paper's years on the S&P 500 +3.1 (t 1.3). Every stock series positive after publication but all t < 0.6; the gate could only see about 7 bps. No card. [gate](results/lunar.md), [write-up](wide-6.md) |
| rmd-december | Demography (cohort flows) | dead (gate, wide-7) | - | wide-6's W12: December sales forced by required minimum distributions. wide-7 gate (rule pushed first): SPY's last ten December sessions, excess of the year's drift, in the waiver years 2009 and 2020 against the other years: -0.06% (permutation p 0.51); TLT -0.18%; S&P 500 index 1975-2024 -0.31%. The gate could only see 4-5% in ten sessions. No card. [gate](results/rmd-december.md), [write-up](wide-7.md) |
| festival-gold | Anthropology (lunisolar calendars) | dead (gate, wide-7) | - | wide-6's W13. wide-7 gate on GLD 2004-2025 (rule pushed first): the 15 sessions before Dhanteras and the Lunar New Year against the same month's mean, -1.9 bps a day (t -0.30; -8.6 to 2010, +1.1 from 2011), rank 10 of 15 weekly shifts. Baur's (2013) autumn effect reversed after 2010 (September +22 to -9, November +29 to -7 bps a day). No card. [gate](results/festival-gold.md), [write-up](wide-7.md) |
| wash-sale-echo | Tax law (30-day refractory period) | dead (gate, wide-7) | - | wide-6's W14. wide-7 gate on 21 ETFs (rule pushed first): return over days 31-45 after the third Friday of December on the November loss, -0.003 (t -0.07) in tax years 1994-2011 and +0.023 (t 0.43) in 2012-2024; coin placebo slope above the ETFs'. A loser rebound shows at the turn of the year after 2012 (t 3.9, year clusters; a placebo window gives t of 2.5 to 4 too): a lead, not a result. No card. [gate](results/wash-sale-echo.md), [write-up](wide-7.md) |
| cat-claims | Catastrophe meteorology | dead (gate, wide-8) | - | wide-6's W15. wide-8 gate (rule pushed first): 104 US landfalls 2002-2025 from NOAA HURDAT2, LQD minus half of TLT over 20 sessions on the Saffir-Simpson category, +0.01 points per category (t 0.09); halves -0.44 and +0.13; rank 8 of 23 year-shifted calendars. Major landfalls saw corporates lead, not lag (+0.91 points over tropical storms). No card. [gate](results/cat-claims.md), [write-up](wide-8.md) |
| geomagnetic-storm | Heliophysics (Kp/Ap index) | dead (gate, wide-8) | - | wide-7's W16. wide-8 gate (rule pushed first; daily Ap from GFZ Potsdam, keyless, CC BY 4.0): SPY 2003-2025 six sessions after a severe storm (Ap >= 100) +18.2 bps a day over calm (t +2.46, wrong sign), minor storms +0.8, rank 29 of 31 shifted Ap calendars; GSPC 1950-2002 (paper's years) -4.4 (t -1.05). No card. [gate](results/geomagnetic-storm.md), [write-up](wide-8.md) |
| fork-premium | Software release engineering (scheduled activation) | dead (gate, wide-9) | - | wide-7's W17. wide-9 gate (rule pushed first; ETH and BTC cached, keyless): ETH minus BTC over the ten days into minus the ten days after 15 mainnet upgrades 2016-2025, mean +0.70% (t 0.23), rank 19 of 41 calendars moved by k x 30 days; Pre -0.06%, Post -0.76%; scope 1 +2.9% vs 0 -0.4% (5 vs 10 events). Placebo t sd 1.05: independent events, normal null about right. No card. [gate](results/fork-premium.md) |
| elimination-mood | Sport sociology (knockout-match mood shocks) | new | - | wide-8's W18: next-day index fall after a national team's World Cup or Euro elimination (Edmans, Garcia, Norli 2007, from memory); dose = round x football weight, wins as placebo; DAX, FTSE, Nikkei cached; post-sample 2006-2024, about 25 events (weak). Gate first. Plan in `wide-1.md`, last section |
| enso-commodity | Oceanography (El Nino index) | dead (gate, wide-9) | - | wide-8's W19. wide-9 gate (rule pushed first; NOAA CPC ONI, keyless): DBC six-month return on the lagged ONI, 2014-2025 -2.5 points per degree (t -0.92), rank 32 of 41 year-shifted ONI calendars; 2006-2013 +1.8 (t 0.44). Highest returns after La Nina, not El Nino. DBC is mostly energy; the non-fuel channel (DBA) is untested. Placebo t sd 1.74. No card. [gate](results/enso-commodity.md) |
| hdd-gas | Meteorology (heating degree days) | dead (gate, weather-1) | - | weather-1, card pushed before any return data. NOAA CPC daily HDD weighted by gas-heated homes (keyless), 7-day surprise vs a rolling 20-year normal, against UNG's next-week return (entry 4 days after the week), winters 2007-08..2024-25: -0.036 points per 10 degree days (t -0.29, 389 weeks), rank 19 of 41 winter-derangement placebos (placebo t sd 1.12); halves +0.17 / -0.25. Even the same-week move is small (t 1.68): the market trades the forecast. Next weather angle: forecast revisions (CPC 6-10/8-14 day outlook archive). No card. [gate](results/hdd-gas.md), [write-up](weather-1.md) |
| cpc-revision | Meteorology (forecast revisions) | dead (gate, weather-2) | - | weather-2, card pushed before any price. Keyless CPC 6-10/8-14 day outlook shapefiles exist only from 2012-09 (13 train winters). Dose: change in a gas-weighted cold-outlook index (tercile probabilities at state population centroids, Census-division weights recovered from CPC's gas-weighted degree days) between the issues before session t and before the previous session; y: UNG open-to-close of t (entry after the ~3 pm ET issue). -0.076 points per 0.10 (t -0.68, 1,327 sessions), rank 36 of 41 winter-derangement placebos (sd 0.95, median +0.78); halves both negative. The dose is real: close before the issue day to the next open +1.86 per 0.10 (t 7.9). Priced before the open; nothing follows. No card. [gate](results/cpc-revision.md), [write-up](weather-2.md) |
| turn-of-year-losers | Calendar / tax-loss selling (seen cell of W14's gate) | forward (proposed) | - | wide-8: pre-registered for the 2026/27 turn: slope t of the 31 Dec..10 Jan return on the YTD loss to November across 21 ETFs, against an empirical null of 153 placebo windows (sd of t 2.18); pass needs t >= 4.87 (p <= 0.02); power 8% at the lead's slope. Entry `forward/proposed-wide8.jsonl`, NOT frozen. Not a mechanism of the list, no try. [null](results/turn-of-year-null.md), [write-up](wide-8.md) |
| congress-workload | Legislative studies (roll-call counts, Anscombe transform) | dead (gate, wide-15) | - | wide-15's W27, card pushed before any price. Policy-risk premium after busy legislative weeks: SPY's next 4 weeks on 2 sqrt(n + 3/8) of House + Senate roll calls, in-session dummy and past 4/13/26/52-week returns as controls, 1994-2025: -0.009% per unit (t -0.19), rank 25 of 41 earlier-dose placebos (SD 1.08). In-session dummy +0.34% per 4 weeks (t +0.69). [result](results/congress-workload.md) |
| refund-runoff | Public finance x hydrology (Nash-cascade unit hydrograph) | dead (gate, wide-15) | - | wide-15's W28, card pushed before any price. Weekly IRS individual-refund surprise (Daily Treasury Statement, same-ISO-week median of three earlier years) passed through a gamma kernel, against QQQ, IWM, BTC, ETH next 4 weeks, 2008-2025: +0.281% per unit (t +1.44), rank 7 of 41 (placebo SD 1.92: a seasonal dose). Shown QQQ+IWM t +2.67 noted only. Flow size far too small for the slope. [result](results/refund-runoff.md) |
| settlement-fails | Settlement logistics (fails as backorders) x peaks over threshold | new (scored 5, parked) | - | wide-15's X11: Treasury fails spikes mean scarce collateral, a convenience premium, so lower TLT returns after; F2 with controls (fails surge in flights to quality). Needs NY Fed primary-dealer fails files (several formats). Prior 0.5% |
| rule-intensity | Administrative law x text counts | new (scored 4, parked) | - | wide-15's X9: regulatory-risk premium on sector funds after heavy weeks of final rules (Federal Register API, keyless, 1994-); rule waves follow crises with lags (controls). Prior 0.5% |
| petro-recycling | Resource economics (petro-state fiscal rules) | parked (scored 3) | - | wide-15's X5: oil exporters sell foreign assets when oil falls. `oil_13w` already screened flat (info-1, slow-1) and the `oil` rule died: seen and killed in other words |
| fomc-dissent | Social choice (committee voting) | parked (scored 3) | - | wide-15's X12: dissents signal policy uncertainty, a term premium until the next meeting; about 255 meetings 1994-2025 (power 0) |
| refund-filtered-set | Public finance, computational linguistics, mining | filtered (wide-15) | - | wide-15's X2 `stimulus-runoff` (amounts by statute, dates announced: F1), X3 `path-act-shift` (a legal timing shift, no dose: F1), X4 `withheld-nowcast` (public news: F1), X10 `news-text-vol` (fitted to VIX: F2); X6 `hydro-hash` and X7 `curtailment-hash` score 0 and 1 (difficulty adjustment holds issuance, so hash-rate swings carry no flow) |

### Run survey-2: 2023-2026 literature (2026-11-18)

Sources and the ranking note (written before any number) in [survey-2.md](survey-2.md). Seven
new candidates; the family of the `wide-*` lineage is now 61. One carded and tested; held-out
year unspent.

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| fomc-cycle | Monetary-policy calendar (Cieslak, Morse, Vissing-Jorgensen, JF 2019) | dead (tested) | [card](cards/fomc-cycle.md) | Stock slots only in even FOMC-cycle weeks: +0.18 Sharpe over `tsmom12` on full train (p 0.03, 4 of 5 eras, both other sets positive), all of it 1994-2016, the paper's sample. After publication (2017-2025) SPY's even-minus-odd spread is -5.7 bps a day (t -1.2; in-sample +11.0, t 3.1) and the gate trails the twin (-0.05). Fails the family bar (0.00164) and both post-publication bars. `even-overlay` (idle cash into stocks in even weeks) 0.96 vs 1.05. [result](results/fomc-cycle.md) |
| xtsmom | Cross-asset trend (Pitkäjärvi, Suominen, Vaittinen, JFE 2020) | dead (tested) | [card](cards/xtsmom.md) | Stock slots only while the 10-year bond's 12-month return is also positive: 1.05 vs 1.05 for `tsmom12` (+0.00, p 0.49, 1 of 5 eras); it only cuts exposure (62% vs 76%). Since 2017 -0.06. SPY up-trend days, bond-up minus bond-down: -0.2 bps a day 1994-2015, +0.4 (t 0.1) after 2016; the effect is only on the S&P 500 index 1980-1993 (+21.5, t 2.2). 6-month bond and the paper's bond leg worse. Fails the family bar and both post-sample bars. [result](results/xtsmom.md), `survey-3.md` |
| fomc-bond-drift | Monetary-policy calendar (Pan and Peng 2025; Hillenbrand, RFS 2025) | parked (forward only) | - | Idle cash into TLT around FOMC days; about 12 bps a meeting; half is the 1989-2020 fall in yields. The sample covers all of our train: no honest train test. Forward descriptive check at most (`survey-3.md`). Prior under 1% |
| announcement-premium | Macro announcements (Savor and Wilson 2013/2014; Lucca and Moench 2015; Ai, Bansal, Guo 2023; disputed, Management Science 2025) | dead (event study) | - | FOMC leg: SPY day 0 +30.9 bps over other days in 1994-2011 (t 3.1), -0.8 (t -0.06, 87 meetings) in 2015-2025; pre-set gate (t >= 2 after publication) not met, no card (`ann-1.md`). CPI/payroll legs dropped by literature |
| turning-points | Trend (Goulding, Harvey, Mazzoleni, JFE 2023) | dead (literature) | - | State-dependent blend of 12- and 1-month trend; 0.52 vs 0.51 gross in the paper; `ensemble-tsmom` already tied (`survey-3.md`) |
| nonlinear-tsmom | Machine learning (Moskowitz et al., SSRN 2025) | dead (literature) | - | ML on past returns; run 2's seven ML cards found nothing (AUC 0.50) (`survey-3.md`) |
| crypto-corr | Crypto (Yae and Tian 2021) | dead (literature) | - | BTC timed by its correlation with stocks; daily horizon against 60 bps (`survey-3.md`) |

### Run survey-4: effects with a post-publication record (2026-11-18)

Sources, candidates and the pick rule (written before any number) in [survey-4.md](survey-4.md).
Four mechanisms new to the lineage (family now 65, bar p < 0.10 / 65 = 0.00154); two carded and
tested; held-out year unspent.

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| ts-carry | Carry (Koijen, Moskowitz, Pedersen, Vrugt, JFE 2018; Baltussen, Swinkels, van Vliet, JFE 2021) | dead (tested) | [card](cards/ts-carry.md) | SPY, QQQ, TLT trend slots only while carry (dividend yield or 10-year yield minus bills) is positive: 0.97 vs 1.05 (-0.08, p 0.78); at the running mean 1.02 (-0.03). All of the loss is the stock leg: SPY out 54% of its trend days, and stock carry's sign carries no timing information (-0.7 / -1.2 bps a day before / after 2012-10). The documented survivor is cross-country carry, which this book cannot hold. Post hoc trace only: TLT above its running-mean carry +11 bps a day after 2012-10 (t 1.9). [result](results/ts-carry.md) |
| halloween | Calendar (Bouman and Jacobsen, AER 2002; Andrade et al., FAJ 2013; Zhang and Jacobsen, JIMF 2021) | dead (tested) | [card](cards/halloween.md) | Stock trend slots only November-April: 0.96 vs 1.05 (-0.08, p 0.87), 0 of 5 eras; ahead only in 1998-2012 (+0.06), R13's own new-data years. SPY winter minus summer +5.9 bps a day 1998-2012 (t 1.3), -0.5 (t -0.1) after 2012-05; S&P 500 1962-1993 t 2.0-2.1. Out of universe positive on old data. [result](results/halloween.md) |
| seasonal-20y | Return seasonality (Heston and Sadka 2008; Keloharju et al. 2016; Baltussen et al. 2021) | dead (tested) | [card](cards/seasonal-20y.md) | A slot only in calendar months whose 20-year same-month average is not below the asset's average month. Cross-sectional gate on 23 ETFs failed (`survey-7.md`). Time-series form (`seasonal-1.md`, PR #148): behind holding on US industries 1945-2025 (-0.13, z -1.89; before 1981 -0.11, so not even 'strong pre-1981'), 13 developed markets (-0.07) and the six (-0.07); overlay behind `tsmom12` on the six (0.88 vs 1.06, z -2.76). Mostly the price of switching in and out: off-cycle placebos lose more (-0.21), the true lag ranks 1 of 11 (weak trace). [result](results/seasonal-1.md) |
| ts-value | Value (Baltussen et al. 2021; Welch and Goyal 2008) | new | - | Stock slots only while the dividend yield is above its running median; TLT while the real yield is. Dividend-yield timing already fails out of sample (Welch and Goyal). Prior under 1% |
| live-check | Live fund records (AQR TSMOM factor vs AQMIX; 9 trend, 3 risk-parity funds) | descriptive (no pick) | [card](cards/live-check.md) | `tsmom12` correlates 0.17 with live trend funds and 0.40 with SPY; Sharpe above bills 2010-2025 1.11, equal to holding (1.11), live trend funds 0.19. Paper TSMOM 1.41 (1985-2009) -> 0.35 after; AQMIX 0.29: haircut 80%. Our lead over holding +0.29 before 2010, 0.00 after. [result](results/live-check.md), [note](survey-5.md) |
| where-rp | Risk parity (Maillard, Roncalli, Teiletche, JPM 2010; Kirby and Ostdiek, JFQA 2012) | dead (tested) | `rp-1.md` step 2 | `where-vol` with the protocol's inverse-vol slot sizes, carded after rp-1's diagnosis (2022 gap to live risk-parity funds = the coin slot at equal dollars, 89% of its risk). 1.05 vs 1.05 for `tsmom12` (+0.00, p 0.50), worst loss 24.5% vs 36.5%, growth 12.4% vs 17.8%: a risk dial. 2022 -19.7% (coins fixed, unfiltered TLT now -8.2 pts) vs `tsmom12` -12.8%, funds -16.1%. Fails bar 1 (family 74); `where-vol`/`blend-ws` not revived. [result](results/rp-1.md) |

### Trend tune: anatomy and honest tuning of `tsmom12` (trend-tune, 2026-11-18)

Card and write-up: [trend-tune.md](trend-tune.md), fixed before any number. Sharpe on the six
assets, 1994-2025 / since 2003: `tsmom12` 1.05 / 1.20. Held-out year unspent.

| Idea | Kind | Status | Card | Reason |
|---|---|---|---|---|
| wf-asset | Walk-forward lookback per asset | dead (tested) | [trend-tune.md](trend-tune.md) | 1.01 / 1.18 (-0.04, p 0.78); 45% more trading, nothing gained. [result](results/trend-tune.md) |
| wf-pooled | Walk-forward lookback for the book | dead (tested) | [trend-tune.md](trend-tune.md) | 1.02 / 1.19 (-0.03, p 0.63); wanders between 6 and 9 months. [result](results/trend-tune.md) |
| wf-shrunk | Per asset, shrunk toward 12 months | dead (tested) | [trend-tune.md](trend-tune.md) | Never leaves 12 months on the six assets: it is `tsmom12`. [result](results/trend-tune.md) |
| trend-tune-surface | 98 settings of the trend rule | described (no pass bar) | [trend-tune.md](trend-tune.md) | A flat plateau from 6 to 12 months, any decision frequency, any threshold; best cell +0.08, luck alone +0.17. Not candidates. [result](results/trend-tune-anatomy.md) |
| trend-1926 | Trend, older data | described (crash insurance, not "a property") | [trend-1926.md](trend-1926.md) | Two eras, one card each. 1927-1961: market 0.88 vs 0.55 (+0.33, p 0.02), worst loss 38% vs 84%; book +0.45; about two thirds is 1929-1932 (without it +0.11, p 0.18); 1946-1961 -0.09. 1962-2001, "crashes only": 0.88 vs 0.80 (+0.07, p 0.26), worst loss 32% vs 48%; book +0.05; without 1973-1974 -0.03. The lead on US stocks is 1929-32 and 1973-74 only; days out rougher only in the bear-market halves. Replay gaps: holiday-Friday weeks, no deciding number moves. [era 1](results/trend-1926.md), [era 2](results/trend-1926-era2.md) |
| insure-1 | Trend, crash insurance | described (insurance real and timing-driven; premium about 1, handed back in rebounds) | [insure-1.md](insure-1.md) | 270 falls of 25%+ on the US market and 10 industries 1927-2025, 50 effective episodes: `tsmom12` lost less in 48 (avoided half the fall vs 0.27 for random timing, 0 of 1,000 rotations as good). Net of the year after the low: 16 of 50, mean -0.3 log pts. Premium (growth given up per unit of loss avoided) 1.07 vs 1.63 for holding 73% fixed; 0.86 in 1927-61, ~1.35 since 1962. Fails in fast falls (net -6.6, 15 of 63). [tables](results/insure-1.md) |
| insure-2 | Trend, crash insurance per era and outside the US | described (insurance robust; cheaper than holding less in every era and set, significantly in 3 of 6; premium today 1.3-1.5) | [insure-2.md](insure-2.md) | Per era (US): trend's premium 0.85 / 1.38 / 1.34 vs fixed exposure 1.38 / 2.15 / 1.53 and random timing 1.63 / 2.60 / 1.91 (1927-61 / 1962-2001 / 2002-25); 2002-25 alone "in between" (p 0.19). 13 developed non-US indices 1966-2025, 19 effective falls: lost less in 17 of 18 (p 7e-5), share avoided 0.49, net -0.9; premium 1.11 vs 1.33 fixed, 1.52 random (p 0.009). Total-return regions 1.23, 10 more markets 1.18 (both in between). Since 2002 about 2 log pts a year behind holding. [tables](results/insure-2.md) |
| fast-reentry | Trend, quicker return after crash lows (`or3-12`: 12-month OR 3-month return positive) | in between (not a pick; first pick in the insure line, family bar 0.05 not met) | [fast-reentry.md](fast-reentry.md) | Same 25% falls as insure-1/2. US 50 effective falls: rebound +8.4 log pts better (41 of 49) but insurance -6.9 (share avoided 0.50 -> 0.35; it also stays in at 36% of `tsmom12`'s exits), net +1.5 (30 of 50, p 0.10 / 0.19). Non-US 19: net +4.7 (12 of 19, bootstrap p 0.002). Premium 1.07 -> 0.97 (non-US 1.11 -> 0.97; US 2002-25 1.34 -> 1.33) but mean position 73% -> 83%, US market worst loss 38% -> 51%: a smaller policy, not cheaper insurance. Helps most in fast falls (non-US +7.4). [tables](results/fast-reentry.md) pooled-1 (#142), Sharpe on 41 markets: +0.018 (z 0.47), below the +0.039 its extra exposure gives on a random walk: no timing gain. [pooled-1](pooled-1.md) |
| fast-reentry-2 | Trend, "armed" re-entry after crash lows (`arm3-12`: exit as `tsmom12`, re-enter when the 3-month return turns positive); `or3-12` vs exposure controls | in between (not a pick; second pick in the insure line, family bar 0.025 not met); line closed | [fast-reentry.md](fast-reentry.md) | US 50 falls: net +1.8 (28 of 50, p 0.24 / 0.11), rebound +7.7, insurance -5.9 (share 0.50 -> 0.37, guard fails). Keeping the exits saved only 1 log pt: the leak is the re-entry (1929-33 rallies). Non-US +5.3. `or3-12`'s premium 0.97 is timing, not exposure (fixed 83%: 1.61). Close the re-entry and insure pick lines. pooled-1 (#142): `arm3-12` +0.015 (z 0.39), below its random-walk exposure effect (+0.029). Line stays closed. |
| insure-4 | Trend, crash insurance: PPUT (S&P 500 + monthly 5% OTM put) while `tsmom12` is in, bills when out | dead (tested; worse than `tsmom12`, bar not met) | [card](cards/insure-4.md) | S&P 500 1986-07..2025-10: Sharpe above bills 0.47 vs `tsmom12` 0.58, paired d -0.110, SE 0.066, z -1.67 (bar 4.70). CAGR 7.8% vs 10.8% (2.9 pts a year dearer than trend, more than PPUT held always). Covers the fast crashes (1987 -11% vs -33%, 2020 -6% vs -20%), worst loss 19% vs 33%, insurance cost 0.15 (trend 0.02, PPUT 0.28). The puts' payoffs come when trend is already out (post hoc: PPUT minus hold about -3.3 pts a year while in, -1.1 while out). [write-up](insure-4.md), [tables](results/insure-4.md) |
| own-vol-target | Volatility targeting of the `tsmom12` sleeve (`vt-own-70-x`, `vt-own-26-x`: share = min(1, k / sigma52), expanding k, monthly reset; risk-menu-3, #110) | equity-only at best (pooled-1: lean positive at 70% on stocks; pooled-2: killed on bonds and currencies) | [pooled-1](pooled-1.md), [pooled-2](pooled-2.md) | Six assets: 1.04 / 0.97 vs 0.94 (+0.10 / +0.03, about one SE). pooled-1 (#142, 41 markets): 70% +0.022 per market (z 1.37, 95% -0.01..+0.05; US industries +0.06, ETFs -0.03), 26% -0.012 (z -0.43); both about +0.03 better than no-skill sizing on a random walk. A risk dial with at most a small Sharpe gain. pooled-2 (#159, out of sample): 70% on 21 bond and currency series -0.010 (z -0.57, 95% upper end +0.024: killed; bonds +0.02, currencies -0.05), commodity spot +0.056 (z 2.15, not judged: smoothed PPI); combined with stocks +0.011 (z 0.89). No Sharpe gain outside stocks. |
| coin-fast-exit | cointop-1's coin exits carried to every market (`fade-28`: 12-month AND 28-day up; `stop-0.25`: within 0.25 vol-years of the 1-year high) | `fade-28` dead as a general rule; `stop-0.25` open at the kill line (pooled-1) | [pooled-1](pooled-1.md) | Six assets, coin slots only: +0.04 each (p about 0.3, `cointop-1.md`). pooled-1 (#142, 41 non-coin markets): `fade-28` -0.062 (95% -0.14..+0.02, killed), `stop-0.25` -0.066 (-0.16..+0.03), behind in all four groups: they hold too little; on coins this says nothing. |
| bear-legs | Trend insurance: multi-leg bear markets; can a bear-market rally be told from the bottom at the time? | description (no pick, no rows); nothing distinguishes | [bear-legs.md](bear-legs.md) | 74% of US 25% falls (72% non-US) hold a 10% rally before the low; the 3-month re-entry rules bought 25-26% of those rallies, `tsmom12` 9%; single-leg first falls cost `or3-12` nothing (dI -0.1), 88% of its leak is in falls with rallies. At a 10% rally off the low in a confirmed 25% fall, 7 observables (depth, duration, rally speed, volatility, vol ratio, 12-month return, breadth): US AUC 0.47-0.54, placebo p >= 0.45, non-US the same. The late buy-back is the price of the insurance. 30 looks; no card. [tables](results/bear-legs.md) |
| trend-where-it-pays | Trend, per-asset switch | dead (tested) | [trend-where.md](trend-where.md) | A tie: 1.07 against 1.05 (p 0.27), worst loss 35.3% against 36.5%, but twice the loss in 2022 (-26% against -13%). The depth-of-fall reading is worse. [result](results/trend-where.md) |
| fast-reentry | Trend, re-entry | new | - | Held if the 3-month OR the 12-month return is positive: +0.01 / +0.08 in sample (one of 98 cells). Test only out of universe, then held-out; deflate for 98. Done out of universe: `fast-reentry.md` (falls) and pooled-1 (Sharpe, 41 markets, +0.018, z 0.47): no edge seen; held-out not spent. |
| gsy-runup | Bubbles / crash risk (Greenwood, Shleifer & You 2019) | weak pass on the letter; not a candidate | [card](cards/gsy-runup.md) | Run-up flag (2-year return >= 100%/150%, raw and net of market) is real information: 38%/51% crash within 2 years against 15% base (49 industries 1928-2014). As an exit on `tsmom12` (30 French industries): +0.03 Sharpe 1928-2001 (`flag100-sma` p 0.001, `flag100-vol` p 0.007), +0.02 after 2002 (p 0.2), behind on sector ETFs. `tsmom12` already out on 88% of crash days. [write-up](gsy-1.md), [result](results/gsy-1.md) |
| eu-1 | Robustness, EUR / UCITS universe | described (robustness, no selection) | [card](cards/eu-1.md) | `tsmom12` on SXR8, SXRV, 4GLD, IBGL + BTC/ETH in EUR, retail costs, 2012-2025: 1.44 vs 1.37 on the US six, max DD 31% vs 36.5%, same crash pattern: holds. Coin-free asset-class book: drawdown role holds, Sharpe gap to equal weight -0.21 vs -0.04 (half currency, rest costs). [write-up](eu-1.md) |
| eu-4 | Execution, small EUR book | dead (both reducers fail the drawdown bar) | [card](cards/eu-4.md) | On coin-free `euw`, 83% of flip orders reverse within 4 weeks (half the fee drag). Confirmation over two Fridays and a 0.25-z dead zone cut orders 30 -> 20 / 17 a year at the same Sharpe and 0.89-0.91 position correlation, but deepen max DD by 3.3 / 2.4 pts (slower covid exit): change the rule by the card. eu-3 verdict unchanged. [write-up](eu-4.md) |

### Combinations of the tested models (deep-1, 2026-11-18)

Card and bar in [deep-1.md](deep-1.md), fixed before any number. Sharpe on the six assets,
1994-2025 / since 2003: `tsmom12` 1.05 / 1.20. Sleeves: `tsmom12` and 29 tested models; every
choice walk-forward, refitted each January. Held-out year unspent.

| Idea | Kind | Status | Card | Reason |
|---|---|---|---|---|
| deep-1-stack | `tsmom12` plus the model least like it in its losing weeks, inverse-variance shares | dead (tested) | [deep-1.md](deep-1.md) | 1.01 / 1.22; picked the Fed-hike gate, then 60/40 just before 2022. Behind on 2 of 3 other sets. [result](results/deep-1.md) |
| deep-1-switch | Per trend state, the model with the best past Sharpe in that state | dead (tested) | [deep-1.md](deep-1.md) | 1.02 / 1.05; chose gates that had dodged the last crash and sat out 2023-24 (2022-25: -0.32). [result](results/deep-1.md) |
| deep-1-meta | Ridge meta-learner on the sleeves' weekly returns | dead (tested; nearest miss) | [deep-1.md](deep-1.md) | 1.08 / 1.27 (p = 0.27), ahead on 2 of 3 other sets, but equal to the plain average of all sleeves (1.06 / 1.29). A smoother ride for less growth, not skill. [result](results/deep-1.md) |

### Complementary blends from the failure map (combo-1, 2026-11-18)

Card and bar in [combo-1.md](combo-1.md), fixed after the map and before any blend number. Bar
p < 0.10 / 72. Six assets, 1994-2025 / since 2003: `tsmom12` 1.05 / 1.20. Held-out year unspent.

| Idea | Kind | Status | Card | Reason |
|---|---|---|---|---|
| combo-1 blend-ws | `where-vol` + `stop-0.25`, equal risk (excess correlation 0.00) | dead (tested; closest miss) | [combo-1.md](combo-1.md) | 1.13 / 1.35, p = 0.059, worst loss 28.9%; fails the family bar and eras (2 of 5; behind 2022-25, where both sleeves fail). Out of universe +0.02 / +0.02 / +0.00. [result](results/combo-1.md) |
| combo-1 blend-iv | `tsmom12` + `inverse-vol`, equal risk | dead (tested) | [combo-1.md](combo-1.md) | 1.07 / 1.42, p = 0.39, worst loss 44.4% (2000-02). The risk dial again. [result](results/combo-1.md) |

New, not yet carded (from the failure atlas, [results/deep-1-atlas.md](results/deep-1-atlas.md)):

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| breadth-gate | Trend / cross-asset | new | - | Drop an out-of-trend asset only while at most a third of the book is in trend. Seen after looking (atlas table 2b: empty slots -4% a year when the book is broadly out of trend, +16 to +23% otherwise); three "off" episodes on the six assets, so it must be judged on other universes. Borders the `trend-tune` lane |
| coin-top-exit | Trend / crypto | new | - | Eight of `tsmom12`'s ten deepest drawdowns are coin tops. Test a volatility-capped coin slot or a faster coin-only exit on the top-100 coin book (hundreds of tops), then carry one setting back to BTC and ETH |
| carry-complement | Carry + trend | new | - | The long-only pool has no complement (hindsight ceiling 1.22). Run deep-1's `stack` unchanged on `tsmom12` and the funding-carry book once carry-3 has its cost answer |
| breadth-book-1 | Trend / universe breadth | dead (tested) | [card](cards/breadth-book-1.md) | `tsmom12` unchanged on mechanically chosen wider universes (33 US ETFs eligible by 2006 data, round-robin by class; top 10 coins by 2019 cap), above bills: the six 1.19 (2008-2025); six + 6/14/29 ETFs 0.96 / 0.83 / 0.65 (z -2.3 to -2.6); ETF-only 0.61-0.37 vs the live four's 0.82; coins top 5/10 0.88/0.75 vs BTC+ETH 1.14 (2020-). Smaller worst loss only via a smaller coin share. N_eff 3.1 -> 3.3-4.2 (avg corr 0.11 -> 0.40). No paper-book spec. [write-up](breadth-book-1.md) |

## wide-16: how to build and size the book (ideas from other fields; `wide-16.md`)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| cost-band | Stochastic control with proportional costs (no-trade region, cube-root law) x Shannon's demon | dead (tested); nearest miss on a design that can pass | [card](cards/cost-band.md) | `tsmom12` with the gym's rebalance band at 5 points (theory width for a coin slot) instead of 1: 1.093 vs 1.045, +0.049, paired SE 0.018, **z 2.76** (above bills z 3.04) against the bar 4.69; 2-point band +0.014, z 2.35. Coins +0.039 (z 2.5). Max DD 32.5% vs 37.4%. Not the fee: coin costs fall only 0.55% -> 0.44% a year (fewer fills, dearer fee tier); post hoc nearly all the gain is the drift itself (coin slots left to run in 2010-21). [result](results/cost-band.md), [write-up](wide-16.md) |
| coin-drift-run | Trend at short horizons (post hoc from cost-band) | not confirmed (tested, coin-drift-1) | [card](cards/coin-drift-run.md) | Letting a held coin slot drift up to 5 points over 1/n earned +0.054 Sharpe on BTC/ETH with coin fills free (wide-16, post hoc). coin-drift-1 (#157) tested the frozen band (as a share of the slot) on cointop-1's ~90-coin book without BTC, ETH or wide-16's six coins: band05 +0.033 net (z 1.80, bar 2), drift part with costs zero +0.014 (z 0.71); the same band on 40 block-shuffled no-trend books gains +0.024 (excess +0.009, z 0.83); band02 +0.011 (z 2.45) is all placebo (excess z 0.62). The gain is fewer trades, not drift; what drift there is sits in 2020-21, wide-16's episode. No case for changing the live band. [result](results/coin-drift-run.md), [write-up](coin-drift-1.md) |
| bet-hedge-seedbank, phenotype-switching, demon-book-cash, portfolio-effect, functional-groups, taylor-law, k-of-n-lookbacks, slew-limit, tranching, leaky-bucket, s-S-inventory, cppi-floor, ideal-free, derating | Ecology, systems biology, information theory, reliability, control, queueing, OR, actuarial science, engineering | dead (overlap, not tested) | - | wide-16 step 1: each is a tested book change in other words (blend with hold, Kelly / soft signal, constant scale, breadth, class slots, vol target, ensemble-tsmom, trend-age / confirm2, eu-3 order budgets, drawdown-control, patch-leaving). Table in `wide-16.md`. |
| xs-century-1 | Long-short multi-asset style premia (value / momentum / carry: HML, UMD, 10 govt bonds, 9 currencies), alpha form vs `tsmom12` over a century (power-map-1 row C2) | dead (tested; informational, needs B7) | [card](cards/xs-century-1.md) | 1928-07..2025-10, alpha vs `tsmom12` on the US market: IR +0.31, z 2.75 after published costs (bar 4.70); gross IR +0.88, z 7.4; with the cheaper published momentum cost z 4.44; since 1994 IR +0.19 (z 0.75). Reading: large gross edge in-sample (on the data HML and UMD were found on, so gross rows cannot decide); net fails the bar; momentum costs decide it. [result](xs-century-1.md) |
